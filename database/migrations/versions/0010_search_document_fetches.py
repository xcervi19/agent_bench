"""newsfind: every fetch attempt per document, kept side by side.

Two paths read the same URL — our own HTTP client and the agent's WebFetch — and
they return different artifacts. `search_documents.content` keeps only the best
result; this table keeps them all, in order, with how long each one took. That
timing is what a later evaluation pass needs to judge which path is worth it.

Append-only: no update path writes here.

Revision ID: 0010_search_document_fetches
Revises: 0009_search_document_content
Create Date: 2026-08-06
"""

import sqlalchemy as sa
from alembic import op

revision = "0010_search_document_fetches"
down_revision = "0009_search_document_content"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "search_document_fetches",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("document_id", sa.BigInteger(), nullable=False),
        sa.Column("method", sa.String(length=16), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("content_chars", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("duration_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "finished_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.ForeignKeyConstraint(["document_id"], ["search_documents.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # Reading one document's attempts in order — the common access pattern.
    op.create_index(
        "ix_search_document_fetches_document",
        "search_document_fetches",
        ["document_id", "id"],
    )
    # Timing and success rate per path, without scanning the text.
    op.create_index(
        "ix_search_document_fetches_method_status",
        "search_document_fetches",
        ["method", "status"],
    )

    # Which path produced the text the document currently holds.
    op.add_column(
        "search_documents", sa.Column("fetch_method", sa.String(length=16), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("search_documents", "fetch_method")
    op.drop_index(
        "ix_search_document_fetches_method_status", table_name="search_document_fetches"
    )
    op.drop_index("ix_search_document_fetches_document", table_name="search_document_fetches")
    op.drop_table("search_document_fetches")
