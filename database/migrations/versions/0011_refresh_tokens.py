"""Refresh tokens: one revocable row per signed-in session.

The access token is a stateless JWT and cannot be cancelled before it expires,
which forced a choice between a one-hour session and an un-cancellable one. This
table is the third option — the long-lived half of the pair lives here, so a
single session can be ended without rotating the signing secret on everybody.

Only the SHA-256 of each token is stored; the raw value exists once, in the
response that issued it. Revoked rows are kept rather than deleted so that a
token coming back after it was spent is still recognisable as a replay.

Revision ID: 0011_refresh_tokens
Revises: 0010_search_document_fetches
Create Date: 2026-08-09
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0011_refresh_tokens"
down_revision = "0010_search_document_fetches"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "refresh_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # Every refresh is a lookup by hash, and the uniqueness is what makes a
    # replayed token resolve to the row that already recorded it as spent.
    op.create_index("ix_refresh_tokens_token_hash", "refresh_tokens", ["token_hash"], unique=True)
    # Signing every session out at once — on replay, and on demand.
    op.create_index("ix_refresh_tokens_user_id", "refresh_tokens", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_refresh_tokens_user_id", table_name="refresh_tokens")
    op.drop_index("ix_refresh_tokens_token_hash", table_name="refresh_tokens")
    op.drop_table("refresh_tokens")
