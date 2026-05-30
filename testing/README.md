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

## Evaluate a completed run for demo/business quality

After `scripts/test_full_pipeline.sh` or `scripts/test_topic.sh` finishes, run the
offline evaluator against the run directory:

```bash
scripts/evaluate_newsfind_run.py testing/runs/<run-dir>
```

It writes:

```
testing/runs/<run-dir>/evaluation/
  evaluation.json   machine-readable scorecard
  evaluation.md     business-review brief for trader/NLP demo prep
```

The scorecard is intentionally about product value, not just JSON validity. It
checks:

- query-plan coverage of actors, languages, source classes, scenarios, and triggers
- evidence quality: source breadth, high-trust source share, freshness, relevance
- citation integrity between `report.md`, `report.json`, and `news.json`
- trading usefulness: market-impact language, thesis status, scenario updates, next queries
- artifact structure expected by the first demo flow

To compare a new run against a previous candidate:

```bash
scripts/evaluate_newsfind_run.py testing/runs/<new-run> \
  --baseline-run testing/runs/<old-run>
```
