from __future__ import annotations

import json
from pathlib import Path

import pytest

from apps.claude_agent.sources.discover import (
    discover_sources,
    discover_sources_for_topic,
    filter_candidates_to_whitelist,
)
from apps.claude_agent.sources.playbooks import (
    MAX_TOPIC_PLAYBOOKS,
    parse_primary_official_sources,
    playbooks_for_topic,
)
from apps.claude_agent.sources.whitelist import (
    entities_named_in,
    entity_matches,
    load_whitelist,
    match_entries,
)

REPO = Path(__file__).resolve().parents[2]
WHITELIST = REPO / "source_whitelist.json"
PLAYBOOKS = REPO / "local_knowledge_sources" / "playbooks"


@pytest.fixture(scope="module")
def whitelist():
    return load_whitelist(WHITELIST)


def test_entity_matches_nioc_variants():
    assert entity_matches("NIOC", "NIOC")
    assert entity_matches("NIOC (via SHANA)", "NIOC")
    assert not entity_matches("NOAA", "NIOC")


def test_match_entries_nioc(whitelist):
    hits = match_entries(whitelist, "NIOC")
    domains = {h.domain for h in hits}
    assert "nioc.ir" in domains
    assert "shana.ir" in domains


def test_parse_iran_playbook_primary_sources():
    text = (PLAYBOOKS / "iran_oil_geopolitics.md").read_text(encoding="utf-8")
    rows = parse_primary_official_sources(text, "iran_oil_geopolitics.md")
    domains = {r.domain for r in rows}
    assert "nioc.ir" in domains
    assert "shana.ir" in domains


def test_discover_nioc_known_sources():
    result = discover_sources(
        "NIOC",
        whitelist_path=WHITELIST,
        playbooks_dir=PLAYBOOKS,
    )
    assert result["query"] == "NIOC"
    assert isinstance(result["known_sources"], list)
    assert result["known_sources"]
    domains = {s["domain"] for s in result["known_sources"]}
    assert "nioc.ir" in domains
    assert "shana.ir" in domains
    assert result["discovered_candidates"] == []
    assert "iran_oil_geopolitics.md" in result["playbook_refs"]

    entities = result["source_targets"]["entities"]
    assert entities
    assert all("known_domains" in e and "playbook_refs" in e for e in entities)
    all_domains = {d for e in entities for d in e["known_domains"]}
    assert all_domains <= domains


def test_discover_dedupes_by_domain():
    result = discover_sources(
        "NIOC",
        whitelist_path=WHITELIST,
        playbooks_dir=PLAYBOOKS,
    )
    domains = [s["domain"] for s in result["known_sources"]]
    assert len(domains) == len(set(domains))


def test_filter_candidates_keeps_only_whitelist():
    kept = filter_candidates_to_whitelist(
        [
            {"entity": "NIOC", "domain": "nioc.ir", "url": "https://nioc.ir/x"},
            {"entity": "Random", "domain": "evil.example", "url": "https://evil.example"},
        ],
        whitelist_path=WHITELIST,
    )
    assert len(kept) == 1
    assert kept[0]["domain"] == "nioc.ir"


def topic_result(topic: str):
    return discover_sources_for_topic(
        topic,
        whitelist_path=WHITELIST,
        playbooks_dir=PLAYBOOKS,
    )


def test_entities_named_in_topic_sentence(whitelist):
    hits = entities_named_in(whitelist, "NIOC crude exports under sanctions")
    assert "nioc.ir" in {h.domain for h in hits}
    assert not entities_named_in(whitelist, "crude exports rebound")


def test_topic_resolves_named_entity_playbook():
    result = topic_result("NIOC crude exports under sanctions")
    assert "iran_oil_geopolitics.md" in result["playbook_refs"]
    domains = {d for e in result["source_targets"]["entities"] for d in e["known_domains"]}
    assert "nioc.ir" in domains


def test_topic_ranks_distinctive_playbook_tokens_first():
    hits = playbooks_for_topic(PLAYBOOKS, "Strait of Hormuz tanker traffic disruption", set())
    assert [h.name for h in hits][0] == "strait_of_hormuz.md"
    assert len(hits) <= 2 * MAX_TOPIC_PLAYBOOKS


def test_topic_playbook_selection_is_bounded():
    result = topic_result("crude oil gas exports imports storage prices sanctions")
    assert len(result["playbook_refs"]) <= 2 * MAX_TOPIC_PLAYBOOKS


def test_topic_targets_are_whitelisted_and_deduped():
    result = topic_result("Saudi Aramco OSP changes for Asian buyers")
    entities = result["source_targets"]["entities"]
    domains = [d for e in entities for d in e["known_domains"]]
    known = {e.domain for e in load_whitelist(WHITELIST)}
    assert domains
    assert len(domains) == len(set(domains))
    assert set(domains) <= known


def test_topic_without_known_vocabulary_returns_no_targets():
    result = topic_result("zzzz qqqq wwww")
    assert result["source_targets"]["entities"] == []
    assert result["playbook_refs"] == []


def test_topic_requires_non_empty_string():
    with pytest.raises(ValueError):
        topic_result("   ")


def test_discover_json_roundtrip_cli_shape():
    result = discover_sources(
        "NIOC",
        whitelist_path=WHITELIST,
        playbooks_dir=PLAYBOOKS,
    )
    dumped = json.loads(json.dumps(result))
    assert "known_sources" in dumped
    assert "discovered_candidates" in dumped
