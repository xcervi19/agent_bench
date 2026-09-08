# Report grounding — everything we already hold reaches the analyst (#51)

**Status:** planned (2026-09-08)
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

## Acceptance criteria

Implementation:

- [ ] `run_deliver` exports the evidence corpus and passes `evidence_dir` /
      `evidence_count` / `evidence_unreadable_count` in `input.json`; a corpus failure is
      logged and the run completes.
- [ ] `newsfind-deliver.md` reads the corpus index before Phase 2 and prefers a corpus file
      over `WebFetch` for a URL already read.
- [ ] `newsfind-deliver.md` keeps `current_state` and `rag_context_refs`, with the rule that
      corpus context is background and never a substitute citation.
- [ ] `search_content.py` extracts `.xlsx` and records `fetched`; `.xls` remains
      `unsupported` with its reason recorded.
- [ ] `export_feeds` reports each feed's age and marks feeds past `feeds_max_age_days` as
      stale in the index and in the exported file's front matter.
- [ ] Degraded facets are visible on the stage event and in the log for both legs.
- [ ] `stage.finished` (deliver) and `refresh.completed` carry `evidence_count`,
      `evidence_unreadable_count`, `feeds_count`, `facets_degraded`.
- [ ] `SourceMixNote` renders the backend payload; `src/lib/sourceQuality.ts` no longer
      carries a second definition.
- [ ] `PATCH /monitor` accepts and validates `short_term_queries`.

Tests — offline, deterministic, no network:

- [ ] Deliver exports the corpus, and a corpus failure does not fail the run
      (mirrors `tests/topics/test_evidence_export.py`).
- [ ] `.xlsx` extraction succeeds and `.xls` is recorded `unsupported`, in
      `tests/topics/test_search_content.py`.
- [ ] A stale feed is exported and marked stale; a fresh feed is not.
- [ ] Degraded facets produce zero feeds **and** a visible signal — the negative case in
      `tests/topics/test_feeds.py` still holds (an India feed is refused for a Hormuz facet
      bag).
- [ ] `PATCH /monitor` accepts a valid plan, rejects a malformed one, and preserves
      `allowed_domains`.
- [ ] Frontend: `SourceMixNote` renders an emitted payload and falls back correctly when a
      legacy artefact carries none.
- [ ] Full suite green (`pytest tests`, `vitest`, `tsc`, `eslint`); `ruff check` introduces
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
