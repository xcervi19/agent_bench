#!/usr/bin/env bash
# Crawl, extract and publish one seed's data feeds into a slot (#55). Runs ON the VPS.
#
#   scripts/devops/slot_refresh_feeds.sh test2 japan_nuclear_official
#
# The same three steps as docs/ops/commands.md "Official data feeds", in one place,
# so a cron line can keep a daily feed daily. Until #55 every feed was published by
# hand, which is fine for PPAC's monthly tables and wrong for a register that changes
# the hour a reactor trips.
#
# Touches only artifacts/ and <state>/feeds of the named slot. Never rebuilds,
# restarts or migrates anything — publishing a feed is not a deploy.
set -euo pipefail

SLOT="${1:?Usage: $0 test1|test2 <seed>}"
SEED="${2:?Usage: $0 test1|test2 <seed>}"

case "$SLOT" in
  test1) DIR="$HOME/agent_bench_test1"; STATE_DIR=state_test1 ;;
  test2) DIR="$HOME/agent_bench_test2"; STATE_DIR=state_test2 ;;
  *) echo "Unknown slot: $SLOT (use test1 or test2)" >&2; exit 1 ;;
esac

cd "$DIR"
export COMPOSE_PROJECT_NAME="$SLOT"
C=(docker compose -f docker-compose.yml -f "infra/docker-compose.$SLOT.yml" -f infra/docker-compose.slot-minimal.yml)

# The container runs as uid 1001; a root-owned dir here fails the crawl with
# PermissionError before anything is spent (#53 lost a run to exactly that).
mkdir -p artifacts "$STATE_DIR/feeds"
chown -R 1001:1001 artifacts "$STATE_DIR/feeds"

"${C[@]}" run --rm --no-deps -v "$PWD/source_crawler:/app/source_crawler:ro" -v "$PWD/artifacts:/app/artifacts" \
  --entrypoint python claude_agent -m source_crawler crawl --seed "$SEED"
"${C[@]}" run --rm --no-deps -v "$PWD/source_crawler:/app/source_crawler:ro" -v "$PWD/artifacts:/app/artifacts" \
  --entrypoint python claude_agent -m source_crawler extract
"${C[@]}" run --rm --no-deps -v "$PWD/artifacts:/app/artifacts" --entrypoint python claude_agent -c \
  "from pathlib import Path; from apps.claude_agent.topics.feeds import publish; \
   print(publish(Path('/app/artifacts/collected_text'), '/state'))"
