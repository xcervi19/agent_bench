"""Market signal — higher-level insight derived from one or more events."""

from uuid import UUID, uuid4

from sqlalchemy import JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from agentic_core.database import Base, TenantMixin, TimestampMixin


class Signal(Base, TenantMixin, TimestampMixin):
    __tablename__ = "signals"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    kind: Mapped[str] = mapped_column(String(64), nullable=False)
    commodity: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    region: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    direction: Mapped[str] = mapped_column(String(16), nullable=False)  # bullish/bearish/neutral
    confidence: Mapped[float] = mapped_column(nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    event_ids: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
