# RAG full stable evaluation — #11

**Status:** done (2026-05-27)  
**Depends on:** #10 (RAG main corpus), #12 (Caddy), #13 (Multi-env)

## Goal

Stable, recoverable end-to-end evaluation of the Newsfind pipeline (plan → deliver → refresh) across deployed instances. Captures **both output channels** (agent debug log + user-facing business output) and produces structured `evaluation.json` for cross-instance quality comparison — including plan-stage RAG usage (`rag_refs_count`, query strategy).

## Problem

Before this ticket:
- Test scripts (`test_full_pipeline.sh`) had no recovery — crash at minute 8 = restart from zero
- No stable test vectors — hard to compare quality across instances or runs
- No structured output for comparison — only terminal output
- No separation of debug logs vs business results
- Event stream was captured live-only — if SSE dropped, data was lost

## Solution

### Two-channel output model

The system produces two distinct output channels:

| Channel | Content | Purpose |
|---------|---------|---------|
| **agent_log/** | Full SSE event stream, tool calls with input/output previews, stage timing, cost per stage, errors | Debug and observability — what the system did and how |
| **business_output/** | intro.md, parsed.json, news.json, report.json, report.md, refresh deltas | What the user sees — the product output |

Plus:
- **evaluation.json** — structured metrics extracted from both channels, machine-comparable
- **runner.log** — timestamped human-readable run log
- **state.json** — checkpoint for recovery

### Stable test vector

Single stable vector (`V001_hormuz` in `testing/vectors.json`) exercises the full lifecycle:
1. Create topic → plan (query strategy + intro, RAG context refs)
2. Approve → deliver (web search + report)
3. Monitor → refresh (latest news delta)

### Recovery

State machine with checkpoints after every step:
```
not_started → planning → planned → delivering → reported → collecting → completed
```

`--resume` reads `state.json`, checks server state, and continues from last checkpoint.

### evaluation.json schema

```json
{
  "vector_id": "V001_hormuz",
  "env": "test1",
  "api": "https://agent-test1.particletico.com",
  "topic_id": "uuid",
  "timestamp": "iso",
  "claude_version": "2.1.145",
  "timing": {"plan_sec", "deliver_sec", "refresh_sec", "total_sec"},
  "cost": {"plan_usd", "deliver_usd", "refresh_usd", "total_usd"},
  "events": {
    "total_events", "tool_calls", "tool_errors",
    "tool_names": {"WebSearch": 13, "WebFetch": 4, ...},
    "stages": [{"stage", "duration_ms", "cost_usd"}]
  },
  "plan": {
    "queries_count", "languages", "language_count",
    "rag_refs_count", "working_thesis", "entities_actors",
    "scenarios_count", "monitoring_triggers"
  },
  "deliver": {
    "sources_total", "sources_with_date", "sources_newest_date",
    "sources_unique_publishers", "sources_avg_relevance",
    "source_classes", "queries_executed", "queries_with_results",
    "drops", "key_findings_count", "scenarios_count",
    "thesis_status", "thesis_update", "open_questions_count",
    "next_queries_count", "report_lines", "report_words",
    "unique_citations", "summary_md"
  },
  "refresh": {
    "enabled", "new_sources_count", "queries_executed",
    "duration_ms", "cost_usd", "status"
  }
}
```

## Artifacts

| Path | Role |
|------|------|
| `testing/vectors.json` | Stable test vector definition |
| `scripts/test_vector_runner.sh` | Recoverable test runner with two-channel output |
| `scripts/compare_evaluations.sh` | Cross-instance comparison tool |
| `testing/.env.test1` | Test slot 1 config |
| `testing/.env.test2` | Test slot 2 config |
| `testing/.env.testing` | Production config |

### Output layout

```
testing/results/<env>/<timestamp>/
  state.json              ← recovery checkpoint
  runner.log              ← timestamped human-readable log
  evaluation.json         ← structured metrics for comparison
  agent_log/
    create_response.json  ← POST /topics response
    events_plan.ndjson    ← live SSE during plan
    events_deliver.ndjson ← live SSE during deliver
    events_refresh_1.ndjson
    events_full.ndjson    ← complete event log from DB (authoritative)
    topic_final.json      ← final topic state
    monitor_response.json
  business_output/
    parsed.json           ← query plan (what frontend renders at gate)
    intro.json            ← structured intro
    intro.md              ← markdown intro
    news.json             ← collected sources with relevance scores
    report.json           ← structured report with findings, scenarios
    report.md             ← markdown report (what user reads)
    refresh_deltas.json   ← refresh cycle results
    refresh_delta.json    ← delta details
    refresh_news.json     ← new sources from refresh
    refresh_report.md     ← refresh summary
```

## Usage

```bash
# Run on test1
scripts/test_vector_runner.sh --env test1

# Run on test2
scripts/test_vector_runner.sh --env test2

# Resume after crash
scripts/test_vector_runner.sh --env test1 --resume

# Compare two runs
scripts/compare_evaluations.sh \
  testing/results/test1/latest/evaluation.json \
  testing/results/test2/latest/evaluation.json
```

## Acceptance criteria

- [x] Stable test vector (`V001_hormuz`) versioned in `testing/vectors.json`
- [x] Two-channel output: `agent_log/` and `business_output/`
- [x] `evaluation.json` with 40+ structured metrics from both channels
- [x] Full event log fetched from DB (not dependent on live SSE)
- [x] Recovery via `state.json` checkpoints at every step
- [x] Refresh cycle included in the test scenario
- [x] `compare_evaluations.sh` produces structured diff table + `comparison.json`
- [x] `latest` symlink for easy access to most recent run
- [x] Multi-env support: test1, test2, prod via `--env` flag

## Related

- `testing/README.md` — usage and evaluation guide
- `docs/specs/done/rag_main_corpus_highest_roi_10.md` — RAG corpus (#10)
- `docs/specs/done/setup_caddy_reverse_proxy_12.md` — Caddy/HTTPS (#12)
- `docs/specs/done/multi_env_pre_frontend_13.md` — multi-env setup (#13)
