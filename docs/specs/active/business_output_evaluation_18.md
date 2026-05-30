# Business output evaluation — #18

**Status:** active (planned)  
**Depends on:** #11 (run harness — artifacts + `evaluation.json`)  
**Lane:** A — *Is the result valuable for users’ business decisions?*  
**See also:** `docs/specs/active/00_testing_vs_evaluation.md`

## Goal

Establish a **repeatable way to judge the information value** of a Newsfind run — not whether the app broke, but whether the **deliverable helps a professional user** (trader, analyst, risk desk) with their topic.

This is the work that connects engineering output to **business requirements** (`docs/specs/business_requirements/business_requirements.md`): informational advantage, actionable insight, timeliness, trust in sources.

## Core question (one sentence)

*“If I were the user who asked for this topic, would I trust and use this plan and report for real decisions?”*

## In scope

### 1. Evaluation rubric (business dimensions)

Document criteria reviewers use — **judgment**, not pass/fail automation:

| Dimension | What to assess |
|-----------|----------------|
| **Topic fit** | Plan and report stay on the user’s question; no drift |
| **Actionability** | Findings and scenarios support decisions (not generic summary) |
| **Evidence** | Sources are relevant, recent enough, varied publishers; citations support claims |
| **Depth** | Key drivers, entities, and horizons covered per business brief pipeline |
| **Clarity** | Intro and report readable; thesis and open questions explicit |
| **Monitoring value** | Refresh delta surfaces *new* material that matters (when run includes refresh) |

Store as `testing/output_evaluation_rubric.md` (or under `docs/product/`).

### 2. Review process

- **When:** After Lane B verification PASS; before client demo; when comparing instances or releases
- **Who:** Human operator and/or evaluator agent (Claude) with rubric
- **Input:** `business_output/` (+ optional `evaluation.json` as *hints*, not verdict)
- **Output:** Short written assessment per run: strengths, gaps, “good enough for pilot Y/N”, compare winner if A vs B

### 3. Evaluator agent playbook

- Standard prompt template referencing rubric + artifact paths
- Example: compare two `report.md` / `news.json` for same vector on test1 vs test2
- **Explicit:** agent must **not** conflate tool_errors=0 with “good product”

### 4. Comparison for improvement (not regression)

- Use `compare_evaluations.sh` + qualitative review to answer: *“Which run is **better for the user**?”*
- Track trends over time on same env (quality drift, not breakage)
- Feed learnings back to corpus, prompts, query templates — **product improvement loop**

### 5. Pilot / demo sign-off (business)

Checklist item for client-facing demos (complements #17 ops checklist):

- [ ] Rubric applied to latest `test1` full run
- [ ] Known weak spots documented (honest gaps)
- [ ] Demo topic and narrative aligned with assessed output

## Out of scope (belongs in Lane B — #15)

- JSON schema validation, API smoke, event sequence invariants
- Hard gates: `min_sources`, `tool_errors == 0`, `qa_report.json` PASS
- CI block on deploy
- Frontend E2E

## Relationship to #11

| #11 provides | #18 uses it for |
|--------------|-----------------|
| `business_output/` | Primary material for rubric |
| `evaluation.json` | Hints (counts, dates, citations) — **not** automatic quality score |
| `compare_evaluations.sh` | Starting point for “which run wins” — human/agent finishes judgment |

## Acceptance criteria (when implemented)

- [ ] Published rubric with business-facing language (non-engineer readable)
- [ ] At least one completed sample evaluation write-up for `V001_hormuz` on test1
- [ ] Evaluator playbook documented in `testing/README.md` under **Business output evaluation**
- [ ] STATUS and active specs use Lane A / Lane B vocabulary consistently

## Related

- `docs/specs/done/rag_full_stable_evaluation_11.md` — harness only
- `docs/specs/active/newsfind_application_verification_15.md` — Lane B
- `docs/specs/active/pilot_ops_v1_17.md` — pilot ops (may link demo sign-off here)
- `testing/README.md` — split evaluation guides
