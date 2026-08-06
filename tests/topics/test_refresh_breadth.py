"""The query cap is the lever on corpus size, so it must actually be a lever.

Search returns roughly nine links per query and we read ~89% of them, which makes
the number of queries — not fetch success — what decides how much a refresh
collects. These tests pin that the cap is honoured and configurable.
"""

from apps.claude_agent.topics.refresh import build_short_term_queries

PARSED = {
    "queries": [{"query": f"parsed query {i}", "priority": 2} for i in range(60)],
    "entities": {"actors": [{"name": "Actor A"}, {"name": "Actor B"}]},
    "monitoring_plan": {"trigger_terms": ["closure", "seizure", "premium"]},
}
REPORT = {"next_queries": [{"q": f"report query {i}", "rationale": "r"} for i in range(30)]}


def test_the_cap_is_honoured():
    assert len(build_short_term_queries(PARSED, REPORT, max_queries=12)) == 12
    assert len(build_short_term_queries(PARSED, REPORT, max_queries=40)) == 40


def test_raising_the_cap_actually_yields_more_queries():
    """The regression that matters: a cap that is ignored above some hidden ceiling."""
    small = build_short_term_queries(PARSED, REPORT, max_queries=12)
    large = build_short_term_queries(PARSED, REPORT, max_queries=40)
    assert len(large) > len(small)
    assert len({q["query"] for q in large}) == len(large), "queries must stay unique"


def test_report_queries_scale_with_the_cap_rather_than_a_fixed_eight():
    large = build_short_term_queries(PARSED, REPORT, max_queries=40)
    from_report = [q for q in large if q["source"] == "report.next_queries"]
    assert len(from_report) > 8, "the next_queries slice must follow the cap"


def test_ids_stay_sequential_and_padded_past_nine():
    plan = build_short_term_queries(PARSED, REPORT, max_queries=40)
    assert [q["id"] for q in plan[:3]] == ["st01", "st02", "st03"]
    assert plan[-1]["id"] == f"st{len(plan):02d}"


def test_a_thin_topic_is_not_padded_to_the_cap():
    """A high cap must not invent queries a topic cannot support."""
    plan = build_short_term_queries({"queries": [{"query": "only one"}]}, None, max_queries=40)
    assert 0 < len(plan) < 40


def test_the_default_stays_conservative():
    """Callers that do not pass a cap keep the old bounded behaviour."""
    assert len(build_short_term_queries(PARSED, REPORT)) == 12
