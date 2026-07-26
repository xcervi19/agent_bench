"""Cross-user isolation on the topic API (#24). No DB: session_scope is stubbed."""

from __future__ import annotations

import uuid
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from apps.claude_agent.auth import Principal, resolve_principal
from apps.claude_agent.config import ClaudeAgentSettings
from apps.claude_agent.topics import routes
from apps.claude_agent.topics.models import Topic

USER_A = uuid.uuid4()
USER_B = uuid.uuid4()
SERVICE = Principal(user_id=None)
NOW = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)


def _settings(**over) -> ClaudeAgentSettings:
    base = dict(database_url="postgresql+asyncpg://x/y", api_key="secret")
    base.update(over)
    return ClaudeAgentSettings(**base)


def _topic(owner: uuid.UUID | None) -> Topic:
    return Topic(
        id=uuid.uuid4(),
        owner_user_id=owner,
        topic="hormuz",
        state="reported",
        topic_id_hash="h",
        last_event_seq=0,
        created_at=NOW,
        updated_at=NOW,
    )


class FakeSession:
    def __init__(self, *topics: Topic):
        self.topics = {t.id: t for t in topics}
        self.added: list[object] = []
        self.statements: list[object] = []

    def add(self, obj) -> None:
        self.added.append(obj)

    async def get(self, _model, pk):
        return self.topics.get(pk)

    async def execute(self, stmt):
        self.statements.append(stmt)
        rows = list(self.topics.values())
        return SimpleNamespace(scalars=lambda: SimpleNamespace(all=lambda: rows))


@pytest.fixture
def fake_scope(monkeypatch):
    def _install(session: FakeSession) -> FakeSession:
        @asynccontextmanager
        async def _scope():
            yield session

        monkeypatch.setattr(routes, "session_scope", _scope)
        return session

    return _install


# ---- principal resolution --------------------------------------------------


async def test_jwt_user_becomes_owner_principal():
    user = SimpleNamespace(id=USER_A)
    principal = await resolve_principal(_settings(), user=user, x_api_key=None)
    assert principal == Principal(user_id=USER_A)


async def test_valid_service_key_becomes_service_principal():
    principal = await resolve_principal(_settings(), user=None, x_api_key="secret")
    assert principal.is_service


async def test_wrong_service_key_is_rejected():
    with pytest.raises(HTTPException) as exc:
        await resolve_principal(_settings(), user=None, x_api_key="nope")
    assert exc.value.status_code == 401


async def test_service_key_rejected_when_bypass_disabled():
    settings = _settings(allow_service_key_bypass=False)
    with pytest.raises(HTTPException) as exc:
        await resolve_principal(settings, user=None, x_api_key="secret")
    assert exc.value.status_code == 401


async def test_jwt_user_still_accepted_when_bypass_disabled():
    settings = _settings(allow_service_key_bypass=False)
    user = SimpleNamespace(id=USER_A)
    principal = await resolve_principal(settings, user=user, x_api_key=None)
    assert principal.user_id == USER_A


# ---- ownership enforcement -------------------------------------------------


async def test_owner_reads_own_topic():
    topic = _topic(USER_A)
    session = FakeSession(topic)
    assert await routes._owned(session, topic.id, Principal(USER_A)) is topic


async def test_other_user_gets_404():
    topic = _topic(USER_A)
    session = FakeSession(topic)
    with pytest.raises(HTTPException) as exc:
        await routes._owned(session, topic.id, Principal(USER_B))
    assert exc.value.status_code == 404


async def test_service_principal_reads_any_topic():
    topic = _topic(USER_A)
    session = FakeSession(topic)
    assert await routes._owned(session, topic.id, SERVICE) is topic


async def test_unknown_topic_gets_404():
    session = FakeSession()
    with pytest.raises(HTTPException) as exc:
        await routes._owned(session, uuid.uuid4(), Principal(USER_A))
    assert exc.value.status_code == 404


# ---- list + create ---------------------------------------------------------


async def test_list_filters_by_owner(fake_scope):
    session = fake_scope(FakeSession(_topic(USER_A)))
    await routes.list_topics(Principal(USER_A))
    assert "owner_user_id" in str(session.statements[0].whereclause)


async def test_list_unfiltered_for_service(fake_scope):
    session = fake_scope(FakeSession(_topic(USER_A)))
    await routes.list_topics(SERVICE)
    assert session.statements[0].whereclause is None


async def test_create_binds_owner(fake_scope, monkeypatch):
    session = fake_scope(FakeSession())

    async def _noop_emit(*args, **kwargs):
        return None

    monkeypatch.setattr(routes, "emit", _noop_emit)
    background = SimpleNamespace(add_task=lambda *a, **k: None)

    await routes.create_topic(
        routes.CreateTopicBody(topic="hormuz"),
        background,
        Principal(USER_A),
        _settings(),
    )

    assert [t.owner_user_id for t in session.added] == [USER_A]
