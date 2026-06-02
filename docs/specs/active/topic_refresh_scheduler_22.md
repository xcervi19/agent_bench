# Topic refresh scheduler — #22

**Status:** active (planned)  
**Depends on:** #17 (monitor + manual `/refresh` shipped), #13 (multi-env VPS)  
**Blocks:** #16 phase 16c (scheduled monitoring UX), #20 (realistic longitudinal cadence)  
**Lane:** Product / backend — *automatic monitoring without external cron*

## Why this exists (gap)

Monitor + manual `POST /refresh` works, but **nothing inside the product triggers refresh on a cadence**. Operators must wire external cron or click refresh themselves. That is not viable for pilot users who expect “keep my topic updated every N hours” without DevOps.

`POST /refresh` stays the **manual on-demand** path (frontend button, user wants news now). This ticket adds **optional automatic scheduling** per monitored topic.

## Goal

Run refresh cycles automatically for topics with an active monitoring subscription and a configured interval, reusing existing `run_refresh` orchestration and SSE events. Manual refresh remains available and idempotent.

## Core question

*"Can a monitored topic stay current on its own, while users can still force an update when they want?"*

## Scope

### 1) Schedule configuration (API + DB)

- Extend `TopicSubscription` (or equivalent) with optional schedule fields, e.g.:
  - `schedule_enabled: bool`
  - `schedule_interval_hours: int | null` (or cron expression — pick one, document it)
  - `next_refresh_at`, `last_scheduled_refresh_at` (for observability)
- `POST /monitor` and `PATCH /monitor` (or equivalent) accept schedule settings.
- `GET /monitor` and `GET /v1/topics` expose schedule status for frontend (#16).
- **No schedule** = monitoring subscription only; user relies on manual `POST /refresh` (current behavior).

### 2) Internal scheduler job

- New job in `claude_agent` (or shared scheduler entrypoint) that periodically:
  - selects active subscriptions where `schedule_enabled` and `next_refresh_at <= now`
  - calls the same refresh path as `POST /refresh` (respect `refresh_locked`, `max_concurrent_jobs`)
  - updates `next_refresh_at` after enqueue or completion (define semantics)
- Enable the **scheduler** service on VPS (`docs/ops/vps.md` — currently not running).
- Emit distinguishable event metadata when refresh was **scheduled** vs **manual** (for UI + testing).

### 3) Frontend contract (minimal backend support)

- Manual `POST /refresh` unchanged — 202 + SSE `refresh.*` events.
- Scheduled runs use the same event stream so the UI stays event-driven (#16).
- List/detail endpoints expose enough for “auto every 6h” vs “manual only” badges.

### 4) Feeds monitoring timeline (#20)

Each scheduled (and manual) refresh cycle appends to per-topic delta history. **#20** rolls cycles in a time window into `monitoring_timeline.json` for retrospective business evaluation — scheduler is the cadence source; timeline assembly is not in this ticket.

### 5) Testing updates

When this ships, **extend** (not replace) manual refresh tests:

- `scripts/test_vector_runner.sh` — add vector flag or step: scheduled refresh fires without `POST /refresh`
- `scripts/test_refresh_cycle.sh` — optional `--scheduled` smoke
- `testing/app_testing_scenario.md` — document schedule setup + manual override
- `testing/README.md` — lifecycle diagram includes scheduler path

Test cases:

- [ ] Monitored, schedule off → only manual `POST /refresh` produces deltas (regression)
- [ ] Monitored, schedule on → refresh completes without manual POST; SSE `refresh.completed`
- [ ] Manual POST while scheduled refresh running → `queued: false` (idempotent lock)
- [ ] `DELETE /monitor` → scheduled job skips topic; manual POST returns 404/409 as today

## Out of scope

- Longitudinal monitoring **evaluation** and valuable-update feedback (**#20**)
- Business rubric for refresh quality (**#18**)
- Mechanical PASS/FAIL rules for refresh artifacts (**#15**)
- Replacing external cron for ops-only environments (may coexist; internal scheduler is default for product)

## Open questions

- Interval-only vs cron (e.g. “every 6h” vs “08:00 UTC daily”) for V1?
- Single global scheduler process vs per-topic APScheduler jobs?
- Backoff when refresh fails repeatedly — pause schedule or retry?
- Should `max_age_hours` and `schedule_interval_hours` be validated together (interval ≤ max_age)?

## Acceptance criteria

- [ ] User can enable monitoring with an optional refresh interval via API.
- [ ] Scheduler service runs on test1/prod and triggers refresh without manual POST.
- [ ] Manual `POST /refresh` still works for topics with or without schedule.
- [ ] SSE clients cannot tell apart scheduled vs manual by missing events (same `refresh.*` stream; optional `trigger: scheduled|manual` in payload).
- [ ] Harness updated: at least one automated test proves scheduler-triggered refresh.
- [ ] `docs/ops/vps.md` documents scheduler enablement and health check.

## Related

- `docs/specs/done/pilot_ops_v1_17.md` — external cron was interim model; superseded for product by this ticket
- `docs/specs/active/signalgather_frontend_v1_16.md` — 16c monitor + deltas UX
- `docs/specs/active/continuous_monitoring_evaluation_20.md` — realistic cadence for longitudinal capture
- `apps/claude_agent/topics/refresh.py`, `apps/claude_agent/topics/models.py`
- `testing/app_testing_scenario.md` §7 (monitor + refresh)
