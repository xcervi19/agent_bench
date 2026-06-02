# Agentic Search — Structured Claude Code Architecture (#9)

Status: **done**

## Goal

Transform ad-hoc search scripts into a structured multi-stage pipeline ("Claude Code" slash commands) that enables machine processing, agent orchestration, and continuous monitoring of trading-relevant topics.

## What was implemented

### Pipeline stages

| Stage | Slash command | Input | Output |
|---|---|---|---|
| **Plan** | `/newsfind-plan` | Topic string + RAG context | `parsed.json` (entities, queries, working thesis, monitoring plan) |
| **Gate** | API: `POST /proceed` | Human review of plan | State transition `planned_awaiting_review → delivering` |
| **Deliver** | `/newsfind-deliver` | `parsed.json` queries | `news.json` (scored sources), `report.json` + `report.md` (structured report with `[s01]` citations) |
| **Monitor** | API: `POST /monitor` | Plan + report artifacts | `TopicSubscription` with auto-built short-term query plan (up to 12 queries) |
| **Refresh** | `/newsfind-refresh` | `input.json` (queries, seen URL hashes, since_iso) | `news.json` (new sources only), `delta.json`, `report.md`, `summary.json` |

### Topic state machine

```
planning → planned_awaiting_review → delivering → reported → (monitor/refresh cycles)
                                                    ↘ failed
```

### Orchestration layer (`apps/claude_agent/topics/`)

- **`pipeline.py`** — `run_plan()`, `run_deliver()`, `_run_slash()` — spawns Claude CLI subprocess, streams SSE events, reads summary artifacts from disk.
- **`refresh.py`** — `run_refresh()`, `build_short_term_queries()` — per-topic DB lock, dedup via `seen_url_hashes`, error handling for `CommandNotAllowedError`.
- **`routes.py`** — Full REST API: CRUD topics, `/proceed` gate, `/monitor`, `/refresh`, `/events` (SSE), `/deltas`, artifact endpoints (`/parsed`, `/news`, `/report`, `/deltas/{seq}/news`, `/deltas/{seq}/report`).
- **`models.py`** — `Topic`, `TopicEvent`, `TopicSubscription`, `TopicRefreshDelta`, `TopicWebhook`.
- **`db.py`** — Async SQLAlchemy session scope.

### SSE event streaming

`GET /v1/topics/{id}/events` streams real-time events: `topic.created`, `stage.started`, `tool_use`, `tool_result`, `stage.finished`, `refresh.started`, `refresh.completed`, `refresh.failed`. SSE stays open during active refresh even for `reported` topics.

### Artifact system

Each run produces files in `state/news/<topic_hash>/runs/<run_id>/`:
- Plan: `parsed.json`, `intro.json`, `intro.md`, `summary.json`
- Deliver: `news.json` (source registry with URLs, relevance scores, source classes), `report.json`, `report.md`, `summary.json`
- Refresh: `input.json`, `news.json` (new sources only), `delta.json`, `report.md`, `summary.json`

### DB migrations

- `0003_newsfind_topics.py` — `topics`, `topic_events`, `topic_webhooks` tables
- `0004_newsfind_monitoring.py` — `topic_subscriptions`, `topic_refresh_deltas` tables

### Test scripts

- `scripts/test_vector_runner.sh` — Canonical end-to-end runner (plan → deliver → refresh), resumable, writes `testing/results/<env>/...` artifacts.
- `scripts/qa_check_run.sh` — Mechanical PASS/FAIL gate on run artifacts (`qa_report.json`).
- `scripts/test_refresh_cycle.sh` — Refresh-only debug run for an already reported topic.
- `scripts/legacy/test_full_pipeline.sh` + `scripts/legacy/test_continue_topic.sh` — legacy fallback scripts.
- `testing/.env.testing` — VPS/API/DB config for test scripts.

## Mapping to original requirements

| Requirement | Implementation |
|---|---|
| Reasoning & Query Generation (RAG Context) | `/newsfind-plan` reads RAG data, outputs `parsed.json` with typed queries, entities, working thesis |
| Search Execution & Initial Report | `/newsfind-deliver` executes queries via `WebSearch`/`WebFetch`, produces scored `news.json` + structured `report.md` with inline citations |
| Advanced Search & Complementary Data | `/newsfind-refresh` runs short-term monitoring queries, deduplicates against all prior runs via `seen_url_hashes`, freshness filter via `max_age_hours` |
| "Claude Code" Architecture | Slash commands in `.claude/commands/`, JSON artifact contracts between stages, subprocess orchestration via `runner.py` |
| State extensibility | Topic stays `reported`, user can trigger unlimited refresh cycles without losing context. All prior sources tracked for dedup. |

## Known limitations

- Refresh is manual-only (no auto-scheduler yet)
- Report citations `[s01]` are opaque labels — no automated resolution to clickable URLs
- No retry/backoff on Claude subprocess failures
