# Scripts Guide

This file defines the supervised script model for the repository.

## 1) Primary testing flow (default for developers)

Use these three commands for normal validation and pilot readiness:

1. `scripts/test_vector_runner.sh --env test1`  
   Full lifecycle harness (plan -> deliver -> refresh), resumable.
2. `scripts/qa_check_run.sh --run-dir testing/results/test1/latest`  
   Mechanical PASS/FAIL gate from artifacts.
3. `scripts/compare_evaluations.sh <eval_a.json> <eval_b.json>` (optional)  
   Compare run quality/performance across environments or dates.

## 2) Script supervision matrix

### Testing (core)

- `scripts/test_vector_runner.sh` — **primary**
- `scripts/qa_check_run.sh` — **primary**
- `scripts/compare_evaluations.sh` — **primary**

### Testing (specialized debug, keep top-level)

- `scripts/test_refresh_cycle.sh` — **specialized**  
  For refresh-only troubleshooting on an existing reported topic.
- `scripts/test_newsfind.sh` — **specialized**  
  For slash-command stream debugging (`/newsfind-queries`) and SSE diagnostics.
- `scripts/utils/list_runs.sh` — **utility**  
  Quick listing of older `testing/runs` captures.

### DevOps / VPS operations

- `scripts/devops/vps_setup_test_slot.sh` — slot setup (test1/test2 worktree + compose)
- `scripts/devops/vps_deploy_caddy.sh` — Caddy deployment/reload helper
- `scripts/devops/ci_verification_smoke.sh` — PR smoke (fixture PASS/FAIL)
- `scripts/devops/ci_vps_e2e_test1.sh` — full vector + gate on VPS
- `scripts/devops/ci_run_vps_e2e_ssh.sh` — SSH driver for VPS E2E
- `scripts/devops/ci_fetch_test1_artifacts.sh` — pull `test1/latest` from VPS for CI upload

### Data / corpus processing

- `scripts/data_processing/consolidate_corpus_l1.py`
- `scripts/data_processing/corpus_l1_to_l2_text.py`

### Runtime/debug utilities

- `scripts/utils/replay_session.py`
- `scripts/utils/list_runs.sh`

### Deprecated fallback (not default path)

Located in `scripts/legacy/`:

- `test_full_pipeline.sh`
- `test_continue_topic.sh`
- `test_topic.sh`

Use legacy scripts only when you explicitly need old behavior.

## 3) Rules for adding new scripts

- If a script is part of daily validation, keep it in `scripts/` and document it in `testing/README.md`.
- If it is one-off or transitional, put it in `scripts/legacy/` or document as specialized debug.
- Do not add a second script for the same primary workflow (avoid duplicate E2E runners).
