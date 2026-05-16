"""newsfind v2: topic subscriptions + refresh deltas.

Revision ID: 0004_newsfind_monitoring
Revises: 0003_newsfind_topics
Create Date: 2026-05-16
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0004_newsfind_monitoring"
down_revision = "0003_newsfind_topics"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "topic_subscriptions",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column(
            "topic_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("topics.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("status", sa.String(16), nullable=False, server_default=sa.text("'active'")),
        sa.Column("short_term_queries", postgresql.JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("max_age_hours", sa.Integer, nullable=False, server_default=sa.text("48")),
        sa.Column("refresh_locked", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("last_refresh_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_refresh_run_id", sa.String(64), nullable=True),
        sa.Column("refresh_count", sa.Integer, nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("topic_id", name="uq_topic_subscriptions_topic_id"),
    )
    op.create_index("ix_topic_subscriptions_status", "topic_subscriptions", ["status"])

    op.create_table(
        "topic_refresh_deltas",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column(
            "topic_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("topics.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "subscription_id",
            sa.BigInteger,
            sa.ForeignKey("topic_subscriptions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("seq", sa.Integer, nullable=False),
        sa.Column("run_id", sa.String(64), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("new_sources_count", sa.Integer, nullable=False, server_default=sa.text("0")),
        sa.Column("queries_executed", sa.Integer, nullable=False, server_default=sa.text("0")),
        sa.Column("duration_ms", sa.Integer, nullable=True),
        sa.Column("total_cost_usd", sa.Float, nullable=True),
        sa.Column("summary_md", sa.Text, nullable=True),
        sa.Column("error", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("topic_id", "seq", name="uq_topic_refresh_deltas_topic_seq"),
    )
    op.create_index(
        "ix_topic_refresh_deltas_topic_created",
        "topic_refresh_deltas",
        ["topic_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_table("topic_refresh_deltas")
    op.drop_table("topic_subscriptions")
