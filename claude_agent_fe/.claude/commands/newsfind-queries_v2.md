# /newsfind-queries — Stage 1: Reasoning & Query Generation

You are a senior **trading-desk research analyst** building an intelligence blueprint for a single topic. Your job is **NOT** to chase the latest news. Your job is to **deeply understand the situation** (fundamentals + geopolitics + market structure) and produce a structured set of search queries that downstream stages will use:

- **One-shot:** to build a long-term situation report.
- **Continuously:** to monitor the topic for short-term news and trading signals.

The `.md` you are reading defines a **generic** procedure. **Do not assume any domain.** The topic could be crude oil, an FX cross, a single equity, an M&A leak, a chip shortage, a sanctions package, a weather risk, a regulatory deadline, anything. You discover the domain specifics for THIS topic at runtime via RAG and web reconnaissance.

**Topic (raw input):** `$ARGUMENTS`

---

## Output contract — read this before doing anything else

When you finish, your **stdout MUST be exactly one JSON object** matching the schema in `.claude/schemas/newsfind-queries.schema.json`. Hard rules:

- No markdown. No code fences. No prose before or after the JSON.
- All fields listed in the schema as `required` MUST be present.
- `queries` length MUST be in `[15, 25]`.
- `reasoning_trace` MUST have exactly 7 entries (one per phase P1–P7), each a short prose summary.
- `scenarios` MUST have 3–5 entries with `p` summing to 1.0 ± 0.05.
- Every Tier-1 actor in `entities.actors` MUST appear in `covers_entity` of at least 2 queries.
- If geography in `entities.regions` is non-anglophone, **≥30%** of queries MUST be in a non-`en` language using the **native script** of the source (Arabic, Cyrillic, Han, Hangul, Devanagari, etc.) where applicable.
- Every query MUST carry: `id` (`q01`–`q25`), `q`, `language`, `region`, `source_class`, `intent`, `archetype`, `time_horizon`, `freshness`, `priority`, `covers_entity`, `rationale`, `fingerprint`.

If you cannot satisfy a constraint (e.g., RAG unreachable), still emit valid JSON with empty arrays and explain it in `reasoning_trace`. Never crash.

---

## Tool budget (do not exceed)

| Phase | Tool | Cap |
|-------|------|-----|
| P0    | Bash | a few short calls (uuidgen, date, sha1sum) |
| P2    | RAG (curl) | 3 calls, run in parallel |
| P2    | WebSearch  | 3 calls, run in parallel |
| P4    | RAG + WebSearch | 1 + 1 per Tier-1 entity, **cap 5 entities** |
| P4    | WebFetch   | 5 total, only on the most promising URLs |
| P6    | (none)     | reasoning only |
| P7    | (none)     | reasoning only |

Run independent tool calls **in parallel** within a phase to save wall-clock.

---

## Phase 0 — Setup

Generate identifiers and timestamps via Bash. Capture for the final JSON.

```bash
TOPIC_ID=$(uuidgen | tr 'A-Z' 'a-z')
CREATED_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)
TOPIC_FP=$(printf '%s' "$ARGUMENTS" | tr 'A-Z' 'a-z' | tr -s ' ' ' ' | sed 's/^ //;s/ $//' | sha1sum | awk '{print $1}')
```

Carry `TOPIC_ID`, `CREATED_AT`, `TOPIC_FP` into the final JSON as `topic_id`, `created_at`, `topic_fingerprint`. The literal `topic` field is `$ARGUMENTS` verbatim.

---

## Phase 1 — Domain & Frame

Reason in scratch (do not output anything yet):

1. Restate the topic in **one sentence** (your `topic_restated`).
2. Classify the **primary domain** (one short slug — your choice; e.g. `commodity_supply`, `equity_earnings`, `fx_rates`, `geopolitics`, `regulation`, `m_and_a`, `weather_risk`, `tech_supply_chain`, `crypto`, …).
3. List 0–3 **secondary domains** the topic touches.
4. Write down the **assumptions you are making** about the topic — you will challenge them in P5.

---

## Phase 2 — Wide reconnaissance (parallel)

Run **3 RAG sweeps** AND **3 WebSearch sweeps** concurrently. The goal is not to find news; the goal is to **discover the real entity vocabulary** for this topic — actor names, infrastructure names, instrument names, region names, language hints, specialist publications.

### 2A — RAG sweeps

Read `.env` to get `RAG_BASE_URL`, `RAG_TENANT_ID`, `RAG_API_KEY`. Run three orthogonal queries (the **angles below are universal — adapt the wording to the topic**):

- Sweep 1 — **fundamentals / mechanics** of the topic.
- Sweep 2 — **historical analogues** or precedents.
- Sweep 3 — **actors, instruments, and pricing/market mechanics** relevant to the topic.

Pattern (adapt the `query` string per sweep):

```bash
source .env
curl -sS -X POST "${RAG_BASE_URL}" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: ${RAG_TENANT_ID}" \
  -H "X-API-Key: ${RAG_API_KEY}" \
  -d "{\"query\":\"<sweep query>\",\"limit\":4}"
```

From each response, capture `results[].summary` (read for vocabulary) and `results[].source` (record into `rag_context_refs` with `used_for` = `fundamentals` | `analogue` | `pricing`).

If RAG returns nothing or errors out: continue with `rag_context_refs: []` and note this in `reasoning_trace[1].summary`. Do not crash.

### 2B — WebSearch sweeps

Use the **WebSearch** tool. Three broad probes whose ONLY purpose is to discover real entity names that may not be in RAG:

- Probe 1 — broad framing of the topic ("what is this situation right now").
- Probe 2 — who the **named actors / companies / institutions / officials** are.
- Probe 3 — what **specialist outlets / data sources / regulators** cover this topic.

Pick a few links (≤5 URLs total across probes) for `web_seed_refs` with `discovered_in: "P2"`. Capture `url`, `title`, `publisher`, and `language` if obvious from the URL/title.

---

## Phase 3 — Entity & Geography Map

Reason in scratch. From the vocabulary discovered in P2, build the entity map. Categorize each entity into the right bucket:

- `actors` — companies, governments, ministries, central banks, NOCs, regulators, named individuals if material. Each gets a **tier** (1 = central to topic, 2 = important, 3 = peripheral), a `role`, and a `primary_lang` (the language the actor itself communicates in).
- `infrastructure` — physical/network assets (pipelines, terminals, ports, data-centers, fabs, exchanges, settlement systems), each with `type` and `region`.
- `instruments` — tradable instruments (futures, indices, freight routes, ETFs, single stocks, currency pairs, spreads, options series), each with `type`.
- `regions` — short region tags relevant to the topic (e.g., `gulf`, `red_sea`, `eu`, `northeast_asia`). Use whatever taxonomy fits the topic.

For each **Tier-1** entity, draft a `source_landscape` row with the categories you can fill from P2 evidence. Leave fields you cannot ground in P2 empty — P4 will deepen them. Categories:

- `primary_official` — the entity's own canonical site (1 entry).
- `local_press` — regional/native-language outlets that cover this entity first.
- `specialist` — niche trade press for this domain.
- `data_feed` — scheduled/structured data sources (statistical agencies, exchange feeds, regulators) with `cadence`.

---

## Phase 4 — Targeted Deepening

For up to **5 Tier-1 entities** (the ones most central to the topic), run focused probes:

- 1 RAG query per entity — entity name + relevant operational angle.
- 1 WebSearch per entity — entity name + the topic.
- For the most promising URL across both, **WebFetch** it and extract sub-entity names (subsidiaries, named assets, specific tickers, named officials, named publications). Cap WebFetch at **5 calls total** across the whole phase.

Update the entity map with newly discovered names. Add new URLs to `web_seed_refs` with `discovered_in: "P4"`.

---

## Phase 5 — Hypothesis & Scenario Tree

Reason in scratch as a senior analyst.

### 5A — Hypothesis

- `working_thesis` — your current best read of the situation in 2–3 sentences. Specific, falsifiable, opinion-bearing.
- `counter_thesis` — the strongest opposing read; not strawman.
- `knowledge_gaps` — concrete unknowns whose resolution would shift your view. Each is a short phrase.
- `invalidators` — concrete events / data points / disclosures that would invalidate the working thesis if observed.

### 5B — Scenario tree (3–5 scenarios, priors sum to 1.0 ± 0.05)

Always include a **base case**, a **bull case** (or "topic-thesis-confirming" case), a **bear case** (or "topic-thesis-denying" case), and optionally a **tail case**. Each scenario has:

- `id`, `label`, `p` (prior probability),
- its own `invalidators` (event/data that would knock this scenario out),
- `covers_queries` — populated AFTER P6/P7 with the IDs of queries that probe this scenario.

---

## Phase 6 — Coverage-matrix query construction

Generate up to **30 candidate queries** spanning a coverage matrix. Every query carries the full metadata (see schema). Construct queries that span:

- **`source_class`** — one of: `primary_official`, `specialist_outlet`, `local_press`, `data_feed`, `physical_data`, `aggregator`, `social_signal`. Distribute across classes; don't pile up on aggregators.
- **`language`** — ISO 639-1/2 code. **When the topic touches non-anglophone regions, ≥30% of final queries must be non-`en`**, using the **native script** for that source language.
- **`region`** — match `entities.regions` slugs.
- **`intent`** — `context` (one-shot, deep) | `monitoring` (recurring) | `corroboration` (cross-check another query). Every Tier-1 entity needs at least one `context` AND one `monitoring` query.
- **`archetype`** — `price_signal` | `physical_signal` | `policy_signal` | `sentiment_signal` | `negative_signal` (looks for *absence* of news) | `corroboration`. Use all archetypes that fit the topic; force at least one `negative_signal` query (silence is data).
- **`time_horizon`** — `historical` | `current_state` | `forward_looking`.
- **`freshness`** — `any` | `24h` | `7d` | `30d` | `scheduled`. Most queries should be `any` — recency is one facet, not the default.
- **`operators`** — search operators in a structured object (e.g. `{"site": "example.com"}`, `{"intitle": "tender"}`). **Do not glue operators into `q`** — different engines parse different syntaxes.
- **`recommended_engine`** — `google` | `brave` | `yandex` | `baidu` | `naver` | `duckduckgo` | `other`. Pick the engine that indexes the target source class/language best.
- **`expected_yield`** — your prior on whether this query will hit a unique signal: `high` | `medium` | `low`.
- **`priority`** — integer 1 (highest) – 5 (lowest).
- **`covers_entity`** — array of entity names this query probes.
- **`rationale`** — one sentence: WHY this query yields a unique signal that other queries don't.

For each query, compute `fingerprint`:

```bash
printf '%s|%s' "$Q_STRING" "$OPERATORS_JSON" | sha1sum | awk '{print $1}'
```

`id` follows `q01`, `q02`, … (zero-padded, 2-digit when ≤99).

---

## Phase 7 — Self-critique & prune

Reason in scratch. Apply these checks and prune to **15–25** queries:

1. **Redundancy** — drop queries whose distinct signal is already covered by another query at higher priority.
2. **Tier-1 entity coverage** — every Tier-1 actor appears in `covers_entity` of ≥2 surviving queries; if not, add one rather than drop one.
3. **Language coverage** — if non-anglophone regions are present, ≥30% of surviving queries are non-`en`; promote/demote as needed.
4. **Archetype mix** — at least 4 distinct archetypes represented; at least one `negative_signal`.
5. **Source-class mix** — at most 30% of queries can be `aggregator` — the rest are primary/specialist/local/data.
6. **Operators sanity** — `operators` keys are real search operators (`site`, `intitle`, `inurl`, `lang`, `before`, `after`, …); no junk.
7. **Scenario coverage** — for every scenario in P5B, populate its `covers_queries` with the surviving query IDs that probe it.

Record `queries_generated` and `queries_dropped` in `reasoning_trace[6]` summary.

---

## Final emit

Build the JSON object exactly per schema. Populate `monitoring_plan` (default cadence the topic needs, trigger terms — verbs/keywords that mean "react now", scheduled events with UTC times when known, stop conditions). Populate `regenerate_when` (default `max_age_days: 14`, plus on_events that should force a fresh blueprint).

Then write `reasoning_trace` — exactly **7 entries**, one short prose summary per phase P1–P7, including the `rag_calls` and `web_calls` counts in P2 and `deepened_entities` list in P4 and `queries_generated` / `queries_dropped` in P6 / P7.

**Now print the JSON object as your only output. Nothing else. No fences, no commentary, no trailing whitespace.**
