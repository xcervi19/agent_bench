#!/usr/bin/env bash
# scripts/test_continue_topic.sh — Resume a topic from any stage
#
# Use this after timeout or to continue from manual /proceed call.
# This script picks up where the pipeline left off and shows you the results.
#
# Sources testing/.env.testing for API/VPS config.
#
# Usage:
#   scripts/test_continue_topic.sh <TOPIC_ID>
#   scripts/test_continue_topic.sh 5b4848e1-4449-44b4-ad56-584225ceb483

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

TOPIC_ID="${1:?Usage: $0 <TOPIC_ID>}"

# ── Validate deps ───────────────────────────────────────────
for cmd in curl jq sed date; do
  command -v "$cmd" >/dev/null || { echo "missing: $cmd" >&2; exit 1; }
done

# ── Run directory ───────────────────────────────────────────
TS="$(date -u +%Y-%m-%dT%H-%MZ)"
SHORT_ID="${TOPIC_ID:0:8}"
RUN_DIR="$REPO_ROOT/testing/runs/${TS}__continue__${SHORT_ID}"
mkdir -p "$RUN_DIR"

CONTINUE_START=$(date +%s)

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  CONTINUE TOPIC"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  API:       $API"
echo "  TOPIC_ID:  $TOPIC_ID"
echo "  RUN_DIR:   $RUN_DIR"
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

# ── Fetch current topic state ───────────────────────────────
echo "◆ Fetching topic state..."
TOPIC_STATE=$(curl -fsS "$API/v1/topics/$TOPIC_ID" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  | tee "$RUN_DIR/topic_state.json" \
  | jq -r '.state // "unknown"')

TOPIC_NAME=$(jq -r '.topic' "$RUN_DIR/topic_state.json")
PLAN_RUN_ID=$(jq -r '.plan_run_id // empty' "$RUN_DIR/topic_state.json")
DELIVER_RUN_ID=$(jq -r '.deliver_run_id // empty' "$RUN_DIR/topic_state.json")

echo "  ✓ Topic: $TOPIC_NAME"
echo "  ✓ State: $TOPIC_STATE"
echo

# ── Handle each state ───────────────────────────────────────
case "$TOPIC_STATE" in
  
  "planning")
    echo "  ⏸️  Topic is still planning. Waiting for completion..."
    echo
    
    echo "◆ Waiting for plan to complete..."
    echo "  💭 Agent thinking..."
    echo
    
    # Stream events until needs_input
    PLAN_DIR="$RUN_DIR/plan/${PLAN_RUN_ID}"
    mkdir -p "$PLAN_DIR"
    
    curl -N -sS "$API/v1/topics/$TOPIC_ID/events" \
      -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
      2>/dev/null | while IFS= read -r line; do
      
      if [[ "$line" =~ ^data:\ ]]; then
        event_json=$(echo "${line#data: }" | jq . 2>/dev/null)
        event_type=$(echo "$event_json" | jq -r '.event_type // empty')
        
        case "$event_type" in
          "agent_thinking")
            thinking=$(echo "$event_json" | jq -r '.thinking // empty')
            if [[ -n "$thinking" ]]; then
              echo "    💭 $(echo "$thinking" | head -c 100)..."
            fi
            ;;
          "tool_use")
            tool=$(echo "$event_json" | jq -r '.tool // empty')
            echo "    🔧 Tool: $tool"
            ;;
          "needs_input")
            echo ""
            echo "  ✓ Plan complete!"
            break
            ;;
          "error")
            error=$(echo "$event_json" | jq -r '.error // empty')
            echo "  ❌ ERROR: $error"
            break
            ;;
        esac
      fi
    done
    
    echo
    echo "  → Topic now in 'planned_awaiting_review' state"
    echo "  → Run: scripts/test_continue_topic.sh $TOPIC_ID"
    ;;
  
  "planned_awaiting_review")
    echo "  ⏸️  Plan approved. Ready to proceed to delivery."
    echo
    echo "◆ Proceeding to delivery..."
    
    curl -fsS -X POST "$API/v1/topics/$TOPIC_ID/proceed" \
      -H "X-API-Key: $CLAUDE_AGENT_API_KEY" >/dev/null
    
    echo "  ✓ Proceeding..."
    echo
    
    # Stream delivery events
    echo "  🤖 Agent searching..."
    echo
    
    DELIVER_DIR="$RUN_DIR/deliver/${DELIVER_RUN_ID}"
    mkdir -p "$DELIVER_DIR"
    
    curl -N -sS "$API/v1/topics/$TOPIC_ID/events" \
      -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
      2>/dev/null | while IFS= read -r line; do
      
      if [[ "$line" =~ ^data:\ ]]; then
        event_json=$(echo "${line#data: }" | jq . 2>/dev/null)
        event_type=$(echo "$event_json" | jq -r '.event_type // empty')
        
        case "$event_type" in
          "agent_thinking")
            thinking=$(echo "$event_json" | jq -r '.thinking // empty')
            if [[ -n "$thinking" ]]; then
              echo "    💭 $(echo "$thinking" | head -c 100)..."
            fi
            ;;
          "tool_success")
            query=$(echo "$event_json" | jq -r '.query // empty')
            results=$(echo "$event_json" | jq -r '.result_count // 0')
            if [[ -n "$query" ]]; then
              echo "    ✓ Query: \"$query\" → $results results"
            fi
            ;;
          "assistant_message")
            text=$(echo "$event_json" | jq -r '.text // empty' | head -c 80)
            if [[ -n "$text" ]]; then
              echo "    💬 $text..."
            fi
            ;;
          "done")
            echo ""
            echo "  ✓ Delivery complete!"
            break
            ;;
          "error")
            error=$(echo "$event_json" | jq -r '.error // empty')
            echo "  ❌ ERROR: $error"
            break
            ;;
        esac
      fi
    done
    
    echo
    ;;
  
  "delivering")
    echo "  🔄 Topic is currently delivering. Waiting..."
    echo
    
    echo "◆ Streaming delivery progress..."
    echo "  🤖 Agent searching..."
    echo
    
    DELIVER_DIR="$RUN_DIR/deliver/${DELIVER_RUN_ID}"
    mkdir -p "$DELIVER_DIR"
    
    curl -N -sS "$API/v1/topics/$TOPIC_ID/events" \
      -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
      2>/dev/null | while IFS= read -r line; do
      
      if [[ "$line" =~ ^data:\ ]]; then
        event_json=$(echo "${line#data: }" | jq . 2>/dev/null)
        event_type=$(echo "$event_json" | jq -r '.event_type // empty')
        
        case "$event_type" in
          "agent_thinking")
            thinking=$(echo "$event_json" | jq -r '.thinking // empty')
            if [[ -n "$thinking" ]]; then
              echo "    💭 $(echo "$thinking" | head -c 100)..."
            fi
            ;;
          "tool_success")
            query=$(echo "$event_json" | jq -r '.query // empty')
            results=$(echo "$event_json" | jq -r '.result_count // 0')
            if [[ -n "$query" ]]; then
              echo "    ✓ Query: \"$query\" → $results results"
            fi
            ;;
          "done")
            echo ""
            echo "  ✓ Delivery complete!"
            break
            ;;
          "error")
            error=$(echo "$event_json" | jq -r '.error // empty')
            echo "  ❌ ERROR: $error"
            break
            ;;
        esac
      fi
    done
    
    echo
    ;;
  
  "reported")
    echo "  ✅ Topic complete! Report ready."
    echo
    ;;
  
  "failed")
    ERROR=$(jq -r '.error // "unknown error"' "$RUN_DIR/topic_state.json")
    echo "  ❌ Topic failed: $ERROR" >&2
    exit 1
    ;;
  
  "cancelled")
    echo "  ⊘ Topic was cancelled."
    exit 0
    ;;
  
  *)
    echo "  ❓ Unknown state: $TOPIC_STATE" >&2
    exit 1
    ;;
esac

# ═══════════════════════════════════════════════════════════
# FETCH & DISPLAY RESULTS
# ═══════════════════════════════════════════════════════════

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  RESULTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

# Fetch deliver run ID (might have changed)
DELIVER_RUN_ID=$(curl -fsS "$API/v1/topics/$TOPIC_ID" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  | jq -r '.deliver_run_id // empty')

if [[ -z "$DELIVER_RUN_ID" ]] || [[ "$DELIVER_RUN_ID" == "null" ]]; then
  echo "  (no deliver run yet)"
  exit 0
fi

DELIVER_DIR="$RUN_DIR/deliver/${DELIVER_RUN_ID}"
mkdir -p "$DELIVER_DIR"

# Save artifacts
echo "◆ Fetching report..."

curl -fsS "$API/v1/topics/$TOPIC_ID/news" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  | jq . > "$DELIVER_DIR/news.json" 2>/dev/null || echo "(news not available)"

curl -fsS "$API/v1/topics/$TOPIC_ID/report" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  | jq . > "$DELIVER_DIR/report.json" 2>/dev/null || echo "(report not available)"

curl -fsS "$API/v1/topics/$TOPIC_ID/report.md" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  > "$DELIVER_DIR/report.md" 2>/dev/null || echo "(report.md not available)"

echo "  ✓ Report saved"
echo

# ── Report summary ─────────────────────────────────────────
echo "  ┌─── REPORT SUMMARY ──────────────────────────"
if [ -f "$DELIVER_DIR/report.json" ]; then
  jq -r '
    "  │ Thesis:      \(.thesis_status // .working_thesis // "n/a" | .[0:80])",
    "  │ Findings:    \(.key_findings // [] | length)",
    "  │ Scenarios:   \(.scenarios // [] | length)",
    "  │ Sources:     \(.sources_count // (.sources // [] | length))"
  ' "$DELIVER_DIR/report.json" 2>/dev/null || echo "  │ (parse error)"
fi
echo "  └─────────────────────────────────────────────"
echo

# ── Top sources ─────────────────────────────────────────────
echo "  ┌─── TOP SOURCES ──────────────────────────────"
if [ -f "$DELIVER_DIR/news.json" ]; then
  jq -r '
    [.sources[] | select(.relevance_score != null)]
    | sort_by(-.relevance_score)
    | .[:5][]
    | "  │ [\(.relevance_score)] \(.title // "untitled" | .[0:60])"
  ' "$DELIVER_DIR/news.json" 2>/dev/null || echo "  │ (no sources)"
fi
echo "  └─────────────────────────────────────────────"
echo

# ── Report preview ──────────────────────────────────────────
echo "  ┌─── REPORT PREVIEW ───────────────────────────"
if [ -f "$DELIVER_DIR/report.md" ] && [ -s "$DELIVER_DIR/report.md" ]; then
  head -15 "$DELIVER_DIR/report.md" | sed 's/^/  │ /'
  echo "  │ ..."
fi
echo "  └─────────────────────────────────────────────"
echo

# ── Artifacts ──────────────────────────────────────────────
CONTINUE_END=$(date +%s)
CONTINUE_DURATION=$((CONTINUE_END - CONTINUE_START))

echo "✅ Continue complete!"
echo "   Duration: ${CONTINUE_DURATION}s"
echo "   Run Dir:  $RUN_DIR"
echo
echo "  Next steps:"
echo "    • Full report:  cat $DELIVER_DIR/report.md"
echo "    • All sources:  jq '.sources' $DELIVER_DIR/news.json"
echo "    • Start monitoring: scripts/test_refresh_cycle.sh $TOPIC_ID"
echo
