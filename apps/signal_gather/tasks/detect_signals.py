"""Sweep recent events, build signals (rules + agent), fan out alerts."""

from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import select

from agentic_core.agents import CrewRunContext
from agentic_core.database import session_scope
from agentic_core.workers import task

from ..agents import SignalEngineCrew
from ..agents.parsing import parse_json_object
from ..models import Event, Signal, UserProfile
from ..services import SignalProposal, detect_signals, fan_out_alert


@task("signal_gather.detect_signals")
async def detect_signals_task(tenant_id: UUID, payload: dict[str, Any]) -> dict[str, Any]:
    window_hours = int(payload.get("window_hours", 12))
    events = await _recent_events(tenant_id, window_hours)
    proposals = detect_signals(events)
    if not proposals:
        return {"signals": 0, "alerts": 0}

    signals = await _persist_signals(tenant_id, events, proposals)
    alerts = await _fan_out(tenant_id, signals)
    return {"signals": len(signals), "alerts": alerts}


async def _recent_events(tenant_id: UUID, window_hours: int) -> list[Event]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=window_hours)
    async with session_scope() as db:
        stmt = (
            select(Event)
            .where(Event.tenant_id == tenant_id, Event.created_at >= cutoff)
            .order_by(Event.created_at.desc())
        )
        return list((await db.execute(stmt)).scalars().all())


async def _persist_signals(
    tenant_id: UUID, events: list[Event], proposals: list[SignalProposal]
) -> list[Signal]:
    by_id = {e.id: e for e in events}
    refined = [await _refine(tenant_id, by_id, p) for p in proposals]

    async with session_scope() as db:
        signals = [_build_signal(tenant_id, p, r) for p, r in zip(proposals, refined, strict=True)]
        db.add_all(signals)
    return signals


async def _refine(
    tenant_id: UUID, by_id: dict[UUID, Event], proposal: SignalProposal
) -> dict[str, Any]:
    crew_inputs = {
        "events": [_event_summary(by_id[eid]) for eid in proposal.event_ids if eid in by_id],
        "rule_proposal": {
            "kind": proposal.kind,
            "direction": proposal.direction,
            "confidence": proposal.confidence,
            "rationale": proposal.rationale,
        },
    }
    result = await SignalEngineCrew().run(
        CrewRunContext(tenant_id=tenant_id, inputs=crew_inputs)
    )
    return parse_json_object(result.output)


def _build_signal(tenant_id: UUID, proposal: SignalProposal, refined: dict[str, Any]) -> Signal:
    return Signal(
        id=uuid4(),
        tenant_id=tenant_id,
        kind=refined.get("kind") or proposal.kind,
        commodity=proposal.commodity,
        region=proposal.region,
        direction=refined.get("direction") or proposal.direction,
        confidence=float(refined.get("confidence") or proposal.confidence),
        rationale=refined.get("rationale") or proposal.rationale,
        event_ids=[str(eid) for eid in proposal.event_ids],
    )


async def _fan_out(tenant_id: UUID, signals: list[Signal]) -> int:
    profiles = await _profiles_for_tenant(tenant_id)
    if not profiles:
        return 0

    alerts_sent = 0
    async with session_scope() as db:
        for signal in signals:
            for profile in profiles:
                if _matches_profile(signal, profile):
                    await fan_out_alert(db, tenant_id, profile, signal)
                    alerts_sent += 1
    return alerts_sent


async def _profiles_for_tenant(tenant_id: UUID) -> list[UserProfile]:
    async with session_scope() as db:
        stmt = select(UserProfile).where(UserProfile.tenant_id == tenant_id)
        return list((await db.execute(stmt)).scalars().all())


def _matches_profile(signal: Signal, profile: UserProfile) -> bool:
    if signal.confidence < profile.impact_threshold:
        return False
    if profile.commodities and signal.commodity not in profile.commodities:
        return False
    if profile.regions and signal.region not in profile.regions:
        return False
    return True


def _event_summary(event: Event) -> dict[str, Any]:
    return {
        "id": str(event.id),
        "category": event.category,
        "commodity": event.commodity,
        "region": event.region,
        "summary": event.summary,
        "impact_score": event.impact_score,
    }
