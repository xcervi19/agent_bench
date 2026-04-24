"""Trader profile: commodities/regions/themes they care about."""

from uuid import UUID, uuid4

from sqlalchemy import JSON, String
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
