# Planning: two lanes for “checking a run”

**Purpose:** One shared runner (#11) produces artifacts. After that, we treat **two different questions** as separate work — separate tickets, separate acceptance, separate language in docs.

---

## Lane A — Business output evaluation

**Question:** *Is this result actually useful for our users’ business?*

Does the plan, report, sources, and refresh delta give a trader or analyst **real informational advantage** — something they could act on or trust for decisions?

| Aspect | What it is |
|--------|------------|
| **Focus** | Meaning and value of the **product output** (intro, queries, sources, findings, scenarios, report narrative) |
| **Success** | “This run is **better / good enough** for the business” (judgment, comparison, improvement) |
| **Methods** | Human review, evaluator-agent rubric, side-by-side run comparison on **content**, periodic quality reviews |
| **Not** | Deploy gate, schema validation, “did the API return 200” |

**Ticket:** `#18` — `business_output_evaluation_18.md`  
**Builds on:** `#11` harness (`business_output/`, `evaluation.json` as *signals*, not as pass/fail)

---

## Lane B — Application verification (classic testing)

**Question:** *Did the application still work correctly? Did we break something we already know how to detect?*

Did the pipeline finish, artifacts exist and match contracts, events look healthy, and known failure modes from ops are absent?

| Aspect | What it is |
|--------|------------|
| **Focus** | **Correctness and stability** of the system — pipeline, API, artifacts, events |
| **Success** | **PASS / FAIL** — safe to demo, deploy, or merge |
| **Methods** | Schema checks, state-machine invariants, smoke vectors, threshold gates, `qa_report.json`, CI block |
| **Not** | “Is this report insightful for Hormuz?” (that is Lane A) |

**Ticket:** `#15` — `newsfind_application_verification_15.md` (renamed from “QA automation”)  
**Thin gate for pilot:** subset wired from `#17` until `#15` is full

---

## Shared foundation (done)

**Ticket `#11`:** Recoverable full run + two channels + `evaluation.json` + compare script.

- **Does not** answer either lane by itself — it **feeds** both.
- Rename mentally: “evaluation harness” = **capture & compare infrastructure**, not “business quality sign-off.”

---

## How current active tickets map

| Ticket | Lane | Role |
|--------|------|------|
| **#11** (done) | Both | Run once, store artifacts + metrics |
| **#18** (new) | A | Rubric, review process, evaluator playbooks, “which run is better for the user” |
| **#15** | B | Automated verification, regression catalog, CI gate |
| **#17** | Ops | Pilot-ready API/docs/smoke — **not** business quality program |
| **#16** | Product | Frontend — uses API verified in B, quality judged in A |

---

## Language to use in tickets and STATUS

| Avoid (ambiguous) | Prefer |
|-------------------|--------|
| “QA” alone | **Application verification** (B) or **output evaluation** (A) |
| “Quality” alone | **Business value of output** (A) vs **system works** (B) |
| “Evaluation” alone | **Business output evaluation** (A) vs **evaluation harness** (#11) |
| “Thresholds” in #11 README as quality | In B: **gates**; in A: **indicators** for review |

---

## When both run on the same artifact folder

```
test_vector_runner.sh  →  run_dir/
                              ├── business_output/     → Lane A reviews here
                              ├── agent_log/           → Lane B checks here
                              └── evaluation.json      → B: gates; A: hints for review
```

1. **Lane B first (automated):** `qa_check_run.sh` → PASS/FAIL. If FAIL, fix the app; no point in deep business review.
2. **Lane A (human/agent):** Only on PASS (or ad hoc for experiments): rubric on `report.md`, sources, findings.

---

## Related docs

- `testing/README.md` — split guides: verification vs business evaluation
- `docs/specs/active/business_output_evaluation_18.md`
- `docs/specs/active/newsfind_application_verification_15.md`
- `docs/specs/active/pilot_ops_v1_17.md`
