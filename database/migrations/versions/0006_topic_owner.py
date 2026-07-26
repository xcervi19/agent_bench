"""newsfind #24: per-user topic ownership.

owner_user_id is nullable: topics created before this migration and topics
created by the service key (ops smoke, eval harness) have no user. NULL owner
means "service-owned" — only service-key callers can read those rows.

Revision ID: 0006_topic_owner
Revises: 0005_topic_schedule
Create Date: 2026-07-25
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0006_topic_owner"
down_revision = "0005_topic_schedule"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "topics",
        sa.Column("owner_user_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_topics_owner_user_id",
        "topics",
        "users",
        ["owner_user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_index(
        "ix_topics_owner_updated_at",
        "topics",
        ["owner_user_id", sa.text("updated_at DESC")],
    )


def downgrade() -> None:
    op.drop_index("ix_topics_owner_updated_at", table_name="topics")
    op.drop_constraint("fk_topics_owner_user_id", "topics", type_="foreignkey")
    op.drop_column("topics", "owner_user_id")
