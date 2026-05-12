"""Claude Agent API: drive the Claude Code CLI behind HTTP.

Run:  uvicorn apps.claude_agent.app:app --host 0.0.0.0 --port 8002
"""

from __future__ import annotations

import logging
import sys
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from .config import get_settings
from .jobs import JobManager
from .routes import router
from .topics.db import is_configured as topics_db_configured
from .topics.events import EventBus
from .topics.orchestrator import TopicSupervisor
from .topics.routes import router as topics_router


def _configure_logging(level: str, app_env: str) -> None:
    log_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(stream=sys.stdout, level=log_level, format="%(message)s")

    processors: list = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    processors.append(
        structlog.dev.ConsoleRenderer()
        if app_env == "local"
        else structlog.processors.JSONRenderer()
    )

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


@asynccontextmanager
async def _lifespan(app: FastAPI):
    settings = get_settings()
    app.state.job_manager = JobManager(settings)

    # Topic pipeline (newsfind-pipeline-v1). Optional: only wires up when a
    # database URL is configured. The /v1/topics/* router gracefully returns
    # 503 when DB is not configured, so the rest of the API is unaffected.
    supervisor: TopicSupervisor | None = None
    if topics_db_configured(settings):
        bus = EventBus()
        supervisor = TopicSupervisor(settings, bus)
        app.state.topic_bus = bus
        app.state.topic_supervisor = supervisor
        try:
            resumed = await supervisor.resume_in_flight()
            if resumed:
                structlog.get_logger("claude_agent").info(
                    "claude_agent.topics.resumed", count=resumed
                )
        except Exception:
            structlog.get_logger("claude_agent").exception(
                "claude_agent.topics.resume_failed"
            )

    structlog.get_logger("claude_agent").info(
        "claude_agent.start",
        workspace_dir=settings.workspace_dir,
        claude_bin=settings.claude_bin,
        allowed_commands=settings.allowed_commands,
        topics_enabled=topics_db_configured(settings),
    )
    try:
        yield
    finally:
        if supervisor is not None:
            await supervisor.shutdown()


def build_app() -> FastAPI:
    settings = get_settings()
    _configure_logging(settings.log_level, settings.app_env)

    app = FastAPI(
        title="Claude Agent API",
        description=(
            "Headless Claude Code CLI behind FastAPI. Submit slash commands, "
            "stream events, manage jobs."
        ),
        version="0.1.0",
        lifespan=_lifespan,
    )

    @app.get("/healthz", tags=["health"])
    async def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/readyz", tags=["health"])
    async def readyz() -> dict[str, str]:
        from .runner import claude_version

        ver = await claude_version(get_settings())
        if not ver:
            return {"status": "degraded", "reason": "claude binary not available"}
        return {"status": "ready", "claude_version": ver}

    app.include_router(router)
    app.include_router(topics_router)
    return app


app = build_app()
