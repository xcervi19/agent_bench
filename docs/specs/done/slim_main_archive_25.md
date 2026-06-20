# Slim main — archive legacy stack — #25

**Status:** shipped  
**Lane:** Platform hygiene — remove deprecated code from `main`, preserve on archive branch

## Goal

`main` should reflect only the **shipped Newsfind product** (Claude Code topic
pipeline + RAG + eval). The CrewAI **Signal Gather** application and its
compose services move to a revival branch.

## Delivered

- Tag `archive/pre-slim-2026` and branch `archive/signal_gather-platform` at pre-cleanup `main`
- Removed `apps/signal_gather` from `main`; RAG models/services live under `apps/rag_adhoc/`
- Slim `docker-compose.yml`: `postgres`, `rag_adhoc`, `claude_agent` only
- Removed from `pyproject.toml`: `crewai`, `redis`, `rq`, `apscheduler`, `boto3`, `feedparser`
- Removed unused `agentic_core` modules: `workers/`, `scheduler/`, `storage/`, `crew_wrapper.py`
- Alembic `env.py` registers `rag_adhoc.models` instead of `signal_gather.models`
- Docs: `docs/archive/README.md`, product/ops updates

## Not in scope

- Dropping legacy DB tables (`signals`, `user_profiles`, …) — data preserved
- Migrating `#24` auth — `agentic_core` auth modules kept on `main`
- Reviving Signal Gather on `main`

## Acceptance

- [x] Archive ref pushed; `docs/archive/README.md` explains restore path
- [x] Local compose starts postgres + rag_adhoc + claude_agent
- [x] `source_ingest.ingest` and `rag_adhoc` search use `apps/rag_adhoc` models
- [x] Existing pytest suite passes
