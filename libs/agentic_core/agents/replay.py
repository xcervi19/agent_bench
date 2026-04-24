"""Session recorder: every step of a crew run is persisted for later replay."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import JSON, DateTime, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base, TenantMixin, TimestampMixin, session_scope


class AgentSession(Base, TenantMixin, TimestampMixin):
    __tablename__ = "agent_sessions"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    crew: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="running", nullable=False)
    inputs: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    output: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error: Mapped[str | None] = mapped_column(String, nullable=True)


class AgentEvent(Base, TenantMixin):
    __tablename__ = "agent_events"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), index=True, nullable=False)
    kind: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )


@dataclass
class RecordedEvent:
    kind: str
    payload: dict[str, Any] = field(default_factory=dict)


class SessionRecorder:
    """Accumulates events in-memory, then flushes to DB at session end."""

    def __init__(self, session_id: UUID, tenant_id: UUID, crew: str) -> None:
        self.session_id = session_id
        self.tenant_id = tenant_id
        self.crew = crew
        self._events: list[RecordedEvent] = []

    def record(self, kind: str, **payload: Any) -> None:
        self._events.append(RecordedEvent(kind=kind, payload=payload))

    async def start(self, inputs: dict[str, Any]) -> None:
        async with session_scope() as s:
            s.add(
                AgentSession(
                    id=self.session_id,
                    tenant_id=self.tenant_id,
                    crew=self.crew,
                    status="running",
                    inputs=inputs,
                )
            )

    async def finish(self, output: dict[str, Any] | None = None, error: str | None = None) -> None:
        status = "failed" if error else "completed"
        async with session_scope() as s:
            await _update_session(s, self.session_id, status=status, output=output, error=error)
            await _persist_events(s, self)

    @property
    def events(self) -> list[RecordedEvent]:
        return list(self._events)


async def _update_session(session, session_id: UUID, **fields: Any) -> None:
    from sqlalchemy import update

    await session.execute(
        update(AgentSession).where(AgentSession.id == session_id).values(**fields)
    )


async def _persist_events(session, recorder: SessionRecorder) -> None:
    session.add_all(
        [
            AgentEvent(
                tenant_id=recorder.tenant_id,
                session_id=recorder.session_id,
                kind=event.kind,
                payload=event.payload,
            )
            for event in recorder.events
        ]
    )
