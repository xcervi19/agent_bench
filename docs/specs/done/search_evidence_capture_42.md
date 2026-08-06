# Search evidence capture — #42

**Status:** done (2026-08-02)
**Lane:** Platform / Backend
**Depends on:** #36 (`execute_search` stub — search still lives in the deliver agent)
**Blocks:** later evaluation pass over the corpus (cheap-model reading, strategy TBD)

---

## Goal / Problem

Nothing persisted what web search actually returned. The event log kept a 600-char
preview that cut mid-URL, so ~3–4 of ~10 links survived and no snippets. `news.json`
kept only agent-self-reported counts plus the hits that survived filtering: on the
frozen baseline, 24 queries → 200 reported results → 28 kept, with `drops`
accounting for exactly 1. ~171 results vanished without trace, and the retained
numbers were unverifiable because the agent produced them itself.

Consequence: search precision/recall was not measurable, "search found nothing"
was indistinguishable from "agent discarded it", and runs were not reproducible
against the same search output.

## Solution / What was delivered

Capture every hit, per topic, continuously — **no verdict at capture time**.
Quality is judged later by a separate pass over the corpus.

Two layers, because they answer different questions:

- `search_documents` — deduplicated, one row per (topic, URL). What the corpus
  contains. A document surfaced by 50 refreshes is read once by the later pass.
- `search_observations` — append-only, one row per (query, run, rank) sighting.
  How search behaved over time. Never updated, never deduplicated.

Files:

- `apps/claude_agent/topics/search_evidence.py` — `parse_hits`, `record_hits`,
  `SearchEvidenceRecorder` (correlates `WebSearch` `tool_use` → `tool_result`
  across the agent stream).
- `apps/claude_agent/topics/models.py` — `SearchDocument`, `SearchObservation`.
- `database/migrations/versions/0008_search_evidence.py`.
- Wired into both agent stream loops: `pipeline.py` (plan + deliver legs) and
  `refresh.py` (every refresh cycle), so monitoring accumulates evidence too.
- `tests/topics/test_search_evidence.py`.

## Design decisions

**No verdict column.** Whether a hit was any good is decided later, after longer
observation, by a cheap model reading the articles. A verdict written at capture
time would freeze a judgement that will not hold. What *is* recoverable without a
verdict: `url_hash` uses the same `sha1(url)[:16]` convention as
`news.json#sources`, so joining evidence to the delivered report by URL identity
tells us afterwards which hits were used — a fact, not an opinion.

**Recording is separate from using.** Nothing captured here flows into the report.
The existing filtering in the deliver agent is untouched, so output quality cannot
be degraded by low-value content entering the corpus. The filter stops being
invisible and irreversible; it does not stop being applied.

**Parsing fails loud.** No try/except around hit parsing. If the WebSearch result
shape changes, the run raises instead of silently recording nothing — silent
evidence loss is the exact bug being fixed here.

## Article text capture (resolved — delivered)

Originally deferred pending "fetch everything vs. fetch behind a coarse filter".
Resolved: **attempt everything, record the outcome, do not engineer around blocks.**
Any capture-time filter would reintroduce the verdict this design removes.

- `apps/claude_agent/topics/search_content.py` — background loop draining documents
  with no `fetch_status` yet. Identifying user agent, robots.txt honoured (missing
  or unreachable robots allows), one request per host at a time.
- Outcomes are first-class data, not errors: `fetched`, `thin` (paywall teaser),
  `blocked` (401/402/403/429), `not_found`, `disallowed`, `unsupported` (non-HTML),
  `error`. Over time these accumulate into a per-domain accessibility map — which
  whitelisted sources we can never verify is itself a finding.
- HTML → text reuses `source_ingest.text_extract.html_to_text` rather than adding a
  dependency; the Dockerfile now copies `source_ingest` (it was absent from the
  image, so the import would have failed only in production).
- Runs entirely outside the agent. Costs no tokens, and cannot slow or break a
  topic run. Fetching via the agent's `WebFetch` was rejected: it bills every
  article through the model's context, and large page bodies already overflow the
  stream reader limit (`runner.py`).

**Expect a large share to fail, by design.** Commercial news sits behind bot
protection and paywalls; the primary and official sources the whitelist targets
mostly do not. The coverage lost skews toward what the rubric values least. No
proxies, no CAPTCHA solving, no paywall circumvention — partial coverage with
honest accounting beats an unmaintainable arms race.

## Scope explicitly not included

- **The judging pass itself.** Strategy is not designed. When it lands, judgements
  go in a separate layer keyed by strategy version, never overwriting, so a revised
  strategy can be re-run over the same corpus.
- **Retention policy** for topics that go inactive.
- The 600-char event-log preview is unchanged; it stays a UI concern now that
  evidence lives in its own store.

## Verification

- `tests/topics/test_search_evidence.py` — 6 tests: multi-link parse, text-block
  content, errored search → empty, malformed links → raises, `url_hash` convention,
  tool_use/tool_result correlation with interleaved non-search tools.
- `tests/topics/test_search_content.py` — 12 tests over a mocked transport: text
  extraction drops script/style, thin pages keep what there was, each block class
  maps to its status, non-HTML is skipped rather than garbled, robots disallow is
  honoured, missing robots allows, robots is fetched once per host, network failure
  is recorded not raised.
- Full suite: 264 passed.
- Ruff: no new findings (6 pre-existing errors in `models.py`/`refresh.py` untouched).
- **Migrations not yet applied against Postgres** — Docker daemon was down locally.
  `alembic upgrade head` still needs to run on a real database before deploy.
- **The fetcher has never run against the live web.** Every test uses a mocked
  transport, so the real block/success ratio is unmeasured. First production run
  should be read as a measurement, not a smoke test.
