# Development Status

_Update this file as work progresses. The agent reads it every session to understand current context._

---

## In Progress

### News Pipeline v2 — Subscribe & Refresh
- **Spec:** `docs/specs/active/news_pipeline_v2.md`
- **What's done:** API design, DB schema design, slash command spec (`/newsfind-refresh`)
- **What's missing:**
  - `apps/claude_agent/topics/scheduler.py` — background polling loop
  - `apps/claude_agent/topics/refresh.py` — single refresh cycle orchestration
  - `POST /v1/topics/{id}/subscribe` + `DELETE` + `GET /deltas` endpoints in `routes.py`
  - Alembic migration: `topic_subscriptions` + `topic_refresh_deltas` tables
  - `/newsfind-refresh` slash command in `claude_agent_fe/.claude/commands/`
- **Next step:** implement `scheduler.py` + `refresh.py`, then wire routes

---

## Known Bugs

### RAG env vars dropped on container recreate
- **Symptom:** `rag_context_refs: []` + `"RAG unavailable — no .env configuration found"`
- **Cause:** `docker compose up --force-recreate` drops env injection for `claude_agent`
- **Workaround:**
  ```bash
  docker compose up -d --force-recreate claude_agent
  docker compose exec claude_agent sh -lc 'env | grep -E "^RAG_"'
  # if blank: check docker-compose.yml env_file order for claude_agent
  ```
- **Full debug steps:** `docs/ops/debugging.md` → "RAG unavailable" section

---

## Recently Completed

| What | Date | Spec |
|---|---|---|
| **#10 RAG main corpus (highest ROI)** — download, chunk, ingest (66 docs / 3090 events) | May 22, 2026 | `docs/specs/done/rag_main_corpus_highest_roi_10.md` |
| Reproducible run artifacts + token-aware cache for `/newsfind-queries` | May 9–10, 2026 | `docs/specs/done/reproducible_artifacts_and_cache.md` |
| News pipeline v1 deployment to VPS (topic orchestrator + event stream) | May 2026 | `docs/specs/done/deployment_newsfind_pipeline_v1.md` |
| Non-root container user migration (UID 1001) | May 2026 | `docs/ops/debugging.md` |

---

## Blocked / Parked

_(nothing currently)_
