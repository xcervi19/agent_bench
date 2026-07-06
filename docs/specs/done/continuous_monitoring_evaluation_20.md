# Continuous monitoring evaluation & valuable-update feedback — #20

**Status:** active (planned)  
**Depends on:** #11 (run harness), #18 (evaluator agent + rubric), #21 (timeliness/channel metrics), **#22** (scheduler cadence for realistic windows)  
**Lane:** A (business) — *monitoring-over-time variant*  
**Related tickets:** #15 (technical verification), #18 (single-run + retrospective business evaluation), #19 (execution), #22 (periodic refresh)

## Why this exists (gap)

Today's harness runs a single cold lifecycle (plan → deliver → **one or few manual `/refresh` cycles back-to-back**). That proves the refresh **mechanism** works; it does **not** prove monitoring value over time.

We do **not** yet:

- run the scheduler (or equivalent) across **real calendar time** (hours/days/weeks) and capture every cycle,
- assemble **all news gathered in that window** into one **chronological timeline** artifact,
- hand that timeline to the **#18 evaluator agent** for **retrospective** business judgment (P4),
- mark specific historical updates as **highly valuable** and feed that signal back to the agent.

This ticket closes that gap. It covers **timeline capture + assembly**, **retrospective evaluation inputs**, and **monitoring-quality judgment** — distinct from single-shot `/refresh` smoke in #11/#15.

## Goal

Make topic monitoring **measurable and improvable over time**: run periodic refresh over a defined window, **rollup all discovered news into a timeline**, then let the evaluator agent judge **retrospective** business performance — not only “did one refresh work?”

## Core question

*"Over days and weeks, does the system keep finding the newest material that genuinely matters for this topic — and can we learn from which past updates were most valuable?"*

## Two testing / evaluation modes (both required)

| Mode | What it proves | Harness today | Owner |
|------|----------------|---------------|--------|
| **A — Refresh mechanism** | `POST /monitor` + `POST /refresh` (or one vector refresh step) completes; artifacts + SSE OK | `scripts/test_vector_runner.sh`, `scripts/test_refresh_cycle.sh` | #11 / #15 |
| **B — Monitoring over time** | Scheduler runs for window `[T_start, T_end]`; timeline assembled; evaluator judges P4 retrospectively | **Not built** — this ticket | **#20** (+ #22 for cadence) |

Mode A stays. Mode B is the missing product/evaluation capability.

## Scope

### 1) Longitudinal refresh capture

- Run periodic refresh for a monitored topic over a configured window (**#22** scheduler preferred; manual/cron triggers acceptable until #22 ships).
- Persist **each cycle** as today: `delta.json`, `news.json`, `summary.json`, `report.md` per `TopicRefreshDelta` / run dir.
- Preserve dedup integrity across cycles (`seen_url_hashes`) while confirming fresh signal still gets through.

### 2) Monitoring timeline (rollup artifact)

After the window ends (or on demand), **assemble one retrospective bundle** from all cycles in range:

- **`monitoring_timeline.json`** (proposed name) — ordered list of entries, each linking:
  - cycle metadata (`seq`, `run_id`, `started_at`, `completed_at`, `trigger`: `scheduled|manual`)
  - new sources from that cycle (`news.json` subset or refs)
  - delta summary (`delta.json` / `summary.json` highlights)
  - optional per-cycle `report.md` excerpt
- **Deduplicated source index** across the window (canonical `url_hash`, first_seen_at, contributing cycles).
- **Window metadata**: `topic_id`, `T_start`, `T_end`, `schedule_interval_hours`, `cycles_total`, `cycles_with_new_material`.

Storage: under `testing/results/<env>/<monitoring_run_id>/` for evaluation runs, and/or API `GET /v1/topics/{id}/monitoring/timeline?from=&to=` for product/FE later.

Purpose: one file (plus optional `monitoring_timeline.md` human summary) the **#18 evaluator agent** reads to answer “what did monitoring surface over this period?” without opening N separate delta folders.

### 3) Retrospective business evaluation (feeds #18 P4)

- Invocation playbook: evaluator receives `monitoring_timeline.json` + rubric **P4** (not a single `refresh_news.json`).
- Output: `monitoring_quality_review.json` + `.md` (extends #18 `quality_review` pattern) with:
  - window-level verdict (`good_enough_for_pilot`, materiality trend, decay, gaps)
  - per-cycle callouts where relevant
  - link to valuable-update labels (§5 below)
- **Retrospective** = judgment after the window closes; distinct from per-cycle PASS in #15.

### 4) Monitoring-quality evaluation (per series, not per run)

Evaluated by the **#18 evaluator agent** with a monitoring-specific rubric:

- **New-material rate:** share of cycles that surface genuinely new, on-thesis updates (vs empty/noise).
- **Materiality:** are new updates decision-relevant (trigger terms hit, thesis movement) or trivial?
- **Duplication discipline:** no re-reporting of already-seen sources.
- **Drift:** does monitoring stay on-topic over time?
- **Coverage continuity:** are important channels still reached on later cycles (links to #21)?

### 5) Valuable-update feedback loop

- A mechanism to label historical deltas/sources as **highly valuable** (human and/or evaluator-agent assigned), stored alongside the monitoring history.
- These labels become reusable context the production agent can be given ("these past updates proved highly valuable for this topic") to bias future monitoring toward similar high-value signal.
- Define the label schema (e.g. `{topic_id, delta_seq, source_ids[], value: high|med, reason, labeled_by}`) and where it lives.

### 6) Outputs

- `monitoring_timeline.json` (+ optional `.md`) per evaluation window.
- `monitoring_quality_review.json` / `.md` from evaluator agent (#18 P4).
- A persisted, queryable record of valuable updates per topic.

### 7) Evaluation harness (Mode B)

- Script or vector profile, e.g. `scripts/test_monitoring_window.sh` or `vectors.json` entry `V002_monitoring_window`:
  1. plan → deliver → monitor (with schedule when #22 exists)
  2. run for configured duration or N scheduled cycles (real time or accelerated — document choice)
  3. assemble `monitoring_timeline.json`
  4. optional: invoke evaluator agent step (or manual operator step documented in `testing/README.md`)
- Do **not** conflate with vector runner’s back-to-back manual refresh (Mode A).

## Out of scope

- Single-run business judgment (**#18**)
- Mechanical PASS/FAIL of an individual refresh run (**#15**)
- Metric instrumentation internals — time-to-surface, channel classification (**#21**)
- Scheduler implementation itself (**#22** — this ticket consumes it)

## Open questions

- Where does monitoring history live (filesystem under `testing/`, DB, or both)?
- Real-time cadence for test topics vs accelerated simulation for CI.
- Timeline assembly: on-demand API vs batch job at window end?
- Who assigns "valuable" labels first — human operator, evaluator agent, or both with reconciliation?
- How is the valuable-update record fed back into the production agent prompt/context?

## Acceptance criteria

- [ ] Mode A unchanged: manual `/refresh` smoke still passes via existing harness (#11/#15).
- [ ] Mode B: monitored topic runs across a defined time window with multiple refresh cycles (scheduler or documented external trigger).
- [ ] `monitoring_timeline.json` produced for at least one test window with schema documented in `testing/README.md`.
- [ ] #18 evaluator agent applied P4 retrospectively to one timeline → `monitoring_quality_review.json`.
- [ ] Monitoring-quality rubric (P4 window-level) exists alongside per-cycle hints.
- [ ] Valuable-update label schema defined and at least one series labeled.
- [ ] Documented path for feeding valuable-update context back to the production agent.
- [ ] Clear boundary vs #18 single-run, #21 metrics, #22 scheduler implementation.

## Related

- `docs/specs/active/business_output_evaluation_18.md`
- `docs/specs/active/timeliness_channel_metrics_21.md`
- `apps/claude_agent/topics/refresh.py`
- `claude_agent_fe/.claude/commands/newsfind-refresh.md`
- `scripts/test_refresh_cycle.sh`
- `testing/app_testing_scenario.md` (§ refresh/monitoring)
