#!/usr/bin/env bash
# Create or refresh a test slot on the VPS (worktree + .env + minimal compose up).
# Usage (from laptop):
#   scripts/devops/vps_setup_test_slot.sh test1 [git-branch]
#   scripts/devops/vps_setup_test_slot.sh test2 feature/my-branch
set -euo pipefail

SLOT="${1:?Usage: $0 test1|test2 [branch]}"
BRANCH="${2:-main}"
SSH_KEY="${SSH_KEY:-$HOME/.ssh/contabo_ed25519}"
VPS_HOST="${VPS_HOST:-root@79.143.179.212}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

case "$SLOT" in
  test1)
    DIR=agent_bench_test1
    COMPOSE_SLOT=infra/docker-compose.test1.yml
    STATE_DIR=state_test1
    POSTGRES_DB=agentic_test1
    ;;
  test2)
    DIR=agent_bench_test2
    COMPOSE_SLOT=infra/docker-compose.test2.yml
    STATE_DIR=state_test2
    POSTGRES_DB=agentic_test2
    ;;
  *)
    echo "Unknown slot: $SLOT (use test1 or test2)" >&2
    exit 1
    ;;
esac

scp -i "$SSH_KEY" \
  "$REPO_ROOT/infra/docker-compose.test1.yml" \
  "$REPO_ROOT/infra/docker-compose.test2.yml" \
  "$REPO_ROOT/infra/docker-compose.slot-minimal.yml" \
  "$VPS_HOST:~/agent_bench/infra/"

ssh -i "$SSH_KEY" "$VPS_HOST" bash -s -- "$SLOT" "$BRANCH" "$DIR" "$COMPOSE_SLOT" "$STATE_DIR" "$POSTGRES_DB" <<'REMOTE'
set -euo pipefail
SLOT="$1"
BRANCH="$2"
DIR="$3"
COMPOSE_SLOT="$4"
STATE_DIR="$5"
POSTGRES_DB="$6"

cd ~/agent_bench
if [[ ! -d "../${DIR}" ]]; then
  git fetch origin
  git worktree add "../${DIR}" "origin/${BRANCH}" 2>/dev/null || git worktree add "../${DIR}" "${BRANCH}"
fi

cd ~/"${DIR}"
git fetch origin
git checkout "${BRANCH}" 2>/dev/null || git checkout -B "${BRANCH}" "origin/${BRANCH}" 2>/dev/null || true
mkdir -p infra "${STATE_DIR}"
cp -f ~/agent_bench/infra/docker-compose.test1.yml infra/
cp -f ~/agent_bench/infra/docker-compose.test2.yml infra/
cp -f ~/agent_bench/infra/docker-compose.slot-minimal.yml infra/

if [[ ! -f .env ]]; then
  cp ~/agent_bench/.env .env
fi
PG_USER="$(grep '^POSTGRES_USER=' .env | cut -d= -f2- | tr -d '\r')"
PG_PASS="$(grep '^POSTGRES_PASSWORD=' .env | cut -d= -f2- | tr -d '\r')"
sed -i "s/^POSTGRES_DB=.*/POSTGRES_DB=${POSTGRES_DB}/" .env
sed -i "s|^DATABASE_URL=.*|DATABASE_URL=postgresql+asyncpg://${PG_USER}:${PG_PASS}@postgres:5432/${POSTGRES_DB}|" .env
sed -i "s/^APP_ENV=.*/APP_ENV=${SLOT}/" .env
if grep -q '^CLAUDE_AGENT_DATABASE_URL=' .env; then
  sed -i "s|^CLAUDE_AGENT_DATABASE_URL=.*|CLAUDE_AGENT_DATABASE_URL=postgresql+asyncpg://${PG_USER}:${PG_PASS}@postgres:5432/${POSTGRES_DB}|" .env
fi

mkdir -p apps/claude_agent
if [[ -f ~/agent_bench/apps/claude_agent/.env ]]; then
  cp ~/agent_bench/apps/claude_agent/.env apps/claude_agent/.env
fi
# RAG via Docker network (not public HTTPS)
grep -q '^RAG_BASE_URL=' apps/claude_agent/.env 2>/dev/null || \
  echo 'RAG_BASE_URL=http://rag_adhoc:8000/v1/search' >> apps/claude_agent/.env
sed -i 's|^RAG_BASE_URL=.*|RAG_BASE_URL=http://rag_adhoc:8000/v1/search|' apps/claude_agent/.env

export COMPOSE_PROJECT_NAME="${SLOT}"
docker compose \
  -f docker-compose.yml \
  -f "${COMPOSE_SLOT}" \
  -f infra/docker-compose.slot-minimal.yml \
  up -d postgres rag_adhoc claude_agent

sleep 6
docker compose ps
echo "--- ${SLOT} ready branch=$(git branch --show-current) DB=${POSTGRES_DB} shared_claude_home=~/agent_bench/claude_home ---"
REMOTE

echo "Slot ${SLOT} deployed. Run: scripts/devops/vps_deploy_caddy.sh (if Caddyfile changed)"
