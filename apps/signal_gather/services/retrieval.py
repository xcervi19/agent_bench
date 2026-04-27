"""Semantic + structured retrieval over events (pgvector + filters + recency)."""

from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Event
from .embeddings import embed


async def search_events_by_text(
    db: AsyncSession,
    tenant_id: UUID,
    query: str,
    *,
    commodity: str | None = None,
    region: str | None = None,
    limit: int = 10,
) -> list[Event]:
    embedding = embed(query)
    if embedding is None:
        return await _filter_events(db, tenant_id, query, commodity, region, limit)
    return await _semantic_events(db, tenant_id, embedding, commodity, region, limit)


async def recent_events_for_profile(
    db: AsyncSession,
    tenant_id: UUID,
    *,
    commodities: list[str],
    regions: list[str],
    hours: int = 48,
    limit: int = 20,
) -> list[Event]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    stmt = select(Event).where(Event.tenant_id == tenant_id, Event.created_at >= cutoff)
    if commodities:
        stmt = stmt.where(Event.commodity.in_(commodities))
    if regions:
        stmt = stmt.where(Event.region.in_(regions))
    stmt = stmt.order_by(Event.created_at.desc()).limit(limit)

    return list((await db.execute(stmt)).scalars().all())


async def _semantic_events(
    db: AsyncSession,
    tenant_id: UUID,
    embedding: list[float],
    commodity: str | None,
    region: str | None,
    limit: int,
) -> list[Event]:
    stmt = select(Event).where(Event.tenant_id == tenant_id)
    if commodity:
        stmt = stmt.where(Event.commodity == commodity)
    if region:
        stmt = stmt.where(Event.region == region)
    stmt = stmt.order_by(Event.embedding.l2_distance(embedding)).limit(limit)

    return list((await db.execute(stmt)).scalars().all())


async def _filter_events(
    db: AsyncSession,
    tenant_id: UUID,
    query: str,
    commodity: str | None,
    region: str | None,
    limit: int,
) -> list[Event]:
    needle = f"%{query.strip()}%"
    stmt = select(Event).where(
        Event.tenant_id == tenant_id,
        or_(Event.summary.ilike(needle), Event.category.ilike(needle)),
    )
    if commodity:
        stmt = stmt.where(Event.commodity == commodity)
    if region:
        stmt = stmt.where(Event.region == region)
    stmt = stmt.order_by(Event.created_at.desc()).limit(limit)

    return list((await db.execute(stmt)).scalars().all())
