"""Official data feeds reaching the analyst (#45).

The property that matters most is the negative one: a feed must not leak into a
topic it has nothing to do with. Handing every run every feed would look like
generosity and read like noise — and on a wide corpus the analyst would start
sourcing Indian gas tables for a Hormuz shipping question.
"""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime, timedelta
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


def test_a_feed_filed_by_iso_code_reaches_a_topic_that_names_the_country():
    """The facets the parse leg actually writes, from the India run of 2026-09-09.

    `INDIA_GAS` above carries both `IN` and `India`, which is what hid this: the
    seed files PPAC under `IN` and the parse leg emits `India` and nothing else,
    so the region axis never intersected and the feed was refused on a run whose
    commodity axis matched perfectly. `feeds.none_matched` (#51) is what made it
    visible — `geo=['india']` beside a feed region of `IN`.
    """
    live_facets = {
        "commodity": ["natural gas", "LNG", "domestic natural gas production", "fertilizers"],
        "geo": ["India"],
    }
    assert matches(PPAC_META, live_facets) is True


def test_resolving_the_country_spelling_does_not_widen_the_leak():
    """A synonym is two names for one place, not a licence to match a neighbour."""
    assert matches(PPAC_META, {"commodity": ["natural gas"], "geo": ["Pakistan"]}) is False
    assert matches(PPAC_META, {"commodity": ["natural gas"], "geo": ["asia pacific"]}) is False


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

    assert index["feed_count"] == 0
    assert index["feeds"] == []
    assert index["available"] == 1
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


# ---- freshness (#51) -------------------------------------------------------
#
# A feed is never withheld for being old. The alternative to a stale figure is
# usually no figure, and the analyst can qualify a number it knows the age of.
# What must not happen is a two-year-old balance quoted as the current state.

NOW = datetime(2026, 9, 8, 12, 0, tzinfo=UTC)


def _dated(days_ago: int) -> str:
    return (NOW - timedelta(days=days_ago)).isoformat()


def test_a_fresh_feed_is_not_marked_stale(tmp_path):
    state = tmp_path / "state"
    _write_feed(state, "ppac", {**PPAC_META, "collected_at": _dated(3)})

    index = export_feeds(str(state), tmp_path / "run" / "feeds", INDIA_GAS, now=NOW)

    assert index["feeds"][0]["age_days"] == 3
    assert index["feeds"][0]["stale"] is False
    assert index["stale_count"] == 0
    body = (tmp_path / "run" / "feeds" / "ppac.txt").read_text()
    assert "stale: false" in body
    assert "stale_note" not in body


def test_a_stale_feed_is_exported_and_marked_in_both_places(tmp_path):
    """Both places: the index a machine reads, and the file the analyst reads.
    A mark only in the index is a mark the model never sees."""
    state = tmp_path / "state"
    _write_feed(state, "ppac", {**PPAC_META, "collected_at": _dated(200)})

    index = export_feeds(str(state), tmp_path / "run" / "feeds", INDIA_GAS, now=NOW)

    assert index["feed_count"] == 1, "a stale feed is still the best number we have"
    assert index["feeds"][0]["stale"] is True
    assert index["feeds"][0]["age_days"] == 200
    assert index["stale_count"] == 1
    body = (tmp_path / "run" / "feeds" / "ppac.txt").read_text()
    assert "stale: true" in body
    assert "age_days: 200" in body
    assert "quote the figure with its period" in body
    assert "CGD | 1481" in body, "the numbers are still there to be read"


def test_the_threshold_is_the_configured_one(tmp_path):
    state = tmp_path / "state"
    _write_feed(state, "ppac", {**PPAC_META, "collected_at": _dated(50)})

    lenient = export_feeds(
        str(state), tmp_path / "lenient" / "feeds", INDIA_GAS, max_age_days=90, now=NOW
    )
    strict = export_feeds(
        str(state), tmp_path / "strict" / "feeds", INDIA_GAS, max_age_days=30, now=NOW
    )

    assert lenient["feeds"][0]["stale"] is False
    assert strict["feeds"][0]["stale"] is True


def test_a_feed_with_no_date_is_stale_rather_than_assumed_current(tmp_path):
    """The mtime fallback covers feeds published before the stamp existed; a
    sidecar whose date is unparseable leaves us unable to say, and "we cannot
    say how old this is" must not read as "this is current"."""
    state = tmp_path / "state"
    _write_feed(state, "ppac", {**PPAC_META, "collected_at": "not a date"})
    path = feeds_root(str(state)) / "ppac.txt"
    import os

    old = (NOW - timedelta(days=400)).timestamp()
    os.utime(path, (old, old))

    index = export_feeds(str(state), tmp_path / "run" / "feeds", INDIA_GAS, now=NOW)

    assert index["feeds"][0]["stale"] is True


def test_no_feed_matching_while_feeds_exist_names_the_facets(caplog):
    """"No feed applies" and "this topic has no facets" both produce zero feeds.
    Only the second is a bug, so the log has to separate them (#51 item 4)."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        state = Path(tmp) / "state"
        _write_feed(state, "ppac", PPAC_META)
        with caplog.at_level(logging.WARNING):
            export_feeds(str(state), Path(tmp) / "run" / "feeds", {"commodity": [], "geo": []})

    message = "\n".join(r.getMessage() for r in caplog.records)
    assert "feeds.none_matched" in message
    assert "available=1" in message
    assert "commodity=[]" in message and "geo=[]" in message


def test_a_matching_run_logs_no_warning(caplog):
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        state = Path(tmp) / "state"
        _write_feed(state, "ppac", PPAC_META)
        with caplog.at_level(logging.WARNING):
            export_feeds(str(state), Path(tmp) / "run" / "feeds", INDIA_GAS)

    assert "feeds.none_matched" not in "\n".join(r.getMessage() for r in caplog.records)


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


def test_publish_stamps_when_the_slot_received_the_feed(tmp_path):
    """`collected_at` is what `export_feeds` ages a feed against, so it has to
    exist before the export can say anything about freshness."""
    collected = tmp_path / "collected_text"
    d = collected / "ppac"
    d.mkdir(parents=True)
    (d / "ppac.txt").write_text("rows", encoding="utf-8")
    (d / "ppac.txt.meta.json").write_text(
        json.dumps({"source_id": "ppac", "tags": ["data_feed"], "source_sha256": "abc"}),
        encoding="utf-8",
    )

    publish(collected, str(tmp_path / "state"), now=NOW)

    meta = json.loads(
        (feeds_root(str(tmp_path / "state")) / "ppac.txt.meta.json").read_text(encoding="utf-8")
    )
    assert meta["collected_at"] == NOW.isoformat()


def test_republishing_unchanged_content_does_not_make_it_look_fresher(tmp_path):
    """The crawler re-downloads on its own cadence. A workbook that has not
    changed is not newer for having been fetched again — otherwise every crawl
    would silently reset the age of a series the publisher stopped updating."""
    collected = tmp_path / "collected_text"
    d = collected / "ppac"
    d.mkdir(parents=True)
    (d / "ppac.txt").write_text("rows", encoding="utf-8")
    (d / "ppac.txt.meta.json").write_text(
        json.dumps({"source_id": "ppac", "tags": ["data_feed"], "source_sha256": "abc"}),
        encoding="utf-8",
    )
    state = str(tmp_path / "state")
    publish(collected, state, now=NOW - timedelta(days=90))

    publish(collected, state, now=NOW)

    meta = json.loads(
        (feeds_root(state) / "ppac.txt.meta.json").read_text(encoding="utf-8")
    )
    assert meta["collected_at"] == (NOW - timedelta(days=90)).isoformat()


def test_new_content_gets_a_new_stamp(tmp_path):
    collected = tmp_path / "collected_text"
    d = collected / "ppac"
    d.mkdir(parents=True)
    (d / "ppac.txt").write_text("rows", encoding="utf-8")
    sidecar = d / "ppac.txt.meta.json"
    sidecar.write_text(
        json.dumps({"source_id": "ppac", "tags": ["data_feed"], "source_sha256": "abc"}),
        encoding="utf-8",
    )
    state = str(tmp_path / "state")
    publish(collected, state, now=NOW - timedelta(days=90))

    sidecar.write_text(
        json.dumps({"source_id": "ppac", "tags": ["data_feed"], "source_sha256": "def"}),
        encoding="utf-8",
    )
    publish(collected, state, now=NOW)

    meta = json.loads(
        (feeds_root(state) / "ppac.txt.meta.json").read_text(encoding="utf-8")
    )
    assert meta["collected_at"] == NOW.isoformat()
