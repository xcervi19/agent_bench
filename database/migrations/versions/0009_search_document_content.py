"""newsfind: article text for captured search hits, plus the fetch outcome.

`fetch_status` doubles as the queue: NULL means "not attempted yet", and the
partial index backs the worker's pending lookup. Every other value is a recorded
outcome — `blocked`, `disallowed` and `not_found` are data about coverage, not
errors to be retried away.

Revision ID: 0009_search_document_content
Revises: 0008_search_evidence
Create Date: 2026-08-04
"""

import sqlalchemy as sa
from alembic import op

revision = "0009_search_document_content"
down_revision = "0008_search_evidence"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("search_documents", sa.Column("content", sa.Text(), nullable=True))
    op.add_column("search_documents", sa.Column("fetch_status", sa.String(length=16), nullable=True))
    op.add_column("search_documents", sa.Column("fetch_error", sa.Text(), nullable=True))
    op.add_column(
        "search_documents", sa.Column("fetched_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.create_index(
        "ix_search_documents_unfetched",
        "search_documents",
        ["first_seen_at"],
        postgresql_where=sa.text("fetch_status IS NULL"),
    )


def downgrade() -> None:
    op.drop_index("ix_search_documents_unfetched", table_name="search_documents")
    op.drop_column("search_documents", "fetched_at")
    op.drop_column("search_documents", "fetch_error")
    op.drop_column("search_documents", "fetch_status")
    op.drop_column("search_documents", "content")
