from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from agentic_core.api import get_db, require_tenant

from ..models import Signal
from ..schemas import SignalOut

router = APIRouter(prefix="/signals", tags=["signals"])


@router.get("", response_model=list[SignalOut])
async def list_signals(
    tenant_id: UUID = Depends(require_tenant),
    db: AsyncSession = Depends(get_db),
    commodity: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
) -> list[Signal]:
    stmt = select(Signal).where(Signal.tenant_id == tenant_id)
    if commodity:
        stmt = stmt.where(Signal.commodity == commodity)
    stmt = stmt.order_by(Signal.created_at.desc()).limit(limit)

    return list((await db.execute(stmt)).scalars().all())
