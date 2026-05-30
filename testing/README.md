# testing/

Stable evaluation harness (#11). Full cold run: plan → deliver → refresh. Fresh topic every time (no cache).

Spec: `docs/specs/done/rag_full_stable_evaluation_11.md`

## How to run

**Prereq:** `testing/.env.test1` (or `.env.test2` / `.env.testing` for prod) with `API`, `CLAUDE_AGENT_API_KEY`. Needs `curl`, `jq`, `bc`. Prod/test URLs must be **HTTPS hostnames** (not `IP:8002` — ports are localhost-only on the VPS).

```bash
# From repo root — full run (~15–30 min)
scripts/test_vector_runner.sh --env test1

# Other slot or prod
scripts/test_vector_runner.sh --env test2
scripts/test_vector_runner.sh --env prod

# After crash — continue same run
scripts/test_vector_runner.sh --env test1 --resume

# Compare two finished runs
scripts/compare_evaluations.sh \
  testing/results/test1/latest/evaluation.json \
  testing/results/test2/latest/evaluation.json
```

**Results:** `testing/results/<env>/<timestamp>/` — `evaluation.json`, `agent_log/`, `business_output/`, `runner.log`. Latest: `testing/results/<env>/latest/`.

## Environments

| Env | URL | Config |
|---|---|---|
| `test1` | `agent-test1.particletico.com` | `testing/.env.test1` |
| `test2` | `agent-test2.particletico.com` | `testing/.env.test2` |
| `prod` | `agent.particletico.com` | `testing/.env.testing` |

## Test Vector

Current vector (`testing/vectors.json`):

| ID | Topic | Stages |
|---|---|---|
| V001_hormuz | Hormuz strait closure options to lower price | plan → deliver → refresh |

Exercises the entire lifecycle: topic creation, query planning with intro, delivery with report, and refresh with latest news delta.

## Two-Channel Output

| Channel | Directory | Content |
|---|---|---|
| **Agent debug log** | `agent_log/` | Complete SSE events, tool calls, stage timing, costs, errors — system internals |
| **Business output** | `business_output/` | intro.md, report.md, news.json, parsed.json — what the user sees |

Plus:
- `evaluation.json` — 40+ structured metrics extracted from both channels
- `runner.log` — timestamped run log
- `state.json` — recovery checkpoint

## Output Layout

```
testing/results/<env>/<timestamp>/
  state.json                ← checkpoint for recovery
  runner.log                ← human-readable run log
  evaluation.json           ← structured metrics for comparison
  agent_log/
    create_response.json    ← POST /topics response
    events_plan.ndjson      ← SSE events during planning
    events_deliver.ndjson   ← SSE events during delivery
    events_refresh_1.ndjson ← SSE events during refresh
    events_full.ndjson      ← complete event log from DB (authoritative)
    topic_final.json        ← final topic state
  business_output/
    parsed.json             ← query plan (search strategy)
    intro.md / intro.json   ← working thesis and intro
    news.json               ← collected sources with scores
    report.json             ← structured report (findings, scenarios)
    report.md               ← markdown report (what user reads)
    refresh_deltas.json     ← refresh cycle results
    refresh_news.json       ← new sources from refresh
    refresh_report.md       ← refresh narrative
```

## Recovery

State machine with checkpoints:
```
not_started → planning → planned → delivering → reported → collecting → completed
```

If interrupted, `--resume` reads state.json, checks server-side topic state, and continues.

## Cross-Instance Comparison

```bash
scripts/compare_evaluations.sh <eval_a.json> <eval_b.json>
```

Outputs a table comparing timing, cost, plan quality, delivery quality, and event metrics. Also writes `comparison.json` for programmatic use.

## Evaluation Guide

See [How to evaluate results](#how-to-evaluate-results) below.

---

## How to Evaluate Results

### 1. Quick comparison between instances

Run the same vector on two instances and compare:

```bash
scripts/test_vector_runner.sh --env test1
scripts/test_vector_runner.sh --env test2
scripts/compare_evaluations.sh \
  testing/results/test1/latest/evaluation.json \
  testing/results/test2/latest/evaluation.json
```

Key metrics to compare:
- **Cost efficiency**: `cost.total_usd` — lower is better for same quality
- **Speed**: `timing.total_sec` — faster means better orchestration
- **Source quality**: `deliver.sources_total`, `deliver.sources_unique_publishers`, `deliver.sources_avg_relevance`
- **Output depth**: `deliver.key_findings_count`, `deliver.report_words`, `deliver.unique_citations`
- **Reliability**: `events.tool_errors` — should be zero

### 2. Track quality over time

Run on the same instance periodically. Compare the `latest` symlink with an older run:

```bash
scripts/compare_evaluations.sh \
  testing/results/test1/2026-05-26T14-00-00Z/evaluation.json \
  testing/results/test1/latest/evaluation.json
```

### 3. Feed evaluation.json to an evaluator agent

The `evaluation.json` is designed for agent consumption. Example prompt:

```
You are evaluating two runs of a news research pipeline.
Compare these evaluation.json files and produce a quality assessment:

Run A (test1): <paste evaluation.json>
Run B (test2): <paste evaluation.json>

Assess:
1. Which run produced higher quality research output? 
   (more sources, better relevance, deeper findings, better citations)
2. Which was more cost-efficient?
3. Which had fewer operational issues? (tool errors, drops)
4. Based on the business_output/ files, which report.md is more 
   comprehensive and actionable?
5. Overall recommendation: which instance version is better?
```

### 4. Deep qualitative review using business_output/

For human or agent review of the actual product:

- **intro.md** — Is the working thesis well-formed and actionable?
- **parsed.json** → `queries` — Are queries diverse (multi-language, multi-angle)?
- **news.json** → `sources` — Are sources recent, relevant, from varied publishers?
- **report.md** — Is the report well-structured with proper citations `[s1]`, clear findings?
- **report.json** → `key_findings` — Are findings specific and evidence-backed?
- **report.json** → `scenarios` — Are scenarios plausible with distinct probability ranges?

### 5. Deep debug review using agent_log/

For diagnosing system behavior:

- **events_full.ndjson** — Every event the system produced (authoritative, from DB)
- Filter by type: `jq 'select(.event_type=="tool_use")' events_full.ndjson`
- Find errors: `jq 'select(.event_type=="tool_result" and .payload.is_error==true)' events_full.ndjson`
- Stage timing: `jq 'select(.event_type=="stage.finished")' events_full.ndjson`
- Trace full tool sequence: `jq '{seq, type: .event_type, tool: .payload.tool}' events_full.ndjson`

### 6. Automated regression check

Write a script that reads evaluation.json and checks thresholds:

```bash
jq -e '
  .deliver.sources_total >= 5 and
  .deliver.key_findings_count >= 2 and
  .deliver.unique_citations >= 3 and
  .events.tool_errors == 0 and
  .cost.total_usd < 2.0
' evaluation.json && echo "PASS" || echo "FAIL"
```

---

## Old Scripts (still work)

| Script | Purpose |
|---|---|
| `scripts/test_full_pipeline.sh` | One-shot A→Z (no recovery) |
| `scripts/test_continue_topic.sh` | Resume a single topic by ID |
| `scripts/test_refresh_cycle.sh` | Refresh cycle on a reported topic |
| `scripts/test_topic.sh` | Quick single-command test |
