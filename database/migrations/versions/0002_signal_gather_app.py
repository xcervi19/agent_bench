"""signal_gather: alerts, reports, profile preferences.

Revision ID: 0002_signal_gather
Revises: 0001_init
Create Date: 2026-04-25
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0002_signal_gather"
down_revision = "0001_init"
branch_labels = None
depends_on = None

NEW_TABLES = ("reports", "alerts")


def upgrade() -> None:
    _extend_user_profiles()
    _create_reports()
    _create_alerts()
    for table in NEW_TABLES:
        _enable_rls(table)


def downgrade() -> None:
    for table in reversed(NEW_TABLES):
        op.execute(f"DROP POLICY IF EXISTS tenant_isolation ON {table}")
        op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
        op.drop_table(table)
    _shrink_user_profiles()


def _extend_user_profiles() -> None:
    op.add_column(
        "user_profiles",
        sa.Column("alert_channels", postgresql.JSON, nullable=False, server_default=sa.text("'[]'::json")),
    )
    op.add_column(
        "user_profiles",
        sa.Column("briefing_cadence", sa.String(16), nullable=False, server_default="daily"),
    )
    op.add_column(
        "user_profiles",
        sa.Column("impact_threshold", sa.Float, nullable=False, server_default="0.6"),
    )
    op.add_column("user_profiles", sa.Column("raw_setup_text", sa.Text, nullable=True))


def _shrink_user_profiles() -> None:
    op.drop_column("user_profiles", "raw_setup_text")
    op.drop_column("user_profiles", "impact_threshold")
    op.drop_column("user_profiles", "briefing_cadence")
    op.drop_column("user_profiles", "alert_channels")


def _create_reports() -> None:
    op.create_table(
        "reports",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), index=True),
        sa.Column("kind", sa.String(32), nullable=False),
        sa.Column("title", sa.String(256), nullable=False),
        sa.Column("body", sa.Text, nullable=False),
        sa.Column("signal_ids", postgresql.JSON, nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column("event_ids", postgresql.JSON, nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def _create_alerts() -> None:
    op.create_table(
        "alerts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("signal_id", postgresql.UUID(as_uuid=True), index=True),
        sa.Column("severity", sa.String(16), nullable=False),
        sa.Column("title", sa.String(256), nullable=False),
        sa.Column("body", sa.Text, nullable=False),
        sa.Column("channels", postgresql.JSON, nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column("delivered", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("read", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
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
