#!/usr/bin/env bash
# Create or refresh a test slot on the VPS (worktree + .env + compose up).
# Usage (from laptop):
#   scripts/vps_setup_test_slot.sh test1 [git-branch]
#   scripts/vps_setup_test_slot.sh test2 feature/my-branch
#
# Slots: test1 → ~/agent_bench_test1, test2 → ~/agent_bench_test2
set -euo pipefail

SLOT="${1:?Usage: $0 test1|test2 [branch]}"
BRANCH="${2:-main}"
SSH_KEY="${SSH_KEY:-$HOME/.ssh/contabo_ed25519}"
VPS_HOST="${VPS_HOST:-root@79.143.179.212}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

case "$SLOT" in
  test1)
    DIR=agent_bench_test1
    COMPOSE_FILE=infra/docker-compose.test1.yml
    POSTGRES_DB=agentic_test1
    REDIS_DB=1
    S3_BUCKET=documents_test1
    ;;
  test2)
    DIR=agent_bench_test2
    COMPOSE_FILE=infra/docker-compose.test2.yml
    POSTGRES_DB=agentic_test2
    REDIS_DB=2
    S3_BUCKET=documents_test2
    ;;
  *)
    echo "Unknown slot: $SLOT (use test1 or test2)" >&2
    exit 1
    ;;
esac

# Sync infra + scripts needed on VPS
scp -i "$SSH_KEY" \
  "$REPO_ROOT/infra/docker-compose.test1.yml" \
  "$REPO_ROOT/infra/docker-compose.test2.yml" \
  "$REPO_ROOT/infra/docker-compose.vps-bind-local.yml" \
  "$VPS_HOST:~/agent_bench/infra/"

ssh -i "$SSH_KEY" "$VPS_HOST" bash -s -- "$SLOT" "$BRANCH" "$DIR" "$COMPOSE_FILE" "$POSTGRES_DB" "$REDIS_DB" "$S3_BUCKET" <<'REMOTE'
set -euo pipefail
SLOT="$1"
BRANCH="$2"
DIR="$3"
COMPOSE_FILE="$4"
POSTGRES_DB="$5"
REDIS_DB="$6"
S3_BUCKET="$7"

cd ~/agent_bench
if [[ ! -d "../${DIR}" ]]; then
  git fetch origin
  git worktree add "../${DIR}" "origin/${BRANCH}" 2>/dev/null || git worktree add "../${DIR}" "${BRANCH}"
fi

cd ~/"${DIR}"
git fetch origin
git checkout "${BRANCH}" 2>/dev/null || git checkout -B "${BRANCH}" "origin/${BRANCH}" 2>/dev/null || true
mkdir -p infra claude_home_"${SLOT}" state_"${SLOT}"
cp -f ~/agent_bench/infra/docker-compose.test1.yml infra/ 2>/dev/null || true
cp -f ~/agent_bench/infra/docker-compose.test2.yml infra/ 2>/dev/null || true

if [[ ! -f .env ]]; then
  cp ~/agent_bench/.env .env
fi
# Always align slot-specific vars (safe to re-run)
PG_USER="$(grep '^POSTGRES_USER=' .env | cut -d= -f2- | tr -d '\r')"
PG_PASS="$(grep '^POSTGRES_PASSWORD=' .env | cut -d= -f2- | tr -d '\r')"
sed -i "s/^POSTGRES_DB=.*/POSTGRES_DB=${POSTGRES_DB}/" .env
sed -i "s|^DATABASE_URL=.*|DATABASE_URL=postgresql+asyncpg://${PG_USER}:${PG_PASS}@postgres:5432/${POSTGRES_DB}|" .env
sed -i "s|^REDIS_URL=.*|REDIS_URL=redis://redis:6379/${REDIS_DB}|" .env
sed -i "s/^S3_BUCKET=.*/S3_BUCKET=${S3_BUCKET}/" .env
sed -i "s/^APP_ENV=.*/APP_ENV=${SLOT}/" .env
if grep -q '^CLAUDE_AGENT_DATABASE_URL=' .env; then
  sed -i "s|^CLAUDE_AGENT_DATABASE_URL=.*|CLAUDE_AGENT_DATABASE_URL=postgresql+asyncpg://${PG_USER}:${PG_PASS}@postgres:5432/${POSTGRES_DB}|" .env
fi

if [[ -f ~/agent_bench/apps/claude_agent/.env ]] && [[ ! -f apps/claude_agent/.env ]]; then
  mkdir -p apps/claude_agent
  cp ~/agent_bench/apps/claude_agent/.env apps/claude_agent/.env
fi

export COMPOSE_PROJECT_NAME="${SLOT}"
docker compose -f docker-compose.yml -f "${COMPOSE_FILE}" up -d \
  postgres redis minio api rag_adhoc claude_agent

sleep 6
docker compose ps
echo "--- ${SLOT} ready on branch $(git branch --show-current) DB=${POSTGRES_DB} ---"
REMOTE

echo "Slot ${SLOT} deployed. Enable Caddy vhosts and run: scripts/vps_deploy_caddy.sh"
