"""The adapter for sources whose file moves but whose page does not (#45).

The case it exists for: PPAC republishes India's gas balance every month under a
new timestamped filename, so a fixed endpoint goes stale and a `{month}/{year}`
template cannot guess the prefix. Only the tail of the name is stable.
"""

from __future__ import annotations

from unittest.mock import patch

import pytest

from source_crawler.adapters.landing_link import LandingLinkAdapter, _candidate_links
from source_crawler.models import SourceConfig, SourceTarget

XLSX = b"PK\x03\x04" + b"0" * 2048


class _Resp:
    def __init__(
        self,
        body: bytes = b"",
        status: int = 200,
        url: str = "https://ppac.gov.in/natural-gas/sectoral-consumption",
        content_type: str = "text/html",
        headers: dict | None = None,
    ):
        self.content = body
        self.status_code = status
        self.url = url
        self.headers = {"content-type": content_type, **(headers or {})}

    @property
    def text(self) -> str:
        return self.content.decode("utf-8", "replace")


# The real shape of the PPAC page: the link sits after attributes that contain
# spaces, which is what broke the first implementation.
PAGE = (
    b'<div style="visibility: visible;">'
    b'<a class="fz18 fw400 my-4 mb-auto" '
    b'href="https://ppac.gov.in/uploads/page-images/1787815916_4_NG-C-Sectoral-Consumption.xlsx" '
    b'target="_blank">Current</a>'
    b'<a class="x y" href="/uploads/page-images/1781859871_2_NG-H_Sectoral_Consumption.xlsx">Historical</a>'
    b"</div>"
)

CURRENT = "https://ppac.gov.in/uploads/page-images/1787815916_4_NG-C-Sectoral-Consumption.xlsx"

CONFIG = SourceConfig(
    source_id="ppac_gas_sectoral_consumption",
    adapter="landing_link",
    endpoint="https://ppac.gov.in/natural-gas/sectoral-consumption",
    title="PPAC sectoral consumption",
    extras={
        "link_pattern": r"NG-C[-_]Sectoral[-_]Consumption\.xlsx?$",
        "extension": ".xlsx",
    },
)


def test_a_link_after_multi_word_attributes_is_still_found():
    """Regression: quote-pairing drifts and eats the link.

    A regex that pairs quotes matches `class="fz18 fw400 …"` only as far as the
    first space, fails, then re-anchors so that the *opening* quote of the next
    attribute is consumed as a closing delimiter. The href that follows is then
    never offered as a candidate, and a page that plainly contains the file looks
    like it does not — the failure mode that would silently send a working source
    down the manual browser-fetch path.
    """
    links = _candidate_links(PAGE.decode(), CONFIG.endpoint, CONFIG.extras["link_pattern"])
    assert links == [CURRENT]


def test_relative_links_are_resolved_against_the_page():
    links = _candidate_links(PAGE.decode(), CONFIG.endpoint, r"NG-H[-_]Sectoral[-_]Consumption")
    assert links == [
        "https://ppac.gov.in/uploads/page-images/1781859871_2_NG-H_Sectoral_Consumption.xlsx"
    ]


def test_the_current_series_is_picked_over_the_archive():
    """`NG-C` is the live file, `NG-H` the history. Matching loosely would pin
    the topic to an archive that never moves again."""
    links = _candidate_links(PAGE.decode(), CONFIG.endpoint, CONFIG.extras["link_pattern"])
    assert all("NG-H" not in url for url in links)


def test_discover_then_fetch_returns_the_file():
    adapter = LandingLinkAdapter()
    with patch(
        "source_crawler.adapters.landing_link.http_get",
        side_effect=[
            _Resp(PAGE),
            _Resp(XLSX, url=CURRENT, content_type="application/vnd.ms-excel",
                  headers={"last-modified": "Thu, 27 Aug 2026 07:31:56 GMT"}),
        ],
    ):
        refs = adapter.discover(CONFIG)
        assert refs[0].url == CURRENT
        doc = adapter.fetch(refs[0], CONFIG)

    assert doc.body == XLSX
    assert doc.extension == ".xlsx"
    # Provenance a later reader needs: which page it came from, which file that
    # page pointed at on the day, and how fresh the publisher said it was.
    assert doc.meta["landing"] == CONFIG.endpoint
    assert doc.meta["resolved_url"] == CURRENT
    assert doc.meta["last_modified"] == "Thu, 27 Aug 2026 07:31:56 GMT"


def test_an_html_error_page_is_not_stored_as_the_dataset():
    """These sites answer "gone" with a 200 and a styled page. Storing that as
    the balance would put an error message where numbers are expected."""
    adapter = LandingLinkAdapter()
    with patch(
        "source_crawler.adapters.landing_link.http_get",
        side_effect=[_Resp(PAGE), _Resp(b"<!DOCTYPE html><html>404</html>" + b" " * 2048)],
    ):
        refs = adapter.discover(CONFIG)
        with pytest.raises(ValueError, match="HTML error page"):
            adapter.fetch(refs[0], CONFIG)


def test_a_script_generated_link_says_to_use_browser_fetch():
    """PPAC's `consumption` and `production` pages build their links in JS. The
    adapter must name the semi-automatic route rather than guess at a URL —
    defeating a scripted download is deliberately out of scope."""
    adapter = LandingLinkAdapter()
    with (
        patch(
            "source_crawler.adapters.landing_link.http_get",
            return_value=_Resp(b'<a onclick="dl(4)">Download</a>'),
        ),
        pytest.raises(RuntimeError, match="browser-fetch"),
    ):
        adapter.discover(CONFIG)


def test_a_missing_pattern_is_refused_rather_than_matching_everything():
    adapter = LandingLinkAdapter()
    bare = SourceConfig(source_id="x", adapter="landing_link", endpoint="https://e.com")
    with (
        patch("source_crawler.adapters.landing_link.http_get", return_value=_Resp(PAGE)),
        pytest.raises(RuntimeError, match="link_pattern"),
    ):
        adapter.discover(bare)


def test_evaluate_reports_a_viable_source_with_its_freshness():
    """`evaluate` answers what a register entry cannot: a domain that resolves is
    not the same as a source that hands over data."""
    adapter = LandingLinkAdapter()
    target = SourceTarget(
        url=CONFIG.endpoint,
        source_id="ppac_gas_sectoral_consumption",
        hints={"link_pattern": CONFIG.extras["link_pattern"], "title": "PPAC"},
    )
    with patch(
        "source_crawler.adapters.landing_link.http_get",
        side_effect=[
            _Resp(PAGE),
            _Resp(XLSX, url=CURRENT, headers={"last-modified": "Thu, 27 Aug 2026 07:31:56 GMT"}),
        ],
    ):
        assessment = adapter.evaluate(target)

    assert assessment.viable is True
    assert "27 Aug 2026" in assessment.reason
    assert assessment.proposed_config.source_id == "ppac_gas_sectoral_consumption"


def test_evaluate_records_a_block_instead_of_retrying_it():
    adapter = LandingLinkAdapter()
    target = SourceTarget(url=CONFIG.endpoint, hints={"link_pattern": "x"})
    with patch(
        "source_crawler.adapters.landing_link.http_get", return_value=_Resp(b"", status=403)
    ):
        assessment = adapter.evaluate(target)

    assert assessment.viable is False
    assert "403" in assessment.reason
