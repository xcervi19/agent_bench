from collections.abc import AsyncIterator
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from agentic_core.api.deps import get_db
from agentic_core.database import set_tenant_id
from .config import get_rag_settings


async def adhoc_tenant(
    x_tenant_id: Annotated[str | None, Header(alias="X-Tenant-Id")] = None,
    x_api_key: Annotated[str | None, Header()] = None,
) -> UUID:
    expected = get_rag_settings().api_key
    if expected and x_api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key")
    if not x_tenant_id:
        raise HTTPException(
            status_code=400, detail="Missing X-Tenant-Id (RLS tenant UUID, same as main app)."
        )
    try:
        tid = UUID(x_tenant_id.strip())
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid X-Tenant-Id") from e
    set_tenant_id(tid)
    return tid


async def get_adhoc_db(
    _tenant: UUID = Depends(adhoc_tenant),
) -> AsyncIterator[AsyncSession]:
    """Resolves adhoc_tenant first, then reuses the main app DB session (RLS from X-Tenant-Id)."""
    async for session in get_db():
        yield session
