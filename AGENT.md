# agent_bench

Monorepo for the Agentic Platform: a reusable multi-agent framework with two applications built on top.

## Applications

| App | Location | Purpose |
|---|---|---|
| `signal_gather` | `apps/signal_gather/` | Commodity market intelligence (CrewAI crews: discovery → events → signals → briefings) |
| `claude_agent` | `apps/claude_agent/` | Claude-powered topic research pipeline (`/newsfind-*` slash commands) |

The shared framework lives in `libs/agentic_core/`.  
Claude slash commands workspace: `claude_agent_fe/` (mounted into the `claude_agent` container).

## Services & Ports

| Service | Local | VPS |
|---|---|---|
| `api` (signal_gather) | 8000 | 8001 |
| `claude_agent` | 8002 | 8002 |
| `rag_adhoc` | 8003 | 8003 |
| `postgres` | 5432 | — (tunnel to 5433) |
| `redis` | 6379 | — |

## Repo Layout

```
agent_bench/
├── apps/
│   ├── signal_gather/          ← commodity intel API (CrewAI)
│   └── claude_agent/           ← news research pipeline (Claude CLI)
├── libs/
│   └── agentic_core/           ← shared framework (pip-installable)
├── claude_agent_fe/
│   └── .claude/commands/       ← slash commands: /newsfind-*, /trade-*, /rag-*
├── testing/                    ← test scripts + captured runs
├── source_ingest/              ← preprocess + embed local knowledge
├── database/
│   ├── migrations/             ← Alembic
│   └── seeds/
├── docs/
│   ├── architecture/           ← stable system design docs
│   ├── ops/                    ← commands, debugging, DB queries
│   └── specs/
│       ├── active/             ← features in progress
│       └── done/               ← completed + archived specs
├── docker-compose.yml
├── .env                        ← top-level (postgres creds, shared)
└── apps/claude_agent/.env      ← claude_agent service config
```

## Quick Commands

```bash
# Start everything locally
docker compose up --build

# Seed demo data (signal_gather)
docker compose exec api python -m database.seeds.seed_scenario signal_gather_commodity_trading

# Run migrations
docker compose run --rm --no-deps --entrypoint alembic api upgrade head

# Rebuild + restart claude_agent only
docker compose build claude_agent && docker compose up -d claude_agent

# Health checks
curl -s http://localhost:8002/readyz
curl -s http://localhost:8002/v1/agent/info -H "X-API-Key: $CLAUDE_AGENT_API_KEY" | jq

# Run a topic (streaming)
export API="http://localhost:8002"
curl -N -X POST "$API/v1/agent/stream" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -d '{"command":"/newsfind-queries","args":"Hormuz strait closure options to lower price","timeout_sec":900}'
```

## Key Documentation

| What | Where |
|---|---|
| Current work, bugs, blockers | `STATUS.md` |
| Platform architecture | `docs/architecture/framework.md` |
| Signal Gather product brief | `docs/architecture/signal_gather.md` |
| VPS deploy + SSH commands | `docs/ops/commands.md` |
| Debug cheat sheet + war stories | `docs/ops/debugging.md` |
| DB debug queries | `docs/ops/db_commands.md` |
| News pipeline v2 spec (in progress) | `docs/specs/active/news_pipeline_v2.md` |
| Testing scenarios | `testing/README.md` |

## Tech Stack

- **Language:** Python 3.12
- **API:** FastAPI + Pydantic v2 + SQLAlchemy 2.0
- **DB:** PostgreSQL + pgvector + Alembic
- **Queue:** Redis
- **Agent orchestration:** CrewAI (`signal_gather`), Claude CLI (`claude_agent`)
- **Containers:** Docker Compose (local) → single-node VPS (production)
- **Embeddings:** OpenAI `text-embedding-3-small`
