"""A stored monitoring plan must not go on asking for the month it was written in (#54).

`build_short_term_queries` bakes `latest YYYY-MM` into the query text, and nothing
rewrites the plan afterwards. The India plan was written 2026-09-09; on 2026-10-02 all
nineteen of its queries still said `latest 2026-09`, so every cycle was asking a search
engine for last month's news and then reporting what came back as current.

The re-stamp happens on the copy handed to the agent. These tests pin that, and pin that
an entry without a hint is left alone rather than "repaired".
"""

from apps.claude_agent.topics.refresh import (
    build_short_term_queries,
    restamp_recency_hints,
)


def test_the_hint_is_moved_to_the_current_month():
    [entry] = restamp_recency_hints(
        [{"query": "PPAC monthly gas report latest 2026-09"}], today_iso="2026-10-02"
    )
    assert entry["query"] == "PPAC monthly gas report latest 2026-10"


def test_an_entry_without_a_hint_is_untouched():
    plan = [{"query": "india gas sectoral consumption", "allowed_domains": ["ppac.gov.in"]}]
    assert restamp_recency_hints(plan, today_iso="2026-10-02") == plan


def test_the_stored_plan_is_not_mutated():
    """The plan belongs to the owner; `PATCH /monitor` is how it changes, not a refresh."""
    plan = [{"query": "cea plant load factor latest 2026-09"}]
    restamp_recency_hints(plan, today_iso="2026-10-02")
    assert plan[0]["query"] == "cea plant load factor latest 2026-09"


def test_everything_else_on_the_entry_survives_the_restamp():
    [entry] = restamp_recency_hints(
        [{
            "id": "st01",
            "query": "PNGRB city gas bidding round latest 2026-09",
            "language": "en",
            "priority": 1,
            "source": "parsed.queries",
            "allowed_domains": ["pngrb.gov.in"],
        }],
        today_iso="2026-10-02",
    )
    assert entry["allowed_domains"] == ["pngrb.gov.in"], "the domain filter is the point"
    assert (entry["id"], entry["priority"], entry["source"]) == ("st01", 1, "parsed.queries")


def test_a_plan_built_today_round_trips_unchanged():
    """A freshly written plan already carries this month, so the re-stamp is a no-op."""
    plan = build_short_term_queries(
        {"queries": [{"query": "india lng imports", "priority": 1}]},
        None,
        today_iso="2026-10-02",
    )
    assert restamp_recency_hints(plan, today_iso="2026-10-02") == plan
    assert plan[0]["query"].endswith("latest 2026-10")


def test_a_plan_written_in_september_is_restamped_in_october():
    """The India case, end to end through the real builder."""
    plan = build_short_term_queries(
        {"queries": [{"query": "india lng imports", "priority": 1}]},
        None,
        today_iso="2026-09-09",
    )
    assert plan[0]["query"].endswith("latest 2026-09")
    [entry] = restamp_recency_hints(plan, today_iso="2026-10-02")
    assert entry["query"].endswith("latest 2026-10")
