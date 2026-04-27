"""Assemble the inputs for a daily/weekly briefing for one user."""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Event, Signal, UserProfile


@dataclass
class BriefingBundle:
    profile: UserProfile
    signals: list[Signal]
    events: list[Event]
    window_hours: int


WINDOW_FOR_CADENCE = {"daily": 24, "weekly": 24 * 7}


async def collect_briefing(
    db: AsyncSession, tenant_id: UUID, user_id: UUID, cadence: str
) -> BriefingBundle | None:
    profile = await _load_profile(db, tenant_id, user_id)
    if profile is None:
        return None

    window = WINDOW_FOR_CADENCE.get(cadence, 24)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=window)

    signals = await _recent_signals(db, tenant_id, profile, cutoff)
    events = await _recent_events(db, tenant_id, profile, cutoff)

    return BriefingBundle(profile=profile, signals=signals, events=events, window_hours=window)


async def _load_profile(db: AsyncSession, tenant_id: UUID, user_id: UUID) -> UserProfile | None:
    stmt = select(UserProfile).where(
        UserProfile.tenant_id == tenant_id, UserProfile.user_id == user_id
    )
    return (await db.execute(stmt)).scalar_one_or_none()


async def _recent_signals(
    db: AsyncSession, tenant_id: UUID, profile: UserProfile, cutoff: datetime
) -> list[Signal]:
    stmt = select(Signal).where(Signal.tenant_id == tenant_id, Signal.created_at >= cutoff)
    if profile.commodities:
        stmt = stmt.where(Signal.commodity.in_(profile.commodities))
    if profile.regions:
        stmt = stmt.where(Signal.region.in_(profile.regions))
    stmt = stmt.order_by(Signal.confidence.desc()).limit(20)
    return list((await db.execute(stmt)).scalars().all())


async def _recent_events(
    db: AsyncSession, tenant_id: UUID, profile: UserProfile, cutoff: datetime
) -> list[Event]:
    stmt = select(Event).where(Event.tenant_id == tenant_id, Event.created_at >= cutoff)
    if profile.commodities:
        stmt = stmt.where(Event.commodity.in_(profile.commodities))
    if profile.regions:
        stmt = stmt.where(Event.region.in_(profile.regions))
    stmt = stmt.order_by(Event.created_at.desc()).limit(40)
    return list((await db.execute(stmt)).scalars().all())
