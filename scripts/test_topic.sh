#!/usr/bin/env bash
# scripts/test_topic.sh — drive the topic pipeline end-to-end via the HTTP API.
#
# Required: API, CLAUDE_AGENT_API_KEY
# Optional: AUTO_PROCEED=true|false (default true), TIMEOUT_SEC=900

set -euo pipefail

DEFAULT_TOPIC="Hormuz strait closure options to lower price"
TOPIC="${1:-$DEFAULT_TOPIC}"
AUTO_PROCEED="${AUTO_PROCEED:-true}"
TIMEOUT_SEC="${TIMEOUT_SEC:-900}"

: "${API:?set API, e.g. export API=http://79.143.179.212:8002}"
: "${CLAUDE_AGENT_API_KEY:?set CLAUDE_AGENT_API_KEY}"
for cmd in curl jq sed tee date tr; do command -v "$cmd" >/dev/null; done

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TS="$(date -u +%Y-%m-%dT%H-%MZ)"
SLUG="$(echo "$TOPIC" | tr 'A-Z' 'a-z' | tr -cs 'a-z0-9' '-' | sed 's/^-//;s/-$//' | cut -c1-50)"
RUN_DIR="$REPO_ROOT/testing/runs/${TS}__topic__${SLUG}"
mkdir -p "$RUN_DIR"

echo "API:     $API"
echo "TOPIC:   $TOPIC"
echo "RUN_DIR: $RUN_DIR"

curl -fsS "$API/readyz" >/dev/null

TOPIC_ID=$(curl -fsS -X POST "$API/v1/topics" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -d "$(jq -nc --arg t "$TOPIC" '{topic:$t}')" \
  | tee "$RUN_DIR/create.json" \
  | jq -r .topic_id)
echo "topic_id=$TOPIC_ID"

EVENTS="$RUN_DIR/events.ndjson"
echo "Tailing SSE → $EVENTS"

curl -N -sS "$API/v1/topics/$TOPIC_ID/events" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  | sed -n 's/^data: //p' \
  | tee "$EVENTS" \
  | jq -rc --unbuffered '
      "[seq=\(.seq) \(.event_type)] " +
        (.payload
          | (if .stage then "stage=\(.stage) " else "" end)
          + (if .tool  then "tool=\(.tool) "   else "" end)
          + (if .from  then "\(.from)→\(.to) " else "" end)
          + (if .headline then "| \(.headline[0:80])" else "" end)
          + (if .summary_md then "| report ready" else "" end)
          + (if .error then "| ERR=\(.error[0:120])" else "" end)
        )
    ' &
TAIL_PID=$!
trap 'kill "$TAIL_PID" 2>/dev/null || true' EXIT

wait_for_event() {
  local name="$1"; local waited=0
  while ! grep -q "\"event_type\":\"$name\"" "$EVENTS" 2>/dev/null; do
    if grep -qE '"event_type":"(error|cancelled)"' "$EVENTS" 2>/dev/null; then
      echo "===== terminal event before $name ====="
      grep -E '"event_type":"(error|cancelled)"' "$EVENTS" | tail -1 | jq .
      exit 1
    fi
    sleep 2; waited=$((waited+2))
    if [ "$waited" -gt "$TIMEOUT_SEC" ]; then
      echo "timeout waiting for $name after ${waited}s" >&2; exit 1
    fi
  done
}

echo "Waiting for needs_input…"
wait_for_event "needs_input"

echo "===== GATE — fetching intro.md ====="
curl -fsS "$API/v1/topics/$TOPIC_ID/intro.md" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" | tee "$RUN_DIR/intro.md"
echo

if [ "$AUTO_PROCEED" != "true" ]; then
  read -r -p "Press Enter to proceed…" _
fi

curl -fsS -X POST "$API/v1/topics/$TOPIC_ID/proceed" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" >/dev/null

echo "Waiting for report.ready…"
wait_for_event "report.ready"

for art in parsed intro news report; do
  curl -fsS "$API/v1/topics/$TOPIC_ID/$art" \
    -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
    | jq . > "$RUN_DIR/${art}.json" || echo "($art not available)"
done
for art in intro report; do
  curl -fsS "$API/v1/topics/$TOPIC_ID/${art}.md" \
    -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
    > "$RUN_DIR/${art}.md" || echo "(${art}.md not available)"
done

curl -fsS "$API/v1/topics/$TOPIC_ID" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  | jq . > "$RUN_DIR/topic.json"

echo
echo "===== DONE ====="
jq '{id, state, plan_run_id, deliver_run_id, error}' "$RUN_DIR/topic.json"
ls -la "$RUN_DIR"
