"""initial schema: extensions, tables, RLS.

Revision ID: 0001_init
Revises:
Create Date: 2026-04-25
"""

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects import postgresql

revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None

EMBED_DIM = 1536
TENANT_TABLES = ("users", "documents", "events", "signals", "user_profiles",
                 "agent_sessions", "agent_events")


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    _create_users()
    _create_documents()
    _create_events()
    _create_signals()
    _create_user_profiles()
    _create_agent_sessions()
    _create_agent_events()

    for table in TENANT_TABLES:
        _enable_rls(table)


def downgrade() -> None:
    for table in reversed(TENANT_TABLES):
        op.execute(f"DROP POLICY IF EXISTS tenant_isolation ON {table}")
        op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")

    for table in ("agent_events", "agent_sessions", "user_profiles", "signals",
                  "events", "documents", "users"):
        op.drop_table(table)


def _create_users() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(320), unique=True, nullable=False),
        sa.Column("hashed_password", sa.String(1024), nullable=False),
        sa.Column("is_active", sa.Boolean, default=True, nullable=False),
        sa.Column("is_superuser", sa.Boolean, default=False, nullable=False),
        sa.Column("is_verified", sa.Boolean, default=False, nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
    )


def _create_documents() -> None:
    op.create_table(
        "documents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("source", sa.String(128), nullable=False),
        sa.Column("url", sa.String(2048)),
        sa.Column("title", sa.String(512)),
        sa.Column("language", sa.String(8)),
        sa.Column("s3_key", sa.String(1024), nullable=False),
        sa.Column("content", sa.Text),
        sa.Column("embedding", Vector(EMBED_DIM)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.execute("CREATE INDEX ix_documents_embedding ON documents USING ivfflat (embedding vector_l2_ops)")


def _create_events() -> None:
    op.create_table(
        "events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("document_id", postgresql.UUID(as_uuid=True), index=True),
        sa.Column("category", sa.String(64), nullable=False),
        sa.Column("commodity", sa.String(64), index=True),
        sa.Column("region", sa.String(64), index=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True)),
        sa.Column("summary", sa.Text, nullable=False),
        sa.Column("entities", postgresql.JSON, nullable=False, server_default=sa.text("'{}'::json")),
        sa.Column("impact_score", sa.Float),
        sa.Column("embedding", Vector(EMBED_DIM)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.execute("CREATE INDEX ix_events_embedding ON events USING ivfflat (embedding vector_l2_ops)")


def _create_signals() -> None:
    op.create_table(
        "signals",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("kind", sa.String(64), nullable=False),
        sa.Column("commodity", sa.String(64), index=True),
        sa.Column("region", sa.String(64), index=True),
        sa.Column("direction", sa.String(16), nullable=False),
        sa.Column("confidence", sa.Float, nullable=False),
        sa.Column("rationale", sa.Text, nullable=False),
        sa.Column("event_ids", postgresql.JSON, nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def _create_user_profiles() -> None:
    op.create_table(
        "user_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), unique=True, nullable=False),
        sa.Column("display_name", sa.String(128)),
        sa.Column("commodities", postgresql.JSON, nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column("regions", postgresql.JSON, nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column("themes", postgresql.JSON, nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column("risk_appetite", sa.String(16), nullable=False, server_default="medium"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def _create_agent_sessions() -> None:
    op.create_table(
        "agent_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("crew", sa.String(128), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="running"),
        sa.Column("inputs", postgresql.JSON, nullable=False, server_default=sa.text("'{}'::json")),
        sa.Column("output", postgresql.JSON),
        sa.Column("error", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def _create_agent_events() -> None:
    op.create_table(
        "agent_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("kind", sa.String(64), nullable=False),
        sa.Column("payload", postgresql.JSON, nullable=False, server_default=sa.text("'{}'::json")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def _enable_rls(table: str) -> None:
    op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY tenant_isolation ON {table}
        USING (tenant_id::text = current_setting('app.tenant_id', true))
        WITH CHECK (tenant_id::text = current_setting('app.tenant_id', true))
        """
    )
