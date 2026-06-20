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

## Shipped stack (main)

| Component | Role |
|-----------|------|
| `apps/claude_agent` | Topic pipeline + in-app refresh scheduler (#22) |
| `apps/rag_adhoc` | RAG search during **plan**; `documents`/`events` models |
| `libs/agentic_core` | Auth/DB layer for **#24** |
| `source_ingest` / `oil_rag_collector` | RAG corpus ops (not user-facing) |
| `libs/eval_framework` | Lane A quality evaluation (#23) |

## Archived (not on main)

CrewAI **Signal Gather** (RSS → signals → briefings) — branch
`archive/signal_gather-platform`. See `docs/archive/README.md`.

## VPS environments

| Slot | Public URL | Isolated |
|------|------------|----------|
| prod | `https://agent.particletico.com` | DB `agentic`, own RAG |
| test1 | `https://agent-test1.particletico.com` | DB `agentic_test1`, own RAG |
| test2 | `https://agent-test2.particletico.com` | DB `agentic_test2`, own RAG |

**Shared:** one Claude CLI login (`~/agent_bench/claude_home`), one Caddy.  
**Hidden:** Postgres, RAG host ports (no Redis/MinIO on slim compose).

## Docs

- Testing: `testing/app_testing_scenario.md`
- Architecture: `docs/specs/done/agentic_search_claude_code_architecture.md`
- VPS ops: `docs/ops/vps.md`
- Business: `docs/specs/business_requirements/business_requirements.md`
