# Testing /newsfind-queries from local Mac via the API

The goal: call the deployed API from your laptop and get either a clean blueprint JSON or a clear error.

---

## Setup

```bash
export CLAUDE_AGENT_API_KEY="<your key>"
export API="http://79.143.179.212:8002"

TS=$(date -u +%Y-%m-%dT%H-%MZ)
TOPIC="Hormuz strait closure options to lower price"
SLUG=$(echo "$TOPIC" | tr 'A-Z' 'a-z' | tr -cs 'a-z0-9' '-' | sed 's/^-//;s/-$//' | cut -c1-50)
RUN_DIR=~/Documents/projects/agent_bench/testing/runs/${TS}__newsfind-queries__${SLUG}
mkdir -p "$RUN_DIR"
echo "$RUN_DIR"
```

---

## 1. Pre-flight — service alive and command registered

```bash
curl -s "$API/readyz"
# expect: {"status":"ready","claude_version":"..."}

curl -s "$API/v1/agent/info" -H "X-API-Key: $CLAUDE_AGENT_API_KEY" | jq '.allowed_commands'
# expect: array including "/newsfind-queries"
```

curl -N -X POST "$API/v1/agent/stream" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -d "{\"command\":\"/newsfind-queries\",\"args\":\"$TOPIC\",\"timeout_sec\":900}" \
  | sed -n 's/^data: //p' \
  | tee "$RUN_DIR/stream.ndjson" \
  | jq -rc --unbuffered '
      if .type=="run_started" then "START run_id=\(.run_id) topic_id=\(.topic_id)"
      elif .type=="cache_hit" then "CACHE parsed=\(.parsed_path)"
      elif .type=="assistant" and .message.content then
        .message.content[] | select(.type=="tool_use") | "TOOL \(.name)"
      elif .type=="result" then "RESULT \(.duration_ms)ms cost=$\(.total_cost_usd // 0) cached=\(.cached // false)"
      elif .type=="artifact_finalized" then "SAVED status=\(.status) parsed=\(.parsed_path)"
      elif .type=="end" then "END exit_code=\(.exit_code)"
      else empty end'

jq -r 'select(.type=="result") | .result' "$RUN_DIR/stream.ndjson" \
  | tail -1 | jq . > "$RUN_DIR/parsed.json"

jq '{schema_version,topic_id,domain,topic,
     rag_refs:(.rag_context_refs|length),web_refs:(.web_seed_refs|length),
     queries_count:(.queries|length),
     languages:(.queries|map(.language)|unique),
     priorities:(.queries|group_by(.priority)|map({p:.[0].priority,n:length}))}' \
   "$RUN_DIR/parsed.json" > "$RUN_DIR/summary.json"

jq -r '.queries[] | "\(.id) [p\(.priority)] [\(.language)] [\(.intent)] \(.text // .q)\n  why: \(.rationale)\n"' \
   "$RUN_DIR/parsed.json" > "$RUN_DIR/queries.txt"
