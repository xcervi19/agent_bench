# SignalGather frontend V1 — topic intelligence UI — #16

**Status:** planned  
**Depends on:** #9 (topic pipeline API + SSE), #13 (multi-env HTTPS slots), #17 (`GET /v1/topics` for topic list)

## Goal

Deliver a **modern, responsive web frontend** for SignalGather that turns the existing Newsfind topic API into a **trader-grade product experience**: natural-language topic setup, live pipeline visibility, human review gates, strategic reports, and monitored refresh deltas — without requiring curl or manual artifact inspection.

The UI must feel **alive**: data loads progressively as the backend produces it, and the app stays connected and updated via **server-pushed events** (scheduler + agent work → events → UI).

## Problem

Today the shipped product surface is **API-only** (`POST /v1/topics`, SSE `/events`, artifact routes). Business requirements (`docs/specs/business_requirements/business_requirements.md`) define rich user interfaces — signals dashboard, events feed, briefings, alerts — but none exist yet. Manual testing via `testing/app_testing_scenario.md` proves the pipeline works; it does not deliver ROI for professional users.

Without a frontend:
- Users cannot easily review plans, approve gates, or read reports in context
- Long-running agent work (plan/deliver/refresh) has no transparent progress UX
- Scheduled monitoring has no “what’s new since I last looked” surface
- The product cannot compete on **time saved** and **reaction speed** vs Bloomberg/Reuters-style workflows

## Product alignment

Maps to **Minimalist V1 Core Pipeline** (business brief §5):

| Pipeline step | User-facing UI |
|---------------|----------------|
| 1. Topic foundation & context | Create topic (NL input) → live planning → intro + query plan review |
| 2. Comprehensive strategic reporting | Deliver progress → report reader (markdown + citations + sources) |
| 3. Market impact & downstream analysis | Report sections: findings, scenarios, impact (from `report.json` / `report.md`) |
| 4. Interval news gathering | Enable monitor → refresh timeline → delta view (new sources + updated report) |

**Deferred to later specs** (business brief §3.4 — full vision, not V1):
- Global real-time signals dashboard across all topics
- Cross-topic search & historical exploration
- Email/chat alerts and daily/weekly briefing digests
- Full `signal_gather` RSS → signals stack UI

## UX principles (non-negotiable for V1)

1. **Event-driven, not poll-heavy** — UI subscribes to `GET /v1/topics/{id}/events` (SSE). Fetch artifacts when events indicate readiness (`intro.ready`, `report.ready`, `refresh.completed`), not on a blind timer.
2. **Progressive disclosure** — Show state + current stage first; stream activity (stages, tools) in a collapsible panel; hydrate artifacts as they appear.
3. **Reconnect-safe** — Resume SSE from last `seq` (`from_seq` query param). On reconnect, reconcile topic state + fetch any missing artifacts.
4. **Trust & control** — Clear topic state badge; explicit **Proceed** / **Cancel** at `planned_awaiting_review`; monitor interval visible; errors surfaced with retry context.
5. **Trader-readable density** — Scannable headlines, source links, relevance, timestamps; report citations link to sources where possible.
6. **Responsive & modern** — Works on desktop and tablet; dark/light acceptable; fast first paint; no “wait for full JSON blob” blank screens.

## V1 scope — screens & flows

### A. Topic list (home)

- List user topics: title/slug, **state**, last activity, monitor on/off, “new since last visit” badge (from delta metadata when available)
- **New topic** — single NL text field (mirrors business brief setup example)
- Empty state with short onboarding copy

### B. Topic workspace (primary screen)

Single-topic command center with tabs or sections:

| Section | Data source | Behavior |
|---------|-------------|----------|
| **Status bar** | `GET /v1/topics/{id}` + SSE `state.changed` | State machine badge, elapsed time, cost summary if in events |
| **Live activity** | SSE: `stage.*`, `tool_use`, `tool_result`, `refresh.*`, `error` | Append-only feed; auto-scroll optional; tool I/O previews collapsed by default |
| **Plan review** | `/intro.md`, `/parsed` | Shown at gate; query table (intent, language, priority); **Proceed** / **Cancel** |
| **Report** | `/report`, `/report.md`, `/news` | Markdown render; source list with scores; key findings / scenarios from JSON |
| **Monitoring** | `POST /monitor`, `/deltas`, delta artifact routes | Toggle monitor + interval; refresh history list; open delta detail (new sources, delta report) |
| **Manual refresh** | `POST /refresh` | Trigger button when monitored; shows in activity feed |

### C. Auth & environment (minimal V1)

- API key in env or login screen (match existing `X-API-Key` on `claude_agent`)
- Configurable API base URL (prod / test1 / test2 from `docs/product/README.md`)

## Technical approach

### Real-time transport

**V1: SSE** — already implemented and battle-tested (`apps/claude_agent/topics/routes.py`). Frontend uses `EventSource` or fetch-based SSE reader with:
- `from_seq` for replay after disconnect
- Event types per `docs/specs/done/agentic_search_claude_code_architecture.md`

**WebSockets:** out of scope for V1 unless SSE proves insufficient for bidirectional needs (e.g. cancel mid-flight). Document as future option in architecture notes.

### Frontend stack (recommended, not mandated in spec)

- **SPA or SSR app** in monorepo (e.g. `apps/signalgather_web/` or `frontend/`)
- TypeScript + component library suited to data-dense dashboards (e.g. React + Tailwind/shadcn)
- Client state: topic list + per-topic event buffer + artifact cache invalidated by event type
- Markdown renderer for `intro.md` / `report.md`

### Backend changes (minimal)

Prefer **consume existing API**; add endpoints only where UI blockers exist:

| Need | Possible addition |
|------|-------------------|
| Topic list metadata | Ensure `GET /v1/topics` returns fields UI needs (state, updated_at, monitor status) |
| CORS | Enable for app origin on `claude_agent` if UI served separately |
| Static hosting | Caddy route for `app.particletico.com` or path on existing host |

No duplicate business logic in the frontend — orchestration stays in `claude_agent`.

### Deployment

- Build static assets or Node server image
- Serve via Caddy alongside existing `agent*.particletico.com` endpoints (#12, #13)
- Test against **test1** before prod

## Phases

| Phase | Deliverable |
|-------|-------------|
| **16a — Shell + create + live plan** | Topic list, create topic, SSE activity, intro/plan at gate, proceed |
| **16b — Deliver + report** | Deliver progress, report + sources viewer |
| **16c — Monitor + deltas** | Monitor controls, delta timeline, refresh UX (depends on scheduler) |
| **16d — Polish** | Responsive pass, empty/error states, reconnect UX, env switcher |

## Acceptance criteria

### Core journey
- [ ] User creates topic from NL input without using curl
- [ ] User sees live planning progress (stages/tools) via SSE
- [ ] User reviews intro + query plan and clicks Proceed at gate
- [ ] User sees deliver progress and reads finished report with sources
- [ ] User enables monitoring and sees refresh cycles update the UI via events
- [ ] User opens a refresh delta and sees new sources / updated report content

### Real-time & resilience
- [ ] UI reconnects after tab sleep or network drop without losing event history (`from_seq`)
- [ ] Artifact fetches triggered by relevant events, not fixed-interval polling of all endpoints
- [ ] Terminal states (`reported`, `failed`, `cancelled`) reflected correctly; active refresh keeps stream open

### UX quality
- [ ] Responsive layout usable on desktop and tablet widths
- [ ] Loading skeletons / placeholders while artifacts are not yet available (404 handled gracefully)
- [ ] Errors from SSE and API shown in context with topic state preserved

### Ops
- [ ] Documented deploy path for at least one test slot (test1)
- [ ] `docs/product/README.md` updated when UI is user-facing
- [ ] Manual test scenario in `testing/` or short UI smoke checklist

## Out of scope (V1)

- Global multi-topic signals dashboard
- User accounts / multi-tenant auth beyond API key
- Email, Slack, or push notifications
- LLM chat inside the UI for topic setup (NL form field is enough for V1)
- WebSocket server (unless SSE blocker documented)
- Mobile-native apps
- Editing agent query plans in UI (read + approve only)

## Related

- `docs/specs/business_requirements/business_requirements.md` — product vision, V1 pipeline, future UI list
- `docs/product/README.md` — shipped API surface today
- `docs/specs/done/agentic_search_claude_code_architecture.md` — state machine, events, artifacts (#9)
- `docs/specs/done/multi_env_pre_frontend_13.md` — prod/test1/test2 (#13)
- `testing/app_testing_scenario.md` — reference flows the UI must replace
- `docs/specs/active/pilot_ops_v1_17.md` — backend pilot-ready work including `GET /v1/topics`

## Open decisions (resolve at kickoff)

1. **App location in monorepo** — `apps/signalgather_web/` vs separate repo
2. **Hosting URL** — `app.particletico.com` vs path on `agent.particletico.com`
3. **Auth model V1** — API key in settings vs simple login proxy
4. **Citation links** — resolve `[s01]` to source URLs in UI (known API limitation in #9)
