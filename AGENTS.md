# AGENTS.md

## Cursor Cloud specific instructions

### Product overview

Python 3.12 monorepo: **Signal Gather** (commodity intelligence API on port 8000) plus **RAG adhoc** (8001) and **claude_agent** (8002). Full stack runs via Docker Compose from repo root.

### First-time local files (not in git)

Before `docker compose up`, ensure:

```bash
cp .env.example.pro .env
sudo touch /etc/claude-worker.env
mkdir -p claude_home state
```

Create `apps/claude_agent/.env` (required by compose; see `scripts/devops/vps_setup_test_slot.sh`):

```bash
cat > apps/claude_agent/.env <<'EOF'
RAG_BASE_URL=http://rag_adhoc:8000/v1/search
RAG_TENANT_ID=00000000-0000-0000-0000-000000000001
RAG_API_KEY=
CLAUDE_AGENT_API_KEY=dev-local-key
CLAUDE_AGENT_DATABASE_URL=postgresql+asyncpg://agentic:agentic@postgres:5432/agentic
EOF
```

### Docker in Cloud Agent VMs

Docker CE is installed but **dockerd is not managed by systemd** in this environment. Start it once per VM session before compose:

```bash
sudo dockerd > /tmp/dockerd.log 2>&1 &
sleep 3
sudo docker info
```

Storage driver is `fuse-overlayfs` (see `/etc/docker/daemon.json`).

### Running the stack

```bash
sudo docker compose up --build -d
sudo docker compose ps
```

Minimal Newsfind overlay (postgres + rag_adhoc + claude_agent only): add `-f infra/docker-compose.slot-minimal.yml` and omit api/worker/scheduler/redis/minio.

Seed demo data:

```bash
sudo docker compose exec -T api python -m database.seeds.seed_scenario signal_gather_commodity_trading
```

Health checks: `curl http://localhost:8000/healthz`, `:8001/healthz`, `:8002/healthz`.

### Python / CI (no Docker)

Use the project venv via `uv` (see `pyproject.toml`):

```bash
export PATH="$HOME/.local/bin:$PATH"
uv sync --extra dev
uv run python -m pytest tests/qa -q
uv run python -m pytest tests/eval -q
bash scripts/devops/ci_verification_smoke.sh
```

`ruff check .` reports many pre-existing style findings; CI does not run ruff today.

### Auth for API demos

Signal Gather endpoints require JWT. Register + login, then call `/events` or `/search`:

```bash
curl -s -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"devpassword123","tenant_id":"00000000-0000-0000-0000-000000000001"}'
TOKEN=$(curl -s -X POST http://localhost:8000/auth/jwt/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'username=demo@example.com&password=devpassword123' | jq -r .access_token)
curl -s http://localhost:8000/events -H "Authorization: Bearer $TOKEN"
```

RAG adhoc uses `X-Tenant-Id` only (no JWT): `POST http://localhost:8001/v1/search`.

### External secrets (optional)

- `OPENAI_API_KEY` — embeddings / CrewAI (semantic search returns empty without it; filter APIs still work).
- Claude Code auth — `claude auth login` into `./claude_home` for full claude_agent topic pipelines.
