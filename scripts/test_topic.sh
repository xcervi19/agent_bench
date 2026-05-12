#!/usr/bin/env bash
# scripts/test_topic.sh
#
# Drive a full /v1/topics/* pipeline end-to-end:
#   1. POST /v1/topics  → creates topic, runs Stage 1+2, pauses at the gate.
#   2. Tail SSE until needs_input event arrives.
#   3. POST /v1/topics/{id}/proceed → unblocks Stages 3+4.
#   4. Tail SSE until report.ready (or error).
#   5. Pull every artifact (parsed/intro/intro.md/news/report/report.md) to disk.
#
# Usage:
#   scripts/test_topic.sh "<topic>"
#   scripts/test_topic.sh                       # uses default Hormuz topic
#
# Required env vars:
#   API                    e.g. http://79.143.179.212:8002
#   CLAUDE_AGENT_API_KEY   API key for X-API-Key header
#
# Optional:
#   INTRO_STYLE=trader      raw|trader|executive|analyst (default: raw)
#   FORCE_REFRESH=true      bypass Stage-1 cache
#   TIMEOUT_SEC=900         per-stage CLI timeout
#   AUTO_PROCEED=false      set true to auto-press Proceed without confirming

set -euo pipefail

DEFAULT_TOPIC="Hormuz strait closure options to lower price"
TOPIC="${1:-$DEFAULT_TOPIC}"

INTRO_STYLE="${INTRO_STYLE:-raw}"
FORCE_REFRESH="${FORCE_REFRESH:-false}"
TIMEOUT_SEC="${TIMEOUT_SEC:-900}"
AUTO_PROCEED="${AUTO_PROCEED:-true}"

for cmd in curl jq sed tee date tr; do
  command -v "$cmd" >/dev/null || { echo "missing dependency: $cmd" >&2; exit 1; }
done
: "${API:?env var API is not set, e.g. export API=http://79.143.179.212:8002}"
: "${CLAUDE_AGENT_API_KEY:?env var CLAUDE_AGENT_API_KEY is not set}"

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TS="$(date -u +%Y-%m-%dT%H-%MZ)"
SLUG="$(echo "$TOPIC" | tr 'A-Z' 'a-z' | tr -cs 'a-z0-9' '-' | sed 's/^-//;s/-$//' | cut -c1-50)"
RUN_DIR="$REPO_ROOT/testing/runs/${TS}__topic__${SLUG}"
mkdir -p "$RUN_DIR"

echo "API:           $API"
echo "TOPIC:         $TOPIC"
echo "INTRO_STYLE:   $INTRO_STYLE"
echo "FORCE_REFRESH: $FORCE_REFRESH"
echo "TIMEOUT_SEC:   $TIMEOUT_SEC"
echo "AUTO_PROCEED:  $AUTO_PROCEED"
echo "RUN_DIR:       $RUN_DIR"
echo "---"

if ! curl -fsS "$API/readyz" >/dev/null; then
  echo "readyz failed — API not reachable at $API" >&2
  exit 1
fi

#-------------------------------------------------------------------------------
# 1. Create topic
#-------------------------------------------------------------------------------
BODY=$(jq -nc \
  --arg topic "$TOPIC" \
  --arg intro_style "$INTRO_STYLE" \
  --argjson force "$FORCE_REFRESH" \
  --argjson timeout "$TIMEOUT_SEC" \
  '{topic:$topic, intro_style:$intro_style, force_refresh:$force, timeout_sec:$timeout}')

echo "$BODY" | jq . > "$RUN_DIR/create_request.json"

CREATE_RESP=$(curl -fsS -X POST "$API/v1/topics" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -d "$BODY")
echo "$CREATE_RESP" | jq . > "$RUN_DIR/create_response.json"

TOPIC_ID=$(echo "$CREATE_RESP" | jq -r '.topic_id')
[ -n "$TOPIC_ID" ] || { echo "no topic_id in create response" >&2; exit 1; }
echo "Created topic_id=$TOPIC_ID"

#-------------------------------------------------------------------------------
# 2. Tail SSE in background, look for needs_input → proceed → report.ready
#-------------------------------------------------------------------------------
EVENTS="$RUN_DIR/events.ndjson"
echo "Tailing SSE → $EVENTS"

curl -N -sS "$API/v1/topics/$TOPIC_ID/events" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  | sed -n 's/^data: //p' \
  | tee "$EVENTS" \
  | jq -rc --unbuffered '
      "[seq=\(.seq) \(.event_type)] " +
        (.payload
          | if .stage then "stage=\(.stage)" else "" end
          + (if .from then " state \(.from)→\(.to)" else "" end)
          + (if .summary_short then " | \(.summary_short[0:80])" else "" end)
          + (if .gate then " | gate=\(.gate)" else "" end)
          + (if .error then " | ERR=\(.error[0:140])" else "" end)
        )
    ' &
TAIL_PID=$!
trap 'kill "$TAIL_PID" 2>/dev/null || true' EXIT

#-------------------------------------------------------------------------------
# 3. Wait for needs_input (gate), then POST /proceed
#-------------------------------------------------------------------------------
echo "Waiting for needs_input event…"
WAITED=0
while true; do
  if grep -q '"event_type":"needs_input"' "$EVENTS" 2>/dev/null; then
    break
  fi
  if grep -q '"event_type":"error"' "$EVENTS" 2>/dev/null; then
    echo "===== ERROR while waiting for gate ====="
    grep '"event_type":"error"' "$EVENTS" | tail -1 | jq .
    exit 1
  fi
  sleep 2
  WAITED=$((WAITED + 2))
  if [ "$WAITED" -gt "$TIMEOUT_SEC" ]; then
    echo "Timeout waiting for gate after ${WAITED}s" >&2
    exit 1
  fi
done

echo
echo "===== GATE REACHED — Stage 1+2 done. ====="
curl -fsS "$API/v1/topics/$TOPIC_ID/intro.md" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" | tee "$RUN_DIR/intro.md" || true
echo

if [ "$AUTO_PROCEED" != "true" ]; then
  read -r -p "Press Enter to proceed (or Ctrl-C to bail)…" _
fi

curl -fsS -X POST "$API/v1/topics/$TOPIC_ID/proceed" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -d '{"from_state":"planned_awaiting_review"}' \
  | jq . > "$RUN_DIR/proceed_response.json"

#-------------------------------------------------------------------------------
# 4. Wait for report.ready (or error / cancelled)
#-------------------------------------------------------------------------------
echo "Waiting for report.ready event…"
WAITED=0
while true; do
  if grep -q '"event_type":"report.ready"' "$EVENTS" 2>/dev/null; then
    break
  fi
  if grep -qE '"event_type":"(error|cancelled)"' "$EVENTS" 2>/dev/null; then
    echo "===== terminal event before report ====="
    grep -E '"event_type":"(error|cancelled)"' "$EVENTS" | tail -1 | jq .
    exit 1
  fi
  sleep 3
  WAITED=$((WAITED + 3))
  if [ "$WAITED" -gt "$((TIMEOUT_SEC * 2))" ]; then
    echo "Timeout waiting for report after ${WAITED}s" >&2
    exit 1
  fi
done

#-------------------------------------------------------------------------------
# 5. Pull every artifact
#-------------------------------------------------------------------------------
echo
echo "===== REPORT READY — pulling artifacts ====="
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
jq '{id, state, stages_done, available_actions, error}' "$RUN_DIR/topic.json"
echo
echo "Artifacts under: $RUN_DIR"
ls -la "$RUN_DIR"
