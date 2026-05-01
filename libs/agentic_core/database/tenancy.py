"""Tenant context propagated from JWT/worker job down to Postgres RLS policies."""

from contextlib import contextmanager
from contextvars import ContextVar
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

_tenant_ctx: ContextVar[UUID | None] = ContextVar("tenant_id", default=None)


def current_tenant_id() -> UUID | None:
    return _tenant_ctx.get()


def set_tenant_id(tenant_id: UUID | None) -> None:
    _tenant_ctx.set(tenant_id)


@contextmanager
def tenant_scope(tenant_id: UUID):
    token = _tenant_ctx.set(tenant_id)
    try:
        yield
    finally:
        _tenant_ctx.reset(token)


async def apply_tenant_to_session(session: AsyncSession) -> None:
    """Push current tenant into the DB session so RLS policies can read it."""
    tenant_id = current_tenant_id()
    if tenant_id is None:
        return
    # SET LOCAL does not accept prepared-statement placeholders ($1); inline UUID is safe here.
    await session.execute(text(f"SET LOCAL app.tenant_id = '{tenant_id}'"))
