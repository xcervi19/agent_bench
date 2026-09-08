"""Refresh token service — offline, with a stand-in session.

The service only ever runs two queries (by hash, by user), so a fake that reads
the bound parameter is enough to exercise rotation and revocation without a
database.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from agentic_core.api.refresh_token_model import RefreshToken
from agentic_core.api.refresh_tokens import (
    hash_token,
    is_live,
    issue,
    new_token,
    revoke,
    revoke_all,
    rotate,
)

NOW = datetime(2026, 8, 9, 12, 0, tzinfo=UTC)
LIFETIME = 60 * 60 * 24 * 30


class _Result:
    def __init__(self, rows: list[RefreshToken]) -> None:
        self._rows = rows

    def scalar_one_or_none(self) -> RefreshToken | None:
        return self._rows[0] if self._rows else None

    def scalars(self):
        return iter(self._rows)


class FakeSession:
    def __init__(self, rows: list[RefreshToken] | None = None) -> None:
        self.rows = list(rows or [])

    def add(self, row: RefreshToken) -> None:
        self.rows.append(row)

    async def execute(self, statement):
        params = statement.compile().params
        if "token_hash_1" in params:
            wanted = params["token_hash_1"]
            return _Result([r for r in self.rows if r.token_hash == wanted])
        wanted = params["user_id_1"]
        return _Result([r for r in self.rows if r.user_id == wanted])


def _row(
    raw: str,
    *,
    user_id: str = "user-1",
    expires_in: int = LIFETIME,
    revoked_at: datetime | None = None,
    now: datetime = NOW,
) -> RefreshToken:
    """A stored token, expiring `expires_in` after `now`.

    `now` defaults to the frozen `NOW` the pure-function tests assert against.
    Tests that drive production code must pass the real clock instead: `revoke_all`
    reads `datetime.now(UTC)` itself, so a row anchored to a fixed past date is
    already expired by the time the code sees it, and revocation then correctly
    does nothing. That is how these tests silently stopped exercising revocation
    30 days after `NOW`.
    """
    return RefreshToken(
        user_id=user_id,
        token_hash=hash_token(raw),
        expires_at=now + timedelta(seconds=expires_in),
        revoked_at=revoked_at,
    )


def test_the_stored_hash_is_not_the_token():
    raw = new_token()
    assert hash_token(raw) != raw
    assert len(hash_token(raw)) == 64


def test_two_tokens_never_collide():
    assert len({new_token() for _ in range(200)}) == 200


def test_a_live_token_is_neither_revoked_nor_past_its_expiry():
    assert is_live(_row("a"), NOW)


def test_a_revoked_token_is_dead_even_before_expiry():
    assert not is_live(_row("a", revoked_at=NOW), NOW)


def test_expiry_is_exclusive_so_the_final_instant_does_not_count():
    assert not is_live(_row("a", expires_in=0), NOW)


@pytest.mark.asyncio
async def test_issue_stores_only_the_hash_and_returns_the_raw_token():
    session = FakeSession()
    raw = await issue(session, "user-1", lifetime_seconds=LIFETIME, now=NOW)

    assert len(session.rows) == 1
    stored = session.rows[0]
    assert stored.token_hash == hash_token(raw)
    assert stored.token_hash != raw
    assert stored.expires_at == NOW + timedelta(seconds=LIFETIME)


@pytest.mark.asyncio
async def test_rotate_spends_the_old_token_and_returns_a_live_successor():
    old = _row("old")
    session = FakeSession([old])

    result = await rotate(session, "old", lifetime_seconds=LIFETIME, now=NOW)

    assert result is not None
    user_id, successor = result
    assert user_id == "user-1"
    assert old.revoked_at == NOW
    assert successor != "old"
    assert is_live(session.rows[-1], NOW)


@pytest.mark.asyncio
async def test_an_unknown_token_is_refused_without_touching_anything():
    live = _row("mine")
    session = FakeSession([live])

    assert await rotate(session, "never-issued", lifetime_seconds=LIFETIME, now=NOW) is None
    assert is_live(live, NOW)


@pytest.mark.asyncio
async def test_an_expired_token_is_refused_but_leaves_other_sessions_alone():
    expired = _row("old", expires_in=-1)
    other = _row("other-device")
    session = FakeSession([expired, other])

    assert await rotate(session, "old", lifetime_seconds=LIFETIME, now=NOW) is None
    assert is_live(other, NOW), "an ordinary expiry is not evidence of theft"


@pytest.mark.asyncio
async def test_replaying_a_spent_token_ends_every_session_the_user_has():
    """Either a thief has a copy or a client hoarded one; only one is safe to assume."""
    spent = _row("stolen", revoked_at=NOW - timedelta(minutes=5))
    other = _row("other-device")
    session = FakeSession([spent, other])

    assert await rotate(session, "stolen", lifetime_seconds=LIFETIME, now=NOW) is None
    assert not is_live(other, NOW)


@pytest.mark.asyncio
async def test_replay_defence_stops_at_the_user_it_belongs_to():
    spent = _row("stolen", revoked_at=NOW - timedelta(minutes=5))
    stranger = _row("theirs", user_id="user-2")
    session = FakeSession([spent, stranger])

    await rotate(session, "stolen", lifetime_seconds=LIFETIME, now=NOW)

    assert is_live(stranger, NOW)


@pytest.mark.asyncio
async def test_revoke_ends_one_session_and_reports_whether_it_was_live():
    live = _row("here")
    session = FakeSession([live])

    assert await revoke(session, "here", now=NOW) is True
    assert live.revoked_at == NOW
    assert await revoke(session, "here", now=NOW) is False, "already dead is not a second sign-out"


@pytest.mark.asyncio
async def test_revoking_an_unknown_token_is_not_an_error():
    assert await revoke(FakeSession(), "never-issued", now=NOW) is False


@pytest.mark.asyncio
async def test_revoke_all_counts_only_the_sessions_it_actually_ended():
    session = FakeSession(
        [
            _row("a"),
            _row("b"),
            _row("already-out", revoked_at=NOW - timedelta(days=1)),
            _row("stale", expires_in=-1),
        ]
    )

    assert await revoke_all(session, "user-1", now=NOW) == 2


class _Scope:
    """Stands in for `session_scope()` — a context manager over one fake session."""

    def __init__(self, session: FakeSession) -> None:
        self.session = session

    async def __aenter__(self) -> FakeSession:
        return self.session

    async def __aexit__(self, *exc: object) -> bool:
        return False


class _User:
    id = "user-1"


@pytest.mark.asyncio
async def test_changing_a_password_ends_every_session_it_opened(monkeypatch):
    """Resetting usually means the old password leaked; its sessions must go with it."""
    from agentic_core.api import users

    live = datetime.now(UTC)
    session = FakeSession([_row("laptop", now=live), _row("phone", now=live)])
    monkeypatch.setattr(users, "session_scope", lambda: _Scope(session))

    manager = object.__new__(users.UserManager)
    await manager.on_after_update(_User(), {"password": "new-one"})

    assert all(not is_live(row, live) for row in session.rows)


@pytest.mark.asyncio
async def test_an_unrelated_profile_update_leaves_sessions_alone(monkeypatch):
    from agentic_core.api import users

    live = datetime.now(UTC)
    session = FakeSession([_row("laptop", now=live)])
    monkeypatch.setattr(users, "session_scope", lambda: _Scope(session))

    manager = object.__new__(users.UserManager)
    await manager.on_after_update(_User(), {"email": "new@example.com"})

    assert is_live(session.rows[0], live)
