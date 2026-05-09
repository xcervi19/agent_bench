#!/usr/bin/env bash
# scripts/test_newsfind.sh
#
# Run /newsfind-queries against the deployed API, stream live progress,
# and persist a reproducible debug capture under testing/runs/.
#
# Usage:
#   scripts/test_newsfind.sh "<topic>"
#   scripts/test_newsfind.sh "<topic>" --force-refresh
#   scripts/test_newsfind.sh "<topic>" --timeout 1200
#   scripts/test_newsfind.sh                       # uses default Hormuz topic
#
# Required env vars:
#   API                    e.g. http://79.143.179.212:8002
#   CLAUDE_AGENT_API_KEY   API key for X-API-Key header

set -euo pipefail

DEFAULT_TOPIC="Hormuz strait closure options to lower price"
TIMEOUT_SEC=900
FORCE_REFRESH=false

TOPIC="${1:-$DEFAULT_TOPIC}"
shift || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --force-refresh) FORCE_REFRESH=true; shift ;;
    --timeout)       TIMEOUT_SEC="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done

for cmd in curl jq sed tee date tr; do
  command -v "$cmd" >/dev/null || { echo "missing dependency: $cmd" >&2; exit 1; }
done
: "${API:?env var API is not set, e.g. export API=http://79.143.179.212:8002}"
: "${CLAUDE_AGENT_API_KEY:?env var CLAUDE_AGENT_API_KEY is not set}"

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TS="$(date -u +%Y-%m-%dT%H-%MZ)"
SLUG="$(echo "$TOPIC" \
        | tr 'A-Z' 'a-z' \
        | tr -cs 'a-z0-9' '-' \
        | sed 's/^-//;s/-$//' \
        | cut -c1-50)"
RUN_DIR="$REPO_ROOT/testing/runs/${TS}__newsfind-queries__${SLUG}"
mkdir -p "$RUN_DIR"

echo "API:           $API"
echo "TOPIC:         $TOPIC"
echo "TIMEOUT_SEC:   $TIMEOUT_SEC"
echo "FORCE_REFRESH: $FORCE_REFRESH"
echo "RUN_DIR:       $RUN_DIR"
echo "---"

if ! curl -fsS "$API/readyz" >/dev/null; then
  echo "readyz failed — API not reachable at $API" >&2
  exit 1
fi

BODY="$(jq -nc \
  --arg cmd "/newsfind-queries" \
  --arg args "$TOPIC" \
  --argjson timeout "$TIMEOUT_SEC" \
  --argjson force "$FORCE_REFRESH" \
  '{command:$cmd, args:$args, timeout_sec:$timeout, force_refresh:$force}')"

echo "$BODY" | jq . > "$RUN_DIR/request.json"

STREAM="$RUN_DIR/stream.ndjson"
echo ">>> streaming (tee -> $STREAM)"
echo

CURL_RC=0
{ curl -N -sS -X POST "$API/v1/agent/stream" \
    -H "Content-Type: application/json" \
    -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
    -d "$BODY"; \
  echo "__CURL_RC__=$?"; } \
  | sed -n 's/^data: //p' \
  | tee "$STREAM" \
  | jq -rc --unbuffered '
      if .type=="run_started"          then "START run_id=\(.run_id) topic_id=\(.topic_id)"
      elif .type=="cache_hit"          then "CACHE parsed=\(.parsed_path)"
      elif .type=="assistant" and .message.content then
        .message.content[]
        | select(.type=="tool_use")
        | "TOOL \(.name): \((.input | tostring)[0:140])"
      elif .type=="user" and (.message.content[0].type//"") == "tool_result" then
        "  <- tool returned"
      elif .type=="result"             then "RESULT \(.duration_ms)ms cost=$\(.total_cost_usd // 0) cached=\(.cached // false)"
      elif .type=="artifact_finalized" then "SAVED status=\(.status) parsed=\(.parsed_path)"
      elif .type=="end"                then "END exit_code=\(.exit_code)"
      elif .type=="error"              then "ERROR [\(.stage // "?")] \(.error_type // "?"): \(.error)"
      else empty end' || true

echo
echo ">>> stream finished"

# Recover curl's exit code (sentinel was inserted before sed stripped 'data:' prefixes,
# so it survives in the pipe even though it's not in stream.ndjson).
# Do nothing here; the sentinel was filtered out by sed, so we can't read it back.
# Instead, rely on stream.ndjson contents to decide success/failure below.

# 1) Hard fail if stream is empty (network/proxy died before any byte arrived).
if [ ! -s "$STREAM" ]; then
  echo
  echo "================ STREAM EMPTY ================"
  echo "No SSE bytes received from $API/v1/agent/stream."
  echo "Likely: curl: (18), reverse proxy buffering, or server-side crash"
  echo "BEFORE the orchestrator could yield. Check VPS logs:"
  echo "  ssh root@<vps> 'cd ~/agent_bench && docker compose logs --tail=200 claude_agent'"
  echo "=============================================="
  exit 1
fi

# 2) Hard fail (with full context) if any error event is in the stream.
if jq -e 'select(.type=="error")' "$STREAM" >/dev/null 2>&1; then
  echo
  echo "================ ERROR ================"
  jq 'select(.type=="error")' "$STREAM"
  echo "======================================="
  echo
  echo "Stream saved at: $STREAM"
  exit 1
fi

# 3) Hard fail if exit_code in the end event is non-zero.
END_CODE=$(jq -r 'select(.type=="end") | .exit_code' "$STREAM" | tail -1)
if [ -n "$END_CODE" ] && [ "$END_CODE" != "0" ]; then
  echo
  echo "================ END exit_code=$END_CODE ================"
  echo "Stream ended with non-zero exit code but no error event was emitted."
  echo "Stream saved at: $STREAM"
  exit 1
fi

# 4) Hard fail if no result event appeared.
if ! jq -e 'select(.type=="result")' "$STREAM" >/dev/null; then
  echo "no result event in stream — see $STREAM" >&2
  exit 1
fi

jq -r 'select(.type=="result") | .result' "$STREAM" \
  | tail -1 \
  | jq . > "$RUN_DIR/parsed.json"

jq '{
  schema_version,
  topic_id,
  domain,
  topic,
  actors:        .entities.actors,
  regions:       .entities.regions,
  rag_refs:      (.rag_context_refs // [] | length),
  web_refs:      (.web_seed_refs    // [] | length),
  queries_count: (.queries          // [] | length),
  languages:     (.queries // [] | map(.language) | unique),
  priorities:    (.queries // [] | group_by(.priority)
                                | map({priority: .[0].priority, count: length})),
  current_state,
  working_thesis
}' "$RUN_DIR/parsed.json" > "$RUN_DIR/summary.json"

jq -r '
  .queries[]?
  | "\(.id) [p\(.priority)] [\(.language)] [\(.intent)] \(.text // .q)\n  why: \(.rationale)\n"
' "$RUN_DIR/parsed.json" > "$RUN_DIR/queries.txt"

echo
echo "================ DECISION SUMMARY ================"
jq . "$RUN_DIR/summary.json"
echo "=================================================="
echo
echo "Artifacts:"
echo "  $RUN_DIR/request.json"
echo "  $RUN_DIR/stream.ndjson"
echo "  $RUN_DIR/parsed.json    <- consume from upper logic"
echo "  $RUN_DIR/summary.json"
echo "  $RUN_DIR/queries.txt"
