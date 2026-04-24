from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from agentic_core.api import get_db, require_tenant

from ..models import Event
from ..schemas import EventOut

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[EventOut])
async def list_events(
    tenant_id: UUID = Depends(require_tenant),
    db: AsyncSession = Depends(get_db),
    commodity: str | None = Query(default=None),
    region: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
) -> list[Event]:
    stmt = select(Event).where(Event.tenant_id == tenant_id)
    if commodity:
        stmt = stmt.where(Event.commodity == commodity)
    if region:
        stmt = stmt.where(Event.region == region)
    stmt = stmt.order_by(Event.created_at.desc()).limit(limit)

    return list((await db.execute(stmt)).scalars().all())
