"""Lightweight async SQLAlchemy session for the claude_agent topics package.

We deliberately keep this independent of ``agentic_core.database`` because
``agentic_core.config`` requires settings (Redis, S3, ...) that the
claude_agent service does not own. The same physical Postgres is shared.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from functools import lru_cache

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ..config import ClaudeAgentSettings, get_settings


class DatabaseNotConfigured(RuntimeError):
    """Raised when topic endpoints are called without ``CLAUDE_AGENT_DATABASE_URL``."""


@lru_cache
def get_engine() -> AsyncEngine:
    settings = get_settings()
    if not settings.database_url:
        raise DatabaseNotConfigured(
            "CLAUDE_AGENT_DATABASE_URL is empty; /v1/topics/* requires Postgres."
        )
    return create_async_engine(
        settings.database_url,
        pool_pre_ping=True,
        future=True,
        # SSE keeps a session open while streaming; never expire/refresh on commit.
    )


@lru_cache
def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        get_engine(),
        expire_on_commit=False,
        class_=AsyncSession,
    )


@asynccontextmanager
async def session_scope() -> AsyncIterator[AsyncSession]:
    """Transactional session. Commits on clean exit, rolls back on exception."""
    maker = get_sessionmaker()
    async with maker() as session:
        async with session.begin():
            yield session


@asynccontextmanager
async def read_session() -> AsyncIterator[AsyncSession]:
    """Read-only session that does NOT begin a transaction (useful for SSE)."""
    maker = get_sessionmaker()
    async with maker() as session:
        yield session


def is_configured(settings: ClaudeAgentSettings | None = None) -> bool:
    s = settings or get_settings()
    return bool(s.database_url)
