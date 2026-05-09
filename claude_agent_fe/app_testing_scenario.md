# Testing /newsfind-queries

The new lightweight version targets ~90-150s end-to-end. Use streaming for live visibility.

---

## 1. Original sync mode (slow, no progress, easy to pipe to jq)

```bash
curl -s -X POST http://79.143.179.212:8002/v1/agent/run \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -d '{"command":"/newsfind-queries","args":"Hormuz strait closure options to lower price","timeout_sec":900}' \
  | jq '.parsed' > /tmp/newsfind_A.json
```

---

## 2. Streaming mode — raw events (see everything live)

```bash
curl -N -X POST http://79.143.179.212:8002/v1/agent/stream \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -d '{"command":"/newsfind-queries","args":"Hormuz strait closure options to lower price","timeout_sec":900}'
```

`-N` disables curl buffering — required for SSE.

---

## 3. Streaming mode — filtered live view (recommended)

Shows phase markers, tool calls, and the final result line:

```bash
curl -N -X POST http://79.143.179.212:8002/v1/agent/stream \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -d '{"command":"/newsfind-queries","args":"Hormuz strait closure options to lower price","timeout_sec":900}' \
  | awk -W interactive '/^data: /{sub(/^data: /,""); print; fflush()}' \
  | jq -rc --unbuffered '
      if .type=="assistant" and .message.content then
        .message.content[]
        | select(.type=="tool_use")
        | "→ \(.name): \((.input | tostring)[0:140])"
      elif .type=="user" and (.message.content[0].type//"") == "tool_result" then
        "← tool returned"
      elif .type=="result" then
        "✓ DONE in \(.duration_ms)ms, cost $\(.total_cost_usd // 0)"
      else empty end'
```

Expected output:

```
→ Bash: echo '{"phase":"P1","status":"start","label":"domain & frame"}'
← tool returned
→ Bash: echo '{"phase":"P1","status":"done"}'
← tool returned
→ Bash: echo '{"phase":"P2","status":"start","label":"initial state read"}'
← tool returned
→ Bash: source .env && curl -sS -X POST "${RAG_BASE_URL}" ...
← tool returned
→ WebSearch: {"query":"..."}
← tool returned
→ Bash: echo '{"phase":"P2","status":"done","rag_calls":1,"web_calls":1}'
← tool returned
→ Bash: echo '{"phase":"P3","status":"start","label":"entities & thesis"}'
← tool returned
→ Bash: echo '{"phase":"P4","status":"start","label":"build queries"}'
← tool returned
→ Bash: echo '{"phase":"P4","status":"done","queries":12}'
← tool returned
✓ DONE in 118000ms, cost $0.08
```

---

## 4. Streaming mode + capture final JSON to a file

Watch live AND save the final blueprint to disk for inspection:

```bash
curl -N -X POST http://79.143.179.212:8002/v1/agent/stream \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -d '{"command":"/newsfind-queries","args":"Hormuz strait closure options to lower price","timeout_sec":900}' \
  | awk -W interactive '/^data: /{sub(/^data: /,""); print; fflush()}' \
  | tee /tmp/newsfind_A.stream.ndjson \
  | jq -rc --unbuffered '
      if .type=="assistant" and .message.content then
        .message.content[] | select(.type=="tool_use") | "→ \(.name)"
      elif .type=="result" then
        "✓ DONE"
      else empty end'

# After it finishes, extract the parsed JSON:
grep '"type":"result"' /tmp/newsfind_A.stream.ndjson \
  | head -1 \
  | jq -r '.result' \
  | jq . > /tmp/newsfind_A.json

cat /tmp/newsfind_A.json | jq '{stage, domain, current_state, queries: (.queries | length)}'
```

---

## 5. Sanity checks on the parsed output

```bash
jq '
  .schema_version,
  .domain,
  .current_state,
  (.entities.actors | length) as $actors |
  (.queries | length) as $qs |
  (.queries | map(.language) | unique) as $langs |
  {actors: $actors, queries: $qs, languages: $langs}
' /tmp/newsfind_A.json
```

Pass criteria:
- `schema_version == "0.2.0"`
- `domain` is a non-empty short slug
- `current_state` is 2-3 sentences grounded in P2
- `queries` length in `[10, 15]`
- Both `context` and `monitoring` intents represented
- For non-anglophone topics: ≥30% non-`en` queries

---

## 6. Domain-agnostic check (run a non-commodity topic)

```bash
curl -N -X POST http://79.143.179.212:8002/v1/agent/stream \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -d '{"command":"/newsfind-queries","args":"Nvidia Q2 datacenter revenue guidance risk","timeout_sec":900}' \
  | awk -W interactive '/^data: /{sub(/^data: /,""); print; fflush()}' \
  | tee /tmp/newsfind_B.stream.ndjson \
  | jq -rc --unbuffered 'if .type=="assistant" and .message.content then .message.content[] | select(.type=="tool_use") | "→ \(.name)" elif .type=="result" then "✓ DONE" else empty end'

grep '"type":"result"' /tmp/newsfind_B.stream.ndjson | head -1 | jq -r '.result' | jq . > /tmp/newsfind_B.json
jq '{domain, actors: .entities.actors, queries: (.queries|length)}' /tmp/newsfind_B.json
```

Expected: `domain` is something like `equity_earnings` or `tech_supply_chain`; `actors` are semiconductor/datacenter names — proves no oil/gas hardcoding bled through.
