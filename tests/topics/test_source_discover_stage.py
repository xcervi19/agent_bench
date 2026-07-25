"""Offline test for the Python pre-plan source_discover stage (#36).

No DB and no network: `emit` is stubbed and discovery reads the repo whitelist
and playbook markdown directly.
"""

from __future__ import annotations

import asyncio
import json
import uuid

import pytest

from apps.claude_agent.topics import pipeline


@pytest.fixture
def emitted(monkeypatch):
    events: list[tuple[str, dict]] = []

    async def fake_emit(topic_id, event_type, payload):
        events.append((event_type, payload))
        return len(events)

    monkeypatch.setattr(pipeline, "emit", fake_emit)
    return events


TOPIC = "NIOC crude exports under sanctions"


def test_source_discover_writes_whitelisted_targets(tmp_path, emitted):
    asyncio.run(pipeline.run_source_discover(uuid.uuid4(), TOPIC, tmp_path))

    targets = json.loads((tmp_path / "source_targets.json").read_text(encoding="utf-8"))
    domains = {d for e in targets["entities"] for d in e["known_domains"]}
    assert "nioc.ir" in domains
    assert all("playbook_refs" in e and "signals" in e for e in targets["entities"])


def test_source_discover_emits_stage_events(tmp_path, emitted):
    asyncio.run(pipeline.run_source_discover(uuid.uuid4(), TOPIC, tmp_path))

    assert [name for name, _ in emitted] == ["stage.started", "stage.finished"]
    assert {p["stage"] for _, p in emitted} == {"source_discover"}
    assert emitted[-1][1]["entities"] > 0


def test_source_discover_rejects_empty_topic(tmp_path, emitted):
    with pytest.raises(ValueError):
        asyncio.run(pipeline.run_source_discover(uuid.uuid4(), "   ", tmp_path))

    assert not (tmp_path / "source_targets.json").exists()
