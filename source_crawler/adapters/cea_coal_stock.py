"""CEA Daily Coal Stock Report — every coal-fired plant in India, every day (#56).

The Central Electricity Authority's Fuel Management Division publishes, for each
of ~190 coal-fired stations (~225 GW), the stock it holds against the stock it is
required to hold, the coal it received and burnt that day, and a remark naming
who is meant to fix a shortfall ("SECL/MCL to ensure coal supply as per subgroup
plan"). A plant below 25 % of its normative stock is flagged critical. That is the
Indian coal balance at the point where it becomes power, published by the
regulator a day after the fact. News reports "N plants critical" once a crisis is
under way; this report has the plant, the utility and the trend before that.

Why this is its own adapter rather than `static_pdf`
----------------------------------------------------
The landing page (`npp.gov.in/dailyCoalReports`) is a form: a date picker that
POSTs with a session and a `_csrf` token. The files behind it, though, sit at a
dated path that needs neither (measured 2026-10-09):

    /public-reports/cea/daily/fuel/08-10-2026/dailyCoal1-2026-10-08.pdf

so the adapter walks back from today to the newest file that exists, then keeps
going for a week. One report is a level; a week of them is a direction, and the
direction — stocks drawn down because receipts run below burn — is the trade.

Why the PDF and not the `.xls` next to it
-----------------------------------------
The `.xls` is legacy BIFF from JasperReports, and the crawler carries no reader
for it (`openpyxl` reads `.xlsx` only). `pypdf`'s layout mode keeps each plant on
one line with its columns in order, which a single regex reads whole: 191 of 191
plant rows on the 2026-10-08 report.
"""

from __future__ import annotations

import io
import re
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone

import httpx
from pypdf import PdfReader

from ..base import SourceAdapter
from ..models import (
    DocRef,
    DownloadedDoc,
    SourceAssessment,
    SourceConfig,
    SourceTarget,
)
from ..registry import register
from ._http import DEFAULT_HEADERS

LANDING_URL = "https://npp.gov.in/dailyCoalReports"
REPORT_URL = "https://npp.gov.in/public-reports/cea/daily/fuel/{dmy}/dailyCoal1-{ymd}.pdf"
IST = timezone(timedelta(hours=5, minutes=30))

# How far back to look for the newest report (weekends and holidays included),
# and how many reports make the trend.
LOOKBACK_DAYS = 10
HISTORY_REPORTS = 7

_AS_ON_RE = re.compile(r"AS ON (\d{2}-\d{2}-\d{4})")
# The numeric tail every plant row and every total row shares, columns 6-17.
_NUMS = (
    r"(\d+) (\d+)% (?:(\d+) )?([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+) (\d+)%"
)
_PLANT_RE = re.compile(r"^(\d+) (.+?) " + _NUMS + r"( \*)? ([\d.]+) ([\d.]+)(?: (.*))?$")
_TOTAL_RE = re.compile(r"^(.+?) " + _NUMS + r" (\d+) ([\d.]+) ([\d.]+)$")
_SECTION_RE = re.compile(r"^([A-D])\.? (PLANT|PLANTS|NOT IN OPERATION)")
_MODE_PARTS = {"RAIL", "ROAD", "PITHEAD", "SEA", "BELT", "MGR", "CONVEYOR"}
_SECTIONS = {
    "A": "domestic coal",
    "B": "designed on imported coal",
    "C": "not in operation",
    "D": "washery rejects",
}
# Totals worth carrying into the feed, by the label CEA prints.
_KEY_TOTALS = (
    "Grand Total = A+B+C+D",
    "TOTAL A",
    "TOTAL B",
    "State Gencos -Total",
    "Central Gencos -Total",
    "TOTAL NTPC & NTPC JV",
)


@dataclass(frozen=True)
class Plant:
    section: str
    state: str
    genco: str
    mode: str
    name: str
    capacity_mw: int
    plf_pct: int
    normative_days: int
    daily_req_kt: float
    normative_kt: float
    domestic_kt: float
    imported_kt: float
    stock_kt: float
    pct_of_normative: int
    critical: bool
    receipt_kt: float
    consumption_kt: float
    remark: str

    @property
    def days_of_burn(self) -> float | None:
        """Stock over the day's actual burn: how long the pile lasts at today's rate."""
        return self.stock_kt / self.consumption_kt if self.consumption_kt > 0 else None


@dataclass(frozen=True)
class Total:
    label: str
    capacity_mw: int
    stock_kt: float
    normative_kt: float
    pct_of_normative: int
    critical_count: int
    receipt_kt: float
    consumption_kt: float


@dataclass
class Report:
    as_on: date
    url: str
    plants: list[Plant] = field(default_factory=list)
    totals: dict[str, Total] = field(default_factory=dict)


def _split_prefix(prefix: str) -> tuple[str, str, str, str]:
    """`Uttar Pradesh IPP RAIL ROSA TPP Ph-I` → state, genco, mode, station name.

    The mode of transport is the anchor: a token made only of RAIL/ROAD/SEA/...
    joined by hyphens. GENCO is the token before it, the state everything before
    that, the station everything after.
    """
    tokens = prefix.split()
    for i, tok in enumerate(tokens):
        # A long mode wraps in its cell and arrives cut: `RAIL-SEA-` (…ROAD below).
        parts = {part for part in tok.upper().split("-") if part}
        if i >= 2 and parts and parts <= _MODE_PARTS:
            mode = tok.upper().rstrip("-")
            # A two-word GENCO (`NTPC JV`): capitals before it are GENCO, not state.
            start = i - 1
            while start > 1 and tokens[start - 1].isupper():
                start -= 1
            return (" ".join(tokens[:start]), " ".join(tokens[start:i]), mode,
                    " ".join(tokens[i + 1 :]))
    # Some rows leave the mode blank. States print in title case and GENCOs in
    # capitals, so the first all-capitals token ends the state.
    for i, tok in enumerate(tokens):
        if i >= 1 and tok.isupper():
            return " ".join(tokens[:i]), tok, "", " ".join(tokens[i + 1 :])
    raise ValueError(f"cannot split plant row prefix: {prefix!r}")


def parse_report(pdf: bytes, *, url: str = "") -> Report:
    """Read one Daily Coal Stock Report PDF into plants and totals."""
    reader = PdfReader(io.BytesIO(pdf))
    return parse_lines(
        [
            line
            for page in reader.pages
            for line in page.extract_text(extraction_mode="layout").splitlines()
        ],
        url=url,
    )


def parse_lines(raw_lines: list[str], *, url: str = "") -> Report:
    """Parse the report's text, one layout line per element, into plants and totals."""
    lines = [" ".join(line.split()) for line in raw_lines]
    lines = [line for line in lines if line]
    as_on = next((m.group(1) for m in map(_AS_ON_RE.search, lines) if m), None)
    if as_on is None:
        raise ValueError("no 'AS ON dd-mm-yyyy' header — not a CEA daily coal stock report")
    report = Report(as_on=datetime.strptime(as_on, "%d-%m-%Y").date(), url=url)

    section = "A"
    for line in lines:
        if m := _SECTION_RE.match(line):
            section = m.group(1)
            continue
        if m := _PLANT_RE.match(line):
            state, genco, mode, name = _split_prefix(m.group(2))
            report.plants.append(Plant(
                section=section, state=state, genco=genco, mode=mode, name=name,
                capacity_mw=int(m.group(3)), plf_pct=int(m.group(4)),
                normative_days=int(m.group(5) or 0), daily_req_kt=float(m.group(6)),
                normative_kt=float(m.group(7)), domestic_kt=float(m.group(8)),
                imported_kt=float(m.group(9)), stock_kt=float(m.group(10)),
                pct_of_normative=int(m.group(11)), critical=bool(m.group(12)),
                receipt_kt=float(m.group(13)), consumption_kt=float(m.group(14)),
                remark=(m.group(15) or "").strip(),
            ))
            continue
        if (m := _TOTAL_RE.match(line)) and m.group(1) in _KEY_TOTALS:
            report.totals[m.group(1)] = Total(
                label=m.group(1), capacity_mw=int(m.group(2)),
                normative_kt=float(m.group(6)), stock_kt=float(m.group(9)),
                pct_of_normative=int(m.group(10)), critical_count=int(m.group(11)),
                receipt_kt=float(m.group(12)), consumption_kt=float(m.group(13)),
            )
    if not report.plants:
        raise ValueError(f"no plant rows parsed from the {as_on} report — layout changed")
    if "Grand Total = A+B+C+D" not in report.totals:
        raise ValueError(f"no grand total in the {as_on} report — layout changed")
    return report


def _mt(kt: float) -> str:
    return f"{kt / 1000:.2f}"


def _plant_line(p: Plant) -> str:
    days = p.days_of_burn
    return " | ".join([
        p.name, p.state, p.genco, p.mode, str(p.capacity_mw), f"{p.plf_pct}%",
        f"{p.stock_kt:.1f}", f"{p.pct_of_normative}%", f"{days:.1f}" if days is not None else "-",
        f"{p.receipt_kt:.1f}", f"{p.consumption_kt:.1f}", "CRITICAL" if p.critical else "",
        p.remark,
    ])


_PLANT_COLUMNS = (
    "station | state | genco | transport | MW | PLF this month | stock kt | % of normative | "
    "days at today's burn | receipt kt | burn kt | flag | CEA remark"
)

_LEGEND = """\
# CEA Daily Coal Stock Report — coal-fired power stations, India

Source: Central Electricity Authority, Fuel Management Division, published on the National
Power Portal, {landing}. Latest report: AS ON {as_on} ({url}).
Units: kt = thousand tonnes, Mt = million tonnes. "Normative stock" is the stock a plant is
required to hold (days of requirement at 85 % PLF; fewer days for pithead plants). CEA flags a
plant CRITICAL when its stock is below 25 % of normative. "Days at today's burn" is stock divided
by the day's actual consumption — computed here, not printed by CEA.
Sections: A = plants on domestic coal (linkage / captive block), B = designed on imported coal,
C = not in operation, D = washery rejects.

"""


def coal_stock_text(reports: list[Report]) -> str:
    """Render a week of reports as one feed, newest first; the newest carries the detail."""
    if not reports:
        raise ValueError("no CEA daily coal stock reports to render")
    reports = sorted(reports, key=lambda r: r.as_on, reverse=True)
    latest, oldest = reports[0], reports[-1]
    parts = [_LEGEND.format(landing=LANDING_URL, as_on=latest.as_on.strftime("%d-%m-%Y"), url=latest.url)]

    parts += [
        "## Trend — all plants (grand total A+B+C+D), newest first",
        "",
        "report date | stock Mt | % of normative | plants critical | receipt kt | burn kt | receipt - burn kt",
    ]
    for r in reports:
        g = r.totals["Grand Total = A+B+C+D"]
        parts.append(" | ".join([
            r.as_on.isoformat(), _mt(g.stock_kt), f"{g.pct_of_normative}%", str(g.critical_count),
            f"{g.receipt_kt:.1f}", f"{g.consumption_kt:.1f}", f"{g.receipt_kt - g.consumption_kt:+.1f}",
        ]))

    parts += [
        "",
        f"## Totals on {latest.as_on.isoformat()}",
        "",
        "group | MW | stock Mt | normative Mt | % of normative | plants critical | receipt kt | burn kt",
    ]
    for label in _KEY_TOTALS:
        if t := latest.totals.get(label):
            parts.append(" | ".join([
                label, str(t.capacity_mw), _mt(t.stock_kt), _mt(t.normative_kt),
                f"{t.pct_of_normative}%", str(t.critical_count), f"{t.receipt_kt:.1f}", f"{t.consumption_kt:.1f}",
            ]))

    if oldest is not latest:
        before = {(p.name, p.genco): p for p in oldest.plants}
        moves = [
            (p, p.stock_kt - before[(p.name, p.genco)].stock_kt)
            for p in latest.plants
            if (p.name, p.genco) in before and p.section != "C"
        ]
        moves.sort(key=lambda pm: pm[1])
        parts += [
            "",
            f"## Largest stock draws, {oldest.as_on.isoformat()} → {latest.as_on.isoformat()}",
            "",
            "station | state | genco | MW | stock kt then | stock kt now | change kt | % of normative now | flag",
        ]
        for p, delta in moves[:15]:
            parts.append(" | ".join([
                p.name, p.state, p.genco, str(p.capacity_mw),
                f"{before[(p.name, p.genco)].stock_kt:.1f}", f"{p.stock_kt:.1f}", f"{delta:+.1f}",
                f"{p.pct_of_normative}%", "CRITICAL" if p.critical else "",
            ]))
        newly = [
            p for p in latest.plants
            if p.critical and (p.name, p.genco) in before and not before[(p.name, p.genco)].critical
        ]
        parts += ["", f"Newly critical since {oldest.as_on.isoformat()}: "
                  + (", ".join(f"{p.name} ({p.state}, {p.capacity_mw} MW)" for p in newly) or "none")]

    critical = sorted((p for p in latest.plants if p.critical), key=lambda p: p.pct_of_normative)
    parts += [
        "",
        f"## Critical plants on {latest.as_on.isoformat()} — lowest stock first ({len(critical)})",
        "",
        _PLANT_COLUMNS,
        *(_plant_line(p) for p in critical),
    ]
    for section, title in _SECTIONS.items():
        rows = [p for p in latest.plants if p.section == section]
        if rows:
            parts += ["", f"## All plants, section {section} ({title}), {latest.as_on.isoformat()}", "",
                      _PLANT_COLUMNS, *(_plant_line(p) for p in rows)]
    parts.append("")
    return "\n".join(parts)


def report_url(day: date) -> str:
    return REPORT_URL.format(dmy=day.strftime("%d-%m-%Y"), ymd=day.isoformat())


def _fetch_reports(
    *, today: date | None = None, timeout_sec: float = 90.0
) -> list[Report]:
    """The newest report and the ones before it, up to `HISTORY_REPORTS`.

    A day with no file (weekend, holiday, not yet posted) is simply skipped; a
    file that exists but does not parse is an error, because that means the
    layout changed and a silent gap would hide it.
    """
    today = today or datetime.now(IST).date()
    reports: list[Report] = []
    with httpx.Client(
        timeout=httpx.Timeout(timeout_sec), headers=DEFAULT_HEADERS, follow_redirects=True
    ) as client:
        for back in range(LOOKBACK_DAYS + HISTORY_REPORTS * 2):
            if len(reports) >= HISTORY_REPORTS:
                break
            if not reports and back > LOOKBACK_DAYS:
                break
            url = report_url(today - timedelta(days=back))
            resp = client.get(url)
            if resp.status_code == 404 or "pdf" not in resp.headers.get("content-type", "").lower():
                continue
            if resp.status_code >= 400:
                raise RuntimeError(f"HTTP {resp.status_code} for {url}")
            reports.append(parse_report(resp.content, url=url))
    if not reports:
        raise RuntimeError(f"no CEA daily coal stock report in the last {LOOKBACK_DAYS} days")
    return reports


@register
class CeaCoalStockAdapter(SourceAdapter):
    """CEA Daily Coal Stock Report (a week of it) → text feed (data feed, not RAG)."""

    name = "cea_coal_stock"

    def evaluate(self, target: SourceTarget) -> SourceAssessment:
        try:
            text = coal_stock_text(_fetch_reports())
        except Exception as exc:
            return SourceAssessment(
                adapter=self.name, endpoint=target.url, viable=False, reason=str(exc)
            )
        return SourceAssessment(
            adapter=self.name,
            endpoint=target.url,
            viable=True,
            reason=f"coal stock feed ok ({len(text)} chars)",
            proposed_config=SourceConfig(
                source_id=target.source_id or "cea_daily_coal_stock",
                adapter=self.name,
                endpoint=target.url,
                extras={"pipeline": "data_feed"},
            ),
        )

    def discover(self, config: SourceConfig) -> list[DocRef]:
        return [DocRef(url=config.endpoint, title=config.title or config.source_id)]

    def fetch(self, ref: DocRef, config: SourceConfig) -> DownloadedDoc:
        text = coal_stock_text(_fetch_reports())
        return DownloadedDoc(
            ref=ref,
            body=text.encode("utf-8"),
            content_type="text/plain; charset=utf-8",
            extension=".txt",
            meta={
                "source_id": config.source_id,
                "title": config.title or config.source_id,
                "url": ref.url,
                "publisher": config.publisher,
                "tier": config.tier,
                "domain": config.domain,
                "commodity": config.commodity,
                "region": config.region,
                "tags": list(config.tags),
                "pipeline": "data_feed",
            },
        )
