# Newsfind application verification — #15

**Status:** active (in progress)  
**Depends on:** #11 (stable run harness), #13 (multi-env)  
**Lane:** B — *Does the application still work correctly?*  
**Related tickets:** #11 (harness), #18 (business output evaluation), #19 (DevOps test execution)

## Goal

Provide a **repeatable technical PASS/FAIL signal** for Newsfind runs.  
This ticket defines **what to test** and **what counts as passing** so regressions are detected early and can later become strict release gates.

This is application correctness and regression safety. It is **not** a business-value judgment.

## Core question

*“Did we break product mechanics, output contracts, or known operational invariants?”*

## Responsibility split

- **#15 (this ticket):** test definitions, assertions, and pass/fail criteria.
- **#19:** where and how these tests execute on VPS/GitHub checks.
- **#18:** business usefulness and qualitative output judgment.

## Test levels in scope

### 1) Unit tests (fast, non-billable, PR-level)

Unit tests must validate deterministic logic without external paid inference:

- artifact parsing and validation helpers
- threshold evaluators (`min_sources`, `min_findings`, citations count)
- event sequence/invariant validators
- `qa_check_run.sh` logic through fixture-based tests (good run vs broken run)

Expected runtime: short enough for every PR.  
No network dependency on VPS slots.

### 2) Integration/E2E run verification (artifact-driven)

Validate run outputs from `test_vector_runner.sh`:

- required files exist and are non-empty (`evaluation.json`, `agent_log/events_full.ndjson`, `business_output/*`)
- output schema/structure checks for plan and deliver artifacts
- hard thresholds for technical validity (not quality scoring)
- topic reaches expected terminal state (`reported` unless explicitly testing failure paths)

Output artifact: `qa_report.json` with `{ passed, failed_checks, summary, checks[] }`.

### 3) Operational invariants

From `agent_log/events_full.ndjson` and `topic_final.json`:

- expected high-level stage progression exists
- no unrecovered error terminal path in successful runs
- stage timing/cost fields are present when expected
- citation integrity in report remains mechanically valid

### 4) Smoke checks

Minimal vector(s) for quick signal:

- readiness endpoint (`GET /readyz`)
- lightweight topic path for fast end-to-end confidence

## Server process reference (definition only)

This ticket defines expected behavior for server-side execution:

1. run vector on `test1`/`test2`
2. run QA gate on produced run directory
3. emit machine-readable pass/fail artifact (`qa_report.json`)
4. in current informational mode: mark QA failure as advisory; in later required mode: block deployment/release on QA failure

Execution mechanics (workflows, runners, branch protection, artifact upload) are implemented in **#19**.

## Known-bad regression catalog (must fail)

| Check | Example failure |
|-------|-----------------|
| Missing required artifact | No `report.json` after successful deliver |
| Broken event log | Empty/missing `events_full.ndjson` |
| Tool error regression | `events.tool_errors > 0` |
| Citation integrity break | report cites `[sN]` with no matching source evidence |
| Stuck lifecycle | topic never reaches expected terminal state |

## Out of scope

- Human or LLM-as-judge business-value scoring (**#18**)
- VPS execution wiring and GitHub check orchestration (**#19**)
- Frontend E2E (Playwright)
- Load/stress testing

## Planned artifacts

| Path | Role |
|------|------|
| `testing/qa_rules.json` | Machine-readable rules and thresholds |
| `scripts/qa_check_run.sh` | Post-run PASS/FAIL evaluator |
| `testing/results/<env>/<ts>/qa_report.json` | Gate result per run |
| `testing/baselines/` | Optional baseline metrics for mechanical drift detection |

## Acceptance criteria

- [ ] Unit-test scope is explicitly documented and runnable in CI.
- [ ] `qa_check_run.sh` passes on healthy fixtures and fails on injected-bad fixtures.
- [ ] Full V001 run on `test1` produces `qa_report.json` with `passed: true` when healthy.
- [ ] Known-bad regression cases are represented as explicit failing checks.
- [ ] `testing/README.md` documents verification flow and references #19 for execution.
- [ ] Docs consistently state: #15 = technical gate, #18 = business evaluation, #19 = execution pipeline.

## Related

- `docs/specs/done/rag_full_stable_evaluation_11.md` — harness foundation
- `docs/specs/active/business_output_evaluation_18.md` — business lane
- `docs/specs/active/devops_vps_test_execution_19.md` — execution lane
- `testing/vectors.json`
- `scripts/test_vector_runner.sh`
- `scripts/qa_check_run.sh`
