#!/usr/bin/env python3
"""Set a new password for an existing account.

There is no self-service reset: no email transport is configured, so
/auth/forgot-password is deliberately not mounted rather than issuing tokens
nobody ever receives. On an invitation-only deployment the operator resets it.

    SIGNALGATHER_PASSWORD='...' python3 scripts/owner/reset_password.py you@example.com
    python3 scripts/owner/reset_password.py you@example.com        # prompts instead

Hand the new password to the user over a channel you trust, and have them change
it once they are in. Password rules and hashing come from fastapi-users'
UserManager, the same path registration uses.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
sys.path[:0] = [str(REPO_ROOT), str(REPO_ROOT / "libs"), str(HERE)]

from create_user import read_password  # noqa: E402

from apps.claude_agent.auth import bootstrap_auth_env  # noqa: E402
from apps.claude_agent.config import get_settings  # noqa: E402


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reset an account password.")
    parser.add_argument("email")
    return parser.parse_args(argv)


async def reset(email: str, password: str) -> str:
    from agentic_core.api.auth_routes import UserUpdate
    from agentic_core.api.users import UserManager, get_user_db
    from fastapi_users.exceptions import UserNotExists

    user_db_gen = get_user_db()
    user_db = await anext(user_db_gen)
    try:
        manager = UserManager(user_db)
        try:
            user = await manager.get_by_email(email)
        except UserNotExists:
            raise SystemExit(f"no account for {email}") from None
        await manager.update(UserUpdate(password=password), user, safe=True)
        await user_db.session.commit()
        return str(user.id)
    finally:
        await user_db_gen.aclose()


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    bootstrap_auth_env()
    if not get_settings().database_url:
        raise SystemExit("CLAUDE_AGENT_DATABASE_URL is not set")

    password = read_password()
    try:
        user_id = asyncio.run(reset(args.email, password))
    except SystemExit:
        raise
    except Exception as exc:
        raise SystemExit(f"could not reset {args.email}: {exc}") from exc

    print(f"password reset  email={args.email}  user_id={user_id}")
    print("existing sessions stay valid until their JWT expires")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
