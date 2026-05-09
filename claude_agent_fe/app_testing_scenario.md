# Testing /newsfind-queries from local Mac via the API

The goal: call the deployed API from your laptop and get either a clean blueprint JSON or a clear error.

---

## Setup

```bash
export CLAUDE_AGENT_API_KEY="<your key>"
export API="http://79.143.179.212:8002"
```

---

## 1. Pre-flight — service alive and command registered

```bash
curl -s "$API/readyz"
# expect: {"status":"ready","claude_version":"..."}

curl -s "$API/v1/agent/info" -H "X-API-Key: $CLAUDE_AGENT_API_KEY" | jq '.allowed_commands'
# expect: array including "/newsfind-queries"
```

If `/newsfind-queries` is missing from the allowlist → rebuild claude_agent on the VPS so the updated `apps/claude_agent/.env` is baked in.

---

## 2. Streaming with filtered live view (recommended path)

See phase markers + tool calls live, then a final `✓ DONE`. Best UX for any long command.

```bash
curl -N -X POST "$API/v1/agent/stream" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -d '{"command":"/newsfind-queries","args":"Hormuz strait closure options to lower price","timeout_sec":900}' \
  | sed -e 's/^data: //' \
  | jq -rc --unbuffered '
      if .type=="assistant" and .message.content then
        .message.content[]
        | select(.type=="tool_use")
        | "→ \(.name): \((.input | tostring)[0:140])"
      elif .type=="user" and (.message.content[0].type//"") == "tool_result" then
        "← tool returned"
      elif .type=="result" then
        "✓ DONE in \(.duration_ms)ms, cost $\(.total_cost_usd // 0)"
      elif .type=="end" then
        "[stream ended, exit_code=\(.exit_code)]"
      else empty end'
```

Notes:
- `-N` disables curl buffering (mandatory for SSE).
- `sed -e 's/^data: //'` strips the SSE prefix.
- `jq --unbuffered` flushes line by line so output is live.
- Watch for the phase echoes (`{"phase":"P1",...}`) inside Bash tool calls — that's the agent telling you where it is.

---

## 3. Streaming + capture final JSON to file

Same as Section 2, but tee the raw stream to disk so you can extract the final blueprint after it finishes.

```bash
curl -N -X POST "$API/v1/agent/stream" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -d '{"command":"/newsfind-queries","args":"Hormuz strait closure options to lower price","timeout_sec":900}' \
  | sed -e 's/^data: //' \
  | tee /tmp/newsfind.stream.ndjson \
  | jq -rc --unbuffered '
      if .type=="assistant" and .message.content then
        .message.content[] | select(.type=="tool_use") | "→ \(.name)"
      elif .type=="result" then "✓ DONE"
      elif .type=="end"    then "[exit_code=\(.exit_code)]"
      else empty end'

# After the run, extract the final parsed JSON:
grep '"type":"result"' /tmp/newsfind.stream.ndjson \
  | head -1 \
  | jq -r '.result' \
  | jq . > /tmp/newsfind.json

# Quick sanity check of what came back:
jq '{stage, schema_version, domain, current_state, queries_count: (.queries | length)}' /tmp/newsfind.json
```

---

## 4. Sync mode — one-shot, no progress (only for short commands)

```bash
curl -s -X POST "$API/v1/agent/run" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -d '{"command":"/newsfind-queries","args":"Hormuz strait closure options to lower price","timeout_sec":900}' \
  | jq '{status, exit_code, error, duration_ms, parsed}'
```

Reading the response:
- `status: "succeeded"` + `parsed.stage == "queries"` → blueprint is in `parsed`.
- `status: "failed"` + non-null `error` → CLI exited non-zero. Check `stderr` for clues.
- `status: "timeout"` → command exceeded `timeout_sec`. Increase the timeout or use streaming.

---

## 5. Async job mode — fire and poll (good for background runs)

```bash
JOB=$(curl -s -X POST "$API/v1/agent/jobs" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -d '{"command":"/newsfind-queries","args":"Hormuz strait closure options to lower price","timeout_sec":900}' \
  | jq -r '.id')
echo "Job: $JOB"

# Poll every 10s until terminal status:
while :; do
  S=$(curl -s "$API/v1/agent/jobs/$JOB" -H "X-API-Key: $CLAUDE_AGENT_API_KEY" | jq -r '.status')
  echo "$(date +%T) status=$S"
  case "$S" in succeeded|failed|cancelled|timeout) break;; esac
  sleep 10
done

# Get the result (parsed JSON or error message):
curl -s "$API/v1/agent/jobs/$JOB" -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  | jq '{status: .status, parsed: .result.parsed, error: .result.error}'
```

---

## 6. Pass criteria (sanity-check the parsed blueprint)

After Section 3 leaves a file at `/tmp/newsfind.json`:

```bash
jq -e '
  .schema_version == "0.2.0"                                      and
  (.queries | length) >= 10 and (.queries | length) <= 15         and
  (.entities.actors | length) >= 1                                and
  (.queries | map(.intent)       | unique | sort) == ["context","monitoring"] and
  (.current_state | length) > 20                                  and
  (.working_thesis | length) > 20
' /tmp/newsfind.json && echo "PASS" || echo "FAIL"
```

---

## 7. If something looks wrong — debug on the VPS

```bash
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212

# Container logs (last 100 lines, follow live):
docker compose logs --tail=100 -f claude_agent

# Test the slash command DIRECTLY inside the container.
# IMPORTANT: pass the slash command + topic as ONE quoted string.
docker compose exec -w /workspace/claude_agent_fe claude_agent \
  claude -p --output-format json --permission-mode dontAsk \
  "/newsfind-queries Hormuz strait closure options to lower price"

# Same thing but streaming, to see live tool calls:
docker compose exec -w /workspace/claude_agent_fe claude_agent \
  claude -p --output-format stream-json --permission-mode dontAsk \
  "/newsfind-queries Hormuz strait closure options to lower price" \
  | head -60
```

Common failure modes and what to check:

| Symptom | Likely cause | Where to look |
|---|---|---|
| `Unknown command: /newsfind-queries` | wrong cwd OR command not allowlisted | confirm `info.allowed_commands`; CLI test must use `-w /workspace/claude_agent_fe` |
| Model says "topic is missing" | slash command + topic not passed as ONE string | quote them together: `"/newsfind-queries TOPIC..."` |
| `exit_code: 1` with empty parsed | RAG endpoint unreachable from container | check `RAG_BASE_URL` env, ping `http://rag_adhoc:8000/readyz` from inside container |
| `status: "timeout"` | command genuinely slow, or hung | increase `timeout_sec`, check logs for what tool stalled |
| Stream has `→ Bash` echoes but never `✓ DONE` | model is still working OR stuck mid-phase | watch logs; if no output for 60s+ on a phase, kill and retry |
