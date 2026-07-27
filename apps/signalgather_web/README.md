# SignalGather web — topic intelligence UI (#16)

React + TypeScript SPA over the shipped `claude_agent` topic API. No business
logic lives here: the app authenticates, reads the API, streams events, and
renders artifacts.

**Phases 16a–16d (this build):** sign in, topic list, natural-language topic
creation, and a topic workspace with live SSE activity and four sections —
Plan (review gate, Proceed/Cancel), Report, Sources, Monitoring (schedule,
manual refresh, delta timeline).

**Not built:** global multi-topic dashboard, cross-topic search, email/Slack
alerts, in-UI plan editing.

---

## How it is served

The bundle is baked into the `claude_agent` image and served by FastAPI at
**`/app`** — the same origin as the API, so the browser needs no CORS grant and
the JWT travels on a plain `Authorization` header.

| Piece | Where |
|---|---|
| SPA mount (`/app`, history fallback) | `_mount_web` in `apps/claude_agent/app.py` |
| CORS (only for a separately-served UI) | `_mount_cors` in the same file |
| Build stage | `web` stage in `docker/Dockerfile.claude_agent` |
| Settings | `CLAUDE_AGENT_WEB_DIST`, `CLAUDE_AGENT_CORS_ORIGINS` |

```
https://agent-test1.particletico.com/app        ← the UI
https://agent-test1.particletico.com/v1/topics  ← the API it calls
```

## Local development

```bash
cd apps/signalgather_web
npm install
npm run dev            # http://localhost:5173/app/
```

`vite dev` proxies `/v1`, `/auth`, `/users`, `/healthz`, `/readyz` to
`http://localhost:8002`, so dev is same-origin too and **no CORS setting is
required**. Point the proxy elsewhere with:

```bash
SIGNALGATHER_API_URL=https://agent-test1.particletico.com npm run dev
```

The **Environment** picker on the sign-in screen switches slot at runtime
(same-origin / local / test1 / test2 / prod). Switching signs you out — JWTs are
signed per deployment. If you pick a slot whose origin differs from the page,
that deployment must allow this origin:

```bash
CLAUDE_AGENT_CORS_ORIGINS=http://localhost:5173
```

## Scripts

| Command | Does |
|---|---|
| `npm run dev` | Dev server with API proxy |
| `npm run build` | `tsc -b` then `vite build` → `dist/` |
| `npm test` | Vitest (unit + component) |
| `npm run lint` | ESLint |
| `npm run typecheck` | `tsc -b` only |

## Layout

```
src/
├── lib/
│   ├── api.ts             typed API client; 404 = "artifact not ready yet"
│   ├── session.ts         JWT + selected API base (localStorage)
│   ├── sse.ts             fetch-based SSE reader: from_seq resume + backoff
│   ├── useTopicStream.ts  one topic's live model, by artifact group
│   ├── AuthContext.tsx    session bootstrap + sign in/out
│   ├── citations.ts       [s01] → links into the source list
│   ├── eventText.ts       event → one scannable feed line
│   ├── markdown.ts        marked + DOMPurify (prose only; agent output is untrusted)
│   ├── lastSeen.ts        client-side "new since your last visit"
│   ├── format.ts          relative/elapsed time helpers
│   ├── types.ts           API + artifact shapes
│   └── widgets/           widget contract (types.ts) + parser (parse.ts)
├── components/
│   ├── ArtifactMarkdown.tsx   prose + widgets + citations — the only artifact renderer
│   ├── widgets/registry.tsx   type → component; the one place a new widget lands
│   ├── report/                ReportView, SourcesPanel, ThesisBadge
│   ├── monitor/               MonitorPanel, DeltaTimeline
│   └── …                      StateBadge, ActivityFeed, PlanReview, QueryTable
├── pages/                 LoginPage, TopicListPage, TopicWorkspacePage
└── App.tsx / main.tsx     shell + routes (basename `/app`)
```

## Design notes

**Why not `EventSource`.** It cannot send an `Authorization` header, and
`/v1/topics/{id}/events` is owner-scoped (#24). `streamTopicEvents` uses fetch +
`ReadableStream` and parses the wire format itself.

**Reconnect contract.** The reader tracks the highest `seq` it delivered and
resumes with `?from_seq=<seq>`, so a drop replays nothing twice and skips
nothing. A `: done` comment means the server closed on purpose (terminal state)
and is *not* retried; any other end of body is a drop and backs off
500 ms → 10 s. On give-up the topic is re-read once so the badge still matches
the server.

**No polling.** Artifacts are fetched when an event says they exist
(`intro.ready` / `needs_input`), plus once on mount if `plan_run_id` is already
set — which covers reopening a topic whose gate was reached while you were away.

**Untrusted markdown.** Artifacts are written by an agent, so prose is rendered
through DOMPurify. `intro.json` backs the plan panel if the markdown is missing.

**Adaptive rendering.** The agent decides how a block of its output looks. It
emits a widget in the markdown:

````
```markdown-ui-widget
{"type": "entity-chips", "items": ["NIOC", "OPEC"]}
```
````

`ArtifactMarkdown` splits prose from widgets, renders prose as sanitized
markdown, resolves `[s01]` citations, and looks widgets up in
`components/widgets/registry.tsx`. **Adding a presentation is a validator branch
in `lib/widgets/parse.ts` plus one registry entry — no screen changes.** The
agent-facing contract is `claude_agent_fe/.claude/widgets.md`.

An unknown type or a bad payload renders a "cannot display" disclosure with the
reason and the raw payload. That is deliberate: an agent shipping a widget ahead
of the frontend must degrade visibly, never blank a section of a report.

Legacy `<EntityChips>` / `<Highlights>` / `<NewsCard/>` tags in artifacts already
on disk still render, mapped onto the same registry. Don't add tags to the
sanitizer whitelist to make new ones work — that re-creates the per-output-type
coupling the registry removes.

**Why not the `markdown-ui` library** (blueprintlab): closed widget set —
`Widget.tsx` dispatches through a hard-coded map over a static import with no
registration API — covering chat forms and quizzes, not report presentation, and
it renders without sanitization. Full evaluation in
`docs/specs/active/signalgather_frontend_v1_16.md` → "16b".

## Related

- `docs/specs/active/signalgather_frontend_v1_16.md` — the spec
- `docs/specs/done/topic_user_ownership_24.md` — JWT + per-user topics
- `testing/ui_smoke_16.md` — manual smoke checklist
