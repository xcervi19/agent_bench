# Newsfind Evaluation Process

This evaluation layer answers a demo question that JSON-shape checks cannot:

> Is this output useful enough for a trading/NLP expert to believe the product
> can create business value?

The first-pass evaluator is deterministic and offline. It reads the artifacts
from one completed run and produces `evaluation/evaluation.json` plus
`evaluation/evaluation.md` next to the run.

## What it judges

The evaluator scores five areas, 20 points each:

1. **Plan quality** - query count, actor coverage, language coverage, source
   class diversity, scenarios, and monitoring triggers.
2. **Evidence quality** - source breadth, relevance, high-trust source share,
   date coverage, query hit rate, and evidence that filtering ran.
3. **Citation integrity** - every markdown citation maps to a source ID, key
   findings carry source IDs, and scenario updates are evidence-backed.
4. **Trading usefulness** - the report explains market mechanisms, thesis
   status, scenarios, next queries, confidence, and open questions.
5. **Artifact structure** - report sections, summary size, intro availability,
   source affordances, and enough substance for expert review.

The output verdict is:

- `demo_ready` - score >= 80 and no critical missing artifacts
- `expert_review_required` - score >= 65 but below demo-ready quality
- `not_demo_ready` - missing core artifacts or score below 65

## Run it

```bash
scripts/evaluate_newsfind_run.py testing/runs/<run-dir>
```

Compare a new candidate against an older run:

```bash
scripts/evaluate_newsfind_run.py testing/runs/<new-run> \
  --baseline-run testing/runs/<old-run>
```

Use a threshold in automation:

```bash
scripts/evaluate_newsfind_run.py testing/runs/<run-dir> --fail-under 80
```

`scripts/test_full_pipeline.sh` runs the evaluator automatically at the end of a
successful pipeline run. Set `RUN_EVALUATION=false` to skip it or
`EVAL_FAIL_UNDER=80` to make the script fail when demo quality is below the
target.

## Human review questions

The evaluator deliberately keeps a human review step. For the first demo, the
reviewer should ask:

- Does the report identify the concrete market mechanism, not just the news
  event?
- Would a trader know what to monitor next after reading the report?
- Are high-impact claims backed by primary or specialist sources?
- Are remaining blind spots explicit enough for an expert reviewer to trust the
  system?

## What this does not do yet

This is not an LLM-as-judge system and does not verify factual correctness
against external ground truth. It is a repeatable product-quality gate for run
artifacts. A later evaluation layer can add expert-labeled topics, answer keys,
or pairwise LLM judging once we have real reviewer feedback from trading/NLP
users.
