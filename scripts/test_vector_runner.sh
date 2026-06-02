#!/usr/bin/env bash
# scripts/test_vector_runner.sh — Full lifecycle test: plan → deliver → refresh
#
# Two output channels:
#   agent_log/      — complete SSE event stream, tool calls, timing (debug channel)
#   business_output/ — what the user sees: intro.md, report.md, news, sources
#   evaluation.json — structured metrics for cross-instance comparison
#
# Recoverable: writes state.json checkpoint after every step.
#
# Usage:
#   scripts/test_vector_runner.sh --env test1          # run on test slot 1
#   scripts/test_vector_runner.sh --env test2          # run on test slot 2
#   scripts/test_vector_runner.sh --env prod           # run on production
#   scripts/test_vector_runner.sh --env test1 --resume # resume after crash
#   scripts/test_vector_runner.sh --env test1 --force  # re-run even if passed
#
# Output: testing/results/<env>/<timestamp>/
#   state.json, runner.log, evaluation.json
#   agent_log/events_full.ndjson, events_plan.ndjson, events_deliver.ndjson, ...
#   business_output/intro.md, report.md, parsed.json, news.json, report.json, ...

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VECTORS_FILE="$REPO_ROOT/testing/vectors.json"

# ── Parse args ───────────────────────────────────────────────
TARGET_ENV=""
FORCE=false
RESUME=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --env)     TARGET_ENV="$2"; shift 2 ;;
    --force)   FORCE=true; shift ;;
    --resume)  RESUME=true; shift ;;
    -h|--help)
      echo "Usage: $0 --env test1|test2|prod [--force] [--resume]"
      exit 0
      ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done

if [ -z "$TARGET_ENV" ]; then
  echo "Error: --env is required (test1, test2, or prod)" >&2
  exit 1
fi

# ── Load environment ─────────────────────────────────────────
case "$TARGET_ENV" in
  test1) ENV_FILE="$REPO_ROOT/testing/.env.test1" ;;
  test2) ENV_FILE="$REPO_ROOT/testing/.env.test2" ;;
  prod)  ENV_FILE="$REPO_ROOT/testing/.env.testing" ;;
  *)     echo "Unknown env: $TARGET_ENV (use test1, test2, or prod)" >&2; exit 1 ;;
esac

if [ ! -f "$ENV_FILE" ]; then
  echo "Missing env file: $ENV_FILE" >&2
  exit 1
fi
# shellcheck disable=SC1090
source "$ENV_FILE"

for cmd in curl jq sed date bc; do
  command -v "$cmd" >/dev/null || { echo "missing: $cmd" >&2; exit 1; }
done

# ── Load vector ──────────────────────────────────────────────
VID="V001_hormuz"
TOPIC=$(jq -r '.vectors[0].topic' "$VECTORS_FILE")
TIMEOUT=$(jq -r '.vectors[0].timeout_sec // 900' "$VECTORS_FILE")
AUTO_PROCEED=$(jq -r '.vectors[0].auto_proceed // true' "$VECTORS_FILE")
THRESHOLDS=$(jq -c '.vectors[0].thresholds // {}' "$VECTORS_FILE")
REFRESH_CYCLES=$(jq -r '.vectors[0].refresh_cycles // 0' "$VECTORS_FILE")
REFRESH_MAX_AGE=$(jq -r '.vectors[0].refresh_max_age_hours // 48' "$VECTORS_FILE")
REFRESH_TIMEOUT=$(jq -r '.vectors[0].refresh_timeout_sec // 600' "$VECTORS_FILE")

# ── Run directory ────────────────────────────────────────────
RESULTS_BASE="$REPO_ROOT/testing/results/$TARGET_ENV"
mkdir -p "$RESULTS_BASE"

if [ "$RESUME" = "true" ]; then
  RUN_DIR=""
  for sf in "$RESULTS_BASE"/*/state.json; do
    [ -f "$sf" ] || continue
    st=$(jq -r '.status // "completed"' "$sf")
    if [ "$st" != "completed" ]; then
      RUN_DIR=$(jq -r '.run_dir' "$sf")
      break
    fi
  done
  if [ -z "$RUN_DIR" ]; then
    echo "No incomplete run found. Starting fresh."
    RESUME=false
  else
    echo "Resuming: $RUN_DIR"
    # Clear failed marker so the run can continue
    tmp="$RUN_DIR/state.json.tmp"
    jq 'del(.message, .finished_at) | .status="running"' "$RUN_DIR/state.json" > "$tmp" \
      && mv "$tmp" "$RUN_DIR/state.json"
  fi
fi

if [ "$RESUME" != "true" ]; then
  TS="$(date -u +%Y-%m-%dT%H-%M-%SZ)"
  RUN_DIR="$RESULTS_BASE/$TS"
  mkdir -p "$RUN_DIR"
fi

STATE_FILE="$RUN_DIR/state.json"
AGENT_LOG="$RUN_DIR/agent_log"
BIZ_OUT="$RUN_DIR/business_output"
EVAL_FILE="$RUN_DIR/evaluation.json"
QA_REPORT_FILE="$RUN_DIR/qa_report.json"
mkdir -p "$AGENT_LOG" "$BIZ_OUT"

# ── Logging ──────────────────────────────────────────────────
LOG_FILE="$RUN_DIR/runner.log"
log() { echo "[$(date -u +%H:%M:%S)] $*" | tee -a "$LOG_FILE"; }

# ── State helpers ────────────────────────────────────────────
init_state() {
  if [ ! -f "$STATE_FILE" ]; then
    jq -nc \
      --arg env "$TARGET_ENV" \
      --arg api "$API" \
      --arg rd "$RUN_DIR" \
      --arg topic "$TOPIC" \
      --arg vid "$VID" \
      --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
      '{status:"running", env:$env, api:$api, run_dir:$rd, topic:$topic, vector_id:$vid, started_at:$ts, step:"not_started"}' \
      > "$STATE_FILE"
  fi
}

get_step()  { jq -r '.step // "not_started"' "$STATE_FILE"; }
get_field() { jq -r ".$1 // empty" "$STATE_FILE"; }

save_step() {
  local step="$1"; shift
  local extra="${1:-"{}"}"
  local tmp="$STATE_FILE.tmp"
  jq --arg s "$step" --argjson e "$extra" '.step=$s | .updated_at=(now|todate) | . += $e' \
    "$STATE_FILE" > "$tmp" && mv "$tmp" "$STATE_FILE"
}

save_result() {
  local status="$1" msg="$2"
  local tmp="$STATE_FILE.tmp"
  jq --arg s "$status" --arg m "$msg" \
    '.status=$s | .message=$m | .finished_at=(now|todate)' \
    "$STATE_FILE" > "$tmp" && mv "$tmp" "$STATE_FILE"
}

# ── SSE helpers ──────────────────────────────────────────────
start_sse_tail() {
  local topic_id="$1" events_file="$2"
  curl -N -sS "$API/v1/topics/$topic_id/events" \
    -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
    2>/dev/null \
    | sed -n 's/^data: //p' \
    >> "$events_file" &
  echo $!
}

wait_for_event() {
  local event_name="$1" timeout="$2" events_file="$3"
  local waited=0
  while ! grep -q "\"event_type\":\"$event_name\"" "$events_file" 2>/dev/null; do
    if grep -qE '"event_type":"error"' "$events_file" 2>/dev/null; then
      local err
      err=$(grep '"event_type":"error"' "$events_file" | tail -1 | jq -r '.payload.error // "unknown"' 2>/dev/null)
      log "    ✗ Error: $err"
      return 1
    fi
    sleep 3; waited=$((waited + 3))
    if [ "$waited" -gt "$timeout" ]; then
      return 2
    fi
  done
}

# Poll GET /topics — reliable when long-lived SSE drops (HTTPS idle timeout).
wait_for_topic_state() {
  local want_state="$1" timeout="$2"
  local waited=0 state
  while true; do
    state=$(curl -fsS "$API/v1/topics/$TOPIC_ID" \
      -H "X-API-Key: $CLAUDE_AGENT_API_KEY" 2>/dev/null | jq -r '.state // "unknown"')
    if [ "$state" = "$want_state" ]; then
      return 0
    fi
    if [ "$state" = "failed" ]; then
      local err
      err=$(curl -fsS "$API/v1/topics/$TOPIC_ID" \
        -H "X-API-Key: $CLAUDE_AGENT_API_KEY" 2>/dev/null | jq -r '.error // "unknown"')
      log "    ✗ Topic failed: $err"
      return 1
    fi
    sleep 3
    waited=$((waited + 3))
    if [ "$waited" -gt "$timeout" ]; then
      state=$(curl -fsS "$API/v1/topics/$TOPIC_ID" \
        -H "X-API-Key: $CLAUDE_AGENT_API_KEY" 2>/dev/null | jq -r '.state // "unknown"')
      if [ "$state" = "$want_state" ]; then
        log "    ⚠ SSE lag; server state=$state (ok)"
        return 0
      fi
      log "    ✗ Timeout after ${waited}s waiting for state=$want_state (got $state)"
      return 2
    fi
  done
}

_events_max_seq() {
  local f="$1"
  [ -s "$f" ] || { echo 0; return; }
  # Parse line-by-line and skip malformed lines (a concurrent SSE writer can leave
  # a partial line); a single bad line must not blank out the whole max-seq.
  jq -Rrs 'split("\n") | map(select(length > 0) | (fromjson? | .seq // 0)) | (max // 0)' "$f" 2>/dev/null || echo 0
}

# Backfill events via short SSE bursts (stream stays open on non-terminal states).
sync_events_from_api() {
  local topic_id="$1" outfile="$2"
  local from_seq target max_seq rounds=0
  touch "$outfile"
  from_seq=$(_events_max_seq "$outfile")
  while [ "$rounds" -lt 60 ]; do
    target=$(curl -fsS "$API/v1/topics/$topic_id" \
      -H "X-API-Key: $CLAUDE_AGENT_API_KEY" 2>/dev/null \
      | jq -r '.last_event_seq // 0')
    if [ "$from_seq" -ge "$target" ]; then
      break
    fi
    curl -N -sS --max-time 10 "$API/v1/topics/$topic_id/events?from_seq=$from_seq" \
      -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
      2>/dev/null \
      | sed -n 's/^data: //p' \
      >> "$outfile" || true
    max_seq=$(_events_max_seq "$outfile")
    if [ "$max_seq" -le "$from_seq" ]; then
      rounds=$((rounds + 1))
    else
      rounds=0
      from_seq="$max_seq"
    fi
    sleep 1
  done
}

# ── Fetch complete event log from DB ─────────────────────────
fetch_full_event_log() {
  local topic_id="$1" outfile="$2"
  log "  Syncing complete event log from API..."
  : > "$outfile"
  sync_events_from_api "$topic_id" "$outfile"
  local count
  count=$(wc -l < "$outfile" 2>/dev/null | tr -d ' ')
  log "  ✓ $count events synced"
}

# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

init_state

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  V001_hormuz — Full Pipeline + Refresh"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ENV:      $TARGET_ENV"
echo "  API:      $API"
echo "  TOPIC:    $TOPIC"
echo "  TIMEOUT:  ${TIMEOUT}s"
echo "  REFRESH:  ${REFRESH_CYCLES} cycle(s)"
echo "  RUN_DIR:  $RUN_DIR"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

# ── Health check ─────────────────────────────────────────────
log "◆ Health check → $API"
HEALTH_START=$(date +%s)
HEALTH_RESP=$(curl -fsS --max-time 10 "$API/readyz" 2>/dev/null || echo '{"status":"unreachable"}')
HEALTH_END=$(date +%s)
HEALTH_MS=$(( (HEALTH_END - HEALTH_START) * 1000 ))

if echo "$HEALTH_RESP" | jq -e '.status == "ready"' >/dev/null 2>&1; then
  CLAUDE_VER=$(echo "$HEALTH_RESP" | jq -r '.claude_version // "unknown"')
  log "  ✓ API healthy (${HEALTH_MS}ms, claude=$CLAUDE_VER)"
else
  log "  ✗ API not reachable"; exit 1
fi
log ""

STEP=$(get_step)

if [ "$STEP" = "completed" ] && [ "$FORCE" != "true" ]; then
  log "Already completed. Use --force to re-run."
  jq -r '"  status=\(.status)  \(.message // "")"' "$STATE_FILE"
  exit 0
fi

# ═══════════════════════════════════════════════════════════════
# STEP 1: CREATE TOPIC
# ═══════════════════════════════════════════════════════════════
if [ "$STEP" = "not_started" ]; then
  log "━━ STEP 1: Create topic"
  log "  $TOPIC"

  TOPIC_ID=$(curl -fsS -X POST "$API/v1/topics" \
    -H "Content-Type: application/json" \
    -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
    -d "$(jq -nc --arg t "$TOPIC" '{topic:$t}')" \
    2>/dev/null \
    | tee "$AGENT_LOG/create_response.json" \
    | jq -r .topic_id)

  if [ -z "$TOPIC_ID" ] || [ "$TOPIC_ID" = "null" ]; then
    log "  ✗ Failed to create topic"
    save_result "failed" "topic creation failed"
    exit 1
  fi

  log "  ✓ topic_id=$TOPIC_ID"
  save_step "planning" "{\"topic_id\":\"$TOPIC_ID\",\"plan_start\":$(date +%s)}"
  STEP="planning"
fi

TOPIC_ID=$(get_field "topic_id")

# ═══════════════════════════════════════════════════════════════
# STEP 2: WAIT FOR PLAN
# ═══════════════════════════════════════════════════════════════
if [ "$STEP" = "planning" ]; then
  STATE_NOW=$(curl -fsS "$API/v1/topics/$TOPIC_ID" \
    -H "X-API-Key: $CLAUDE_AGENT_API_KEY" 2>/dev/null | jq -r '.state // "unknown"')
  if [ "$STATE_NOW" = "planned_awaiting_review" ]; then
    log "  ✓ Plan already complete (recovered)"
    save_step "planned" '{}'
    STEP="planned"
  elif [ "$STATE_NOW" = "failed" ]; then
    ERR=$(curl -fsS "$API/v1/topics/$TOPIC_ID" \
      -H "X-API-Key: $CLAUDE_AGENT_API_KEY" 2>/dev/null | jq -r '.error // "unknown"')
    log "  ✗ Topic failed on server: $ERR"
    save_result "failed" "server: $ERR"
    exit 1
  elif [ "$STATE_NOW" = "reported" ]; then
    log "  ✓ Already reported (recovered)"
    save_step "reported" '{}'
    STEP="reported"
  fi
fi

if [ "$STEP" = "planning" ]; then
  log "━━ STEP 2: Waiting for plan (topic=$TOPIC_ID)..."

  EVENTS_FILE="$AGENT_LOG/events_plan.ndjson"
  touch "$EVENTS_FILE"
  TAIL_PID=$(start_sse_tail "$TOPIC_ID" "$EVENTS_FILE")

  (tail -f "$EVENTS_FILE" 2>/dev/null | jq -rc --unbuffered '
    if   .event_type=="tool_use"       then "      🔧 \(.payload.tool // "?")"
    elif .event_type=="tool_result" and .payload.is_error then "      ⚠ tool error"
    elif .event_type=="stage.finished" then "      ✓ \(.payload.stage) (\(.payload.duration_ms)ms $\(.payload.total_cost_usd))"
    elif .event_type=="intro.ready"    then "      ★ INTRO: \((.payload.headline // "")[0:80])"
    elif .event_type=="needs_input"    then "      ⏸ GATE: plan ready"
    else empty end
  ' 2>/dev/null | while IFS= read -r line; do log "$line"; done) &
  PROGRESS_PID=$!

  PLAN_OK=false
  if wait_for_topic_state "planned_awaiting_review" "$TIMEOUT"; then
    PLAN_OK=true
  elif [ "$(curl -fsS "$API/v1/topics/$TOPIC_ID" -H "X-API-Key: $CLAUDE_AGENT_API_KEY" 2>/dev/null \
      | jq -r '.state')" = "planned_awaiting_review" ]; then
    PLAN_OK=true
  fi

  kill "$TAIL_PID" "$PROGRESS_PID" 2>/dev/null; wait "$TAIL_PID" "$PROGRESS_PID" 2>/dev/null
  sync_events_from_api "$TOPIC_ID" "$EVENTS_FILE"

  if [ "$PLAN_OK" = "true" ]; then
    PLAN_END=$(date +%s)
    PLAN_START=$(get_field "plan_start")
    PLAN_DUR=$((PLAN_END - PLAN_START))
    log "  ✓ Plan complete (${PLAN_DUR}s, events=$(_events_max_seq "$EVENTS_FILE"))"

    # Save business output
    curl -fsS "$API/v1/topics/$TOPIC_ID/parsed" -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
      | jq . > "$BIZ_OUT/parsed.json" 2>/dev/null || true
    curl -fsS "$API/v1/topics/$TOPIC_ID/intro.md" -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
      > "$BIZ_OUT/intro.md" 2>/dev/null || true
    curl -fsS "$API/v1/topics/$TOPIC_ID/intro" -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
      | jq . > "$BIZ_OUT/intro.json" 2>/dev/null || true

    save_step "planned" "{\"plan_duration_sec\":$PLAN_DUR}"
    STEP="planned"
  else
    local diag ev_lines
    diag=$(curl -fsS "$API/v1/topics/$TOPIC_ID" -H "X-API-Key: $CLAUDE_AGENT_API_KEY" 2>/dev/null \
      | jq -c '{state, error, last_event_seq}' 2>/dev/null || echo "(unreachable)")
    log "    ✗ Topic state: $diag"
    ev_lines=$(wc -l < "$EVENTS_FILE" 2>/dev/null | tr -d ' ')
    log "    ✗ Events captured: ${ev_lines} lines"
    save_result "failed" "plan did not complete"
    exit 1
  fi
fi

# ═══════════════════════════════════════════════════════════════
# STEP 3: PROCEED → DELIVER
# ═══════════════════════════════════════════════════════════════
if [ "$STEP" = "planned" ]; then
  if [ "$AUTO_PROCEED" != "true" ]; then
    log "  ⏸ Manual mode. Approve via API then --resume."
    save_step "awaiting_proceed" '{}'
    exit 0
  fi

  log "━━ STEP 3: Proceeding to deliver..."
  curl -fsS -X POST "$API/v1/topics/$TOPIC_ID/proceed" \
    -H "X-API-Key: $CLAUDE_AGENT_API_KEY" >/dev/null 2>&1

  save_step "delivering" "{\"deliver_start\":$(date +%s)}"
  STEP="delivering"
fi

if [ "$STEP" = "awaiting_proceed" ]; then
  STATE_NOW=$(curl -fsS "$API/v1/topics/$TOPIC_ID" \
    -H "X-API-Key: $CLAUDE_AGENT_API_KEY" 2>/dev/null | jq -r '.state // "unknown"')
  if [ "$STATE_NOW" = "delivering" ] || [ "$STATE_NOW" = "reported" ]; then
    save_step "delivering" "{\"deliver_start\":$(date +%s)}"
    STEP="delivering"
  else
    log "  ⏸ Still awaiting proceed (state=$STATE_NOW)."
    exit 0
  fi
fi

# ═══════════════════════════════════════════════════════════════
# STEP 4: WAIT FOR DELIVERY
# ═══════════════════════════════════════════════════════════════
if [ "$STEP" = "delivering" ]; then
  STATE_NOW=$(curl -fsS "$API/v1/topics/$TOPIC_ID" \
    -H "X-API-Key: $CLAUDE_AGENT_API_KEY" 2>/dev/null | jq -r '.state // "unknown"')

  if [ "$STATE_NOW" = "reported" ]; then
    log "  ✓ Already reported (recovered)"
    save_step "reported" '{}'
    STEP="reported"
  else
    log "━━ STEP 4: Waiting for delivery (topic=$TOPIC_ID)..."

    EVENTS_FILE="$AGENT_LOG/events_deliver.ndjson"
    touch "$EVENTS_FILE"
    TAIL_PID=$(start_sse_tail "$TOPIC_ID" "$EVENTS_FILE")

    (tail -f "$EVENTS_FILE" 2>/dev/null | jq -rc --unbuffered '
      if   .event_type=="tool_use"       then "      🔧 \(.payload.tool // "?"): \((.payload.input_preview // "")[0:60])"
      elif .event_type=="tool_result" and .payload.is_error then "      ⚠ tool error: \((.payload.output_preview // "")[0:60])"
      elif .event_type=="stage.finished" then "      ✓ \(.payload.stage) (\(.payload.duration_ms)ms $\(.payload.total_cost_usd))"
      elif .event_type=="report.ready"   then "      ★ REPORT READY"
      else empty end
    ' 2>/dev/null | while IFS= read -r line; do log "$line"; done) &
    PROGRESS_PID=$!

    DELIVER_OK=false
    if wait_for_topic_state "reported" "$TIMEOUT"; then
      DELIVER_OK=true
    elif [ "$(curl -fsS "$API/v1/topics/$TOPIC_ID" -H "X-API-Key: $CLAUDE_AGENT_API_KEY" 2>/dev/null \
        | jq -r '.state')" = "reported" ]; then
      DELIVER_OK=true
    fi

    kill "$TAIL_PID" "$PROGRESS_PID" 2>/dev/null; wait "$TAIL_PID" "$PROGRESS_PID" 2>/dev/null
    sync_events_from_api "$TOPIC_ID" "$EVENTS_FILE"

    if [ "$DELIVER_OK" = "true" ]; then
      DELIVER_END=$(date +%s)
      DELIVER_START=$(get_field "deliver_start")
      DELIVER_DUR=$((DELIVER_END - DELIVER_START))
      log "  ✓ Delivery complete (${DELIVER_DUR}s, events=$(_events_max_seq "$EVENTS_FILE"))"

      # Save business output
      curl -fsS "$API/v1/topics/$TOPIC_ID/news" -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
        | jq . > "$BIZ_OUT/news.json" 2>/dev/null || true
      curl -fsS "$API/v1/topics/$TOPIC_ID/report" -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
        | jq . > "$BIZ_OUT/report.json" 2>/dev/null || true
      curl -fsS "$API/v1/topics/$TOPIC_ID/report.md" -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
        > "$BIZ_OUT/report.md" 2>/dev/null || true

      save_step "reported" "{\"deliver_duration_sec\":$DELIVER_DUR}"
      STEP="reported"
    else
      local diag ev_lines
      diag=$(curl -fsS "$API/v1/topics/$TOPIC_ID" -H "X-API-Key: $CLAUDE_AGENT_API_KEY" 2>/dev/null \
        | jq -c '{state, error, last_event_seq}' 2>/dev/null || echo "(unreachable)")
      log "    ✗ Topic state: $diag"
      ev_lines=$(wc -l < "$EVENTS_FILE" 2>/dev/null | tr -d ' ')
      log "    ✗ Events captured: ${ev_lines} lines"
      save_result "failed" "deliver did not complete"
      exit 1
    fi
  fi
fi

# ═══════════════════════════════════════════════════════════════
# STEP 5: REFRESH CYCLE (optional)
# ═══════════════════════════════════════════════════════════════
if [ "$STEP" = "reported" ] && [ "$REFRESH_CYCLES" -gt 0 ]; then
  log "━━ STEP 5: Refresh (${REFRESH_CYCLES} cycle)..."

  # Start monitoring
  MON_CODE=$(curl -sS -o "$AGENT_LOG/monitor_response.json" -w "%{http_code}" \
    -X POST "$API/v1/topics/$TOPIC_ID/monitor" \
    -H "Content-Type: application/json" \
    -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
    -d "{\"max_age_hours\": $REFRESH_MAX_AGE}" 2>/dev/null)

  if [ "$MON_CODE" -ge 400 ]; then
    MON_STATUS=$(curl -sS "$API/v1/topics/$TOPIC_ID/monitor" \
      -H "X-API-Key: $CLAUDE_AGENT_API_KEY" 2>/dev/null | jq -r '.status // "none"')
    if [ "$MON_STATUS" != "active" ]; then
      log "  ⚠ Monitor failed (HTTP $MON_CODE), skipping refresh"
      save_step "collecting" '{}'
      STEP="collecting"
    else
      log "  ✓ Monitoring already active"
    fi
  else
    QCOUNT=$(jq -r '.queries_count // 0' "$AGENT_LOG/monitor_response.json" 2>/dev/null)
    log "  ✓ Monitoring started ($QCOUNT queries)"
  fi

  if [ "$STEP" = "reported" ]; then
    for CYCLE in $(seq 1 "$REFRESH_CYCLES"); do
      REFRESH_START=$(date +%s)
      log "  Triggering refresh cycle $CYCLE..."

      REFRESH_RESP=$(curl -fsS -X POST "$API/v1/topics/$TOPIC_ID/refresh" \
        -H "X-API-Key: $CLAUDE_AGENT_API_KEY" 2>/dev/null)
      QUEUED=$(echo "$REFRESH_RESP" | jq -r '.queued')

      if [ "$QUEUED" != "true" ]; then
        log "  ⚠ Refresh not queued, skipping"
        continue
      fi

      RF_EVENTS="$AGENT_LOG/events_refresh_${CYCLE}.ndjson"
      : > "$RF_EVENTS"
      TAIL_PID=$(start_sse_tail "$TOPIC_ID" "$RF_EVENTS")

      (tail -f "$RF_EVENTS" 2>/dev/null | jq -rc --unbuffered '
        if   .event_type=="refresh.started"   then "      ▶ Refresh started"
        elif .event_type=="tool_use"          then "      🔧 \(.payload.tool // "?")"
        elif .event_type=="refresh.completed" then "      ✓ Done (new=\(.payload.new_sources_count), $\(.payload.total_cost_usd))"
        elif .event_type=="refresh.failed"    then "      ✗ FAILED: \(.payload.error // "?")"
        else empty end
      ' 2>/dev/null | while IFS= read -r line; do log "$line"; done) &
      PROGRESS_PID=$!

      RF_WAITED=0
      RF_DONE=false
      while [ "$RF_WAITED" -lt "$REFRESH_TIMEOUT" ]; do
        if grep -q '"refresh.completed"' "$RF_EVENTS" 2>/dev/null; then
          RF_DONE=true; break
        fi
        if grep -q '"refresh.failed"' "$RF_EVENTS" 2>/dev/null; then
          break
        fi
        sleep 3; RF_WAITED=$((RF_WAITED + 3))
      done

      kill "$TAIL_PID" "$PROGRESS_PID" 2>/dev/null; wait "$TAIL_PID" "$PROGRESS_PID" 2>/dev/null

      REFRESH_END=$(date +%s)
      REFRESH_DUR=$((REFRESH_END - REFRESH_START))

      if [ "$RF_DONE" = "true" ]; then
        log "  ✓ Refresh cycle $CYCLE complete (${REFRESH_DUR}s)"
        # Save refresh business output
        curl -fsS "$API/v1/topics/$TOPIC_ID/deltas?limit=1" \
          -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
          | jq . > "$BIZ_OUT/refresh_deltas.json" 2>/dev/null || true

        LATEST_SEQ=$(jq -r '.deltas[0].seq // empty' "$BIZ_OUT/refresh_deltas.json" 2>/dev/null)
        if [ -n "$LATEST_SEQ" ] && [ "$LATEST_SEQ" != "null" ]; then
          curl -fsS "$API/v1/topics/$TOPIC_ID/deltas/$LATEST_SEQ" \
            -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
            | jq . > "$BIZ_OUT/refresh_delta.json" 2>/dev/null || true
          curl -fsS "$API/v1/topics/$TOPIC_ID/deltas/$LATEST_SEQ/news" \
            -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
            | jq . > "$BIZ_OUT/refresh_news.json" 2>/dev/null || true
          curl -fsS "$API/v1/topics/$TOPIC_ID/deltas/$LATEST_SEQ/report" \
            -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
            > "$BIZ_OUT/refresh_report.md" 2>/dev/null || true
        fi
      else
        log "  ✗ Refresh cycle $CYCLE did not complete"
      fi
    done

    save_step "collecting" "{\"refresh_done\":true,\"refresh_duration_sec\":$REFRESH_DUR}"
    STEP="collecting"
  fi
elif [ "$STEP" = "reported" ]; then
  save_step "collecting" '{"refresh_done":false}'
  STEP="collecting"
fi

# ═══════════════════════════════════════════════════════════════
# STEP 6: COLLECT FULL EVENT LOG + BUILD EVALUATION
# ═══════════════════════════════════════════════════════════════
if [ "$STEP" = "collecting" ]; then
  log "━━ STEP 6: Building evaluation..."

  # Fetch complete event log from DB (authoritative, not dependent on SSE tail)
  fetch_full_event_log "$TOPIC_ID" "$AGENT_LOG/events_full.ndjson"

  # Fetch topic state
  curl -fsS "$API/v1/topics/$TOPIC_ID" \
    -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
    | jq . > "$AGENT_LOG/topic_final.json" 2>/dev/null || true

  # Fetch business output if not already present (recovery case)
  [ -s "$BIZ_OUT/parsed.json" ] || curl -fsS "$API/v1/topics/$TOPIC_ID/parsed" \
    -H "X-API-Key: $CLAUDE_AGENT_API_KEY" | jq . > "$BIZ_OUT/parsed.json" 2>/dev/null || true
  [ -s "$BIZ_OUT/news.json" ] || curl -fsS "$API/v1/topics/$TOPIC_ID/news" \
    -H "X-API-Key: $CLAUDE_AGENT_API_KEY" | jq . > "$BIZ_OUT/news.json" 2>/dev/null || true
  [ -s "$BIZ_OUT/report.json" ] || curl -fsS "$API/v1/topics/$TOPIC_ID/report" \
    -H "X-API-Key: $CLAUDE_AGENT_API_KEY" | jq . > "$BIZ_OUT/report.json" 2>/dev/null || true
  [ -s "$BIZ_OUT/report.md" ] || curl -fsS "$API/v1/topics/$TOPIC_ID/report.md" \
    -H "X-API-Key: $CLAUDE_AGENT_API_KEY" > "$BIZ_OUT/report.md" 2>/dev/null || true
  [ -s "$BIZ_OUT/intro.md" ] || curl -fsS "$API/v1/topics/$TOPIC_ID/intro.md" \
    -H "X-API-Key: $CLAUDE_AGENT_API_KEY" > "$BIZ_OUT/intro.md" 2>/dev/null || true

  # ── Build evaluation.json from artifacts ────────────────────
  EVENTS_FULL="$AGENT_LOG/events_full.ndjson"

  # Extract metrics from events
  EVENTS_METRICS=$(jq -rsc '
    {
      total_events: length,
      tool_calls: [.[] | select(.event_type=="tool_use")] | length,
      tool_errors: [.[] | select(.event_type=="tool_result" and .payload.is_error==true)] | length,
      tool_names: ([.[] | select(.event_type=="tool_use") | .payload.tool] | group_by(.) | map({key: .[0], value: length}) | from_entries),
      stages: [.[] | select(.event_type=="stage.finished") | {stage: .payload.stage, duration_ms: .payload.duration_ms, cost_usd: .payload.total_cost_usd}],
      plan_cost_usd: ([.[] | select(.event_type=="stage.finished" and .payload.stage=="plan") | .payload.total_cost_usd // 0] | add // 0),
      deliver_cost_usd: ([.[] | select(.event_type=="stage.finished" and .payload.stage=="deliver") | .payload.total_cost_usd // 0] | add // 0),
      refresh_cost_usd: ([.[] | select(.event_type=="refresh.completed") | .payload.total_cost_usd // 0] | add // 0),
      refresh_new_sources: ([.[] | select(.event_type=="refresh.completed") | .payload.new_sources_count // 0] | add // 0)
    }
  ' "$EVENTS_FULL" 2>/dev/null || echo '{}')

  # Extract plan metrics
  PLAN_METRICS='{}'
  if [ -s "$BIZ_OUT/parsed.json" ]; then
    PLAN_METRICS=$(jq -c '{
      queries_count: (.queries // [] | length),
      languages: (.queries // [] | map(.language) | unique),
      language_count: (.queries // [] | map(.language) | unique | length),
      rag_refs_count: (.rag_context_refs // [] | length),
      working_thesis: (.working_thesis // "n/a" | .[0:200]),
      topic_restated: (.topic_restated // "n/a"),
      entities_actors: (.entities.actors // [] | map(.name // .)),
      scenarios_count: (.scenarios // [] | length),
      monitoring_triggers: (.monitoring_plan.trigger_terms // [])
    }' "$BIZ_OUT/parsed.json" 2>/dev/null || echo '{}')
  fi

  # Extract deliver metrics
  DELIVER_METRICS='{}'
  if [ -s "$BIZ_OUT/news.json" ] && [ -s "$BIZ_OUT/report.json" ]; then
    NEWS_METRICS=$(jq -c '{
      sources_total: (.sources // [] | length),
      sources_with_date: ([.sources // [] | .[] | select(.published_at != null)] | length),
      sources_newest_date: ([.sources // [] | .[] | select(.published_at != null) | .published_at] | sort | reverse | .[0] // "n/a"),
      sources_oldest_date: ([.sources // [] | .[] | select(.published_at != null) | .published_at] | sort | .[0] // "n/a"),
      sources_unique_publishers: ([.sources // [] | .[] | .publisher // "unknown"] | unique | length),
      sources_avg_relevance: (([.sources // [] | .[] | .relevance_score // 0] | add // 0) / ((.sources // [] | length) | if . == 0 then 1 else . end) | . * 100 | floor / 100),
      source_classes: ([.sources // [] | .[] | .source_class // "unknown"] | group_by(.) | map({key: .[0], value: length}) | from_entries),
      queries_executed: (.executed_queries // [] | length),
      queries_with_results: ([.executed_queries // [] | .[] | select((.results_count // 0) > 0)] | length),
      drops: (.drops // {})
    }' "$BIZ_OUT/news.json" 2>/dev/null || echo '{}')

    REPORT_METRICS=$(jq -c '{
      key_findings_count: (.key_findings // [] | length),
      scenarios_count: (.scenario_updates // .scenarios // [] | length),
      thesis_status: (.thesis_status // "n/a"),
      thesis_update: (.thesis_update_md // "n/a" | .[0:300]),
      open_questions_count: (.open_questions // [] | length),
      next_queries_count: (.next_queries // [] | length),
      summary_md: (.summary_md // "n/a" | .[0:500])
    }' "$BIZ_OUT/report.json" 2>/dev/null || echo '{}')

    REPORT_MD_STATS='{}'
    if [ -s "$BIZ_OUT/report.md" ]; then
      RL=$(wc -l < "$BIZ_OUT/report.md" | tr -d ' ')
      RW=$(wc -w < "$BIZ_OUT/report.md" | tr -d ' ')
      RC=$(grep -oE '\[s[0-9]+\]' "$BIZ_OUT/report.md" 2>/dev/null | sort -u | wc -l | tr -d ' ')
      REPORT_MD_STATS=$(jq -nc --argjson l "$RL" --argjson w "$RW" --argjson c "$RC" \
        '{report_lines: $l, report_words: $w, unique_citations: $c}')
    fi

    DELIVER_METRICS=$(echo "$NEWS_METRICS $REPORT_METRICS $REPORT_MD_STATS" \
      | jq -sc '.[0] * .[1] * .[2]' 2>/dev/null || echo '{}')
  fi

  # Extract refresh metrics
  REFRESH_METRICS='{"enabled":false}'
  if [ -s "$BIZ_OUT/refresh_deltas.json" ]; then
    REFRESH_METRICS=$(jq -c '{
      enabled: true,
      new_sources_count: (.deltas[0].new_sources_count // 0),
      queries_executed: (.deltas[0].queries_executed // 0),
      duration_ms: (.deltas[0].duration_ms // 0),
      cost_usd: (.deltas[0].total_cost_usd // 0),
      status: (.deltas[0].status // "n/a")
    }' "$BIZ_OUT/refresh_deltas.json" 2>/dev/null || echo '{"enabled":false}')
  fi

  # Timing
  PLAN_DUR=$(get_field "plan_duration_sec")
  DELIVER_DUR=$(get_field "deliver_duration_sec")
  REFRESH_DUR=$(get_field "refresh_duration_sec")
  PLAN_DUR="${PLAN_DUR:-0}"
  DELIVER_DUR="${DELIVER_DUR:-0}"
  REFRESH_DUR="${REFRESH_DUR:-0}"
  TOTAL_DUR=$((PLAN_DUR + DELIVER_DUR + REFRESH_DUR))

  # Assemble evaluation.json
  jq -nc \
    --arg vid "$VID" \
    --arg env "$TARGET_ENV" \
    --arg api "$API" \
    --arg topic "$TOPIC" \
    --arg topic_id "$TOPIC_ID" \
    --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    --arg claude_ver "$CLAUDE_VER" \
    --argjson plan_dur "$PLAN_DUR" \
    --argjson deliver_dur "$DELIVER_DUR" \
    --argjson refresh_dur "$REFRESH_DUR" \
    --argjson total_dur "$TOTAL_DUR" \
    --argjson events "$EVENTS_METRICS" \
    --argjson plan "$PLAN_METRICS" \
    --argjson deliver "$DELIVER_METRICS" \
    --argjson refresh "$REFRESH_METRICS" \
    '{
      vector_id: $vid,
      env: $env,
      api: $api,
      topic: $topic,
      topic_id: $topic_id,
      timestamp: $ts,
      claude_version: $claude_ver,
      timing: {plan_sec: $plan_dur, deliver_sec: $deliver_dur, refresh_sec: $refresh_dur, total_sec: $total_dur},
      cost: {plan_usd: $events.plan_cost_usd, deliver_usd: $events.deliver_cost_usd, refresh_usd: $events.refresh_cost_usd, total_usd: (($events.plan_cost_usd // 0) + ($events.deliver_cost_usd // 0) + ($events.refresh_cost_usd // 0))},
      events: $events,
      plan: $plan,
      deliver: $deliver,
      refresh: $refresh
    }' > "$EVAL_FILE"

  log "  ✓ evaluation.json written"

  # Thin mechanical verification gate (ticket #17, full rules in #15).
  log "  Running QA gate..."
  if bash "$REPO_ROOT/scripts/qa_check_run.sh" --run-dir "$RUN_DIR" --out "$QA_REPORT_FILE"; then
    log "  ✓ QA PASS ($QA_REPORT_FILE)"
  else
    log "  ✗ QA FAIL ($QA_REPORT_FILE)"
    save_result "failed" "qa gate failed"
    exit 1
  fi

  # Update symlink for latest
  ln -sf "$RUN_DIR" "$RESULTS_BASE/latest"

  save_step "completed" '{}'
  save_result "completed" "evaluation ready"
  STEP="completed"
fi

# ═══════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ═══════════════════════════════════════════════════════════════
echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "  DONE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

if [ -s "$EVAL_FILE" ]; then
  jq -r '
    "  Timing:   plan=\(.timing.plan_sec)s deliver=\(.timing.deliver_sec)s total=\(.timing.total_sec)s",
    "  Cost:     plan=$\(.cost.plan_usd) deliver=$\(.cost.deliver_usd) total=$\(.cost.total_usd)",
    "  Sources:  \(.deliver.sources_total // "?") (\(.deliver.sources_unique_publishers // "?") publishers)",
    "  Findings: \(.deliver.key_findings_count // "?")  Thesis: \(.deliver.thesis_status // "?")",
    "  Report:   \(.deliver.report_lines // "?") lines, \(.deliver.report_words // "?") words, \(.deliver.unique_citations // "?") citations",
    "  Events:   \(.events.total_events // "?") total, \(.events.tool_calls // "?") tool calls, \(.events.tool_errors // "?") errors"
  ' "$EVAL_FILE" 2>/dev/null
fi

if [ -s "$QA_REPORT_FILE" ]; then
  jq -r '
    "  QA:       \(.passed | if . then "PASS" else "FAIL" end) (\(.summary.checks_total) checks)"
  ' "$QA_REPORT_FILE" 2>/dev/null
fi

echo
echo "  Output:"
echo "    evaluation.json     $EVAL_FILE"
echo "    qa_report.json      $QA_REPORT_FILE"
echo "    agent_log/          $AGENT_LOG/"
echo "    business_output/    $BIZ_OUT/"
echo "    runner.log          $LOG_FILE"
echo
echo "  Compare:  scripts/compare_evaluations.sh $EVAL_FILE <other_eval.json>"
echo "  Resume:   $0 --env $TARGET_ENV --resume"
echo
