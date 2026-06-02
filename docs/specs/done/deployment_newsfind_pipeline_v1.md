# === LOCAL ===
git add -A
git commit -m "newsfind-pipeline-v1: topic orchestrator + event stream"
git push origin main

# === VPS ===
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212
cd ~/agent_bench
git pull origin main

# 1. ENV — add the new vars to apps/claude_agent/.env on the VPS
#    (or rely on docker-compose's auto-wired CLAUDE_AGENT_DATABASE_URL).
$EDITOR apps/claude_agent/.env
# Make sure these lines are present:
#   CLAUDE_AGENT_DATABASE_URL=postgresql+asyncpg://agentic:agentic@postgres:5432/agentic
#   CLAUDE_AGENT_MAX_CONCURRENT_TOPICS=8
#   CLAUDE_AGENT_WEBHOOK_MAX_RETRIES=3
#   CLAUDE_AGENT_SEARCH_MAX_QUERIES=15
#   CLAUDE_AGENT_ALLOWED_COMMANDS=[...,"/newsfind-search","/newsfind-report"]

# Top-level .env must have Postgres creds for compose interpolation:
$EDITOR .env
#   POSTGRES_DB=agentic
#   POSTGRES_USER=agentic
#   POSTGRES_PASSWORD=<real password>

# 2. Build images
docker compose build api claude_agent

# 3. DB → start postgres, then api (which runs `alembic upgrade head`
#    → applies 0003_newsfind_topics → creates the four topic tables).
docker compose up -d postgres
docker compose up -d api
docker compose exec api alembic current        # should show 0003_newsfind_topics

# 4. claude_agent picks up new tables, slash commands, and routes
docker compose up -d claude_agent
docker compose logs -f --tail=200 claude_agent
#   → look for: claude_agent.start ... topics_enabled=True

# 5. Smoke test
curl -fsS http://127.0.0.1:8002/readyz
docker compose exec postgres psql -U agentic -d agentic -c '\dt topic*'
#   → topics, topic_events, topic_inputs, topic_webhooks

then test:
export API=http://79.143.179.212:8002
export CLAUDE_AGENT_API_KEY=<value from VPS apps/claude_agent/.env>
scripts/test_vector_runner.sh --env prod
# → testing/results/prod/<UTC>/... (evaluation.json, qa_report.json, agent_log/, business_output/)