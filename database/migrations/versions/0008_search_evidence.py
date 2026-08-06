"""newsfind: persist every web-search hit per topic, unfiltered and unjudged.

`search_documents` is deduplicated per (topic, url); `search_observations` is
append-only, one row per (query, run, rank) sighting. No verdict column by
design — whether a hit was worth anything is decided by a later evaluation pass,
and the join back to `news.json#sources` on `url_hash` recovers what was used.

Revision ID: 0008_search_evidence
Revises: 0007_topic_public
Create Date: 2026-08-02
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0008_search_evidence"
down_revision = "0007_topic_public"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "search_documents",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("topic_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("url_hash", sa.String(length=16), nullable=False),
        sa.Column("domain", sa.String(length=255), nullable=False),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("first_seen_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["topic_id"], ["topics.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("topic_id", "url_hash", name="uq_search_documents_topic_url"),
    )
    op.create_index("ix_search_documents_topic_domain", "search_documents", ["topic_id", "domain"])

    op.create_table(
        "search_observations",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("topic_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("document_id", sa.BigInteger(), nullable=False),
        sa.Column("run_id", sa.String(length=64), nullable=False),
        sa.Column("query", sa.Text(), nullable=False),
        sa.Column("rank", sa.Integer(), nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["topic_id"], ["topics.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["document_id"], ["search_documents.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_search_observations_topic_run", "search_observations", ["topic_id", "run_id"])
    op.create_index("ix_search_observations_document", "search_observations", ["document_id"])


def downgrade() -> None:
    op.drop_table("search_observations")
    op.drop_table("search_documents")
