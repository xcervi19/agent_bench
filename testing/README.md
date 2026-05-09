# testing/

Local debug captures from the laptop. **Not source of truth.**
Source of truth = `state/news/<topic_id>/runs/<run_id>/` written by the API.

## Layout

```
runs/<UTC-timestamp>__<command>__<topic-slug>/
  request.json    body sent to /v1/agent/stream
  stream.ndjson   raw SSE events (data: prefix stripped)
  parsed.json     business JSON only (this is what upper logic consumes)
  summary.json    decision-summary jq output
  queries.txt     human-readable list of generated queries
```

`runs/` is gitignored. Reruns are reproducible from `state/` and the API cache.

## Run a test

```bash
export API="http://79.143.179.212:8002"
export CLAUDE_AGENT_API_KEY="<your key>"

scripts/test_newsfind.sh
scripts/test_newsfind.sh "EU LNG supply disruption winter 2026"
scripts/test_newsfind.sh "Hormuz strait closure options to lower price" --force-refresh
scripts/test_newsfind.sh "China coal import shock" --timeout 1200
```

## List recent runs

```bash
scripts/list_runs.sh
```
