"""Deterministic seed scenario for commodity trading demo."""

from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

from agentic_core.database import session_scope, tenant_scope

from ..models import Event, Signal, UserProfile

DEMO_TENANT_ID = UUID("00000000-0000-0000-0000-000000000001")
DEMO_USER_ID = UUID("00000000-0000-0000-0000-000000000010")


async def seed() -> None:
    with tenant_scope(DEMO_TENANT_ID):
        async with session_scope() as db:
            db.add(_demo_profile())
            db.add_all(_demo_events())
            db.add_all(_demo_signals())


def _demo_profile() -> UserProfile:
    return UserProfile(
        id=uuid4(),
        tenant_id=DEMO_TENANT_ID,
        user_id=DEMO_USER_ID,
        display_name="Demo Trader",
        commodities=["power", "gas"],
        regions=["Europe"],
        themes=["supply disruption", "policy"],
        risk_appetite="medium",
        alert_channels=["web"],
        briefing_cadence="daily",
        impact_threshold=0.5,
        raw_setup_text=(
            "I trade European power and gas. Watch supply disruptions and EU policy. "
            "Send me morning briefings and instant alerts on high-impact events."
        ),
    )


def _demo_events() -> list[Event]:
    now = datetime.now(timezone.utc)
    return [
        Event(
            id=uuid4(),
            tenant_id=DEMO_TENANT_ID,
            category="supply_disruption",
            commodity="gas",
            region="Europe",
            occurred_at=now - timedelta(hours=5),
            summary="Unplanned Norwegian pipeline outage reduces gas flows to continental Europe.",
            entities={"operators": ["Gassco"], "countries": ["NO", "DE"]},
            impact_score=0.72,
        ),
        Event(
            id=uuid4(),
            tenant_id=DEMO_TENANT_ID,
            category="policy",
            commodity="power",
            region="Europe",
            occurred_at=now - timedelta(hours=30),
            summary="EU accelerates review of capacity market reforms; decision expected Q3.",
            entities={"institutions": ["European Commission"]},
            impact_score=0.4,
        ),
    ]


def _demo_signals() -> list[Signal]:
    return [
        Signal(
            id=uuid4(),
            tenant_id=DEMO_TENANT_ID,
            kind="price_pressure",
            commodity="gas",
            region="Europe",
            direction="bullish",
            confidence=0.68,
            rationale="Pipeline outage tightens balance; front-month likely supported.",
            event_ids=[],
        ),
    ]
