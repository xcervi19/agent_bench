# SignalGather frontend V1 — topic intelligence UI — #16

**Status:** **16a–16d implemented** (code + 178 offline frontend tests green; test1 smoke pending)  
**Depends on:** #9 (topic pipeline API + SSE), #13 (multi-env HTTPS slots), #17 (`GET /v1/topics` for topic list), **#24** (topics bound to authenticated users)
**Blocks:** #37 (pilot first-use experience)

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

| Phase | Deliverable | Status |
|-------|-------------|--------|
| **16a — Shell + create + live plan** | Topic list, create topic, SSE activity, intro/plan at gate, proceed | **shipped** |
| **16b — Deliver + report** | Deliver progress, report + sources viewer, **adaptive widget rendering**, citation resolution | **shipped** |
| **16c — Monitor + deltas** | Monitor controls, delta timeline, refresh UX | **shipped** |
| **16d — Polish** | Responsive pass, empty/error states, reconnect UX, env switcher, new-since-last-visit | **shipped** |

## 16b — adaptive widget rendering (markdown-ui pattern)

**Why this exists.** The original pipeline design
(`github_issue/newsfind_pipeline_v1.md`, commit `d792fff`, since deleted from the
repo) made this principle #5: *"Markdown-ui-friendly delivery. Every user-facing
artifact has both a structured JSON view and a markdown rendition, so a
markdown-ui frontend can render natively"* — and required `intro.md` / `report.md`
to reference custom components by name, e.g.
`<EntityChips entities="..."/>`, `<Highlights items="..."/>`. The requirement was
lost when that file was deleted and never carried into #16, so **16a does not
implement it**. It is a first-class 16b deliverable.

**Product goal.** The agent decides how its output is presented. Adding a new
kind of report block must not require a frontend change — no per-output-type
component wiring, ever.

**Decision (kickoff, 2026-07-26): build it ourselves, same pattern — do not
adopt `markdown-ui`.** The library at <https://markdown-ui.blueprintlab.io/>
(`@markdown-ui/marked-ext`, `@markdown-ui/mdui-lang`, `@markdown-ui/react` 0.4.0)
was evaluated against the source:

- ✅ Right pattern, and built on `marked`, which the app already uses; peer React
  ^18||^19; `parseDSLStreaming` renders partial widgets as tokens arrive.
- ❌ **Closed widget set.** `Widget.tsx` dispatches through a hard-coded
  `typeMapping` over a static `import * as widgets` — there is no registration
  API. The catalogue is text-input, button-group, select, select-multi, slider,
  form, chart-{line,bar,pie,scatter}, MCQ, short-answer, quiz: built for chat and
  quizzes. Our report blocks (entity chips, source list with relevance, scenario
  table, highlights) **cannot be added**, so it would not remove per-output
  frontend work — only the charts would come for free.
- ❌ Renders via `dangerouslySetInnerHTML` with **no sanitization**; our markdown
  is LLM-written and currently goes through DOMPurify.
- ⚠️ v0.4.0, single maintainer, debug `console.log`s left in shipped code.

**Shape to build** (own code, no new runtime dependency — `marked` + DOMPurify
are already in the app):

1. **Widget DSL in markdown.** A fenced block the agent emits, parsed into a
   typed descriptor. Keep the syntax close to markdown-ui's
   ` ```markdown-ui-widget ` so their widgets stay adoptable later.
2. **Widget registry** — `type → React component`, one lookup, one place to
   extend. An unknown type degrades to a readable block, never a crash or a
   blank panel.
3. **Sanitization stays.** Widget payloads are validated against the registry's
   schema before render; surrounding prose keeps going through DOMPurify.
4. **Streaming-tolerant.** A half-written widget in a streaming artifact renders
   a placeholder, not garbage.
5. **Contract update.** `claude_agent_fe/.claude/commands/newsfind-plan.md` and
   `newsfind-deliver.md` emit registry widgets instead of today's bare
   `<EntityChips>` / `<Highlights>` tags.

### What was built

| Piece | Where |
|---|---|
| Widget contract + validation | `src/lib/widgets/types.ts`, `src/lib/widgets/parse.ts` |
| type → component registry | `src/components/widgets/registry.tsx` |
| Composed renderer (prose + widgets + citations) | `src/components/ArtifactMarkdown.tsx` |
| `[s01]` → source links | `src/lib/citations.ts` |
| Agent contract | `claude_agent_fe/.claude/widgets.md` (+ plan/deliver/refresh prompts) |

Shipped widget types: `entity-chips`, `highlights`, `callout`, `metrics`,
`key-findings`, `scenario-table`, `news-card`, `source-list`. Adding one is a
validator branch plus a registry entry — no change to any screen.

**Deviation from markdown-ui, deliberate:** the fence name
` ```markdown-ui-widget ` is kept so their widgets stay adoptable, but the body
is **JSON**, not their positional DSL. An LLM emits valid JSON far more reliably
than a quoted-positional grammar, and JSON validates cleanly per type. Adopting
their widget set later means adding a DSL parse branch in `parse.ts`.

**Legacy artifacts keep working.** Reports already on disk contain
`<EntityChips>`, `<Highlights>`, `<NewsCard source-id/>`; the parser maps those
onto the same registry. An inline `<NewsCard/>` inside a sentence degrades to a
citation rather than being dropped. New output uses the fenced form.

**Failure is visible, not silent.** An unregistered type or a payload that fails
its contract renders a "cannot display" disclosure carrying the reason and the
raw payload — an agent shipping ahead of the frontend must not blank a section
of a report.

## 16a — what shipped

App lives at **`apps/signalgather_web/`** (React 19 + TypeScript + Vite +
Tailwind v4), served by `claude_agent` at **`/app`**.

| Area | Delivered |
|---|---|
| Auth | JWT sign-in + self-registration against `/auth/jwt/login` and `/auth/register` (#24); token in `localStorage`; session re-validated via `/users/me` on load; env picker (same-origin / local / test1 / test2 / prod) |
| Topic list | Owner-scoped list with state badges, relative timestamps, “needs your review” flag, empty state, NL create field (⌘/Ctrl+Enter) |
| Workspace | Status bar (state, elapsed, event count), live activity feed, plan review (`intro.md` + `intro.json` fallback + `parsed.json` query table), Proceed / Cancel |
| Real-time | `src/lib/sse.ts` — fetch-based SSE (EventSource cannot send `Authorization`), `from_seq` resume, 500 ms→10 s backoff, `: done` = clean close, no retry on 401/404 |
| Artifact loading | Fetched on `intro.ready` / `needs_input`, plus once on mount when `plan_run_id` exists (covers a gate reached while away); 404 renders a placeholder, never an error |
| Safety | Agent-written markdown rendered through DOMPurify |
| Backend | `_mount_cors` + `_mount_web` in `apps/claude_agent/app.py`; settings `CLAUDE_AGENT_CORS_ORIGINS`, `CLAUDE_AGENT_WEB_DIST` |
| Deploy | `web` build stage in `docker/Dockerfile.claude_agent`; existing `agent-test1` Caddy vhost serves `/app` unchanged; repo-root `.dockerignore` added |
| Tests | 75 frontend (vitest: SSE parse/resume/backoff, API client, markdown sanitizing, event copy, plan gate, topic list) + 12 backend (`tests/topics/test_web_hosting.py`) |
| Docs | `apps/signalgather_web/README.md`, `testing/ui_smoke_16.md` |

## 16b–16d — what shipped

| Area | Delivered |
|---|---|
| Workspace | Tabbed sections — Plan / Report / Sources / Monitoring. Tabs appear only once the pipeline can back them, and the section matching the topic's state is preselected until the user picks one |
| Report (16b) | `report.md` through the widget pipeline, executive summary, thesis-status badge, thesis update, key findings + scenario updates rendered **through the same registry** so the two paths cannot drift, open questions, suggested next cycle |
| Sources (16b) | Every `news.json` source with relevance meter, class, publisher, language, publish date, originating queries; sort by relevance/recency, official-only filter, search-budget and drop counts |
| Citations (16b) | `[s01]` / `[s01, s03]` resolve to links that jump to the source; unresolved ids render visibly unresolved rather than as dead text. Closes open decision #4 |
| Monitoring (16c) | Subscription and schedule kept visibly separate (a subscription can be active with no schedule); freshness window, schedule interval, pause/resume, manual refresh, cycles-run / last / next facts |
| Deltas (16c) | Refresh timeline with per-cycle outcome, cost and duration; artifacts load only when a cycle is opened; cycles that found nothing stay visible |
| Event wiring | Artifact groups (plan / report / monitor / deltas) with per-group invalidation, one in-flight fetch each, and a re-run when a change lands mid-fetch |
| Polish (16d) | New-since-last-visit badge (client-side, `src/lib/lastSeen.ts`), per-group skeletons, retryable errors, responsive two-column → single-column layout |
| Tests | 178 frontend (widget parse, citations, registry render, report, sources, monitor, deltas, stream wiring, SSE, API) |

**Still out of scope (unchanged):** global multi-topic dashboard, cross-topic
search, email/Slack alerts, in-UI plan editing, mobile-native apps.

**Verification status:** typecheck / lint / 75 frontend tests / 140 backend tests
pass, and the bundled `/app` mount was smoke-tested live against a local
`claude_agent`. The full journey in `testing/ui_smoke_16.md` still needs a run on
**test1** with a real agent — Docker was unavailable in the build environment.

## Acceptance criteria

`[x]` = delivered in 16a. `[~]` = built and unit-tested, awaiting the test1 smoke
run in `testing/ui_smoke_16.md`.

### Core journey
- [x] User creates topic from NL input without using curl
- [x] User sees live planning progress (stages/tools) via SSE
- [x] User reviews intro + query plan and clicks Proceed at gate
- [x] User sees deliver progress and reads finished report with sources
- [~] User enables monitoring and sees refresh cycles update the UI via events
- [~] User opens a refresh delta and sees new sources / updated report content

### Real-time & resilience
- [~] UI reconnects after tab sleep or network drop without losing event history (`from_seq`)
- [x] Artifact fetches triggered by relevant events, not fixed-interval polling of all endpoints
- [x] Terminal states (`reported`, `failed`, `cancelled`) reflected correctly; active refresh keeps stream open

### UX quality
- [~] Responsive layout usable on desktop and tablet widths
- [x] Loading skeletons / placeholders while artifacts are not yet available (404 handled gracefully)
- [x] Errors from SSE and API shown in context with topic state preserved

### Ops
- [x] Documented deploy path for at least one test slot (test1) — `testing/ui_smoke_16.md` §0
- [x] `docs/product/README.md` updated when UI is user-facing
- [x] Manual test scenario in `testing/` or short UI smoke checklist

## Out of scope (V1)

- Global multi-topic signals dashboard
- Backend user ownership & JWT wiring — **#24** (frontend consumes it here)
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
- `apps/signalgather_web/README.md` — the shipped app: stack, dev, deploy, design notes
- `testing/ui_smoke_16.md` — manual smoke checklist for the 16a journey
- `testing/app_testing_scenario.md` — reference flows the UI must replace
- `docs/specs/done/pilot_ops_v1_17.md` — backend pilot-ready work including `GET /v1/topics`
- `docs/specs/done/topic_user_ownership_24.md` — per-user topic ownership & access control
- `docs/specs/active/pilot_first_use_experience_37.md` — onboarding, recovery,
  return-use clarity, and pilot validation after phases 16a–b

## Open decisions — resolved at 16a kickoff

1. **App location in monorepo** — **`apps/signalgather_web/`** (monorepo; one
   deploy artifact with the API that serves it).
2. **Hosting URL** — **path on the existing agent host**: `/app` on
   `agent{,-test1,-test2}.particletico.com`. Same origin as the API means no CORS
   in the deployed path and no new Caddy vhost or certificate. A dedicated
   `app.particletico.com` stays possible later — set `CLAUDE_AGENT_CORS_ORIGINS`
   and point a vhost at the static bundle.
3. **Auth model V1** — **JWT** via `POST /auth/jwt/login` (#24); the SPA stores
   the Bearer token in `localStorage` and re-validates it against `/users/me` on
   load. `EventSource` was rejected for SSE because it cannot carry the header.
4. **Citation links** — **done in 16b** (`src/lib/citations.ts`). `[s01]` markers
   are rewritten into anchors that jump to the source row, on already-sanitized
   HTML and text nodes only, so code blocks and existing links are untouched. An
   id absent from `news.json` renders visibly unresolved.
