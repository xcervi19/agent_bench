"""Cron callable: enqueue a briefing task for every active profile in a tenant."""

import asyncio
from uuid import UUID

from sqlalchemy import select

from agentic_core.database import session_scope, tenant_scope
from agentic_core.workers import enqueue

from ..models import UserProfile


def dispatch_daily_briefings(tenant_id: UUID) -> None:
    asyncio.run(_dispatch(tenant_id, cadence="daily"))


def dispatch_weekly_briefings(tenant_id: UUID) -> None:
    asyncio.run(_dispatch(tenant_id, cadence="weekly"))


async def _dispatch(tenant_id: UUID, cadence: str) -> None:
    profiles = await _profiles_with_cadence(tenant_id, cadence)
    for profile in profiles:
        enqueue(
            "signal_gather.generate_briefing",
            tenant_id=tenant_id,
            payload={"user_id": str(profile.user_id), "cadence": cadence},
        )


async def _profiles_with_cadence(tenant_id: UUID, cadence: str) -> list[UserProfile]:
    with tenant_scope(tenant_id):
        async with session_scope() as db:
            stmt = select(UserProfile).where(
                UserProfile.tenant_id == tenant_id,
                UserProfile.briefing_cadence == cadence,
            )
            return list((await db.execute(stmt)).scalars().all())
