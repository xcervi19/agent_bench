# Newsfind QA automation (guardrails) — #15

**Status:** active (queued)  
**Depends on:** #11 (stable evaluation harness), #13 (multi-env)

## Two tracks

| Track | Ticket | Role |
|-------|--------|------|
| **Improve quality** | #11 (done) | Cold full runs, `evaluation.json`, compare instances, agent/human review |
| **Hold quality** | #15 (this) | Automated pass/fail on known rules — catch regressions and known bad behavior |

#11 answers: *“How good is this run vs another?”*  
#15 answers: *“Did we break something we already know how to detect?”*

## Goal

Full QA layer on top of the existing runner: after each run (or on CI), assert invariants on artifacts, events, API behavior, and thresholds. Fail fast with a clear report. No manual diff required for baseline safety.

## In scope (project context)

### 1. Structural / schema checks

Validate outputs against command contracts (`claude_agent_fe/.claude/commands/`):

- **Plan:** `parsed.json` — `queries[]` shape, ids, languages; `intro.json` / `summary.json` present; `intro.md` non-empty
- **Deliver:** `news.json` — `sources[]` with `url`, `relevance_score`, `source_class`; `report.json` — `key_findings`, scenarios; `report.md` — citation markers `[sN]`
- **Refresh:** `delta.json` / refresh artifacts when monitoring enabled

Use JSON Schema or `jq` assertions; fail with file + field path.

### 2. Threshold gates (extend `vectors.json`)

#11 already has soft checks in the runner; #15 should make them **hard gates**:

- Plan: `min_queries`, `max_queries`, `min_rag_refs`
- Deliver: `min_sources`, `min_findings`, `min_scenarios`, `report_min_lines`
- Events: `tool_errors == 0`, topic reaches `reported` (or expected terminal state)
- Cost ceiling (optional per env): `cost.total_usd < max`

Output: `qa_report.json` with `{passed, failures[]}`.

### 3. Event / pipeline invariants

From `agent_log/events_full.ndjson` and `topic_final.json`:

- Required sequence: `topic.created` → `stage.finished` (plan) → `needs_input` → … → `report.ready`
- No `event_type: error` before success
- `state.changed` ends in `reported` (not `failed` / stuck `planning`)
- Stage timing present on `stage.finished`

### 4. Smoke / health vectors

Lightweight vectors in `testing/vectors.json` (e.g. `V000_health`):

- `GET /readyz` only, or minimal topic with short timeout
- Run before/after deploy on `test1` / `test2`

### 5. Known-bad behavior catalog

Documented checks for failures seen in ops (extend over time):

| Check | Example failure |
|-------|-----------------|
| Permission on `/state/news` | Topic stuck `planning`, empty events |
| Empty `events_full.ndjson` | SSE/DB write failure |
| `summary.json` missing after stage | Slash command did not complete |
| All sources undated | Deliver quality regression |
| Report citations without matching sources | Broken `[sN]` integrity |

### 6. Runner integration

- `scripts/qa_check_run.sh <run_dir>` — reads `evaluation.json` + `business_output/` + `agent_log/`, writes `qa_report.json`, exit 1 on fail
- Optional: `test_vector_runner.sh` calls it at end of STEP 6
- CI: run vector on `test1` after deploy → `qa_check_run.sh` → block if fail

### 7. Comparison / baselines (later)

- Store last-known-good `evaluation.json` per env as `testing/baselines/<env>/V001.json`
- Fail if metrics drop below baseline (sources, findings, citations) — separate from cross-instance compare in #11

## Out of scope (for #15 v1)

- LLM-as-judge quality scoring (stays manual/agent in #11)
- Cache-hit / warm-path testing (`/newsfind-queries` + `force_refresh: false`) — different ticket
- Frontend E2E (Playwright) — pre-frontend phase
- Load/stress testing

## Artifacts (planned)

| Path | Role |
|------|------|
| `testing/qa_rules.json` | Machine-readable rules + thresholds per vector |
| `scripts/qa_check_run.sh` | Post-run assertion engine |
| `testing/results/<env>/<ts>/qa_report.json` | Pass/fail + failure list |
| `testing/baselines/` | Optional golden metrics per env |

## Acceptance criteria (when implemented)

- [ ] `qa_check_run.sh` fails a run with injected bad artifact (local test)
- [ ] All rules in `qa_rules.json` documented with rationale
- [ ] V001 full run produces `qa_report.json` with `passed: true` on healthy instance
- [ ] CI hook documented in `testing/README.md`
- [ ] Clear split documented: #11 = explore/compare, #15 = gate/hold

## Related

- `docs/specs/done/rag_full_stable_evaluation_11.md` — evaluation harness (#11)
- `docs/specs/done/reproducible_artifacts_and_cache.md` — cache path (not used by #11 cold runs)
- `testing/vectors.json`, `scripts/test_vector_runner.sh`, `scripts/compare_evaluations.sh`
