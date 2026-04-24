"""Semantic + structured retrieval over events (pgvector)."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Event


async def search_similar_events(
    db: AsyncSession,
    tenant_id: UUID,
    embedding: list[float],
    *,
    commodity: str | None = None,
    region: str | None = None,
    limit: int = 10,
) -> list[Event]:
    stmt = select(Event).where(Event.tenant_id == tenant_id)
    if commodity:
        stmt = stmt.where(Event.commodity == commodity)
    if region:
        stmt = stmt.where(Event.region == region)
    stmt = stmt.order_by(Event.embedding.l2_distance(embedding)).limit(limit)

    return list((await db.execute(stmt)).scalars().all())
