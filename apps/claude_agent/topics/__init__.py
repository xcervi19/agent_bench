"""Topic Pipeline Orchestrator v1 (newsfind-pipeline-v1).

This package wraps the existing Stage 1 ``/newsfind-queries`` slash command
in a multi-stage, async, API-first pipeline:

    queries (Stage 1) → intro (Stage 2) → [GATE] → search (Stage 3) → report (Stage 4)

Public entry points are exposed via :mod:`apps.claude_agent.topics.routes`
(included in :mod:`apps.claude_agent.app`). Each topic has:

* a row in Postgres (``topics``) with its current state machine state,
* an append-only event log (``topic_events``) used both for audit and SSE replay,
* a per-topic asyncio task driving stages forward,
* on-disk artifacts under ``state/news/<topic_id_hash>/runs/<run_id>/``.

The pipeline is designed so prompts can iterate freely (slash commands are just
markdown files) without forcing schema migrations: orchestration metadata stays
generic (``payload JSONB``) and every artifact JSON carries ``schema_version``.
"""
