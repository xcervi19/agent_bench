"""Public topic sharing (#40). No DB: session_scope is stubbed.

Two properties matter more than the rest and are tested first:

  * a stranger can only ever *read*, and only published rows;
  * a published topic cannot spend money — no pipeline action, no refresh, and
    the scheduler will not pick it up.
"""

from __future__ import annotations

import uuid
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from apps.claude_agent.auth import Principal
from apps.claude_agent.config import ClaudeAgentSettings
from apps.claude_agent.topics import public_routes, routes
from apps.claude_agent.topics import refresh as refresh_mod
from apps.claude_agent.topics.models import Topic, TopicSubscription

USER_A = uuid.uuid4()
USER_B = uuid.uuid4()
NOW = datetime(2026, 8, 1, 9, 0, tzinfo=UTC)


def _settings(**over) -> ClaudeAgentSettings:
    base = dict(database_url="postgresql+asyncpg://x/y", api_key="secret")
    base.update(over)
    return ClaudeAgentSettings(**base)


def _topic(
    owner: uuid.UUID | None = USER_A,
    *,
    state: str = "reported",
    is_public: bool = False,
) -> Topic:
    return Topic(
        id=uuid.uuid4(),
        owner_user_id=owner,
        topic="hormuz",
        state=state,
        topic_id_hash="h",
        plan_run_id="plan-1",
        deliver_run_id="deliver-1",
        last_event_seq=0,
        is_public=is_public,
        published_at=NOW if is_public else None,
        created_at=NOW,
        updated_at=NOW,
    )


def _requested_id(stmt) -> uuid.UUID | None:
    """The `Topic.id == <uuid>` a statement binds, if it binds one."""
    for value in stmt.compile().params.values():
        if isinstance(value, uuid.UUID):
            return value
    return None


class FakeSession:
    """Enough of AsyncSession for these routes: get by pk, and execute(select).

    `execute` filters the in-memory rows through the statement's WHERE clause the
    only way that matters here — by honouring `is_public`, which is the predicate
    the public API's safety rests on.
    """

    def __init__(self, *rows: object):
        self.topics = {r.id: r for r in rows if isinstance(r, Topic)}
        self.subs = [r for r in rows if isinstance(r, TopicSubscription)]
        self.added: list[object] = []
        self.statements: list[object] = []

    def add(self, obj) -> None:
        self.added.append(obj)

    async def flush(self) -> None:
        return None

    async def get(self, model, pk):
        if model is Topic:
            return self.topics.get(pk)
        return next((s for s in self.subs if s.id == pk), None)

    async def execute(self, stmt):
        self.statements.append(stmt)
        where = getattr(stmt, "whereclause", None)
        clause = str(where) if where is not None else ""
        if "topic_subscriptions" in clause:
            rows: list[object] = list(self.subs)
        else:
            rows = list(self.topics.values())
            if "is_public" in clause:
                rows = [r for r in rows if r.is_public]
            wanted = _requested_id(stmt)
            if wanted is not None:
                rows = [r for r in rows if r.id == wanted]

        def _one_or_none():
            if len(rows) > 1:
                raise AssertionError("expected at most one row")
            return rows[0] if rows else None

        return SimpleNamespace(
            scalars=lambda: SimpleNamespace(all=lambda: rows),
            scalar_one_or_none=_one_or_none,
        )


@pytest.fixture
def fake_scope(monkeypatch):
    def _install(session: FakeSession, *modules) -> FakeSession:
        @asynccontextmanager
        async def _scope():
            yield session

        for module in modules or (routes, public_routes):
            monkeypatch.setattr(module, "session_scope", _scope)
        return session

    return _install


@pytest.fixture(autouse=True)
def silent_emit(monkeypatch):
    seen: list[tuple] = []

    async def _emit(topic_id, event_type, payload):
        seen.append((topic_id, event_type, payload))

    monkeypatch.setattr(routes, "emit", _emit)
    monkeypatch.setattr(refresh_mod, "emit", _emit)
    return seen


# ---- the public API is structurally read-only -------------------------------


def test_public_router_exposes_no_write_routes():
    """The guarantee is the router's shape, not a reviewer's memory.

    Anonymous callers reach this router. If a POST/PATCH/DELETE ever lands on
    it, some stranger can make us run an agent — so fail the build instead.
    """
    for route in public_routes.router.routes:
        assert set(route.methods) <= {"GET", "HEAD"}, f"{route.path} accepts {route.methods}"


def test_public_router_has_no_event_stream():
    """No unauthenticated long-poll: a frozen topic has nothing to stream."""
    assert not any(route.path.endswith("/events") for route in public_routes.router.routes)


# ---- published rows only ----------------------------------------------------


async def test_public_detail_serves_a_published_topic(fake_scope):
    topic = _topic(is_public=True)
    fake_scope(FakeSession(topic))
    payload = await public_routes.get_public_topic(topic.id)
    assert payload["id"] == str(topic.id)
    assert payload["read_only"] is True


async def test_public_detail_hides_a_private_topic(fake_scope):
    topic = _topic(is_public=False)
    fake_scope(FakeSession(topic))
    with pytest.raises(HTTPException) as exc:
        await public_routes.get_public_topic(topic.id)
    assert exc.value.status_code == 404


async def test_public_listing_filters_on_is_public(fake_scope):
    session = fake_scope(FakeSession(_topic(is_public=True), _topic(owner=USER_B)))
    result = await public_routes.list_public_topics()
    assert result["count"] == 1
    assert "is_public" in str(session.statements[0].whereclause)


async def test_public_payload_omits_owner_and_run_ids(fake_scope):
    topic = _topic(is_public=True)
    fake_scope(FakeSession(topic))
    payload = await public_routes.get_public_topic(topic.id)
    assert "owner_user_id" not in payload
    assert "plan_run_id" not in payload and "deliver_run_id" not in payload
    assert "error" not in payload
    # Presence is still discoverable — a reader needs to know a report exists.
    assert payload["has_report"] is True


async def test_public_listing_rejects_an_oversized_limit(fake_scope):
    fake_scope(FakeSession())
    with pytest.raises(HTTPException) as exc:
        await public_routes.list_public_topics(limit=10_000)
    assert exc.value.status_code == 422


# ---- publishing -------------------------------------------------------------


async def test_publish_marks_the_topic_public(fake_scope, silent_emit):
    topic = _topic()
    fake_scope(FakeSession(topic))
    result = await routes.publish_topic(topic.id, Principal(USER_A))
    assert topic.is_public is True
    assert topic.published_at is not None
    assert result["public_path"] == f"/v1/public/topics/{topic.id}"
    assert [e[1] for e in silent_emit] == ["topic.published"]


async def test_publish_requires_a_reported_topic(fake_scope):
    topic = _topic(state="planning")
    fake_scope(FakeSession(topic))
    with pytest.raises(HTTPException) as exc:
        await routes.publish_topic(topic.id, Principal(USER_A))
    assert exc.value.status_code == 409
    assert topic.is_public is False


async def test_publish_is_idempotent_and_keeps_the_original_date(fake_scope):
    topic = _topic(is_public=True)
    first = topic.published_at
    fake_scope(FakeSession(topic))
    result = await routes.publish_topic(topic.id, Principal(USER_A))
    assert result["already_published"] is True
    assert topic.published_at == first


async def test_publish_pauses_monitoring_and_its_schedule(fake_scope):
    topic = _topic()
    sub = TopicSubscription(
        id=1,
        topic_id=topic.id,
        status="active",
        short_term_queries=[],
        max_age_hours=48,
        schedule_enabled=True,
        schedule_interval_hours=6,
        next_refresh_at=NOW,
    )
    fake_scope(FakeSession(topic, sub))
    result = await routes.publish_topic(topic.id, Principal(USER_A))
    assert result["monitoring_paused"] is True
    assert sub.status == "paused"
    assert sub.schedule_enabled is False
    assert sub.next_refresh_at is None


async def test_publish_waits_for_a_refresh_that_is_already_running(fake_scope):
    """Otherwise the cycle finishes *after* the share and rewrites the snapshot
    readers were handed — `run_refresh` only checks `is_public` on entry."""
    topic = _topic()
    sub = TopicSubscription(
        id=1,
        topic_id=topic.id,
        status="active",
        short_term_queries=[],
        max_age_hours=48,
        refresh_locked=True,
    )
    fake_scope(FakeSession(topic, sub))
    with pytest.raises(HTTPException) as exc:
        await routes.publish_topic(topic.id, Principal(USER_A))
    assert exc.value.status_code == 409
    assert "refresh is running" in exc.value.detail
    assert topic.is_public is False


async def test_another_user_cannot_publish_your_topic(fake_scope):
    topic = _topic(owner=USER_A)
    fake_scope(FakeSession(topic))
    with pytest.raises(HTTPException) as exc:
        await routes.publish_topic(topic.id, Principal(USER_B))
    assert exc.value.status_code == 404
    assert topic.is_public is False


async def test_unpublish_returns_the_topic_to_private(fake_scope, silent_emit):
    topic = _topic(is_public=True)
    fake_scope(FakeSession(topic))
    result = await routes.unpublish_topic(topic.id, Principal(USER_A))
    assert topic.is_public is False
    assert topic.published_at is None
    assert result["public_path"] is None
    assert [e[1] for e in silent_emit] == ["topic.unpublished"]


async def test_unpublish_is_idempotent(fake_scope):
    topic = _topic()
    fake_scope(FakeSession(topic))
    result = await routes.unpublish_topic(topic.id, Principal(USER_A))
    assert result["already_private"] is True


# ---- a published topic is frozen -------------------------------------------


async def test_mutable_rejects_a_published_topic():
    topic = _topic(is_public=True)
    session = FakeSession(topic)
    with pytest.raises(HTTPException) as exc:
        await routes._mutable(session, topic.id, Principal(USER_A))
    assert exc.value.status_code == 409
    assert "unpublish" in exc.value.detail


async def test_owner_still_reads_a_published_topic():
    topic = _topic(is_public=True)
    session = FakeSession(topic)
    assert await routes._owned(session, topic.id, Principal(USER_A)) is topic


@pytest.mark.parametrize("state", ["planned_awaiting_review", "reported", "planning"])
def test_published_topics_advertise_no_actions(state):
    assert routes._actions(state, True) == []
    # ...and the states themselves are unchanged when the topic is private.
    assert routes._actions(state, False) == routes._actions(state)


async def test_refresh_endpoint_refuses_a_published_topic(fake_scope):
    topic = _topic(is_public=True)
    fake_scope(FakeSession(topic))
    dispatched: list[tuple] = []
    background = SimpleNamespace(add_task=lambda *a, **k: dispatched.append(a))

    with pytest.raises(HTTPException) as exc:
        await routes.trigger_refresh(topic.id, background, Principal(USER_A), _settings())
    assert exc.value.status_code == 409
    assert dispatched == []


async def test_monitor_endpoint_refuses_a_published_topic(fake_scope):
    topic = _topic(is_public=True)
    fake_scope(FakeSession(topic))
    with pytest.raises(HTTPException) as exc:
        await routes.start_monitoring(
            topic.id, routes.MonitorBody(), Principal(USER_A), _settings()
        )
    assert exc.value.status_code == 409


async def test_proceed_refuses_a_published_topic(fake_scope):
    topic = _topic(state="planned_awaiting_review", is_public=True)
    fake_scope(FakeSession(topic))
    dispatched: list[tuple] = []
    background = SimpleNamespace(add_task=lambda *a, **k: dispatched.append(a))

    with pytest.raises(HTTPException) as exc:
        await routes.proceed(topic.id, background, Principal(USER_A), _settings())
    assert exc.value.status_code == 409
    assert dispatched == []


# ---- nothing spends money on a published topic ------------------------------


async def test_run_refresh_skips_a_published_topic(monkeypatch, silent_emit):
    """The last line of defence: a refresh already queued when the owner hit
    Share must not start a Claude run."""
    topic = _topic(is_public=True)

    @asynccontextmanager
    async def _scope():
        yield FakeSession(topic)

    monkeypatch.setattr(refresh_mod, "session_scope", _scope)

    async def _fail_lock(_subscription_id):
        raise AssertionError("run_refresh must bail out before taking the lock")

    monkeypatch.setattr(refresh_mod, "_try_acquire_lock", _fail_lock)

    await refresh_mod.run_refresh(topic.id, 1, _settings(), trigger="scheduled")

    assert [(e[1], e[2]["reason"]) for e in silent_emit] == [
        ("refresh.skipped", "topic_published")
    ]


async def test_scheduler_never_claims_a_published_topic(monkeypatch):
    """The due-query itself must exclude published topics.

    Asserted against the compiled SQL rather than the returned rows: the filter
    has to be in the statement Postgres runs, not in a Python check after it.
    """
    from sqlalchemy.dialects import postgresql

    from apps.claude_agent.topics import scheduler

    captured: list[object] = []

    class CapturingSession(FakeSession):
        async def execute(self, stmt):
            captured.append(stmt)
            return SimpleNamespace(scalars=lambda: SimpleNamespace(all=lambda: []))

    @asynccontextmanager
    async def _scope():
        yield CapturingSession()

    monkeypatch.setattr(scheduler, "session_scope", _scope)

    assert await scheduler.claim_due_subscriptions(NOW, 5) == []

    sql = str(captured[0].compile(dialect=postgresql.dialect()))
    assert "is_public" in sql
    assert "NOT IN" in sql.upper()
