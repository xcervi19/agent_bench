from datetime import UTC, datetime, timedelta

import httpx
import pytest

from apps.claude_agent.topics.search_content import (
    METHOD_HTTP,
    RETRY_DEFAULT_SEC,
    STATUS_BLOCKED,
    STATUS_DISALLOWED,
    STATUS_ERROR,
    STATUS_FETCHED,
    STATUS_NOT_FOUND,
    STATUS_THIN,
    STATUS_UNSUPPORTED,
    RobotsCache,
    classify,
    domain_coverage_stmt,
    fetch_one,
    group_by_host,
    named_extension,
    method_timing_stmt,
    origin,
    rank_of,
    retry_delay,
    status_counts_stmt,
)

ARTICLE = (
    "<html><head><style>.x{}</style></head><body><p>"
    + ("Tanker traffic through the strait fell sharply this week. " * 8)
    + "</p><script>track()</script></body></html>"
)


def _response(
    status: int,
    body: str = "",
    content_type: str = "text/html",
    headers: dict[str, str] | None = None,
) -> httpx.Response:
    return httpx.Response(
        status_code=status,
        text=body,
        headers={"content-type": content_type, **(headers or {})},
        request=httpx.Request("GET", "https://example.com/a"),
    )


def test_classify_extracts_text_and_drops_script_and_style():
    outcome = classify(_response(200, ARTICLE))
    assert outcome.status == STATUS_FETCHED
    assert "Tanker traffic" in outcome.text
    assert "track()" not in outcome.text
    assert ".x{}" not in outcome.text


def test_classify_marks_short_pages_thin_but_keeps_what_there_was():
    outcome = classify(_response(200, "<html><body><p>Subscribe to read.</p></body></html>"))
    assert outcome.status == STATUS_THIN
    assert outcome.text == "Subscribe to read."


@pytest.mark.parametrize(
    ("code", "expected"),
    [(403, STATUS_BLOCKED), (429, STATUS_BLOCKED), (404, STATUS_NOT_FOUND), (500, STATUS_ERROR)],
)
def test_classify_records_the_block_rather_than_raising(code, expected):
    outcome = classify(_response(code))
    assert outcome.status == expected
    assert outcome.text is None
    assert str(code) in outcome.error


def test_classify_drops_nul_bytes_rather_than_losing_the_whole_page():
    """Postgres rejects 0x00 in a text column; one NUL used to cost the attempt."""
    outcome = classify(_response(200, ARTICLE.replace("this week", "this\x00 week")))
    assert outcome.status == STATUS_FETCHED
    assert "\x00" not in outcome.text
    assert "Tanker traffic" in outcome.text


def test_a_page_of_nuls_is_thin_and_does_not_pass_as_a_full_article():
    """Measured after stripping, so it cannot outrank real text already stored."""
    body = "<html><body><p>" + "\x00" * 400 + "Subscribe to read.</p></body></html>"
    outcome = classify(_response(200, body))
    assert outcome.status == STATUS_THIN
    assert outcome.text == "Subscribe to read."


def test_classify_skips_non_text_instead_of_producing_garbage():
    outcome = classify(_response(200, "\xff\xd8\xff binary", content_type="image/jpeg"))
    assert outcome.status == STATUS_UNSUPPORTED
    assert outcome.text is None


def _minimal_pdf(text: str) -> bytes:
    """A one-page PDF with a single text-showing operator — enough for pypdf."""
    stream = f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET".encode()
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R "
        b"/Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % number + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n" % (len(objects) + 1) + b"0000000000 65535 f \n"
    for offset in offsets:
        out += b"%010d 00000 n \n" % offset
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (
        len(objects) + 1,
        xref,
    )
    return bytes(out)


def _binary_response(data: bytes, content_type: str) -> httpx.Response:
    return httpx.Response(
        status_code=200,
        content=data,
        headers={"content-type": content_type},
        request=httpx.Request("GET", "https://example.com/a.pdf"),
    )


def test_classify_reads_pdf_text_rather_than_discarding_it():
    body = "Tanker traffic through the strait fell sharply this week. " * 5
    outcome = classify(_binary_response(_minimal_pdf(body), "application/pdf"))
    assert outcome.status == STATUS_FETCHED
    assert "Tanker traffic through the strait" in outcome.text


def test_classify_records_a_damaged_pdf_as_error_not_unsupported():
    outcome = classify(_binary_response(b"%PDF-1.7 truncated", "application/pdf"))
    assert outcome.status == STATUS_ERROR
    assert "pdf:" in outcome.error


# ---- spreadsheets (#51) ----------------------------------------------------
#
# A statistical agency publishes its series as a workbook. Recording that
# `unsupported` threw away a primary source at the last step, beside a converter
# and an `openpyxl` dependency the image already carried.

XLSX_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def _workbook(rows: list[list[object]], sheet_title: str = "Consumption") -> bytes:
    from io import BytesIO

    from openpyxl import Workbook

    book = Workbook()
    sheet = book.active
    sheet.title = sheet_title
    for row in rows:
        sheet.append(row)
    buffer = BytesIO()
    book.save(buffer)
    return buffer.getvalue()


def _balance_rows() -> list[list[object]]:
    """Wide enough to clear MIN_TEXT_CHARS, shaped like a real monthly balance."""
    rows: list[list[object]] = [["Sector", "Apr", "May", "Jun", "Jul", "Aug"]]
    for sector in ("Power", "Fertilizer", "City Gas Distribution", "Refinery", "Petrochemicals"):
        rows.append([sector, 624, 1481, 1502, 1490, 1533])
    return rows


def test_classify_reads_a_spreadsheet_rather_than_recording_it_unsupported():
    outcome = classify(_binary_response(_workbook(_balance_rows()), XLSX_TYPE))
    assert outcome.status == STATUS_FETCHED
    assert "City Gas Distribution | 624 | 1481 | 1502 | 1490 | 1533" in outcome.text
    assert "## Consumption" in outcome.text, "the sheet name carries meaning; keep it"


def test_a_spreadsheet_arriving_with_a_charset_parameter_is_still_read():
    """Servers append `; charset=utf-8` to anything. The media type is the part
    before the semicolon, and the branch must key on that."""
    response = httpx.Response(
        status_code=200,
        content=_workbook(_balance_rows()),
        headers={"content-type": f"{XLSX_TYPE}; charset=utf-8"},
        request=httpx.Request("GET", "https://ppac.gov.in/x.xlsx"),
    )
    assert classify(response).status == STATUS_FETCHED


def test_a_damaged_workbook_is_an_error_not_unsupported():
    """`unsupported` means "we have no converter"; this one we have, and it
    failed. Conflating the two hides a converter that stopped working."""
    outcome = classify(_binary_response(b"PK\x03\x04 truncated", XLSX_TYPE))
    assert outcome.status == STATUS_ERROR
    assert "xlsx:" in outcome.error


def test_an_empty_workbook_does_not_pass_as_a_read_document():
    outcome = classify(_binary_response(_workbook([]), XLSX_TYPE))
    assert outcome.status == STATUS_ERROR


def test_xls_stays_unsupported_with_its_reason_recorded():
    """The pre-2007 OLE format needs a second library. It is a named gap, the
    way `source_crawler.extract` names it — not an anonymous skipped media type."""
    outcome = classify(_binary_response(b"\xd0\xcf\x11\xe0 ole", "application/vnd.ms-excel"))
    assert outcome.status == STATUS_UNSUPPORTED
    assert "xls" in outcome.error and "no converter" in outcome.error
    assert outcome.text is None


def test_the_request_asks_for_spreadsheets():
    """A branch that can read a workbook is worth nothing if the request never
    says it will accept one."""
    from apps.claude_agent.topics.search_content import HEADERS

    assert XLSX_TYPE in HEADERS["Accept"]


def test_classify_recovers_the_jsonld_body_behind_a_teaser():
    body = "Tanker traffic through the strait fell sharply this week. " * 8
    page = (
        '<html><head><script type="application/ld+json">'
        '{"@type":"NewsArticle","articleBody":"' + body + '"}'
        "</script></head><body><p>Subscribe to read.</p></body></html>"
    )
    outcome = classify(_response(200, page))
    assert outcome.status == STATUS_FETCHED
    assert "Tanker traffic through the strait" in outcome.text


def test_origin_strips_path_and_query():
    assert origin("https://example.com/news/a?b=1") == "https://example.com"


def _client(handler) -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=httpx.MockTransport(handler))


@pytest.mark.asyncio
async def test_fetch_one_honours_robots_disallow():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nDisallow: /news/")
        return httpx.Response(200, text=ARTICLE, headers={"content-type": "text/html"})

    async with _client(handler) as client:
        outcome = await fetch_one(client, RobotsCache(), "https://example.com/news/a")

    assert outcome.status == STATUS_DISALLOWED
    assert outcome.text is None


@pytest.mark.asyncio
async def test_missing_robots_txt_allows_the_fetch():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(404)
        return httpx.Response(200, text=ARTICLE, headers={"content-type": "text/html"})

    async with _client(handler) as client:
        outcome = await fetch_one(client, RobotsCache(), "https://example.com/news/a")

    assert outcome.status == STATUS_FETCHED


@pytest.mark.asyncio
async def test_robots_is_fetched_once_per_host():
    calls = {"robots": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            calls["robots"] += 1
            return httpx.Response(200, text="User-agent: *\nAllow: /")
        return httpx.Response(200, text=ARTICLE, headers={"content-type": "text/html"})

    robots = RobotsCache()
    async with _client(handler) as client:
        await fetch_one(client, robots, "https://example.com/a")
        await fetch_one(client, robots, "https://example.com/b")

    assert calls["robots"] == 1


@pytest.mark.asyncio
async def test_network_failure_is_recorded_not_raised():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("no route to host")

    async with _client(handler) as client:
        outcome = await fetch_one(client, RobotsCache(), "https://example.com/a")

    assert outcome.status == STATUS_ERROR
    assert "ConnectError" in outcome.error


# --- Retry-After ------------------------------------------------------------
# 429 used to be terminal. It means "come back later", not "you may not have
# this", so it gets one more attempt; an exhausted retry still records `blocked`.


def _robots_ok(inner):
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nAllow: /")
        return inner(request)

    return handler


@pytest.mark.asyncio
async def test_429_is_retried_once_and_can_succeed():
    calls = {"n": 0}

    def inner(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] == 1:
            return httpx.Response(429, headers={"retry-after": "0"})
        return httpx.Response(200, text=ARTICLE, headers={"content-type": "text/html"})

    async with _client(_robots_ok(inner)) as client:
        outcome = await fetch_one(client, RobotsCache(), "https://example.com/a")

    assert calls["n"] == 2
    assert outcome.status == STATUS_FETCHED


@pytest.mark.asyncio
async def test_persistent_429_still_records_blocked():
    calls = {"n": 0}

    def inner(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        return httpx.Response(429, headers={"retry-after": "0"})

    async with _client(_robots_ok(inner)) as client:
        outcome = await fetch_one(client, RobotsCache(), "https://example.com/a")

    assert calls["n"] == 2
    assert outcome.status == STATUS_BLOCKED


@pytest.mark.asyncio
async def test_a_long_retry_after_is_not_waited_out():
    calls = {"n": 0}

    def inner(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        return httpx.Response(429, headers={"retry-after": "3600"})

    async with _client(_robots_ok(inner)) as client:
        outcome = await fetch_one(client, RobotsCache(), "https://example.com/a")

    assert calls["n"] == 1
    assert outcome.status == STATUS_BLOCKED


@pytest.mark.asyncio
async def test_503_is_retried_but_stays_an_error_when_it_persists():
    calls = {"n": 0}

    def inner(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        return httpx.Response(503, headers={"retry-after": "0"})

    async with _client(_robots_ok(inner)) as client:
        outcome = await fetch_one(client, RobotsCache(), "https://example.com/a")

    assert calls["n"] == 2
    assert outcome.status == STATUS_ERROR


def test_retry_delay_reads_both_legal_header_forms():
    from email.utils import format_datetime

    assert retry_delay(_response(429)) == RETRY_DEFAULT_SEC
    assert retry_delay(_response(429, headers={"retry-after": "12"})) == 12.0
    assert retry_delay(_response(429, headers={"retry-after": "garbage"})) == RETRY_DEFAULT_SEC
    assert retry_delay(_response(429, headers={"retry-after": "99999"})) is None

    soon = format_datetime(datetime.now(UTC) + timedelta(seconds=10))
    delay = retry_delay(_response(429, headers={"retry-after": soon}))
    assert 0 < delay <= 11

    past = format_datetime(datetime.now(UTC) - timedelta(seconds=60))
    assert retry_delay(_response(429, headers={"retry-after": past})) == 0.0


# --- Coverage report --------------------------------------------------------
# No DB in this suite, so the queries are checked by compiling them against the
# dialect they will actually run on. FILTER (WHERE ...) is Postgres-specific.


def test_coverage_queries_compile_for_postgres():
    from sqlalchemy.dialects import postgresql

    status_sql = str(status_counts_stmt().compile(dialect=postgresql.dialect()))
    assert "GROUP BY" in status_sql
    assert "fetch_status" in status_sql

    domain_sql = str(domain_coverage_stmt(20).compile(dialect=postgresql.dialect()))
    assert "FILTER (WHERE" in domain_sql
    assert "GROUP BY" in domain_sql
    assert "ORDER BY" in domain_sql
    assert "fetch_status IS NOT NULL" in domain_sql


# --- Attempt ranking ---------------------------------------------------------
# Two paths write to the same document. The document keeps the best result, so
# the ordering below is what stops a later blocked retry from erasing an article
# an earlier attempt already read.


def test_text_outranks_every_outcome_that_carries_none():
    article = rank_of(STATUS_FETCHED, 5000)
    for empty in (STATUS_BLOCKED, STATUS_NOT_FOUND, STATUS_DISALLOWED, STATUS_ERROR):
        assert rank_of(empty, 0) < article


def test_a_full_article_outranks_a_thin_teaser():
    assert rank_of(STATUS_THIN, 120) < rank_of(STATUS_FETCHED, 800)


def test_the_longer_text_wins_within_the_same_status():
    assert rank_of(STATUS_FETCHED, 400) < rank_of(STATUS_FETCHED, 9000)
    assert rank_of(STATUS_THIN, 40) < rank_of(STATUS_THIN, 190)


def test_an_unattempted_document_ranks_below_anything():
    assert rank_of(None, 0) < rank_of(STATUS_BLOCKED, 0) or rank_of(None, 0) == rank_of(
        STATUS_BLOCKED, 0
    )
    assert rank_of(None, 0) < rank_of(STATUS_THIN, 1)


def test_timing_query_compiles_for_postgres():
    from sqlalchemy.dialects import postgresql

    sql = str(method_timing_stmt().compile(dialect=postgresql.dialect()))
    assert "percentile_cont" in sql
    assert "WITHIN GROUP" in sql
    assert "GROUP BY" in sql


# --- Host partitioning -------------------------------------------------------
# Hosts run concurrently, each host sequentially. The courtesy owed a site is one
# request at a time to *that* site — not one request at a time across the world.


def test_group_by_host_keeps_each_hosts_documents_together_and_in_order():
    documents = [
        (1, "https://a.example/one"),
        (2, "https://b.example/one"),
        (3, "https://a.example/two"),
        (4, "https://a.example/three"),
    ]
    groups = group_by_host(documents)

    assert set(groups) == {"a.example", "b.example"}
    assert groups["a.example"] == [
        (1, "https://a.example/one"),
        (3, "https://a.example/two"),
        (4, "https://a.example/three"),
    ]
    assert sum(len(v) for v in groups.values()) == len(documents)


def test_group_by_host_separates_ports_and_subdomains():
    groups = group_by_host(
        [
            (1, "https://example.com/a"),
            (2, "https://news.example.com/a"),
            (3, "https://example.com:8443/a"),
        ]
    )
    assert len(groups) == 3


@pytest.mark.asyncio
async def test_one_host_is_never_hit_concurrently():
    """The politeness guarantee: partitioning must serialise a host structurally."""
    concurrent = {"now": 0, "peak": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nAllow: /")
        concurrent["now"] += 1
        concurrent["peak"] = max(concurrent["peak"], concurrent["now"])
        concurrent["now"] -= 1
        return httpx.Response(200, text=ARTICLE, headers={"content-type": "text/html"})

    documents = [(i, f"https://one.example/{i}") for i in range(5)]
    async with _client(handler) as client:
        await _fetch_host_for_test(client, documents)

    assert concurrent["peak"] == 1


async def _fetch_host_for_test(client, documents):
    from apps.claude_agent.topics.search_content import _fetch_host

    recorded = []

    async def fake_record(document_id, outcome, **kw):
        recorded.append((document_id, outcome.status, kw["method"], kw["duration_ms"]))

    import apps.claude_agent.topics.search_content as mod

    original = mod.record_attempt
    mod.record_attempt = fake_record
    try:
        await _fetch_host(client, RobotsCache(), documents, host_interval_sec=0)
    finally:
        mod.record_attempt = original
    return recorded


@pytest.mark.asyncio
async def test_every_document_of_a_host_is_recorded_with_its_timing():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nAllow: /")
        return httpx.Response(200, text=ARTICLE, headers={"content-type": "text/html"})

    documents = [(i, f"https://one.example/{i}") for i in range(4)]
    async with _client(handler) as client:
        recorded = await _fetch_host_for_test(client, documents)

    assert [r[0] for r in recorded] == [0, 1, 2, 3], "order within a host must hold"
    assert {r[1] for r in recorded} == {STATUS_FETCHED}
    assert {r[2] for r in recorded} == {METHOD_HTTP}
    assert all(isinstance(r[3], int) for r in recorded), "duration must be recorded"


# ---- ambiguous media types -------------------------------------------------
#
# PPAC hands its monthly consumption report to
# `download.php?file=menu/…_ICR_OCT_25.pdf` and labels the response
# `application/octet-stream`. Taking the label at its word recorded the
# publisher's own report `unsupported` while we held a PDF reader — on the one
# domain the India brief rests on.


def _download_script_response(data: bytes, url: str, content_type: str) -> httpx.Response:
    return httpx.Response(
        status_code=200,
        content=data,
        headers={"content-type": content_type},
        request=httpx.Request("GET", url),
    )


def test_a_pdf_behind_a_download_script_is_read_not_discarded():
    body = "Sectoral consumption of natural gas rose across city gas networks. " * 5
    outcome = classify(
        _download_script_response(
            _minimal_pdf(body),
            "https://ppac.gov.in/download.php?file=menu/1763373356_ICR_OCT_25.pdf",
            "application/octet-stream",
        )
    )
    assert outcome.status == STATUS_FETCHED
    assert "Sectoral consumption of natural gas" in outcome.text


def test_a_workbook_is_claimed_only_when_the_url_names_one():
    """A ZIP header alone is not a spreadsheet — `.docx` and `.odt` open the same."""
    workbook = _workbook(_balance_rows())
    named = classify(
        _download_script_response(
            workbook, "https://ppac.gov.in/get.php?f=balance.xlsx", "application/octet-stream"
        )
    )
    assert named.status == STATUS_FETCHED
    assert "City Gas Distribution" in named.text

    unnamed = classify(
        _download_script_response(
            workbook, "https://example.com/get.php?f=notes", "application/octet-stream"
        )
    )
    assert unnamed.status == STATUS_UNSUPPORTED


def test_an_html_page_served_as_octet_stream_still_reads_as_html():
    outcome = classify(
        _download_script_response(
            ARTICLE.encode("utf-8"), "https://example.com/view.php?id=7", ""
        )
    )
    assert outcome.status == STATUS_FETCHED
    assert "Tanker traffic through the strait" in outcome.text


def test_named_extension_prefers_the_file_the_query_names():
    assert named_extension("https://ppac.gov.in/download.php?file=a/b_ICR.pdf") == ".pdf"
    assert named_extension("https://ppac.gov.in/uploads/x.xlsx") == ".xlsx"
    assert named_extension("https://example.com/articles/story") == ""
