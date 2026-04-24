"""Background task: generate a personalized insight for a user query."""

from typing import Any
from uuid import UUID

from sqlalchemy import select

from agentic_core.agents import CrewRunContext
from agentic_core.database import session_scope
from agentic_core.workers import task

from ..agents import PersonalizedTraderCrew
from ..models import Event, UserProfile


@task("signal_gather.generate_insight")
async def generate_insight(tenant_id: UUID, payload: dict[str, Any]) -> dict[str, Any]:
    profile = await _load_profile(tenant_id, payload.get("user_id"))
    evidence = await _load_recent_evidence(tenant_id, payload.get("commodity"), payload.get("region"))

    inputs = {
        "query": payload.get("query", ""),
        "profile": profile,
        "evidence": evidence,
    }
    result = await PersonalizedTraderCrew().run(CrewRunContext(tenant_id=tenant_id, inputs=inputs))

    return {"session_id": str(result.session_id), "output": result.output}


async def _load_profile(tenant_id: UUID, user_id: Any) -> dict[str, Any]:
    if user_id is None:
        return {}
    async with session_scope() as db:
        row = (
            await db.execute(
                select(UserProfile)
                .where(UserProfile.tenant_id == tenant_id, UserProfile.user_id == user_id)
            )
        ).scalar_one_or_none()
    if row is None:
        return {}
    return {
        "display_name": row.display_name,
        "commodities": row.commodities,
        "regions": row.regions,
        "themes": row.themes,
        "risk_appetite": row.risk_appetite,
    }


async def _load_recent_evidence(
    tenant_id: UUID, commodity: str | None, region: str | None, limit: int = 8
) -> list[dict[str, Any]]:
    stmt = select(Event).where(Event.tenant_id == tenant_id)
    if commodity:
        stmt = stmt.where(Event.commodity == commodity)
    if region:
        stmt = stmt.where(Event.region == region)
    stmt = stmt.order_by(Event.created_at.desc()).limit(limit)

    async with session_scope() as db:
        rows = (await db.execute(stmt)).scalars().all()

    return [{"id": str(e.id), "summary": e.summary, "commodity": e.commodity} for e in rows]
