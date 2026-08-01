# Multi-run, multi-topic evaluation baseline — #41

**Status:** planned
**Lane:** A — *is the deliverable valuable?* (methodology for #23)
**Depends on:** #23 (eval framework), #11 (harness + vectors)
**Blocks:** any credible "did this change improve the product?" claim
**Relates to:** #39 (source authority — its effect cannot currently be measured), #18, #20

## Goal

Make Lane A evaluation able to distinguish a real improvement from run-to-run
noise, by scoring **many runs across many topics** instead of one run of one
topic.

## Problem

`testing/baselines/hormuz_90d_2026-08-01` is a single prod run of a single brief,
frozen on 2026-08-01 and scored 3.84/5. It cannot support the claim it was
created to support.

The pipeline performs **live web search**. Re-running the same `topic.txt`
tomorrow returns different publishers, different publication dates and different
relevance scores. The baseline captured one sample and no estimate of the spread
around it, so a future delta of ±0.3 cannot be attributed: it may be the code, it
may be the news cycle. **The variance has never been measured, so no threshold
for "better" exists.**

### The noise sits in the heaviest-weighted layer

Splitting the 14 rubric categories by what they actually read:

| Layer (weight) | Determined by the pipeline | Determined by what the web held that day |
|---|---|---|
| Information Discovery (**0.40**) | source_authority_assessment | primary_source_discovery, **information_latency**, source_coverage, non_obvious_source_discovery |
| Research Quality (0.30) | entity_discovery, relationship_discovery, causal_reasoning, research_depth | signal_to_noise |
| Trading Intelligence (0.30) | actionability, potential_market_impact | market_relevance, information_edge |

Four of the five categories carrying 40 % of the weight move with the news cycle
rather than with the code. Structural categories — those counting entities,
scenarios, findings and citation structure — are reproducible; discovery
categories are not.

### `information_latency` is worse than volatile, it is time-coupled

It scores median source age **relative to run time**. The identical set of
sources scores lower simply for being evaluated later, so every future candidate
is penalised for existing after the baseline. As written it cannot be compared
across dates at all.

### A single topic cannot generalise

One brief on one subject. A change that improves grounding for, say, Chinese
industrial demand would not register. Conversely a topic-specific quirk reads as
a system-wide result.

## Scope

### 1) Measure the noise floor

Run one brief **N times** (N ≥ 3) unchanged, score each, and record per-category
median and spread. That spread is the threshold below which a delta means
nothing. Without it every comparison is unfalsifiable.

### 2) Baseline as a set, not a run

A baseline becomes **M topics × N runs**, seeded from `testing/vectors.json`
rather than one ad-hoc brief. Topics should span domains — not three variations
of Hormuz — so a domain-specific regression is visible.

### 3) Compare by win rate, not by delta

`eval_framework aggregate` already exists for this and is unused. Win rate over
many paired comparisons is robust to any single run's luck in a way a
score difference is not. Relative mode stays for inspecting one pair.

### 4) Decide what to do with the time-coupled categories

Options, to be chosen at kickoff:

- exclude `information_latency` from cross-date comparison;
- normalise source age against the run date rather than absolute hours;
- score it only within a run set, never across sets.

Doing nothing means every future run scores worse for free.

### 5) Report structural and discovery quality separately

A single blended number hides that one half is reproducible and the other is
not. A verdict should state both, and the confidence attached to each.

### 6) Automate the run → `business_output/` path for prod runs

The 2026-08-01 baseline was assembled by hand. `test_vector_runner.sh` produces
the harness layout; nothing writes a **prod** run into
`testing/results/prod/<timestamp>/`. Until that exists, every evaluation repeats
manual work and invites inconsistency.

## Acceptance criteria

- [ ] Per-category noise floor published from N ≥ 3 repeat runs of one brief
- [ ] Baseline set covers M ≥ 3 topics across at least two domains
- [ ] `aggregate` produces a win-rate verdict over the set
- [ ] A documented rule for when a delta counts as an improvement, expressed against the measured spread
- [ ] `information_latency` handled per §4, with the choice recorded
- [ ] Structural and discovery quality reported separately
- [ ] A prod run lands in `testing/results/prod/<timestamp>/` without hand-assembly
- [ ] `testing/baselines/README.md` updated; the single-run baseline demoted to a reference sample

## Out of scope

- Changing the rubric weights or categories (#23 owns the rubric)
- The LLM judge (`--evaluator llm`) — orthogonal; it has the same variance problem
- Improving the scores. This ticket measures; #39 and whitelist coverage move.

## Cost note

Each run is a full plan + deliver cycle: ~14 min and roughly $3.40 reported
equivalent on the shared Claude subscription. A 3-topic × 3-run baseline is
~9 runs, ~2 h wall clock. Budget it deliberately; there is no spend cap in the
app.

## Related

- `libs/eval_framework/` — framework; `aggregate` mode already implemented
- `testing/baselines/README.md`, `testing/baselines/hormuz_90d_2026-08-01/`
- `testing/vectors.json` — existing vector concept to build the set from
- `docs/specs/active/trading_intelligence_evaluation_23.md`
- `docs/specs/active/source_authority_enforcement_39.md` — the change whose
  effect this ticket would let us actually measure
