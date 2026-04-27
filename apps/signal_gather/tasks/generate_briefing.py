"""Generate a daily/weekly briefing for one user, persist as a Report row."""

from typing import Any
from uuid import UUID, uuid4

from agentic_core.agents import CrewRunContext
from agentic_core.database import session_scope
from agentic_core.workers import task

from ..agents import BriefingCrew
from ..models import Report
from ..services import collect_briefing
from ..services.briefings import BriefingBundle


@task("signal_gather.generate_briefing")
async def generate_briefing(tenant_id: UUID, payload: dict[str, Any]) -> dict[str, Any]:
    user_id = UUID(payload["user_id"])
    cadence = payload.get("cadence", "daily")

    bundle = await _collect(tenant_id, user_id, cadence)
    if bundle is None:
        return {"status": "no_profile"}

    body = await _write_briefing(tenant_id, bundle)
    report = await _persist_report(tenant_id, user_id, cadence, bundle, body)
    return {"status": "ok", "report_id": str(report.id)}


async def _collect(tenant_id: UUID, user_id: UUID, cadence: str) -> BriefingBundle | None:
    async with session_scope() as db:
        return await collect_briefing(db, tenant_id, user_id, cadence)


async def _write_briefing(tenant_id: UUID, bundle: BriefingBundle) -> str:
    inputs = {
        "profile": _profile_summary(bundle),
        "signals": [_signal_summary(s) for s in bundle.signals],
        "events": [_event_summary(e) for e in bundle.events],
        "window_hours": bundle.window_hours,
    }
    result = await BriefingCrew().run(CrewRunContext(tenant_id=tenant_id, inputs=inputs))
    return result.output.get("result", "") or ""


async def _persist_report(
    tenant_id: UUID, user_id: UUID, cadence: str, bundle: BriefingBundle, body: str
) -> Report:
    report = Report(
        id=uuid4(),
        tenant_id=tenant_id,
        user_id=user_id,
        kind=cadence,
        title=_title(bundle, cadence),
        body=body,
        signal_ids=[str(s.id) for s in bundle.signals],
        event_ids=[str(e.id) for e in bundle.events],
    )
    async with session_scope() as db:
        db.add(report)
    return report


def _title(bundle: BriefingBundle, cadence: str) -> str:
    name = bundle.profile.display_name or "Trader"
    return f"{cadence.title()} briefing — {name}"


def _profile_summary(bundle: BriefingBundle) -> dict[str, Any]:
    p = bundle.profile
    return {
        "commodities": p.commodities,
        "regions": p.regions,
        "themes": p.themes,
        "risk_appetite": p.risk_appetite,
    }


def _signal_summary(signal) -> dict[str, Any]:
    return {
        "kind": signal.kind,
        "commodity": signal.commodity,
        "region": signal.region,
        "direction": signal.direction,
        "confidence": signal.confidence,
        "rationale": signal.rationale,
    }


def _event_summary(event) -> dict[str, Any]:
    return {
        "category": event.category,
        "commodity": event.commodity,
        "region": event.region,
        "summary": event.summary,
        "impact_score": event.impact_score,
    }
