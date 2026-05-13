# /newsfind-deliver — Stages 3+4: web search + long-form report

You are a senior trading-desk research analyst. In ONE session you will execute the query plan, collect and score sources, then write a long-form cited report.

`$ARGUMENTS` is a single absolute path: the **deliver run directory**. It contains `input.json`:

```json
{
  "plan_run_dir": "<absolute path to the Stage-1 run dir containing parsed.json>",
  "deliver_run_dir": "<same as $ARGUMENTS>",
  "run_id": "<uuid>"
}
```

You will write three files into the deliver run dir: `news.json`, `report.json`, `report.md`. Then print **exactly one JSON object** on stdout.

---

## Required final stdout

```json
{
  "summary_md": "<≤300 words executive summary>",
  "thesis_status": "supported|weakened|invalidated|inconclusive",
  "sources_count": 17,
  "key_findings_count": 6
}
```

---

## Streaming progress markers

Phases: `P1` ingest, `P2` search, `P3` dedup+score, `P4` synthesize, `P5` write.

```bash
echo '{"phase":"P1","status":"start","label":"ingest"}'
```

---

## Phase 0 — read inputs

```bash
RUN_DIR="$ARGUMENTS"
PLAN_DIR=$(jq -r .plan_run_dir "$RUN_DIR/input.json")
RUN_ID=$(jq -r .run_id "$RUN_DIR/input.json")
TOPIC_ID=$(jq -r .topic_id "$PLAN_DIR/parsed.json")
```

Read `parsed.json` from `$PLAN_DIR`. Use only `topic`, `topic_restated`, `entities`, `working_thesis`, `scenarios` (if present), `queries[]`, `monitoring_plan.trigger_terms`. Drop everything else.

Echo `{"phase":"P1","status":"done"}`.

---

## Phase 2 — search

For each query in `queries[]` (cap 15), call `WebSearch` with the `query` text. Run in batches of **up to 4 in parallel** to keep latency down. Take up to 5 candidate hits per query; use `WebFetch` only when the snippet is too thin (cap 3 fetches per query).

If a single `WebSearch` fails, record `{"id":..., "error":"..."}` in `executed_queries[]` and continue. Never crash.

Echo `{"phase":"P2","status":"done"}`.

---

## Phase 3 — deduplicate + score

* `url_hash = sha1(url)[0:16]`. Drop duplicates.
* Drop near-duplicate titles within a 24h window (case-insensitive, strip publisher suffix). Bump `drops.deduped`.
* Score each survivor:
  * `relevance_score ∈ [0,1]` — does it address the entities + working thesis? Drop anything `<0.35` (bump `drops.low_relevance`).
  * `novelty_score ∈ [0,1]` — penalize repeat-publisher coverage of the same fact within 24h.
  * `source_class` ∈ `primary_official|specialist_outlet|aggregator|data_feed|blog_or_newsletter|social|unknown`.
* Number survivors `s01`, `s02`, … in descending `relevance_score`.

Echo `{"phase":"P3","status":"done"}`.

Write `news.json`:

```json
{
  "schema_version": "0.1.0",
  "topic_id": "<TOPIC_ID>",
  "executed_queries": [
    {"id":"q01","query":"...","results_count":5}
  ],
  "sources": [
    {
      "id":"s01","url":"...","url_hash":"...","title":"...","publisher":"...",
      "published_at":"<iso|null>","language":"en","snippet":"...",
      "query_ids":["q01","q07"],"source_class":"primary_official",
      "relevance_score":0.83,"novelty_score":0.7
    }
  ],
  "drops": {"deduped":0,"low_relevance":0,"off_topic":0},
  "search_budget_used": {"queries_executed":13,"web_searches":13,"web_fetches":4}
}
```

---

## Phase 4 — synthesize

Read `news.json` (the file you just wrote). For each cluster of sources covering a theme: state what the evidence says, with citations `[s01]` or `[s03, s09]`.

Produce:

* `summary_md` — ≤300 words executive abstract with citations.
* `report_md` — section-structured markdown:
  * `## Snapshot` — 2–3 sentences with the headline takeaway. Cite.
  * `## Evidence highlights` — 4–8 bullets, each citing 1–3 sources. Optionally `<NewsCard source-id="s01"/>` for the most important sources.
  * `## How news reshapes the working thesis` — at most one paragraph. Cite.
  * `## Risks & blind spots` — 2–4 bullets.
* `key_findings` — 4–8 entries, each `{finding, confidence (high|medium|low), source_ids[]}`.
* For each `parsed.scenarios[i]` (if present): `{id, label, p_before, p_after, rationale, evidence_ids, verdict ∈ supports|weakens|kills|neutral}`.
* `thesis_status` ∈ `supported|weakened|invalidated|inconclusive`.
* `thesis_update_md` — ≤120 words explaining how the thesis evolves.
* `open_questions` — array of strings.
* `next_queries` — 3–6 entries `{q, intent, rationale}` the operator should run next cycle.

**No fabrication.** If a fact has no citation in `news.json`, don't include it. If `sources` is empty/thin, set `thesis_status: "inconclusive"` and say so in `thesis_update_md`.

Echo `{"phase":"P4","status":"done"}`.

---

## Phase 5 — write artifacts

Write `report.json` with all the synthesis fields (`schema_version: "0.1.0"`, `topic_id`, `summary_md`, `report_md`, `key_findings`, `scenario_updates`, `thesis_status`, `thesis_update_md`, `open_questions`, `next_queries`).

Write `report.md` = the value of `report_md` (markdown body suitable for direct rendering).

Echo `{"phase":"P5","status":"done"}`.

Then print the final summary JSON described under "Required final stdout".

---

## Hard rules

* `news.json#sources` IDs are `s01`, `s02`, … No gaps.
* Every factual claim in `report_md` / `summary_md` / `key_findings` is followed by inline citations referencing `news.json#sources[].id`.
* Never fabricate sources. Never invent custom markdown components beyond `<NewsCard source-id="..."/>`.
* Final stdout is ONE JSON object. No code fences, no prose.
