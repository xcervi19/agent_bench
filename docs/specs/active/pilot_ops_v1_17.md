# Backend V1 pilot-ready — #17

**Status:** in progress  
**Depends on:** #11 (stable evaluation harness), #13 (multi-env HTTPS)  
**Blocks:** #16 (frontend topic list needs `GET /v1/topics`)

## Goal

Make the existing Newsfind topic API **repeatable and demo-safe** on prod/test without new pipeline features. Close **V1 API + ops** so a client pilot can run plan → deliver → refresh without an engineer in the loop.

This is **pilot readiness**, not “100% backend forever.” The core loop already works on prod (see `testing/results/prod/2026-05-27T14-21-00Z/evaluation.json`).

## Problem

- `STATUS.md` and some docs still describe monitor/refresh as missing; they are shipped.
- `testing/app_testing_scenario.md` uses raw IP URLs instead of prod/test HTTPS.
- No hard QA gate after vector runs — regressions can slip into client demos.
- Manual smoke items (cancel, concurrent topics, webhooks) unchecked.
- `GET /v1/topics` list endpoint missing — blocks frontend home screen (#16).

## Subtasks

1. **Update STATUS.md** — Mark monitor/refresh shipped; set next step to this ticket.
2. **Fix `testing/app_testing_scenario.md`** — Prod/test HTTPS URLs; link to `scripts/test_vector_runner.sh`.
3. **Pre-demo checklist** — RAG env verify + test1 run in `testing/README.md` or `docs/ops/vps.md`.
4. **`scripts/qa_check_run.sh`** — Pass/fail on evaluation thresholds (sources, findings, citations, `tool_errors == 0`, optional cost cap).
5. **Wire QA into vector runner** — Call `qa_check_run.sh` at end of `scripts/test_vector_runner.sh`.
6. **Smoke-test edge cases** — Cancel mid-run, concurrent topics, webhook subscribe on test1; record results.
7. **`GET /v1/topics`** — List endpoint in `apps/claude_agent/topics/routes.py` for frontend topic home.

## Out of scope

- SignalGather frontend (#16) — separate ticket
- Full QA automation (#15) — only thin gate (subtasks 4–5) here
- Internal VPS scheduler — external cron + `POST /refresh` is the model
- RAG recreate bug fix — track in `STATUS.md` known bugs unless it blocks demo

## Acceptance criteria

- [ ] `scripts/test_vector_runner.sh --env test1` finishes with QA **PASS**
- [ ] Demo docs match prod HTTPS; operator needs no raw IP
- [ ] Manual smoke items checked or documented as known gaps
- [ ] `GET /v1/topics` returns topic list for FE

## Related

- `docs/specs/done/rag_full_stable_evaluation_11.md` — evaluation harness (#11)
- `docs/specs/active/newsfind_qa_automation_15.md` — full QA layer (defer)
- `docs/specs/signalgather_frontend_v1_16.md` — frontend (#16)
- `testing/README.md`, `testing/app_testing_scenario.md`
- `docs/ops/debugging.md` — RAG env workaround
