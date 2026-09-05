"""Official data feeds reaching the analyst (#45).

The property that matters most is the negative one: a feed must not leak into a
topic it has nothing to do with. Handing every run every feed would look like
generosity and read like noise — and on a wide corpus the analyst would start
sourcing Indian gas tables for a Hormuz shipping question.
"""

from __future__ import annotations

import json
from pathlib import Path

from apps.claude_agent.topics.feeds import export_feeds, feeds_root, matches, publish

INDIA_GAS = {"commodity": ["natural gas"], "geo": ["IN", "India"]}
HORMUZ_CRUDE = {"commodity": ["crude oil"], "geo": ["Iran", "Strait of Hormuz"]}

PPAC_META = {
    "source_id": "ppac_gas_sectoral_consumption",
    "title": "PPAC — Natural Gas Sectoral Consumption (monthly)",
    "publisher": "Petroleum Planning & Analysis Cell (PPAC), Government of India",
    "url": "https://ppac.gov.in/natural-gas/sectoral-consumption",
    "commodity": "natural_gas",
    "region": "IN",
    "document_type": "official_data",
    "tags": ["ppac", "india", "data_feed"],
}


def _write_feed(state: Path, name: str, meta: dict, text: str = "Power | 624\nCGD | 1481\n") -> None:
    root = feeds_root(str(state))
    root.mkdir(parents=True, exist_ok=True)
    (root / f"{name}.txt").write_text(text, encoding="utf-8")
    (root / f"{name}.txt.meta.json").write_text(json.dumps(meta), encoding="utf-8")


# ---- selection -------------------------------------------------------------


def test_a_feed_reaches_the_topic_it_describes():
    assert matches(PPAC_META, INDIA_GAS) is True


def test_a_feed_does_not_leak_into_an_unrelated_topic():
    assert matches(PPAC_META, HORMUZ_CRUDE) is False


def test_the_wrong_commodity_in_the_right_country_is_still_wrong():
    """India crude and India gas are different balances. Region agreement alone
    would hand a crude topic the gas table and invite a confident wrong number."""
    india_crude = {"commodity": ["crude oil"], "geo": ["India"]}
    assert matches(PPAC_META, india_crude) is False


def test_the_right_commodity_in_the_wrong_country_is_still_wrong():
    assert matches(PPAC_META, {"commodity": ["natural gas"], "geo": ["Bangladesh"]}) is False


def test_a_global_feed_has_no_region_to_disagree_with():
    """JODI publishes world data. A missing axis cannot disqualify a feed —
    otherwise the only feeds that ever match are the country-scoped ones."""
    jodi = {"source_id": "jodi_gas_world", "commodity": "natural_gas", "tags": ["data_feed"]}
    assert matches(jodi, INDIA_GAS) is True
    assert matches(jodi, HORMUZ_CRUDE) is False


def test_a_topic_with_no_facets_gets_nothing():
    """Better an empty feeds dir than every feed. #38 can fail to produce facets,
    and the failure must not turn into "read everything"."""
    assert matches(PPAC_META, {}) is False
    assert matches(PPAC_META, {"commodity": [], "geo": []}) is False


def test_underscores_spaces_and_case_are_the_same_word():
    """A seed says `natural_gas`, facets say `Natural Gas`. Neither is wrong."""
    assert matches({"commodity": "natural_gas", "region": "in"}, INDIA_GAS) is True


# ---- export ----------------------------------------------------------------


def test_export_writes_the_matching_feed_with_its_provenance(tmp_path):
    state = tmp_path / "state"
    _write_feed(state, "ppac_gas_sectoral_consumption", PPAC_META)

    index = export_feeds(str(state), tmp_path / "run" / "feeds", INDIA_GAS)

    assert index["feed_count"] == 1
    assert index["available"] == 1
    body = (tmp_path / "run" / "feeds" / "ppac_gas_sectoral_consumption.txt").read_text()
    # The analyst cites the publisher and the URL, so both travel with the text
    # rather than living only in an index the model may not open.
    assert "publisher: Petroleum Planning" in body
    assert "https://ppac.gov.in/natural-gas/sectoral-consumption" in body
    assert "CGD | 1481" in body


def test_export_reports_what_it_skipped_rather_than_looking_empty(tmp_path):
    """`available` vs `feed_count` separates "no feed applies to this topic" from
    "no feeds are published at all" — the distinction #46 had to add to search."""
    state = tmp_path / "state"
    _write_feed(state, "ppac_gas_sectoral_consumption", PPAC_META)

    index = export_feeds(str(state), tmp_path / "run" / "feeds", HORMUZ_CRUDE)

    assert index == {"feed_count": 0, "feeds": [], "available": 1}
    assert not (tmp_path / "run" / "feeds" / "index.json").exists()


def test_a_missing_feeds_directory_is_not_an_error(tmp_path):
    """A slot that has never run the crawler must still deliver reports."""
    assert export_feeds(str(tmp_path / "nothing"), tmp_path / "run", INDIA_GAS)["feed_count"] == 0


def test_a_feed_without_a_sidecar_is_skipped_not_guessed_at(tmp_path):
    state = tmp_path / "state"
    feeds_root(str(state)).mkdir(parents=True)
    (feeds_root(str(state)) / "orphan.txt").write_text("numbers", encoding="utf-8")

    assert export_feeds(str(state), tmp_path / "run", INDIA_GAS)["feed_count"] == 0


def test_an_oversized_feed_is_truncated_rather_than_dropped(tmp_path, monkeypatch):
    from apps.claude_agent.topics import feeds as feeds_mod

    monkeypatch.setattr(feeds_mod, "MAX_CHARS_PER_FEED", 50)
    state = tmp_path / "state"
    _write_feed(state, "big", {**PPAC_META, "source_id": "big"}, text="x" * 500)

    index = export_feeds(str(state), tmp_path / "run" / "feeds", INDIA_GAS)

    assert index["feed_count"] == 1
    assert "[... truncated]" in (tmp_path / "run" / "feeds" / "big.txt").read_text()


# ---- publish ---------------------------------------------------------------


def test_publish_takes_series_and_leaves_the_big_reports_in_rag(tmp_path):
    """OPEC's MOMR is `official_data` too, and 300k characters of it already sit
    in RAG where a topic retrieves the paragraph it needs. Copying it here would
    hand every crude run the whole document twice over."""
    collected = tmp_path / "collected_text"
    for name, tags in (
        ("ppac_gas_sectoral_consumption", ["ppac", "data_feed"]),
        ("opec_momr", ["opec", "momr", "balance"]),
    ):
        d = collected / name
        d.mkdir(parents=True)
        (d / f"{name}.txt").write_text("rows", encoding="utf-8")
        (d / f"{name}.txt.meta.json").write_text(
            json.dumps({"source_id": name, "document_type": "official_data", "tags": tags}),
            encoding="utf-8",
        )

    published = publish(collected, str(tmp_path / "state"))

    assert published == ["ppac_gas_sectoral_consumption"]
    root = feeds_root(str(tmp_path / "state"))
    assert (root / "ppac_gas_sectoral_consumption.txt").is_file()
    assert (root / "ppac_gas_sectoral_consumption.txt.meta.json").is_file()
    assert not (root / "opec_momr.txt").exists()
