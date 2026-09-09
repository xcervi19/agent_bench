"""Everything we already hold reaches the analyst (#51).

Four mechanisms collect material for a topic — the #42 evidence store, the RAG
corpus, #45's official feeds, and the plan leg's own retrieval — and before this
ticket the leg that writes the report a customer reads consumed almost none of
it. These tests hold the connections open.

The property under test is not "the report is better". That is #23/#41 and one
run cannot show it. It is the narrower, checkable one: **the inputs arrived, and
the run says so** — so a later comparison has counters to compare rather than a
state directory to go digging in.

No DB and no network: `session_scope` is stubbed and the agent leg is a fake that
writes the artifacts a real one would.
"""

from __future__ import annotations

import json
import logging
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from types import SimpleNamespace

import pytest

from apps.claude_agent.config import ClaudeAgentSettings
from apps.claude_agent.topics import pipeline as pipeline_mod
from apps.claude_agent.topics import refresh as refresh_mod
from apps.claude_agent.topics.facets import FACETS_SCHEMA_VERSION, fallback_facets
from apps.claude_agent.topics.models import Topic, TopicSubscription
from apps.claude_agent.topics.source_quality import SOURCE_MIX_FILENAME

TOPIC_ID = uuid.uuid4()
TOPIC_HASH = "h" * 40
PLAN_RUN_ID = "plan-1"
TOPIC_TEXT = "India natural gas demand"

NEWS = {
    "sources": [
        {"id": "s01", "url": "https://ppac.gov.in/x", "source_class": "primary_official"},
        {"id": "s02", "url": "https://example.com/y", "source_class": "specialist_outlet"},
    ]
}
SUMMARY = {"summary_md": "ok", "thesis_status": "supported", "sources_count": 2}


def _settings(tmp_path: Path, **over) -> ClaudeAgentSettings:
    base = dict(state_dir=str(tmp_path / "state"), database_url="postgresql+asyncpg://x/y")
    base.update(over)
    return ClaudeAgentSettings(**base)


def _topic() -> Topic:
    return Topic(
        id=TOPIC_ID,
        topic=TOPIC_TEXT,
        state="planned_awaiting_review",
        topic_id_hash=TOPIC_HASH,
        plan_run_id=PLAN_RUN_ID,
        last_event_seq=0,
    )


class FakeSession:
    """Enough of AsyncSession for the two orchestration legs: get by pk, add, execute."""

    def __init__(self, *rows: object) -> None:
        self.rows = list(rows)
        self.added: list[object] = []

    def add(self, obj: object) -> None:
        self.added.append(obj)

    async def flush(self) -> None:
        return None

    async def get(self, model, pk):
        return next((r for r in self.rows if isinstance(r, model)), None)

    async def execute(self, stmt):
        return SimpleNamespace(
            scalar_one=lambda: 1,
            scalar_one_or_none=lambda: 1,
            scalars=lambda: SimpleNamespace(all=lambda: []),
            all=lambda: [],
        )


@pytest.fixture
def events(monkeypatch):
    """Every emitted event, in order. Both legs emit through the same function."""
    seen: list[tuple[str, dict]] = []

    async def _emit(topic_id, event_type, payload):
        seen.append((event_type, payload))
        return len(seen)

    monkeypatch.setattr(pipeline_mod, "emit", _emit)
    monkeypatch.setattr(refresh_mod, "emit", _emit)
    return seen


def _payload(events: list[tuple[str, dict]], event_type: str, **match) -> dict:
    for name, payload in events:
        if name == event_type and all(payload.get(k) == v for k, v in match.items()):
            return payload
    raise AssertionError(f"no {event_type} event matching {match} in {[e[0] for e in events]}")


# ---------------------------------------------------------------------------
# the deliver leg
# ---------------------------------------------------------------------------


@pytest.fixture
def deliver(monkeypatch, tmp_path):
    """Drive `run_deliver` with a fake agent leg that writes what a real one writes."""
    session = FakeSession(_topic())

    @asynccontextmanager
    async def _scope():
        yield session

    monkeypatch.setattr(pipeline_mod, "session_scope", _scope)

    async def _advance(topic_id, **kwargs):
        return None

    monkeypatch.setattr(pipeline_mod, "advance_public_view", _advance)
    monkeypatch.setattr(pipeline_mod, "load_whitelisted_domains", lambda: frozenset())

    async def _stream(req, settings):
        run_dir = Path(req.args)
        (run_dir / "news.json").write_text(json.dumps(NEWS), encoding="utf-8")
        (run_dir / "summary.json").write_text(json.dumps(SUMMARY), encoding="utf-8")
        yield json.dumps({"type": "result", "subtype": "success", "duration_ms": 12})

    monkeypatch.setattr(pipeline_mod, "stream_claude", _stream)

    # The corpus wait talks to the database through its own session scope, not
    # the one patched above. A drained queue is the uninteresting case, so it is
    # the default here and the waiting tests below override it.
    async def _drained(topic_id):
        return 0

    monkeypatch.setattr(pipeline_mod, "pending_count", _drained)
    monkeypatch.setattr(pipeline_mod, "CORPUS_POLL_SEC", 0.01)

    async def _run(settings: ClaudeAgentSettings) -> Path:
        await pipeline_mod.run_deliver(TOPIC_ID, settings)
        runs = Path(settings.state_dir) / "news" / TOPIC_HASH / "runs"
        written = [d for d in runs.iterdir() if d.name != PLAN_RUN_ID]
        assert len(written) == 1, "exactly one deliver run dir"
        return written[0]

    return _run


def _cache_facets(settings: ClaudeAgentSettings, facets: dict) -> None:
    path = Path(settings.state_dir) / "news" / TOPIC_HASH / "facets.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(facets), encoding="utf-8")


def _good_facets() -> dict:
    return {
        "schema_version": FACETS_SCHEMA_VERSION,
        "topic": TOPIC_TEXT,
        "canonical_topic_en": TOPIC_TEXT,
        "input_language": "en",
        "source_languages": ["en"],
        "commodity": ["natural gas"],
        "geo": ["India"],
        "entities": [],
        "signals": [],
        "degraded": False,
        "degraded_reason": None,
    }


async def test_deliver_exports_the_corpus_and_says_where_it_is(monkeypatch, tmp_path, deliver, events):
    """The whole ticket in one assertion: the deliver leg no longer writes the
    baseline report from search snippets while the full text sits in the store."""
    exported: dict = {}

    async def _export(topic_id, destination, *, max_documents, **kwargs):
        destination.mkdir(parents=True, exist_ok=True)
        (destination / "a1b2.md").write_text("full article text", encoding="utf-8")
        exported["max_documents"] = max_documents
        return {"document_count": 3, "unreadable_count": 1}

    monkeypatch.setattr(pipeline_mod, "export_evidence", _export)
    settings = _settings(tmp_path, evidence_max_documents=25)

    run_dir = await deliver(settings)

    payload = json.loads((run_dir / "input.json").read_text(encoding="utf-8"))
    assert payload["evidence_dir"] == str(run_dir / "evidence")
    assert payload["evidence_count"] == 3
    assert payload["evidence_unreadable_count"] == 1
    assert (run_dir / "evidence" / "a1b2.md").is_file()
    assert exported["max_documents"] == 25, "the cap is the configured one"


async def test_a_corpus_failure_does_not_cost_the_report(monkeypatch, tmp_path, deliver, events):
    """`run_refresh` has always degraded this way; deliver must match it. A
    report the customer can read beats a corpus we could not export."""

    async def _boom(*args, **kwargs):
        raise RuntimeError("the store is down")

    monkeypatch.setattr(pipeline_mod, "export_evidence", _boom)

    run_dir = await deliver(_settings(tmp_path))

    payload = json.loads((run_dir / "input.json").read_text(encoding="utf-8"))
    assert payload["evidence_dir"] is None
    assert payload["evidence_count"] == 0
    assert _payload(events, "report.ready"), "the run still finished"


async def test_a_zero_cap_disables_the_export_entirely(monkeypatch, tmp_path, deliver, events):
    called: list[int] = []

    async def _export(*args, **kwargs):
        called.append(1)
        return {"document_count": 1, "unreadable_count": 0}

    monkeypatch.setattr(pipeline_mod, "export_evidence", _export)

    run_dir = await deliver(_settings(tmp_path, evidence_max_documents=0))

    assert called == []
    assert json.loads((run_dir / "input.json").read_text())["evidence_dir"] is None


async def test_the_run_says_what_the_analyst_was_given(monkeypatch, tmp_path, deliver, events):
    """These four counters are what a second India run is compared against. Read
    off the event log, they need no access to the state directory."""

    async def _export(topic_id, destination, **kwargs):
        return {"document_count": 106, "unreadable_count": 15}

    monkeypatch.setattr(pipeline_mod, "export_evidence", _export)
    settings = _settings(tmp_path)
    _cache_facets(settings, _good_facets())

    await deliver(settings)

    finished = _payload(events, "stage.finished", stage="deliver")
    assert finished["evidence_count"] == 106
    assert finished["evidence_unreadable_count"] == 15
    assert finished["feeds_count"] == 0
    assert finished["facets_degraded"] is False


async def test_degraded_facets_are_visible_rather_than_a_silent_zero(
    monkeypatch, tmp_path, deliver, events, caplog
):
    """`fallback_facets` empties commodity and geo, and `feeds.matches` then
    refuses every feed — so a parse-leg failure removes the whole official-data
    channel with no error. The count of zero is correct and uninformative; the
    signal is what separates "no feed applies" from "the topic has no facets"."""

    async def _export(topic_id, destination, **kwargs):
        return {"document_count": 0, "unreadable_count": 0}

    monkeypatch.setattr(pipeline_mod, "export_evidence", _export)
    settings = _settings(tmp_path)
    _cache_facets(settings, fallback_facets(TOPIC_TEXT, reason="TimeoutError: parse leg"))

    with caplog.at_level(logging.WARNING):
        await deliver(settings)

    assert _payload(events, "stage.finished", stage="deliver")["facets_degraded"] is True
    assert "deliver.facets_degraded" in "\n".join(r.getMessage() for r in caplog.records)


async def test_a_topic_that_never_parsed_counts_as_degraded(
    monkeypatch, tmp_path, deliver, events
):
    """No cached facets is the same blindness as degraded ones, and must not be
    reported as a healthy run that happened to match no feed."""

    async def _export(topic_id, destination, **kwargs):
        return {"document_count": 0, "unreadable_count": 0}

    monkeypatch.setattr(pipeline_mod, "export_evidence", _export)

    await deliver(_settings(tmp_path))

    assert _payload(events, "stage.finished", stage="deliver")["facets_degraded"] is True


async def test_the_deliver_run_records_the_source_mix_on_disk(
    monkeypatch, tmp_path, deliver, events
):
    """A public reader gets no event stream, so the figure has to be a file —
    otherwise the UI is left recomputing a narrower one of its own (#51 item 7)."""

    async def _export(topic_id, destination, **kwargs):
        return {"document_count": 0, "unreadable_count": 0}

    monkeypatch.setattr(pipeline_mod, "export_evidence", _export)

    run_dir = await deliver(_settings(tmp_path))

    written = json.loads((run_dir / SOURCE_MIX_FILENAME).read_text(encoding="utf-8"))
    assert written == _payload(events, "report.ready")["source_mix"]
    assert written["total"] == 2
    assert written["authoritative"] == 1


# ---------------------------------------------------------------------------
# the refresh leg — the same counters, the same signal
# ---------------------------------------------------------------------------


@pytest.fixture
def do_refresh(monkeypatch, tmp_path):
    session = FakeSession(_topic(), TopicSubscription(
        id=1,
        topic_id=TOPIC_ID,
        status="active",
        short_term_queries=[],
        max_age_hours=48,
        refresh_count=0,
    ))

    @asynccontextmanager
    async def _scope():
        yield session

    monkeypatch.setattr(refresh_mod, "session_scope", _scope)

    async def _true(*args, **kwargs):
        return True

    async def _false(*args, **kwargs):
        return False

    async def _none(*args, **kwargs):
        return None

    monkeypatch.setattr(refresh_mod, "_is_frozen", _false)
    monkeypatch.setattr(refresh_mod, "_try_acquire_lock", _true)
    monkeypatch.setattr(refresh_mod, "_release_lock", _none)
    monkeypatch.setattr(refresh_mod, "advance_public_view", _none)
    monkeypatch.setattr(refresh_mod, "load_whitelisted_domains", lambda: frozenset())

    async def _slash(topic_id, refresh_dir, settings):
        (refresh_dir / "news.json").write_text(json.dumps(NEWS), encoding="utf-8")
        return 0.1, 12, None, {"new_sources_count": 1, "queries_executed": 2}

    monkeypatch.setattr(refresh_mod, "_run_refresh_slash", _slash)

    async def _export(topic_id, destination, **kwargs):
        return {"document_count": 42, "unreadable_count": 7}

    monkeypatch.setattr(refresh_mod, "export_evidence", _export)

    async def _run(settings: ClaudeAgentSettings) -> None:
        await refresh_mod.run_refresh(TOPIC_ID, 1, settings)

    return _run


async def test_refresh_reports_the_same_counters(tmp_path, do_refresh, events):
    settings = _settings(tmp_path)
    _cache_facets(settings, _good_facets())

    await do_refresh(settings)

    completed = _payload(events, "refresh.completed")
    assert completed["evidence_count"] == 42
    assert completed["evidence_unreadable_count"] == 7
    assert completed["feeds_count"] == 0
    assert completed["facets_degraded"] is False


async def test_refresh_says_when_its_facets_degraded(tmp_path, do_refresh, events, caplog):
    settings = _settings(tmp_path)
    _cache_facets(settings, fallback_facets(TOPIC_TEXT, reason="ValueError: empty"))

    with caplog.at_level(logging.WARNING):
        await do_refresh(settings)

    assert _payload(events, "refresh.completed")["facets_degraded"] is True
    assert "refresh.facets_degraded" in "\n".join(r.getMessage() for r in caplog.records)


# ---- waiting for the corpus to be fetched ----------------------------------
#
# The plan leg records a hit the moment it sees one; the fetcher reads the page
# behind it on a background poll. Deliver starts when the operator proceeds,
# which on a fresh topic is a minute later — so without a wait the foundational
# report is written from whatever happened to be fetched by then. On the India
# run of 2026-09-09 that was 5 documents out of 149 captured.


async def test_deliver_waits_for_its_own_documents_to_be_fetched(
    monkeypatch, tmp_path, deliver, events
):
    counts = iter([7, 3, 0])
    seen: list[int] = []

    async def _pending(topic_id):
        value = next(counts)
        seen.append(value)
        return value

    monkeypatch.setattr(pipeline_mod, "pending_count", _pending)

    exported: dict = {}

    async def _export(topic_id, destination, *, max_documents, **kwargs):
        destination.mkdir(parents=True, exist_ok=True)
        exported["called"] = True
        return {"document_count": 61, "unreadable_count": 4}

    monkeypatch.setattr(pipeline_mod, "export_evidence", _export)

    run_dir = await deliver(_settings(tmp_path, deliver_corpus_wait_sec=30))

    assert seen == [7, 3, 0], "polled until the queue drained"
    assert exported["called"], "exported only after waiting"
    payload = json.loads((run_dir / "input.json").read_text(encoding="utf-8"))
    assert payload["evidence_count"] == 61


async def test_a_queue_that_will_not_drain_still_delivers(
    monkeypatch, tmp_path, deliver, events, caplog
):
    """A slow host must cost the wait once, not the report."""

    async def _stuck(topic_id):
        return 12

    monkeypatch.setattr(pipeline_mod, "pending_count", _stuck)

    async def _export(topic_id, destination, *, max_documents, **kwargs):
        destination.mkdir(parents=True, exist_ok=True)
        return {"document_count": 5, "unreadable_count": 0}

    monkeypatch.setattr(pipeline_mod, "export_evidence", _export)

    with caplog.at_level(logging.WARNING):
        run_dir = await deliver(_settings(tmp_path, deliver_corpus_wait_sec=1))

    assert (run_dir / "news.json").is_file(), "the report is written anyway"
    assert "corpus_wait_expired" in caplog.text
    assert "pending=12" in caplog.text


async def test_a_corpus_wait_failure_does_not_cost_the_report(
    monkeypatch, tmp_path, deliver, events
):
    async def _boom(topic_id):
        raise RuntimeError("database is down")

    monkeypatch.setattr(pipeline_mod, "pending_count", _boom)

    async def _export(topic_id, destination, *, max_documents, **kwargs):
        destination.mkdir(parents=True, exist_ok=True)
        return {"document_count": 2, "unreadable_count": 0}

    monkeypatch.setattr(pipeline_mod, "export_evidence", _export)

    run_dir = await deliver(_settings(tmp_path, deliver_corpus_wait_sec=30))
    assert (run_dir / "news.json").is_file()


async def test_a_zero_wait_does_not_query_the_queue_at_all(
    monkeypatch, tmp_path, deliver, events
):
    async def _never(topic_id):
        raise AssertionError("the queue must not be counted when the wait is off")

    monkeypatch.setattr(pipeline_mod, "pending_count", _never)

    async def _export(topic_id, destination, *, max_documents, **kwargs):
        destination.mkdir(parents=True, exist_ok=True)
        return {"document_count": 1, "unreadable_count": 0}

    monkeypatch.setattr(pipeline_mod, "export_evidence", _export)

    run_dir = await deliver(_settings(tmp_path, deliver_corpus_wait_sec=0))
    assert (run_dir / "news.json").is_file()
