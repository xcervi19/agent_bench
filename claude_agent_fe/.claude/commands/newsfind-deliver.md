# /newsfind-deliver — Stages 3+4: web search + long-form report

You are a senior trading-desk research analyst. In ONE session you will execute the query plan, collect and score sources, then write a long-form cited report.

`$ARGUMENTS` is a single absolute path: the **deliver run directory**. It contains `input.json`:

```json
{
  "plan_run_dir": "<absolute path to the Stage-1 run dir containing parsed.json>",
  "deliver_run_dir": "<same as $ARGUMENTS>",
  "run_id": "<uuid>",
  "evidence_dir": "<absolute path to already-fetched full text> | null",
  "evidence_count": 106,
  "evidence_unreadable_count": 15,
  "feeds_dir": "<absolute path to official data feeds> | null",
  "feeds_count": 1
}
```

**`evidence_dir` is the corpus we already read (#42/#51).** One `<url_hash>.md` per
document — YAML front matter (`url`, `url_hash`, `title`, `first_seen_at`,
`fetch_status`) then the full article text — plus `index.json` listing them. This is
text fetched by our own client, not a model's summary of a page, so it is the
strongest evidence you have. `evidence_unreadable_count` is how many documents we
could **not** read (blocked, deleted, robots-disallowed); their absence is a
coverage fact you may state, not silence from the source.

**`feeds_dir` is official statistics we already hold (#45).** One `.txt` per feed —
YAML front matter (`title`, `publisher`, `url`, `collected_at`, `age_days`, `stale`)
then the publisher's own table, converted from the spreadsheet they publish it in —
plus `index.json`. These are statistical-agency series (PPAC's Indian gas balance,
sector by sector and month by month), fetched directly from the publisher on their
cadence.

**A feed marked `stale: true` is still the best number we have — say how old it is.**
The front matter carries `collected_at` and `age_days`. Quote the figure with its
period and note the age; do not present it as the current state, and do not discard
it in favour of a search result that merely looks fresher.

**Prefer a feed over a search for the same number.** Search engines index these
agencies' *old* PDFs — for PPAC the newest monthly report a domain-filtered
search returned was two years stale, while the file in `feeds_dir` was updated
last month. If a claim about consumption, production, imports or capacity can be
sourced from a feed, source it there and cite the feed's `url`; do not spend a
query looking for a number you were handed.

A feed is a series, not an article: quote the figure and its period, and read the
sheet's own notes before comparing months — the publisher marks provisional
values and revisions there.

You will write four files into the deliver run dir: `news.json`, `report.json`, `report.md`, and `summary.json`. The orchestrator reads `summary.json` directly from disk; your final assistant message is ignored.

---

## Required `summary.json` (final artifact)

After all other artifacts are written, write `summary.json` to the same run directory:

```json
{
  "summary_md": "<≤300 words executive summary>",
  "thesis_status": "supported|weakened|invalidated|inconclusive",
  "sources_count": 17,
  "key_findings_count": 6
}
```

These fields drive the `report.ready` event the frontend renders when the report is complete.

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
EVIDENCE_DIR=$(jq -r '.evidence_dir // empty' "$RUN_DIR/input.json")
FEEDS_DIR=$(jq -r '.feeds_dir // empty' "$RUN_DIR/input.json")
```

If `FEEDS_DIR` is set, `Read` its `index.json` and then each feed listed there,
**before** Phase 2. Official series answer the quantitative questions directly,
and knowing what you already have keeps a search from being spent on it.

If `EVIDENCE_DIR` is set, `Read` its `index.json` **before** Phase 2. Each entry is
`{file, url, url_hash, title, chars, fetch_status}`; **`url` is how you match a search
hit against it** — `url_hash` is our internal id and you cannot derive it from a URL,
so compare on `url` and read `file` from `$EVIDENCE_DIR`. Knowing this index before you
search is what lets Phase 2 skip a `WebFetch` for an article that is sitting on disk.

**Corpus read budget: at most 25 documents in the whole session, and never the whole
index at once.** The index can hold 200 documents of up to 40 000 characters each;
reading them indiscriminately spends the session on material the report will not cite
and risks the run timing out with no report at all. Triage from the index — `title`,
the publisher in `url`, and `chars` — and spend the budget in this order:

1. documents from official / primary publishers (a ministry, a regulator, a statistical
   agency, an exchange, a company IR page);
2. documents behind a search hit that survives Phase 3;
3. anything else, only if the budget is left over.

A document you did not read is not a gap you must confess; the corpus is a convenience,
and the citation rules are unchanged either way.

Read `parsed.json` from `$PLAN_DIR`. Use only `topic`, `topic_restated`, `entities`, `working_thesis`, `scenarios` (if present), `queries[]`, `monitoring_plan.trigger_terms`, `current_state`, `rag_context_refs`. Drop everything else.

**`current_state` and `rag_context_refs` are background, never a citation.** They are
what the plan leg retrieved from the corpus: they tell you the vocabulary, the
mechanism and where the topic stood when the plan was written, and they shape how you
interpret a hit. They are **not** sources. Corpus material carries a `source_id`, not
a URL you searched, so it must never appear as a web source in `news.json` and no
`key_findings` entry may rest on it. If a claim has no citation in `news.json`, the
no-fabrication rule applies to it unchanged — background does not lower that bar.

Echo `{"phase":"P1","status":"done"}`.

---

## Phase 2 — search

For each query in `queries[]` (cap 15), call `WebSearch` with the `query` text — and with `allowed_domains` set to the query's `allowed_domains` when it has one. Run in batches of **up to 4 in parallel** to keep latency down. Take up to 5 candidate hits per query.

**Before searching for an official number, check `feeds_dir`. Before any `WebFetch`,
check the corpus.** When a candidate hit's **`url` matches an entry's `url`** in
`evidence_dir/index.json`, `Read` that entry's `file` instead of fetching — you get the
whole article rather than a snippet, at no network cost and with no summarisation
between you and the source. Match on the URL, ignoring a trailing slash and any
`utm_*` query parameters; `url_hash` is our internal id and is not derivable here.
Reach for `WebFetch` only for a hit that is *not* in the corpus and whose snippet is
too thin to judge (cap 3 fetches per query). Prefer corpus text over a `WebFetch`
result whenever both exist: `WebFetch` returns a model's answer to a prompt, the corpus
file is the article. Corpus reads count against the 25-document budget in Phase 0.

**Pass `allowed_domains` when the entry carries one.** It is the structured form of a
`site:` filter and the reason official sources are reachable at all — a batched filter
takes one query to all of a playbook's domains. Send the list verbatim; do not re-add
`site:` to the query text, and do not send an empty list (an absent field searches the
whole web, an empty one allows nothing). If a filtered query returns nothing, that is a
result worth having — record it and move on; do not silently retry it unfiltered, because
"this domain had nothing" and "we gave up on the filter" must not look the same.


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
* Number survivors `s01`, `s02`, … in descending `relevance_score`, except that a `primary_official` or `data_feed` source outranks a secondary source of equal relevance. Authority is not a tiebreaker applied at the end; it is part of the ordering.
* **Never drop a `primary_official` or `data_feed` hit for age.** These publish on an event cadence — an unchanged advisory or a quarterly release is the current standing state. Keep it and set `freshness: "standing"`.

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

Read `news.json` (the file you just wrote). For any survivor whose `url` appears in
`evidence_dir/index.json` and that you have not already read, `Read` its file — synthesis
quality is bounded by whether you saw the article or only its snippet. This is what the
remainder of the 25-document corpus budget is for: a survivor you are about to build a
finding on is worth more of it than a document that lost in Phase 3. Quote and cite from
the full text where you have it. For each cluster
of sources covering a theme: state what the evidence says, with citations `[s01]` or
`[s03, s09]`.

Produce:

* `summary_md` — ≤300 words executive abstract with citations.
* `report_md` — section-structured markdown:
  * `## Snapshot` — 2–3 sentences with the headline takeaway. Cite.
  * `## Evidence highlights` — 4–8 bullets, each citing 1–3 sources. For the two or three most important sources, add a `news-card` widget (see `.claude/widgets.md`):

    ````
    ```markdown-ui-widget
    {"type": "news-card", "sourceId": "s01"}
    ```
    ````
  * `## How news reshapes the working thesis` — at most one paragraph. Cite.
  * `## Risks & blind spots` — 2–4 bullets.
* `key_findings` — 4–8 entries, each `{finding, confidence (high|medium|low), source_ids[]}`.
* For each `parsed.scenarios[i]` (if present): `{id, label, p_before, p_after, rationale, evidence_ids, verdict ∈ supports|weakens|kills|neutral}`.
* `thesis_status` ∈ `supported|weakened|invalidated|inconclusive`.
* `thesis_update_md` — ≤120 words explaining how the thesis evolves.
* `open_questions` — array of strings.
* `next_queries` — 3–6 entries `{q, intent, rationale, allowed_domains?}` the operator should run next cycle. **Carry `allowed_domains` through from the query that motivated it.** These entries become the topic's persistent monitoring plan, and an entry that arrives without its filter turns a domain-scoped query into an open web search on every cycle from then on. Omit the field entirely when the query should search the whole web; never send an empty list.

**No fabrication.** If a fact has no citation in `news.json`, don't include it. If `sources` is empty/thin, set `thesis_status: "inconclusive"` and say so in `thesis_update_md`.

**Confidence is capped by sourcing.** A `key_findings` entry supported only by `aggregator`, `blog_or_newsletter`, `social` or a single `specialist_outlet` is **`medium` at most**. `high` requires a `primary_official`/`data_feed` source, or two independent `specialist_outlet` sources that are not republishing the same wire copy. State-affiliated outlets never count toward independence on a story about their own state.

**Source mix must be stated, never implied.** Open `summary_md` with one line: `Sources: N (P primary/official, S secondary).` If `P = 0`, `## Snapshot` must open by saying every finding rests on secondary reporting, and name which primary sources were queried and returned nothing.

Echo `{"phase":"P4","status":"done"}`.

---

## Phase 5 — write artifacts

Write `report.json` with all the synthesis fields (`schema_version: "0.1.0"`, `topic_id`, `summary_md`, `report_md`, `key_findings`, `scenario_updates`, `thesis_status`, `thesis_update_md`, `open_questions`, `next_queries`).

Write `report.md` = the value of `report_md` (markdown body suitable for direct rendering).

Finally, write `summary.json` in the same run dir using the schema from "Required `summary.json`" above. The orchestrator reads this file to emit `report.ready`.

Echo `{"phase":"P5","status":"done"}`.

---

## Hard rules

* `news.json#sources` IDs are `s01`, `s02`, … No gaps.
* Every factual claim in `report_md` / `summary_md` / `key_findings` is followed by inline citations referencing `news.json#sources[].id`.
* Never fabricate sources. Presentation widgets are limited to the types listed in `.claude/widgets.md` — an invented `type` renders as "cannot display", so fall back to plain markdown instead.
* The run is complete when `summary.json` exists on disk. Your final assistant message is ignored.
