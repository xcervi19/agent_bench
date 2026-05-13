"""newsfind topics: state machine + event log + webhooks.

Revision ID: 0003_newsfind_topics
Revises: 0002_signal_gather
Create Date: 2026-05-13
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
        sa.Column("state", sa.String(32), nullable=False),
        sa.Column("topic_id_hash", sa.String(64), nullable=False),
        sa.Column("plan_run_id", sa.String(64), nullable=True),
        sa.Column("deliver_run_id", sa.String(64), nullable=True),
        sa.Column("error", sa.Text, nullable=True),
        sa.Column("last_event_seq", sa.BigInteger, nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_topics_state", "topics", ["state"])

    op.create_table(
        "topic_events",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column(
            "topic_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("topics.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("seq", sa.BigInteger, nullable=False),
        sa.Column("event_type", sa.String(64), nullable=False),
        sa.Column("payload", postgresql.JSONB, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("topic_id", "seq", name="uq_topic_events_topic_seq"),
    )
    op.create_index("ix_topic_events_topic_id_seq", "topic_events", ["topic_id", "seq"])

    op.create_table(
        "topic_webhooks",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column(
            "topic_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("topics.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("url", sa.Text, nullable=False),
        sa.Column("secret", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_topic_webhooks_topic_id", "topic_webhooks", ["topic_id"])


def downgrade() -> None:
    op.drop_table("topic_webhooks")
    op.drop_table("topic_events")
    op.drop_table("topics")
