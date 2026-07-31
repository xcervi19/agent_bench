#!/usr/bin/env python3
"""Create a SignalGather account without public registration.

The deployment is invitation-only (CLAUDE_AGENT_ALLOW_PUBLIC_REGISTRATION=false),
so this is how an operator issues an account.

    SIGNALGATHER_PASSWORD='...' python3 scripts/owner/create_user.py you@example.com
    python3 scripts/owner/create_user.py you@example.com          # prompts instead

The password is read from the environment or a hidden prompt, never from argv,
so it stays out of shell history and process listings. Hashing goes through
fastapi-users' own UserManager — never hand-roll it.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
import uuid
from getpass import getpass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(REPO_ROOT), str(REPO_ROOT / "libs")]

from apps.claude_agent.auth import bootstrap_auth_env  # noqa: E402
from apps.claude_agent.config import get_settings  # noqa: E402


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create an invitation-only account.")
    parser.add_argument("email")
    parser.add_argument(
        "--tenant-id",
        default=None,
        help="Reuse an existing tenant. Omitted: a fresh tenant is minted.",
    )
    parser.add_argument("--superuser", action="store_true")
    return parser.parse_args(argv)


def read_password() -> str:
    password = os.environ.get("SIGNALGATHER_PASSWORD")
    if password:
        return password
    first = getpass("Password: ")
    if first != getpass("Repeat password: "):
        raise SystemExit("passwords do not match")
    if len(first) < 8:
        raise SystemExit("password must be at least 8 characters")
    return first


async def create(email: str, password: str, tenant_id: uuid.UUID, superuser: bool) -> uuid.UUID:
    from agentic_core.api.auth_routes import UserCreate
    from agentic_core.api.users import UserManager, get_user_db

    user_db_gen = get_user_db()
    user_db = await anext(user_db_gen)
    try:
        manager = UserManager(user_db)
        user = await manager.create(
            UserCreate(
                email=email,
                password=password,
                tenant_id=tenant_id,
                is_superuser=superuser,
            )
        )
        await user_db.session.commit()
        return user.id
    finally:
        await user_db_gen.aclose()


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    bootstrap_auth_env()
    if not get_settings().database_url:
        raise SystemExit("CLAUDE_AGENT_DATABASE_URL is not set")

    tenant_id = uuid.UUID(args.tenant_id) if args.tenant_id else uuid.uuid4()
    password = read_password()

    try:
        user_id = asyncio.run(create(args.email, password, tenant_id, args.superuser))
    except Exception as exc:
        raise SystemExit(f"could not create {args.email}: {exc}") from exc

    print(f"created  email={args.email}")
    print(f"         user_id={user_id}")
    print(f"         tenant_id={tenant_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
