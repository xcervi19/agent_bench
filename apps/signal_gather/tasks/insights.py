"""Generate a personalized insight for a free-form user query."""

from typing import Any
from uuid import UUID

from sqlalchemy import select

from agentic_core.agents import CrewRunContext
from agentic_core.database import session_scope
from agentic_core.workers import task

from ..agents import PersonalizedTraderCrew
from ..models import Event, UserProfile
from ..services import search_events_by_text


@task("signal_gather.generate_insight")
async def generate_insight(tenant_id: UUID, payload: dict[str, Any]) -> dict[str, Any]:
    query = payload.get("query", "")
    commodity = payload.get("commodity")
    region = payload.get("region")
    user_id = payload.get("user_id")

    profile = await _load_profile(tenant_id, user_id)
    evidence = await _load_evidence(tenant_id, query, commodity, region)

    inputs = {"query": query, "profile": profile, "evidence": evidence}
    result = await PersonalizedTraderCrew().run(
        CrewRunContext(tenant_id=tenant_id, inputs=inputs)
    )
    return {"session_id": str(result.session_id), "output": result.output}


async def _load_profile(tenant_id: UUID, user_id: Any) -> dict[str, Any]:
    if user_id is None:
        return {}
    async with session_scope() as db:
        stmt = select(UserProfile).where(
            UserProfile.tenant_id == tenant_id, UserProfile.user_id == UUID(str(user_id))
        )
        row = (await db.execute(stmt)).scalar_one_or_none()
    if row is None:
        return {}
    return {
        "display_name": row.display_name,
        "commodities": row.commodities,
        "regions": row.regions,
        "themes": row.themes,
        "risk_appetite": row.risk_appetite,
    }


async def _load_evidence(
    tenant_id: UUID, query: str, commodity: str | None, region: str | None
) -> list[dict[str, Any]]:
    async with session_scope() as db:
        events = await search_events_by_text(
            db, tenant_id, query, commodity=commodity, region=region, limit=8
        )
    return [_event_summary(e) for e in events]


def _event_summary(event: Event) -> dict[str, Any]:
    return {
        "id": str(event.id),
        "summary": event.summary,
        "commodity": event.commodity,
        "region": event.region,
        "category": event.category,
        "impact_score": event.impact_score,
    }
