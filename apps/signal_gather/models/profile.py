"""Trader profile: commodities/regions/themes + alert prefs + raw NL setup text."""

from uuid import UUID, uuid4

from sqlalchemy import JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from agentic_core.database import Base, TenantMixin, TimestampMixin


class UserProfile(Base, TenantMixin, TimestampMixin):
    __tablename__ = "user_profiles"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), unique=True, nullable=False)
    display_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    commodities: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    regions: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    themes: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    risk_appetite: Mapped[str] = mapped_column(String(16), default="medium", nullable=False)
    alert_channels: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    briefing_cadence: Mapped[str] = mapped_column(String(16), default="daily", nullable=False)
    impact_threshold: Mapped[float] = mapped_column(default=0.6, nullable=False)
    raw_setup_text: Mapped[str | None] = mapped_column(Text, nullable=True)
