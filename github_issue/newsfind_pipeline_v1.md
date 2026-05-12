# Topic Pipeline Orchestrator v1 — Async State Machine, Event Stream, API-First

> **Ticket name suggestion:** `newsfind-pipeline-v1: Topic Pipeline Orchestrator + Event Stream`
>
> **One-line goal:** Wrap the existing `/newsfind-queries` Stage 1 in a multi-stage, async, API-first pipeline (Stages 1→4) with a per-topic state machine, structured event stream (SSE + webhook), and a first user-control gate — designed so prompts/agents can keep iterating freely and any modern frontend (e.g. markdown-ui / Blueprint Lab) can consume it.

---

## 1. Background

We already have:

- A working Stage 1 slash command `/newsfind-queries` that produces a structured "intelligence blueprint" JSON (`schema_version: 0.2.0`).
- A FastAPI service (`apps/claude_agent/`) exposing `/v1/agent/run`, `/v1/agent/stream`, `/v1/agent/jobs`.
- A reproducible artifact layer (`apps/claude_agent/artifacts.py` + `orchestrator.py`) that persists `request.json`, `stream.ndjson`, `raw_result.json`, `parsed.json`, `meta.json`, and `index.json` per run under `state/news/<topic_id>/runs/<run_id>/`.
- An input-fingerprint cache that prevents re-spending tokens for identical inputs (see `compute_input_fingerprint` in `artifacts.py`).
- A local debug harness `scripts/test_newsfind.sh` + `scripts/list_runs.sh` writing to `testing/runs/`.
- Hardened error propagation: structured `error` events with `stage`, `error_type`, `error`, `traceback` from both `/run` and `/stream`.

What we do **not** have yet:

- Stages 2 (intro), 3 (search), 4 (report). Stage 5 (live monitor) is explicitly out of scope for v1.
- A first-class "Topic" resource with a state machine.
- A unified event stream across stages.
- User-input gates between stages.
- Postgres-backed orchestration metadata.
- A delivery channel suitable for B2B clients (webhooks).

This ticket builds those missing pieces while preserving everything above.

---

## 2. Goals

1. **Topic = first-class resource.** A topic owns its state machine, its run history, and its delivery subscribers.
2. **Async, API-first orchestration.** A topic is started via `POST /v1/topics`, drives all stages internally, and publishes structured events. The frontend is just one consumer.
3. **User control.** At least one explicit gate (after Stage 1) where the pipeline pauses and waits for `POST /v1/topics/{id}/proceed`.
4. **Iteration-safe contracts.** Versioned JSON schemas + URL versioning + additive event types, so we can keep changing prompts/agents/output shape without breaking consumers.
5. **Markdown-ui-friendly delivery.** Every user-facing artifact has both a structured JSON view and a markdown rendition, so a markdown-ui frontend can render natively.
6. **Reproducibility preserved.** Every Stage still writes the full artifact set (request / stream / raw_result / parsed / meta) to disk under the topic's directory.
7. **B2B-ready.** SSE for in-house dashboard, webhook for hedge-fund integrations, REST poll as fallback. Same event payload over all three.
8. **No lock-in.** Prompts (`.md` slash commands) and agent behavior must remain freely editable. JSON schema changes flow through `schema_version`. Orchestration metadata stays generic enough to never need migrations for prompt changes.

## 3. Non-Goals (v1)

- Stage 5 live monitor / news channel. Designed for v2.
- Replacing the existing Stage 1 slash command — wrap, don't rewrite.
- Authentication beyond the existing `X-API-Key` (multi-tenant auth is a separate ticket).
- Multi-replica or distributed worker. Single-process asyncio is acceptable for v1.
- Replacing files with DB for heavy artifacts. Files stay.
- Any frontend code. Frontend is a separate ticket; this ticket only delivers the API and event contract that the frontend will consume.
- Real-time push from Stage 5 (live news). v1 stops at "user has read the report and could now decide to subscribe to monitoring".

---

## 4. Architecture Overview

```
┌────────────────────────────────────────────────────────────┐
│                       API LAYER                             │
│  POST /v1/topics                  create + start pipeline   │
│  GET  /v1/topics/{id}             current state + artifacts │
│  GET  /v1/topics/{id}/events      SSE event stream          │
│  POST /v1/topics/{id}/inputs      mid-process steering      │
│  POST /v1/topics/{id}/proceed     advance past a gate       │
│  POST /v1/topics/{id}/cancel                                │
│  POST /v1/topics/{id}/subscribe   register webhook (B2B)    │
│  GET  /v1/topics/{id}/parsed      Stage 1 artifact          │
│  GET  /v1/topics/{id}/intro       Stage 2 artifact (md+json)│
│  GET  /v1/topics/{id}/news        Stage 3 artifact          │
│  GET  /v1/topics/{id}/report      Stage 4 artifact (md+json)│
└────────────────────────────────────────────────────────────┘
            │                                  ▲
            ▼                                  │ SSE / webhook
┌────────────────────────────────────────────────────────────┐
│                   ORCHESTRATOR (async)                      │
│  Topic state machine  ─►  Stage runners  ─►  Event bus     │
│   created → planning → planned_awaiting_review → searching  │
│            → searched → reporting → reported (→ archived)   │
│                                                             │
│  • One asyncio.Task per active topic (Phase 1)              │
│  • Calls existing slash commands for Stages 1, 3, 4         │
│  • Stage 2 runs in pure Python (no LLM)                     │
│  • Publishes structured events for every transition         │
└────────────────────────────────────────────────────────────┘
            │                  │                    │
            ▼                  ▼                    ▼
       ┌──────────┐      ┌─────────┐         ┌───────────┐
       │ Postgres │      │  Files  │         │ Webhook   │
       │ topics   │      │ state/  │         │ delivery  │
       │ events   │      │ news/   │         │ (B2B)     │
       │ inputs   │      │ <id>/   │         │           │
       │ webhooks │      │ ...json │         │           │
       └──────────┘      └─────────┘         └───────────┘
```

**Phase 1 (v1):** orchestrator runs **inside the FastAPI process** as `asyncio.Task`s, one per active topic. Concurrency capped by a semaphore. On API restart, the orchestrator scans `topics WHERE state IN ('planning','searching','reporting','planned_awaiting_review')` and either resumes (running stages) or remains paused (awaiting gates).

**Phase 2 (out of scope for v1):** orchestrator extracted to a dedicated worker process consuming jobs from Redis. Designed in v1 by ensuring no in-memory state is shared between API request handlers and orchestrator — they communicate only through Postgres + the event bus.

---

## 5. Stage Contracts

Lock these contracts in v1. Iteration on prompt content is free; iteration on JSON keys requires a `schema_version` bump.

| Stage | Slash command | Input | Output (artifact files) | Trigger | LLM? |
|---|---|---|---|---|---|
| **1. Plan** | `/newsfind-queries` (existing) | `{topic, intro_style?, ...}` | `parsed.json` | user (POST /v1/topics) | Sonnet |
| **2. Intro** | (no slash command) | `parsed.json` | `intro.json` + `intro.md` | auto after Stage 1 | None (Python templating) |
| **3. Search** | `/newsfind-search` (NEW) | `parsed.json`, search budget | `news.json` | user `proceed` past planning gate | Sonnet/Haiku mix |
| **4. Report** | `/newsfind-report` (NEW) | `parsed.json` + `news.json` | `report.json` + `report.md` | auto after Stage 3 (no gate in v1) | Sonnet |

### 5.1 Stage 2 — Intro (Pure Python)

**Input:** `parsed.json` only.

**Why no LLM:** Stage 1 already emits client-quality prose (`topic_restated`, `current_state`, `working_thesis`). Stage 2 is **assembly**, not generation. Cheaper, instant, deterministic, never hallucinates.

**Output `intro.json`:**

```json
{
  "schema_version": "0.1.0",
  "topic_id": "...",
  "style": "trader|executive|analyst|raw",
  "headline": "<one-line restatement of the topic>",
  "understanding": "<1–2 sentence paraphrase of topic_restated>",
  "current_state_short": "<≤3 sentences from current_state>",
  "working_thesis_short": "<≤2 sentences from working_thesis>",
  "approach": {
    "queries_count": 13,
    "languages": ["en", "ar", "fa"],
    "regions": ["gulf", "northeast_asia", "eu", "north_america"],
    "key_actors_top5": ["Iran (IRGC)", "United States (DoE)", "..."]
  },
  "highlights": [
    "Will search 13 angles in 4 languages",
    "Working thesis: ...",
    "Will check ceasefire status, SPR releases, bypass pipeline utilization"
  ],
  "next_step": "Press Proceed to begin web search and source collection."
}
```

**Output `intro.md`:** the same content rendered as markdown, ready for markdown-ui consumption. Must reference custom components by name when appropriate (e.g. `<EntityChips entities="..."/>`, `<Highlights items="..."/>`); fallback to plain markdown when not.

**Optional Haiku polish (opt-in via `intro_style`):** `style="executive"` or non-`en` requested locale → invoke a Haiku call to translate / re-tone. Defaults to plain Python.

**Hard rule:** Stage 2 MUST NOT invent facts. It only restructures `parsed.json`.

### 5.2 Stage 3 — Search (`/newsfind-search`)

**Input:** `parsed.json`. Must extract only:

- `topic_restated`
- `entities` (actors, regions, languages)
- `queries[]` (with their budgets)
- `monitoring_plan.trigger_terms`

Drop `reasoning_trace`, `scenarios`, `working_thesis` — those are not needed for retrieval.

**Behavior:**

- Execute each query against the configured search backend.
- Apply per-query freshness filter (`24h | 7d | 30d | any`) where supported.
- Fetch / scrape candidate articles when needed (cap WebFetch).
- Deduplicate by URL hash + title hash + 24h window.
- Score each article for relevance to (`entities`, `working_thesis`, `trigger_terms`) — Haiku is acceptable here for cost.
- Return a structured news collection.

**Output `news.json`:**

```json
{
  "schema_version": "0.1.0",
  "topic_id": "...",
  "executed_queries": [
    { "id": "q01", "query": "...", "results_count": 5 }
  ],
  "sources": [
    {
      "id": "s01",
      "url": "...",
      "url_hash": "...",
      "title": "...",
      "publisher": "...",
      "published_at": "<iso>",
      "language": "en",
      "snippet": "...",
      "query_ids": ["q01", "q07"],
      "source_class": "primary_official",
      "relevance_score": 0.83,
      "novelty_score": 0.7
    }
  ],
  "drops": {
    "deduped": 12,
    "low_relevance": 27,
    "off_topic": 3
  },
  "search_budget_used": {
    "queries_executed": 13,
    "web_searches": 13,
    "web_fetches": 6,
    "haiku_score_calls": 47
  }
}
```

### 5.3 Stage 4 — Report (`/newsfind-report`)

**Input:** Stage 1 `parsed.json` (selected fields) + Stage 3 `news.json` (titles + snippets + URLs only — NOT full article bodies).

**Behavior:**

- Synthesize a long-form expert report grounded in cited sources.
- Update / contrast the Stage 1 working thesis with new evidence.
- For each scenario in Stage 1, mark whether news supports / weakens / kills it.
- Assign each "key finding" a confidence band and citations.
- Identify open questions and recommended next searches.

**Output `report.json`:**

```json
{
  "schema_version": "0.1.0",
  "topic_id": "...",
  "summary_md": "<≤300 words executive summary in markdown>",
  "report_md": "<full markdown report — section-structured, citations as [s01], [s02]>",
  "key_findings": [
    {
      "finding": "...",
      "confidence": "high|medium|low",
      "source_ids": ["s01", "s12"]
    }
  ],
  "scenario_updates": [
    { "id": "S1", "label": "Base", "p_before": 0.50, "p_after": 0.45, "rationale": "...", "evidence_ids": ["s03","s09"] }
  ],
  "thesis_status": "supported|weakened|invalidated|inconclusive",
  "thesis_update_md": "<short markdown explaining how the thesis evolves>",
  "open_questions": ["..."],
  "next_queries": [
    { "q": "...", "intent": "monitoring", "rationale": "..." }
  ]
}
```

**Output `report.md`:** the markdown body extracted from `report_md`, suitable for direct markdown-ui rendering. May include domain-specific custom components.

---

## 6. Topic State Machine

```
created
  └─► planning             (Stage 1 running)
       ├─► failed
       └─► planned_awaiting_review
            ├─► cancelled
            ├─► searching   (after POST /proceed)
            │    ├─► failed
            │    └─► searched
            │         └─► reporting
            │              ├─► failed
            │              └─► reported
            │                   └─► archived (manual or TTL)
            └─► (if no gate configured) → searching directly
```

**State invariants:**

- A topic is in exactly one state at any instant.
- Every transition produces an event in `topic_events`.
- `failed` carries `failed_at_stage`, `error_type`, `error`, `traceback`.
- `cancelled` is allowed from any non-terminal state.
- Resumability: on API startup, scan `topics WHERE state IN ('planning','searching','reporting')`. If a stage was running, restart it (idempotent — Stage 1 is fingerprint-cached; Stage 3/4 must also be idempotent on `topic_id` + input fingerprint).

**Gates v1:** only one gate is shipped: `planned_awaiting_review`. The pipeline pauses indefinitely after Stage 1+2 until the user calls `POST /v1/topics/{id}/proceed`. Future tickets can add more gates by extending the state machine.

---

## 7. Storage

### 7.1 Postgres (orchestration metadata)

This is the right time to introduce Postgres for orchestration. Tables are intentionally generic so prompt iteration cannot force a migration.

```sql
-- Core topic state machine
CREATE TABLE topics (
  id              UUID PRIMARY KEY,
  topic           TEXT NOT NULL,
  topic_id_hash   TEXT NOT NULL,   -- = current artifacts/topic_id_from_args(args)
  state           TEXT NOT NULL,   -- enum-ish, but stored as text for flexibility
  current_stage   TEXT,            -- 'queries'|'intro'|'search'|'report' or NULL
  request         JSONB NOT NULL,  -- the original POST body
  failed_at_stage TEXT,
  error           TEXT,
  traceback       TEXT,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  archived_at     TIMESTAMPTZ
);

-- Append-only event log (drives SSE replay + audit)
CREATE TABLE topic_events (
  id          BIGSERIAL PRIMARY KEY,
  topic_id    UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
  seq         BIGINT NOT NULL,        -- per-topic monotonically increasing
  event_type  TEXT NOT NULL,          -- 'stage.started', 'state.changed', etc.
  event_version TEXT NOT NULL DEFAULT '1',
  payload     JSONB NOT NULL,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(topic_id, seq)
);
CREATE INDEX ON topic_events (topic_id, id);

-- User input messages (gate proceed, focus hints, etc.)
CREATE TABLE topic_inputs (
  id          BIGSERIAL PRIMARY KEY,
  topic_id    UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
  kind        TEXT NOT NULL,          -- 'proceed' | 'focus' | 'clarify' | 'constraint'
  payload     JSONB NOT NULL,
  consumed_at TIMESTAMPTZ,            -- NULL until orchestrator processes it
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX ON topic_inputs (topic_id, consumed_at);

-- Webhook subscribers (B2B integrations)
CREATE TABLE topic_webhooks (
  id           BIGSERIAL PRIMARY KEY,
  topic_id     UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
  url          TEXT NOT NULL,
  secret       TEXT,                   -- HMAC signing key
  event_filter TEXT[],                 -- e.g. ['report.ready','news.added']; NULL = all
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  disabled_at  TIMESTAMPTZ
);
```

Use Alembic for migrations (`alembic.ini` already exists in repo).

### 7.2 Files (artifacts — unchanged philosophy)

```
state/news/<topic_id_hash>/
  index.json
  runs/<run_id>/
    request.json
    stream.ndjson
    raw_result.json
    parsed.json       ← Stage 1 (existing)
    intro.json        ← Stage 2 (NEW)
    intro.md          ← Stage 2 (NEW)
    news.json         ← Stage 3 (NEW)
    report.json       ← Stage 4 (NEW)
    report.md         ← Stage 4 (NEW)
    meta.json
```

The existing `topic_id_hash` derivation (sha1 of normalized args) is preserved. The Postgres `topics.id` is a NEW UUID (different from the hash) so the same args submitted by different users produce different topics.

`index.json` MAY include cross-stage pointers (`latest_intro_path`, `latest_news_path`, `latest_report_path`) so command-line debug stays easy.

---

## 8. API Contracts

All endpoints under `/v1/`. All payloads JSON. All errors structured (`{error, error_type, traceback?}`).

### 8.1 Create + Start a Topic

```http
POST /v1/topics
Content-Type: application/json
X-API-Key: ...

{
  "topic": "Hormuz strait closure options to lower price",
  "intro_style": "trader",                      // optional, default "raw"
  "stages": ["queries","intro","search","report"], // optional; default all
  "gates": ["planned_awaiting_review"],         // optional; default this one
  "force_refresh": false,                       // optional
  "webhook": {                                  // optional
    "url": "https://client.example.com/hook",
    "secret": "shared-secret"
  }
}

→ 202 Accepted
{
  "topic_id": "01HX...",
  "state": "planning",
  "events_url": "/v1/topics/01HX.../events"
}
```

### 8.2 Status

```http
GET /v1/topics/{id}
→ {
  "id": "01HX...",
  "state": "planned_awaiting_review",
  "current_stage": "queries",
  "stages_done": ["queries","intro"],
  "artifacts": {
    "parsed":  "/v1/topics/01HX.../parsed",
    "intro":   "/v1/topics/01HX.../intro",
    "news":    null,
    "report":  null
  },
  "available_actions": ["proceed","input","cancel"],
  "error": null,
  "created_at": "...",
  "updated_at": "..."
}
```

### 8.3 Live Event Stream (SSE)

```http
GET /v1/topics/{id}/events?from_seq=0
Accept: text/event-stream
```

- If `from_seq=N`, server replays all events with `seq > N` from `topic_events`, then keeps the connection open for new events.
- Each event:

```
id: 42
event: stage.finished
data: { ... }
```

- Heartbeat every 15s to keep proxies happy: `:heartbeat\n\n`.

### 8.4 Mid-Process Input

```http
POST /v1/topics/{id}/inputs
{
  "kind": "focus",                  // or "clarify" | "constraint"
  "payload": { "focus": "asia_lng_market" }
}
→ 202 { "accepted": true, "applies_to_next_stage": "search" }
```

In v1, only the **proceed** action is fully wired (advance past a gate). Other input kinds are accepted, persisted to `topic_inputs`, and logged — but the orchestrator does not yet read them. Future stages will drain pending inputs at the start of each stage.

### 8.5 Proceed Past Gate

```http
POST /v1/topics/{id}/proceed
{ "from_state": "planned_awaiting_review" }
→ 202 { "accepted": true, "new_state": "searching" }
```

If `from_state` does not match the current state → 409.

### 8.6 Cancel

```http
POST /v1/topics/{id}/cancel
→ 202 { "accepted": true }
```

Cancels the asyncio task (if any), kills the Claude subprocess (if running), transitions to `cancelled`, emits event.

### 8.7 Subscribe (Webhook)

```http
POST /v1/topics/{id}/subscribe
{
  "url": "https://...",
  "secret": "...",
  "event_filter": ["stage.finished","report.ready","needs_input"]
}
→ 201 { "subscription_id": 7 }
```

Server POSTs each matching event to the URL with `X-Signature: sha256=<hmac(secret, body)>` header.

### 8.8 Artifact Endpoints

Each returns the corresponding JSON file (or 404 if not yet produced):

- `GET /v1/topics/{id}/parsed`
- `GET /v1/topics/{id}/intro`        (returns `intro.json`)
- `GET /v1/topics/{id}/intro.md`     (returns `intro.md` as `text/markdown`)
- `GET /v1/topics/{id}/news`
- `GET /v1/topics/{id}/report`       (returns `report.json`)
- `GET /v1/topics/{id}/report.md`    (returns `report.md` as `text/markdown`)

---

## 9. Event Types (v1)

All events have at minimum: `seq`, `event_type`, `event_version`, `topic_id`, `created_at`, `payload`.

| event_type | When | Payload (selected) |
|---|---|---|
| `topic.created` | After `POST /v1/topics` | `{topic, request}` |
| `state.changed` | Every state transition | `{from, to, reason?}` |
| `stage.started` | Stage begins | `{stage, run_id}` |
| `stage.progress` | Optional sub-stage marker (e.g. Stage 1 phase echoes) | `{stage, phase, message?}` |
| `stage.finished` | Stage completes successfully | `{stage, run_id, artifact_path}` |
| `intro.ready` | After Stage 2 | `{summary_short, highlights}` |
| `news.added` | Per article during Stage 3 | `{source_id, title, url, score}` |
| `news.batch_done` | After Stage 3 finishes | `{count, drops}` |
| `report.ready` | After Stage 4 | `{summary_md, thesis_status}` |
| `needs_input` | At a gate | `{gate, prompt, available_inputs}` |
| `input.received` | After `POST /inputs` | `{kind, payload}` |
| `cancelled` | After `POST /cancel` | `{reason?}` |
| `error` | Any stage failure | `{stage, error_type, error, traceback}` |

**Versioning:** new event types are additive (free). Renaming or breaking-change to an existing event requires bumping `event_version` and supporting both for one release.

---

## 10. User Input Model

Two patterns exist; v1 ships only A.

**A. Gate (paused waiting for user)** — implemented in v1
- Pipeline transitions to `planned_awaiting_review`.
- Emits `needs_input` event.
- Waits indefinitely (no timeout in v1).
- Resumes on `POST /v1/topics/{id}/proceed`.

**B. Steering (running pipeline reads pending hints)** — designed but NOT implemented in v1
- API accepts and persists inputs at any time.
- Each stage, at start, drains pending `topic_inputs` and folds them into its prompt.
- v1 stores them in `topic_inputs` and emits `input.received`, but no stage consumes them yet. This keeps the API surface forward-compatible.

---

## 11. Iteration Safety / Versioning Rules

Non-negotiable disciplines that protect us from lock-in:

1. **URL versioning:** all endpoints under `/v1/`.
2. **JSON schema versioning:** every artifact JSON has `schema_version`. Bump on breaking change; emit both for one release.
3. **Event versioning:** every event has `event_version`. Add new event types freely; never silently change an existing payload.
4. **Frontend reads ONLY the API.** Never touches `state/news/...` directly.
5. **Additive > breaking.** Add `news_v2.json` next to `news.json` for one release before retiring the old shape.
6. **Prompt iteration is free.** Editing `.md` slash command files only changes the input fingerprint and triggers a fresh Claude call. No schema impact.
7. **Postgres tables stay generic.** `payload JSONB` for events/inputs absorbs all prompt evolution without migrations.

---

## 12. Frontend Integration (markdown-ui / Blueprint Lab)

The frontend is **not** part of this ticket, but the API contract here is built for it.

- **Both formats per stage:** every user-facing stage (Intro, Report) emits both `*.json` (structured) and `*.md` (markdown for direct rendering).
- **Markdown components:** Stage 2 + Stage 4 may emit markdown referencing custom components like `<EntityChips actors="..."/>`, `<Highlights items="..."/>`, `<NewsCard source-id="s01"/>`, `<ScenarioTree scenarios="..."/>`. The frontend defines these components; the backend never renders HTML.
- **Live updates via SSE:** the frontend opens `GET /v1/topics/{id}/events`. State changes drive UI navigation; per-stage events update local component state.
- **Action buttons:** the frontend reads `available_actions` from `GET /v1/topics/{id}` and renders Proceed / Cancel / Input controls accordingly.
- **B2B integration parity:** webhook subscribers receive the exact same event payloads as SSE consumers — no special path.

---

## 13. Build Order

Each step is a small, independently shippable PR. The next agent should follow this order. Do **not** start Stage 5 in this ticket.

1. **Postgres schema + Alembic migration** — `topics`, `topic_events`, `topic_inputs`, `topic_webhooks`. No code wired yet. Verify migration up/down.
2. **Topic resource scaffolding** — `POST /v1/topics`, `GET /v1/topics/{id}`. Persist row, return state. No orchestrator yet (state stays at `created`).
3. **In-process orchestrator + Stage 1 wrapper** — `POST /v1/topics` enqueues an `asyncio.Task` that runs Stage 1 via the existing orchestrator code, persists `topic_events` for `state.changed`, `stage.started`, `stage.finished`. Validate: a topic created via API now produces `parsed.json` exactly as the existing standalone command does.
4. **SSE event stream** — `GET /v1/topics/{id}/events` with replay-from-seq support. Validate end-to-end with `curl -N`.
5. **Stage 2 (intro) — pure Python** — emits `intro.json` + `intro.md` and `intro.ready` event after Stage 1.
6. **Gate `planned_awaiting_review` + `POST /proceed`** — the first user-control surface. `needs_input` event emitted. Pipeline waits.
7. **Stage 3 (`/newsfind-search`) — slash command + orchestrator wrapper + artifacts** — emits `news.added` per article and `stage.finished` at end. New slash command file under `claude_agent_fe/.claude/commands/newsfind-search.md` with its own JSON schema in `.claude/schemas/`.
8. **Stage 4 (`/newsfind-report`) — slash command + orchestrator wrapper + artifacts** — emits `report.ready`.
9. **Webhook subscriptions** — `POST /v1/topics/{id}/subscribe` + delivery worker (HMAC signed, retry policy). Same event payload as SSE.
10. **Artifact endpoints** — `GET /v1/topics/{id}/{parsed|intro|news|report}` (json + .md variants).
11. **Cancellation + resumability** — `POST /cancel`, plus startup hook that re-enqueues in-flight topics from Postgres.
12. **CLI / docs** — extend `scripts/test_newsfind.sh` (or add `scripts/test_topic.sh`) to drive a full pipeline via the new API; update `claude_agent_fe/app_testing_scenario.md` and `debugging_readme.md` accordingly.

---

## 14. Open Decisions To Resolve Before Coding

The next agent must surface these and get explicit answers from the user:

1. **Search backend.** Tavily / Brave / Serper / SearXNG / WebSearch via Claude itself? Determines API key, env var name, rate limits, cost.
2. **Stage 3 budget defaults.** Max queries to execute? Max WebFetches? Max Haiku scoring calls per topic? Pick safe defaults.
3. **Relevance scoring model.** Haiku at score time, or rules-based with Sonnet for borderline cases?
4. **Topic ID strategy.** UUID server-generated (recommended) vs user-supplied slug.
5. **Gate-after-Stage-3?** Should there be a "review news before report" gate in v1, or auto-flow to Stage 4? Recommendation: no gate in v1; add later.
6. **Markdown components vocabulary.** Concrete list of components Stage 2/4 may emit. Coordinate with frontend ticket.
7. **Webhook retry policy.** Max retries, backoff, dead-letter behavior.
8. **TTL / archival.** When does a topic become `archived`? Manual only, or after N days idle?

---

## 15. Definition of Done

- [ ] Postgres tables exist and are reachable from the API container.
- [ ] `POST /v1/topics` creates a topic, drives Stages 1→2 automatically, pauses at `planned_awaiting_review`, emits all events.
- [ ] `POST /v1/topics/{id}/proceed` advances through Stages 3→4 to `reported`.
- [ ] `GET /v1/topics/{id}` returns the correct state and artifact pointers at every step.
- [ ] `GET /v1/topics/{id}/events` streams SSE in real time AND replays past events from `from_seq`.
- [ ] All four artifact endpoints return their JSON; `intro.md` and `report.md` return `text/markdown`.
- [ ] `POST /v1/topics/{id}/cancel` cleanly stops a running pipeline and transitions state.
- [ ] `POST /v1/topics/{id}/subscribe` registers a webhook; events are delivered to the URL with HMAC signature.
- [ ] Restarting the claude_agent container resumes any in-flight topic without data loss.
- [ ] End-to-end demo on the Hormuz topic produces `parsed.json` + `intro.json` + `intro.md` + `news.json` + `report.json` + `report.md` and a complete `topic_events` row set.
- [ ] All artifact JSONs include `schema_version`; all events include `event_version`.
- [ ] `scripts/test_topic.sh` (or extended `test_newsfind.sh`) drives the whole flow from CLI and prints a friendly transcript.
- [ ] `debugging_readme.md` updated with the new failure modes (DB unreachable, gate stuck, webhook failing).
- [ ] No regression in the existing `/v1/agent/run` and `/v1/agent/stream` endpoints — they continue to serve the standalone Stage 1 command.

---

## 16. References

Existing code the next agent should read first:

- `apps/claude_agent/app.py` — FastAPI bootstrap, lifespan
- `apps/claude_agent/routes.py` — current `/v1/agent/*` endpoints (the new `/v1/topics/*` endpoints live alongside, not replacing)
- `apps/claude_agent/orchestrator.py` — Stage 1 orchestration logic; the new pipeline orchestrator extends this pattern per stage
- `apps/claude_agent/artifacts.py` — `ArtifactStore`, `RunRecorder`, `compute_input_fingerprint`, `topic_id_from_args` — REUSED by every stage
- `apps/claude_agent/schemas.py` — `RunRequest`, `RunResult`, `JobStatus`
- `apps/claude_agent/config.py` — settings prefix `CLAUDE_AGENT_`; new settings live here
- `claude_agent_fe/.claude/commands/newsfind-queries.md` — Stage 1 prompt, model for new stage commands
- `claude_agent_fe/.claude/schemas/newsfind-queries.schema.json` — Stage 1 output schema, model for new schemas
- `docker-compose.yml` — `claude_agent` service definition; Postgres already wired
- `database/` and `alembic.ini` — existing migration setup
- `scripts/test_newsfind.sh` — debug harness pattern
- `agent_framework.md` — long-term framework vision (informational)
- `debugging_readme.md` — runtime debugging recipes (extend with new failure modes)
- `testing/runs/<latest>/parsed.json` — concrete example of Stage 1 output

Out-of-scope but relevant for context:

- `apps/rag_adhoc/` — RAG service used by Stage 1 (will be re-used by Stage 3)
- `apps/signal_gather/` — sibling app, not modified by this ticket
