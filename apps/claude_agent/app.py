"""Claude Agent API: drive the Claude Code CLI behind HTTP.

Run:  uvicorn apps.claude_agent.app:app --host 0.0.0.0 --port 8002
"""

from __future__ import annotations

import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import structlog
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .config import ClaudeAgentSettings, get_settings
from .jobs import JobManager
from .routes import router


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


def _warn_on_disabled_pipeline_commands(settings: ClaudeAgentSettings) -> None:
    """Surface an allowlist that silently disables part of the topic pipeline.

    Deployments set `CLAUDE_AGENT_ALLOWED_COMMANDS` in their own `.env`, which
    replaces the defaults in `config.py` wholesale. A leg added to the pipeline
    but not to that list degrades quietly instead of erroring, so the only clue
    is a report that looks thin. Say it once, loudly, at boot.
    """
    if not settings.allowed_commands:  # empty list means allow all
        return
    from .topics.pipeline import PIPELINE_COMMANDS
    from .topics.refresh import REFRESH_COMMAND

    required = (*PIPELINE_COMMANDS, REFRESH_COMMAND)
    missing = [c for c in required if c not in settings.allowed_commands]
    if missing:
        structlog.get_logger("claude_agent").warning(
            "claude_agent.pipeline_commands_not_allowed",
            missing=missing,
            hint="add them to CLAUDE_AGENT_ALLOWED_COMMANDS; those stages will degrade",
        )


def _warn_on_open_topic_api(settings: ClaudeAgentSettings) -> None:
    """Shout when /v1/topics/* is readable with no credentials at all.

    `_service_key_accepted` treats an empty `api_key` as "accept everyone" while
    the bypass is on, so a config slip that blanks the key turns every caller
    into the service principal — which sees *all* topics, not just its own. That
    happened on prod: `environment:` in docker-compose overrode the key from
    env_file with "". Nothing failed, nothing 500'd; the API simply answered
    strangers. Boot-time noise is the cheapest place to catch it.
    """
    if not settings.database_url:  # topic API not mounted at all
        return
    if settings.allow_service_key_bypass and not settings.api_key:
        structlog.get_logger("claude_agent").error(
            "claude_agent.topic_api_unauthenticated",
            hint=(
                "service-key bypass is on with an empty CLAUDE_AGENT_API_KEY: every "
                "anonymous caller is the service role and can read all topics. Set "
                "CLAUDE_AGENT_API_KEY, or CLAUDE_AGENT_ALLOW_SERVICE_KEY_BYPASS=false "
                "for a product deployment."
            ),
        )


@asynccontextmanager
async def _lifespan(app: FastAPI):
    settings = get_settings()
    app.state.job_manager = JobManager(settings)
    structlog.get_logger("claude_agent").info(
        "claude_agent.start",
        workspace_dir=settings.workspace_dir,
        claude_bin=settings.claude_bin,
        allowed_commands=settings.allowed_commands,
    )
    _warn_on_disabled_pipeline_commands(settings)
    _warn_on_open_topic_api(settings)

    app.state.scheduler = None
    if settings.database_url and settings.scheduler_enabled:
        from .topics.scheduler import RefreshScheduler

        scheduler = RefreshScheduler(settings)
        scheduler.start()
        app.state.scheduler = scheduler

    try:
        yield
    finally:
        if app.state.scheduler is not None:
            await app.state.scheduler.stop()


def _mount_cors(app: FastAPI, settings: ClaudeAgentSettings) -> None:
    """Allow a separately-served UI origin (#16) — e.g. `vite dev` on :5173.

    Credentials stay off: the SPA sends a Bearer token, not cookies, so a
    wildcard origin remains legal here.
    """
    if not settings.cors_origins:
        return
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Type"],
    )


def _mount_web(app: FastAPI, settings: ClaudeAgentSettings) -> None:
    """Serve the built SPA at /app so the UI shares the API origin (no CORS).

    Unknown /app/* paths fall back to index.html — client-side routes like
    /app/topics/<uuid> must survive a hard reload.
    """
    if not settings.web_dist:
        return
    dist = Path(settings.web_dist)
    index = dist / "index.html"
    if not index.is_file():
        structlog.get_logger("claude_agent").warning(
            "claude_agent.web_dist_missing", web_dist=str(dist)
        )
        return

    if (dist / "assets").is_dir():
        app.mount("/app/assets", StaticFiles(directory=str(dist / "assets")), name="web-assets")

    @app.get("/app", include_in_schema=False)
    @app.get("/app/{path:path}", include_in_schema=False)
    async def spa(path: str = "") -> FileResponse:
        candidate = (dist / path).resolve()
        if path and dist.resolve() in candidate.parents and candidate.is_file():
            return FileResponse(str(candidate))
        return FileResponse(str(index), media_type="text/html; charset=utf-8")

    structlog.get_logger("claude_agent").info("claude_agent.web_mounted", web_dist=str(dist))


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

    _mount_cors(app, settings)

    app.include_router(router)
    if settings.database_url:
        from .auth import bootstrap_auth_env

        bootstrap_auth_env()

        from agentic_core.api import build_auth_routers

        from .topics.routes import router as topics_router

        for auth_router in build_auth_routers():
            app.include_router(auth_router)
        app.include_router(topics_router)

    _mount_web(app, settings)
    return app


app = build_app()
