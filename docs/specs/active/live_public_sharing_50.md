# Live public sharing — #50

**Status:** implemented 2026-09-01 — awaiting migration + deploy
**Lane:** Product / API + frontend — *a shared report that keeps up with its topic*
**Depends on:** #40 (public topic sharing), #24 (topic ownership), #22 (refresh scheduler), #16 (SignalGather UI)
**Blocks / feeds:** #37 (pilot first-use) — a link handed to a prospect is the cheapest demo we have
**Supersedes:** the *freeze* half of #40. The anonymous-read design of #40 (per-row opt-in, GET-only router, narrow payload) is kept intact and is not reopened.

## Problem

#40 made a topic shareable by making it **dead**. Publishing sets `is_public`,
and from that moment `_mutable()` answers 409 to proceed, cancel, subscribe,
monitor and refresh — for the owner too — monitoring is paused, its schedule is
cleared, and both the scheduler's due-query and `run_refresh` skip the row. What
a reader gets is the state at the instant of sharing, forever, until the owner
takes the link down.

That is the wrong trade for the product. A topic's value is that it is *being
watched*: the report is a standing answer that monitoring keeps current. Freezing
it to share it means the moment a report becomes worth showing to someone, it
stops being worth reading. In practice the owner faces a choice nobody should
have to make — keep the topic alive, or let anyone see it.

The requirement is the opposite of a handover:

> A report can be exposed publicly, **read-only**, while staying **active** and
> **owned**. The owner keeps every control — settings, monitoring, refresh — and
> the public view is a presentation surface that shows the fully updated state,
> not a snapshot taken at share time.

Two things must not be lost while unfreezing:

1. **No anonymous request may cause a Claude run.** This was #40's real
   guarantee, and it never depended on the freeze — it comes from the shape of
   `public_routes.py` (GET handlers only, no write route to reach). It stays
   exactly as it is.
2. **A reader must never see a half-written state.** Freezing gave read
   consistency for free: nothing could change under a reader. Once the topic
   moves while it is being read, consistency has to be built rather than
   assumed — see scope item 4, which is the substance of this ticket.

The snapshot behaviour is still legitimate for one case — "here is the picture as
of the day we signed" — so it survives as an explicit mode rather than as the
only mode.

## Core question

Can an owner publish a topic, keep refreshing and monitoring it, and have a
stranger's open tab show the newest completed cycle — while no anonymous request
can ever start a run and no reader can ever load a run that is still in flight?

## Scope

### 1. `share_mode` — the owner picks what "shared" means

Migration `0013_topic_share_mode` adds to `topics`:

| Column | Type | Meaning |
|---|---|---|
| `share_mode` | `VARCHAR(16) NOT NULL DEFAULT 'live'` | `live` = public view follows the topic; `frozen` = #40 behaviour |
| `public_deliver_run_id` | `VARCHAR(64) NULL` | The deliver run the **public** view reads — see item 4 |
| `public_updated_at` | `TIMESTAMPTZ NULL` | When the public view last advanced; the poll stamp |
| `frozen_at` | `TIMESTAMPTZ NULL` | When a share was pinned — the date a snapshot reader is shown |

A `CHECK (share_mode IN ('live','frozen'))` goes with them: the mode decides
whether the owner is locked out of their own topic, which is not a thing to
leave to a typo.

Backfill, in the same migration:

```sql
UPDATE topics SET share_mode = 'frozen', frozen_at = published_at WHERE is_public;  -- keep the promise made to existing links
UPDATE topics SET public_deliver_run_id = deliver_run_id WHERE state = 'reported';
UPDATE topics SET public_updated_at = updated_at WHERE is_public;
```

Anything already published was published under freeze semantics; it stays frozen
until its owner says otherwise. (Prod has nothing published — this matters on
test1, where `9f2607da` is live.)

`is_public` remains the **only** predicate the anonymous router consults.
`share_mode` never widens visibility; it decides which state the public view
resolves to and whether owner writes are refused. Keeping the two apart means the
#40 leak analysis still holds unchanged: one boolean, in the `WHERE` clause.

### 2. The freeze becomes mode-scoped, not publish-scoped

| Site | Today (#40) | After |
|---|---|---|
| `routes._mutable()` | 409 while `is_public` | 409 while `is_public AND share_mode='frozen'` |
| `routes._actions()` | `[]` while `is_public` | normal actions while live; `[]` while frozen |
| `publish_topic` | pauses monitoring, clears schedule | **live:** touches neither. **frozen:** #40 behaviour |
| `publish_topic` while `refresh_locked` | 409 `refresh_locked` | **live:** allowed. **frozen:** 409, unchanged — a cycle finishing after the freeze would rewrite the snapshot |
| `refresh.run_refresh()` | `refresh.skipped {reason: topic_published}` | skips only frozen topics; reason value becomes `topic_frozen` |
| `scheduler.claim_due_subscriptions()` | excludes `is_public` rows | excludes `share_mode='frozen'` rows |
| `unpublish_topic` | monitoring stays paused | **live:** nothing was paused, nothing to restore. **frozen:** unchanged |

The guarantee those last two lines carry over from #40 is worth restating in its
new form, because it is narrower and must be written down as such:

> A **frozen** shared topic can never spend. A **live** shared topic spends only
> what its owner's own monitoring settings spend — the same cost it would incur
> unshared. Publishing changes no cost, in either mode, and **no anonymous
> request contributes to either**.

### 3. Mode is chosen at publish and changeable while shared

```
POST   /v1/topics/{id}/publish   {"mode": "live"}   # default when the body is omitted
PATCH  /v1/topics/{id}/publish   {"mode": "frozen"} # switch while shared
DELETE /v1/topics/{id}/publish                      # unchanged — link dies immediately
```

- `POST` stays idempotent: publishing an already-published topic keeps
  `published_at` and returns `already_published` with the current mode. It does
  **not** silently change the mode — that is what `PATCH` is for.
- `live → frozen` pins the current state: pauses monitoring, clears the schedule,
  stamps `frozen_at`, and is refused with 409 while a refresh cycle is in flight
  (the #40 reason, in the only place it still applies). No copying is needed —
  the pointer of item 4 simply stops advancing.
- `frozen → live` hands control back but does **not** resume monitoring. Turning
  spending back on stays an explicit choice, exactly as #40 argued for unpublish.
- Events: `topic.published` payload carries `share_mode`; new
  `topic.share_mode_changed {from, to, monitoring_paused}`.

### 4. Consistent public reads — resolve through completed work only

This is the part the freeze was doing for us, and the part that must now be
explicit. Two hazards, one rule.

**Hazard A — `deliver_run_id` points at a run before that run has written
anything.** `run_deliver` sets `row.deliver_run_id` and *then* starts the Claude
run (`pipeline.py:240`). Today no path re-delivers a `reported` topic, so this is
latent; the moment a live shared topic can be re-run, every public artifact route
404s for the length of the run and a failed run leaves the link permanently
broken.

**Hazard B — a refresh delta row exists from the moment the cycle starts.**
`run_refresh` inserts `TopicRefreshDelta(status="running")` up front, so
`list_deltas` would advertise cycle *n+1* to the public listing minutes before
its `report.md` exists.

**Rule: the public view only ever resolves state that has finished.**

- Public artifacts read `public_deliver_run_id`, never `deliver_run_id`. A single
  helper advances the pointer — and stamps `public_updated_at` — at exactly two
  places: successful completion of `run_deliver`, and successful completion of a
  refresh cycle. Failure advances nothing, so a broken run cannot blank a shared
  report; the previous good state stays up.
- `list_public_deltas` and the per-delta artifact routes filter
  `status = 'completed'`. A running or failed cycle is invisible publicly.
- The owner's routes are untouched and keep reading `deliver_run_id`: the owner
  *should* see work in flight.

Net effect: a live public report advances atomically at cycle boundaries. A
reader mid-cycle sees the previous complete state, never a partial one, and never
a 404 on a link that worked a minute ago.

`plan_run_id` (intro, parsed) is left as-is: it is written once at creation and
no path rewrites it for a `reported` topic. If re-planning is ever added, it
needs the same pointer treatment — noted in Known gaps.

### 5. Public payload — enough for a reader to trust the freshness

`public_routes._payload()` gains, alongside today's fields:

```jsonc
{
  "share_mode": "live",
  "read_only": true,                  // unchanged: true in both modes
  "frozen_at": null,                  // set in frozen mode
  "updates": {
    "live": true,                     // this page will keep changing
    "last_updated_at": "2026-09-01T…",// public_updated_at
    "update_count": 7,                // completed cycles
    "latest_seq": 7
  }
}
```

Still deliberately **not** public, extending the #40 table:

| Omitted | Why |
|---|---|
| `next_refresh_at`, `schedule_interval_hours` | The cadence is an owner setting and a spend decision, not a finding. "Updated 2 hours ago" answers the reader's actual question |
| Running / failed cycles | See item 4 — an in-flight state is not a shared state |
| `owner_user_id`, run ids, `error` | Unchanged from #40 |
| SSE `/events` | Unchanged from #40 — no unauthenticated long-poll. Item 6 is the alternative |

`GET /v1/public/topics/{id}` answers `Cache-Control: public, max-age=30`;
artifact routes keep `FileResponse`'s `ETag`/`Last-Modified`, so a poll that
re-fetches an unchanged `report.md` costs a 304.

### 6. The public page shows the update, without holding a connection

`usePublicTopic` today is documented as "fetch, then stop — no stream, no
polling, no retry timer running in a stranger's tab", which was correct when the
topic could not change. It becomes:

- poll `GET /v1/public/topics/{id}` every **60 s**, only when
  `share_mode === 'live'`;
- only while `document.visibilityState === 'visible'` — a backgrounded tab costs
  nothing, and resumes on focus with an immediate poll;
- compare the stamp (`updates.last_updated_at`, `updates.latest_seq`, `state`);
  re-fetch artifacts **only** when it moves;
- back off (60 s → 5 min) after consecutive failures, and never poll a frozen
  topic — its hook keeps today's fetch-once behaviour.

This stays inside #40's rule against anonymous long-polls: these are short cached
GETs against one indexed row, not a held DB-polling connection per reader.

Presentation:

- `PublicTopicPage` header: **Live · updated 2 hours ago** with a dot, or
  **Snapshot · as of 12 Aug 2026** in frozen mode.
- New cycles arriving while the page is open are surfaced ("2 updates since you
  opened this"), not swapped in silently.
- `PublicTopicListPage` shows mode + last-updated per row.
- No action control anywhere on the public pages — unchanged, and asserted.

### 7. Owner-side controls

- `SharePanel`: mode selector at publish time (Live / Snapshot, live default,
  each with one line on what it means), mode switch while shared, and the copy
  rewritten — the current text promises a freeze in five places.
- `PublishedBanner`: live → "Shared publicly — readers see this report as it
  updates. You keep full control."; frozen → today's wording.
- Monitoring, refresh and settings panels **stay enabled** while live-published;
  they currently explain the freeze.

### 8. Tests

`tests/topics/test_public_sharing.py` keeps its route-table assertion (a non-GET
route on the public router still fails the build) and gains the live-mode axis:

| Case | Expectation |
|---|---|
| Owner refresh / monitor / cancel while **live**-published | allowed |
| Same while **frozen** | 409, unchanged |
| Scheduler due-query | claims live-published, skips frozen |
| `run_refresh` on a frozen topic | `refresh.skipped {reason: topic_frozen}` |
| Cycle in `running` | absent from public deltas; `/deltas/{seq}` 404s |
| Cycle completed | appears; `public_updated_at` advanced |
| Failed deliver on a live shared topic | previous report still served |
| Publish default mode | `live` |
| `PATCH` live → frozen | monitoring paused; 409 while `refresh_locked` |
| `PATCH` frozen → live | control returns; monitoring stays paused |
| Unpublish from live | monitoring keeps running |
| `available_actions` while live-published | non-empty |
| Public payload | still no `owner_user_id`, run ids, `error` |

Frontend (`vitest`): polling fires only in live mode, only while visible, and
re-fetches artifacts only on a stamp change; frozen renders with no timer.

## Out of scope

- **Unlisted / tokenised links** — a live shared topic is still reachable at
  `/app/shared/<topic-id>` and still listed on the public index. The share-token
  idea stays a #40 known gap; this ticket does not touch link identity.
- **Partial sharing** (report but not sources) — #40 gap, unchanged.
- **Editing report text.** "Owner can edit" here means the owner keeps every
  control the pipeline gives them (refresh, monitoring, settings). A report body
  editor is not part of this ticket and has no ticket yet.
- **Anonymous SSE / websockets** — item 6 is the deliberate alternative.
- **Reader-facing extras** (comments, subscribe-to-updates, email digests) — no
  ticket; would need an anonymous write path, which is exactly what #40 forbids.
- **#34** topic ops table, **#37** first-use UX — adjacent surfaces, separate tickets.

## Acceptance criteria

- [x] Migration `0013_topic_share_mode` adds the four columns and backfills existing published rows to `frozen`
- [x] `POST /publish` defaults to `live`; `PATCH /publish` switches mode both ways; `DELETE` unchanged
- [x] A **live**-published topic accepts every owner action it would accept unshared, and `available_actions` is non-empty
- [x] A **frozen**-published topic behaves exactly as #40 shipped it
- [x] Scheduler and `run_refresh` skip frozen topics only; a live shared topic refreshes on schedule
- [x] Public artifact routes resolve `public_deliver_run_id`; an in-flight or failed run is never served
- [x] Running / failed refresh cycles are invisible on the public router; completed ones appear and advance `public_updated_at`
- [x] Public payload carries `share_mode` + `updates`, and still omits owner id, run ids, error, and the refresh schedule
- [x] Public router is still GET-only — asserted over its route table
- [x] Anonymous requests still cannot cause a run: no public route reaches `run_deliver`, `run_refresh` or the scheduler
- [x] `/app/shared/<id>` updates itself within ~60 s of a completed cycle, without a session and without a held connection; a hidden tab polls not at all
- [x] Share panel lets the owner pick and change the mode; no copy in the UI promises a freeze in live mode
- [x] `pytest tests/topics` and `vitest` green; `tsc` + `eslint` clean
- [ ] Verified in a browser: publish live → refresh the topic as owner → the logged-out tab picks the new cycle up → switch to snapshot → it stops moving → unpublish → 404

## Artifacts

| Path | What |
|---|---|
| `database/migrations/versions/0013_topic_share_mode.py` | `share_mode`, `public_deliver_run_id`, `public_updated_at`, `frozen_at`, check constraint, backfill |
| `apps/claude_agent/topics/models.py` | The columns, `SHARE_LIVE`/`SHARE_FROZEN`, and `is_frozen(row)` — the one predicate that means "pinned" |
| `apps/claude_agent/topics/routes.py` | `ShareBody`, mode-aware `_mutable`/`_actions`, `publish_topic(mode)`, `set_share_mode` (PATCH), `_pin` |
| `apps/claude_agent/topics/serving.py` | `advance_public_view()` — the only place the public pointer and stamp move |
| `apps/claude_agent/topics/pipeline.py` | Advances the pointer after `run_deliver` has actually written its files |
| `apps/claude_agent/topics/refresh.py` | `_is_frozen`, `refresh.skipped {reason: topic_frozen}`, `list_deltas(statuses=…)`, stamp on a completed cycle |
| `apps/claude_agent/topics/scheduler.py` | Due-query excludes `share_mode='frozen'`, not every share |
| `apps/claude_agent/topics/public_routes.py` | `share_mode` + `updates` in the payload, artifacts via `public_deliver_run_id`, completed-only deltas, `Cache-Control` |
| `apps/signalgather_web/src/lib/usePublicTopic.ts` | Visibility-gated 60 s poll with a stamp comparison and backoff; frozen shares still fetch once |
| `apps/signalgather_web/src/components/SharePanel.tsx` | Mode choice at publish, pin/unpin while shared, `PublishedBanner` per mode |
| `apps/signalgather_web/src/pages/PublicTopic{,List}Page.tsx` | Live/Snapshot badge, "updated N ago", "N updates since you opened this" |
| `apps/signalgather_web/src/components/{PlanReview,monitor/MonitorPanel}.tsx`, `pages/TopicListPage.tsx` | Owner-side copy: only a *pinned* share explains a lockout |
| `tests/topics/test_public_sharing.py` | 50 cases — both modes, mode switching, pointer, completed-only reads |
| `apps/signalgather_web/src/lib/usePublicTopic.test.tsx` | 5 cases — polls, does not re-download unchanged research, silent on frozen and hidden tabs |

## Usage

```bash
# Live by default: the link keeps up, the owner keeps control
curl -X POST -H "Authorization: Bearer $JWT" -H 'Content-Type: application/json' \
  -d '{"mode":"live"}' https://agent.particletico.com/v1/topics/$TOPIC/publish

# Still refreshable while shared — this used to answer 409
curl -X POST -H "Authorization: Bearer $JWT" \
  https://agent.particletico.com/v1/topics/$TOPIC/refresh

# What a reader sees: mode + freshness, no schedule, no plumbing
curl https://agent.particletico.com/v1/public/topics/$TOPIC
# -> {"read_only":true,"share_mode":"live",
#     "updates":{"live":true,"last_updated_at":"…","update_count":3,"latest_seq":3}, …}

# Pin it when the link must stop moving; switch back when it should not
curl -X PATCH -H "Authorization: Bearer $JWT" -H 'Content-Type: application/json' \
  -d '{"mode":"frozen"}' https://agent.particletico.com/v1/topics/$TOPIC/publish
```

## Verification so far

`pytest tests` **362 passed** (50 in `test_public_sharing.py`), `vitest` **239
passed** across 22 files, `tsc --noEmit` clean, `eslint src --max-warnings 0`
clean. Ruff clean on the files touched; the pre-existing `UP017`/`I001` findings
in this package are unchanged and not from this work.

**Not yet done:** migration applied on test1 or prod, and the browser pass —
publish live, refresh as owner, watch a logged-out tab pick the cycle up, pin,
watch it stop, unpublish, link 404s.

## Known gaps this ticket accepts

- **Cycle-granular freshness.** "Updated" advances when a cycle completes, not while it runs. A reader watching during a 10-minute refresh sees the previous state — intended, and the only thing that keeps public reads consistent.
- **Polling, not push.** Up to 60 s of staleness in an open tab, by design; SSE for anonymous readers stays refused.
- **Re-planning would need the same pointer.** `plan_run_id` is written before the plan run produces `parsed.json` / `intro.md`. Safe only because a `reported` topic cannot re-plan today.
- **Discovery is still `ILIKE %q%`** over published topics (#40 gap), and republishing still revives an old URL (#40 gap) — untouched here.
- **The public listing is still all-or-nothing**: publishing live means listed publicly.

## Related

- `docs/specs/done/public_topic_sharing_40.md` — the sharing model this changes; its anonymous-read design is kept whole
- `docs/specs/done/topic_user_ownership_24.md` — the ownership scoping the public router sits outside of
- `docs/specs/active/topic_refresh_scheduler_22.md` — the scheduler whose due-query changes here
- `docs/specs/active/signalgather_frontend_v1_16.md` — the UI surface; `testing/ui_smoke_16.md` §7e is the logged-out browser pass
- `docs/specs/active/pilot_first_use_experience_37.md` — a live link is the first thing a prospect sees
- Incident `1672fe9` (2026-07-27) — why anonymous read stays per-row opt-in, and why `is_public` alone gates the public router
