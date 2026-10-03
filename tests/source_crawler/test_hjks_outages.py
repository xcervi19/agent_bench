"""HJKS outage CSV → nuclear-only feed (#55).

The fixture is built the way the platform serves it: CP932, its own Japanese
header, every fuel type mixed together, and a cause column with embedded newlines.
"""

from __future__ import annotations

import csv
import io

import pytest

from source_crawler.adapters.hjks_outages import (
    nuclear_outages_text,
    parse_outages_csv,
)

HEADER = [
    "エリア", "発電事業者", "発電所コード", "発電所名", "発電形式", "ユニット名",
    "認可出力", "停止区分", "種別", "低下量", "停止日時", "復旧見通し", "復旧予定日",
    "停止原因", "最終更新日時",
]


def _row(plant, unit, kind, typ, start, back, cause, updated, fuel="原子力", kw="1180000"):
    return ["関西", "関西電力株式会社", "1", plant, fuel, unit, kw, kind, typ, "",
            start, "あり" if back else "なし", back, cause, updated]


def _csv(rows) -> bytes:
    buf = io.StringIO()
    writer = csv.writer(buf, quoting=csv.QUOTE_ALL)
    writer.writerow(HEADER)
    writer.writerows(rows)
    return buf.getvalue().encode("cp932")


ROWS = [
    # Open: unplanned, no return date.
    _row("大飯発電所", "３号機", "計画外停止", "停止・設備故障", "2026/08/08 23:56", "",
         "発電機設備故障", "2026/10/02 16:42"),
    # Open: inspection with a return date still ahead.
    _row("高浜発電所", "３号機", "計画停止", "停止・定期検査等", "2026/04/07 11:00", "2026/11/10",
         "定期検査", "2026/01/08 10:39"),
    # Closed: return date passed.
    _row("美浜発電所", "３号機", "計画停止", "停止・定期検査等", "2026/06/16 10:00", "2026/09/15",
         "定期検査", "2026/09/15 20:41"),
    # Future: booked but not started.
    _row("高浜発電所", "４号機", "計画停止", "停止・定期検査等", "2026/11/14 11:00", "2027/07/10",
         "定期検査", "2026/08/27 17:24"),
    # Placeholder start date — never "open".
    _row("大飯発電所", "３号機", "出力低下", "低下・その他", "9998/12/25 17:00", "9999/02/22",
         "試運転\n最大低下量：1,180,000kW", "2026/10/02 16:41"),
    # Not nuclear, and the newest update in the register: sets "as of", is not listed.
    _row("柳井発電所", "２－２号", "出力低下", "低下・送電線等制約", "2026/10/05 00:00", "2026/10/05",
         "系統作業", "2026/10/03 20:57", fuel="火力（ガス）", kw="198000"),
]


def _sections(text: str) -> tuple[str, str]:
    open_part, _, all_part = text.partition("## All nuclear entries")
    return open_part, all_part


def test_only_nuclear_rows_are_kept():
    text = nuclear_outages_text(_csv(ROWS))
    assert "柳井" not in text
    assert "5 entries" in text


def test_as_of_is_the_registers_newest_update_not_the_fetch_clock():
    """So the text changes only when the publisher's data does."""
    assert "as of 2026/10/03 20:57 JST" in nuclear_outages_text(_csv(ROWS))


def test_open_section_holds_started_stops_whose_return_is_not_past():
    open_part, _ = _sections(nuclear_outages_text(_csv(ROWS)))
    assert "発電機設備故障" in open_part, "unplanned stop with no return date is open"
    assert "高浜発電所 | ３号機" in open_part, "inspection returning 11-10 is open"
    assert "美浜発電所" not in open_part, "returned 09-15"
    assert "高浜発電所 | ４号機" not in open_part, "starts 11-14"
    assert "9998/12/25" not in open_part, "placeholder dates are never open"


def test_all_entries_are_newest_update_first_one_line_each():
    _, all_part = _sections(nuclear_outages_text(_csv(ROWS)))
    lines = [ln for ln in all_part.splitlines() if " | " in ln and not ln.startswith("plant")]
    assert len(lines) == 5, "the embedded newline in a cause must not split a row"
    assert lines[0].endswith("2026/10/02 16:42 | 関西電力株式会社")
    assert "高浜発電所 | ３号機" in lines[-1]


def test_capacity_is_reported_in_megawatts():
    assert "| 1180 |" in nuclear_outages_text(_csv(ROWS))


def test_a_changed_header_fails_loudly():
    body = _csv(ROWS).replace("発電形式".encode("cp932"), "形式".encode("cp932"))
    with pytest.raises(ValueError, match="unexpected HJKS header"):
        parse_outages_csv(body)


def test_a_register_with_no_nuclear_rows_fails_rather_than_publishing_an_empty_feed():
    with pytest.raises(ValueError, match="no nuclear rows"):
        nuclear_outages_text(_csv(ROWS[-1:]))
