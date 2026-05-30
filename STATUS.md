# Development Status

_Update this file as work progresses. The agent reads it every session to understand current context._

---

## In Progress

### Backend V1 pilot-ready (#17)
- **Spec:** `docs/specs/active/pilot_ops_v1_17.md`
- **Lane:** Ops / demo readiness (not business quality program)
- **What's done:** Core API loop on prod (plan → deliver → refresh); run harness #11; monitor/refresh v2 shipped
- **What's missing:** Demo docs on HTTPS, thin **application verification** gate, manual smoke tests, `GET /v1/topics`
- **Next step:** Fix `testing/app_testing_scenario.md`; add `scripts/qa_check_run.sh` + wire into vector runner

### Business output evaluation (#18)
- **Spec:** `docs/specs/active/business_output_evaluation_18.md`
- **Lane:** A — *Is the deliverable valuable for users' business decisions?*
- **What's done:** Taxonomy + rubric scope defined; tied to #11 artifacts
- **What's missing:** `testing/output_evaluation_rubric.md`, sample evaluation write-up, evaluator playbook
- **Next step:** Draft rubric; run one full qualitative review on latest test1 `V001_hormuz`

### Newsfind application verification (#15)
- **Spec:** `docs/specs/active/newsfind_application_verification_15.md`
- **Lane:** B — *Did the application work? PASS/FAIL regression gate*
- **What's done:** Verification scope (schema, thresholds, event invariants, runner integration)
- **What's missing:** `scripts/qa_check_run.sh`, `testing/qa_rules.json`, `qa_report.json`, CI integration
- **Next step:** Thin gate in #17 first, then expand full #15 ruleset

**Planning anchor:** `docs/specs/active/00_testing_vs_evaluation.md`

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
