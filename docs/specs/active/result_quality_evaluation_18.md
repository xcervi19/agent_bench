# Result quality evaluation — information value for traders — #18

**Status:** active (planned)
**Depends on:** #11 (stable evaluation harness — produces `evaluation.json` and `business_output/`)
**Sibling ticket:** #15 (functional regression guardrails — *did we break the app?*)
**Informs:** #17 (pilot readiness), #16 (frontend), business roadmap

> This is the **sophisticated** axis. It does not ask whether the pipeline
> ran without errors (that is #15). It asks whether the artifact a paying
> trader receives is **actually worth paying for**.

## Why this is its own ticket

The previous active specs (#15, #17) mixed two very different concerns under
the word *“QA”*:

1. *Did we break the application?* — a functional regression problem with
   binary, deterministic answers. Owned by #15.
2. *Is the output information genuinely useful for the user’s business
   decisions?* — a domain / product / quality problem with rubric-based,
   partly subjective answers. **Owned by this ticket (#18).**

These need different methods, different cadences, different reviewers, and
different definitions of success. Conflating them produces a layer that is
either too soft to gate deploys (because subjective scores can’t be hard
gates) or too hard to grow (because rubric work gets blocked by CI plumbing).

#18 is where we invest in **how good is the product, really**.

## Goal

Build a repeatable evaluation of the **information value** of Newsfind
output, anchored in the business brief
(`docs/specs/business_requirements/business_requirements.md`):

> *“deliver a significant informational and competitive advantage … structured,
> timely, and highly personalized trading insights … complementary to — and
> capable of surpassing — Bloomberg or Reuters.”*

Concretely, given a stable test vector (e.g. `V001_hormuz`) and the run’s
`business_output/` + `evaluation.json`, produce a structured **quality
review** that says how well the run serves a commodity trader, where it’s
weak, and how it compares to baseline / sibling runs.

This is **not** a CI gate. It is a continuous, evolving rubric used to drive
product improvement and to qualify a build as **demo-ready** / **pilot-ready
on quality grounds** — separately from “the app didn’t crash”.

## What “information value” means here

Working definition we will refine. A run has high information value if its
output gives a domain user (trader, analyst, risk manager) at least one of:

1. **Time saved** — replaces hours of manual scanning with a structured
   briefing they would otherwise have to assemble.
2. **Better risk visibility** — surfaces participants, scenarios, downstream
   exposures they would otherwise miss or underweight.
3. **Edge / alpha hint** — names a non-obvious mechanism, second-order
   effect, or contrarian signal.
4. **Decision scaffolding** — frames the topic in a way that makes the next
   action clearer (which markets to watch, which sources to monitor, which
   counterparties matter).

Anything weaker than this — “the report is well-formed”, “there are five
sources”, “citations resolve” — is in #15’s territory.

## Evaluation dimensions

Each run is reviewed across these dimensions. Each dimension has a rubric
(0–3 or pass/weak/strong) and prose justification. The structure stabilizes
over time; the rubric text evolves with what we learn from real traders.

### 1. Topic foundation quality

Source: `business_output/intro.md`, `parsed.json`, `evaluation.json` (`plan.*`).

- Working thesis is **specific** and **falsifiable**, not generic.
- Entities / actors named are the **actually relevant** ones for the topic
  (countries, operators, regulators, instruments) — not just the obvious.
- Query plan covers the topic from **multiple angles** (geo, supply,
  regulation, finance) and **multiple languages** when warranted.
- RAG context is used where it should be — i.e. the working thesis reflects
  long-term context, not just the day’s news.

### 2. Source quality (substantive, not structural)

Source: `business_output/news.json`.

- **Primary vs secondary** mix appropriate to the topic (operator releases,
  regulator filings, primary reporting vs aggregator rewrites).
- **Recency** matches the topic’s news horizon.
- **Publisher diversity** — not collapsed to one outlet or one country’s
  press.
- **Relevance score distribution** — top sources are actually on-topic,
  not tangential.
- *Note:* the structural existence of `sources[]`, `relevance_score`,
  `source_class` is verified by #15. This dimension is about whether the
  set of sources, taken as a whole, is what a trader would actually want.

### 3. Findings — actionability

Source: `business_output/report.json` → `key_findings`,
`business_output/report.md`.

- Findings are **specific** (name entities, magnitudes, timeframes), not
  paraphrased headlines.
- Each finding ties to a **mechanism** the trader can reason about, not just
  an event description.
- Findings differentiate **fact** from **interpretation** clearly.
- Findings would survive a “so what?” challenge from a senior analyst.

### 4. Scenarios / market impact

Source: `business_output/report.json` → `scenarios`, `report.md` impact
sections.

- Scenarios are **distinct** (not minor rewordings of one base case) and
  cover plausible alternative paths.
- Probability / severity framing is internally consistent.
- Scenarios connect the topic to **downstream markets** (per business brief
  §5.3) — which contracts, which spreads, which exposures move.
- At least one scenario is **non-obvious** — adds insight beyond the
  consensus headline.

### 5. Citation evidence fit (semantic)

Source: `report.md` `[sN]` markers cross-referenced with `news.json`.

- Each cited source actually **supports the specific claim** it backs (not
  just topic-adjacent).
- Strong claims are not backed by weak / aggregator sources.
- Important claims are not **uncited**.
- *Note:* structural `[sN]` integrity (the marker resolves to a source) is
  #15. Whether the source matches the claim is here.

### 6. Alignment with user intent

Source: vector definition (`testing/vectors.json` topic / NL setup), full
business output.

- Output reflects what the user asked for — e.g. for a “Hormuz strait
  closure options to lower price” topic, downstream price impact and
  re-routing options should be covered, not just geopolitics.
- Output stays in the **trading-decision lane** (per business brief §1):
  not generic news, not pure punditry.

### 7. Refresh delta value (when refresh ran)

Source: `business_output/refresh_*.{json,md}`,
`evaluation.json` (`refresh.*`).

- Delta is **genuinely new** — not re-summarizing already-reported news.
- Delta connects to the **existing thesis** — extends, contradicts, or
  qualifies it, rather than starting fresh.
- Delta has **trader-relevant urgency framing** (what changed *for the
  position*).

## Methods

A mix, layered:

### A. Rubric review (structured, repeatable)

A reviewer (human or agent) scores each dimension above against
`testing/quality_rubric.md`. Output:

```
testing/results/<env>/<ts>/quality_review.json
testing/results/<env>/<ts>/quality_review.md
```

Where `quality_review.json` includes per-dimension scores, justifications,
and cross-links to the artifact lines / source IDs that drove the score.

### B. LLM-as-judge

Automated rubric pass using a frontier model. Prompt template lives in
`testing/quality_judge_prompt.md` and is versioned so scores are comparable
over time. The judge consumes:

- `business_output/` (the product)
- `evaluation.json` (metric context, but not used as the judgement)
- the rubric from `testing/quality_rubric.md`

Output is a `quality_review.json` of the same shape as A. We track
**agreement between human and judge** as a separate metric and tune the
prompt when divergence is high.

### C. Golden / reference comparison

For each stable vector we maintain a **reference run** at
`testing/quality_baselines/<vector_id>/reference/`. It is a hand-picked
high-quality run (or hand-edited gold report). New runs are diffed against
the reference along each dimension. This catches *quality drift* that
metric thresholds wouldn’t — for example, sources getting blander, scenarios
collapsing to one base case, findings drifting toward generic.

> Quality drift detection lives here, deliberately *not* in #15.

### D. Domain spot-check

Periodic review by a domain reader (trader / analyst). Focused on
dimensions 3, 4, 6 (actionability, scenarios, intent alignment) which are
hardest for an LLM judge to score reliably. Outputs feed back into the
rubric.

## Cross-vector / cross-instance comparison

Extends `scripts/compare_evaluations.sh` with a *quality* dimension:

- `scripts/compare_quality.sh <review_a.json> <review_b.json>` — diff per
  dimension, flag regressions vs. reference.
- Used to answer questions #11 explicitly leaves open: *“test1 and test2
  both ran clean; which produced the more useful brief?”*

## Vectors required for meaningful quality review

#11 ships one stable vector (`V001_hormuz`). Quality evaluation needs
**topic diversity** to be representative. We add (in this ticket):

- A **structural / supply** topic (already covered by V001-class)
- A **regulatory** topic (e.g. EU gas regulation change)
- A **macro / monetary** topic (e.g. central-bank impact on commodities)
- A **disruption / event** topic (e.g. hurricane / outage)

Vectors are added incrementally; each new vector ships with a hand-curated
reference run.

## Out of scope (lives in other tickets)

- Schema / structural validity of artifacts → #15
- Tool error counts, state machine, SSE/DB invariants → #15
- API up-time, deploy smoke → #15
- Cost ceilings as runaway-spend guards → #15 (cost as a *quality* signal —
  e.g. “great results per dollar” — can live here later, but not as a gate)
- Frontend rendering of report → #16
- LLM-as-judge **as a deploy gate** — explicitly *not* this ticket. Quality
  scores inform release decisions; they do not block CI.

## Artifacts (planned)

| Path | Role |
|------|------|
| `testing/quality_rubric.md` | Versioned rubric per dimension (this is the spec readers iterate on) |
| `testing/quality_judge_prompt.md` | Versioned prompt for LLM-as-judge |
| `testing/quality_baselines/<vector_id>/reference/` | Hand-curated reference run per vector |
| `scripts/quality_review_run.sh <run_dir>` | Runs LLM-as-judge against `business_output/` → `quality_review.json` |
| `scripts/compare_quality.sh <a> <b>` | Per-dimension quality diff |
| `testing/results/<env>/<ts>/quality_review.json` | Per-run structured review |
| `testing/results/<env>/<ts>/quality_review.md` | Human-readable narrative review |

## Acceptance criteria (when implemented)

- [ ] `testing/quality_rubric.md` covers all 7 dimensions, with a working
      definition of *information value* the team agrees on
- [ ] `quality_review.json` schema documented; same shape from human review
      and LLM-as-judge
- [ ] `scripts/quality_review_run.sh` produces a `quality_review.json` for a
      `business_output/` directory deterministically (same input → same
      structure; LLM scores allowed to vary, recorded as such)
- [ ] At least **one reference run per V001_hormuz** exists in
      `testing/quality_baselines/`
- [ ] One full pass of human review + LLM-as-judge on V001_hormuz, with
      agreement / divergence noted
- [ ] At least one additional vector category (regulatory / macro /
      disruption) added to `testing/vectors.json` with its own reference
      run
- [ ] `scripts/compare_quality.sh` produces a per-dimension diff usable in
      release readiness reviews
- [ ] Cross-link in `STATUS.md`, #15, and #17 documenting the split:
      *#11 = explore/compare metrics*, *#15 = functional regression*,
      **#18 = information value**

## Open questions (track here, not in code)

- How do we recruit a domain reader cadence we can sustain?
- Which frontier model do we standardize on for LLM-as-judge, and how do
  we version-pin scores so a model upgrade doesn’t silently move the bar?
- Do we want a single composite *Quality score* per run, or only
  per-dimension scores? (Default: per-dimension only; composite scores tend
  to flatten signal.)
- How do reference runs age — do we periodically re-curate, or freeze them?

## Related

- `docs/specs/business_requirements/business_requirements.md` — definition
  of product value (topic, signal, ROI for traders)
- `docs/specs/done/rag_full_stable_evaluation_11.md` — `evaluation.json`
  and two-channel output that this ticket consumes
- `docs/specs/active/newsfind_qa_automation_15.md` — sibling functional
  regression layer
- `docs/specs/active/pilot_ops_v1_17.md` — pilot readiness; consumes
  quality reviews for the *demo-safe on quality grounds* call
- `testing/README.md` — “How to evaluate results” §4 (qualitative review)
  is the seed for the rubric here
