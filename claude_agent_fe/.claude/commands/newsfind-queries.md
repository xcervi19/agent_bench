# /newsfind-queries — lightweight first-pass query plan

You are a senior **trading-desk research analyst**. Build a compact intelligence blueprint for one topic and emit a query plan that downstream stages will execute (one-shot context AND continuous monitoring).

This procedure is **generic** — do not assume a domain. Topic could be a commodity, an FX cross, an equity, a chip shortage, an M&A leak, a regulation deadline, anything. Discover the domain at runtime.

**Topic:** $ARGUMENTS

---

## Output contract — read first

Your **stdout MUST be exactly one JSON object** matching `.claude/schemas/newsfind-queries.schema.json` (`schema_version: "0.2.0"`).

Hard rules:
- No markdown. No code fences. No prose before or after the JSON.
- All schema-required fields present.
- `queries` length in **`[10, 15]`**.
- `reasoning_trace` has exactly **4 entries** (P1–P4).
- `entities.actors` non-empty; every Tier-1 actor name in `covers_entity` of ≥1 query.
- If `entities.regions` is non-anglophone, **≥30%** of queries are non-`en` using **native script**.
- At least one `monitoring`-intent query AND one `context`-intent query.
- If RAG or WebSearch fail, leave the corresponding refs array empty and note it in `reasoning_trace`. **Never crash.**

---

## Streaming progress markers

You are run with `--output-format json` OR `--output-format stream-json`. In stream mode, callers want phase-by-phase visibility. **At the start of each phase**, run a single Bash echo:

```bash
echo '{"phase":"P1","status":"start","label":"domain & frame"}'
```

Use phase IDs `P1` … `P4`. Keep the JSON one line. These echoes appear in the SSE stream as `tool_use` events for the consumer to render. Cost is negligible.

---

## Tool budget (do not exceed)

| Phase | Tool | Cap |
|-------|------|-----|
| P0    | Bash | 2 short calls (uuidgen, date) |
| P2    | RAG (curl)  | **1 call** |
| P2    | WebSearch   | **1 call** |
| P3    | (reasoning only) | — |
| P4    | (reasoning only) | — |

Run P2's RAG and WebSearch **in parallel** (one assistant turn, two tool calls).

---

## Phase 0 — Setup (no marker)

```bash
TOPIC_ID=$(uuidgen | tr 'A-Z' 'a-z')
CREATED_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)
```

Carry `TOPIC_ID` and `CREATED_AT` into the JSON as `topic_id` and `created_at`. The `topic` field is `$ARGUMENTS` verbatim.

---

## Phase 1 — Domain & frame

Echo `{"phase":"P1","status":"start","label":"domain & frame"}` then reason in scratch:

1. Restate the topic in **one sentence** → `topic_restated`.
2. Choose **one short slug** for the primary domain → `domain` (your free choice; e.g. `commodity_supply`, `equity_earnings`, `fx_rates`, `geopolitics`, `regulation`, `m_and_a`, `tech_supply_chain`, `crypto`, `weather_risk`, …).

Echo `{"phase":"P1","status":"done"}`.

---

## Phase 2 — Initial state read (parallel: 1 RAG + 1 WebSearch)

Echo `{"phase":"P2","status":"start","label":"initial state read"}`.

Read `.env` for `RAG_BASE_URL`, `RAG_TENANT_ID`, `RAG_API_KEY`. **In a single assistant turn, fire BOTH calls in parallel:**

**Call A — RAG (one query covering fundamentals + actors + market mechanics):**

```bash
source .env
curl -sS -X POST "${RAG_BASE_URL}" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: ${RAG_TENANT_ID}" \
  -H "X-API-Key: ${RAG_API_KEY}" \
  -d "{\"query\":\"<one synthesized query covering the topic's fundamentals, key actors, and market mechanics>\",\"limit\":5}"
```

Capture `results[].source` into `rag_context_refs[]` with `used_for: "context"`. Read `results[].summary` for vocabulary. If the call errors out → leave `rag_context_refs: []` and note it.

**Call B — WebSearch (one broad probe to learn current public framing and named entities):**

Use the WebSearch tool with one query. From the top results, capture up to **3 URLs** into `web_seed_refs[]` (`url`, `title`, `language` if obvious from URL/title).

Echo `{"phase":"P2","status":"done","rag_calls":1,"web_calls":1}`.

---

## Phase 3 — Entity sketch + working thesis

Echo `{"phase":"P3","status":"start","label":"entities & thesis"}`.

From P2 evidence, build **lightweight** structures (not exhaustive):

- `entities.actors` — list of actor names (strings, not objects). Mark Tier-1 vs Tier-2 by ordering: first 3 are Tier-1.
- `entities.regions` — short region tags (e.g., `gulf`, `eu`, `northeast_asia`).
- `entities.primary_languages` — ISO 639-1 codes for the languages relevant sources publish in (e.g., `["en","ar","fa"]`).
- `current_state` — **2-3 sentences** describing where the topic is **today**, grounded in P2 evidence. This is the most important narrative field.
- `working_thesis` — **2 sentences**: your current best read of the situation, opinion-bearing.

Echo `{"phase":"P3","status":"done"}`.

---

## Phase 4 — Build queries (10-15)

Echo `{"phase":"P4","status":"start","label":"build queries"}`.

Generate 10-15 queries. Distribute across:

- **`source_class`** — `primary_official` | `specialist_outlet` | `local_press` | `data_feed` | `aggregator`. At most 30% can be `aggregator`.
- **`language`** — ISO 639-1 code. **Native script** when applicable.
- **`region`** — slug from `entities.regions`.
- **`intent`** — `context` | `monitoring`. Both must appear.
- **`freshness`** — `any` | `24h` | `7d`. Most queries should be `any`; mark only true breaking-news queries as `24h`/`7d`.
- **`priority`** — integer 1 (highest) – 5 (lowest).
- **`covers_entity`** — array of entity names from `entities.actors`.
- **`rationale`** — **one short sentence** explaining the unique signal this query yields.

`id` is `q01`, `q02`, … (zero-padded). No fingerprint, no operators object, no engine field — keep it minimal.

Inline self-check before emitting:
1. Drop redundant queries (same entity + same source_class + same intent → keep highest priority).
2. Ensure ≥30% non-`en` if non-anglophone regions present.
3. Ensure both intents appear.
4. Ensure every Tier-1 actor in `covers_entity` of ≥1 query.

Echo `{"phase":"P4","status":"done","queries":<final count>}`.

---

## Final emit

Build `monitoring_plan` with a default cadence the topic warrants (`1h` / `6h` / `24h`) and a short `trigger_terms` array (verbs/keywords that mean "react now" for this topic).

Write `reasoning_trace` — exactly **4 entries**, one short prose summary per phase P1–P4, including `rag_calls` and `web_calls` in P2's entry and `queries` count in P4's entry.

**Now print the JSON object as your only output. Nothing else.**
