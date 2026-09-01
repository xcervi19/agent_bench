"""newsfind #50: a shared topic can stay live instead of being frozen.

#40 made sharing and freezing the same act: `is_public` meant both "anyone may
read this" and "nobody, the owner included, may change it". This splits them.

`share_mode` decides only what sharing *does to the owner* — `live` leaves every
control in place, `frozen` keeps the #40 behaviour. It never widens visibility:
`is_public` is still the one predicate the anonymous router puts in its WHERE
clause, so the 2026-07-27 leak analysis (`1672fe9`) is unchanged.

The other two columns are what replaces the read consistency the freeze used to
give for free. `deliver_run_id` is set *before* a deliver run writes anything and
a refresh delta row exists from the moment its cycle starts, so a live public
view that followed them would serve 404s mid-run and advertise cycles that have
produced no report yet. `public_deliver_run_id` and `public_updated_at` are
advanced only when work has actually finished, so the public view moves in whole
cycles or not at all. `frozen_at` records when a live share was pinned.

Backfill: anything already published was published under freeze semantics and
keeps them — its readers were promised a fixed state. New shares default to
live. (Prod has nothing published; test1 has one topic, `9f2607da`.)

Revision ID: 0013_topic_share_mode
Revises: 0012_search_queries
Create Date: 2026-09-01
"""

import sqlalchemy as sa
from alembic import op

revision = "0013_topic_share_mode"
down_revision = "0012_search_queries"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "topics",
        sa.Column(
            "share_mode",
            sa.String(length=16),
            nullable=False,
            server_default=sa.text("'live'"),
        ),
    )
    op.add_column(
        "topics", sa.Column("public_deliver_run_id", sa.String(length=64), nullable=True)
    )
    op.add_column(
        "topics", sa.Column("public_updated_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column("topics", sa.Column("frozen_at", sa.DateTime(timezone=True), nullable=True))
    op.create_check_constraint(
        "ck_topics_share_mode", "topics", sa.text("share_mode IN ('live', 'frozen')")
    )

    # Already-shared rows were shared under a promise of a fixed state.
    op.execute("UPDATE topics SET share_mode = 'frozen', frozen_at = published_at WHERE is_public")
    # A reported topic's deliver run is finished by definition, so it is exactly
    # what the public view should already be pointing at.
    op.execute(
        "UPDATE topics SET public_deliver_run_id = deliver_run_id WHERE state = 'reported'"
    )
    op.execute("UPDATE topics SET public_updated_at = updated_at WHERE is_public")


def downgrade() -> None:
    op.drop_constraint("ck_topics_share_mode", "topics", type_="check")
    op.drop_column("topics", "frozen_at")
    op.drop_column("topics", "public_updated_at")
    op.drop_column("topics", "public_deliver_run_id")
    op.drop_column("topics", "share_mode")
