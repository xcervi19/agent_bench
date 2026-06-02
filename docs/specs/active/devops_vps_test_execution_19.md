# DevOps VPS test execution and GitHub checks — #19

**Status:** active (planned)  
**Depends on:** #15 (verification definitions), #13 (multi-env), #17 (pilot-ready ops baseline)  
**Lane:** DevOps execution  
**Related tickets:** #15 (technical test rules), #18 (business evaluation)

## Goal

Make test outcomes **visible and reliable first**, then enforceable later, by running defined checks on the right environments and publishing clear GitHub status checks.

This ticket defines **how tests are executed** on infrastructure (CI + VPS), not what the assertions are.

## Core question

*“Can we trust that every change is validated by repeatable unit and VPS E2E checks, with pass/fail visible in GitHub?”*

## Rollout mode (important)

This ticket is delivered in two phases:

- **Phase 1 (current): Informational mode**
  - checks run and publish results in GitHub
  - failures are visible but do **not** block merge/release
  - goal: stabilize signal quality and reduce false positives
- **Phase 2 (later): Required mode**
  - selected checks become required in branch protection
  - merge/release is blocked when required checks fail

## Scope

### 1) GitHub checks model

Introduce explicit checks with stable names:

- `unit-tests` (fast PR check)
- `verification-smoke` (optional fast run check)
- `vps-e2e-test1` (post-deploy technical verification on test slot)
- `qa-gate` (pass/fail derived from `qa_report.json`)

In both phases, `qa-gate` should report failure when `.passed == false`.  
Blocking behavior is controlled by rollout phase (informational vs required).

### 2) Execution topology

- **PR pipeline:** run unit tests and lightweight validation without billable inference.
- **Post-merge / deploy pipeline:** deploy target environment, run vector on VPS slot, run `qa_check_run.sh`, publish artifacts.
- **Nightly or scheduled (optional):** longer full-vector regression runs.

### 3) VPS runner process

For `test1` (and optionally `test2`):

1. verify environment health (`/readyz`, required env)
2. execute `scripts/test_vector_runner.sh --env test1`
3. execute `scripts/qa_check_run.sh --run-dir testing/results/test1/latest`
4. upload `evaluation.json`, `qa_report.json`, `runner.log`, and key run metadata
5. report check status back to GitHub

### 4) Visibility and auditability

- Every failed check must include a short reason and link to artifacts/logs.
- Check summary should include vector id, env, and pass/fail count.
- Release readiness must be inferable directly from GitHub checks (no manual shell-only interpretation).

### 5) Branch protection and release policy

- **Phase 1:** keep checks non-required (advisory only), document expected reaction to red checks.
- **Phase 2:** protect main branch with required checks (`unit-tests`, `qa-gate`, and any required deployment check).
- **Phase 2:** merge/release is blocked when required checks are red.
- Document override policy (who can bypass and under which incident conditions) for Phase 2.

## Out of scope

- Defining test rules/threshold semantics (owned by #15)
- Business output usefulness verdicts (owned by #18)
- New product features unrelated to testing/deployment

## Deliverables

- GitHub workflow file(s) under `.github/workflows/`
- documented check contract in `testing/README.md` and/or `docs/ops/commands.md`
- artifact retention policy for test evidence
- operational runbook for rerun and triage

## Acceptance criteria

### Phase 1 (current, informational)

- [ ] Checks appear in GitHub on PR and post-merge paths with stable names.
- [ ] `qa-gate` status is driven by `qa_report.json` and turns red reliably on failing fixtures.
- [ ] VPS e2e run on `test1` produces visible artifacts accessible from the check.
- [ ] Docs explain rerun flow, failure triage, and ownership boundaries (#15 vs #19 vs #18).
- [ ] Docs explicitly state these checks are currently advisory (non-blocking).

### Phase 2 (later, required)

- [ ] Selected checks are marked required in branch protection.
- [ ] Merge/release is blocked when required checks are red.
- [ ] Override policy is documented and approved.

## Related

- `docs/specs/active/newsfind_application_verification_15.md`
- `docs/specs/active/business_output_evaluation_18.md`
- `scripts/test_vector_runner.sh`
- `scripts/qa_check_run.sh`
- `scripts/devops/vps_setup_test_slot.sh`
- `testing/README.md`
