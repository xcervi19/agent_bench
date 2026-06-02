# Development Status

_Update this file as work progresses. The agent reads it every session to understand current context._

---

## In Progress

### Backend V1 pilot-ready (#17)
- **Spec:** `docs/specs/active/pilot_ops_v1_17.md`
- **Lane:** Ops / demo readiness (not business quality program)
- **What's done:** Core API loop on prod (plan → deliver → refresh); run harness #11; monitor/refresh v2 shipped; HTTPS demo docs updated; thin QA gate (`scripts/qa_check_run.sh`) wired into vector runner; `GET /v1/topics` added
- **What's missing:** Manual smoke execution evidence (cancel mid-run, concurrent topics, webhook delivery) and recording outcomes as works/broken
- **Next step:** Execute manual smoke suite on test1 and record Lane B outcomes; then run Lane A business sign-off flow (#18) for demo readiness

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
- **Spec:** `docs/specs/signalgather_frontend_v1_16.md`
- **What's done:** Task spec from business requirements + event-driven UX principles
- **What's missing:** App scaffold, topic list/workspace, SSE client, artifact views, monitor/delta UI, deploy to test1
- **Next step:** Blocked on #17 subtask `GET /v1/topics`; then resolve open decisions (repo path, hosting URL, auth) and implement phase 16a

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

---

## Recently Completed

| What | Date | Spec |
|---|---|---|
| **#11 RAG full stable evaluation** — vector runner, recovery, `evaluation.json` | May 27, 2026 | `docs/specs/done/rag_full_stable_evaluation_11.md` |
| **News Pipeline v2 — monitor & refresh** — `/monitor`, `/refresh`, `/deltas`, `/newsfind-refresh` | May 2026 | `apps/claude_agent/topics/refresh.py`, `testing/app_testing_scenario.md` §7 |
| **#10 RAG main corpus (highest ROI)** — download, chunk, ingest (66 docs / 3090 events) | May 22, 2026 | `docs/specs/done/rag_main_corpus_highest_roi_10.md` |
| Reproducible run artifacts + token-aware cache for `/newsfind-queries` | May 9–10, 2026 | `docs/specs/done/reproducible_artifacts_and_cache.md` |
| News pipeline v1 deployment to VPS (topic orchestrator + event stream) | May 2026 | `docs/specs/done/deployment_newsfind_pipeline_v1.md` |
| Non-root container user migration (UID 1001) | May 2026 | `docs/ops/debugging.md` |

---

## Blocked / Parked

_(nothing currently)_
