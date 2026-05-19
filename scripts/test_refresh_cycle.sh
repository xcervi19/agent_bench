#!/usr/bin/env bash
# scripts/test_refresh_cycle.sh — Run refresh on a reported topic to get latest news
#
# Sources testing/.env.testing for API/VPS config.
# Optionally starts monitoring if not yet active.
# Prints delta summary: new sources, cost, timing.
#
# Usage:
#   scripts/test_refresh_cycle.sh <TOPIC_ID>                    # single refresh
#   scripts/test_refresh_cycle.sh <TOPIC_ID> --monitor          # start monitoring first
#   scripts/test_refresh_cycle.sh <TOPIC_ID> --max-age 24       # override max_age_hours
#   scripts/test_refresh_cycle.sh <TOPIC_ID> --repeat 3         # run N refresh cycles

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# ── Load config ─────────────────────────────────────────────
ENV_FILE="$REPO_ROOT/testing/.env.testing"
if [ -f "$ENV_FILE" ]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
else
  echo "Missing $ENV_FILE — create it first." >&2
  exit 1
fi

# ── Parse args ──────────────────────────────────────────────
TOPIC_ID="${1:?Usage: $0 <TOPIC_ID> [--monitor] [--max-age N] [--repeat N]}"
shift

START_MONITOR=false
MAX_AGE_HOURS="${REFRESH_MAX_AGE_HOURS:-48}"
REPEAT=1
TIMEOUT_SEC="${TIMEOUT_SEC:-300}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --monitor)   START_MONITOR=true; shift ;;
    --max-age)   MAX_AGE_HOURS="$2"; shift 2 ;;
    --repeat)    REPEAT="$2"; shift 2 ;;
    --timeout)   TIMEOUT_SEC="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done

# ── Validate deps ───────────────────────────────────────────
for cmd in curl jq sed date; do
  command -v "$cmd" >/dev/null || { echo "missing: $cmd" >&2; exit 1; }
done

# ── Run directory ───────────────────────────────────────────
TS="$(date -u +%Y-%m-%dT%H-%MZ)"
SHORT_ID="${TOPIC_ID:0:8}"
RUN_DIR="$REPO_ROOT/testing/runs/${TS}__refresh__${SHORT_ID}"
mkdir -p "$RUN_DIR"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  REFRESH CYCLE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  API:         $API"
echo "  TOPIC_ID:    $TOPIC_ID"
echo "  MAX_AGE:     ${MAX_AGE_HOURS}h"
echo "  REPEAT:      $REPEAT"
echo "  RUN_DIR:     $RUN_DIR"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

# ── Health check ────────────────────────────────────────────
echo "◆ Health check..."
if ! curl -fsS "$API/readyz" >/dev/null 2>&1; then
  echo "  ✗ API not reachable at $API" >&2
  exit 1
fi
echo "  ✓ API is healthy"
echo

# ── Verify topic exists and is reported ─────────────────────
echo "◆ Checking topic state..."
TOPIC_STATE=$(curl -fsS "$API/v1/topics/$TOPIC_ID" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  | tee "$RUN_DIR/topic.json" \
  | jq -r '.state')

TOPIC_NAME=$(jq -r '.topic' "$RUN_DIR/topic.json")

if [ "$TOPIC_STATE" != "reported" ]; then
  echo "  ✗ Topic state is '$TOPIC_STATE' — must be 'reported' to refresh." >&2
  echo "  Run the full pipeline first: scripts/test_full_pipeline.sh" >&2
  exit 1
fi
echo "  ✓ Topic: $TOPIC_NAME"
echo "  ✓ State: $TOPIC_STATE"
echo

# ═══════════════════════════════════════════════════════════
# START MONITORING (if needed or requested)
# ═══════════════════════════════════════════════════════════

# Check if monitoring is already active
MONITOR_STATUS=$(curl -sS "$API/v1/topics/$TOPIC_ID/monitor" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" 2>/dev/null \
  | jq -r '.status // "none"' 2>/dev/null || echo "none")

if [ "$MONITOR_STATUS" = "none" ] || [ "$START_MONITOR" = "true" ]; then
  echo "◆ Starting monitoring (max_age=${MAX_AGE_HOURS}h)..."
  HTTP_CODE=$(curl -sS -o "$RUN_DIR/monitor.json" -w "%{http_code}" \
    -X POST "$API/v1/topics/$TOPIC_ID/monitor" \
    -H "Content-Type: application/json" \
    -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
    -d "{\"max_age_hours\": $MAX_AGE_HOURS}")

  if [ "$HTTP_CODE" -ge 400 ]; then
    echo "  ✗ POST /monitor failed (HTTP $HTTP_CODE):"
    jq -r '.detail // .' "$RUN_DIR/monitor.json" 2>/dev/null || cat "$RUN_DIR/monitor.json"
    echo
    echo "  Possible causes:"
    echo "    • parsed.json missing on VPS (plan artifacts not on disk)"
    echo "    • Topic has no plan_run_id"
    echo "  Debug: curl -sS \"$API/v1/topics/$TOPIC_ID\" -H \"X-API-Key: $CLAUDE_AGENT_API_KEY\" | jq '{plan_run_id, deliver_run_id, state}'"
    exit 1
  fi

  MONITOR_RESP=$(cat "$RUN_DIR/monitor.json")
  QUERIES_COUNT=$(echo "$MONITOR_RESP" | jq -r '.queries_count')
  echo "  ✓ Monitoring active — $QUERIES_COUNT short-term queries"
  echo

  # Print query plan
  echo "  ┌─── SHORT-TERM QUERIES ──────────────────────"
  echo "$MONITOR_RESP" | jq -r '
    .short_term_queries[]
    | "  │ [\(.id)] [\(.language)] p\(.priority) \(.query)"
  ' 2>/dev/null || echo "  │ (could not parse queries)"
  echo "  └─────────────────────────────────────────────"
  echo
elif [ "$MONITOR_STATUS" = "paused" ]; then
  echo "  ✗ Monitoring is paused. Re-activate with --monitor flag." >&2
  exit 1
else
  echo "◆ Monitoring already active"
  echo
fi

# ═══════════════════════════════════════════════════════════
# RUN REFRESH CYCLE(S)
# ═══════════════════════════════════════════════════════════

for CYCLE in $(seq 1 "$REPEAT"); do
  CYCLE_START=$(date +%s)

  if [ "$REPEAT" -gt 1 ]; then
    echo "━━ REFRESH CYCLE $CYCLE/$REPEAT ━━━━━━━━━━━━━━━━━━"
  else
    echo "━━ REFRESH ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  fi
  echo

  # ── Get current event seq (to filter SSE) ────────────────
  LAST_SEQ=$(jq -r '.last_event_seq // 0' "$RUN_DIR/topic.json")

  # ── Trigger refresh ──────────────────────────────────────
  echo "  ▶ Triggering refresh..."
  REFRESH_RESP=$(curl -fsS -X POST "$API/v1/topics/$TOPIC_ID/refresh" \
    -H "X-API-Key: $CLAUDE_AGENT_API_KEY")

  QUEUED=$(echo "$REFRESH_RESP" | jq -r '.queued')
  if [ "$QUEUED" != "true" ]; then
    REASON=$(echo "$REFRESH_RESP" | jq -r '.reason // "unknown"')
    echo "  ⏸ Not queued: $REASON"
    if [ "$REPEAT" -gt 1 ]; then
      echo "  Waiting 30s before retry..."
      sleep 30
      continue
    fi
    exit 0
  fi
  echo "  ✓ Refresh queued"

  # ── Tail SSE for this refresh ────────────────────────────
  REFRESH_EVENTS="$RUN_DIR/refresh_${CYCLE}_events.ndjson"
  touch "$REFRESH_EVENTS"

  curl -N -sS "$API/v1/topics/$TOPIC_ID/events?from_seq=$LAST_SEQ" \
    -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
    | sed -n 's/^data: //p' \
    | tee "$REFRESH_EVENTS" \
    | jq -rc --unbuffered '
        if   .event_type=="refresh.started"   then "  ▶ Refresh started (queries=\(.payload.queries))"
        elif .event_type=="tool_use"          then "    🔧 \(.payload.tool): \((.payload.input_preview // "")[0:80])"
        elif .event_type=="tool_result"       then "    ◀ result [err=\(.payload.is_error)]"
        elif .event_type=="refresh.completed" then "\n  ✓ Refresh done (new=\(.payload.new_sources_count), \(.payload.duration_ms)ms, $\(.payload.total_cost_usd))"
        elif .event_type=="refresh.failed"    then "\n  ✗ FAILED: \(.payload.error)"
        elif .event_type=="refresh.skipped"   then "  ⏸ Skipped: \(.payload.reason)"
        else empty end
    ' &
  TAIL_PID=$!

  # ── Wait for refresh to complete ─────────────────────────
  WAITED=0
  COMPLETED=false
  while [ "$WAITED" -lt "$TIMEOUT_SEC" ]; do
    if grep -q '"event_type":"refresh.completed"' "$REFRESH_EVENTS" 2>/dev/null; then
      COMPLETED=true
      break
    fi
    if grep -q '"event_type":"refresh.failed"' "$REFRESH_EVENTS" 2>/dev/null; then
      echo
      echo "  ✗ Refresh failed"
      grep '"event_type":"refresh.failed"' "$REFRESH_EVENTS" | jq -r '.payload.error' 2>/dev/null
      kill "$TAIL_PID" 2>/dev/null || true
      break
    fi
    sleep 2
    WAITED=$((WAITED + 2))
  done

  # Give SSE a moment to flush, then kill tail
  sleep 2
  kill "$TAIL_PID" 2>/dev/null || true
  wait "$TAIL_PID" 2>/dev/null || true

  CYCLE_END=$(date +%s)
  CYCLE_DURATION=$((CYCLE_END - CYCLE_START))

  if [ "$COMPLETED" != "true" ]; then
    if [ "$WAITED" -ge "$TIMEOUT_SEC" ]; then
      echo "  ✗ Timeout after ${TIMEOUT_SEC}s"
    fi
    if [ "$REPEAT" -gt 1 ] && [ "$CYCLE" -lt "$REPEAT" ]; then
      echo "  Continuing to next cycle..."
      continue
    fi
    exit 1
  fi

  # ── Get deltas ───────────────────────────────────────────
  echo
  DELTAS=$(curl -fsS "$API/v1/topics/$TOPIC_ID/deltas?limit=5" \
    -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
    | tee "$RUN_DIR/refresh_${CYCLE}_deltas.json")

  # ── Print delta summary ────────────────────────────────
  echo "  ┌─── REFRESH RESULT ──────────────────────────"
  echo "$DELTAS" | jq -r '
    .deltas[0] |
    "  │ Seq:            \(.seq)",
    "  │ Status:         \(.status)",
    "  │ New sources:    \(.new_sources_count)",
    "  │ Queries run:    \(.queries_executed)",
    "  │ Duration:       \(.duration_ms)ms",
    "  │ Cost:           $\(.total_cost_usd)",
    "  │ Created:        \(.created_at)"
  ' 2>/dev/null || echo "  │ (could not parse deltas)"
  echo "  └─────────────────────────────────────────────"
  echo

  # ── Print summary markdown ─────────────────────────────
  SUMMARY_MD=$(echo "$DELTAS" | jq -r '.deltas[0].summary_md // empty' 2>/dev/null)
  if [ -n "$SUMMARY_MD" ]; then
    echo "  ┌─── SUMMARY ──────────────────────────────────"
    echo "$SUMMARY_MD" | head -20 | sed 's/^/  │ /'
    echo "  └─────────────────────────────────────────────"
    echo
  fi

  # ── Get delta artifact (new sources detail) ──────────────
  LATEST_SEQ=$(echo "$DELTAS" | jq -r '.deltas[0].seq')
  if [ -n "$LATEST_SEQ" ] && [ "$LATEST_SEQ" != "null" ]; then
    curl -fsS "$API/v1/topics/$TOPIC_ID/deltas/$LATEST_SEQ" \
      -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
      | jq . > "$RUN_DIR/refresh_${CYCLE}_delta_detail.json" 2>/dev/null || true

    if [ -f "$RUN_DIR/refresh_${CYCLE}_delta_detail.json" ]; then
      echo "  ┌─── NEW SOURCES ──────────────────────────────"
      jq -r '
        (.new_sources // .sources // [])[:5][]
        | "  │ \(.published_at // "no date") — \(.title // "untitled" | .[0:60])"
      ' "$RUN_DIR/refresh_${CYCLE}_delta_detail.json" 2>/dev/null || echo "  │ (no new sources)"
      echo "  └─────────────────────────────────────────────"
      echo
    fi
  fi

  echo "  Cycle $CYCLE completed in ${CYCLE_DURATION}s"
  echo

  # ── Pause between cycles ────────────────────────────────
  if [ "$REPEAT" -gt 1 ] && [ "$CYCLE" -lt "$REPEAT" ]; then
    echo "  Waiting 10s before next cycle..."
    sleep 10
  fi
done

# ═══════════════════════════════════════════════════════════
# HISTORY: All refresh deltas for this topic
# ═══════════════════════════════════════════════════════════
echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  REFRESH HISTORY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ALL_DELTAS=$(curl -fsS "$API/v1/topics/$TOPIC_ID/deltas?limit=20" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY")

echo "$ALL_DELTAS" | jq -r '
  .deltas[] |
  "  #\(.seq)  \(.status)  new=\(.new_sources_count)  queries=\(.queries_executed)  \(.duration_ms)ms  $\(.total_cost_usd)  \(.created_at)"
' 2>/dev/null || echo "  (no refresh history)"

TOTAL_NEW=$(echo "$ALL_DELTAS" | jq '[.deltas[] | .new_sources_count // 0] | add // 0' 2>/dev/null || echo "0")
TOTAL_COST=$(echo "$ALL_DELTAS" | jq '[.deltas[] | .total_cost_usd // 0] | add // 0' 2>/dev/null || echo "0")
TOTAL_REFRESHES=$(echo "$ALL_DELTAS" | jq '.deltas | length' 2>/dev/null || echo "0")

echo
echo "  Total: $TOTAL_REFRESHES refreshes, $TOTAL_NEW new sources, \$$TOTAL_COST"
echo

# ── Artifacts ──────────────────────────────────────────────
echo "  ┌─── ARTIFACTS ───────────────────────────────"
echo "  │ $RUN_DIR/"
ls -1 "$RUN_DIR" | while read -r f; do
  SIZE=$(ls -lh "$RUN_DIR/$f" | awk '{print $5}')
  echo "  │   $f  ($SIZE)"
done
echo "  └─────────────────────────────────────────────"
echo

# ── Next steps ────────────────────────────────────────────
echo "  ┌─── NEXT STEPS ──────────────────────────────"
echo "  │ Run again:          $0 $TOPIC_ID"
echo "  │ Run 3 cycles:       $0 $TOPIC_ID --repeat 3"
echo "  │ Stop monitoring:    curl -X DELETE \"$API/v1/topics/$TOPIC_ID/monitor\" -H \"X-API-Key: $CLAUDE_AGENT_API_KEY\""
echo "  │ Full report:        cat testing/runs/*__pipeline__*/03_report.md"
echo "  └─────────────────────────────────────────────"
echo
