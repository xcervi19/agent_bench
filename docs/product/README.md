# Product — Newsfind Topic Intelligence

**Brand:** SignalGather (business brief)  
**Shipped surface (V1):** Topic pipeline on `claude_agent`.

## What the product does

1. User defines a **macro topic** (e.g. Hormuz strait / LNG supply).
2. System **plans** — RAG context, entities, search queries, intro for human review.
3. User **approves** the plan.
4. System **delivers** — web search, sources, strategic `report.md`.
5. User **monitors** — periodic refresh for new news only (deltas, deduped).

**API:** `POST /v1/topics`, SSE `/events`, `/proceed`, `/monitor`, `/refresh`, artifact routes.  
**Public URL (prod):** `https://agent.particletico.com`  
**Web UI (#16a):** `/app` on the same host — sign-in, topic list, NL topic
creation, live activity, plan review + Proceed/Cancel. Report reading (16b) and
monitoring controls (16c) are still API-only.

## Shipped stack (main)

| Component | Role |
|-----------|------|
| `apps/claude_agent` | Topic pipeline + in-app refresh scheduler (#22); serves the UI at `/app` |
| `apps/signalgather_web` | SignalGather web UI (#16) — React SPA over the topic API |
| `apps/rag_adhoc` | RAG search during **plan**; `documents`/`events` models |
| `libs/agentic_core` | Auth/DB layer for **#24** |
| `source_ingest` / `oil_rag_collector` | RAG corpus ops (not user-facing) |
| `source_crawler` | Extensible crawl/download foundation — see `docs/architecture/source_crawler.md` and operator guide `docs/architecture/source_acquisition_pipeline.md` |
| `libs/eval_framework` | Lane A quality evaluation (#23) |

## Archived (not on main)

CrewAI **Signal Gather** (RSS → signals → briefings) — branch
`archive/signal_gather-platform`. See `docs/archive/README.md`.

## VPS environments

| Slot | Public URL | UI | Isolated |
|------|------------|----|----------|
| prod | `https://agent.particletico.com` | `/app` | DB `agentic`, own RAG |
| test1 | `https://agent-test1.particletico.com` | `/app` | DB `agentic_test1`, own RAG |
| test2 | `https://agent-test2.particletico.com` | `/app` | DB `agentic_test2`, own RAG |

**Auth:** the UI signs users in with a JWT (`POST /auth/jwt/login`, #24) and each
user sees only their own topics. Slots running the harness default
`CLAUDE_AGENT_ALLOW_SERVICE_KEY_BYPASS=true` treat unauthenticated callers as a
service role — set it to `false` on any slot used as a real product surface.

**Shared:** one Claude CLI login (`~/agent_bench/claude_home`), one Caddy.  
**Hidden:** Postgres, RAG host ports (no Redis/MinIO on slim compose).

## Docs

- Testing: `testing/app_testing_scenario.md`; UI smoke: `testing/ui_smoke_16.md`
- Web UI: `apps/signalgather_web/README.md`
- Architecture: `docs/specs/done/agentic_search_claude_code_architecture.md`
- Source crawler: `docs/architecture/source_crawler.md`
- Source acquisition pipeline: `docs/architecture/source_acquisition_pipeline.md`
- VPS ops: `docs/ops/vps.md`
- Business: `docs/specs/business_requirements/business_requirements.md`
