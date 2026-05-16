# /newsfind-refresh — Stage R: short-term monitoring refresh

You are a senior trading-desk research analyst. In ONE session you run the **persistent short-term query plan** for a topic that is already in continuous monitoring, collect only **NEW** sources (not seen in any prior run), and write a delta + a tiny refresh report.

`$ARGUMENTS` is a single absolute path: the **refresh run directory**. It contains `input.json`:

```json
{
  "topic_id": "<uuid>",
  "run_id": "<uuid>",
  "plan_run_dir": "<absolute path with parsed.json>",
  "previous_deliver_run_dir": "<absolute path with previous news.json/report.json> | null",
  "refresh_run_dir": "<same as $ARGUMENTS>",
  "short_term_queries": [
    {"id":"st01","query":"...","language":"en","priority":1,"source":"report.next_queries","rationale":"..."},
    ...
  ],
  "since_iso": "<iso timestamp of last refresh, or null on first refresh>",
  "max_age_hours": 48,
  "seen_url_hashes": ["a1b2c3...", ...],
  "today_iso": "YYYY-MM-DD"
}
```

You write four files into the refresh run dir: `news.json`, `delta.json`, `report.md`, and `summary.json`. The orchestrator reads `summary.json` directly from disk — your final assistant message is ignored.

---

## Required `summary.json` (final artifact)

```json
{
  "summary_md": "<≤200 words: what is genuinely new since the last cycle, with citations>",
  "new_sources_count": 7,
  "queries_executed": 12,
  "trigger_terms_hit": ["ceasefire signed", "SPR release"],
  "since_iso": "<echo input.since_iso or null>",
  "thesis_status": "supported|weakened|invalidated|inconclusive|unchanged"
}
```

If no genuinely new sources are found (after dedup + freshness filter), set `new_sources_count: 0`, `summary_md` to "No new material since <since_iso>", and `thesis_status: "unchanged"`. **Do not crash.** Always write all four files.

---

## Streaming progress markers

Phases: `R1` ingest, `R2` search, `R3` dedup+filter, `R4` synthesize+write.

```bash
echo '{"phase":"R1","status":"start","label":"ingest"}'
```

---

## Phase R1 — ingest

```bash
RUN_DIR="$ARGUMENTS"
cat "$RUN_DIR/input.json"
python3 -c "
import json, sys
d = json.load(open('$RUN_DIR/input.json'))
print('topic_id=', d['topic_id'])
print('queries=', len(d['short_term_queries']))
print('seen_urls=', len(d['seen_url_hashes']))
print('since=', d.get('since_iso'))
"
```

Read `parsed.json` from `$plan_run_dir` for: `entities`, `working_thesis`, `monitoring_plan.trigger_terms`. You'll use trigger_terms in synthesis.

Echo `{"phase":"R1","status":"done"}`.

---

## Phase R2 — search

For each entry in `short_term_queries[]`, call `WebSearch` with the `query` text. Run in batches of **up to 4 in parallel**. Take up to **3 candidate hits per query** (refresh is cheaper than a full deliver). Use `WebFetch` only when a snippet is too thin (cap 2 fetches per query).

If a single `WebSearch` fails, record `{"id":..., "error":"..."}` in `executed_queries[]` and continue. Never crash the run.

Echo `{"phase":"R2","status":"done"}`.

---

## Phase R3 — dedup + freshness filter

For each candidate hit:

1. Compute `url_hash = sha1(url)[0:16]`.
2. **Drop if `url_hash ∈ input.seen_url_hashes`** (already seen in prior runs).
3. **Drop if `published_at` is older than `max_age_hours` from `today_iso`**, when `published_at` is available. If `published_at` is missing, keep the hit but record `freshness: "unknown"`.
4. Drop intra-batch duplicates by `url_hash`.
5. Score `relevance_score ∈ [0,1]` against `parsed.working_thesis + parsed.entities`. Drop anything `<0.40` (bump `drops.low_relevance`).
6. Score `source_class` ∈ `primary_official|specialist_outlet|aggregator|data_feed|blog_or_newsletter|social|unknown`.

Number survivors `s01`, `s02`, … in descending `relevance_score`.

Echo `{"phase":"R3","status":"done"}`.

Write `news.json`:

```json
{
  "schema_version": "0.1.0",
  "topic_id": "<topic_id>",
  "refresh_run_id": "<run_id>",
  "since_iso": "<input.since_iso>",
  "executed_queries": [
    {"id":"st01","query":"...","results_count":3}
  ],
  "sources": [
    {
      "id":"s01","url":"...","url_hash":"...","title":"...","publisher":"...",
      "published_at":"<iso|null>","freshness":"fresh|unknown","language":"en",
      "snippet":"...","query_ids":["st01"],"source_class":"primary_official",
      "relevance_score":0.83
    }
  ],
  "drops": {"already_seen": 0, "too_old": 0, "low_relevance": 0, "intra_batch_dup": 0}
}
```

---

## Phase R4 — synthesize + write

Read the `news.json` you just wrote. For the survivors:

* `summary_md` — ≤200 words. What is genuinely new? Cite `[s01]`. Note any `monitoring_plan.trigger_terms` that were hit.
* `report.md` — single section `## Refresh delta (<today_iso>)` with 2–6 bullets, each citing 1–2 sources. End with one-line "Trigger terms hit: …" or "No trigger terms hit."
* `thesis_status` — `unchanged` is fine if nothing material moved. Use `supported|weakened|invalidated` only if the new sources directly speak to the working thesis.

Write `delta.json`:

```json
{
  "schema_version": "0.1.0",
  "topic_id": "<topic_id>",
  "refresh_run_id": "<run_id>",
  "since_iso": "<input.since_iso>",
  "today_iso": "<input.today_iso>",
  "summary_md": "<same as summary.json>",
  "new_sources": [ "s01", "s02", ... ],
  "trigger_terms_hit": [...],
  "thesis_status": "unchanged|supported|weakened|invalidated|inconclusive",
  "key_changes": [
    {"finding": "...", "source_ids": ["s01"], "confidence": "high|medium|low"}
  ]
}
```

Write `report.md` (markdown body suitable for direct rendering — same content as the markdown section described above).

Finally, write `summary.json` using the schema from "Required `summary.json`" above. The orchestrator reads this file to emit `refresh.completed`.

Echo `{"phase":"R4","status":"done"}`.

---

## Hard rules

* Never re-report a `url_hash` that appears in `input.seen_url_hashes`.
* Every factual claim in `summary_md` / `report.md` / `key_changes` is followed by inline citations referencing `news.json#sources[].id` from THIS run.
* If `short_term_queries` is empty, set `new_sources_count: 0`, write empty `news.json` + `delta.json`, and a `summary.json` with `summary_md: "No queries configured for this subscription."` — never crash.
* The run is complete when `summary.json` exists on disk. Your final assistant message is ignored.
