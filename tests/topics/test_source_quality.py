from __future__ import annotations

import json

import pytest

from apps.claude_agent.topics.source_quality import (
    SourceMix,
    host_of,
    is_authoritative,
    is_whitelisted,
    read_sources,
    summarize,
    summarize_run,
)

DOMAINS = frozenset({"ukmto.org", "aramco.com", "shana.ir"})


def source(**over) -> dict[str, object]:
    return {"id": "s01", "url": "https://example.com/a", "source_class": "specialist_outlet", **over}


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://www.ukmto.org/advisory", True),
        ("https://ukmto.org/advisory", True),
        ("https://news.aramco.com/x", True),
        ("https://example.com/ukmto.org", False),
        ("https://notukmto.org/x", False),
        ("https://ukmto.org.evil.com/x", False),
        ("", False),
        ("not a url", False),
    ],
)
def test_is_whitelisted(url, expected):
    assert is_whitelisted(url, DOMAINS) is expected


def test_host_of_lowercases():
    assert host_of("https://WWW.UKMTO.ORG/x") == "www.ukmto.org"


def test_primary_official_is_authoritative_off_whitelist():
    assert is_authoritative(source(source_class="primary_official"), DOMAINS)


def test_data_feed_is_authoritative():
    assert is_authoritative(source(source_class="data_feed"), DOMAINS)


def test_whitelisted_domain_is_authoritative_despite_class():
    row = source(url="https://www.ukmto.org/a", source_class="specialist_outlet")
    assert is_authoritative(row, DOMAINS)


def test_outlet_off_whitelist_is_not_authoritative():
    assert not is_authoritative(source(), DOMAINS)


def test_summarize_counts_both_dimensions():
    mix = summarize(
        [
            source(source_class="primary_official", url="https://ukmto.org/a"),
            source(source_class="primary_official", url="https://iea.org/a"),
            source(source_class="specialist_outlet", url="https://aramco.com/a"),
            source(source_class="specialist_outlet", url="https://cnbc.com/a"),
        ],
        DOMAINS,
    )
    assert mix == SourceMix(total=4, authoritative=3, whitelisted=2)
    assert mix.authoritative_ratio == 0.75
    assert not mix.is_entirely_secondary


def test_entirely_secondary_is_flagged():
    mix = summarize([source(), source(url="https://aljazeera.com/a")], DOMAINS)
    assert mix == SourceMix(total=2, authoritative=0, whitelisted=0)
    assert mix.is_entirely_secondary


def test_empty_run_is_not_flagged_as_secondary():
    mix = summarize([], DOMAINS)
    assert mix.authoritative_ratio == 0.0
    assert not mix.is_entirely_secondary


def test_payload_shape():
    payload = summarize([source(source_class="primary_official")], DOMAINS).as_payload()
    assert payload == {
        "total": 1,
        "authoritative": 1,
        "whitelisted": 0,
        "authoritative_ratio": 1.0,
        "entirely_secondary": False,
    }


def test_read_sources_skips_non_objects(tmp_path):
    path = tmp_path / "news.json"
    path.write_text(json.dumps({"sources": [source(), "junk", None]}), encoding="utf-8")
    assert len(read_sources(path)) == 1


def test_read_sources_tolerates_missing_file(tmp_path):
    assert read_sources(tmp_path / "absent.json") == []


def test_read_sources_tolerates_malformed_json(tmp_path):
    path = tmp_path / "news.json"
    path.write_text("{not json", encoding="utf-8")
    assert read_sources(path) == []


def test_summarize_run_reads_the_runs_news_file(tmp_path):
    (tmp_path / "news.json").write_text(
        json.dumps({"sources": [source(url="https://ukmto.org/a")]}), encoding="utf-8"
    )
    assert summarize_run(tmp_path, DOMAINS) == SourceMix(total=1, authoritative=1, whitelisted=1)


def test_summarize_run_on_failed_cycle_is_empty(tmp_path):
    assert summarize_run(tmp_path, DOMAINS) == SourceMix(total=0, authoritative=0, whitelisted=0)


def test_matches_the_observed_prod_refresh():
    observed = [
        source(url="https://www.alhadath.net/a"),
        source(url="https://www.france24.com/ar/a"),
        source(url="https://sputnikarabic.ae/a"),
        source(url="https://www.bloomberg.com/a"),
        source(url="https://www.aljazeera.com/a"),
        source(url="https://www.cnbc.com/a"),
        source(url="https://www.aljazeera.com/b"),
        source(url="https://www.scmp.com/a"),
    ]
    mix = summarize(observed, DOMAINS)
    assert mix.is_entirely_secondary
    assert mix.authoritative == 0
