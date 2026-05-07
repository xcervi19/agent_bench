# AGENTS.md

## Cursor Cloud specific instructions

### Architecture Overview

This is a Python 3.12 monorepo with:
- `libs/agentic_core/` — reusable multi-agent orchestration framework
- `apps/signal_gather/` — commodity market intelligence application (FastAPI)
- `apps/rag_adhoc/` — standalone semantic search API

### Development Environment

**Package manager:** `uv` (lockfile: `uv.lock`)

**Infrastructure (Docker Compose):** PostgreSQL+pgvector (port 5432), Redis (port 6379), MinIO (port 9000/9001)

Start infrastructure only:
```bash
sudo dockerd &>/tmp/dockerd.log &  # if Docker daemon not running
sudo docker compose up -d postgres redis minio
```

**Run migrations:**
```bash
PYTHONPATH="libs:." uv run alembic upgrade head
```

**Run API locally (dev mode with hot reload):**
```bash
PYTHONPATH="libs:." uv run uvicorn apps.signal_gather.entrypoints.api:app --host 0.0.0.0 --port 8000 --reload
```

**Run worker:**
```bash
PYTHONPATH="libs:." uv run python -m apps.signal_gather.entrypoints.worker
```

**Run scheduler:**
```bash
PYTHONPATH="libs:." uv run python -m apps.signal_gather.entrypoints.scheduler
```

### Lint & Test

```bash
uv run ruff check .         # lint (93 pre-existing issues in codebase)
uv run ruff format --check . # format check
uv run pytest               # no tests exist yet (tests/ dir doesn't exist)
```

### Key Gotchas

1. **PYTHONPATH is required** when running outside Docker: `PYTHONPATH="libs:."` so both `agentic_core` and `apps` resolve.
2. **Docker daemon must be started manually** in Cloud VMs: `sudo dockerd &>/tmp/dockerd.log &` then wait ~3s before using docker commands.
3. **Registration requires `tenant_id`** field (UUID) in the request body alongside email/password.
4. **`.env` file** must exist at repo root with `DATABASE_URL`, `REDIS_URL`, `S3_*` vars. The settings class loads from `.env` automatically. No `.env.example` is committed; see `libs/agentic_core/config.py` for all required fields.
5. **OpenAI API key** is optional for basic API testing. Without it, CrewAI agents and semantic search won't function, but all HTTP endpoints still respond.
6. **fuse-overlayfs + iptables-legacy** are required for Docker-in-Docker in Cloud Agent VMs.
