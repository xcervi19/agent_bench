"""Reconstruct a past agent session for debugging / regression testing."""

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from sqlalchemy import select

from ..agents.replay import AgentEvent, AgentSession
from ..database import session_scope, tenant_scope


@dataclass
class ReplayedSession:
    id: UUID
    tenant_id: UUID
    crew: str
    status: str
    inputs: dict[str, Any]
    output: dict[str, Any] | None
    error: str | None
    events: list[dict[str, Any]]


async def load_session(session_id: UUID, *, tenant_id: UUID) -> ReplayedSession:
    with tenant_scope(tenant_id):
        async with session_scope() as s:
            session_row = (
                await s.execute(select(AgentSession).where(AgentSession.id == session_id))
            ).scalar_one()
            event_rows = (
                await s.execute(
                    select(AgentEvent)
                    .where(AgentEvent.session_id == session_id)
                    .order_by(AgentEvent.created_at)
                )
            ).scalars().all()

    return ReplayedSession(
        id=session_row.id,
        tenant_id=session_row.tenant_id,
        crew=session_row.crew,
        status=session_row.status,
        inputs=session_row.inputs,
        output=session_row.output,
        error=session_row.error,
        events=[{"kind": e.kind, "payload": e.payload} for e in event_rows],
    )
