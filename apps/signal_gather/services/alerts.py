"""Alert delivery.

Web channel = persisting an Alert row (UI polls). Email/chat are stubs that
log the intent; production transports plug in here behind a single function.
"""

from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from agentic_core.logging import get_logger

from ..models import Alert, Signal, UserProfile

log = get_logger(__name__)


async def fan_out_alert(
    db: AsyncSession,
    tenant_id: UUID,
    profile: UserProfile,
    signal: Signal,
) -> Alert:
    alert = Alert(
        id=uuid4(),
        tenant_id=tenant_id,
        user_id=profile.user_id,
        signal_id=signal.id,
        severity=_severity(signal.confidence),
        title=_title(signal),
        body=signal.rationale,
        channels=profile.alert_channels,
        delivered=False,
    )
    db.add(alert)
    await db.flush()

    _deliver(alert, profile.alert_channels)
    alert.delivered = True
    return alert


def _severity(confidence: float) -> str:
    if confidence >= 0.8:
        return "critical"
    if confidence >= 0.6:
        return "warning"
    return "info"


def _title(signal: Signal) -> str:
    parts = [signal.kind]
    if signal.commodity:
        parts.append(signal.commodity)
    if signal.region:
        parts.append(signal.region)
    return " · ".join(parts)


def _deliver(alert: Alert, channels: list[str]) -> None:
    for channel in channels or ["web"]:
        log.info("alert.deliver", channel=channel, alert_id=str(alert.id), title=alert.title)
