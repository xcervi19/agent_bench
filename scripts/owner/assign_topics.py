#!/usr/bin/env python3
"""Reassign topic ownership to an account.

Topics created before #24, or by the service key, carry owner_user_id = NULL and
are invisible in the UI because every route filters by owner. This hands them to
a real account so they show up.

    python3 scripts/owner/assign_topics.py you@example.com --unowned
    python3 scripts/owner/assign_topics.py you@example.com --all --apply

Dry run by default: it prints what it would change and touches nothing until
--apply. Child rows (events, subscriptions, deltas, webhooks) resolve access
through topic_id, so only the topics table moves.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
import uuid
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(REPO_ROOT), str(REPO_ROOT / "libs")]

from sqlalchemy import select, update  # noqa: E402

from apps.claude_agent.auth import bootstrap_auth_env  # noqa: E402
from apps.claude_agent.config import get_settings  # noqa: E402
from apps.claude_agent.topics.db import session_scope  # noqa: E402
from apps.claude_agent.topics.models import Topic  # noqa: E402


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reassign topic ownership.")
    parser.add_argument("email", help="Account that should own the topics.")
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--unowned", action="store_true", help="Only owner_user_id IS NULL.")
    scope.add_argument("--all", action="store_true", help="Every topic, whoever owns it.")
    scope.add_argument("--from-email", help="Only topics owned by this account.")
    parser.add_argument("--apply", action="store_true", help="Write. Without it, dry run.")
    return parser.parse_args(argv)


async def resolve_user(email: str) -> uuid.UUID:
    from agentic_core.api.user_model import User

    async with session_scope() as session:
        row = (
            await session.execute(select(User).where(User.email == email))
        ).scalar_one_or_none()
        if row is None:
            raise SystemExit(f"no account for {email} — create it with create_user.py first")
        return row.id


def scope_filter(args: argparse.Namespace, from_user_id: uuid.UUID | None):
    if args.unowned:
        return Topic.owner_user_id.is_(None)
    if args.from_email:
        return Topic.owner_user_id == from_user_id
    return None


async def run(args: argparse.Namespace) -> int:
    target_id = await resolve_user(args.email)
    from_user_id = await resolve_user(args.from_email) if args.from_email else None
    condition = scope_filter(args, from_user_id)

    async with session_scope() as session:
        statement = select(Topic)
        if condition is not None:
            statement = statement.where(condition)
        topics = (await session.execute(statement)).scalars().all()
        rows = [(t.id, t.owner_user_id, t.state, t.topic[:60]) for t in topics]

    if not rows:
        print("nothing matched")
        return 0

    for topic_id, owner, state, title in rows:
        print(f"  {topic_id}  owner={owner or 'NULL'}  {state:<24} {title}")
    print(f"{len(rows)} topic(s) -> {args.email} ({target_id})")

    if not args.apply:
        print("\ndry run — re-run with --apply to write")
        return 0

    async with session_scope() as session:
        statement = update(Topic).values(owner_user_id=target_id)
        if condition is not None:
            statement = statement.where(condition)
        await session.execute(statement)
    print(f"\nreassigned {len(rows)} topic(s)")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    bootstrap_auth_env()
    if not get_settings().database_url:
        raise SystemExit("CLAUDE_AGENT_DATABASE_URL is not set")
    return asyncio.run(run(args))


if __name__ == "__main__":
    raise SystemExit(main())
