# Topic ops table (frontend) — #34

**Status:** planned  
**Label:** `frontend`  
**Depends on:** #16 (SignalGather frontend shell), **#24** (per-user topic ownership + JWT), **#22** (scheduler fields on monitor API)  
**Blocks:** Pilot ops without curl; admin visibility on prod/test  
**Lane:** Product / frontend — *topic list as an ops-grade monitoring table*

## Goal

Deliver a **Topic ops table** screen in the SignalGather frontend that lists topics in a dense, scannable table — the same information an operator today gathers manually via `GET /v1/topics` + `GET /monitor` per topic (as in ops curl checks).

Two visibility modes:

| Mode | Who | What they see |
|------|-----|----------------|
| **User** | Authenticated normal account (JWT) | Only topics where `owner_user_id == current user` (#24) |
| **Admin** | `is_superuser == true` **or** documented service-key ops session | **All** topics in the environment, plus owner identity |

The table is the **home / ops view** for monitoring cadence — not a replacement for the per-topic workspace (#16 phase 16b–c), but the entry point to open one.

## Problem

Today, checking “which topics are scheduled, when is the next refresh, is a refresh running?” requires manual API calls per topic. There is no UI equivalent of the ops summary table used during pilot runs (topic name, state, scheduler on/off, interval, next/last refresh, refresh count, lock status).

Without this screen:

- Operators cannot see scheduled topics at a glance on prod/test
- Normal users cannot see **their** monitored topics and cadence after reconnecting
- Admins cannot audit all topics without curl or DB access
- Stop/pause actions (PATCH schedule off, DELETE monitor) stay undocumented for non-engineers

## Reference — target table shape (per row)

Each topic row exposes the fields below. Column headers are fixed; values come from API (see § API contract).

| Column | Source | Example |
|--------|--------|---------|
| **Topic** | `GET /v1/topics` → `topic` | Chinese Demand & Stimulus |
| **Topic ID** | `id` (truncated + copy full) | `2d09f18a…127d` |
| **State** | `state` | `reported` |
| **Monitor** | `monitor.status` | `active` / `paused` / `—` |
| **Scheduler** | `monitor.schedule_enabled` + `schedule_interval_hours` | **ON** — every 1h / **OFF** |
| **Next refresh** | `monitor.next_refresh_at` | `2026-07-06T11:32:19Z` / `—` |
| **Last refresh** | `monitor.last_refresh_at` | `2026-07-06T09:40:27Z` |
| **Refresh count** | `monitor.refresh_count` | `45` |
| **In progress** | `monitor.refresh_locked` | Yes (spinner) / No |
| **Updated** | `updated_at` | relative + absolute tooltip |

**Admin-only columns**

| Column | Source | Example |
|--------|--------|---------|
| **Owner** | `owner_email` or `owner_user_id` (truncated) | `pilot@example.com` |
| **Created** | `created_at` | `2026-07-04` |

Sort default: **`updated_at` descending** (newest activity first). Optional filters: state, scheduler on/off, monitor active/paused.

## User flows

### A. Normal user — “My topics”

1. User logs in (JWT via #24 / #16 auth).
2. Lands on **Topics** table scoped to their topics only.
3. Sees scheduler/monitor columns for topics in `reported` (and monitor subscription exists).
4. Row click → topic workspace (#16).
5. Optional row actions (if monitor exists):
   - **Stop scheduler** — `PATCH /monitor` `{ "schedule_enabled": false }` (monitor stays)
   - **Pause monitoring** — `DELETE /monitor` (confirm dialog)
   - **Manual refresh** — `POST /refresh` (disabled when `refresh_locked` or monitor paused)

### B. Admin — “All topics”

1. Admin logs in with `is_superuser` **or** ops uses service-key session (documented, env-gated — same as #24 harness bypass).
2. Same table as above but **unfiltered** list + **Owner** column.
3. Admin can stop scheduler / pause monitoring on **any** topic (same actions as user on own topics).
4. Visual badge: **Admin view — all topics** so it is obvious scope is global.

### C. Empty & loading states

- No topics: onboarding CTA → **New topic** (#16 create flow).
- Topic without monitor: monitor/scheduler columns show `—`; actions hidden or disabled with tooltip (“Enable monitoring from workspace”).
- In-flight refresh: **In progress** column shows spinner; stop-scheduler still allowed; pause monitoring allowed (current refresh may finish — document in UI copy).

## UX requirements

1. **Dense table** — desktop-first; horizontal scroll on tablet acceptable; no card-only layout for this screen.
2. **No N+1 in UI** — list endpoint must return monitor summary inline (see backend note); do not call `GET /monitor` per row on page load.
3. **Confirm destructive actions** — pause monitoring and stop scheduler require confirm modal with one-line consequence.
4. **Live updates** — optional V1: poll list every 60s **or** refresh on tab focus; full SSE per-row is out of scope for this ticket (workspace handles SSE).
5. **Timezone** — show UTC in tooltip; local time in cell if browser locale available.
6. **Czech + EN copy** — i18n-ready strings; English default for V1.

## API contract (backend additions — coordinate with #24)

`GET /v1/topics` today returns only topic metadata (`id`, `topic`, `state`, timestamps). Extend list items **or** add `GET /v1/topics?include=monitor` for:

```json
{
  "items": [
    {
      "id": "2d09f18a-7512-4a56-87d2-1b8302bd127d",
      "topic": "Chinese Demand & Stimulus",
      "state": "reported",
      "created_at": "2026-07-04T14:09:09.433796+00:00",
      "updated_at": "2026-07-06T10:32:41.862762+00:00",
      "monitor": {
        "status": "active",
        "schedule_enabled": true,
        "schedule_interval_hours": 1,
        "next_refresh_at": "2026-07-06T11:32:19.623205+00:00",
        "last_refresh_at": "2026-07-06T09:40:27.143852+00:00",
        "last_scheduled_refresh_at": "2026-07-06T09:40:27.143852+00:00",
        "refresh_count": 44,
        "refresh_locked": true
      }
    }
  ],
  "count": 1,
  "limit": 50,
  "offset": 0
}
```

Rules:

- `monitor` is **`null`** when no subscription exists (not 404 per row).
- **User JWT:** list filtered by `owner_user_id`; monitor block only for owned topics.
- **Admin (`is_superuser`):** unfiltered list; include `owner_user_id` + `owner_email` (or display name) on each item.
- **Service key (ops):** same as admin when bypass enabled (#24).
- Pagination: keep existing `limit` / `offset`; default `limit=50`, max 200.

Mutations (reuse existing routes — no new endpoints required):

| Action | API |
|--------|-----|
| Stop scheduler | `PATCH /v1/topics/{id}/monitor` `{ "schedule_enabled": false }` |
| Pause monitoring | `DELETE /v1/topics/{id}/monitor` |
| Manual refresh | `POST /v1/topics/{id}/refresh` |

Ownership: non-owner → **404** on mutations (#24).

## Scope

### In scope (frontend #34)

- Topics table page/component with columns above
- User-scoped list (JWT)
- Admin-scoped list (superuser + documented ops path)
- Row actions: stop scheduler, pause monitoring, open workspace
- Filters: state, scheduler on/off (client or query param)
- Confirm modals + toast on success/error
- Link from #16 shell nav (“Topics” / home)

### Backend (minimal — can ship in same PR or unblock #24 follow-up)

- Enriched `GET /v1/topics` with embedded `monitor` summary (single query / join)
- Admin list + owner fields when `is_superuser`
- Tests: list shape, user filter, admin sees all, monitor null when absent

### Out of scope

- Per-topic SSE on list page
- Abort in-flight refresh (no API today)
- Full topic workspace, report reader, create flow — **#16**
- User registration UX polish — **#16** / **#24**
- Cross-environment table (one API base URL per deployment)
- Bulk actions (stop all schedulers)

## Phases

| Phase | Deliverable |
|-------|-------------|
| **34a — Read-only table** | User list + monitor columns; row → workspace |
| **34b — Row actions** | Stop scheduler, pause monitoring, manual refresh |
| **34c — Admin view** | Superuser all-topics + owner column |

Recommended order: **34a after #24**; **34c** can follow 34a if backend admin list ships with #24.

## Acceptance criteria

### User view
- [ ] Logged-in user sees only their topics in the table.
- [ ] Each row shows topic, state, monitor status, scheduler on/off + interval, next/last refresh, refresh count, in-progress flag.
- [ ] Topics without monitor show `—` in monitor columns without errors.
- [ ] Clicking a row opens the topic workspace (#16 route).

### Admin view
- [ ] User with `is_superuser=true` sees all topics and an Owner column.
- [ ] Admin badge/copy makes global scope obvious.
- [ ] Admin can stop scheduler and pause monitoring on any topic (with confirm).

### Actions & API
- [ ] Stop scheduler sets `schedule_enabled: false` and clears next refresh in UI after refresh.
- [ ] Pause monitoring sets monitor status to paused; manual refresh disabled with clear message.
- [ ] List load uses one API call (no per-row `GET /monitor` on initial render).

### Ops
- [ ] Short UI smoke checklist added (test1): create topic → monitor → table shows scheduler ON → stop → OFF.
- [ ] Documented in `docs/product/README.md` under frontend surfaces when shipped.

## Open questions

- Admin via **`is_superuser`** only vs separate `role=admin` enum?
- Show **service-key ops mode** in the same UI (API key in settings) or admin JWT only for prod?
- Include **cost summary** column from last refresh delta (nice-to-have — defer)?
- Query params for filter/sort on server vs client-only for V1?

## Related

- `docs/specs/done/signalgather_frontend_v1_16.md` — shell, workspace, auth (#16)
- `docs/specs/active/topic_user_ownership_24.md` — JWT scoping + admin bypass (#24)
- `docs/specs/done/topic_refresh_scheduler_22.md` — scheduler fields (#22)
- `testing/app_testing_scenario.md` §7.2a — PATCH/DELETE monitor curl reference
- Ops manual check pattern: prod topic `2d09f18a-7512-4a56-87d2-1b8302bd127d` (Chinese Demand & Stimulus) — reference row for QA
