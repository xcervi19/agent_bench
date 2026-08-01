# Evaluation baselines

Frozen runs to compare future output against, using Lane A
(`libs/eval_framework`, #23) in relative mode.

`testing/results/` is gitignored, so a run left there is machine-local. These are
committed on purpose: a baseline nobody else can see is not a baseline.

## Comparing

```bash
scripts/evaluate_output.sh relative \
  --baseline  testing/baselines/hormuz_90d_2026-08-01 \
  --candidate testing/results/prod/latest
```

Prints Better / Equal / Worse per layer and writes `quality_review.json` next to
the candidate. Aggregate many of those into win rates:

```bash
scripts/evaluate_output.sh aggregate testing/results/*/*/comparison.json
```

## What makes a comparison valid

**The input must match.** Each baseline pins the exact brief in `topic.txt`.
Running a *different* topic and comparing scores measures the topic, not the
system — a broad brief will out-score a narrow one on entity discovery no matter
what changed in the pipeline. Re-run `topic.txt` verbatim.

**The evaluator must match.** `baseline.json` records the framework commit the
scores came from. The heuristic evaluator is deterministic, so identical
artifacts always give identical scores — but a rubric or scorer change moves
every number. If `framework_commit` differs from HEAD, re-score the baseline
before comparing rather than trusting the stored figure:

```bash
scripts/evaluate_output.sh absolute --run-dir testing/baselines/<id>
```

**The heuristic is a floor, not a verdict.** It counts measurable structure. It
cannot tell you whether a claim is true. `--evaluator llm` adds judgment and
needs `OPENAI_API_KEY`.

## Baselines

### `hormuz_90d_2026-08-01`

First prod run scored end to end after #38, #39 and #16b were all live.

| | |
|---|---|
| Overall | **3.84 / 5 (77/100)** |
| Information Discovery (40%) | 2.90 |
| Research Quality (30%) | 4.59 |
| Trading Intelligence (30%) | 4.36 |

Known weaknesses this baseline deliberately captures, so an improvement shows up
as a real delta rather than noise:

- **`primary_source_discovery` 1.75/5** — 7 of 28 sources primary/official.
  #39 stopped the freshness filter deleting primaries; it did not create more.
  Whitelist coverage for maritime/insurance primaries is the open lever.
- **`information_latency` 0.0/5** — median source age 1335 h (~55 days). Not
  caused by #39's `standing` sources: excluding them the median is still 987 h.
  For a brief asking about "current state", this is the biggest single gap.
- **`information_edge` 3.24/5** — multilingual component 2.5.

Research Quality and Trading Intelligence are already strong: the agent reasons
well over what it finds, and what it finds is the problem.
