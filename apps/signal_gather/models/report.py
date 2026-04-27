"""Briefing/report generated for a user profile (daily, weekly, ad-hoc)."""

from uuid import UUID, uuid4

from sqlalchemy import JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from agentic_core.database import Base, TenantMixin, TimestampMixin


class Report(Base, TenantMixin, TimestampMixin):
    __tablename__ = "reports"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), index=True, nullable=True)
    kind: Mapped[str] = mapped_column(String(32), nullable=False)  # daily/weekly/adhoc
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    signal_ids: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    event_ids: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
