"""newsfind-pipeline-v1: topic orchestration tables.

Adds Postgres-backed orchestration metadata for the topic pipeline:

* ``topics`` — one row per topic, drives the state machine.
* ``topic_events`` — append-only event log, drives SSE replay + audit.
* ``topic_inputs`` — user steering messages (proceed / focus / clarify / constraint).
* ``topic_webhooks`` — B2B subscriber registrations.

These tables are intentionally generic (``payload JSONB``) so prompt and
schema iteration on the slash commands does not force migrations. They live
outside the agentic_core RLS-scoped tables (no ``tenant_id`` in v1).

Revision ID: 0003_newsfind_topics
Revises: 0002_signal_gather
Create Date: 2026-05-10
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0003_newsfind_topics"
down_revision = "0002_signal_gather"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "topics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("topic", sa.Text, nullable=False),
        sa.Column("topic_id_hash", sa.String(64), nullable=False),
        sa.Column("state", sa.String(64), nullable=False, server_default="created"),
        sa.Column("current_stage", sa.String(32), nullable=True),
        sa.Column("request", postgresql.JSONB, nullable=False),
        sa.Column("failed_at_stage", sa.String(32), nullable=True),
        sa.Column("error", sa.Text, nullable=True),
        sa.Column("error_type", sa.String(128), nullable=True),
        sa.Column("traceback", sa.Text, nullable=True),
        sa.Column("queries_run_id", sa.String(64), nullable=True),
        sa.Column("intro_run_id", sa.String(64), nullable=True),
        sa.Column("search_run_id", sa.String(64), nullable=True),
        sa.Column("report_run_id", sa.String(64), nullable=True),
        sa.Column(
            "last_event_seq",
            sa.BigInteger,
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_topics_topic_id_hash", "topics", ["topic_id_hash"])
    op.create_index("ix_topics_state", "topics", ["state"])

    op.create_table(
        "topic_events",
        sa.Column(
            "id", sa.BigInteger, primary_key=True, autoincrement=True
        ),
        sa.Column(
            "topic_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("topics.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("seq", sa.BigInteger, nullable=False),
        sa.Column("event_type", sa.String(64), nullable=False),
        sa.Column("event_version", sa.String(16), nullable=False, server_default="1"),
        sa.Column("payload", postgresql.JSONB, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.UniqueConstraint("topic_id", "seq", name="uq_topic_events_topic_seq"),
    )
    op.create_index(
        "ix_topic_events_topic_id_id", "topic_events", ["topic_id", "id"]
    )

    op.create_table(
        "topic_inputs",
        sa.Column(
            "id", sa.BigInteger, primary_key=True, autoincrement=True
        ),
        sa.Column(
            "topic_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("topics.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("kind", sa.String(32), nullable=False),
        sa.Column("payload", postgresql.JSONB, nullable=False),
        sa.Column("consumed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_index(
        "ix_topic_inputs_topic_consumed",
        "topic_inputs",
        ["topic_id", "consumed_at"],
    )

    op.create_table(
        "topic_webhooks",
        sa.Column(
            "id", sa.BigInteger, primary_key=True, autoincrement=True
        ),
        sa.Column(
            "topic_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("topics.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("url", sa.Text, nullable=False),
        sa.Column("secret", sa.Text, nullable=True),
        sa.Column("event_filter", postgresql.ARRAY(sa.Text), nullable=True),
        sa.Column(
            "delivery_failures",
            sa.Integer,
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "last_delivered_seq",
            sa.BigInteger,
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("disabled_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_topic_webhooks_topic_id", "topic_webhooks", ["topic_id"])


def downgrade() -> None:
    op.drop_index("ix_topic_webhooks_topic_id", table_name="topic_webhooks")
    op.drop_table("topic_webhooks")

    op.drop_index("ix_topic_inputs_topic_consumed", table_name="topic_inputs")
    op.drop_table("topic_inputs")

    op.drop_index("ix_topic_events_topic_id_id", table_name="topic_events")
    op.drop_table("topic_events")

    op.drop_index("ix_topics_state", table_name="topics")
    op.drop_index("ix_topics_topic_id_hash", table_name="topics")
    op.drop_table("topics")
