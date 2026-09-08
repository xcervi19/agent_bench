"""A monitoring plan has to be changeable after the topic is under monitoring (#51).

The plan is written once at `POST /monitor` and, before this, `PATCH /monitor`
could not touch it — so no query improvement could ever reach a topic that was
already being watched, which is every topic worth improving. This is the
affordance only; *which* queries to change from measured yield is #46.

Validation matters more here than in most routes: what arrives goes straight
into the refresh agent's `input.json`. `allowed_domains` is the field the care is
for — it is the structured form of a `site:` filter and the reason official
sources are reachable at all, so an entry that loses it silently becomes an open
web search on every cycle from then on.

No DB: `session_scope` is stubbed.
"""

from __future__ import annotations

import uuid
from contextlib import asynccontextmanager
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from apps.claude_agent.auth import Principal
from apps.claude_agent.config import ClaudeAgentSettings
from apps.claude_agent.topics import routes
from apps.claude_agent.topics.models import Topic, TopicSubscription
from apps.claude_agent.topics.refresh import validate_short_term_queries

USER = uuid.uuid4()
TOPIC_ID = uuid.uuid4()


# ---- the validator ---------------------------------------------------------


def test_a_plan_entry_keeps_its_domain_filter():
    [entry] = validate_short_term_queries(
        [{"query": "india gas sectoral consumption", "allowed_domains": ["PPAC.gov.in"]}]
    )
    assert entry["allowed_domains"] == ["ppac.gov.in"], "normalised to a bare host"
    assert entry["query"] == "india gas sectoral consumption"
    assert entry["id"] == "st01"


def test_an_unfiltered_entry_omits_the_field_rather_than_carrying_an_empty_one():
    [entry] = validate_short_term_queries([{"query": "open web question"}])
    assert "allowed_domains" not in entry


def test_an_empty_domain_list_is_refused_rather_than_stored():
    """Absent means "search the whole web", empty means "allow nothing". A caller
    who sent `[]` meant the first, and storing it would silently mute the query."""
    with pytest.raises(ValueError, match="omit the field"):
        validate_short_term_queries([{"query": "q", "allowed_domains": []}])


def test_ids_are_renumbered_rather_than_trusted():
    """`executed_queries` in the refresh artifact keys on these, so a duplicate
    or a gap makes the delta unreadable."""
    entries = validate_short_term_queries(
        [{"query": "a", "id": "st07"}, {"query": "b", "id": "st07"}]
    )
    assert [e["id"] for e in entries] == ["st01", "st02"]


def test_defaults_match_what_the_builder_produces():
    [entry] = validate_short_term_queries([{"query": "q"}])
    assert entry["language"] == "en"
    assert entry["priority"] == 2
    assert set(entry) == {"query", "language", "priority", "source", "rationale", "id"}


@pytest.mark.parametrize(
    "bad",
    [
        {"query": "   "},
        {"query": "q", "language": "english"},
        {"query": "q", "priority": 0},
        {"query": "q", "priority": 99},
        {"query": "q", "allowed_domains": "ppac.gov.in"},
        "not an object",
    ],
)
def test_a_malformed_entry_is_refused(bad):
    with pytest.raises(ValueError):
        validate_short_term_queries([bad])


def test_the_body_itself_must_be_a_list():
    with pytest.raises(ValueError, match="must be a list"):
        validate_short_term_queries({"query": "q"})


def test_an_empty_plan_is_accepted():
    """A topic can legitimately be parked with no queries; the refresh command
    handles that case explicitly rather than crashing."""
    assert validate_short_term_queries([]) == []


# ---- the route -------------------------------------------------------------


class FakeSession:
    def __init__(self, topic: Topic, sub: TopicSubscription) -> None:
        self.topic = topic
        self.sub = sub

    async def get(self, model, pk):
        return self.topic if model is Topic else self.sub

    async def execute(self, stmt):
        return SimpleNamespace(scalar_one_or_none=lambda: self.sub)


@pytest.fixture
def patch_monitor(monkeypatch):
    topic = Topic(
        id=TOPIC_ID,
        owner_user_id=USER,
        topic="india gas",
        state="reported",
        topic_id_hash="h",
        plan_run_id="plan-1",
        deliver_run_id="deliver-1",
        last_event_seq=0,
        is_public=False,
        share_mode="live",
    )
    sub = TopicSubscription(
        id=1,
        topic_id=TOPIC_ID,
        status="active",
        short_term_queries=[{"id": "st01", "query": "old", "priority": 2}],
        max_age_hours=48,
        schedule_enabled=False,
        schedule_interval_hours=None,
        refresh_count=0,
        refresh_locked=False,
    )
    session = FakeSession(topic, sub)

    @asynccontextmanager
    async def _scope():
        yield session

    monkeypatch.setattr(routes, "session_scope", _scope)

    emitted: list[tuple[str, dict]] = []

    async def _emit(topic_id, event_type, payload):
        emitted.append((event_type, payload))

    monkeypatch.setattr(routes, "emit", _emit)

    async def _call(body: dict):
        return await routes.update_monitoring(
            TOPIC_ID,
            routes.UpdateMonitorBody(**body),
            Principal(user_id=USER),
            ClaudeAgentSettings(database_url="postgresql+asyncpg://x/y"),
        )

    return SimpleNamespace(call=_call, sub=sub, emitted=emitted)


async def test_patch_replaces_the_plan_and_preserves_the_filter(patch_monitor):
    await patch_monitor.call({
        "short_term_queries": [
            {"query": "ppac monthly gas balance", "allowed_domains": ["ppac.gov.in"]},
            {"query": "cgd authorisations", "priority": 1},
        ]
    })

    stored = patch_monitor.sub.short_term_queries
    assert [e["query"] for e in stored] == ["ppac monthly gas balance", "cgd authorisations"]
    assert stored[0]["allowed_domains"] == ["ppac.gov.in"]
    assert "allowed_domains" not in stored[1]


async def test_patch_rejects_a_malformed_plan_without_touching_the_stored_one(patch_monitor):
    before = list(patch_monitor.sub.short_term_queries)

    with pytest.raises(HTTPException) as exc:
        await patch_monitor.call({"short_term_queries": [{"query": ""}]})

    assert exc.value.status_code == 422
    assert patch_monitor.sub.short_term_queries == before


async def test_the_event_says_how_many_queries_the_topic_now_runs(patch_monitor):
    """A plan change alters what every later cycle costs and covers, so the size
    of it belongs on the event log rather than only in the database."""
    await patch_monitor.call({
        "short_term_queries": [{"query": "a"}, {"query": "b"}, {"query": "c"}]
    })

    [(name, payload)] = patch_monitor.emitted
    assert name == "monitor.updated"
    assert payload["queries_count"] == 3


async def test_a_patch_that_does_not_mention_the_plan_leaves_it_alone(patch_monitor):
    before = list(patch_monitor.sub.short_term_queries)

    result = await patch_monitor.call({"max_age_hours": 72})

    assert patch_monitor.sub.short_term_queries == before
    assert patch_monitor.sub.max_age_hours == 72
    assert result["queries_count"] == 1
