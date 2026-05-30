# Backend V1 pilot-ready — #17

**Status:** in progress  
**Depends on:** #11 (stable run harness), #13 (multi-env HTTPS)  
**Blocks:** #16 (frontend topic list needs `GET /v1/topics`)

## Goal

Make the existing Newsfind topic API **repeatable and demo-safe** on prod/test without new pipeline features. Close **V1 API + ops** so a client pilot can run plan → deliver → refresh without an engineer in the loop.

This is **pilot readiness** (operations and API surface), not the full **business evaluation program** (#18) or full **verification suite** (#15).

## Problem

- `STATUS.md` and some docs still describe monitor/refresh as missing; they are shipped.
- `testing/app_testing_scenario.md` uses raw IP URLs instead of prod/test HTTPS.
- No automated **application verification** hook after vector runs — mechanical regressions can slip into client demos.
- Manual smoke items (cancel, concurrent topics, webhooks) unchecked.
- `GET /v1/topics` list endpoint missing — blocks frontend home screen (#16).

## Subtasks

### Ops & documentation

1. **Update STATUS.md** — Mark monitor/refresh shipped; set next step to this ticket.
2. **Fix `testing/app_testing_scenario.md`** — Prod/test HTTPS URLs; link to `scripts/test_vector_runner.sh`.
3. **Pre-demo checklist** — RAG env verify + test1 run in `testing/README.md` or `docs/ops/vps.md`.

### Application verification (thin — full rules in #15)

4. **`scripts/qa_check_run.sh` (minimal)** — PASS/FAIL on mechanical checks: `tool_errors == 0`, required artifacts present, basic thresholds (sources, findings, citations).
5. **Wire into vector runner** — Call `qa_check_run.sh` at end of `scripts/test_vector_runner.sh`.

*Business “is this report good enough for the client?” → **#18**, not this ticket.*

### API & manual smoke

6. **Smoke-test edge cases** — Cancel mid-run, concurrent topics, webhook subscribe on test1; record results in Lane B terms (works / broken).
7. **`GET /v1/topics`** — List endpoint in `apps/claude_agent/topics/routes.py` for frontend topic home.

## Out of scope

- SignalGather frontend (#16) — separate ticket
- Full verification ruleset, baselines, CI — **#15**
- Rubric, evaluator playbooks, business sign-off — **#18**
- Internal VPS scheduler — external cron + `POST /refresh` is the model
- RAG recreate bug fix — track in `STATUS.md` known bugs unless it blocks demo

## Acceptance criteria

- [ ] `scripts/test_vector_runner.sh --env test1` finishes with verification **PASS** (`qa_report.json` or equivalent)
- [ ] Demo docs match prod HTTPS; operator needs no raw IP
- [ ] Manual smoke items checked or documented as known gaps
- [ ] `GET /v1/topics` returns topic list for FE
- [ ] Demo ops checklist references #18 for business sign-off when needed

## Related

- `docs/specs/done/rag_full_stable_evaluation_11.md` — harness (#11)
- `docs/specs/active/newsfind_application_verification_15.md` — full verification (#15)
- `docs/specs/active/business_output_evaluation_18.md` — business judgment (#18)
- `docs/specs/signalgather_frontend_v1_16.md` — frontend (#16)
- `testing/README.md`, `testing/app_testing_scenario.md`
