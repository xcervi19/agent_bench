"""Fetch the page behind every captured search hit, in the background.

Nothing is filtered: every document in the evidence store is attempted, because a
filter here would be exactly the capture-time verdict the evidence design avoids.
Outcomes are recorded rather than retried away — a domain that always blocks us is
a fact about our coverage, and the later evaluation pass needs to know it.

Deliberately polite: identifying user agent, robots.txt respected, one request per
host at a time. There is no attempt to defeat bot protection; blocked is a valid
outcome.

Coverage is raised by reading what publishers already hand us rather than by
pretending to be someone else:

  * JSON-LD article bodies, which sites emit for search engines even when the
    rendered HTML is a teaser (see `html_article_text`).
  * PDFs, which used to be discarded as an unsupported media type.
  * A single retry on 429/503, which say "later" rather than "no".

`coverage()` reports what is left over, per status and per domain — that is the
input for deciding where a feed or a publisher API is worth arranging.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser

import httpx
from sqlalchemy import func, select

from source_ingest.text_extract import html_article_text, pdf_bytes_to_text

from ..config import ClaudeAgentSettings
from .db import session_scope
from .models import SearchDocument, SearchDocumentFetch

logger = logging.getLogger(__name__)

STATUS_FETCHED = "fetched"
STATUS_THIN = "thin"
STATUS_BLOCKED = "blocked"
STATUS_NOT_FOUND = "not_found"
STATUS_DISALLOWED = "disallowed"
STATUS_UNSUPPORTED = "unsupported"
STATUS_ERROR = "error"

BLOCKED_CODES = {401, 402, 403, 429}
MIN_TEXT_CHARS = 200

# Which path made the attempt. They do not yield the same artifact — `http` is
# text we extracted from the raw response ourselves, `agent` is text the model's
# WebFetch already processed — so an evaluation pass must be able to tell them
# apart rather than reading one `content` column and guessing.
METHOD_HTTP = "http"
METHOD_AGENT = "agent"

# How good an outcome is, for deciding whether it replaces what the document
# already holds. Anything not listed carries no text and never supersedes text.
STATUS_RANK = {STATUS_FETCHED: 2, STATUS_THIN: 1}

# "Come back later" is not "you may not have this". Both codes get one more
# attempt; if it still fails the status is whatever `classify` would have said
# anyway (429 -> blocked, 503 -> error), so exhausted retries stay visible.
RETRY_CODES = {429, 503}
MAX_RETRIES = 1
RETRY_DEFAULT_SEC = 5.0
RETRY_AFTER_CAP_SEC = 60.0

TEXT_TYPES = {"text/html", "application/xhtml+xml", "text/plain", ""}
PDF_TYPES = {"application/pdf", "application/x-pdf"}

USER_AGENT = "SignalGatherBot/1.0 (+evidence corpus; contact: team@techartsociety.com)"
HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/pdf",
    "Accept-Language": "en;q=0.9,*;q=0.5",
}


@dataclass(frozen=True)
class FetchOutcome:
    status: str
    text: str | None = None
    error: str | None = None


def classify(response: httpx.Response) -> FetchOutcome:
    if response.status_code in BLOCKED_CODES:
        return FetchOutcome(STATUS_BLOCKED, error=f"HTTP {response.status_code}")
    if response.status_code == 404:
        return FetchOutcome(STATUS_NOT_FOUND, error="HTTP 404")
    if response.status_code >= 400:
        return FetchOutcome(STATUS_ERROR, error=f"HTTP {response.status_code}")
    media_type = response.headers.get("content-type", "").split(";")[0].strip().lower()
    if media_type in PDF_TYPES:
        try:
            text = pdf_bytes_to_text(response.content, str(response.url))
        except Exception as exc:  # pypdf raises a wide family on damaged files
            return FetchOutcome(STATUS_ERROR, error=f"pdf: {type(exc).__name__}: {exc}")
    elif media_type in TEXT_TYPES:
        text = html_article_text(response.text)
    else:
        return FetchOutcome(STATUS_UNSUPPORTED, error=media_type)
    if len(text) < MIN_TEXT_CHARS:
        return FetchOutcome(STATUS_THIN, text=text or None, error=f"{len(text)} chars")
    return FetchOutcome(STATUS_FETCHED, text=text)


def origin(url: str) -> str:
    parts = urlsplit(url)
    return f"{parts.scheme}://{parts.netloc}"


class RobotsCache:
    """One robots.txt lookup per host, reused for the rest of the batch.

    An unreachable or missing robots.txt allows fetching — the standard reading,
    and the alternative would silently drop every host that does not publish one.
    """

    def __init__(self) -> None:
        self._parsers: dict[str, RobotFileParser | None] = {}

    async def allows(self, client: httpx.AsyncClient, url: str) -> bool:
        root = origin(url)
        if root not in self._parsers:
            self._parsers[root] = await self._load(client, root)
        parser = self._parsers[root]
        return True if parser is None else parser.can_fetch(USER_AGENT, url)

    async def _load(self, client: httpx.AsyncClient, root: str) -> RobotFileParser | None:
        try:
            response = await client.get(f"{root}/robots.txt")
        except httpx.HTTPError:
            return None
        if response.status_code >= 400:
            return None
        parser = RobotFileParser()
        parser.parse(response.text.splitlines())
        return parser


def retry_delay(response: httpx.Response) -> float | None:
    """How long to wait before retrying, or None if we should not.

    Honours `Retry-After` in either legal form (delta-seconds or HTTP-date) and
    falls back to a small fixed pause when the header is absent, which is the
    common shape of a 429. A host asking for longer than the cap is telling us to
    go away for now, so we record the block instead of sitting on the batch.
    """
    raw = (response.headers.get("retry-after") or "").strip()
    if not raw:
        return RETRY_DEFAULT_SEC
    try:
        delay = float(int(raw))
    except ValueError:
        try:
            when = parsedate_to_datetime(raw)
        except (TypeError, ValueError):
            return RETRY_DEFAULT_SEC
        if when.tzinfo is None:
            when = when.replace(tzinfo=UTC)
        delay = (when - datetime.now(UTC)).total_seconds()
    delay = max(0.0, delay)
    return None if delay > RETRY_AFTER_CAP_SEC else delay


async def fetch_one(client: httpx.AsyncClient, robots: RobotsCache, url: str) -> FetchOutcome:
    if not await robots.allows(client, url):
        return FetchOutcome(STATUS_DISALLOWED, error="robots.txt")
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = await client.get(url)
        except httpx.HTTPError as exc:
            return FetchOutcome(STATUS_ERROR, error=f"{type(exc).__name__}: {exc}")
        if attempt == MAX_RETRIES or response.status_code not in RETRY_CODES:
            break
        delay = retry_delay(response)
        if delay is None:
            break
        logger.info("content.retry code=%s delay=%.1fs url=%s", response.status_code, delay, url)
        await asyncio.sleep(delay)
    return classify(response)


async def _pending(limit: int) -> list[tuple[int, str]]:
    async with session_scope() as s:
        rows = await s.execute(
            select(SearchDocument.id, SearchDocument.url)
            .where(SearchDocument.fetch_status.is_(None))
            .order_by(SearchDocument.first_seen_at)
            .limit(limit)
        )
        return list(rows.all())


def rank_of(status: str | None, chars: int) -> tuple[int, int]:
    """Orders outcomes so a later failure cannot erase text we already hold.

    A retry that gets blocked must not wipe the article a previous attempt read.
    Within the same status the longer text wins — that is how the agent's fetch
    takes over a paywalled teaser our own client recorded as `thin`.
    """
    return (STATUS_RANK.get(status or "", 0), chars)


async def record_attempt(
    document_id: int,
    outcome: FetchOutcome,
    *,
    method: str,
    started_at: datetime,
    duration_ms: int,
) -> None:
    """Append the attempt, then update the document only if this result is better."""
    chars = len(outcome.text or "")
    async with session_scope() as s:
        s.add(
            SearchDocumentFetch(
                document_id=document_id,
                method=method,
                status=outcome.status,
                error=outcome.error,
                content=outcome.text,
                content_chars=chars,
                duration_ms=duration_ms,
                started_at=started_at,
                finished_at=datetime.now(UTC),
            )
        )
        document = await s.get(SearchDocument, document_id)
        if document is None:
            return
        current = rank_of(document.fetch_status, len(document.content or ""))
        # `>=` on a first attempt (both ranks (0, 0)) so an outcome carrying no
        # text still leaves the queue and gets recorded on the document.
        if document.fetch_status is None or rank_of(outcome.status, chars) > current:
            document.content = outcome.text
            document.fetch_status = outcome.status
            document.fetch_error = outcome.error
            document.fetched_at = datetime.now(UTC)
            document.fetch_method = method


def status_counts_stmt():
    """One row per recorded outcome, plus a NULL row for the unattempted queue."""
    return select(SearchDocument.fetch_status, func.count()).group_by(SearchDocument.fetch_status)


def domain_coverage_stmt(limit: int):
    """Attempted vs. readable per domain, worst first. Ignores the pending queue."""
    attempted = func.count()
    readable = func.count().filter(SearchDocument.fetch_status == STATUS_FETCHED)
    return (
        select(SearchDocument.domain, attempted, readable)
        .where(SearchDocument.fetch_status.is_not(None))
        .group_by(SearchDocument.domain)
        .order_by((attempted - readable).desc(), SearchDocument.domain)
        .limit(limit)
    )


def method_timing_stmt():
    """Attempts, outcome and latency per path — the input for judging which pays off."""
    duration = SearchDocumentFetch.duration_ms
    return (
        select(
            SearchDocumentFetch.method,
            SearchDocumentFetch.status,
            func.count().label("attempts"),
            func.round(func.avg(duration)).label("avg_ms"),
            func.percentile_cont(0.95).within_group(duration.asc()).label("p95_ms"),
        )
        .group_by(SearchDocumentFetch.method, SearchDocumentFetch.status)
        .order_by(SearchDocumentFetch.method, func.count().desc())
    )


async def coverage(domain_limit: int = 20) -> dict:
    """What the corpus can actually read, by outcome and by domain.

    A NULL `fetch_status` is the queue rather than a result, so it is reported as
    `pending` instead of being folded into the outcome counts — otherwise a large
    backlog reads as a coverage problem. `worst_domains` ranks by how many
    attempted documents we could not turn into text, which is where a feed or an
    API is worth arranging.
    """
    async with session_scope() as s:
        status_rows = await s.execute(status_counts_stmt())
        by_status = {status: count for status, count in status_rows.all()}
        domain_rows = await s.execute(domain_coverage_stmt(domain_limit))
        domains = domain_rows.all()
        timing_rows = await s.execute(method_timing_stmt())
        timings = timing_rows.all()

    pending = by_status.pop(None, 0)
    attempted = sum(by_status.values())
    readable = by_status.get(STATUS_FETCHED, 0)
    return {
        "pending": pending,
        "attempted": attempted,
        "readable": readable,
        "readable_pct": round(100.0 * readable / attempted, 1) if attempted else None,
        "by_status": dict(sorted(by_status.items(), key=lambda kv: -kv[1])),
        "worst_domains": [
            {
                "domain": domain,
                "attempted": total,
                "readable": got,
                "unreadable": total - got,
            }
            for domain, total, got in domains
            if total > got
        ],
        "by_method": [
            {
                "method": method,
                "status": status,
                "attempts": attempts,
                "avg_ms": int(avg_ms) if avg_ms is not None else None,
                "p95_ms": int(p95_ms) if p95_ms is not None else None,
            }
            for method, status, attempts, avg_ms, p95_ms in timings
        ],
    }


class _HostPacer:
    """Keeps consecutive requests to the same host at least `interval` apart."""

    def __init__(self, interval_sec: float) -> None:
        self._interval = interval_sec
        self._last: dict[str, float] = {}

    async def wait(self, url: str) -> None:
        host = urlsplit(url).netloc
        now = asyncio.get_running_loop().time()
        earliest = self._last.get(host, 0.0) + self._interval
        if earliest > now:
            await asyncio.sleep(earliest - now)
        self._last[host] = asyncio.get_running_loop().time()


async def fetch_pending(limit: int, *, host_interval_sec: float = 2.0) -> int:
    """Attempt every unfetched document, up to `limit`. Returns how many were attempted."""
    documents = await _pending(limit)
    if not documents:
        return 0
    robots = RobotsCache()
    pacer = _HostPacer(host_interval_sec)
    async with httpx.AsyncClient(
        headers=HEADERS, follow_redirects=True, timeout=httpx.Timeout(30.0)
    ) as client:
        for document_id, url in documents:
            await pacer.wait(url)
            # Timed from here, so the robots.txt lookup on a host's first document
            # counts against this path — it is part of what our client costs.
            started_at = datetime.now(UTC)
            clock = time.monotonic()
            outcome = await fetch_one(client, robots, url)
            duration_ms = int((time.monotonic() - clock) * 1000)
            await record_attempt(
                document_id,
                outcome,
                method=METHOD_HTTP,
                started_at=started_at,
                duration_ms=duration_ms,
            )
            logger.info(
                "content.fetch status=%s ms=%s url=%s", outcome.status, duration_ms, url
            )
    return len(documents)


class ContentFetcher:
    """Background loop draining the unfetched-document queue."""

    def __init__(self, settings: ClaudeAgentSettings) -> None:
        self.settings = settings
        self._stop = asyncio.Event()
        self._task: asyncio.Task | None = None

    def start(self) -> None:
        if self._task is not None:
            return
        self._stop.clear()
        self._task = asyncio.create_task(self._loop(), name="search-content-fetcher")
        logger.info(
            "content_fetcher.started poll_interval=%ss batch=%s",
            self.settings.content_fetch_poll_interval_sec,
            self.settings.content_fetch_batch_size,
        )

    async def stop(self) -> None:
        self._stop.set()
        if self._task is not None:
            await asyncio.gather(self._task, return_exceptions=True)
            self._task = None
        logger.info("content_fetcher.stopped")

    async def tick(self) -> int:
        return await fetch_pending(self.settings.content_fetch_batch_size)

    async def _loop(self) -> None:
        while not self._stop.is_set():
            try:
                await self.tick()
            except Exception:  # pragma: no cover - a bad batch must not kill the loop
                logger.exception("content_fetcher.tick failed")
            with contextlib.suppress(TimeoutError):
                await asyncio.wait_for(
                    self._stop.wait(), timeout=self.settings.content_fetch_poll_interval_sec
                )
