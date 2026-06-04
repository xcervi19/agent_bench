# DevOps VPS test execution and GitHub checks — #19

**Status:** done (2026-06-02, Phase 1)  
**Depends on:** #15 (verification definitions), #13 (multi-env), #17 (pilot-ready ops)  
**Feeds:** repeatable CI visibility for Lane B; unblocks confident use of #18 on fresh runs  
**Lane:** DevOps execution

## Goal / Problem

Make test outcomes **visible and reliable** on GitHub and VPS before making them merge-blocking. #15 defined rules; this ticket wires **where and how** they run.

## Solution / What was delivered (Phase 1)

| Deliverable | Path |
|-------------|------|
| PR workflow | `.github/workflows/pr-verification.yml` |
| VPS E2E workflow | `.github/workflows/vps-e2e-test1.yml` |
| Secrets / ops guide | `.github/README.md` |
| PR smoke script | `scripts/devops/ci_verification_smoke.sh` |
| VPS E2E (on host) | `scripts/devops/ci_vps_e2e_test1.sh` |
| VPS E2E (SSH driver) | `scripts/devops/ci_run_vps_e2e_ssh.sh` |
| Env writer (CI) | `scripts/devops/ci_write_test1_env.sh` |
| Artifact fetch | `scripts/devops/ci_fetch_test1_artifacts.sh` |
| Docs | `testing/README.md` (GitHub CI), `docs/ops/commands.md` |

### Stable GitHub check names

| Check | When |
|-------|------|
| `unit-tests` | Every PR — `pytest tests/qa` |
| `verification-smoke` | Every PR — fixture PASS + injected FAIL |
| `qa-gate` | PR — gate on `testing/fixtures/good_run`; VPS job — live `qa_report.json` |
| `vps-e2e-test1` | **Manual only** (`workflow_dispatch`) — SSH sync + vector on test1 |

Phase 1: `continue-on-error: true` on VPS jobs → **advisory** (documented; not branch-protection required).

### VPS process (SSH)

1. Sync `scripts/`, `testing/qa_rules.json`, `fixtures/`, `vectors.json` to `~/agent_bench_test1`
2. `git pull` optional ref on worktree
3. Write `testing/.env.test1` from secrets
4. `scripts/test_vector_runner.sh --env test1`
5. Gate via runner → `qa_report.json`
6. `scp` artifacts back → GitHub upload (14-day retention)

**Validated:** fixture gate PASS on VPS via SSH (`qa_check_run.sh` on `testing/fixtures/good_run`).

## Usage

### One-time GitHub setup

Add repository secrets per `.github/README.md`: `VPS_SSH_PRIVATE_KEY`, `TEST1_API`, `TEST1_CLAUDE_AGENT_API_KEY`.

### Local

```bash
python -m pytest tests/qa -q
bash scripts/devops/ci_verification_smoke.sh
export TEST1_API=… TEST1_CLAUDE_AGENT_API_KEY=…
bash scripts/devops/ci_run_vps_e2e_ssh.sh
```

### Rerun / triage

| Symptom | Owner | Action |
|---------|-------|--------|
| `unit-tests` red | #15 | Fix gate/rules/tests |
| `verification-smoke` red | #15 | Fixture or smoke script |
| `vps-e2e-test1` red | Ops / app | Download artifact; SSH logs; re-run workflow |
| Report “bad” but CI green | #18 | Business rubric, not `qa-gate` |

## Acceptance criteria

### Phase 1 (done)

- [x] Checks on PR and post-merge paths with stable names
- [x] `qa-gate` driven by `qa_report.json` (fixture on PR; live on VPS workflow)
- [x] VPS E2E produces uploadable artifacts (workflow + `ci_fetch_test1_artifacts.sh`)
- [x] Docs: rerun, triage, #15 vs #19 vs #18, advisory mode
- [x] SSH path verified (fixture gate on VPS)

### Phase 2 (later — not done)

- [ ] Required checks in branch protection
- [ ] Merge blocked on red required checks
- [ ] Documented override policy

## Related

- `docs/specs/done/newsfind_application_verification_15.md`
- `docs/specs/active/business_output_evaluation_18.md`
- `.github/workflows/`, `.github/README.md`
- `scripts/devops/vps_setup_test_slot.sh`
