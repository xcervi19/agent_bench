# Backend V1 pilot-ready — #17

**Status:** done (verified on `test1`, 2026-06-02)  
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

- [x] `scripts/test_vector_runner.sh --env test1` finishes with verification **PASS** (`qa_report.json` or equivalent)
- [x] Demo docs match prod HTTPS; operator needs no raw IP
- [x] Manual smoke items checked or documented as known gaps
- [x] `GET /v1/topics` returns topic list for FE
- [x] Demo ops checklist references #18 for business sign-off when needed

## Closure — verification 2026-06-02 (test1)

All acceptance criteria met. Evidence and how each was satisfied:

**AC1 — vector run PASS.** `scripts/test_vector_runner.sh --env test1` completed full lifecycle
plan → deliver → refresh with **QA PASS (11/11 checks, 0 failed)**. Run:
`testing/results/test1/2026-06-02T13-51-33Z/` (now `latest`).
- deliver: 25 sources / 19 publishers, 7 key findings, 10 unique citations, report 38 lines / 891 words
- refresh: 1 cycle, status `completed`, **15 new sources**, 12 queries
- events: 147 total, 66 tool calls, **0 tool errors**; cost ≈ $2.91 total
- artifacts: `qa_report.json` (`passed: true`), `evaluation.json`, `business_output/*`, `agent_log/events_full.ndjson`

  Two pre-existing harness bugs (#11) were fixed to let the run complete and grade correctly
  (see `scripts/test_vector_runner.sh`):
  1. `_events_max_seq` now parses line-by-line and skips malformed lines — a concurrent SSE
     writer could leave a partial line that made `jq -s` blank the max seq, spinning
     `sync_events_from_api` on `from_seq=0`.
  2. `evaluation.json` `sources_avg_relevance` divided by an array (`[N]`) instead of `N`,
     which crashed `NEWS_METRICS` and dropped `deliver.sources_total` → QA spuriously failed
     `sources_total_threshold`. Fixed the divisor.

**AC2 — HTTPS, no raw IP in demo flow.** `testing/app_testing_scenario.md` and `testing/README.md`
drive every API call via the HTTPS hostname (`$API=https://agent-test1.particletico.com`); the
pre-demo checklist enforces HTTPS hostnames. Raw IP appears only in optional SSH DB/log helpers
(SSH target), not the demo API flow.

**AC3 — manual smoke (Lane B, works/broken).** Executed on `test1`:
- **Concurrent topics:** ✅ 3 topics created together (all `202` → `planned_awaiting_review`),
  `/readyz` healthy throughout; `max_concurrent_jobs` held.
- **Webhook signed delivery:** ✅ `POST /subscribe` → `201`; events delivered to receiver with
  `X-Signature: sha256=…` HMAC **verified** (recomputed HMAC matched). `intro.ready`/`report.ready`
  traverse the same `emit → deliver_event` path.
- **Cancel mid-run:** ⚠️ **known gap.** `POST /cancel` is accepted and momentarily sets
  `cancelled`, but the in-flight background plan/deliver task is **not aborted** — it runs to
  completion and re-sets state (observed `state→cancelled` at seq 4, then `→planned_awaiting_review`
  at seq 34). Cancel from a gate/terminal state works and sticks. Tracked as a known bug; aborting
  the Claude subprocess mid-stream is out of scope for #17 (no new pipeline features).

**AC4 — `GET /v1/topics`.** Implemented (`list_topics` in `apps/claude_agent/topics/routes.py`),
committed to `main`, and **deployed to test1** (worktree `git pull` + `docker compose build/up
claude_agent`). Verified live: `200` with `items[]` (id, topic, state, available_actions,
created/updated_at) and `?state=` filtering. (Before deploy, test1 returned `405 allow: POST`.)

**AC5 — demo ops checklist references #18.** `testing/README.md` → "Pre-demo checklist (pilot ops)"
includes "If output quality judgment is needed … run Lane A rubric from ticket #18."

## Related

- `docs/specs/done/rag_full_stable_evaluation_11.md` — harness (#11)
- `docs/specs/done/newsfind_application_verification_15.md` — full verification (#15)
- `docs/specs/active/business_output_evaluation_18.md` — business judgment (#18)
- `docs/specs/active/signalgather_frontend_v1_16.md` — frontend (#16)
- `testing/README.md`, `testing/app_testing_scenario.md`
