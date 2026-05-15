# Newsfind Pipeline — Full Lifecycle Testing Guide

API: `http://79.143.179.212:8002`

---

## Setup (run once per terminal session)

```bash
export API="http://79.143.179.212:8002"
export TOPIC="Hormuz strait closure options to lower price"
```

---

## 1. Start a topic

```bash
RESP=$(curl -fsS -X POST "$API/v1/topics" \
  -H "Content-Type: application/json" \
  -d "{\"topic\":\"$TOPIC\"}")
echo "$RESP" | jq .
export TOPIC_ID=$(echo "$RESP" | jq -r .topic_id)
echo "TOPIC_ID=$TOPIC_ID"
```

Expected: `{"topic_id":"...","state":"planning","events_url":"..."}`

---

## 2. Watch the system output live (event stream)

In a second terminal, tail the SSE stream while the agent plans:

```bash
export API="http://79.143.179.212:8002"
export TOPIC_ID="<paste from step 1>"

curl -N "$API/v1/topics/$TOPIC_ID/events" \
  | grep '^data: ' | sed 's/^data: //' \
  | jq -r '
      if .event_type=="tool_use" then
        "\n▶ seq=\(.seq) TOOL: \(.payload.tool)\n  \(.payload.input_preview)"
      elif .event_type=="tool_result" then
        "◀ seq=\(.seq) RESULT [err=\(.payload.is_error)]\n  \(.payload.output_preview)"
      elif .event_type=="stage.started" then "\n━━ stage.started: \(.payload.stage) ━━"
      elif .event_type=="stage.finished" then
        "━━ stage.finished: \(.payload.stage) (\(.payload.duration_ms)ms $\(.payload.total_cost_usd))"
      elif .event_type=="intro.ready" then "\n✓ INTRO READY: \(.payload.headline)"
      elif .event_type=="needs_input" then "\n⏸ GATE: \(.payload.gate) — run /proceed or /cancel"
      elif .event_type=="report.ready" then "\n✓ REPORT READY"
      elif .event_type=="state.changed" then "→ state: \(.payload.from) → \(.payload.to)"
      elif .event_type=="error" then "\n✗ ERROR: \(.payload.error)"
      else "  · \(.event_type)"
      end'
```

Stream ends automatically when the topic reaches `planned_awaiting_review` (gate) or `reported`/`failed`.

---

## 3. Check the plan — queries + intro

After the stream shows `⏸ GATE: planned_awaiting_review`, the agent has finished planning.

**See the query plan (what searches will be run):**
```bash
curl -fsS "$API/v1/topics/$TOPIC_ID/parsed" \
  | jq '.queries[] | {id, query, intent, language, priority}'
```

**Count and summarise:**
```bash
curl -fsS "$API/v1/topics/$TOPIC_ID/parsed" \
  | jq '{queries_count: (.queries|length), languages: (.queries|map(.language)|unique), rag_refs: (.rag_context_refs|length)}'
```

**Read the human-readable intro (working thesis, current state, approach):**
```bash
curl -fsS "$API/v1/topics/$TOPIC_ID/intro.md"
```

**Check topic status at any time:**
```bash
curl -fsS "$API/v1/topics/$TOPIC_ID" \
  | jq '{state, available_actions, last_event_seq, error}'
```

---

## 4. Approve or decline the plan

**Approve → start web search + report generation:**
```bash
curl -fsS -X POST "$API/v1/topics/$TOPIC_ID/proceed" | jq .
```

**Decline → cancel the topic:**
```bash
curl -fsS -X POST "$API/v1/topics/$TOPIC_ID/cancel" | jq .
```

After `/proceed`, re-attach the event stream from step 2 to watch the deliver stage.
Deliver takes 5–12 minutes (runs 13+ web searches, fetches sources, synthesises report).

---

## 5. Get the news report

After the stream shows `✓ REPORT READY` and state transitions to `reported`:

**Executive summary (markdown):**
```bash
curl -fsS "$API/v1/topics/$TOPIC_ID/report.md"
```

**Full structured report (JSON with key findings, scenarios, citations):**
```bash
curl -fsS "$API/v1/topics/$TOPIC_ID/report" | jq '{thesis_status, key_findings_count: (.key_findings|length), sources_count}'
```

**All collected news sources:**
```bash
curl -fsS "$API/v1/topics/$TOPIC_ID/news" \
  | jq '.sources[] | {id, title, publisher, published_at, relevance_score, source_class}'
```

**Source count:**
```bash
curl -fsS "$API/v1/topics/$TOPIC_ID/news" | jq '.sources | length'
```

---

## 6. Check latest news (most recent sources)

Sort collected sources by date to see the freshest information:

```bash
curl -fsS "$API/v1/topics/$TOPIC_ID/news" \
  | jq '[.sources[] | select(.published_at != null)] | sort_by(.published_at) | reverse | .[:5] | .[] | {title, publisher, published_at, url}'
```

Check which queries produced results and how many:

```bash
curl -fsS "$API/v1/topics/$TOPIC_ID/news" \
  | jq '.executed_queries[] | {id, query: .query, results: .results_count}'
```

---

## Recover a lost TOPIC_ID

If you close the terminal, find your topic again from the database:

```bash
# Most recent 10 topics
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212 \
  "docker compose -f ~/agent_bench/docker-compose.yml exec -T postgres \
   psql -U agentic -d agentic -P pager=off -c \
   'SELECT id, state, LEFT(topic,60), created_at FROM topics ORDER BY created_at DESC LIMIT 10;'"

# Auto-export the most recent topic ID
export TOPIC_ID=$(ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212 \
  "docker compose -f ~/agent_bench/docker-compose.yml exec -T postgres \
   psql -U agentic -d agentic -t -A -c \
   'SELECT id FROM topics ORDER BY created_at DESC LIMIT 1;'" | tr -d '\r')
echo "TOPIC_ID=$TOPIC_ID"
```

---

---

## Other useful commands & what to test next

### Service health
```bash
curl -fsS "$API/readyz"
```

### Inspect all events for a topic (full audit log in DB)
```bash
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212 \
  "docker compose -f ~/agent_bench/docker-compose.yml exec -T postgres \
   psql -U agentic -d agentic -P pager=off -c \
   \"SELECT seq, event_type, LEFT(payload::text, 200) FROM topic_events WHERE topic_id='$TOPIC_ID' ORDER BY seq;\""
```

### Verify RAG was used (check for RAG curl calls)
```bash
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212 \
  "docker compose -f ~/agent_bench/docker-compose.yml exec -T postgres \
   psql -U agentic -d agentic -P pager=off -c \
   \"SELECT seq, event_type, payload FROM topic_events WHERE topic_id='$TOPIC_ID' AND payload::text ILIKE '%rag_adhoc%' ORDER BY seq;\""
```

### Watch container logs (Python/FastAPI side)
```bash
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212 \
  "docker compose -f ~/agent_bench/docker-compose.yml logs -f --tail=100 claude_agent"
```

### Topics by state (find stuck or failed runs)
```bash
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212 \
  "docker compose -f ~/agent_bench/docker-compose.yml exec -T postgres \
   psql -U agentic -d agentic -P pager=off -c \
   'SELECT state, count(*) FROM topics GROUP BY state ORDER BY count DESC;'"
```

---

## What needs testing before frontend

- [ ] **`GET /v1/topics` (list endpoint)** — does not exist yet; needed by the FE to show all topics. Needs to be added to `apps/claude_agent/topics/routes.py`.
- [ ] **Deliver stage on existing gate topics** — topics stuck at `planned_awaiting_review` from before the fix can be proceeded now; verify they complete cleanly.
- [ ] **Concurrent topics** — start 2–3 topics simultaneously and confirm `max_concurrent_jobs=4` keeps them stable.
- [ ] **Cancel mid-run** — start a topic, cancel it during planning, verify state becomes `cancelled` and the Claude subprocess exits.
- [ ] **Webhook delivery** — register a webhook with `POST /v1/topics/{id}/subscribe {url, secret}` and verify `intro.ready` + `report.ready` payloads arrive signed with HMAC.
- [ ] **Artifact endpoints after failure** — if a topic ends in `failed`, confirm artifact endpoints return 404 (not 500).
- [ ] **v2 continuous monitoring** — not yet implemented; needs scheduler, `/newsfind-refresh` slash command, `topic_subscriptions` + `topic_refresh_deltas` tables, and new API endpoints (`GET /v1/topics/{id}/deltas`, etc.). Spec is in `AGENT.md`.
