# Topic user ownership — #24

**Status:** done (verified on `test1`, 2026-07-26)  
**Depends on:** #17 (topic API + `GET /v1/topics` shipped), #13 (multi-env HTTPS)  
**Blocks:** #16 (frontend topic list + per-user workspace), #22 (scheduler UX: user sees only their monitored topics)  
**Feeds:** #16 (JWT login + scoped APIs)  
**Lane:** Product / backend — *auth & data isolation for the Newsfind topic pipeline*

## Goal

Wire **user authentication** into the shipped `claude_agent` topic API so every topic — plan, deliver, report, monitor subscription, refresh deltas, and artifacts — is **owned by and visible only to the authenticated user** who created it.

Today the topic API uses an optional shared **`X-API-Key`** (service key). Topics have **no `user_id` / `owner_id`**. Any caller with the key can list and access all topics. That is acceptable for pilot ops and the eval harness, but **not** for a multi-user product where background monitoring (#22) collects data while the user is away and the frontend (#16) must show *their* topics when they connect.

This ticket adds the **backend ownership model and access control**. It does **not** build the frontend or login UI.

## Core question

*"When a user is authenticated, do they see only their own topics and collected monitoring data — and can no other user read or mutate them?"*

**Answer:** Yes on `test1` after migration `0006_topic_owner` (cross-user isolation verified on all topic routes + SSE).

## Shipped

| Area | Delivered |
|---|---|
| Schema | Migration `0006_topic_owner`: `topics.owner_user_id` (nullable FK → `users.id`), index `(owner_user_id, updated_at DESC)` |
| Auth | `apps/claude_agent/auth.py` — `Principal` (JWT user or service key); auth routes mounted when DB enabled |
| Enforcement | `_owned()` on all 22 `/v1/topics/*` routes; list filtered by owner; 404 on cross-user access |
| Harness | `CLAUDE_AGENT_ALLOW_SERVICE_KEY_BYPASS` (default `true`); documented in `docs/ops/vps.md`, `testing/app_testing_scenario.md` |
| Tests | `tests/topics/test_ownership.py` (12 tests) |
| Deploy | `test1` at commit `d8d0900`; prod pending separate deploy |

**Deferred (explicit out of scope):** `topics.tenant_id` column; Postgres RLS; CORS for frontend origin (#16 deploy).

**Backfill policy:** `owner_user_id` nullable — pre-migration and service-key topics stay NULL (service role only).

Existing user model: `libs/agentic_core/api/user_model.py` — `User` with `id`, `email`, `tenant_id` (JWT via fastapi-users).

## Scope

### 1) Schema & migration

- Add to `topics` (Alembic migration under `database/migrations/`):
  - `owner_user_id` — UUID, FK → `users.id`, **NOT NULL** for new rows
  - `tenant_id` — UUID, nullable or NOT NULL aligned with `User.tenant_id` (recommended for future RLS parity with `signal_gather` tables)
- Index: `(owner_user_id, updated_at DESC)` for list queries.
- **Backfill policy:** existing rows without owner — either assign to a bootstrap system user, leave nullable temporarily with migration note, or one-time ops script. Document chosen approach in migration + ops doc.

Child rows (`topic_events`, `topic_subscriptions`, `topic_refresh_deltas`, `topic_webhooks`) inherit access via `topic_id` FK — no separate owner column required if all routes resolve topic ownership first.

### 2) Authentication on topic routes

- Replace or layer auth on `apps/claude_agent/topics/routes.py`:
  - **Product path:** `Authorization: Bearer <jwt>` → resolve `User` via `agentic_core` `current_user` dependency.
  - **Ops/harness path:** retain optional `X-API-Key` as **service role** (full access or superuser-only) for `scripts/test_vector_runner.sh`, VPS smoke, and CI — explicitly documented and env-gated (`CLAUDE_AGENT_API_KEY` + `CLAUDE_AGENT_ALLOW_SERVICE_KEY_BYPASS=true` or similar).
- Mount auth routers on `claude_agent` app when `database_url` is set (same Postgres as users table).

### 3) Ownership enforcement (all topic endpoints)

Every handler that accepts `topic_id` must:

1. Load topic.
2. Verify `topic.owner_user_id == current_user.id` (and optionally `tenant_id` match).
3. Return **404** (not 403) on mismatch — avoid leaking topic existence.

Apply to at minimum:

- `GET /v1/topics` — filter `WHERE owner_user_id = :uid`
- `GET /v1/topics/{id}` and all artifact routes (`/parsed`, `/report`, `/news`, …)
- `POST /proceed`, `/cancel`, `/monitor`, `/refresh`, `/subscribe` (webhooks)
- `GET /events` (SSE) — reject connection if not owner
- `GET /deltas`, `/deltas/{seq}`, delta artifact routes

`POST /v1/topics` — set `owner_user_id` (and `tenant_id`) from JWT on insert.

### 4) API contract for frontend (#16)

Expose enough for the UI without duplicating business logic:

| Endpoint / field | Addition |
|---|---|
| `GET /v1/topics` items | Include `owner_user_id` only if needed internally; prefer not to expose other users' ids |
| List response | Scoped list is sufficient; optional `monitor.status`, `schedule_enabled` when #22 ships |
| Auth | Document login flow: `POST /auth/jwt/login` → Bearer on all `/v1/topics/*` |
| CORS | Allow frontend origin on `claude_agent` (may be a one-line config ticket note for #16 deploy) |

### 5) Harness & test updates

- Extend `testing/` so vector runner can authenticate:
  - **Option A:** create/login test user, pass JWT in runner env; or
  - **Option B:** service key bypass for harness only (product disables bypass).
- Add unit/integration tests: user A cannot read user B's topic; list returns only own topics; create binds owner.
- Update `testing/app_testing_scenario.md` with authenticated flow example.

### 6) Ops documentation

- `docs/ops/vps.md` or `docs/product/README.md`: how pilot/demo accounts work; service key vs user JWT.
- Note interaction with #22: scheduled refresh runs server-side — results remain tied to topic owner; when user reconnects via #16 + SSE, they see updates for **their** topics only.

## Out of scope

- **Frontend / login screen** — **#16** (consumes JWT from this ticket)
- **Automatic background scheduler** — **#22** (runs refresh; ownership here ensures collected data is per-user)
- **Business output evaluation** — **#18** / **#23**
- **Full multi-tenant admin UI**, OAuth providers, password reset UX polish
- **Row-level security (RLS)** on `topics` in Postgres — optional follow-up; app-layer checks are sufficient for V1
- **Migrating `signal_gather` user profiles** to Newsfind topics — separate product integration

## Open questions (resolved at ship)

- Service key: **superuser bypass** kept via `CLAUDE_AGENT_ALLOW_SERVICE_KEY_BYPASS` (default on for harness).
- `tenant_id` on topics: **not added** — YAGNI for V1.
- Backfill: **nullable `owner_user_id`** — legacy rows service-owned.

## Acceptance criteria

- [x] Migration adds `owner_user_id` (+ `tenant_id` if chosen) to `topics` with index.
- [x] `POST /v1/topics` persists owner from JWT; unauthenticated requests rejected (401) in product mode.
- [x] `GET /v1/topics` returns only the authenticated user's topics.
- [x] All topic-scoped routes return 404 for another user's `topic_id`.
- [x] SSE `/events` enforces ownership on connect.
- [x] Auth routes (login/register) available on `claude_agent` when DB enabled.
- [x] Harness/CI path documented and working (JWT test user **or** documented service-key bypass).
- [x] Tests cover cross-user isolation (at least: list filter, get 404, create binds owner).
- [x] Ops doc updated: product uses JWT; harness uses documented bypass or test user.

## Related

- `apps/claude_agent/auth.py`, `apps/claude_agent/topics/models.py`, `apps/claude_agent/topics/routes.py`
- `libs/agentic_core/api/auth.py`, `auth_routes.py`, `user_model.py`
- `database/migrations/versions/0006_topic_owner.py`
- `docs/specs/done/pilot_ops_v1_17.md` — `GET /v1/topics` (#17)
- `docs/specs/active/signalgather_frontend_v1_16.md` — consumes JWT + scoped APIs
- `docs/specs/active/topic_refresh_scheduler_22.md` — background collection; data user-scoped via owner
- `testing/app_testing_scenario.md`, `scripts/test_vector_runner.sh`
