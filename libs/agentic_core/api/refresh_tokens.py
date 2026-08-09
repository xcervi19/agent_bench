"""Issue, rotate and revoke refresh tokens.

The access token stays a stateless JWT: cheap to verify on every request, and
impossible to cancel before it expires. The refresh token is deliberately the
opposite — a row we can strike out — so signing out one laptop ends that session
alone, instead of rotating `JWT_SECRET` and signing out every user at once.

Rotation is single-use: spending a token revokes it and mints its successor. A
token that comes back a second time therefore means either theft or a client
that kept a spent copy, and both get the same answer — see `rotate`.
"""

from __future__ import annotations

import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .refresh_token_model import RefreshToken

# 48 bytes -> a 64-character urlsafe string. Well past guessing range, and short
# enough to sit in localStorage next to the JWT without comment.
TOKEN_BYTES = 48


def new_token() -> str:
    return secrets.token_urlsafe(TOKEN_BYTES)


def hash_token(raw: str) -> str:
    """SHA-256, deliberately not a password hash.

    A password is short and guessable, so bcrypt buys time against a dictionary.
    This is 384 random bits with no dictionary to try, so the slow hash would
    protect nothing while adding cost to a call every session makes.
    """
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def is_live(row: RefreshToken, now: datetime) -> bool:
    """Usable right now: neither revoked nor past its expiry."""
    return row.revoked_at is None and row.expires_at > now


async def issue(
    session: AsyncSession,
    user_id: UUID,
    *,
    lifetime_seconds: int,
    now: datetime | None = None,
) -> str:
    """Mint a token for `user_id` and return the raw value — the only time it exists."""
    moment = now or datetime.now(UTC)
    raw = new_token()
    session.add(
        RefreshToken(
            user_id=user_id,
            token_hash=hash_token(raw),
            expires_at=moment + timedelta(seconds=lifetime_seconds),
        )
    )
    return raw


async def _load(session: AsyncSession, raw: str) -> RefreshToken | None:
    return (
        await session.execute(
            select(RefreshToken).where(RefreshToken.token_hash == hash_token(raw))
        )
    ).scalar_one_or_none()


async def rotate(
    session: AsyncSession,
    raw: str,
    *,
    lifetime_seconds: int,
    now: datetime | None = None,
) -> tuple[UUID, str] | None:
    """Spend one token, hand back its successor. `None` means "sign in again".

    A token presented after it was already spent ends every session the user
    has. We cannot tell a thief replaying a stolen copy from a client that
    hoarded a spent one, and only one of those two readings is safe to assume.
    """
    moment = now or datetime.now(UTC)
    row = await _load(session, raw)
    if row is None:
        return None
    if row.revoked_at is not None:
        await revoke_all(session, row.user_id, now=moment)
        return None
    if row.expires_at <= moment:
        return None
    row.revoked_at = moment
    successor = await issue(session, row.user_id, lifetime_seconds=lifetime_seconds, now=moment)
    return row.user_id, successor


async def revoke(session: AsyncSession, raw: str, *, now: datetime | None = None) -> bool:
    """End one session. False when the token was unknown or already dead."""
    moment = now or datetime.now(UTC)
    row = await _load(session, raw)
    if row is None or not is_live(row, moment):
        return False
    row.revoked_at = moment
    return True


async def revoke_all(session: AsyncSession, user_id: UUID, *, now: datetime | None = None) -> int:
    """End every session this user has. Returns how many were live."""
    moment = now or datetime.now(UTC)
    rows = (
        await session.execute(select(RefreshToken).where(RefreshToken.user_id == user_id))
    ).scalars()
    ended = 0
    for row in rows:
        if is_live(row, moment):
            row.revoked_at = moment
            ended += 1
    return ended
