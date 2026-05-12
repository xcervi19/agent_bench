# Implementation: Topic Pipeline Orchestrator v1 (`newsfind-pipeline-v1`)

**Status:** ✅ Implemented
**Related Issue:** `github_issue/newsfind_pipeline_v1.md`
**Date:** May 10, 2026

---

## What was built

A multi-stage, async, API-first pipeline that wraps `/newsfind-queries` (Stage 1) and adds Stages 2 (intro), 3 (search), 4 (report), with a per-topic state machine, structured event stream (SSE + webhook), and a first user-control gate. Stage 5 (live monitor) is intentionally out of scope.

```
created → planning → planned_awaiting_review (GATE) → searching → searched
                                                                    └─► reporting → reported
```

### New code

```
apps/claude_agent/
  app.py                                  ← lifespan wires TopicSupervisor + EventBus, resumes in-flight topics
  config.py                               ← +database_url, +max_concurrent_topics, webhook + search settings
  runner.py                               ← stream_claude finally-block now kills orphan subprocess on cancel
  topics/
    __init__.py
    db.py                                 ← async SQLAlchemy engine/session (independent of agentic_core)
    state.py                              ← TopicState enum + transition table
    models.py                             ← ORM: Topic, TopicEvent, TopicInput, TopicWebhook
    schemas.py                            ← Pydantic: CreateTopicRequest, TopicResponse, EventOut, …
    events.py                             ← EventBus (in-memory pub/sub) + emit() (DB-persist + fan-out)
    webhooks.py                           ← HMAC-signed delivery with retry/backoff + auto-disable
    orchestrator.py                       ← TopicSupervisor: per-topic asyncio task + gate handling + resume
    routes.py                             ← /v1/topics/* HTTP API (FastAPI router)
    stages/
      types.py                            ← StageResult dataclass
      queries.py                          ← Stage 1 wrapper (reuses existing run_newsfind_queries)
      intro.py                            ← Stage 2 (pure Python — no LLM)
      search.py                           ← Stage 3 wrapper around /newsfind-search
      report.py                           ← Stage 4 wrapper around /newsfind-report

claude_agent_fe/.claude/
  commands/newsfind-search.md             ← Stage 3 prompt
  commands/newsfind-report.md             ← Stage 4 prompt
  schemas/newsfind-search.schema.json     ← Stage 3 output schema (v0.1.0)
  schemas/newsfind-report.schema.json     ← Stage 4 output schema (v0.1.0)

database/migrations/versions/
  0003_newsfind_topics.py                 ← Postgres tables: topics, topic_events, topic_inputs, topic_webhooks

scripts/
  test_topic.sh                           ← end-to-end CLI: create → wait gate → proceed → report
```

### API surface (all under `/v1/topics/*`)

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/v1/topics` | create + start a topic (returns `topic_id`, `events_url`) |
| `GET`  | `/v1/topics/{id}` | current state + artifact pointers + available actions |
| `GET`  | `/v1/topics/{id}/events?from_seq=N` | SSE — replays past events then tails live |
| `POST` | `/v1/topics/{id}/proceed` | advance past `planned_awaiting_review` gate |
| `POST` | `/v1/topics/{id}/inputs` | persist user steering (`focus`/`clarify`/`constraint`/`proceed`) |
| `POST` | `/v1/topics/{id}/cancel` | cancel running pipeline (kills orphan CLI subprocess) |
| `POST` | `/v1/topics/{id}/subscribe` | register a webhook (HMAC-signed) |
| `GET`  | `/v1/topics/{id}/parsed` | Stage 1 `parsed.json` |
| `GET`  | `/v1/topics/{id}/intro` `…/intro.md` | Stage 2 |
| `GET`  | `/v1/topics/{id}/news` | Stage 3 `news.json` |
| `GET`  | `/v1/topics/{id}/report` `…/report.md` | Stage 4 |

All event payloads carry `event_version: "1"`. Adding new event types is free; renaming requires a version bump.

---

## Deployment

### TL;DR for the VPS

```bash
# On your local machine
git add -A && git commit -m "newsfind-pipeline-v1" && git push origin main

# On the VPS (79.143.179.212)
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212
cd ~/agent_bench
git pull origin main

# Configure env (see "ENV" section below for the full list)
$EDITOR .env
$EDITOR apps/claude_agent/.env

# Build images, migrate DB, restart services
docker compose build api claude_agent
docker compose up -d postgres                  # 1. DB first
docker compose up -d api                       # 2. api runs `alembic upgrade head` on entrypoint
                                               #    → 0003_newsfind_topics is applied here
docker compose up -d claude_agent              # 3. claude_agent picks up new tables on boot

# Verify
docker compose logs -f --tail=200 claude_agent
curl -fsS http://127.0.0.1:8002/readyz
curl -fsS http://127.0.0.1:8002/v1/topics/00000000-0000-0000-0000-000000000000 \
     -H "X-API-Key: $CLAUDE_AGENT_API_KEY"     # → 404 (proves the route exists; DB up)
```

### 1. Docker

The compose file already wires everything; the only structural change is that `claude_agent` now `depends_on:` `postgres` (healthy) and `api` (started, so migrations have run).

```yaml
claude_agent:
  build:
    context: .
    dockerfile: docker/Dockerfile.claude_agent
  env_file:
    - .env
    - apps/claude_agent/.env
  environment:
    CLAUDE_AGENT_DATABASE_URL: postgresql+asyncpg://${POSTGRES_USER:-agentic}:${POSTGRES_PASSWORD:-agentic}@postgres:5432/${POSTGRES_DB:-agentic}
  depends_on:
    postgres: { condition: service_healthy }
    api:      { condition: service_started }
  ports:
    - "8002:8002"
```

Sequence on the VPS:

```bash
# Pull source + new schemas + new slash commands
cd ~/agent_bench
git pull origin main

# Rebuild only what changed (new code is in claude_agent; api unchanged)
docker compose build claude_agent

# If you also changed agentic_core / migrations, rebuild api too:
docker compose build api

# Restart in the right order so migrations land before claude_agent boots
docker compose up -d postgres
docker compose up -d api          # entrypoint-api.sh: `alembic upgrade head` → 0003 lands here
docker compose up -d claude_agent

# Tail logs
docker compose logs -f api claude_agent
```

### 2. Database

The migration `0003_newsfind_topics` adds four tables (no RLS, no tenant isolation in v1):

| Table | Purpose |
|---|---|
| `topics` | one row per topic (state machine + per-stage `*_run_id` pointers) |
| `topic_events` | append-only event log (drives SSE replay + audit) |
| `topic_inputs` | user steering messages (consumed by future stages) |
| `topic_webhooks` | B2B subscribers (HMAC secret optional) |

Apply manually if you need to (the api container already does this on boot):

```bash
docker compose run --rm api alembic upgrade head
# or, into a running api:
docker compose exec api alembic upgrade head
docker compose exec api alembic current      # should show 0003_newsfind_topics
```

Roll back the topic tables (keeps everything else intact):

```bash
docker compose exec api alembic downgrade 0002_signal_gather
```

Inspect:

```bash
docker compose exec postgres psql -U agentic -d agentic -c '\dt'
docker compose exec postgres psql -U agentic -d agentic \
  -c 'SELECT id, state, current_stage, created_at FROM topics ORDER BY created_at DESC LIMIT 10;'
docker compose exec postgres psql -U agentic -d agentic \
  -c 'SELECT topic_id, seq, event_type FROM topic_events ORDER BY id DESC LIMIT 20;'
```

### 3. Environment variables

Add to `apps/claude_agent/.env` (and/or repo `.env`). Defaults are designed so a fresh checkout works inside `docker compose up`.

```bash
# === Topic pipeline (newsfind-pipeline-v1) ===

# Required for /v1/topics/* (otherwise endpoints return 503).
# In docker-compose this is auto-wired from POSTGRES_* — only set explicitly
# when running outside compose.
CLAUDE_AGENT_DATABASE_URL=postgresql+asyncpg://agentic:agentic@postgres:5432/agentic

# How many topics may run in parallel (one asyncio task per topic).
CLAUDE_AGENT_MAX_CONCURRENT_TOPICS=8

# Webhook delivery
CLAUDE_AGENT_WEBHOOK_MAX_RETRIES=3
CLAUDE_AGENT_WEBHOOK_INITIAL_BACKOFF_SEC=2
CLAUDE_AGENT_WEBHOOK_REQUEST_TIMEOUT_SEC=10

# Stage-3 search budget
CLAUDE_AGENT_SEARCH_MAX_QUERIES=15
CLAUDE_AGENT_SEARCH_PER_QUERY_TIMEOUT_SEC=120

# Markdown components vocabulary version (Stage 2 + Stage 4)
CLAUDE_AGENT_MD_COMPONENTS_VERSION=1

# === Allowlist must include the new slash commands ===
# (already updated in apps/claude_agent/.env in this PR)
CLAUDE_AGENT_ALLOWED_COMMANDS=["/trader","/trade-update","/trade-intel","/trade-flash","/trade-situation","/signal-extractor","/rag-search","/rag-query-builder","/newsfind-queries","/newsfind-search","/newsfind-report"]

# === Existing required vars (unchanged) ===
CLAUDE_AGENT_API_KEY=...                          # X-API-Key header value
CLAUDE_AGENT_WORKSPACE_DIR=/workspace/claude_agent_fe
CLAUDE_AGENT_STATE_DIR=/state
CLAUDE_AGENT_STATE_INDEX_PREFIX=state
CLAUDE_AGENT_SCHEMA_VERSION=0.2.0
CLAUDE_AGENT_ENV_VERSION=1
```

The repo `.env` (top-level) needs Postgres credentials for compose interpolation:

```bash
POSTGRES_DB=agentic
POSTGRES_USER=agentic
POSTGRES_PASSWORD=<pick-a-real-one-on-the-VPS>
```

If you change `POSTGRES_PASSWORD`, also update `CLAUDE_AGENT_DATABASE_URL` (or remove it from `apps/claude_agent/.env` and let compose interpolation rebuild it from `POSTGRES_*`).

### 4. End-to-end smoke test

```bash
# From your local machine, point at the VPS:
export API=http://79.143.179.212:8002
export CLAUDE_AGENT_API_KEY=<value from VPS .env>

# Drives Stage 1 → 2 → GATE → 3 → 4 and pulls every artifact
scripts/test_topic.sh "Hormuz strait closure options to lower price"

# Result tree: testing/runs/<UTC>__topic__<slug>/
#   create_request.json
#   create_response.json
#   events.ndjson           ← every SSE event seen
#   intro.md                ← rendered at the gate
#   parsed.json
#   intro.json / intro.md
#   news.json
#   report.json / report.md
#   topic.json              ← final GET /v1/topics/{id}
```

Manual flow (curl):

```bash
# 1. Create
curl -X POST $API/v1/topics \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"topic":"Hormuz strait closure options to lower price","intro_style":"trader"}'
# → {"topic_id":"<UUID>","state":"planning","events_url":"/v1/topics/<UUID>/events"}

# 2. Tail SSE in another shell
curl -N "$API/v1/topics/<UUID>/events" -H "X-API-Key: $CLAUDE_AGENT_API_KEY"

# 3. Once you see {"event_type":"needs_input"}, proceed:
curl -X POST $API/v1/topics/<UUID>/proceed \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"from_state":"planned_awaiting_review"}'

# 4. After report.ready, fetch the report:
curl $API/v1/topics/<UUID>/report.md -H "X-API-Key: $CLAUDE_AGENT_API_KEY"
```

### 5. Failure modes (extension to `debugging_readme.md`)

| Symptom | Likely cause | Fix |
|---|---|---|
| `503 Topic API requires CLAUDE_AGENT_DATABASE_URL` | env var unset | set it, restart `claude_agent` |
| `psycopg2.errors.UndefinedTable: topics` | migration not run | `docker compose exec api alembic upgrade head` |
| Topic stuck in `planning` after restart | resume re-ran Stage 1 (cache hit) but couldn't enter the gate | check `docker compose logs claude_agent` for orchestrator errors |
| SSE returns nothing | reverse-proxy buffering | nginx: `proxy_buffering off; proxy_read_timeout 86400;` for `/v1/topics/{id}/events` |
| Webhook never fires | `disabled_at` set after 10 failures | `UPDATE topic_webhooks SET disabled_at=NULL, delivery_failures=0 WHERE id=$ID` |
| Stage 3 / 4 fail with "slash command missing" | `claude_agent_fe` bind-mount didn't pick up new `.claude/commands/*.md` | `git pull` on VPS, `docker compose restart claude_agent` |
| `/v1/topics/{id}/cancel` leaves Claude CLI running | Pre-PR runner.py never killed orphan subprocess; this PR adds `proc.kill()` in the finally block | redeploy claude_agent |

---

## Definition of Done — checklist

- [x] Postgres tables exist and reachable from the API container.
- [x] `POST /v1/topics` creates a topic, drives Stages 1→2 automatically, pauses at `planned_awaiting_review`, emits all events.
- [x] `POST /v1/topics/{id}/proceed` advances through Stages 3→4 to `reported`.
- [x] `GET /v1/topics/{id}` returns state and artifact pointers at every step.
- [x] `GET /v1/topics/{id}/events` streams SSE in real time AND replays from `from_seq`.
- [x] All four artifact endpoints return JSON; `intro.md` and `report.md` return `text/markdown`.
- [x] `POST /v1/topics/{id}/cancel` stops a running pipeline + transitions state + kills CLI subprocess.
- [x] `POST /v1/topics/{id}/subscribe` registers a webhook; events delivered with HMAC signature.
- [x] Restarting `claude_agent` resumes in-flight topics (`planning|searching|reporting`).
- [x] All artifact JSONs include `schema_version`; all events include `event_version`.
- [x] `scripts/test_topic.sh` drives the full flow from CLI.
- [x] No regression in `/v1/agent/run` and `/v1/agent/stream` — they still serve the standalone Stage 1 command.
- [ ] End-to-end demo on Hormuz topic against the VPS (run `scripts/test_topic.sh` after deploy).
