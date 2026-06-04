# Newsfind application verification — #15

**Status:** done (2026-06-02)  
**Depends on:** #11 (stable run harness), #13 (multi-env)  
**Feeds:** #18 (business eval expects technical PASS), #19 (CI/VPS runs gate + unit-tests)  
**Lane:** B — *Does the application still work correctly?*

## Goal / Problem

Provide a **repeatable technical PASS/FAIL signal** for Newsfind runs so mechanical regressions are caught before demos and business sign-off. #17 shipped a thin gate; this ticket defines the **full rule catalog**, extended gate, fixtures, and PR-level unit tests.

## Solution / What was delivered

| Component | Path | Role |
|-----------|------|------|
| Rule catalog | `testing/qa_rules.json` | 16 gating checks, thresholds, `known_bad` mapping |
| Gate script | `scripts/qa_check_run.sh` | Rules-driven PASS/FAIL → `qa_report.json` |
| Healthy fixture | `testing/fixtures/good_run/` | Committed run layout for unit tests |
| Unit tests | `tests/qa/` | 16 pytest cases; no network / no billable inference |
| Flow diagram | `testing/README.md` | Real workflow vs unit tests vs gate (mermaid) |
| Runner integration | `scripts/test_vector_runner.sh` | Calls gate after `evaluation.json` |

**Gate checks (all must pass):** required artifacts; `tool_errors == 0`; source/finding/citation thresholds; `topic_final.json` state `reported` (not `failed`); `stage.finished` for plan + deliver (parsed via `jq` on NDJSON); citation integrity (`[sNN]` / `NewsCard` → `news.json` ids).

**Responsibility split (unchanged):** #15 = definitions; #19 = CI/VPS/GitHub execution; #18 = business value.

## Artifacts

- `testing/qa_rules.json`
- `scripts/qa_check_run.sh`
- `testing/fixtures/good_run/`
- `tests/qa/test_qa_gate.py`, `tests/qa/test_qa_rules.py`, `tests/qa/conftest.py`
- Per-run: `testing/results/<env>/<ts>/qa_report.json`

## Usage

```bash
# PR / local — gate logic only (no app)
python -m pytest tests/qa -q

# Re-check an existing run
scripts/qa_check_run.sh --run-dir testing/results/test1/latest

# Full live verification (billable, ~15–30 min)
scripts/test_vector_runner.sh --env test1
jq '.passed' testing/results/test1/latest/qa_report.json
```

## Verified on test1 (V001_hormuz)

| Field | Value |
|-------|--------|
| Run dir | `testing/results/test1/2026-06-02T13-51-33Z` (`latest` symlink) |
| Vector | `V001_hormuz` |
| `qa_report.json` | `passed: true`, 16 checks, 0 failed (re-validated with extended gate 2026-06-02) |
| Topic state | `reported` |

Re-run gate after deploy without a full vector:

```bash
scripts/qa_check_run.sh --run-dir testing/results/test1/latest
```

## Acceptance criteria

- [x] Unit-test scope documented and runnable in CI (`tests/qa/`, `testing/README.md`)
- [x] Gate passes healthy fixtures and fails injected-bad fixtures
- [x] Full V001 run on `test1` produces `qa_report.json` with `passed: true`
- [x] Known-bad regression catalog mapped to explicit failing checks
- [x] `testing/README.md` documents verification flow and references #19
- [x] Docs state: #15 = technical gate, #18 = business, #19 = execution

## Related

- `docs/specs/done/rag_full_stable_evaluation_11.md` — harness
- `docs/specs/done/pilot_ops_v1_17.md` — thin gate + runner wiring
- `docs/specs/active/business_output_evaluation_18.md` — Lane A (needs technical PASS)
- `docs/specs/done/devops_vps_test_execution_19.md` — wire `unit-tests` + `qa-gate` checks
- `testing/README.md` — [Verification flow](../../../testing/README.md#verification-flow-real-run-vs-unit-tests)
