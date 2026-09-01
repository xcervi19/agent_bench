"""Public topic sharing (#40) and live shares (#50). No DB: session_scope is stubbed.

Three properties matter more than the rest and are tested first:

  * a stranger can only ever *read*, and only published rows (#40);
  * a **frozen** share cannot spend money — no pipeline action, no refresh, and
    the scheduler will not pick it up (#40, now scoped to the mode);
  * a **live** share takes nothing away from its owner, and shows a reader only
    state that has finished — never a run in flight (#50).

The middle one used to be "a published topic cannot spend". It is deliberately
narrower now: a live share spends exactly what its owner's own monitoring
spends, and the guarantee that survives untouched is the structural one — no
anonymous request can cause a run, because the public router has no route that
starts one.
"""

from __future__ import annotations

import uuid
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from types import SimpleNamespace

import pytest
from fastapi import HTTPException, Response

from apps.claude_agent.auth import Principal
from apps.claude_agent.config import ClaudeAgentSettings
from apps.claude_agent.topics import public_routes, routes, serving
from apps.claude_agent.topics import refresh as refresh_mod
from apps.claude_agent.topics.models import (
    SHARE_FROZEN,
    SHARE_LIVE,
    Topic,
    TopicRefreshDelta,
    TopicSubscription,
)

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
    share_mode: str = SHARE_LIVE,
    public_deliver_run_id: str | None = "deliver-1",
) -> Topic:
    frozen = is_public and share_mode == SHARE_FROZEN
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
        share_mode=share_mode,
        frozen_at=NOW if frozen else None,
        public_deliver_run_id=public_deliver_run_id,
        public_updated_at=NOW if is_public else None,
        created_at=NOW,
        updated_at=NOW,
    )


def _frozen(**over) -> Topic:
    return _topic(is_public=True, share_mode=SHARE_FROZEN, **over)


def _live(**over) -> Topic:
    return _topic(is_public=True, share_mode=SHARE_LIVE, **over)


def _delta(topic: Topic, seq: int, status: str) -> TopicRefreshDelta:
    return TopicRefreshDelta(
        id=seq,
        topic_id=topic.id,
        subscription_id=1,
        seq=seq,
        run_id=f"refresh-{seq}",
        status=status,
        created_at=NOW,
    )


def _sub(topic: Topic, **over) -> TopicSubscription:
    base = dict(
        id=1,
        topic_id=topic.id,
        status="active",
        short_term_queries=[],
        max_age_hours=48,
    )
    base.update(over)
    return TopicSubscription(**base)


def _requested_id(stmt) -> uuid.UUID | None:
    """The `Topic.id == <uuid>` a statement binds, if it binds one."""
    for value in stmt.compile().params.values():
        if isinstance(value, uuid.UUID):
            return value
    return None


class FakeSession:
    """Enough of AsyncSession for these routes: get by pk, and execute(select).

    `execute` filters the in-memory rows through the statement's WHERE clause the
    two ways that matter here — by honouring `is_public`, the predicate the
    public API's safety rests on, and by honouring a delta's `status`, the
    predicate that keeps a running cycle out of a reader's view (#50).
    """

    def __init__(self, *rows: object):
        self.topics = {r.id: r for r in rows if isinstance(r, Topic)}
        self.subs = [r for r in rows if isinstance(r, TopicSubscription)]
        self.deltas = [r for r in rows if isinstance(r, TopicRefreshDelta)]
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
        params = stmt.compile().params
        if "topic_refresh_deltas" in clause:
            rows: list[object] = list(self.deltas)
            if "status" in clause:
                rows = [d for d in rows if d.status == "completed"]
            if "seq" in clause:
                rows = [d for d in rows if d.seq == params.get("seq_1")]
            if "count(" in str(stmt).lower():
                seqs = [d.seq for d in rows]
                return SimpleNamespace(one=lambda: (len(rows), max(seqs) if seqs else None))
        elif "topic_subscriptions" in clause:
            rows = list(self.subs)
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
    topic = _live()
    fake_scope(FakeSession(topic))
    payload = await public_routes.get_public_topic(topic.id, Response())
    assert payload["id"] == str(topic.id)
    assert payload["read_only"] is True


async def test_public_detail_is_read_only_in_both_modes(fake_scope):
    """Live sharing loosens what the *owner* may do, never what a reader may do."""
    topic = _frozen()
    fake_scope(FakeSession(topic))
    payload = await public_routes.get_public_topic(topic.id, Response())
    assert payload["read_only"] is True
    assert payload["updates"]["live"] is False


async def test_public_detail_hides_a_private_topic(fake_scope):
    topic = _topic(is_public=False)
    fake_scope(FakeSession(topic))
    with pytest.raises(HTTPException) as exc:
        await public_routes.get_public_topic(topic.id, Response())
    assert exc.value.status_code == 404


async def test_public_listing_filters_on_is_public(fake_scope):
    session = fake_scope(FakeSession(_live(), _topic(owner=USER_B)))
    result = await public_routes.list_public_topics()
    assert result["count"] == 1
    assert "is_public" in str(session.statements[0].whereclause)


async def test_public_payload_omits_owner_and_run_ids(fake_scope):
    topic = _live()
    fake_scope(FakeSession(topic))
    payload = await public_routes.get_public_topic(topic.id, Response())
    assert "owner_user_id" not in payload
    assert "plan_run_id" not in payload and "deliver_run_id" not in payload
    assert "public_deliver_run_id" not in payload
    assert "error" not in payload
    # Presence is still discoverable — a reader needs to know a report exists.
    assert payload["has_report"] is True


async def test_public_payload_keeps_the_refresh_schedule_private(fake_scope):
    """When the next run happens is a spending decision, not a finding."""
    topic = _live()
    fake_scope(FakeSession(topic, _sub(topic, schedule_enabled=True, schedule_interval_hours=6)))
    payload = await public_routes.get_public_topic(topic.id, Response())
    flat = str(payload)
    assert "next_refresh_at" not in flat and "schedule_interval_hours" not in flat


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


async def test_publish_defaults_to_a_live_share(fake_scope):
    """The default is the product decision of #50: sharing a report must not
    cost the owner the monitoring that keeps it worth reading."""
    topic = _topic()
    fake_scope(FakeSession(topic))
    result = await routes.publish_topic(topic.id, Principal(USER_A))
    assert topic.share_mode == SHARE_LIVE
    assert topic.frozen_at is None
    assert result["share_mode"] == SHARE_LIVE


async def test_publishing_live_leaves_monitoring_running(fake_scope):
    topic = _topic()
    sub = _sub(topic, schedule_enabled=True, schedule_interval_hours=6, next_refresh_at=NOW)
    fake_scope(FakeSession(topic, sub))
    result = await routes.publish_topic(topic.id, Principal(USER_A))
    assert result["monitoring_paused"] is False
    assert sub.status == "active"
    assert sub.schedule_enabled is True
    assert sub.next_refresh_at == NOW


async def test_publishing_live_is_allowed_mid_refresh(fake_scope):
    """Nothing is being pinned, so a cycle finishing afterwards is not a problem
    — it is the point. It will appear when it completes."""
    topic = _topic()
    fake_scope(FakeSession(topic, _sub(topic, refresh_locked=True)))
    result = await routes.publish_topic(topic.id, Principal(USER_A))
    assert result["share_mode"] == SHARE_LIVE
    assert topic.is_public is True


async def test_publish_requires_a_reported_topic(fake_scope):
    topic = _topic(state="planning")
    fake_scope(FakeSession(topic))
    with pytest.raises(HTTPException) as exc:
        await routes.publish_topic(topic.id, Principal(USER_A))
    assert exc.value.status_code == 409
    assert topic.is_public is False


async def test_publish_is_idempotent_and_keeps_the_original_date_and_mode(fake_scope):
    topic = _frozen()
    first = topic.published_at
    fake_scope(FakeSession(topic))
    result = await routes.publish_topic(
        topic.id, Principal(USER_A), routes.ShareBody(mode=SHARE_LIVE)
    )
    assert result["already_published"] is True
    assert topic.published_at == first
    # A second POST must not quietly unfreeze a snapshot somebody is reading.
    assert topic.share_mode == SHARE_FROZEN


async def test_publish_adopts_the_current_deliver_run_for_older_rows(fake_scope):
    """Rows that predate the public pointer would otherwise share a report the
    public router cannot resolve."""
    topic = _topic(public_deliver_run_id=None)
    fake_scope(FakeSession(topic))
    await routes.publish_topic(topic.id, Principal(USER_A))
    assert topic.public_deliver_run_id == topic.deliver_run_id


async def test_publishing_frozen_pauses_monitoring_and_its_schedule(fake_scope):
    topic = _topic()
    sub = _sub(topic, schedule_enabled=True, schedule_interval_hours=6, next_refresh_at=NOW)
    fake_scope(FakeSession(topic, sub))
    result = await routes.publish_topic(
        topic.id, Principal(USER_A), routes.ShareBody(mode=SHARE_FROZEN)
    )
    assert result["monitoring_paused"] is True
    assert topic.share_mode == SHARE_FROZEN
    assert topic.frozen_at is not None
    assert sub.status == "paused"
    assert sub.schedule_enabled is False
    assert sub.next_refresh_at is None


async def test_freezing_waits_for_a_refresh_that_is_already_running(fake_scope):
    """Otherwise the cycle finishes *after* the freeze and moves the snapshot
    readers were handed — `run_refresh` only checks the mode on entry."""
    topic = _topic()
    fake_scope(FakeSession(topic, _sub(topic, refresh_locked=True)))
    with pytest.raises(HTTPException) as exc:
        await routes.publish_topic(
            topic.id, Principal(USER_A), routes.ShareBody(mode=SHARE_FROZEN)
        )
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
    topic = _frozen()
    fake_scope(FakeSession(topic))
    result = await routes.unpublish_topic(topic.id, Principal(USER_A))
    assert topic.is_public is False
    assert topic.published_at is None
    assert topic.frozen_at is None
    assert result["public_path"] is None
    assert result["share_mode"] is None
    assert [e[1] for e in silent_emit] == ["topic.unpublished"]


async def test_unpublish_is_idempotent(fake_scope):
    topic = _topic()
    fake_scope(FakeSession(topic))
    result = await routes.unpublish_topic(topic.id, Principal(USER_A))
    assert result["already_private"] is True


async def test_unpublishing_a_live_share_leaves_monitoring_alone(fake_scope):
    topic = _live()
    sub = _sub(topic, schedule_enabled=True, schedule_interval_hours=6, next_refresh_at=NOW)
    fake_scope(FakeSession(topic, sub))
    await routes.unpublish_topic(topic.id, Principal(USER_A))
    assert sub.status == "active" and sub.schedule_enabled is True


# ---- switching mode while shared (#50) --------------------------------------


async def test_switching_to_frozen_pins_the_topic(fake_scope, silent_emit):
    topic = _live()
    sub = _sub(topic, schedule_enabled=True, schedule_interval_hours=6, next_refresh_at=NOW)
    fake_scope(FakeSession(topic, sub))
    result = await routes.set_share_mode(
        topic.id, routes.ShareBody(mode=SHARE_FROZEN), Principal(USER_A)
    )
    assert result["changed"] is True and result["monitoring_paused"] is True
    assert topic.share_mode == SHARE_FROZEN and topic.frozen_at is not None
    # The link itself is untouched — this changes what may move, not who may read.
    assert topic.is_public is True and result["public_path"] is not None
    assert [e[1] for e in silent_emit] == ["topic.share_mode_changed"]


async def test_switching_to_frozen_waits_for_a_running_refresh(fake_scope):
    topic = _live()
    fake_scope(FakeSession(topic, _sub(topic, refresh_locked=True)))
    with pytest.raises(HTTPException) as exc:
        await routes.set_share_mode(
            topic.id, routes.ShareBody(mode=SHARE_FROZEN), Principal(USER_A)
        )
    assert exc.value.status_code == 409
    assert topic.share_mode == SHARE_LIVE


async def test_switching_back_to_live_returns_control_but_not_spending(fake_scope):
    """Freezing turned monitoring off deliberately; turning it back on is a
    decision the owner makes, not a side effect of unfreezing."""
    topic = _frozen()
    sub = _sub(topic, status="paused", schedule_enabled=False)
    fake_scope(FakeSession(topic, sub))
    result = await routes.set_share_mode(
        topic.id, routes.ShareBody(mode=SHARE_LIVE), Principal(USER_A)
    )
    assert topic.share_mode == SHARE_LIVE and topic.frozen_at is None
    assert result["monitoring_paused"] is False
    assert sub.status == "paused" and sub.schedule_enabled is False


async def test_switching_to_the_same_mode_changes_nothing(fake_scope, silent_emit):
    topic = _live()
    fake_scope(FakeSession(topic))
    result = await routes.set_share_mode(
        topic.id, routes.ShareBody(mode=SHARE_LIVE), Principal(USER_A)
    )
    assert result["changed"] is False
    assert silent_emit == []


async def test_mode_cannot_be_set_on_a_private_topic(fake_scope):
    topic = _topic()
    fake_scope(FakeSession(topic))
    with pytest.raises(HTTPException) as exc:
        await routes.set_share_mode(
            topic.id, routes.ShareBody(mode=SHARE_FROZEN), Principal(USER_A)
        )
    assert exc.value.status_code == 409


async def test_another_user_cannot_change_your_share_mode(fake_scope):
    topic = _frozen()
    fake_scope(FakeSession(topic))
    with pytest.raises(HTTPException) as exc:
        await routes.set_share_mode(
            topic.id, routes.ShareBody(mode=SHARE_LIVE), Principal(USER_B)
        )
    assert exc.value.status_code == 404
    assert topic.share_mode == SHARE_FROZEN


# ---- a frozen share is pinned; a live one is not ----------------------------


async def test_mutable_rejects_a_frozen_share():
    topic = _frozen()
    session = FakeSession(topic)
    with pytest.raises(HTTPException) as exc:
        await routes._mutable(session, topic.id, Principal(USER_A))
    assert exc.value.status_code == 409
    assert "live sharing" in exc.value.detail


async def test_mutable_accepts_a_live_share():
    """The whole point of #50: publishing does not take the topic away."""
    topic = _live()
    session = FakeSession(topic)
    assert await routes._mutable(session, topic.id, Principal(USER_A)) is topic


async def test_a_private_topic_is_never_frozen_by_a_stale_mode():
    """`share_mode` is meaningless until the row is shared — reading it the other
    way would let an unshared topic lock its own owner out."""
    topic = _topic(is_public=False, share_mode=SHARE_FROZEN)
    session = FakeSession(topic)
    assert await routes._mutable(session, topic.id, Principal(USER_A)) is topic


async def test_owner_still_reads_a_frozen_share():
    topic = _frozen()
    session = FakeSession(topic)
    assert await routes._owned(session, topic.id, Principal(USER_A)) is topic


@pytest.mark.parametrize("state", ["planned_awaiting_review", "reported", "planning"])
def test_frozen_shares_advertise_no_actions(state):
    assert routes._actions(state, True) == []
    # ...and a live share advertises exactly what a private topic would.
    assert routes._actions(state, False) == routes._actions(state)


async def test_refresh_endpoint_refuses_a_frozen_share(fake_scope):
    topic = _frozen()
    fake_scope(FakeSession(topic))
    dispatched: list[tuple] = []
    background = SimpleNamespace(add_task=lambda *a, **k: dispatched.append(a))

    with pytest.raises(HTTPException) as exc:
        await routes.trigger_refresh(topic.id, background, Principal(USER_A), _settings())
    assert exc.value.status_code == 409
    assert dispatched == []


async def test_refresh_endpoint_accepts_a_live_share(fake_scope):
    topic = _live()
    fake_scope(FakeSession(topic, _sub(topic)))
    dispatched: list[tuple] = []
    background = SimpleNamespace(add_task=lambda *a, **k: dispatched.append(a))

    result = await routes.trigger_refresh(topic.id, background, Principal(USER_A), _settings())
    assert result["accepted"] is True
    assert dispatched and dispatched[0][0] is refresh_mod.run_refresh


async def test_monitor_endpoint_refuses_a_frozen_share(fake_scope):
    topic = _frozen()
    fake_scope(FakeSession(topic))
    with pytest.raises(HTTPException) as exc:
        await routes.start_monitoring(
            topic.id, routes.MonitorBody(), Principal(USER_A), _settings()
        )
    assert exc.value.status_code == 409


async def test_proceed_refuses_a_frozen_share(fake_scope):
    topic = _frozen(state="planned_awaiting_review")
    fake_scope(FakeSession(topic))
    dispatched: list[tuple] = []
    background = SimpleNamespace(add_task=lambda *a, **k: dispatched.append(a))

    with pytest.raises(HTTPException) as exc:
        await routes.proceed(topic.id, background, Principal(USER_A), _settings())
    assert exc.value.status_code == 409
    assert dispatched == []


# ---- a reader only ever sees finished state (#50) ---------------------------


async def test_public_artifacts_read_the_public_pointer(fake_scope, monkeypatch):
    """Not `deliver_run_id`: that is assigned before a deliver run writes
    anything, so serving it would 404 a live link for the length of a re-run."""
    topic = _live()
    topic.deliver_run_id = "deliver-2-in-flight"
    topic.public_deliver_run_id = "deliver-1"
    fake_scope(FakeSession(topic))
    served: list[str | None] = []
    monkeypatch.setattr(
        public_routes,
        "artifact_response",
        lambda settings, topic_hash, run_id, filename: served.append(run_id),
    )

    await public_routes.get_public_report_md(topic.id, _settings())
    await public_routes.get_public_news(topic.id, _settings())
    assert served == ["deliver-1", "deliver-1"]


async def test_a_topic_with_no_finished_run_reports_no_report(fake_scope):
    topic = _live(public_deliver_run_id=None)
    fake_scope(FakeSession(topic))
    payload = await public_routes.get_public_topic(topic.id, Response())
    assert payload["has_report"] is False


async def test_public_deltas_hide_a_cycle_that_is_still_running(fake_scope):
    topic = _live()
    session = FakeSession(topic, _delta(topic, 1, "completed"), _delta(topic, 2, "running"))
    fake_scope(session, routes, public_routes, refresh_mod)

    result = await public_routes.list_public_deltas(topic.id)
    assert [d["seq"] for d in result["deltas"]] == [1]


async def test_public_deltas_hide_a_failed_cycle(fake_scope):
    topic = _live()
    session = FakeSession(topic, _delta(topic, 1, "completed"), _delta(topic, 2, "failed"))
    fake_scope(session, routes, public_routes, refresh_mod)

    result = await public_routes.list_public_deltas(topic.id)
    assert [d["seq"] for d in result["deltas"]] == [1]


async def test_a_running_cycles_artifacts_are_not_served(fake_scope):
    """Its `report.md` does not exist yet; a reader must get "not here", not a
    file the pipeline is halfway through writing."""
    topic = _live()
    fake_scope(FakeSession(topic, _delta(topic, 2, "running")))
    with pytest.raises(HTTPException) as exc:
        await public_routes.get_public_delta_report(topic.id, 2, _settings())
    assert exc.value.status_code == 404


async def test_public_payload_counts_only_completed_cycles(fake_scope):
    topic = _live()
    fake_scope(FakeSession(
        topic, _delta(topic, 1, "completed"), _delta(topic, 2, "completed"),
        _delta(topic, 3, "running"),
    ))
    payload = await public_routes.get_public_topic(topic.id, Response())
    assert payload["updates"] == {
        "live": True,
        "last_updated_at": NOW.isoformat(),
        "update_count": 2,
        "latest_seq": 2,
    }


async def test_the_detail_route_is_cacheable(fake_scope):
    """A live share is polled by every open tab; without this the poll is a DB
    read per reader per interval."""
    topic = _live()
    fake_scope(FakeSession(topic))
    response = Response()
    await public_routes.get_public_topic(topic.id, response)
    assert response.headers["Cache-Control"] == "public, max-age=30"


async def test_advance_public_view_moves_the_pointer_and_the_stamp(monkeypatch):
    topic = _live(public_deliver_run_id="deliver-1")

    @asynccontextmanager
    async def _scope():
        yield FakeSession(topic)

    monkeypatch.setattr(serving, "session_scope", _scope)

    await serving.advance_public_view(topic.id, deliver_run_id="deliver-2")
    assert topic.public_deliver_run_id == "deliver-2"
    assert topic.public_updated_at > NOW

    # A refresh cycle produces no new deliver run — only the stamp moves.
    stamped = topic.public_updated_at
    await serving.advance_public_view(topic.id)
    assert topic.public_deliver_run_id == "deliver-2"
    assert topic.public_updated_at > stamped


# ---- nothing spends money on a frozen share ---------------------------------


async def test_run_refresh_skips_a_frozen_share(monkeypatch, silent_emit):
    """The last line of defence: a refresh already queued when the owner froze
    the share must not start a Claude run."""
    topic = _frozen()

    @asynccontextmanager
    async def _scope():
        yield FakeSession(topic)

    monkeypatch.setattr(refresh_mod, "session_scope", _scope)

    async def _fail_lock(_subscription_id):
        raise AssertionError("run_refresh must bail out before taking the lock")

    monkeypatch.setattr(refresh_mod, "_try_acquire_lock", _fail_lock)

    await refresh_mod.run_refresh(topic.id, 1, _settings(), trigger="scheduled")

    assert [(e[1], e[2]["reason"]) for e in silent_emit] == [
        ("refresh.skipped", "topic_frozen")
    ]


async def test_run_refresh_proceeds_on_a_live_share(monkeypatch, silent_emit):
    """Sharing must not silently stop the monitoring the reader is being shown."""
    topic = _live()

    @asynccontextmanager
    async def _scope():
        yield FakeSession(topic)

    monkeypatch.setattr(refresh_mod, "session_scope", _scope)
    reached: list[int] = []

    async def _lock(subscription_id):
        reached.append(subscription_id)
        return False  # stop here; getting this far is the assertion

    monkeypatch.setattr(refresh_mod, "_try_acquire_lock", _lock)

    await refresh_mod.run_refresh(topic.id, 1, _settings(), trigger="scheduled")
    assert reached == [1]


async def test_scheduler_claims_live_shares_but_never_frozen_ones(monkeypatch):
    """The mode filter has to be in the statement Postgres runs, not in a Python
    check after it — asserted against the compiled SQL."""
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
    assert "share_mode" in sql
    assert "NOT IN" in sql.upper()
