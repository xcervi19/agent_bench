"""The whitelist only reaches search if `allowed_domains` survives the plan.

`build_short_term_queries` rebuilds every monitoring entry from scratch, so any
field it does not explicitly carry is dropped. A dropped domain filter turns a
domain-filtered monitoring plan back into an open web search without any error —
the failure is silent, which is why it is pinned here.
"""

from apps.claude_agent.topics.refresh import build_short_term_queries


def _by_query(entries):
    return {e["query"].rsplit(" latest", 1)[0]: e for e in entries}


def test_allowed_domains_survives_from_parsed_queries():
    parsed = {
        "queries": [
            {"query": "india gas sectoral consumption", "priority": 1,
             "allowed_domains": ["ppac.gov.in", "pngrb.gov.in"]},
        ]
    }
    entry = _by_query(build_short_term_queries(parsed, None))["india gas sectoral consumption"]
    assert entry["allowed_domains"] == ["ppac.gov.in", "pngrb.gov.in"]


def test_allowed_domains_survives_from_report_next_queries():
    report = {"next_queries": [{"q": "cgd authorisations", "allowed_domains": ["pngrb.gov.in"]}]}
    entry = _by_query(build_short_term_queries({}, report))["cgd authorisations"]
    assert entry["allowed_domains"] == ["pngrb.gov.in"]


def test_domains_are_normalised_to_bare_hosts():
    """WebSearch matches on the host, so a scheme or www. prefix silently misses."""
    parsed = {"queries": [{"query": "q", "allowed_domains": ["WWW.PPAC.GOV.IN", " pngrb.gov.in "]}]}
    entry = _by_query(build_short_term_queries(parsed, None))["q"]
    assert entry["allowed_domains"] == ["ppac.gov.in", "pngrb.gov.in"]


def test_an_unfiltered_query_omits_the_field_rather_than_sending_an_empty_list():
    """Absent means "search the whole web"; [] would mean "allow nothing"."""
    parsed = {"queries": [{"query": "open web query", "priority": 1}]}
    entry = _by_query(build_short_term_queries(parsed, None))["open web query"]
    assert "allowed_domains" not in entry


def test_empty_and_blank_domain_lists_do_not_become_a_filter():
    parsed = {
        "queries": [
            {"query": "a", "allowed_domains": []},
            {"query": "b", "allowed_domains": ["", "   "]},
        ]
    }
    entries = _by_query(build_short_term_queries(parsed, None))
    assert "allowed_domains" not in entries["a"]
    assert "allowed_domains" not in entries["b"]


def test_trigger_term_fallback_entries_carry_no_filter():
    """Actor × trigger queries are invented here, so there is no origin to inherit."""
    parsed = {
        "entities": {"actors": [{"name": "GAIL"}]},
        "monitoring_plan": {"trigger_terms": ["tariff", "commissioning", "outage"]},
    }
    entries = build_short_term_queries(parsed, None)
    fallback = [e for e in entries if e["source"] == "monitoring_plan"]
    assert fallback
    assert all("allowed_domains" not in e for e in fallback)
