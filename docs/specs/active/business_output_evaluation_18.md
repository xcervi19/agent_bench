# Business output evaluation — #18

**Status:** active (planned)  
**Depends on:** #11 (run harness artifacts), #15 (technical PASS), #19 (execution visibility)  
**Feeds / pairs with:** #20 (continuous monitoring evaluation), #21 (timeliness & channel instrumentation)  
**Lane:** A — *Is the result valuable for users' business decisions?*  
**Related tickets:** #11 (harness), #15 (application verification), #17 (pilot ops), #19 (DevOps test execution)

## Goal

Establish a **repeatable, phase-aware way to judge the information value** of a Newsfind run — not whether the app broke, but whether the **deliverable helps a professional user** (trader, analyst, risk desk) with their topic.

This connects engineering output to **business requirements** (`docs/specs/business_requirements/business_requirements.md`): informational advantage, actionable insight, timeliness, and trust in sources.

## Responsibility split

- **#18 (this ticket):** business usefulness judgment, the evaluator-agent program, and sign-off criteria.
- **#15:** technical correctness and PASS/FAIL mechanics.
- **#19:** where test execution/check visibility happens (CI/VPS/GitHub checks).
- **#20:** running and judging monitoring quality over real calendar time.
- **#21:** raw metrics (timeliness, channel coverage) that make several #18 dimensions measurable.

## Core question (one sentence)

*"If I were the user who asked for this topic, would I trust and use this plan and report for real decisions — and does the system keep finding what matters, fast, over time?"*

---

## What "evaluation using an AI agent" means for us

Business evaluation is performed by a **dedicated Claude agent acting as an Output Quality Curator/Evaluator** — a distinct role from the production Newsfind agent. It does **not** generate the product; it judges it.

### Evaluator agent — operating model

- **Role:** "Output Quality Curator" — a senior trading-desk research reviewer persona, given an explicit rubric and the run artifacts.
- **Invocation:** a defined command/playbook (e.g. an `evaluator` slash-command or scripted prompt) that receives **artifact paths**, not live API access, so evaluation is reproducible against a frozen run directory.
- **Inputs:** `business_output/` (primary), `evaluation.json` (hints only, never the verdict). For **P4 retrospective** monitoring evaluation (**#20**): `monitoring_timeline.json` (all news/deltas in a scheduler window), not a single `refresh_news.json`.
- **Outputs:** a **structured verdict file** per run (proposed `business_output/quality_review.json` + a short human-readable `quality_review.md`):
  - per-phase scores and rationale (see rubric below)
  - top strengths, top risks/gaps
  - `good_enough_for_pilot: yes|no|conditional`
  - explicit assumptions and what would change the verdict
- **Guardrails (hard rules for the evaluator agent):**
  - must **not** equate `tool_errors == 0` or large source counts with "good product"
  - must judge **relevance and specificity**, not volume
  - must separate *operational health* (Lane B / #15) from *information value*
  - must cite the specific artifact/source it is judging (no unsupported claims)
- **Human role:** the operator can accept, override, or annotate the agent verdict. The agent assists judgment; it does not own pilot go/no-go alone.

### Why an agent (not only a human)

- Repeatable rubric application across runs, instances (test1 vs test2), and over time.
- Scales to longitudinal monitoring where a human cannot re-read every cycle.
- Produces structured output we can trend and compare.

---

## Phase-aware evaluation model

The pipeline has distinct phases, and **each phase is a different discipline** that must be judged on its own terms.

| Phase | Pipeline stage / command | What this phase is | Primary evaluation focus |
|-------|--------------------------|--------------------|--------------------------|
| **P1 — Topic comprehension & reference quality** | `/newsfind-plan` (RAG + web seed, framing) | Did we understand the topic as a whole? | Quality of foundational understanding and reference grounding |
| **P2a — Query construction: broad understanding** | `/newsfind-plan` queries with `intent: context` | Building a wide, well-rounded picture | Coverage, angle diversity, language/region fit |
| **P2b — Query construction: latest-news hunting** | `/newsfind-plan` queries with `intent: monitoring` + `/newsfind-refresh` short-term queries | A *different* discipline: catch the newest material fast | Precision of fresh-signal targeting, trigger-term design |
| **P3 — Latest-news search effectiveness** | `/newsfind-deliver` + `/newsfind-refresh` execution | Reaching the freshest, most valuable info quickly | Speed, channel reach (incl. social), source identification & value extraction |
| **P4 — Continuous monitoring value** | scheduler + repeated `/newsfind-refresh` over a **time window** | Sustained, deduplicated, high-value updates | Retrospective: did monitoring over `[T_start, T_end]` surface genuinely new, material news? Judged from **`monitoring_timeline.json`** assembled by **#20**, not one refresh cycle |

### P1 — Topic comprehension & reference quality

At the current stage this is a **primary** focus.

Assess from `parsed.json` (`topic_restated`, `current_state`, `working_thesis`, `entities`, `scenarios`, `rag_context_refs`) and `intro.md`:

- Did the system correctly frame the topic and its real stakes?
- Are key actors/regions/entities identified (no major omissions)?
- Is the working thesis the *most actionable* hypothesis, not a generic summary?
- Is reference grounding credible — are RAG/web seed references relevant and used, or decorative?

### P2 — Query construction (two disciplines)

Evaluate the query plan in `parsed.json.queries[]` and refresh `short_term_queries[]`, judging the two intents **separately**:

- **P2a Broad/context (`intent: context`):** Do queries build genuine breadth — multiple angles, languages (native script where relevant), and source classes — to comprehend the topic?
- **P2b Latest-news (`intent: monitoring`):** Are queries engineered to catch the *newest* developments — sharp trigger terms, freshness windows (`24h|7d`), and the right channels — rather than restating background? This is judged as a distinct skill from P2a.

### P3 — Latest-news search effectiveness

This is the discipline the business cares most about for monitoring. Focus on **how well Claude leverages search systems to reach the latest, most valuable information**:

- **Speed / timeliness:** how fresh are the surfaced sources relative to publication, and how fast did we find them? (Quantified via **#21** metrics: time-to-surface, freshness distribution.)
- **Channel reach:** did we reach beyond generic aggregators into primary/official sources, specialist outlets, **social media**, and data feeds? (`source_class` distribution from `news.json`.)
- **Source identification:** did we find the right sources at all — including non-obvious or non-English ones?
- **Value extraction:** from found sources, did we extract genuinely useful signal (specific, decision-relevant), not just headlines?

### P4 — Continuous monitoring value

Judged over a series of refresh cycles (full treatment in **#20**):

- Across repeated refreshes, does the system keep finding **genuinely new and material** updates (not noise, not duplicates)?
- Does dedup (`seen_url_hashes`) hold while still catching fresh signal?
- Can we, in hindsight, mark specific historical updates as **highly valuable** and confirm they meaningfully improved understanding of the topic? (feedback loop → **#20**)

---

## Evaluation rubric (business dimensions)

Reviewer judgment, not pass/fail automation. The evaluator agent scores each and ties it to a phase.

| Dimension | What to assess | Phase |
|-----------|----------------|-------|
| **Topic fit** | Plan and report stay on the user's question; no drift | P1 |
| **Comprehension depth** | Key drivers, entities, horizons, and reference grounding are sound | P1 |
| **Query breadth** | Context queries cover the topic from enough angles/languages | P2a |
| **Fresh-signal targeting** | Monitoring queries are designed to catch the newest material | P2b |
| **Timeliness** | Sources are fresh; latest news surfaced quickly | P3 (+#21) |
| **Channel reach** | Primary/official, specialist, social, data feeds — not just aggregators | P3 (+#21) |
| **Actionability** | Findings and scenarios support decisions, not generic summary | P3 |
| **Evidence** | Sources relevant, varied publishers; citations support claims | P3 |
| **Clarity** | Intro and report readable; thesis and open questions explicit | P3 |
| **Monitoring value** | Refresh deltas surface *new* material that matters, over time | P4 (→#20) |

Store the rubric as `testing/output_evaluation_rubric.md`.

---

## How the program operates (end to end)

### Server evaluation flow (test1/test2)

1. Check technical result status from `#15` / `qa_report.json` (PASS preferred; if FAIL in informational mode, document risk explicitly).
2. Select a frozen run artifact set from VPS (`testing/results/<env>/<timestamp>/`).
3. Invoke the **evaluator agent** (curator role) with the rubric + artifact paths.
4. Agent writes `quality_review.json` + `quality_review.md` (per-phase scores, strengths, gaps, `good_enough_for_pilot`).
5. Operator reviews/annotates; verdict is stored next to run artifacts for auditability.
6. Use verdict in demo/pilot go/no-go with explicit assumptions.

Execution automation and GitHub check plumbing belong to **#19**; #18 consumes outputs. Trigger is manual/human-decided, not per-commit, and paid AI/token spend is allowed here when needed.

### Comparison & improvement loop

- Use `compare_evaluations.sh` (metrics as hints) + the agent rubric to answer *"which run is better for the user?"* across instances or over time.
- Feed learnings back into corpus, prompts, and query templates — the product improvement loop.

---

## Pilot / demo sign-off (business)

Checklist item for client-facing demos (complements #17 ops checklist):

- [ ] Rubric applied to latest `test1` full run (per-phase)
- [ ] Known weak spots documented (honest gaps)
- [ ] Demo topic and narrative aligned with assessed output
- [ ] Technical gate reference attached (`qa_report.json` from #15)

## Out of scope (belongs in Lane B — #15)

- JSON schema validation, API smoke, event sequence invariants
- Hard gates: `min_sources`, `tool_errors == 0`, `qa_report.json` PASS
- CI block on deploy
- Frontend E2E

## Out of scope (belongs elsewhere)

- CI workflow wiring, required checks, branch protection (**#19**)
- VPS runner orchestration and artifact upload plumbing (**#19**)
- Long-horizon monitoring harness + valuable-update feedback loop (**#20**)
- Timeliness/channel-coverage metric instrumentation (**#21**)

## Relationship to #11

| #11 provides | #18 uses it for |
|--------------|-----------------|
| `business_output/` | Primary material for rubric |
| `evaluation.json` | Hints (counts, dates, citations) — **not** automatic quality score |
| `compare_evaluations.sh` | Starting point for "which run wins" — human/agent finishes judgment |

## Acceptance criteria (when implemented)

- [ ] Published rubric (`testing/output_evaluation_rubric.md`) in business-facing language, organized by phase (P1–P4).
- [ ] Evaluator agent role + invocation defined (curator playbook, inputs, `quality_review.json` schema, guardrails).
- [ ] At least one completed phase-aware evaluation write-up for `V001_hormuz` on test1.
- [ ] Evaluator playbook documented in `testing/README.md` under **Business output evaluation**.
- [ ] Each business verdict references a specific technically passed run (`#15`).
- [ ] Spec clearly distinguishes the two query disciplines (P2a context vs P2b monitoring).
- [ ] Monitoring-over-time and timeliness/channel needs are linked out to #20 and #21 (no scope overlap).
- [ ] STATUS and active specs use consistent boundaries: #15 (technical), #18 (business), #19 (execution), #20 (monitoring), #21 (metrics).

## Related

- `docs/specs/done/rag_full_stable_evaluation_11.md` — harness only
- `docs/specs/active/newsfind_application_verification_15.md` — Lane B
- `docs/specs/active/devops_vps_test_execution_19.md` — execution lane
- `docs/specs/active/continuous_monitoring_evaluation_20.md` — monitoring over time
- `docs/specs/active/timeliness_channel_metrics_21.md` — timeliness & channel metrics
- `docs/specs/done/pilot_ops_v1_17.md` — pilot ops baseline
- `claude_agent_fe/.claude/commands/newsfind-plan.md`, `newsfind-deliver.md`, `newsfind-refresh.md`
- `testing/README.md` — split evaluation guides
