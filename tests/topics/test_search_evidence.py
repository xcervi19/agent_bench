import hashlib
import json
import uuid

import pytest

from apps.claude_agent.topics.search_evidence import (
    SearchCall,
    SearchEvidenceRecorder,
    parse_call,
    parse_hits,
    url_hash,
)

WEB_SEARCH_RESULT = (
    'Web search results for query: "Strait of Hormuz tanker traffic"\n\n'
    'Links: [{"title":"Tracking ship traffic","url":"https://www.nbcnews.com/data-graphics/x"},'
    '{"title":"Ship traffic chart","url":"https://www.statista.com/chart/35984/"}]'
)


def test_parse_hits_reads_every_link():
    hits = parse_hits(WEB_SEARCH_RESULT)
    assert [h["url"] for h in hits] == [
        "https://www.nbcnews.com/data-graphics/x",
        "https://www.statista.com/chart/35984/",
    ]


def test_parse_hits_reads_text_blocks():
    assert parse_hits([{"type": "text", "text": WEB_SEARCH_RESULT}]) == parse_hits(WEB_SEARCH_RESULT)


def test_parse_hits_returns_empty_when_search_errored():
    assert parse_hits("Search failed: rate limited") == []


def test_parse_hits_raises_on_malformed_links():
    with pytest.raises(json.JSONDecodeError):
        parse_hits("Links: [{not json")


def test_url_hash_matches_news_json_convention():
    url = "https://example.com/a"
    assert url_hash(url) == hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]


def test_parse_call_reads_the_domain_filter():
    call = parse_call(
        {
            "query": "india gas",
            "allowed_domains": ["ppac.gov.in", "pngrb.gov.in"],
            "blocked_domains": ["example.com"],
        }
    )
    assert call == SearchCall(
        query="india gas",
        allowed_domains=["ppac.gov.in", "pngrb.gov.in"],
        blocked_domains=["example.com"],
    )


def test_parse_call_keeps_no_filter_distinct_from_empty_filter():
    """None means the call carried no filter; [] means it allowed nothing."""
    assert parse_call({"query": "q"}).allowed_domains is None
    assert parse_call({"query": "q", "allowed_domains": []}).allowed_domains == []


@pytest.fixture
def captured(monkeypatch):
    calls = []

    async def fake_record(topic_id, run_id, call, hits):
        calls.append((run_id, call, [h["url"] for h in hits]))

    monkeypatch.setattr(
        "apps.claude_agent.topics.search_evidence.record_hits", fake_record
    )
    return calls


@pytest.mark.asyncio
async def test_recorder_pairs_query_with_its_result(captured):
    recorder = SearchEvidenceRecorder(uuid.uuid4(), "run-1")
    recorder.note_tool_use(
        {"type": "tool_use", "name": "WebSearch", "id": "t1", "input": {"query": "hormuz"}}
    )
    recorder.note_tool_use({"type": "tool_use", "name": "Bash", "id": "t2", "input": {}})
    await recorder.note_tool_result({"tool_use_id": "t2", "content": WEB_SEARCH_RESULT})
    await recorder.note_tool_result({"tool_use_id": "t1", "content": WEB_SEARCH_RESULT})

    assert captured == [
        (
            "run-1",
            SearchCall(query="hormuz"),
            [
                "https://www.nbcnews.com/data-graphics/x",
                "https://www.statista.com/chart/35984/",
            ],
        )
    ]


@pytest.mark.asyncio
async def test_recorder_carries_the_domain_filter_through(captured):
    recorder = SearchEvidenceRecorder(uuid.uuid4(), "run-1")
    recorder.note_tool_use(
        {
            "type": "tool_use",
            "name": "WebSearch",
            "id": "t1",
            "input": {"query": "india gas", "allowed_domains": ["ppac.gov.in"]},
        }
    )
    await recorder.note_tool_result({"tool_use_id": "t1", "content": WEB_SEARCH_RESULT})

    assert captured[0][1] == SearchCall(query="india gas", allowed_domains=["ppac.gov.in"])


@pytest.mark.asyncio
async def test_a_search_that_returned_nothing_is_still_recorded(captured):
    """The empty search is the observation the pre-#46 recorder threw away.

    "We asked and search returned nothing" and "nobody asked" need opposite
    fixes, so the empty call must reach the store.
    """
    recorder = SearchEvidenceRecorder(uuid.uuid4(), "run-1")
    recorder.note_tool_use(
        {
            "type": "tool_use",
            "name": "WebSearch",
            "id": "t1",
            "input": {"query": "site:shana.ir exports", "allowed_domains": ["shana.ir"]},
        }
    )
    await recorder.note_tool_result(
        {"tool_use_id": "t1", "content": "Search failed: no results"}
    )

    assert captured == [
        ("run-1", SearchCall(query="site:shana.ir exports", allowed_domains=["shana.ir"]), [])
    ]
