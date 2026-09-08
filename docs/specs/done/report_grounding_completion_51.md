# Report grounding — everything we already hold reaches the analyst (#51)

**Status:** done (2026-09-09) — implemented and green offline; **not yet run on a slot**,
see *Verified on a slot* below
**Lane:** Product / quality — *what the report is written from*
**Depends on:** #42 (evidence store + content fetcher), #45 (feeds channel), #38 (facets), #39 (source authority)
**Blocks:** a credible second India run (#45); any claim that the corpus improves output
**Related:** #46 (per-query yield — the search side of the same loop), #47 (routing — what search reaches), #48 (corpus seeding), #49 (discovery lane), #23/#41 (measurement)

---

## Why this exists

The system acquires far more than it uses. Four separate mechanisms collect material for a
topic — the search evidence store (#42), the RAG corpus (#10/#30), official data feeds
(#45), and the plan leg's own retrieval — and the leg that writes the report a customer
reads consumes almost none of it.

Measured on the code at `a556826`:

| Held for the topic | Reaches the deliver leg |
|---|---|
| Full text of every fetched document (~89 % read rate, ~16k chars each) | **No** — `export_evidence` is called only from `run_refresh` |
| The plan leg's RAG context (`rag_context_refs`, `current_state`) | **No** — `newsfind-deliver.md:79` says "drop everything else" |
| Spreadsheets returned by search | **No** — recorded `unsupported`; the converter exists and is unused |
| Official data feeds | Yes, since 2026-09-05 — and silently zero when facets degrade |

So the foundational report — the first and most-read artefact, the one the India run
produced on 2026-09-03 — is written from search snippets of one or two sentences, plus
whichever feeds happened to match. Every downstream quality argument (#39 source authority,
#46 onboarding, #45 India) rests on an analyst that cannot see most of what was collected
for it.

This ticket does not acquire anything new. It connects what four shipped tickets already
built, and finishes each connection to production standard.

## Core question

*After a deliver run, can it be shown from the run's own artefacts that the analyst had the
full text of the documents we fetched, the corpus context the plan retrieved, and every
official series that applies to the topic — and that a claim resting on any of them cites
it?*

## Scope

### 1. The captured corpus reaches the deliver leg

`run_deliver` exports the topic's readable documents the way `run_refresh` already does, and
`newsfind-deliver.md` reads them before searching.

- Call `export_evidence` in `run_deliver`, gated on `settings.refresh_evidence_max_documents`
  as refresh is, and wrap it so a corpus failure cannot cost the report (`run_refresh` is the
  reference implementation).
- Add `evidence_dir`, `evidence_count`, `evidence_unreadable_count` to the deliver
  `input.json`.
- Add the corpus section to `newsfind-deliver.md`, matching the refresh command's contract:
  read `evidence_dir/index.json` first, prefer a corpus file over `WebFetch` for a URL we
  already read, and treat the unreadable count as a coverage fact rather than silence.
- Rename `refresh_evidence_max_documents` to `evidence_max_documents` with the old name
  accepted as an alias, since it now governs both legs.

**Why the deliver leg needs it more than refresh does.** Refresh reports a delta against a
report that already exists; deliver establishes the baseline every later cycle is judged
against. A thin baseline propagates.

### 2. The plan leg's retrieval reaches the report

- Extend the deliver keep-list in `newsfind-deliver.md` Phase 0 to include `current_state`
  and `rag_context_refs`, and state how they are used: as background that shapes
  interpretation, never as a citable source in place of a retrieved document.
- Corpus material carries `source_id`; the report must not present it as a web source. If a
  RAG-derived claim has no web or feed citation, it is background, and the existing
  no-fabrication rule applies unchanged.

### 3. Spreadsheets become readable in the search path

- Add a spreadsheet branch to `search_content.py` beside the PDF branch, using
  `source_ingest.text_extract.xlsx_bytes_to_text`, and add the spreadsheet media types to the
  request `Accept` header.
- Record the outcome as `fetched` when extraction succeeds; keep `unsupported` for formats
  with no converter, and keep `.xls` (pre-2007 OLE) explicitly unsupported with its reason,
  as `source_crawler` already does.
- The converter, its `openpyxl` dependency and its tests already exist — this is a
  connection, not an implementation.

### 4. Feed freshness is visible and cannot fail silently

- `export_feeds` records each feed's `collected_at` age in the index it writes and in the
  entry it returns.
- A feed older than a configurable threshold (`feeds_max_age_days`, default 45 — PPAC is
  monthly) is still exported, and is marked stale in the index and in the file's front
  matter, so the analyst can qualify a figure rather than quote it as current.
- A run that matched no feeds while feeds were available logs a warning naming the topic's
  facets, which is the difference between "no feed applies" and "the topic has no facets".

### 5. Degraded facets cannot silently remove the feed channel

`fallback_facets` sets `commodity` and `geo` to `[]`, and `feeds.matches` returns `False`
for a topic with neither, so a parse-leg failure removes every official series from the run
with no error. #38 designed that degradation to be quiet when it only affected source
discovery; it now gates data the report depends on.

- When facets are degraded, `run_deliver` and `run_refresh` emit the fact on the stage event
  and log it at warning level.
- The feed selection rule itself does not change: handing every feed to a topic with no
  facets is the leak case `tests/topics/test_feeds.py` exists to prevent.

**Correction found on implementation.** "Degraded" was the wrong thing to key on, and
keying on it alone would have shipped a signal that never fires. `run_topic_parse` writes
the facets cache **only when the parse leg succeeds**, so a `fallback_facets` result is
never persisted — a degraded parse reaches the deliver and refresh legs as a *missing*
cache, not as a flag. Separately, a parse that succeeds but names neither a commodity nor a
region is not flagged at all, and blinds the feed channel just as completely, because that
is the exact condition `feeds.matches` refuses on.

`facets.feed_selection_blind()` therefore answers the question the legs actually need —
*can this topic reach a feed at all, and if not why* — over all three cases. The event field
keeps the name `facets_degraded` (item 6). `load_cached_facets` was also carrying the
`degraded` flag out of a round trip through `normalize_facets`, which validates the *agent's*
output and rightly ignores a `degraded` key there; the cache is our own file, so its flag now
survives.

### 6. The run says what the analyst was given

- `stage.finished` for `deliver`, and `refresh.completed`, carry `evidence_count`,
  `evidence_unreadable_count`, `feeds_count` and `facets_degraded`.
- These are the counters the acceptance criteria below are read from, and the reason a future
  run can be compared with this one without opening the state directory.

### 7. One definition of the source mix

`topics/source_quality.py` counts a source authoritative when its class is
`primary_official`/`data_feed` **or** its host is on the register; `src/lib/sourceQuality.ts`
counts the class only, and the frontend never reads the `source_mix` the backend emits. The
figure a customer reads is therefore not the figure the system measured.

- Decide the definition once, in the backend, and record the decision in this spec on
  implementation.
- `SourceMixNote` renders the emitted `source_mix` payload; the duplicate frontend
  computation is deleted, with a fallback to local computation only where no payload exists
  (artefacts written before this change).

**Decision, on implementation (2026-09-09): the backend definition wins, unchanged.** A
source is authoritative when its `source_class` is `primary_official` / `data_feed` **or**
its host is on the register. The two halves are not redundant — the class is the analyst's
judgement about what a document is, the register is our own standing decision about who
publishes it, and a ministry page the analyst classed `unknown` is still a ministry page.
The frontend cannot hold this definition even in principle: the register is a server-side
file and is not shipped to the browser, which is why the narrower version was the one that
existed there.

**How it reaches the UI: a file, not the event.** `source_mix` is still emitted on
`report.ready` / `refresh.completed`, but an event is a moment and a reader arrives later —
and a public reader gets no event stream at all, by design (`public_routes` docstring). So
the run also writes `source_mix.json` into its own directory, served by
`GET /{id}/source-mix` and `GET /{id}/deltas/{seq}/source-mix` on **both** the owner and the
public router. A run written before this change 404s there, and only that case falls back to
the class-only count, now a labelled helper inside `SourceMixNote.tsx`.

### 8. The monitoring plan becomes editable

The plan is written once at `POST /monitor` and never regenerated, and `PATCH /monitor`
cannot change it, so no query improvement can reach a topic already under monitoring.

- `UpdateMonitorBody` accepts `short_term_queries`, validated on the same shape
  `build_short_term_queries` produces, including `allowed_domains`.
- The emitted `monitor.updated` event carries the new query count.
- This is the affordance only. Deciding *which* queries to change from measured yield is
  #46 build item 2 and stays there.

## Out of scope

| Not here | Owner |
|---|---|
| Acquiring topic education into RAG when the corpus has none | **#48** |
| Per-query yield analysis and the operator's tuning loop | **#46** build item 2 |
| The judging pass over the captured corpus | **#46** build item 4 |
| Unfiltered discovery budget, known-source polling, source promotion | **#49** |
| Domain routing and the country label on the register | **#47** |
| Raising the number of queries a plan emits | **#46** |
| Moving the LLM judge off OpenAI | **#43** |
| Whether the resulting report scores better on the rubric | **#23**, **#41** |

The boundary is deliberate: this ticket changes **what the analyst can read**, not what
search finds. Both matter, and conflating them is how a quality change becomes unattributable.

## What was delivered (2026-09-09)

Nothing here acquires anything new; every item connects something four shipped tickets had
already built.

| Scope item | Where it lives now |
|---|---|
| 1 — corpus into deliver | `pipeline.run_deliver` calls `export_evidence` and writes `evidence_dir` / `evidence_count` / `evidence_unreadable_count` into `input.json`, wrapped so a corpus failure logs and the run completes. `newsfind-deliver.md` reads the index in Phase 0 and prefers a corpus file over `WebFetch` in Phase 2 and Phase 4 |
| 1 — setting rename | `evidence_max_documents`, governing both legs; `CLAUDE_AGENT_REFRESH_EVIDENCE_MAX_DOCUMENTS` still resolves, via `AliasChoices` |
| 2 — RAG context into the report | `newsfind-deliver.md` Phase 0 keeps `current_state` and `rag_context_refs`, with the background-never-a-citation rule stated as its own paragraph |
| 3 — spreadsheets | `search_content.classify` gained a spreadsheet branch beside the PDF one; the `Accept` header asks for `.xlsx`; `.xls` is `unsupported` with its reason, in `UNCONVERTIBLE_TYPES` |
| 4 — feed freshness | `export_feeds` takes `max_age_days`, records `collected_at` / `age_days` / `stale` per feed in the index **and** the file's front matter, and warns `feeds.none_matched` naming the facets when feeds exist but none applied. `publish` stamps `collected_at`, holding the stamp while `source_sha256` is unchanged |
| 5 — degraded facets | `facets.feed_selection_blind()`; both legs log at warning level and put `facets_degraded` on the event |
| 6 — counters | `stage.finished` (deliver) via a new `finished_extra` on `_run_slash`, and `refresh.completed` |
| 7 — one source mix | `source_quality.write_source_mix` writes `source_mix.json`; four new GET routes serve it; `src/lib/sourceQuality.ts` is deleted and its class-only count survives as a labelled fallback inside `SourceMixNote.tsx` |
| 8 — editable plan | `refresh.validate_short_term_queries` + `UpdateMonitorBody.short_term_queries`; `monitor.updated` carries `queries_count` |

**Batched into the same prompt change, as the notes below required:**

- #39's `thesis_status` divergence rule, reworded to stand on its own in
  `newsfind-refresh.md` Phase R4 with the required form of the line spelled out.
- #46 build item 0's `next_queries` contract: `newsfind-deliver.md` now specifies
  `{q, intent, rationale, allowed_domains?}`, so a domain-filtered query no longer loses its
  filter on the way into the monitoring plan. The Python side (`_domains` in
  `build_short_term_queries`) already read the field; nothing produced it.

## Artifacts

| Path | What changed |
|---|---|
| `apps/claude_agent/config.py` | `evidence_max_documents` (aliased), `feeds_max_age_days` |
| `apps/claude_agent/topics/pipeline.py` | corpus export, `facets_degraded`, `finished_extra`, `source_mix.json` |
| `apps/claude_agent/topics/refresh.py` | same counters, `validate_short_term_queries` |
| `apps/claude_agent/topics/facets.py` | `feed_selection_blind`, cached `degraded` survives a round trip |
| `apps/claude_agent/topics/feeds.py` | age + staleness, `feeds.none_matched` warning, `collected_at` on publish |
| `apps/claude_agent/topics/search_content.py` | spreadsheet branch, `Accept`, `.xls` reason |
| `apps/claude_agent/topics/source_quality.py` | `write_source_mix`, the definition stated in the module docstring |
| `apps/claude_agent/topics/routes.py` | `PATCH /monitor` plan, `/source-mix` × 2 |
| `apps/claude_agent/topics/public_routes.py` | `/source-mix` × 2 |
| `claude_agent_fe/.claude/commands/newsfind-deliver.md` | corpus, RAG background, feed staleness, `next_queries` filter |
| `claude_agent_fe/.claude/commands/newsfind-refresh.md` | feed staleness, `thesis_status` divergence |
| `apps/signalgather_web/src/…` | `SourceMixPayload`, four API getters, `SourceMixNote` rewrite, `sourceQuality.ts` deleted |
| `tests/topics/test_report_grounding.py` | new — both legs, counters, corpus failure, degraded facets |
| `tests/topics/test_monitor_plan_update.py` | new — the validator and the route |
| `tests/topics/{test_feeds,test_search_content,test_topic_parse_stage,test_source_quality}.py` | freshness, `.xlsx`/`.xls`, `feed_selection_blind`, `source_mix.json` |
| `apps/signalgather_web/src/components/report/SourceMixNote.test.tsx` | new — payload and legacy fallback |

## Usage

```bash
# What a run gave the analyst, without opening the state directory.
curl -s "$API/v1/topics/$TOPIC/events?from_seq=0" -H "Authorization: Bearer $JWT" \
  | grep -E 'stage.finished|refresh.completed' \
  | jq -r 'select(.payload.evidence_count != null)
           | [.event_type, .payload.evidence_count, .payload.evidence_unreadable_count,
              .payload.feeds_count, .payload.facets_degraded] | @tsv'

# The one source-mix figure, owner and public views alike.
curl -s "$API/v1/topics/$TOPIC/source-mix" -H "Authorization: Bearer $JWT" | jq
curl -s "$API/v1/public/topics/$TOPIC/source-mix" | jq

# Change the monitoring plan of a topic already being watched (#51 item 8).
curl -s -X PATCH "$API/v1/topics/$TOPIC/monitor" -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" -d '{
    "short_term_queries": [
      {"query": "PPAC monthly natural gas balance",
       "priority": 1, "allowed_domains": ["ppac.gov.in"]}
    ]
  }' | jq '.queries_count'

# What the deliver run was handed, on disk.
jq '{evidence_count, evidence_unreadable_count, feeds_count}' \
  "$STATE/news/$HASH/runs/$DELIVER_RUN/input.json"
jq '.feeds[] | {source_id, age_days, stale}' \
  "$STATE/news/$HASH/runs/$DELIVER_RUN/feeds/index.json"
```

Env, both optional:

| Var | Default | What it does |
|---|---|---|
| `CLAUDE_AGENT_EVIDENCE_MAX_DOCUMENTS` | 200 | Documents exported into a deliver *or* refresh run dir. `0` disables. The old `CLAUDE_AGENT_REFRESH_EVIDENCE_MAX_DOCUMENTS` still works |
| `CLAUDE_AGENT_FEEDS_MAX_AGE_DAYS` | 45 | Above this a feed is exported and marked stale, never withheld |

## Known gaps

- **Not run on a slot.** Everything below *Verified on a slot* is still open; the offline
  suite proves the wiring, not that a live analyst uses it.
- **The `thesis_status` divergence rule is reworded, not verified.** #39 could not verify it
  without a live cycle and neither can this.
- **`search_content` reads `.xlsx` from the response's declared media type only.** A server
  that returns a workbook as `application/octet-stream` is still `unsupported`. Sniffing the
  ZIP magic would misread every other zip, so the extension is the missing signal and it is
  not in `SearchDocument` today.
- **Deliver's corpus is the whole topic's corpus, newest first, capped.** It is not scoped to
  this run's queries, which is the same behaviour `run_refresh` has always had. Whether a
  relevance-scoped export is better is a judging question and belongs to #46 build item 4.

## Acceptance criteria

Implementation:

- [x] `run_deliver` exports the evidence corpus and passes `evidence_dir` /
      `evidence_count` / `evidence_unreadable_count` in `input.json`; a corpus failure is
      logged and the run completes.
- [x] `newsfind-deliver.md` reads the corpus index before Phase 2 and prefers a corpus file
      over `WebFetch` for a URL already read.
- [x] `newsfind-deliver.md` keeps `current_state` and `rag_context_refs`, with the rule that
      corpus context is background and never a substitute citation.
- [x] `search_content.py` extracts `.xlsx` and records `fetched`; `.xls` remains
      `unsupported` with its reason recorded.
- [x] `export_feeds` reports each feed's age and marks feeds past `feeds_max_age_days` as
      stale in the index and in the exported file's front matter.
- [x] Degraded facets are visible on the stage event and in the log for both legs.
- [x] `stage.finished` (deliver) and `refresh.completed` carry `evidence_count`,
      `evidence_unreadable_count`, `feeds_count`, `facets_degraded`.
- [x] `SourceMixNote` renders the backend payload; `src/lib/sourceQuality.ts` no longer
      carries a second definition.
- [x] `PATCH /monitor` accepts and validates `short_term_queries`.

Tests — offline, deterministic, no network:

- [x] Deliver exports the corpus, and a corpus failure does not fail the run
      (mirrors `tests/topics/test_evidence_export.py`).
- [x] `.xlsx` extraction succeeds and `.xls` is recorded `unsupported`, in
      `tests/topics/test_search_content.py`.
- [x] A stale feed is exported and marked stale; a fresh feed is not.
- [x] Degraded facets produce zero feeds **and** a visible signal — the negative case in
      `tests/topics/test_feeds.py` still holds (an India feed is refused for a Hormuz facet
      bag).
- [x] `PATCH /monitor` accepts a valid plan, rejects a malformed one, and preserves
      `allowed_domains`.
- [x] Frontend: `SourceMixNote` renders an emitted payload and falls back correctly when a
      legacy artefact carries none.
- [x] Full suite green (`pytest tests`, `vitest`, `tsc`, `eslint`); `ruff check` introduces
      no new findings in the files touched.

Verified on a slot, not only offline:

- [ ] One deliver run on test1 whose `stage.finished` reports a non-zero `evidence_count`
      and the expected `feeds_count`.
- [ ] In that run's `report.json`, at least one quantitative claim cites a feed rather than a
      search result, and at least one finding cites a document present in `evidence_dir`.
- [ ] The second India run (#45) is compared with the 2026-09-03 baseline on the counters
      above and on `primary_official` share. **Attribution caveat:** per #41 a single-run
      delta cannot separate this change from news-cycle variance; the counters are
      descriptive evidence that the inputs arrived, not proof of a quality gain.

## Notes for implementation

- `run_refresh` is the reference for every export in this ticket — deliver should end up
  structurally parallel to it, not a second dialect.
- The two slash commands change together. `docker/Dockerfile.claude_agent` bakes the
  whitelist and playbooks but **not** `claude_agent_fe`, which is bind-mounted, so prompt
  changes need no rebuild; the `search_content.py` change does.
- Prompt-contract changes alter how every existing monitored topic behaves, not only new
  ones. Batch them with #39's outstanding `thesis_status` divergence rule, which is waiting
  for exactly this kind of change (see `docs/specs/done/source_authority_enforcement_39.md`).
- **Batch one edit that is not ours.** `newsfind-deliver.md:164` specifies `next_queries` as
  `{q, intent, rationale}` with no `allowed_domains`, so every monitoring plan's priority-1
  block runs unfiltered — and `newsfind-refresh.md:15` shows an example carrying a filter that
  the deliver contract cannot produce. That is **#46** build item 0's scope, not this
  ticket's, but it edits the same two files: land it in the same prompt change rather than
  deploying prompt contracts twice.
- Do not deploy to the slot a customer is shown until a full topic has run on test1 and been
  read.

## Related

- `docs/specs/done/search_evidence_capture_42.md` — the store this ticket finally consumes;
  its *Still open* section lists three of these items.
- `docs/specs/active/india_gas_country_pilot_45.md` — the feeds channel and the run this is
  measured on.
- `docs/specs/active/topic_onboarding_loop_46.md` — the search-side half of the same loop.
- `docs/specs/done/source_authority_enforcement_39.md` — the contract rules these prompt
  edits must not weaken.
- `apps/claude_agent/topics/refresh.py` — the working pattern for every export here.
- `testing/app_testing_scenario.md`, `testing/README.md` — update when behaviour changes.
