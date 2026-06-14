"""newsfind #22: automatic refresh schedule fields on topic_subscriptions.

Adds opt-in scheduling so the in-app scheduler can fire periodic refreshes.
Scheduling is OFF by default (schedule_enabled defaults false); existing rows
keep manual-only behavior.

Revision ID: 0005_topic_schedule
Revises: 0004_newsfind_monitoring
Create Date: 2026-06-13
"""

import sqlalchemy as sa
from alembic import op

revision = "0005_topic_schedule"
down_revision = "0004_newsfind_monitoring"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "topic_subscriptions",
        sa.Column(
            "schedule_enabled",
            sa.Boolean,
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.add_column(
        "topic_subscriptions",
        sa.Column("schedule_interval_hours", sa.Integer, nullable=True),
    )
    op.add_column(
        "topic_subscriptions",
        sa.Column("next_refresh_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "topic_subscriptions",
        sa.Column("last_scheduled_refresh_at", sa.DateTime(timezone=True), nullable=True),
    )
    # Partial index over due, enabled subscriptions — keeps the scheduler scan cheap.
    op.create_index(
        "ix_topic_subscriptions_due",
        "topic_subscriptions",
        ["next_refresh_at"],
        postgresql_where=sa.text("schedule_enabled"),
    )


def downgrade() -> None:
    op.drop_index("ix_topic_subscriptions_due", table_name="topic_subscriptions")
    op.drop_column("topic_subscriptions", "last_scheduled_refresh_at")
    op.drop_column("topic_subscriptions", "next_refresh_at")
    op.drop_column("topic_subscriptions", "schedule_interval_hours")
    op.drop_column("topic_subscriptions", "schedule_enabled")
