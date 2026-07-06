# Timeliness & source-channel coverage metrics — #21

**Status:** active (planned)  
**Depends on:** #11 (run harness / `evaluation.json`)  
**Lane:** Instrumentation (feeds #15, #18, #20)  
**Related tickets:** #15 (technical thresholds), #18 (business evaluation), #20 (monitoring over time)

## Why this exists (gap)

Two business-critical qualities are currently **not measurable** from our artifacts:

- **Timeliness** — "how fast did we surface the latest news?" We capture `published_at` on sources but never compute the gap between publication and discovery, nor a freshness distribution per run.
- **Channel reach** — "did we reach social media and all relevant channels, not just aggregators?" `source_class` exists in `news.json` (`primary_official|specialist_outlet|aggregator|data_feed|blog_or_newsletter|social|unknown`) but is not aggregated into a coverage metric.

Without these numbers, #18 (timeliness, channel reach dimensions) and #20 (coverage continuity) rely on eyeballing. This ticket provides the **objective signal**; judgment stays in #18/#20.

## Goal

Extend run instrumentation so every run/refresh emits **timeliness** and **channel-coverage** metrics that downstream tickets can threshold (#15) or judge (#18/#20).

## Core question

*"Can we put numbers on how fast and how broadly we found the latest information?"*

## Scope

### 1) Timeliness metrics (per run + per refresh cycle)

Derived from `news.json` sources and run timestamps:

- `freshness_distribution` — counts by freshness bucket (`<24h`, `<7d`, `<30d`, older, unknown).
- `time_to_surface` — where `published_at` is known, distribution of (run_time − published_at): median / p90.
- `dated_source_ratio` — share of sources with a usable `published_at`.
- For refresh: newest-source age per cycle, to show how current each delta is.

### 2) Channel-coverage metrics

From `source_class` across `news.json` (and refresh `news.json`):

- `source_class_distribution` — counts/shares per class.
- `channel_breadth` — number of distinct classes reached.
- `primary_vs_aggregator_ratio` — emphasis on primary/official + specialist vs generic aggregators.
- `social_present` — whether social channels contributed at all (per business interest).

### 3) Surfacing into artifacts

- Add a `timeliness` and `channels` block to `evaluation.json` (built in `scripts/test_vector_runner.sh`).
- Keep these as **descriptive metrics**; do not bake business verdicts here.
- Optionally expose the same calculators as standalone helpers reusable by #20 series analysis.

## Out of scope

- Pass/fail thresholds on these metrics (owned by **#15** if/when desired)
- Business interpretation of "fast enough" / "broad enough" (owned by **#18**)
- Monitoring-over-time series evaluation (owned by **#20**)
- Changing the production agent's search behavior (separate product work)

## Open questions

- Reference clock for `time_to_surface`: source discovery event time vs run completion time?
- How to handle missing/unreliable `published_at` without skewing medians.
- Minimum sample size before timeliness percentiles are meaningful.

## Acceptance criteria

- [ ] `evaluation.json` includes `timeliness` and `channels` blocks for full runs and refresh cycles.
- [ ] Metrics computed from existing artifacts without extra paid inference.
- [ ] Documented field definitions (what each metric means, edge cases) in `testing/README.md`.
- [ ] #15 can reference these fields for optional thresholds; #18/#20 can consume them as hints.
- [ ] Behavior verified on a real `test1` run (numbers are plausible and non-empty when data exists).

## Related

- `docs/specs/active/business_output_evaluation_18.md`
- `docs/specs/active/continuous_monitoring_evaluation_20.md`
- `docs/specs/done/newsfind_application_verification_15.md`
- `scripts/test_vector_runner.sh` (evaluation.json builder)
- `claude_agent_fe/.claude/commands/newsfind-deliver.md`, `newsfind-refresh.md`
