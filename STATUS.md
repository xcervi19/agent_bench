# Development Status

_Update this file as work progresses. The agent reads it every session to understand current context._

---

## In Progress

> **Three evaluation axes — keep them distinct.** *#11 (done)* describes a
> run with `evaluation.json`. *#15* is **classic functional testing** —
> *"did we break the app?"*. *#18* is **result quality evaluation** — *"is
> the output actually useful for a trader?"*. Do not collapse #15 and #18
> into a single "QA" ticket; they require different methods, cadences, and
> definitions of success.

### Backend V1 pilot-ready (#17)
- **Spec:** `docs/specs/active/pilot_ops_v1_17.md`
- **What's done:** Core API loop on prod (plan → deliver → refresh); eval harness #11; monitor/refresh v2 shipped
- **What's missing:** Demo docs on HTTPS, **thin functional gate** (subtasks 4–5, consumes #15 rules), **lightweight quality readiness sign-off** (subtask 6, consumes #18 rubric), manual smoke tests, `GET /v1/topics`
- **Next step:** Fix `testing/app_testing_scenario.md`; add `scripts/qa_check_run.sh` (functional only) + wire into vector runner

### Functional regression guardrails (#15)
- **Spec:** `docs/specs/active/newsfind_qa_automation_15.md` (filename kept for cross-refs; ticket re-scoped)
- **Role:** *"Did we break the app?"* — schema, event invariants, error counts, state machine, smoke, known engineering failures. **No content-quality claims.**
- **What's done:** Scope defined and split from quality evaluation; rules categorized as functional only
- **What's missing:** `scripts/qa_check_run.sh`, `testing/qa_rules.json`, `qa_report.json` output, CI integration
- **Next step:** Implement thin gate first in #17 (`qa_check_run.sh` + vector runner hook), then expand full #15 ruleset

### Result quality evaluation — information value for traders (#18)
- **Spec:** `docs/specs/active/result_quality_evaluation_18.md`
- **Role:** *"Is the output actually useful for a commodity trader?"* — rubric review of topic foundation, source quality, finding actionability, scenario plausibility, citation evidence fit, intent alignment, refresh delta value. Built on #11 outputs. **Not a CI gate**, a release-readiness and product-direction tool.
- **What's done:** Spec drafted with 7 evaluation dimensions, methods (rubric / LLM-as-judge / golden reference / domain spot-check), and explicit boundary against #15
- **What's missing:** `testing/quality_rubric.md`, `testing/quality_judge_prompt.md`, reference run for V001_hormuz, `scripts/quality_review_run.sh`, `scripts/compare_quality.sh`, additional vector categories
- **Next step:** Draft `testing/quality_rubric.md` (the rubric is the spec the team iterates on); produce one human review of V001_hormuz against it; then mirror with LLM-as-judge

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
