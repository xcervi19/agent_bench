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
    # FK -> users.id lives in the DB (migration 0006); users is on a different
    # declarative Base, so it is not declared here.
    owner_user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    topic: Mapped[str] = mapped_column(Text, nullable=False)
    state: Mapped[str] = mapped_column(String(32), nullable=False)
    topic_id_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    plan_run_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    deliver_run_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_event_seq: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    # Sharing (#40). is_public is the only thing the anonymous read API consults:
    # true means "this snapshot is world-readable and frozen", false means the
    # row does not exist as far as /v1/public/* is concerned. Default false so a
    # topic is private unless its owner says otherwise.
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
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
    hints) and reused on every refresh.

    Refresh can be driven two ways (#22):
      - **Manual:** POST /v1/topics/{id}/refresh (always available).
      - **Scheduled:** when `schedule_enabled` is true, the in-app scheduler
        fires a refresh every `schedule_interval_hours`. Scheduling is OFF by
        default; enabling it requires an interval.
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
    # --- automatic scheduling (#22): off by default ---
    schedule_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    schedule_interval_hours: Mapped[int | None] = mapped_column(Integer, nullable=True)
    next_refresh_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_scheduled_refresh_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )


class SearchDocument(TopicsBase):
    """One row per distinct URL that web search has ever returned for a topic.

    Deduplicated so a document read by the later evaluation pass costs one read,
    no matter how many refresh cycles surfaced it. `url_hash` uses the same
    sha1(url)[:16] convention as `news.json#sources`, so the evidence store joins
    to the delivered report by URL identity — that join is what later tells us
    whether a hit was used, without recording any verdict at capture time.
    """

    __tablename__ = "search_documents"
    __table_args__ = (UniqueConstraint("topic_id", "url_hash", name="uq_search_documents_topic_url"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )
    url: Mapped[str] = mapped_column(Text, nullable=False)
    url_hash: Mapped[str] = mapped_column(String(16), nullable=False)
    domain: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str | None] = mapped_column(Text, nullable=True)
    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    # Best text we hold for this URL, and the outcome that produced it. A NULL
    # `fetch_status` is the queue: it means "not attempted yet". Every other value
    # is a recorded outcome — blocks and paywalls included, because which sources
    # we can never read is itself a finding about coverage, not a failure to hide.
    #
    # This is a projection, not the record. Every individual attempt — including
    # the ones that lost — lives in `search_document_fetches`.
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    fetch_status: Mapped[str | None] = mapped_column(String(16), nullable=True)
    fetch_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    fetched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    fetch_method: Mapped[str | None] = mapped_column(String(16), nullable=True)


class SearchDocumentFetch(TopicsBase):
    """Append-only: one row per attempt to read a document, whoever made it.

    Two paths reach the same URL — our own HTTP client and the agent's WebFetch —
    and they return different artifacts: raw HTML we extracted ourselves versus
    text the agent already processed. Collapsing both into the document's single
    `content` column would lose which one produced what, so every attempt is kept
    side by side here and the document keeps only the best of them.

    Never updated. Ordering within a document is `id` (monotonic, so two attempts
    in the same millisecond still sort deterministically); `duration_ms` is what
    later tells us which path is worth the wait.
    """

    __tablename__ = "search_document_fetches"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    document_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("search_documents.id", ondelete="CASCADE"), nullable=False
    )
    # "http" (our client) or "agent" (the model's WebFetch). Distinct because the
    # text they yield is not the same kind of artifact.
    method: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Denormalised so coverage and ranking queries never pull the text itself.
    content_chars: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    duration_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    finished_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class SearchObservation(TopicsBase):
    """Append-only: one row every time a query returned a document, at a rank.

    Never updated, never deduplicated — this is the record of how search behaved
    over time, which is a different question from what the corpus contains.
    """

    __tablename__ = "search_observations"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )
    document_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("search_documents.id", ondelete="CASCADE"), nullable=False
    )
    run_id: Mapped[str] = mapped_column(String(64), nullable=False)
    query: Mapped[str] = mapped_column(Text, nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
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
