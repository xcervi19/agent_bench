# Backend V1 pilot-ready — #17

**Status:** in progress
**Depends on:** #11 (stable evaluation harness), #13 (multi-env HTTPS)
**Blocks:** #16 (frontend topic list needs `GET /v1/topics`)
**Related siblings:** #15 (functional regression guardrails), #18 (result quality evaluation)

## Goal

Make the existing Newsfind topic API **repeatable and demo-safe** on
prod/test without new pipeline features. Close **V1 API + ops** so a client
pilot can run plan → deliver → refresh without an engineer in the loop.

This is **pilot readiness**, not “100% backend forever.” The core loop
already works on prod (see
`testing/results/prod/2026-05-27T14-21-00Z/evaluation.json`).

## How this ticket relates to the QA / quality split

Pilot readiness has two distinct meanings, and this ticket needs both:

| Aspect | Question | Owner |
|--------|----------|-------|
| **Functional pilot-ready** | *Will the system run end-to-end without breaking, with deterministic gates we can re-run on every deploy?* | This ticket consumes the **thin functional gate** from #15 |
| **Quality pilot-ready** | *Is the output good enough that we are willing to put it in front of a paying trader?* | This ticket consumes a **quality readiness sign-off** from #18 |

Previously this spec embedded content thresholds (`min_sources`,
`min_findings`, `min_citations`) into the “thin QA gate” subtask. That mixed
the two questions. We now keep the subtasks clean: the gate enforced here is
**functional only**; content-quality readiness is a separate sign-off based
on #18’s rubric review.

## Problem

- `STATUS.md` and some docs still describe monitor/refresh as missing; they
  are shipped.
- `testing/app_testing_scenario.md` uses raw IP URLs instead of prod/test
  HTTPS.
- No **functional** gate after vector runs — engineering regressions can
  slip into client demos.
- No **quality** sign-off step before a client demo — even a clean run might
  produce a thin report and we wouldn’t catch it before a pilot meeting.
- Manual smoke items (cancel, concurrent topics, webhooks) unchecked.
- `GET /v1/topics` list endpoint missing — blocks frontend home screen
  (#16).

## Subtasks

1. **Update STATUS.md** — Mark monitor/refresh shipped; reflect the
   #15 / #17 / #18 split; set next step to this ticket.
2. **Fix `testing/app_testing_scenario.md`** — Prod/test HTTPS URLs; link to
   `scripts/test_vector_runner.sh`.
3. **Pre-demo checklist** — RAG env verify + test1 run in `testing/README.md`
   or `docs/ops/vps.md`. Checklist must clearly separate the
   *functional sign-off* step from the *quality sign-off* step.
4. **`scripts/qa_check_run.sh` — thin functional gate** — Pass/fail on
   **engineering invariants only**, taken from #15’s rule set:
   - Schema validity of `parsed.json`, `news.json`, `report.json`,
     `report.md`
   - Structural citation integrity (`[sN]` markers resolve)
   - `events.tool_errors == 0`
   - State machine reaches `reported` (or expected terminal state)
   - Cost ceiling (operational runaway guard, not a quality signal)
   - **Explicitly out of this gate:** `min_sources`, `min_findings`,
     `min_scenarios`, `unique_citations >= N`, `sources_avg_relevance >= X`,
     “sources newer than Y”, etc. — those move to #18.
5. **Wire functional gate into vector runner** — Call `qa_check_run.sh` at
   end of `scripts/test_vector_runner.sh`; non-zero exit blocks the run
   from being considered green.
6. **Quality readiness sign-off (lightweight in #17)** — Before declaring a
   build pilot-ready, run the V001 vector and produce a #18-style
   `quality_review.json` (human or LLM-as-judge using the rubric draft from
   #18). Record it alongside `qa_report.json`. This is **not a hard gate**
   in CI; it is a **release-readiness checklist item** for client demos.
   Full automation lives in #18.
7. **Smoke-test edge cases** — Cancel mid-run, concurrent topics, webhook
   subscribe on test1; record results.
8. **`GET /v1/topics`** — List endpoint in
   `apps/claude_agent/topics/routes.py` for frontend topic home.

## Out of scope

- SignalGather frontend (#16) — separate ticket
- Full functional regression layer (#15) — only the **thin functional gate**
  (subtasks 4–5) here
- Full result-quality evaluation (#18) — only the **lightweight readiness
  sign-off** (subtask 6) here
- Internal VPS scheduler — external cron + `POST /refresh` is the model
- RAG recreate bug fix — track in `STATUS.md` known bugs unless it blocks
  demo

## Acceptance criteria

- [ ] `scripts/test_vector_runner.sh --env test1` finishes with **functional
      gate PASS** (no schema / event / error / state-machine regressions)
- [ ] Demo docs match prod HTTPS; operator needs no raw IP
- [ ] Pre-demo checklist clearly separates functional sign-off (subtask 5)
      from quality sign-off (subtask 6)
- [ ] At least one `quality_review.json` exists for the build that goes to
      pilot, written against #18’s rubric draft, and reviewed by an owner
- [ ] Manual smoke items checked or documented as known gaps
- [ ] `GET /v1/topics` returns topic list for FE
- [ ] `STATUS.md` reflects the #15 / #17 / #18 three-way split

## Related

- `docs/specs/done/rag_full_stable_evaluation_11.md` — evaluation harness
  (#11)
- `docs/specs/active/newsfind_qa_automation_15.md` — full functional
  regression layer (this ticket only consumes the thin gate)
- `docs/specs/active/result_quality_evaluation_18.md` — full information-
  value evaluation (this ticket only consumes a lightweight readiness
  sign-off)
- `docs/specs/signalgather_frontend_v1_16.md` — frontend (#16)
- `testing/README.md`, `testing/app_testing_scenario.md`
- `docs/ops/debugging.md` — RAG env workaround
