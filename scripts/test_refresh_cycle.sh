#!/usr/bin/env bash
# scripts/test_refresh_cycle.sh — Run refresh on a reported topic to get latest news
#
# Sources testing/.env.testing for API/VPS config.
# SSE-streams live progress (tool calls, search results, phase changes).
# After completion, fetches news.json for the actual queries + sources found.
#
# Usage:
#   scripts/test_refresh_cycle.sh <TOPIC_ID>                    # single refresh
#   scripts/test_refresh_cycle.sh <TOPIC_ID> --monitor          # start monitoring first
#   scripts/test_refresh_cycle.sh <TOPIC_ID> --max-age 24       # override max_age_hours
#   scripts/test_refresh_cycle.sh <TOPIC_ID> --repeat 3         # run N refresh cycles
#   scripts/test_refresh_cycle.sh <TOPIC_ID> --timeout 600      # custom timeout (default 900)

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
TOPIC_ID="${1:?Usage: $0 <TOPIC_ID> [--monitor] [--max-age N] [--repeat N] [--timeout N]}"
shift

START_MONITOR=false
MAX_AGE_HOURS="${REFRESH_MAX_AGE_HOURS:-48}"
REPEAT=1
TIMEOUT_SEC="${TIMEOUT_SEC:-900}"

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
echo "  TIMEOUT:     ${TIMEOUT_SEC}s"
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
TOPIC_JSON=$(curl -fsS "$API/v1/topics/$TOPIC_ID" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY")
echo "$TOPIC_JSON" > "$RUN_DIR/topic.json"

TOPIC_STATE=$(echo "$TOPIC_JSON" | jq -r '.state')
TOPIC_NAME=$(echo "$TOPIC_JSON" | jq -r '.topic')

if [ "$TOPIC_STATE" != "reported" ]; then
  echo "  ✗ Topic state is '$TOPIC_STATE' — must be 'reported' to refresh." >&2
  exit 1
fi
echo "  ✓ Topic: $TOPIC_NAME"
echo "  ✓ State: $TOPIC_STATE"
echo

# ═══════════════════════════════════════════════════════════
# START MONITORING (if needed or requested)
# ═══════════════════════════════════════════════════════════

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
    exit 1
  fi

  MONITOR_RESP=$(cat "$RUN_DIR/monitor.json")
  QUERIES_COUNT=$(echo "$MONITOR_RESP" | jq -r '.queries_count')
  echo "  ✓ Monitoring active — $QUERIES_COUNT short-term queries"
  echo

  echo "  ┌─── SHORT-TERM QUERIES ──────────────────────"
  echo "$MONITOR_RESP" | jq -r '
    .short_term_queries[]
    | "  │ [\(.id)] p\(.priority) \(.query)"
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
  LAST_SEQ=$(echo "$TOPIC_JSON" | jq -r '.last_event_seq // 0')

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
  echo

  # ── Stream SSE with live progress ────────────────────────
  # The SSE endpoint stays open during active refresh (even for reported topics).
  # We display tool_use events in real time, and stop on refresh.completed/failed.
  REFRESH_EVENTS="$RUN_DIR/refresh_${CYCLE}_events.ndjson"
  : > "$REFRESH_EVENTS"

  echo "  ┌─── LIVE PROGRESS ───────────────────────────"

  # Stream SSE, filter data lines, and display progress
  # The while-read loop runs in the current shell so we can break on terminal events.
  set +e
  (curl -N -sS --max-time "$TIMEOUT_SEC" \
    "$API/v1/topics/$TOPIC_ID/events?from_seq=$LAST_SEQ" \
    -H "X-API-Key: $CLAUDE_AGENT_API_KEY" 2>/dev/null \
    || true) \
  | sed -un 's/^data: //p' \
  | while IFS= read -r line; do
      echo "$line" >> "$REFRESH_EVENTS"
      EVENT_TYPE=$(echo "$line" | jq -r '.event_type // empty' 2>/dev/null) || continue

      case "$EVENT_TYPE" in
        refresh.started)
          Q=$(echo "$line" | jq -r '.payload.queries // "?"' 2>/dev/null)
          RUN_ID=$(echo "$line" | jq -r '.payload.run_id // "?"' 2>/dev/null)
          echo "  │ ▶ Refresh started — $Q queries  [run: ${RUN_ID:0:8}]"
          ;;

        tool_use)
          TOOL=$(echo "$line" | jq -r '.payload.tool // "?"' 2>/dev/null)
          PREVIEW=$(echo "$line" | jq -r '.payload.input_preview // ""' 2>/dev/null)

          case "$TOOL" in
            WebSearch|web_search)
              # Extract query from preview: {'query': 'xxx'} or {"query": "xxx"}
              QUERY=$(echo "$PREVIEW" | sed -n "s/.*['\"]query['\"]:[[:space:]]*['\"]\\([^'\"]*\\)['\"].*/\\1/p" | head -1)
              [ -z "$QUERY" ] && QUERY="${PREVIEW:0:80}"
              echo "  │ 🔍 $QUERY"
              ;;
            WebFetch|web_fetch)
              URL=$(echo "$PREVIEW" | sed -n "s/.*['\"]url['\"]:[[:space:]]*['\"]\\([^'\"]*\\)['\"].*/\\1/p" | head -1)
              [ -z "$URL" ] && URL="${PREVIEW:0:80}"
              echo "  │ 📄 Fetch: ${URL:0:80}"
              ;;
            Read|read)
              FILE=$(echo "$PREVIEW" | sed -n "s/.*['\"]file_path['\"]:[[:space:]]*['\"]\\([^'\"]*\\)['\"].*/\\1/p" | head -1)
              [ -z "$FILE" ] && FILE="${PREVIEW:0:60}"
              echo "  │ 📁 Read: ${FILE##*/}"
              ;;
            Write|write)
              FILE=$(echo "$PREVIEW" | sed -n "s/.*['\"]file_path['\"]:[[:space:]]*['\"]\\([^'\"]*\\)['\"].*/\\1/p" | head -1)
              [ -z "$FILE" ] && FILE="${PREVIEW:0:60}"
              echo "  │ ✏️  Write: ${FILE##*/}"
              ;;
            Bash|bash)
              echo "  │ 💻 Bash: ${PREVIEW:0:80}"
              ;;
            *)
              echo "  │ 🔧 $TOOL"
              ;;
          esac
          ;;

        tool_result)
          IS_ERR=$(echo "$line" | jq -r '.payload.is_error // false' 2>/dev/null)
          if [ "$IS_ERR" = "true" ]; then
            PREVIEW=$(echo "$line" | jq -r '.payload.output_preview // "" | .[0:100]' 2>/dev/null)
            echo "  │  ⚠️  Tool error: $PREVIEW"
          fi
          # Successful results: stay quiet to reduce noise
          ;;

        refresh.completed)
          NEW=$(echo "$line" | jq -r '.payload.new_sources_count // 0' 2>/dev/null)
          DUR=$(echo "$line" | jq -r '.payload.duration_ms // 0' 2>/dev/null)
          COST=$(echo "$line" | jq -r '.payload.total_cost_usd // 0' 2>/dev/null)
          DUR_S=$((DUR / 1000))
          echo "  │"
          echo "  │ ✅ Completed — ${NEW} new sources, ${DUR_S}s, \$${COST}"
          # Signal done — the pipe will close when curl exits
          break
          ;;

        refresh.failed)
          ERR=$(echo "$line" | jq -r '.payload.error // "unknown"' 2>/dev/null)
          echo "  │"
          echo "  │ ❌ FAILED: $ERR"
          break
          ;;

        refresh.skipped)
          REASON=$(echo "$line" | jq -r '.payload.reason // "unknown"' 2>/dev/null)
          echo "  │ ⏸  Skipped: $REASON"
          break
          ;;
      esac
    done
  set -e

  echo "  └─────────────────────────────────────────────"
  echo

  # ── Determine final status ──────────────────────────────
  # Check events file for terminal event; fall back to polling if SSE timed out
  COMPLETED=false
  FAILED=false

  if grep -q '"refresh.completed"' "$REFRESH_EVENTS" 2>/dev/null; then
    COMPLETED=true
  elif grep -q '"refresh.failed"' "$REFRESH_EVENTS" 2>/dev/null; then
    FAILED=true
  else
    # SSE didn't deliver terminal event — poll deltas
    echo "  ⏳ SSE ended without terminal event, polling deltas..."
    POLL_WAITED=0
    POLL_TIMEOUT=120
    while [ "$POLL_WAITED" -lt "$POLL_TIMEOUT" ]; do
      LATEST_STATUS=$(curl -sS "$API/v1/topics/$TOPIC_ID/deltas?limit=1" \
        -H "X-API-Key: $CLAUDE_AGENT_API_KEY" 2>/dev/null \
        | jq -r '.deltas[0].status // "none"' 2>/dev/null || echo "none")
      if [ "$LATEST_STATUS" = "completed" ]; then
        COMPLETED=true
        echo "  ✓ Completed (via polling)"
        break
      elif [ "$LATEST_STATUS" = "failed" ]; then
        FAILED=true
        echo "  ✗ Failed (via polling)"
        break
      fi
      sleep 5
      POLL_WAITED=$((POLL_WAITED + 5))
      printf "\r  ⏳ Polling... %ds" "$POLL_WAITED"
    done
    echo
  fi

  CYCLE_END=$(date +%s)
  CYCLE_DURATION=$((CYCLE_END - CYCLE_START))

  if [ "$COMPLETED" != "true" ]; then
    echo "  ✗ Refresh did not complete after ${CYCLE_DURATION}s"
    if [ "$FAILED" = "true" ]; then
      curl -sS "$API/v1/topics/$TOPIC_ID/deltas?limit=1" \
        -H "X-API-Key: $CLAUDE_AGENT_API_KEY" 2>/dev/null \
        | jq -r '.deltas[0] | "  Error: \(.error // "unknown")"' 2>/dev/null
    fi
    if [ "$REPEAT" -gt 1 ] && [ "$CYCLE" -lt "$REPEAT" ]; then
      continue
    fi
    exit 1
  fi

  # ═══════════════════════════════════════════════════════════
  # RESULTS
  # ═══════════════════════════════════════════════════════════

  DELTAS=$(curl -fsS "$API/v1/topics/$TOPIC_ID/deltas?limit=5" \
    -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
    | tee "$RUN_DIR/refresh_${CYCLE}_deltas.json")

  LATEST_SEQ=$(echo "$DELTAS" | jq -r '.deltas[0].seq')

  # ── Delta summary ───────────────────────────────────────
  echo "  ┌─── RESULT ──────────────────────────────────"
  echo "$DELTAS" | jq -r '
    .deltas[0] |
    "  │ Seq:          \(.seq)",
    "  │ New sources:  \(.new_sources_count)",
    "  │ Queries:      \(.queries_executed)",
    "  │ Duration:     \(.duration_ms / 1000 | floor)s",
    "  │ Cost:         $\(.total_cost_usd | tostring | .[0:8])"
  ' 2>/dev/null || echo "  │ (could not parse)"
  echo "  └─────────────────────────────────────────────"
  echo

  # ── Summary text ─────────────────────────────────────────
  SUMMARY_MD=$(echo "$DELTAS" | jq -r '.deltas[0].summary_md // empty' 2>/dev/null)
  if [ -n "$SUMMARY_MD" ]; then
    echo "  ┌─── SUMMARY ──────────────────────────────────"
    echo "$SUMMARY_MD" | fold -s -w 78 | head -20 | sed 's/^/  │ /'
    echo "  └─────────────────────────────────────────────"
    echo
  fi

  # ── Key changes from delta.json ──────────────────────────
  if [ -n "$LATEST_SEQ" ] && [ "$LATEST_SEQ" != "null" ]; then
    curl -fsS "$API/v1/topics/$TOPIC_ID/deltas/$LATEST_SEQ" \
      -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
      > "$RUN_DIR/refresh_${CYCLE}_delta.json" 2>/dev/null || true

    if [ -f "$RUN_DIR/refresh_${CYCLE}_delta.json" ]; then
      KC=$(jq -r '.key_changes // [] | length' "$RUN_DIR/refresh_${CYCLE}_delta.json" 2>/dev/null || echo "0")
      if [ "$KC" -gt 0 ]; then
        echo "  ┌─── KEY CHANGES ──────────────────────────────"
        jq -r '.key_changes[] | "  │ [\(.confidence)] \(.finding | .[0:72]) [\(.source_ids | join(","))]"' \
          "$RUN_DIR/refresh_${CYCLE}_delta.json" 2>/dev/null
        echo "  └─────────────────────────────────────────────"
        echo
      fi
    fi
  fi

  # ── News sources from news.json ──────────────────────────
  if [ -n "$LATEST_SEQ" ] && [ "$LATEST_SEQ" != "null" ]; then
    curl -fsS "$API/v1/topics/$TOPIC_ID/deltas/$LATEST_SEQ/news" \
      -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
      > "$RUN_DIR/refresh_${CYCLE}_news.json" 2>/dev/null || true

    if [ -f "$RUN_DIR/refresh_${CYCLE}_news.json" ] && [ -s "$RUN_DIR/refresh_${CYCLE}_news.json" ]; then
      # Queries executed
      echo "  ┌─── QUERIES EXECUTED ─────────────────────────"
      jq -r '
        .executed_queries // [] | .[]
        | "  │ [\(.id)] \(.query | .[0:60]) → \(.results_count // 0) hits"
      ' "$RUN_DIR/refresh_${CYCLE}_news.json" 2>/dev/null || echo "  │ (no query data)"
      echo "  └─────────────────────────────────────────────"
      echo

      # Dedup stats
      echo "  ┌─── FILTERS ─────────────────────────────────"
      jq -r '
        .drops // {} |
        "  │ Already seen:    \(.already_seen // 0)",
        "  │ Too old:         \(.too_old // 0)",
        "  │ Low relevance:   \(.low_relevance // 0)",
        "  │ Intra-batch dup: \(.intra_batch_dup // 0)"
      ' "$RUN_DIR/refresh_${CYCLE}_news.json" 2>/dev/null || echo "  │ (no filter stats)"
      echo "  └─────────────────────────────────────────────"
      echo

      # Sources
      SRC_COUNT=$(jq '.sources | length' "$RUN_DIR/refresh_${CYCLE}_news.json" 2>/dev/null || echo "0")
      echo "  ┌─── SOURCES ($SRC_COUNT) ───────────────────────────"
      jq -r '
        .sources[:10][] |
        "  │ [\(.id)] rel=\(.relevance_score)  \(.source_class // "?")",
        "  │   \(.title // "untitled" | .[0:70])",
        "  │   \(.url | .[0:78])",
        "  │   \(.published_at // "no date")  queries: \(.query_ids | join(","))",
        "  │"
      ' "$RUN_DIR/refresh_${CYCLE}_news.json" 2>/dev/null || echo "  │ (no sources)"
      echo "  └─────────────────────────────────────────────"
      echo
    fi
  fi

  # ── Refresh report.md ────────────────────────────────────
  if [ -n "$LATEST_SEQ" ] && [ "$LATEST_SEQ" != "null" ]; then
    curl -fsS "$API/v1/topics/$TOPIC_ID/deltas/$LATEST_SEQ/report" \
      -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
      > "$RUN_DIR/refresh_${CYCLE}_report.md" 2>/dev/null || true
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
# HISTORY
# ═══════════════════════════════════════════════════════════
echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  REFRESH HISTORY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ALL_DELTAS=$(curl -fsS "$API/v1/topics/$TOPIC_ID/deltas?limit=20" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY")

echo "$ALL_DELTAS" | jq -r '
  .deltas[] |
  "  #\(.seq)  \(.status)  new=\(.new_sources_count)  q=\(.queries_executed)  \(if .duration_ms then (.duration_ms / 1000 | floor | tostring) + "s" else "-" end)  $\(.total_cost_usd // 0 | tostring | .[0:7])  \(.created_at | .[0:19])"
' 2>/dev/null || echo "  (no history)"

TOTAL_NEW=$(echo "$ALL_DELTAS" | jq '[.deltas[] | .new_sources_count // 0] | add // 0' 2>/dev/null || echo "0")
TOTAL_COST=$(echo "$ALL_DELTAS" | jq '[.deltas[] | .total_cost_usd // 0] | add // 0 | tostring | .[0:7]' 2>/dev/null || echo "0")
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
echo "  │ Run again:       $0 $TOPIC_ID"
echo "  │ Run 3 cycles:    $0 $TOPIC_ID --repeat 3"
echo "  │ View sources:    jq '.sources[]' $RUN_DIR/refresh_1_news.json"
echo "  │ View report:     cat $RUN_DIR/refresh_1_report.md"
echo "  └─────────────────────────────────────────────"
echo
