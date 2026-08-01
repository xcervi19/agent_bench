"""newsfind #40: publish a topic for public, read-only sharing.

`is_public` is the whole authorization story for the anonymous read API: a row
is visible at /v1/public/topics/* when — and only when — this flag is true.
It is NOT NULL with a false server default so an existing row can never be
accidentally public, and so a caller that forgets the column still gets private.

`published_at` records when the snapshot was shared; the partial index backs the
public listing, which only ever scans published rows.

Revision ID: 0007_topic_public
Revises: 0006_topic_owner
Create Date: 2026-08-01
"""

import sqlalchemy as sa
from alembic import op

revision = "0007_topic_public"
down_revision = "0006_topic_owner"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "topics",
        sa.Column(
            "is_public",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.add_column(
        "topics",
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_topics_public_published_at",
        "topics",
        [sa.text("published_at DESC")],
        postgresql_where=sa.text("is_public"),
    )


def downgrade() -> None:
    op.drop_index("ix_topics_public_published_at", table_name="topics")
    op.drop_column("topics", "published_at")
    op.drop_column("topics", "is_public")
