# Public topic sharing — #40

**Status:** verified on test1 2026-08-01 (`fda0876`) — prod deploy pending
**Lane:** Product / frontend + API — *letting a finished topic leave the account that made it*
**Depends on:** #24 (topic ownership), #16 (SignalGather UI), #22 (refresh scheduler)

## Problem

A topic is worth something to more people than the account that created it, but
until now the only way to show someone a report was to be signed in as its
owner. Everything under `/v1/topics/*` is owner-scoped by design (#24), and the
UI has no route that renders without a session.

The obvious way to fix that — loosen the topic API for unauthenticated readers —
is exactly the failure this repo already had once. On 2026-07-27 a blank
`CLAUDE_AGENT_API_KEY` turned every anonymous caller into the service principal
and `GET /v1/topics` answered strangers with all six topics (`1672fe9`). Sharing
must therefore be *narrower* than "let anonymous read", not looser.

The second constraint is money. Every action on a topic — proceed, refresh,
monitor — starts a Claude run and bills us. A shared topic is reachable by
people we have no relationship with, so the guarantee has to be that no
anonymous request can cause a run **at all**, not that we check permissions
carefully before starting one.

## Solution

Publishing marks a **finished** topic world-readable and **freezes** it.

### 1. One flag, checked in the query

`topics.is_public` (NOT NULL, default false) plus `published_at`. Every public
handler loads its row through `_published()`, which puts `is_public` in the
`WHERE` clause — there is no point in the request where an unpublished row is in
hand and a forgotten `if` would leak it. A private topic 404s exactly like a
nonexistent one.

### 2. A separate, GET-only router

`/v1/public/topics/*` (`apps/claude_agent/topics/public_routes.py`) has **no
auth dependency and no write handler**. An anonymous caller cannot start a run
because there is no route that starts one — the safety is structural, not a
check. `tests/topics/test_public_sharing.py` walks the router's own route table
and fails the build if a non-GET route ever appears on it.

Deliberately **not** exposed publicly:

| Omitted | Why |
|---|---|
| SSE `/events` | Frozen topic ⇒ nothing to stream; an unauthenticated long-poll holding a DB-polling connection is a resource tap for no benefit |
| `owner_user_id`, run ids, `error` | The research is shared, not the plumbing or the person |
| Anything non-GET | See above |

### 3. Frozen while published

`_mutable()` wraps `_owned()` and answers **409** for proceed, cancel, subscribe,
monitor (POST/PATCH/DELETE) and refresh while `is_public` is set. This applies to
the owner too: what was shared is the state at the moment of sharing, and
`available_actions` goes empty so the UI offers nothing that would be refused.

Publishing also **pauses monitoring** and clears its schedule, and two further
guards make "a shared topic never spends" true regardless of ordering:

- `claim_due_subscriptions` excludes published topics in the due-query;
- `run_refresh` bails out with `refresh.skipped {reason: topic_published}`
  before taking the lock, so a refresh queued *before* the topic was shared
  still does not run;
- publishing is **refused with 409 while a cycle is already running**
  (`refresh_locked`), because that cycle would finish after the share and
  rewrite the snapshot readers were handed.

Unpublishing is the one write a published topic accepts; monitoring stays paused
afterwards, because turning spending back on should be an explicit choice.

### 4. UI

`/app/shared` and `/app/shared/<id>` render without a session — the only routes
that do. They read through `lib/publicApi.ts`, a separate client that never
attaches the user's token and has no write call in it, so a shared page is the
same page for a signed-in reader and a stranger.

## Artifacts

| Path | What |
|---|---|
| `database/migrations/versions/0007_topic_public.py` | `is_public`, `published_at`, partial index |
| `apps/claude_agent/topics/public_routes.py` | Anonymous GET-only router |
| `apps/claude_agent/topics/serving.py` | Artifact path/response helper shared by both routers |
| `apps/claude_agent/topics/routes.py` | `publish_topic`, `unpublish_topic`, `_mutable`, `_share_payload` |
| `apps/claude_agent/topics/{scheduler,refresh}.py` | Published topics excluded from refresh |
| `apps/signalgather_web/src/lib/publicApi.ts` | Token-free read client + `shareUrl()` |
| `apps/signalgather_web/src/lib/usePublicTopic.ts` | One-shot loader (no stream, no polling) |
| `apps/signalgather_web/src/components/SharePanel.tsx` | Publish/unpublish + link, `PublishedBanner` |
| `apps/signalgather_web/src/pages/PublicTopic{,List}Page.tsx` | Reader-facing pages |
| `tests/topics/test_public_sharing.py` | 25 cases — freeze, visibility, GET-only, no spend |

## Usage

```bash
# Owner publishes a reported topic
curl -X POST -H "Authorization: Bearer $JWT" \
  https://agent.particletico.com/v1/topics/$TOPIC/publish
# -> {"is_public":true,"published_at":"…","public_path":"/v1/public/topics/…",
#     "monitoring_paused":true}

# Anyone, no credentials at all
curl https://agent.particletico.com/v1/public/topics
curl https://agent.particletico.com/v1/public/topics/$TOPIC/report.md

# Frozen while shared
curl -X POST -H "Authorization: Bearer $JWT" \
  https://agent.particletico.com/v1/topics/$TOPIC/refresh
# -> 409 {"detail":"topic is published and read-only; unpublish it first"}

# Owner takes it back
curl -X DELETE -H "Authorization: Bearer $JWT" \
  https://agent.particletico.com/v1/topics/$TOPIC/publish
```

Human link: `https://agent.particletico.com/app/shared/<topic-id>`.

## Acceptance criteria

- [x] Owner can publish a `reported` topic; other states answer 409
- [x] Published topics are readable with **no credentials**, private ones 404
- [x] Public router exposes GET only — asserted over its route table
- [x] Public payload omits owner, run ids and internal error text
- [x] Every mutating owner route answers 409 while published
- [x] Publishing pauses monitoring; scheduler and `run_refresh` both skip published topics
- [x] Publishing is refused while a refresh cycle is in flight
- [x] Unpublish restores control and kills the link
- [x] `/app/shared/*` renders with no session; no action control anywhere on it
- [x] `pytest tests/topics` (113) and `vitest` (211) green; tsc + eslint clean
- [x] Migration `0007_topic_public` applied on **test1** (`0006_topic_owner` → `0007_topic_public (head)`)
- [ ] Migration applied on **prod**
- [ ] Verified in a browser: publish → open the link in a logged-out window → unpublish → link 404s

## Verified on test1 — 2026-08-01

Slot `agent-test1.particletico.com`, branch `feat/public-topic-sharing-40`
(`fda0876`), images rebuilt, migration applied, containers healthy, no errors in
the boot log. Live results against topic `9f2607da`:

| Check | Result |
|---|---|
| Anonymous `GET /v1/topics` | **401** — owner API still closed |
| Anonymous `GET /v1/public/topics` | **200**, lists only the published topic |
| Anonymous `POST/PUT/PATCH/DELETE /v1/public/topics` | **405** on all four |
| Anonymous `GET .../{detail,report,report.md,news,parsed,intro.md,deltas}` | **200** — report body readable with no credentials |
| Public payload | no `owner_user_id`, no run ids, no `error` |
| `POST /refresh`, `/proceed`, `/cancel`, `/monitor` **with a valid service key** | **409** `topic is published and read-only` |
| `available_actions` while published | `[]` |
| After `DELETE /publish` | detail + artifacts **404**, listing empty, owner regains control |
| `/app`, `/app/shared`, `/app/shared/<id>` | **200** |

Left published on test1 for the browser pass:
`https://agent-test1.particletico.com/app/shared/9f2607da-4a94-494d-83bc-2af3ad9a8842`

**Unrelated pre-existing issue seen at boot:** test1's
`CLAUDE_AGENT_ALLOWED_COMMANDS` still lacks `/newsfind-topic-parse`, so #38's
grounding leg degrades on that slot (prod got it in `1672fe9`). Not touched here.

## Known gaps

- **Discovery is a substring match** (`ILIKE %q%`) over published topics. Fine at
  pilot scale; it is not an index and will not stay fine at thousands of rows.
- **Publishing is all-or-nothing.** There is no partial share (report but not
  sources) and no expiring or unguessable link — a published topic is listed
  publicly by design ("everyone can find this topic").
- **Republishing after unpublish** issues the same URL, so an old link starts
  working again. If that is wrong for the product, the fix is a share token
  rather than the topic id in the path.
- `_warn_on_open_topic_api` in `app.py` still covers the *owner* API only; that
  guard is unchanged and unaffected by this feature.

## Related

- `docs/specs/done/topic_user_ownership_24.md` — the ownership model this scopes against
- `docs/specs/active/signalgather_frontend_v1_16.md` — UI this extends
- `docs/specs/done/topic_refresh_scheduler_22.md` — the scheduler that must skip published topics
- Incident: commit `1672fe9` — why anonymous read is opt-in per row, not a config flag
