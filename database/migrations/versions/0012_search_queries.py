"""newsfind: record every search call, including the ones that returned nothing.

`search_observations` can only hold a query that produced a hit, so a search that
came back empty left no trace at all — making "we asked and got nothing" look
exactly like "nobody asked". Those two need opposite fixes, so they have to be
distinguishable.

The same row carries the call's domain filter. Once the whitelist is handed to
WebSearch as `allowed_domains` (#46 build item 0), the filter becomes the most
important fact about a search: a domain that never appeared in an
`allowed_domains` list was never reachable, however the query was worded. Adding
the column before the filter ships is deliberate — the other order destroys the
diagnostic while fixing the yield.

Revision ID: 0012_search_queries
Revises: 0011_refresh_tokens
Create Date: 2026-08-22
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0012_search_queries"
down_revision = "0011_refresh_tokens"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "search_queries",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("topic_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("run_id", sa.String(length=64), nullable=False),
        sa.Column("query", sa.Text(), nullable=False),
        # NULL = no filter on the call; an empty array = a filter that allows
        # nothing. Keep them apart.
        sa.Column("allowed_domains", postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column("blocked_domains", postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column("hit_count", sa.Integer(), nullable=False),
        sa.Column(
            "searched_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(["topic_id"], ["topics.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_search_queries_topic_run", "search_queries", ["topic_id", "run_id"])
    # The zero-yield question — "which searches came back empty" — is the whole
    # point of the table, so make it a cheap lookup.
    op.create_index(
        "ix_search_queries_empty",
        "search_queries",
        ["topic_id"],
        postgresql_where=sa.text("hit_count = 0"),
    )

    op.add_column(
        "search_observations", sa.Column("query_id", sa.BigInteger(), nullable=True)
    )
    op.create_foreign_key(
        "fk_search_observations_query",
        "search_observations",
        "search_queries",
        ["query_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("fk_search_observations_query", "search_observations", type_="foreignkey")
    op.drop_column("search_observations", "query_id")
    op.drop_index("ix_search_queries_empty", table_name="search_queries")
    op.drop_index("ix_search_queries_topic_run", table_name="search_queries")
    op.drop_table("search_queries")
