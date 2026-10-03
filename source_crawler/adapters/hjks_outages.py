"""JEPX HJKS — the generator outage register, reduced to nuclear units (#55).

HJKS (発電情報公開システム) is where every Japanese generator of 100 MW and above
must publish a planned stop, an unplanned stop or a derating, with the cause and
the expected return. For a nuclear fleet that is the whole operating picture:
periodic inspections booked into 2028, a trip and the day it is expected back, a
restart's test-run derating. No aggregator republishes it as a table, and the
utilities' own press pages say the same thing later and one plant at a time.

Why this is its own adapter rather than `static_file`
-----------------------------------------------------
There is no fixed file URL. The CSV is the response to a form POST that carries a
session cookie and a `_csrf` token from the page that rendered the form, so the
fetch is a GET then a POST on one client. The form's generation-type filter is
ignored when the CSV button is used (measured 2026-10-03: `format=1` returned all
58 788 rows, every type), so the filter is applied here instead — on the column,
not on the form.

Why the output is text, not the CSV
-----------------------------------
`source_crawler/extract.py` has no `.csv` converter, and the raw file is 11 MB of
CP932 across every fuel type. The nuclear rows are ~200 and ~25 kB, which is a
feed the analyst can read whole. The rows are written newest-update first, so if
the feed ever outgrows `MAX_CHARS_PER_FEED` the default head-first cut keeps the
recent changes — this is deliberately **not** tagged `chronological`.
"""

from __future__ import annotations

import csv
import io
import re
import ssl
from datetime import datetime

import certifi
import httpx

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

OUTAGES_URL = "https://hjks.jepx.or.jp/hjks/outages"
NUCLEAR = "原子力"
_CSRF_RE = re.compile(r'name="_csrf"\s+value="([^"]+)"')
_EXPECTED_HEADER = (
    "エリア", "発電事業者", "発電所コード", "発電所名", "発電形式", "ユニット名",
    "認可出力", "停止区分", "種別", "低下量", "停止日時", "復旧見通し", "復旧予定日",
    "停止原因", "最終更新日時",
)
# Empty form fields, as the page submits them; only `csv` and `_csrf` carry values.
_FORM_FIELDS = (
    "area", "company", "plantcd", "name", "format", "unitname",
    "maintemode", "assortment", "startdtfrom", "startdtto",
)
_TS_FMT = "%Y/%m/%d %H:%M"
_DATE_FMT = "%Y/%m/%d"

_LEGEND = """\
# JEPX HJKS — nuclear generating unit outages, Japan

Source: Japan Electric Power Exchange, 発電情報公開システム (HJKS), {url}
Every generator >= 100 MW must register planned stops, unplanned stops and deratings here.
Filtered to 発電形式 = 原子力 (nuclear). {count} entries; platform data as of {as_of} JST.

Column legend:
- 停止区分 (stop kind): 計画停止 = planned stop; 計画外停止 = UNPLANNED stop (trip / failure); 出力低下 = derating
- 種別 (type): 停止・定期検査等 = periodic inspection; 停止・設備故障 = equipment failure; 停止・長期計画停止 = long-term planned stop; 低下・その他 = derating, other (often a restart test run, 試運転)
- 復旧見通し (return outlook): あり = a return date is given; なし = no return date given
- capacity is the licensed output in MW; dates are JST
- a stop date in year 9998/9999 is the platform's placeholder for "not yet fixed", not a real date

"""


def _ts(value: str) -> datetime | None:
    try:
        return datetime.strptime(value.strip(), _TS_FMT)
    except ValueError:
        return None


def _date(value: str) -> datetime | None:
    try:
        return datetime.strptime(value.strip(), _DATE_FMT)
    except ValueError:
        return None


def _cell(value: str) -> str:
    """One line per row: the cause column carries its own newlines and tabs."""
    return re.sub(r"\s+", " ", value.replace("　", " ")).strip()


def _mw(kw: str) -> str:
    try:
        return f"{int(kw.replace(',', '')) / 1000:.0f}"
    except ValueError:
        return _cell(kw)


def parse_outages_csv(body: bytes) -> list[dict[str, str]]:
    """Decode HJKS's CP932 CSV into rows keyed by its own column names."""
    text = body.decode("cp932", errors="replace")
    reader = csv.reader(io.StringIO(text))
    header = tuple(next(reader, ()))
    if header[: len(_EXPECTED_HEADER)] != _EXPECTED_HEADER:
        raise ValueError(f"unexpected HJKS header: {header[:6]!r}")
    return [
        dict(zip(_EXPECTED_HEADER, row, strict=False))
        for row in reader
        if len(row) >= len(_EXPECTED_HEADER)
    ]


def _open_now(row: dict[str, str], as_of: datetime) -> bool:
    """Is this unit stopped or derated at `as_of`, by its own published dates?"""
    start = _ts(row["停止日時"])
    if start is None or start > as_of:
        return False
    back = _date(row["復旧予定日"])
    return back is None or back.date() >= as_of.date()


def _line(row: dict[str, str]) -> str:
    return " | ".join([
        _cell(row["発電所名"]),
        _cell(row["ユニット名"]),
        _mw(row["認可出力"]),
        _cell(row["停止区分"]),
        _cell(row["種別"]),
        _cell(row["停止日時"]),
        _cell(row["復旧見通し"]),
        _cell(row["復旧予定日"]),
        _cell(row["停止原因"]),
        _cell(row["最終更新日時"]),
        _cell(row["発電事業者"]),
    ])


_COLUMNS = (
    "plant | unit | MW | stop kind | type | stop from | return outlook | "
    "return date | cause | last updated | operator"
)


def nuclear_outages_text(body: bytes) -> str:
    """Render the nuclear rows of an HJKS outage CSV as a feed the analyst reads whole.

    "As of" is the newest update anywhere in the register, not the clock of the
    machine that fetched it: the text then changes only when the publisher's data
    does, which is what `feeds.publish` keys its freshness stamp on.
    """
    rows = parse_outages_csv(body)
    stamps = [t for t in (_ts(r["最終更新日時"]) for r in rows) if t is not None]
    if not stamps:
        raise ValueError("HJKS CSV carries no parseable update timestamps")
    as_of = max(stamps)
    nuclear = [r for r in rows if r["発電形式"].strip() == NUCLEAR]
    if not nuclear:
        raise ValueError("HJKS CSV carries no nuclear rows — filter or format changed")
    nuclear.sort(key=lambda r: (_ts(r["最終更新日時"]) or datetime.min), reverse=True)
    open_now = [r for r in nuclear if _open_now(r, as_of)]

    parts = [
        _LEGEND.format(url=OUTAGES_URL, count=len(nuclear), as_of=as_of.strftime(_TS_FMT)),
        f"## Open at {as_of.strftime(_TS_FMT)} — stop started, published return date not yet passed",
        "",
        _COLUMNS,
        *(_line(r) for r in open_now),
        "",
        "## All nuclear entries, newest update first",
        "",
        _COLUMNS,
        *(_line(r) for r in nuclear),
        "",
    ]
    return "\n".join(parts)


def _tls_context() -> ssl.SSLContext:
    """A context HJKS will finish a handshake with. Certificate checks stay on.

    The server speaks TLS 1.2 with SHA-1 CBC suites only (`ECDHE-RSA-AES128-SHA`,
    measured 2026-10-03) and answers OpenSSL 3's default security level with a
    handshake-failure alert — curl over LibreSSL connects, Python does not.
    Security level 0 re-admits the legacy suite; capping at 1.2 stops the client
    offering a 1.3 hello the server rejects. Scoped to this adapter alone.
    """
    ctx = ssl.create_default_context(cafile=certifi.where())
    ctx.set_ciphers("DEFAULT:@SECLEVEL=0")
    ctx.maximum_version = ssl.TLSVersion.TLSv1_2
    return ctx


def _download(url: str, *, timeout_sec: float = 120.0) -> bytes:
    with httpx.Client(
        timeout=httpx.Timeout(timeout_sec),
        verify=_tls_context(),
        headers={**DEFAULT_HEADERS, "Accept-Language": "ja,en;q=0.8"},
        follow_redirects=True,
    ) as client:
        page = client.get(url)
        if page.status_code >= 400:
            raise RuntimeError(f"HTTP {page.status_code} for {url}")
        match = _CSRF_RE.search(page.text)
        if not match:
            raise RuntimeError(f"no _csrf token on {url}")
        form = {name: "" for name in _FORM_FIELDS}
        form.update({"csv": "csv", "_csrf": match.group(1)})
        resp = client.post(url, data=form, headers={"Referer": url})
        if resp.status_code >= 400:
            raise RuntimeError(f"HTTP {resp.status_code} for CSV POST {url}")
        if "csv" not in resp.headers.get("content-type", "").lower():
            raise RuntimeError(
                f"expected text/csv from {url}, got {resp.headers.get('content-type')!r}"
            )
        return resp.content


@register
class HjksOutagesAdapter(SourceAdapter):
    """JEPX HJKS outage register → nuclear-only text feed (data feed, not RAG)."""

    name = "hjks_outages"

    def evaluate(self, target: SourceTarget) -> SourceAssessment:
        try:
            text = nuclear_outages_text(_download(target.url))
        except Exception as exc:
            return SourceAssessment(
                adapter=self.name, endpoint=target.url, viable=False, reason=str(exc)
            )
        return SourceAssessment(
            adapter=self.name,
            endpoint=target.url,
            viable=True,
            reason=f"nuclear outage feed ok ({len(text)} chars)",
            proposed_config=SourceConfig(
                source_id=target.source_id or "jepx_hjks_nuclear_outages",
                adapter=self.name,
                endpoint=target.url,
                extras={"pipeline": "data_feed"},
            ),
        )

    def discover(self, config: SourceConfig) -> list[DocRef]:
        return [DocRef(url=config.endpoint, title=config.title or config.source_id)]

    def fetch(self, ref: DocRef, config: SourceConfig) -> DownloadedDoc:
        text = nuclear_outages_text(_download(ref.url))
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
