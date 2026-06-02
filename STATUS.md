# Development Status

_Update this file as work progresses. The agent reads it every session to understand current context._

**Ticket numbers:** `docs/specs/TICKET_REGISTRY.md` (next: **#23**).  
**How to create / prioritize tickets:** `AGENT.md` → Creating a new ticket, Build queue.

---

## Build queue (prioritized)

_Order for completing the **shipped V1 application** (Newsfind + UI + eval). Recompute with **technical-architect** when scope or business priority changes; ticket `#` is an ID, not priority._

| Order | Ticket | Why now | Unblocks |
|------|--------|---------|----------|
| 1 | **#15** Application verification | Technical PASS/FAIL gate before trusting demos and business sign-off | #18, #19 |
| 2 | **#19** DevOps test execution (advisory first) | Makes #15 checks visible on VPS/CI without blocking merges yet | Team confidence in regressions |
| 3 | **#22** Topic refresh scheduler | Automatic monitoring cadence — product expectation for pilot | #16 (16c), #20 |
| 4 | **#16** SignalGather frontend V1 | User-facing surface on shipped API (#17) | Pilot demos without curl |
| 5 | **#21** Timeliness & channel metrics | Measurable inputs for eval lanes | #18, #20 (richer verdicts) |
| 6 | **#18** Business output evaluation | Lane A — is the deliverable decision-useful? | Pilot go/no-go narrative |
| 7 | **#20** Continuous monitoring evaluation | Lane A over time — needs scheduler + rubric | Longitudinal product proof |

**Suggested next pick:** **#15** (finish rule mapping + `qa_rules.json`, then hand runner wiring to #19).

**Parallel (when deps met):** #21 after harness artifacts (#11); #16 phase **16a** (topic list) anytime after #17; do not start #20 until **#22** + **#18** rubric exist.

**Dependency sketch:**

```
#11,#13,#17 (done) ──► #15 ──► #19
                    └──► #22 ──► #16 (16c)
                    └──► #21 ──┐
#15 PASS ─────────────────────► #18 ──► #20
#22 + #18 + #21 ───────────────────────────► #20
```

---

## In Progress

### Business output evaluation (#18)
- **Spec:** `docs/specs/active/business_output_evaluation_18.md`
- **Lane:** A — *Is the deliverable valuable for users' business decisions?*
- **What's done:** Evaluator-agent (Output Quality Curator) role defined; phase-aware rubric (P1 comprehension, P2a/P2b query disciplines, P3 latest-news effectiveness, P4 monitoring value); server evaluation flow
- **What's missing:** `testing/output_evaluation_rubric.md`, `quality_review.json` schema + evaluator playbook, one phase-aware write-up on test1
- **Next step:** Publish rubric + curator playbook; run one evaluated test1 run referencing technical PASS from #15

### Continuous monitoring evaluation & valuable-update feedback (#20)
- **Spec:** `docs/specs/active/continuous_monitoring_evaluation_20.md`
- **Lane:** A — *monitoring-over-time variant of #18*
- **What's done:** Gap framed; two modes (A: `/refresh` smoke, B: scheduler window + timeline + retrospective P4); `monitoring_timeline.json` + evaluator bundle specified
- **What's missing:** Timeline assembly, Mode B harness, monitoring-quality rubric, valuable-update labels, one retrospective evaluator run
- **Next step:** After #22 cadence exists, run one monitoring window on test1 → assemble timeline → P4 evaluator review

### Topic refresh scheduler (#22)
- **Spec:** `docs/specs/active/topic_refresh_scheduler_22.md`
- **Lane:** Product / backend — *automatic refresh cadence per monitored topic*
- **What's done:** Gap framed; manual `/refresh` + monitor shipped (#17); scheduler container defined but not running on VPS
- **What's missing:** Schedule fields on subscription, internal scheduler job, VPS scheduler service, harness tests for scheduled vs manual refresh
- **Next step:** Decide interval model (hours vs cron); extend `POST/PATCH /monitor`; implement scheduler job calling `run_refresh`

### Timeliness & source-channel coverage metrics (#21)
- **Spec:** `docs/specs/active/timeliness_channel_metrics_21.md`
- **Lane:** Instrumentation — *feeds #15, #18, #20*
- **What's done:** Gap framed (no time-to-surface or channel-coverage metrics today); metric definitions drafted
- **What's missing:** `timeliness`/`channels` blocks in `evaluation.json`, field docs, verification on a real run
- **Next step:** Implement metric calculators in `scripts/test_vector_runner.sh` and document fields in `testing/README.md`

### Newsfind application verification (#15)
- **Spec:** `docs/specs/active/newsfind_application_verification_15.md`
- **Lane:** B — *Technical verification definition (what to test and pass/fail criteria)*
- **What's done:** Gate model, artifact checks, thresholds, event invariants, known-bad catalog, server-process expectations defined
- **What's missing:** Explicit unit-test suite coverage and finalized `testing/qa_rules.json` mapped to all checks
- **Next step:** Complete rule mapping + fixture-based test coverage, then hand execution wiring to #19 (advisory mode first)

### DevOps VPS test execution and GitHub checks (#19)
- **Spec:** `docs/specs/active/devops_vps_test_execution_19.md`
- **Lane:** DevOps — *How tests run on CI/VPS and become enforceable in GitHub over time*
- **What's done:** Scope and phased acceptance model defined (informational mode now, required mode later)
- **What's missing:** `.github/workflows/` implementation, check publishing, artifact upload, and later branch-protection switch
- **Next step:** Implement workflows in advisory mode and stabilize signals before enabling required checks

**Execution rule:** Agents execute only `docs/specs/active/*_<n>.md` tickets. Move completed tickets to `docs/specs/done/`.

### SignalGather frontend V1 — topic intelligence UI (#16)
- **Spec:** `docs/specs/active/signalgather_frontend_v1_16.md`
- **What's done:** Task spec from business requirements + event-driven UX principles
- **What's missing:** App scaffold, topic list/workspace, SSE client, artifact views, monitor/delta UI, deploy to test1
- **Next step:** `GET /v1/topics` now shipped (#17 done); resolve open decisions (repo path, hosting URL, auth) and implement phase 16a

---

## Known Bugs

### RAG env vars dropped on container recreate
- **Symptom:** `rag_context_refs: []` + `"RAG unavailable — no .env configuration found"`
- **Cause:** `docker compose up --force-recreate` drops env injection for `claude_agent`
- **Workaround:**
  ```bash
  docker compose up -d --force-recreate claude_agent
  docker compose exec claude_agent sh -lc 'env | grep -E "^RAG_"'
  # if blank: check docker-compose.yml env_file order for claude_agent
  ```
- **Full debug steps:** `docs/ops/debugging.md` → "RAG unavailable" section

### Cancel does not abort an in-flight run
- **Symptom:** `POST /v1/topics/{id}/cancel` during planning/delivering returns `cancelled`, but the topic later reappears at `planned_awaiting_review`/`reported`.
- **Cause:** the background plan/deliver task (and its Claude subprocess) is not cancelled; it runs to completion and re-sets state via `set_state`.
- **Impact:** cancel is only reliable from a gate/terminal state; mid-run cancel does not stop token spend.
- **Found:** #17 Lane B smoke (2026-06-02). Fix needs cooperative cancellation of `run_plan`/`run_deliver`.

---

## Recently Completed

| What | Date | Spec |
|---|---|---|
| **#17 Backend V1 pilot-ready** — `GET /v1/topics` deployed; vector run QA PASS on test1; Lane B smoke (concurrent ✅, webhook+HMAC ✅, cancel mid-run ⚠️ gap); 2 harness bugs fixed | Jun 2, 2026 | `docs/specs/done/pilot_ops_v1_17.md` |
| **#11 RAG full stable evaluation** — vector runner, recovery, `evaluation.json` | May 27, 2026 | `docs/specs/done/rag_full_stable_evaluation_11.md` |
| **News Pipeline v2 — monitor & refresh** — `/monitor`, `/refresh`, `/deltas`, `/newsfind-refresh` | May 2026 | `apps/claude_agent/topics/refresh.py`, `testing/app_testing_scenario.md` §7 |
| **#10 RAG main corpus (highest ROI)** — download, chunk, ingest (66 docs / 3090 events) | May 22, 2026 | `docs/specs/done/rag_main_corpus_highest_roi_10.md` |
| Reproducible run artifacts + token-aware cache for `/newsfind-queries` | May 9–10, 2026 | `docs/specs/done/reproducible_artifacts_and_cache.md` |
| News pipeline v1 deployment to VPS (topic orchestrator + event stream) | May 2026 | `docs/specs/done/deployment_newsfind_pipeline_v1.md` |
| Non-root container user migration (UID 1001) | May 2026 | `docs/ops/debugging.md` |

---

## Blocked / Parked

_(nothing currently)_
