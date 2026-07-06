# Trading Intelligence Evaluation Framework — #23

**Status:** active (in progress — framework implemented; live write-up pending)
**Depends on:** #11 (run harness artifacts), #15 (technical PASS gate)
**Extends / generalizes:** #18 (business output evaluation, Lane A)
**Pairs with:** #20 (continuous monitoring eval), #21 (timeliness & channel metrics)
**Lane:** A — *Is the result valuable for users' business decisions?*

## Goal

A configurable, repeatable framework that measures whether new versions of the
agent produce **better intelligence outputs** and meet the bar of a professional
trading organization. It evaluates the **whole intelligence-generation process**
— information discovery, source selection, research depth, entity/relationship
extraction, reasoning, and business relevance — **not writing quality alone**.

The benchmark persona is a **senior trading analyst**, not a generic chatbot.

## Relationship to #18

#18 framed Lane A with a phase-aware model (P1–P4) and an evaluator-agent
operating model. #23 **implements** Lane A as runnable code and reorganizes the
rubric into the **three-layer / 14-category** model below (the model requested by
the business). The #18 phase concepts map onto these layers:

| #18 phase | #23 layer(s) |
|---|---|
| P1 comprehension / reference quality | Research Quality (entities, depth) + Discovery (coverage) |
| P2a/P2b query disciplines | Information Discovery (coverage, non-obvious, latency targeting) |
| P3 latest-news effectiveness | Information Discovery (latency, primary, authority) + Trading (edge) |
| P4 monitoring value | Out of scope here → #20 (longitudinal) |

#23 keeps the #18 guardrails (relevance over volume; operational health ≠ value).

## Core philosophy

The system's most important capability is **discovering, acquiring, validating,
connecting, and synthesizing information from the internet** — not text. A system
that writes well on incomplete information must score **lower** than one that
discovers superior information. Hence **Information Discovery is weighted 40%**.

## Evaluation modes

- **Mode 1 — Absolute:** score one report against the rubric. No comparison.
- **Mode 2 — Relative:** baseline vs candidate → **Better / Equal / Worse**, plus
  win-rate aggregation across many pairwise comparisons.

## Rubric (0–5 per category; weights configurable)

| Layer (default weight) | Categories |
|---|---|
| **Information Discovery (40%)** | primary_source_discovery, information_latency, source_coverage, non_obvious_source_discovery, source_authority_assessment |
| **Research Quality (30%)** | entity_discovery, relationship_discovery, causal_reasoning, research_depth, signal_to_noise |
| **Trading Intelligence (30%)** | market_relevance, actionability, potential_market_impact, information_edge |

Human-readable rubric: `testing/output_evaluation_rubric.md`.
Machine rubric: `libs/eval_framework/rubric.json`.

## Architecture

Package `libs/eval_framework/` (domain-free engine; rubric is data):

| Module | Responsibility |
|---|---|
| `rubric.py` + `rubric.json` | Layers/categories/weights; configurable, normalized at runtime |
| `artifacts.py` | Load a frozen run dir (`business_output/`, `evaluation.json`) into `RunArtifacts` |
| `scoring.py` | `CategoryScore` → `LayerScore` → `EvaluationResult`; weighted aggregation |
| `evaluators/heuristic.py` | Deterministic, offline scorer (CI anchor, pre-screen, reference) |
| `evaluators/llm.py` | LLM-as-judge "Output Quality Curator" (OpenAI; production) |
| `relative.py` | Pairwise `compare()` + `aggregate_win_rate()` |
| `benchmarks.py` | Pluggable `BenchmarkProvider` registry (agent vs external baselines) |
| `report.py` | Render `quality_review.json` + `quality_review.md` |
| `cli.py` / `__main__.py` | `absolute` / `relative` / `aggregate` / `show-rubric` |

Wrapper: `scripts/evaluate_output.sh`. Tests: `tests/eval/` (offline, non-billable).

## Outputs

Per run, next to artifacts: `quality_review.json` (per-category + per-layer +
overall, 0–5 and 0–100) and `quality_review.md`. Relative runs additionally store
the Better/Equal/Worse verdict and deltas; `aggregate` emits win-rate stats.

## Future benchmarking

Benchmark providers let the **same rubric** score: generic LLM outputs,
internet-disabled models, standard search workflows, human analyst reports,
Bloomberg-/Reuters-style reports. New providers register via
`register_provider()` / `@benchmark_provider` **without redesigning** the engine.

## Success criteria

- [x] Configurable 3-layer / 14-category rubric (0–5), weights overridable.
- [x] Absolute mode (Mode 1) writing `quality_review.{json,md}`.
- [x] Relative mode (Mode 2): Better/Equal/Worse + win-rate aggregation.
- [x] Offline deterministic evaluator + LLM-as-judge evaluator (same rubric).
- [x] Pluggable benchmark-provider abstraction (extensible, registry).
- [x] Offline test suite (`tests/eval/`, 25 tests) — discovery emphasis verified.
- [ ] One LLM-judge write-up on `test1/latest`, referencing a #15 PASS.
- [ ] Documented in `testing/README.md` (done) and adopted in pilot go/no-go.

## Out of scope (belongs elsewhere)

- Mechanical PASS/FAIL gates, schema/API checks (**#15**).
- CI/VPS execution plumbing (**#19**).
- Longitudinal monitoring-over-time evaluation (**#20**).
- Timeliness/channel metric instrumentation in `evaluation.json` (**#21**) — the
  framework consumes those metrics as hints when present.

## Related

- `docs/specs/active/business_output_evaluation_18.md`
- `docs/specs/done/rag_full_stable_evaluation_11.md`
- `docs/specs/done/newsfind_application_verification_15.md`
- `testing/output_evaluation_rubric.md`, `testing/README.md`
