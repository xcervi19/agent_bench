# Product — Newsfind Topic Intelligence

**Brand:** SignalGather (business brief)  
**Shipped surface (V1):** Topic pipeline on `claude_agent` — not the full Signal Gather RSS/signals stack.

## What the product does

1. User defines a **macro topic** (e.g. Hormuz strait / LNG supply).
2. System **plans** — RAG context, entities, search queries, intro for human review.
3. User **approves** the plan.
4. System **delivers** — web search, sources, strategic `report.md`.
5. User **monitors** — periodic refresh for new news only (deltas, deduped).

**API:** `POST /v1/topics`, SSE `/events`, `/proceed`, `/monitor`, `/refresh`, artifact routes.  
**Public URL (prod):** `https://agent.particletico.com`

## In the repo but not the current product UI

| Area | Role |
|------|------|
| `libs/agentic_core` | Reusable platform |
| `apps/signal_gather` | RSS → events → signals → briefings (Iteration 1 README app) |
| `apps/rag_adhoc` | Internal search API; used during **plan** stage |
| `source_ingest` / `oil_rag_collector` | Build RAG corpus (ops, not user-facing) |
| `worker` / `scheduler` | Background jobs for signal_gather |

## VPS environments

| Slot | Public URL | Isolated |
|------|------------|----------|
| prod | `https://agent.particletico.com` | DB `agentic`, own RAG |
| test1 | `https://agent-test1.particletico.com` | DB `agentic_test1`, own RAG |
| test2 | `https://agent-test2.particletico.com` | DB `agentic_test2`, own RAG |

**Shared:** one Claude CLI login (`~/agent_bench/claude_home`), one Caddy.  
**Hidden:** Postgres, RAG host ports, Redis/MinIO (test slots run minimal stack).

## Docs

- Testing: `testing/app_testing_scenario.md`
- Architecture: `docs/specs/done/agentic_search_claude_code_architecture.md`
- VPS ops: `docs/ops/vps.md`
- Business: `docs/specs/business_requirements/business_requirements.md`
