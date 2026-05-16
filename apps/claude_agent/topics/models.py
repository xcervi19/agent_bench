import uuid
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class TopicsBase(DeclarativeBase):
    pass


class Topic(TopicsBase):
    __tablename__ = "topics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic: Mapped[str] = mapped_column(Text, nullable=False)
    state: Mapped[str] = mapped_column(String(32), nullable=False)
    topic_id_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    plan_run_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    deliver_run_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_event_seq: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )


class TopicEvent(TopicsBase):
    __tablename__ = "topic_events"
    __table_args__ = (UniqueConstraint("topic_id", "seq", name="uq_topic_events_topic_seq"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )
    seq: Mapped[int] = mapped_column(BigInteger, nullable=False)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())


class TopicWebhook(TopicsBase):
    __tablename__ = "topic_webhooks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )
    url: Mapped[str] = mapped_column(Text, nullable=False)
    secret: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())


class TopicSubscription(TopicsBase):
    """One row per topic that is being continuously monitored.

    Persists the short-term query plan, which is generated once when monitoring
    starts (from the original parsed.queries + report.next_queries + recency
    hints) and reused on every refresh. A user-driven external scheduler is
    expected to call POST /v1/topics/{id}/refresh on its own cadence — this
    table does not store an interval.
    """

    __tablename__ = "topic_subscriptions"
    __table_args__ = (UniqueConstraint("topic_id", name="uq_topic_subscriptions_topic_id"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="active")
    short_term_queries: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    max_age_hours: Mapped[int] = mapped_column(Integer, nullable=False, default=48)
    refresh_locked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    last_refresh_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_refresh_run_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    refresh_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )


class TopicRefreshDelta(TopicsBase):
    """One row per refresh cycle. Records what was new vs. the previous run."""

    __tablename__ = "topic_refresh_deltas"
    __table_args__ = (UniqueConstraint("topic_id", "seq", name="uq_topic_refresh_deltas_topic_seq"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )
    subscription_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("topic_subscriptions.id", ondelete="CASCADE"), nullable=False
    )
    seq: Mapped[int] = mapped_column(Integer, nullable=False)
    run_id: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)  # running|completed|failed
    new_sources_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    queries_executed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_cost_usd: Mapped[float | None] = mapped_column(nullable=True)
    summary_md: Mapped[str | None] = mapped_column(Text, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
