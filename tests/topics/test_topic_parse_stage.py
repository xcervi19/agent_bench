"""Offline tests for the topic_parse pre-plan stage (#38).

No DB and no CLI: `emit` and `stream_claude` are stubbed. The property under
test is that grounding is best-effort — the stage improves discovery when the
agent cooperates and never blocks a run when it does not.
"""

from __future__ import annotations

import asyncio
import json
import uuid
from pathlib import Path

import pytest

from apps.claude_agent.config import ClaudeAgentSettings
from apps.claude_agent.topics import pipeline
from apps.claude_agent.topics.facets import (
    FACETS_FILENAME,
    discovery_query,
    fallback_facets,
    normalize_facets,
)

CZECH_TOPIC = "Situace kolem Hormuzského průplavu a dodávky ropy"

AGENT_FACETS = {
    "schema_version": "0.1.0",
    "canonical_topic_en": "Strait of Hormuz situation and crude oil supply",
    "input_language": "cs",
    "geo": ["Strait of Hormuz", "Persian Gulf"],
    "commodity": ["crude oil", "LNG"],
    "entities": ["NIOC", "ADNOC"],
    "signals": ["exports", "shipping disruption"],
    "source_languages": ["ar", "fa", "cs"],
}


@pytest.fixture
def emitted(monkeypatch):
    events: list[tuple[str, dict]] = []

    async def fake_emit(topic_id, event_type, payload):
        events.append((event_type, payload))
        return len(events)

    monkeypatch.setattr(pipeline, "emit", fake_emit)
    return events


@pytest.fixture
def settings(tmp_path: Path) -> ClaudeAgentSettings:
    return ClaudeAgentSettings(state_dir=str(tmp_path / "state"))


def stub_leg(monkeypatch, *, writes: dict | None, exit_ok: bool = True):
    """Replace the CLI with a stand-in that writes `facets.json` like the agent.

    Returns a counter so tests can prove the cache avoids a second call.
    """
    calls: list[str] = []

    async def fake_stream(req, _settings):
        calls.append(req.command)
        if writes is not None:
            path = Path(req.args) / FACETS_FILENAME
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(writes), encoding="utf-8")
        subtype = "success" if exit_ok else "error_during_execution"
        yield json.dumps({"type": "result", "subtype": subtype})

    monkeypatch.setattr(pipeline, "stream_claude", fake_stream)
    return calls


def parse(topic: str, out_dir: Path, settings: ClaudeAgentSettings) -> dict:
    return asyncio.run(pipeline.run_topic_parse(uuid.uuid4(), topic, out_dir, settings))


# ── Contract ────────────────────────────────────────────────────────────────


def test_normalize_rejects_output_without_a_canonical_topic():
    with pytest.raises(ValueError):
        normalize_facets({"geo": ["Iran"]}, CZECH_TOPIC)


def test_normalize_drops_junk_and_always_keeps_english():
    facets = normalize_facets(
        {
            "canonical_topic_en": "  Strait of Hormuz   supply  ",
            "input_language": "Czech",
            "geo": ["Iran", "Iran", 42, "  ", "Oman"],
            "source_languages": ["ar", "farsi"],
        },
        CZECH_TOPIC,
    )
    assert facets["canonical_topic_en"] == "Strait of Hormuz supply"
    assert facets["input_language"] == "und"
    assert facets["geo"] == ["Iran", "Oman"]
    assert facets["source_languages"][0] == "en"
    assert "ar" in facets["source_languages"]
    assert facets["degraded"] is False


def test_discovery_query_carries_english_facets_and_the_raw_topic():
    query = discovery_query(normalize_facets(AGENT_FACETS, CZECH_TOPIC))
    assert "Strait of Hormuz" in query
    assert "NIOC" in query
    assert "crude oil" in query
    # The original wording still earns inflection matches on shared proper nouns.
    assert "Hormuzského" in query


def test_fallback_preserves_the_untranslated_topic():
    facets = fallback_facets(CZECH_TOPIC, reason="timeout")
    assert facets["degraded"] is True
    assert facets["degraded_reason"] == "timeout"
    assert discovery_query(facets).startswith("Situace kolem")


# ── Stage behaviour ─────────────────────────────────────────────────────────


def test_stage_writes_facets_and_reports_the_language(tmp_path, emitted, settings, monkeypatch):
    stub_leg(monkeypatch, writes=AGENT_FACETS)
    facets = parse(CZECH_TOPIC, tmp_path, settings)

    written = json.loads((tmp_path / FACETS_FILENAME).read_text(encoding="utf-8"))
    assert written == facets
    assert facets["canonical_topic_en"] == AGENT_FACETS["canonical_topic_en"]
    assert [name for name, _ in emitted] == ["stage.started", "stage.finished"]
    finished = emitted[-1][1]
    assert finished["stage"] == "topic_parse"
    assert finished["input_language"] == "cs"
    assert finished["degraded"] is False


def test_second_run_of_the_same_topic_reuses_the_cache(tmp_path, emitted, settings, monkeypatch):
    calls = stub_leg(monkeypatch, writes=AGENT_FACETS)
    first = parse(CZECH_TOPIC, tmp_path / "run1", settings)
    second = parse(CZECH_TOPIC, tmp_path / "run2", settings)

    assert len(calls) == 1
    assert second["canonical_topic_en"] == first["canonical_topic_en"]
    assert emitted[1][1]["cached"] is False
    assert emitted[3][1]["cached"] is True


@pytest.mark.parametrize(
    "kind,stub",
    [
        ("no_output", {"writes": None}),
        ("agent_failed", {"writes": None, "exit_ok": False}),
        ("empty_canonical", {"writes": {"canonical_topic_en": ""}}),
        ("not_an_object", {"writes": ["nope"]}),
    ],
)
def test_unusable_agent_output_degrades_instead_of_raising(
    tmp_path, emitted, settings, monkeypatch, kind, stub
):
    stub_leg(monkeypatch, **stub)
    facets = parse(CZECH_TOPIC, tmp_path, settings)

    assert facets["degraded"] is True, kind
    assert facets["degraded_reason"]
    assert facets["canonical_topic_en"] == CZECH_TOPIC
    assert emitted[-1][0] == "stage.finished"


def test_degraded_facets_are_not_cached(tmp_path, emitted, settings, monkeypatch):
    """A transient failure must not poison every later run of the topic."""
    stub_leg(monkeypatch, writes=None)
    parse(CZECH_TOPIC, tmp_path / "run1", settings)

    calls = stub_leg(monkeypatch, writes=AGENT_FACETS)
    retried = parse(CZECH_TOPIC, tmp_path / "run2", settings)

    assert len(calls) == 1
    assert retried["degraded"] is False


def test_missing_cli_degrades(tmp_path, emitted, settings, monkeypatch):
    async def exploding_stream(_req, _settings):
        raise FileNotFoundError("claude: not found")
        yield  # pragma: no cover - generator marker

    monkeypatch.setattr(pipeline, "stream_claude", exploding_stream)
    assert parse(CZECH_TOPIC, tmp_path, settings)["degraded"] is True


# ── Downstream ──────────────────────────────────────────────────────────────


def test_translated_facets_ground_a_topic_the_lexical_layer_cannot(
    tmp_path, emitted, settings, monkeypatch
):
    """Portuguese `Ormuz` reaches no whitelist entry on its own; the English
    facets are what make source_discover resolve it."""
    portuguese = "Estreito de Ormuz e o fornecimento de petroleo"
    stub_leg(
        monkeypatch,
        writes={
            "canonical_topic_en": "Strait of Hormuz crude oil supply",
            "input_language": "pt",
            "geo": ["Strait of Hormuz"],
            "commodity": ["crude oil"],
            "source_languages": ["pt", "ar"],
        },
    )
    facets = parse(portuguese, tmp_path, settings)
    asyncio.run(
        pipeline.run_source_discover(uuid.uuid4(), discovery_query(facets), tmp_path)
    )

    targets = json.loads((tmp_path / "source_targets.json").read_text(encoding="utf-8"))
    assert targets["entities"]


def test_source_discover_degrades_when_grounding_data_is_missing(
    tmp_path, emitted, monkeypatch
):
    """#36 shipped an image without the whitelist and failed every topic. The
    stage must warn and hand the plan agent an empty target list instead."""

    def explode(_query):
        raise FileNotFoundError("whitelist not found: /app/source_whitelist.json")

    monkeypatch.setattr(pipeline, "discover_sources_for_topic", explode)
    asyncio.run(pipeline.run_source_discover(uuid.uuid4(), "anything", tmp_path))

    targets = json.loads((tmp_path / "source_targets.json").read_text(encoding="utf-8"))
    assert targets["entities"] == []
    finished = emitted[-1][1]
    assert finished["entities"] == 0
    assert "whitelist not found" in finished["warning"]
