# GitHub Actions (ticket #19)

Phase 1 checks are **advisory** — visible on PRs and after merge, not required in branch protection until Phase 2.

## Workflows

| Workflow | Triggers | Checks |
|----------|----------|--------|
| `pr-verification.yml` | PR, push to `main` | `unit-tests`, `verification-smoke`, `qa-gate` (fixture) |
| `vps-e2e-test1.yml` | **manual only** (`workflow_dispatch`) | `vps-e2e-test1`, `qa-gate` (live `test1`) |

## Repository secrets (VPS E2E)

| Secret | Example / notes |
|--------|-----------------|
| `VPS_SSH_PRIVATE_KEY` | PEM for `root@79.143.179.212` (same key as `~/.ssh/contabo_ed25519` locally) |
| `TEST1_API` | `https://agent-test1.particletico.com` |
| `TEST1_CLAUDE_AGENT_API_KEY` | From `testing/.env.test1` (never commit) |

## Optional repository variables

| Variable | Default |
|----------|---------|
| `VPS_HOST` | `root@79.143.179.212` |
| `VPS_REPO_DIR` | `/root/agent_bench_test1` |

## Local equivalents

```bash
# PR checks (no secrets)
python -m pytest tests/qa -q
bash scripts/devops/ci_verification_smoke.sh

# Full VPS E2E (needs .env.test1 values exported)
export TEST1_API=https://agent-test1.particletico.com
export TEST1_CLAUDE_AGENT_API_KEY=...
bash scripts/devops/ci_run_vps_e2e_ssh.sh
```

## Artifact retention

VPS E2E uploads `test1-e2e-<run_id>` for **14 days** (`evaluation.json`, `qa_report.json`, `runner.log`, …).

## Ownership

- **#15** — rule definitions and `qa_check_run.sh` semantics
- **#19** — CI/VPS execution and GitHub visibility (this folder)
- **#18** — business output evaluation (not run in CI here)
