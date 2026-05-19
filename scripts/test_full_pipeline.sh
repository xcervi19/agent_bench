#!/usr/bin/env bash
# scripts/test_full_pipeline.sh — Run full A→Z pipeline: create → plan → approve → deliver → report
#
# Sources testing/.env.testing for API/VPS config.
# Saves all artifacts to testing/runs/<timestamp>__pipeline__<slug>/
# Prints timing, cost, and quality summary at the end.
#
# Usage:
#   scripts/test_full_pipeline.sh                              # default Hormuz topic
#   scripts/test_full_pipeline.sh "LNG supply disruption EU"   # custom topic
#   AUTO_PROCEED=false scripts/test_full_pipeline.sh           # pause for manual plan review

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

TOPIC="${1:-$DEFAULT_TOPIC}"
AUTO_PROCEED="${AUTO_PROCEED:-true}"
TIMEOUT_SEC="${TIMEOUT_SEC:-900}"

# ── Validate deps ───────────────────────────────────────────
for cmd in curl jq sed tee date tr; do
  command -v "$cmd" >/dev/null || { echo "missing: $cmd" >&2; exit 1; }
done

# ── Run directory ───────────────────────────────────────────
TS="$(date -u +%Y-%m-%dT%H-%MZ)"
SLUG="$(echo "$TOPIC" | tr 'A-Z' 'a-z' | tr -cs 'a-z0-9' '-' | sed 's/^-//;s/-$//' | cut -c1-50)"
RUN_DIR="$REPO_ROOT/testing/runs/${TS}__pipeline__${SLUG}"
mkdir -p "$RUN_DIR"

PIPELINE_START=$(date +%s)

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  FULL PIPELINE TEST (A → Z)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  API:           $API"
echo "  TOPIC:         $TOPIC"
echo "  AUTO_PROCEED:  $AUTO_PROCEED"
echo "  TIMEOUT:       ${TIMEOUT_SEC}s"
echo "  RUN_DIR:       $RUN_DIR"
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

# ═══════════════════════════════════════════════════════════
# STAGE 1: CREATE TOPIC → /newsfind-plan
# ═══════════════════════════════════════════════════════════
STAGE1_START=$(date +%s)
echo "━━ STAGE 1: CREATE TOPIC + PLAN ━━━━━━━━━━━━━━━━━━"
echo

TOPIC_ID=$(curl -fsS -X POST "$API/v1/topics" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -d "$(jq -nc --arg t "$TOPIC" '{topic:$t}')" \
  | tee "$RUN_DIR/create.json" \
  | jq -r .topic_id)

echo "  topic_id = $TOPIC_ID"
echo "  state    = planning"
echo

# ── Tail SSE events in background ──────────────────────────
EVENTS="$RUN_DIR/events.ndjson"
touch "$EVENTS"

curl -N -sS "$API/v1/topics/$TOPIC_ID/events" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  | sed -n 's/^data: //p' \
  | tee "$EVENTS" \
  | jq -rc --unbuffered '
      if   .event_type=="stage.started"   then "  ▶ \(.payload.stage) started"
      elif .event_type=="tool_use"        then "    🔧 \(.payload.tool): \((.payload.input_preview // "")[0:80])"
      elif .event_type=="tool_result"     then "    ◀ result [err=\(.payload.is_error)]"
      elif .event_type=="stage.finished"  then "  ✓ \(.payload.stage) done (\(.payload.duration_ms)ms, $\(.payload.total_cost_usd))"
      elif .event_type=="intro.ready"     then "\n  ★ INTRO READY: \((.payload.headline // "")[0:80])"
      elif .event_type=="needs_input"     then "\n  ⏸ GATE: \(.payload.gate)"
      elif .event_type=="report.ready"    then "\n  ★ REPORT READY"
      elif .event_type=="state.changed"   then "  → state: \(.payload.from) → \(.payload.to)"
      elif .event_type=="error"           then "\n  ✗ ERROR: \(.payload.error)"
      elif .event_type=="refresh.started" then "\n  ▶ REFRESH started (queries=\(.payload.queries))"
      elif .event_type=="refresh.completed" then "  ✓ REFRESH done (new=\(.payload.new_sources_count), $\(.payload.total_cost_usd))"
      elif .event_type=="refresh.failed"  then "  ✗ REFRESH FAILED: \(.payload.error)"
      else empty end
  ' &
TAIL_PID=$!
trap 'kill "$TAIL_PID" 2>/dev/null || true' EXIT

# ── Wait for plan to finish ────────────────────────────────
wait_for_event() {
  local name="$1"; local waited=0
  while ! grep -q "\"event_type\":\"$name\"" "$EVENTS" 2>/dev/null; do
    # Check for terminal errors
    if grep -qE '"event_type":"error"' "$EVENTS" 2>/dev/null; then
      echo
      echo "  ✗ Pipeline failed during wait for $name"
      grep '"event_type":"error"' "$EVENTS" | tail -1 | jq -r '.payload.error // "unknown"'
      # Save what we have
      curl -fsS "$API/v1/topics/$TOPIC_ID" \
        -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
        | jq . > "$RUN_DIR/topic.json" 2>/dev/null || true
      exit 1
    fi
    sleep 2; waited=$((waited+2))
    if [ "$waited" -gt "$TIMEOUT_SEC" ]; then
      echo "  ✗ Timeout waiting for $name after ${waited}s" >&2
      exit 1
    fi
  done
}

wait_for_event "needs_input"
STAGE1_END=$(date +%s)
STAGE1_DURATION=$((STAGE1_END - STAGE1_START))

echo
echo "  ────────────────────────────────────────────"
echo "  Plan completed in ${STAGE1_DURATION}s"
echo

# ── Fetch plan_run_id from topic state ─────────────────────
PLAN_RUN_ID=$(curl -fsS "$API/v1/topics/$TOPIC_ID" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  | jq -r '.plan_run_id // empty')
PLAN_DIR="$RUN_DIR/plan/${PLAN_RUN_ID}"
mkdir -p "$PLAN_DIR"

# ── Save plan artifacts ────────────────────────────────────
curl -fsS "$API/v1/topics/$TOPIC_ID/parsed" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  | jq . > "$PLAN_DIR/parsed.json" 2>/dev/null || echo "  (parsed not available)"

curl -fsS "$API/v1/topics/$TOPIC_ID/intro.md" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  > "$PLAN_DIR/intro.md" 2>/dev/null || echo "  (intro.md not available)"

# ── Print plan summary ────────────────────────────────────
echo "  ┌─── PLAN SUMMARY ───────────────────────────"
if [ -f "$PLAN_DIR/parsed.json" ]; then
  jq -r '
    "  │ Queries:    \(.queries | length)",
    "  │ Languages:  \(.queries | map(.language) | unique | join(", "))",
    "  │ RAG refs:   \(.rag_context_refs // [] | length)",
    "  │ Thesis:     \(.working_thesis // "n/a" | .[0:80])"
  ' "$PLAN_DIR/parsed.json" 2>/dev/null || echo "  │ (parse error)"
fi
echo "  └─────────────────────────────────────────────"
echo

# ── Print intro ───────────────────────────────────────────
if [ -f "$PLAN_DIR/intro.md" ] && [ -s "$PLAN_DIR/intro.md" ]; then
  echo "  ┌─── INTRO (first 10 lines) ─────────────────"
  head -10 "$PLAN_DIR/intro.md" | sed 's/^/  │ /'
  echo "  └─────────────────────────────────────────────"
  echo
fi

# ═══════════════════════════════════════════════════════════
# GATE: Manual approval or auto-proceed
# ═══════════════════════════════════════════════════════════
if [ "$AUTO_PROCEED" != "true" ]; then
  echo "  ⏸ Review the plan above."
  echo "    Artifacts: $PLAN_DIR/parsed.json, $PLAN_DIR/intro.md"
  echo
  read -r -p "  Press ENTER to proceed, or Ctrl+C to abort → " _
  echo
fi

# ═══════════════════════════════════════════════════════════
# STAGE 2: PROCEED → /newsfind-deliver → REPORT
# ═══════════════════════════════════════════════════════════
STAGE2_START=$(date +%s)
echo "━━ STAGE 2: DELIVER (web search + report) ━━━━━━"
echo

curl -fsS -X POST "$API/v1/topics/$TOPIC_ID/proceed" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" >/dev/null

echo "  Proceeding... (this takes 5–12 minutes)"
echo

wait_for_event "report.ready"
STAGE2_END=$(date +%s)
STAGE2_DURATION=$((STAGE2_END - STAGE2_START))

echo
echo "  ────────────────────────────────────────────"
echo "  Deliver completed in ${STAGE2_DURATION}s"
echo

# ── Fetch deliver_run_id from topic state ──────────────────
DELIVER_RUN_ID=$(curl -fsS "$API/v1/topics/$TOPIC_ID" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  | tee "$RUN_DIR/topic.json" \
  | jq -r '.deliver_run_id // empty')
DELIVER_DIR="$RUN_DIR/deliver/${DELIVER_RUN_ID}"
mkdir -p "$DELIVER_DIR"

# ── Save report artifacts ──────────────────────────────────
for art in news report; do
  curl -fsS "$API/v1/topics/$TOPIC_ID/$art" \
    -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
    | jq . > "$DELIVER_DIR/${art}.json" 2>/dev/null || echo "  ($art not available)"
done

curl -fsS "$API/v1/topics/$TOPIC_ID/report.md" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  > "$DELIVER_DIR/report.md" 2>/dev/null || echo "  (report.md not available)"

# ═══════════════════════════════════════════════════════════
# RESULTS SUMMARY
# ═══════════════════════════════════════════════════════════
PIPELINE_END=$(date +%s)
PIPELINE_DURATION=$((PIPELINE_END - PIPELINE_START))

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  PIPELINE COMPLETE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

# ── Timing ─────────────────────────────────────────────────
echo "  ┌─── TIMING ──────────────────────────────────"
echo "  │ Stage 1 (plan):    ${STAGE1_DURATION}s"
echo "  │ Stage 2 (deliver): ${STAGE2_DURATION}s"
echo "  │ Total:             ${PIPELINE_DURATION}s"
echo "  └─────────────────────────────────────────────"
echo

# ── Cost ───────────────────────────────────────────────────
echo "  ┌─── COST ────────────────────────────────────"
if [ -f "$EVENTS" ]; then
  jq -rs '
    [.[] | select(.event_type=="stage.finished")] |
    map("  │ \(.payload.stage): $\(.payload.total_cost_usd // 0)") | .[]
  ' "$EVENTS" 2>/dev/null || echo "  │ (cost data not available)"
  TOTAL_COST=$(jq -rs '[.[] | select(.event_type=="stage.finished") | .payload.total_cost_usd // 0] | add // 0' "$EVENTS" 2>/dev/null || echo "0")
  echo "  │ TOTAL: \$$TOTAL_COST"
fi
echo "  └─────────────────────────────────────────────"
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

# ── News sources ──────────────────────────────────────────
echo "  ┌─── NEWS SOURCES (top 5 by relevance) ───────"
if [ -f "$DELIVER_DIR/news.json" ]; then
  jq -r '
    [.sources[] | select(.relevance_score != null)]
    | sort_by(-.relevance_score)
    | .[:5][]
    | "  │ [\(.relevance_score)] \(.title // "untitled" | .[0:60])"
  ' "$DELIVER_DIR/news.json" 2>/dev/null || echo "  │ (no sources)"
  TOTAL_SOURCES=$(jq '.sources | length' "$DELIVER_DIR/news.json" 2>/dev/null || echo "0")
  echo "  │ Total sources: $TOTAL_SOURCES"
fi
echo "  └─────────────────────────────────────────────"
echo

# ── Latest news ──────────────────────────────────────────
echo "  ┌─── LATEST SOURCES (by date) ────────────────"
if [ -f "$DELIVER_DIR/news.json" ]; then
  jq -r '
    [.sources[] | select(.published_at != null)]
    | sort_by(.published_at) | reverse
    | .[:3][]
    | "  │ \(.published_at) — \(.title // "untitled" | .[0:50]) [\(.publisher // "?")]"
  ' "$DELIVER_DIR/news.json" 2>/dev/null || echo "  │ (no dated sources)"
fi
echo "  └─────────────────────────────────────────────"
echo

# ── Report markdown (first 15 lines) ─────────────────────
if [ -f "$DELIVER_DIR/report.md" ] && [ -s "$DELIVER_DIR/report.md" ]; then
  echo "  ┌─── REPORT (first 15 lines) ──────────────────"
  head -15 "$DELIVER_DIR/report.md" | sed 's/^/  │ /'
  echo "  │ ..."
  REPORT_LINES=$(wc -l < "$DELIVER_DIR/report.md" | tr -d ' ')
  echo "  │ (total: ${REPORT_LINES} lines)"
  echo "  └─────────────────────────────────────────────"
  echo
fi

# ── Artifacts ──────────────────────────────────────────────
echo "  ┌─── ARTIFACTS ───────────────────────────────"
echo "  │ $RUN_DIR/"
echo "  │   events.ndjson"
echo "  │   create.json"
echo "  │   topic.json"
echo "  │   plan/$PLAN_RUN_ID/"
ls -1 "$PLAN_DIR" 2>/dev/null | while read -r f; do
  SIZE=$(ls -lh "$PLAN_DIR/$f" | awk '{print $5}')
  echo "  │     $f  ($SIZE)"
done
echo "  │   deliver/$DELIVER_RUN_ID/"
ls -1 "$DELIVER_DIR" 2>/dev/null | while read -r f; do
  SIZE=$(ls -lh "$DELIVER_DIR/$f" | awk '{print $5}')
  echo "  │     $f  ($SIZE)"
done
echo "  └─────────────────────────────────────────────"
echo

# ── For next step ─────────────────────────────────────────
echo "  ┌─── NEXT STEPS ──────────────────────────────"
echo "  │ View full report:   cat $DELIVER_DIR/report.md"
echo "  │ View all sources:   jq '.sources[] | {title, url}' $DELIVER_DIR/news.json"
echo "  │ Start monitoring:   scripts/test_refresh_cycle.sh $TOPIC_ID"
echo "  │ Re-run pipeline:    $0 \"$TOPIC\""
echo "  └─────────────────────────────────────────────"
echo
echo "  TOPIC_ID=$TOPIC_ID"
echo
