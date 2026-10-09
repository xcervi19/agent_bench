"""CEA Daily Coal Stock Report → coal stock feed (#56).

The fixture lines are copied from the 2026-10-08 report as `pypdf`'s layout mode
returns them: column-aligned with runs of spaces, a wrapped transport mode, a
row with no mode, a two-word GENCO, utility subtotals and the grand total.
"""

from __future__ import annotations

from datetime import date

import pytest

from source_crawler.adapters.cea_coal_stock import (
    coal_stock_text,
    parse_lines,
    report_url,
)


def _lines(as_on: str, *, panipat_stock: str = "31.8", panipat_flag: str = "*",
           grand_stock: str = "20618.9", grand_critical: str = "87") -> list[str]:
    return [
        "CENTRAL ELECTRICITY AUTHORITY",
        f"DAILY COAL STOCK REPORT       (AS ON {as_on})",
        "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
        "A. PLANT HAVING COAL LINKAGES, NO LINKAGES AND COAL BLOCK",
        f" 1     Haryana    HPGCL   RAIL   PANIPAT TPS    710   81%   21   10.3   216.0   "
        f"{panipat_stock}   0.0   {panipat_stock}   15%   {panipat_flag}   0.0   3.0   "
        "BCCL/CCL to ensure coal supply as per subgroup plan.",
        " 6     Punjab     PSPCL   RAIL   ROPAR TPS      840   38%   21   11.2   236.1   401.0   "
        "0.0   401.0   170%   4.0   6.0",
        "        PSPCL-Total        2300   66%   21   29.6   621.7   712.8   0.0   712.8   115%   0   21.0   25.4",
        "80 Tamil Nadu TANGEDCO RAIL-SEA- METTUR TPS 840 70% 21 11.4 239.4 60.1 10.2 70.3 29% 9.8 10.1",
        "82 Tamil Nadu TANGEDCO UDANGUDI TPP 1320 12% 21 17.9 375.0 0.0 20.0 20.0 5% * 0.0 2.2",
        "95 Uttar Pradesh NTPC JV RAIL MEJA STPP 1320 81% 21 17.5 367.5 64.1 0.0 64.1 17% * 9.1 16.0 "
        "NCL to ensure supply of coal as per subgroup plan.",
        "TOTAL A 206521 72% 19 2929.6 56857.1 17819.8 364.1 18183.7 31% 79 2535.3 2555.0",
        "B. PLANTS DESIGNED ON IMPORTED COAL",
        "176 Andhra Pradesh IPP Sea MEENAKSHI ENERGY LTD 1000 44% 21 14.2 297.3 37.7 0.1 37.8 12% * 12.1 11.7 "
        "Plant to build up stock through import",
        "TOTAL B 17774 72% 21 187.6 3939.1 130.5 2237.4 2367.9 60% 6 139.4 165.3",
        "C. NOT IN OPERATION",
        "185 Maharashtra IPP ROAD GEPL TPP Ph-I 120 0% 21 2.4 51.4 0.0 0.0 0.0 0% 0.0 0.0",
        f"Grand Total = A+B+C+D 225188 72% 20 3135.1 61172.9 18010.2 2608.9 {grand_stock} 33% "
        f"{grand_critical} 2682.1 2729.0",
        "https://npp.gov.in 09/10/2026 3.04 PM Page 13 of 13",
    ]


def test_parses_plants_sections_and_totals():
    report = parse_lines(_lines("08-10-2026"))
    assert report.as_on == date(2026, 10, 8)
    by_name = {p.name: p for p in report.plants}
    assert set(by_name) == {
        "PANIPAT TPS", "ROPAR TPS", "METTUR TPS", "UDANGUDI TPP", "MEJA STPP",
        "MEENAKSHI ENERGY LTD", "GEPL TPP Ph-I",
    }

    panipat = by_name["PANIPAT TPS"]
    assert (panipat.state, panipat.genco, panipat.mode) == ("Haryana", "HPGCL", "RAIL")
    assert panipat.stock_kt == 31.8 and panipat.pct_of_normative == 15
    assert panipat.critical and panipat.remark.startswith("BCCL/CCL")
    assert not by_name["ROPAR TPS"].critical

    # A mode that wrapped in its cell, a row without a mode, a two-word GENCO.
    assert by_name["METTUR TPS"].mode == "RAIL-SEA"
    assert (by_name["UDANGUDI TPP"].genco, by_name["UDANGUDI TPP"].mode) == ("TANGEDCO", "")
    assert (by_name["MEJA STPP"].state, by_name["MEJA STPP"].genco) == ("Uttar Pradesh", "NTPC JV")

    assert by_name["MEENAKSHI ENERGY LTD"].section == "B"
    assert by_name["GEPL TPP Ph-I"].section == "C"
    # Utility subtotals are not plants.
    assert all("Total" not in p.name for p in report.plants)

    grand = report.totals["Grand Total = A+B+C+D"]
    assert (grand.stock_kt, grand.critical_count, grand.pct_of_normative) == (20618.9, 87, 33)
    assert report.totals["TOTAL A"].critical_count == 79


def test_rejects_a_page_that_is_not_the_report():
    with pytest.raises(ValueError, match="AS ON"):
        parse_lines(["Something else entirely"])


def test_rejects_a_report_whose_layout_changed():
    lines = [line for line in _lines("08-10-2026") if not line.startswith("Grand Total")]
    with pytest.raises(ValueError, match="grand total"):
        parse_lines(lines)


def test_feed_carries_the_week_newest_first():
    latest = parse_lines(_lines("08-10-2026"))
    week_ago = parse_lines(_lines(
        "02-10-2026", panipat_stock="90.0", panipat_flag="", grand_stock="21050.0", grand_critical="88",
    ))
    text = coal_stock_text([week_ago, latest])

    trend = text.split("## Trend")[1].split("##")[0]
    assert trend.index("2026-10-08 | 20.62") < trend.index("2026-10-02 | 21.05")
    assert "PANIPAT TPS | Haryana | HPGCL | 710 | 90.0 | 31.8 | -58.2" in text
    assert "Newly critical since 2026-10-02: PANIPAT TPS (Haryana, 710 MW)" in text
    # Critical list is lowest stock first; the plant not in operation is not a draw.
    critical = text.split("## Critical plants")[1].split("## All plants")[0]
    assert critical.index("UDANGUDI TPP") < critical.index("MEENAKSHI ENERGY LTD") < critical.index("PANIPAT TPS")
    draws = text.split("## Largest stock draws")[1].split("Newly critical")[0]
    assert "GEPL" not in draws


def test_single_report_has_no_comparison_section():
    text = coal_stock_text([parse_lines(_lines("08-10-2026"))])
    assert "Largest stock draws" not in text
    assert "## Critical plants on 2026-10-08" in text


def test_report_url_is_the_dated_public_path():
    assert report_url(date(2026, 10, 8)) == (
        "https://npp.gov.in/public-reports/cea/daily/fuel/08-10-2026/dailyCoal1-2026-10-08.pdf"
    )
