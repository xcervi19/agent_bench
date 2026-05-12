"""SQLAlchemy ORM models for topic orchestration.

These tables live in the same Postgres as agentic_core but are intentionally
NOT registered with ``agentic_core.database.Base`` — they have their own
``Base`` to keep claude_agent decoupled. Migration: ``database/migrations/
versions/0003_newsfind_topics.py``.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class TopicsBase(DeclarativeBase):
    """Dedicated declarative base so we never accidentally cross-pollinate with
    agentic_core's metadata (which contains RLS-aware tenant tables)."""


class Topic(TopicsBase):
    __tablename__ = "topics"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    topic: Mapped[str] = mapped_column(Text, nullable=False)
    topic_id_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    state: Mapped[str] = mapped_column(String(64), nullable=False, default="created")
    current_stage: Mapped[str | None] = mapped_column(String(32), nullable=True)
    request: Mapped[dict] = mapped_column(JSONB, nullable=False)
    failed_at_stage: Mapped[str | None] = mapped_column(String(32), nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_type: Mapped[str | None] = mapped_column(String(128), nullable=True)
    traceback: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Per-stage run_id pointers (file-system artifact lookups).
    queries_run_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    intro_run_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    search_run_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    report_run_id: Mapped[str | None] = mapped_column(String(64), nullable=True)

    last_event_seq: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    archived_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    events: Mapped[list["TopicEvent"]] = relationship(
        back_populates="topic_obj",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class TopicEvent(TopicsBase):
    __tablename__ = "topic_events"
    __table_args__ = (
        UniqueConstraint("topic_id", "seq", name="uq_topic_events_topic_seq"),
        Index("ix_topic_events_topic_id_id", "topic_id", "id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("topics.id", ondelete="CASCADE"),
        nullable=False,
    )
    seq: Mapped[int] = mapped_column(BigInteger, nullable=False)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    event_version: Mapped[str] = mapped_column(String(16), nullable=False, default="1")
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    topic_obj: Mapped[Topic] = relationship(back_populates="events")


class TopicInput(TopicsBase):
    __tablename__ = "topic_inputs"
    __table_args__ = (
        Index("ix_topic_inputs_topic_consumed", "topic_id", "consumed_at"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("topics.id", ondelete="CASCADE"),
        nullable=False,
    )
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    consumed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class TopicWebhook(TopicsBase):
    __tablename__ = "topic_webhooks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("topics.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    url: Mapped[str] = mapped_column(Text, nullable=False)
    secret: Mapped[str | None] = mapped_column(Text, nullable=True)
    event_filter: Mapped[list[str] | None] = mapped_column(ARRAY(Text), nullable=True)
    delivery_failures: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_delivered_seq: Mapped[int] = mapped_column(
        BigInteger, nullable=False, default=0
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    disabled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
