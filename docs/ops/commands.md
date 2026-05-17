# Operational Commands

## SSH & SCP (VPS)

```bash
# Connect to VPS
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212

# SSH tunnel for Postgres (leave open while running ingest from laptop)
ssh -i ~/.ssh/contabo_ed25519 -N -L 5433:127.0.0.1:5432 root@79.143.179.212

# Copy env files to VPS
scp -i ~/.ssh/contabo_ed25519 .env.examplesmall root@79.143.179.212:~/agent_bench/.env
scp -i ~/.ssh/contabo_ed25519 ./apps/claude_agent/.env root@79.143.179.212:~/agent_bench/apps/claude_agent/.env
```

---

## Deploy / Update VPS App

```bash
# Connect
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212
cd ~/agent_bench

# Pull latest code
git pull origin main

# Rebuild and restart a single service (e.g. claude_agent)
docker compose build claude_agent
docker compose up -d claude_agent
docker compose logs -f claude_agent

# Rebuild multiple services
docker compose build api claude_agent
docker compose up -d api claude_agent
```

---

## Database Migrations

```bash
# Apply migrations (local)
docker compose run --rm --no-deps --entrypoint alembic api upgrade head

# Check current migration
docker compose exec api alembic current

# Verify topic tables exist
docker compose exec postgres psql -U agentic -d agentic -c '\dt topic*'
```

---

## Health Checks & Smoke Tests

```bash
# claude_agent
curl -s http://79.143.179.212:8002/readyz
# expect: {"status":"ready","claude_version":"..."}

curl -s http://79.143.179.212:8002/v1/agent/info \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" | jq '.allowed_commands'

# signal_gather / rag_adhoc
curl -sS -X POST "http://79.143.179.212:8001/v1/search" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: 00000000-0000-0000-0000-000000000001" \
  -H "X-API-Key: kjdjuhf6s8i783hd8j47" \
  -d '{"query":"test","limit":5}'
```

---

## End-to-End API Test (from Mac)

```bash
cd ~/Documents/projects/agent_bench
source apps/claude_agent/.env
export API="http://79.143.179.212:8002"

# Streaming run
curl -N -X POST "$API/v1/agent/stream" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -d '{"command":"/newsfind-queries","args":"Hormuz strait closure options to lower price","timeout_sec":900}' \
  | tee ./newsfind.raw.txt

# Extract final JSON
cat ./newsfind.raw.txt | grep '"type":"result"' | head -1 \
  | jq -r '.result' \
  | jq '{schema_version, domain, queries_count: (.queries | length)}'

# Topic pipeline test (scripts/test_topic.sh)
export CLAUDE_AGENT_API_KEY="<from apps/claude_agent/.env>"
scripts/test_topic.sh "Hormuz strait closure options to lower price"
```

---

## Local Knowledge Ingest

```bash
# Step 1 — preprocess (no API calls)
uv run python -m source_ingest.preprocess \
  --input local_knowledge_sources/oil101.txt \
  --output-dir artifacts/oil101_run1 \
  --book-title "Oil 101" \
  --author "Morgan Downey" \
  --book-slug oil101 \
  --category energy_education \
  --commodity crude_oil

# Step 2 — inspect
head -n 2 artifacts/oil101_run1/chunks.jsonl | python -m json.tool

# Step 3 — open SSH tunnel to Postgres (separate terminal)
ssh -i ~/.ssh/contabo_ed25519 -N -L 5433:127.0.0.1:5432 root@79.143.179.212

# Step 4 — ingest (embed + DB write)
export DATABASE_URL='postgresql+asyncpg://agentic:YOUR_PASSWORD@127.0.0.1:5433/agentic'
export OPENAI_API_KEY='sk-...'
export PYTHONPATH="libs:."
uv run python -m source_ingest.ingest \
  --artifact-dir artifacts/oil101_run1 \
  --tenant-id '00000000-0000-0000-0000-000000000001'
```

---

## Seed & Demo Data

```bash
# Seed signal_gather demo scenario
docker compose exec api python -m database.seeds.seed_scenario signal_gather_commodity_trading

# Replay an agent session (debugging)
docker compose exec api python scripts/replay_session.py \
  --session-id <uuid> \
  --tenant-id 00000000-0000-0000-0000-000000000001
```


# SSH to VPS
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212
cd ~/agent_bench

# Pull latest code (includes migration 0004)
git pull origin main

# Apply migrations inside the running api container
docker compose exec api alembic upgrade head

# Verify current state
docker compose exec api alembic current

# Verify all topic* tables exist
docker compose exec postgres psql -U agentic -d agentic -c '\dt topic*'

# Rebuild claude_agent (includes new /newsfind-refresh command)
docker compose build claude_agent
docker compose up -d claude_agent

# Verify claude_agent is healthy
docker compose logs -f claude_agent
# (wait for "claude_agent.start" log entry, then Ctrl+C)

# Smoke test — check allowed_commands includes /newsfind-refresh
curl -s http://127.0.0.1:8002/v1/agent/info \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" | jq '.allowed_commands | contains(["/newsfind-refresh"])'
# expect: true