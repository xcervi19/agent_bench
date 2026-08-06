from datetime import UTC, datetime, timedelta

import httpx
import pytest

from apps.claude_agent.topics.search_content import (
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
