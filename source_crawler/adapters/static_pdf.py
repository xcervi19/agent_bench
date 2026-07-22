from __future__ import annotations

import re
from urllib.parse import urlparse

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

# Browser-like headers: some CDNs (Akamai/S&P) block bare bot UAs with HTTP 403.
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
MIN_BYTES = 1024
PDF_MAGIC = b"%PDF"
DEFAULT_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/pdf,application/octet-stream;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def _slug_from_url(url: str) -> str:
    path = urlparse(url).path.rstrip("/")
    name = path.rsplit("/", 1)[-1] or "document"
    name = re.sub(r"\.(pdf|ashx)$", "", name, flags=re.IGNORECASE)
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "_", name).strip("_").lower()
    return slug[:120] or "document"


def _http_get(url: str, *, timeout_sec: float = 60.0) -> httpx.Response:
    with httpx.Client(
        timeout=httpx.Timeout(timeout_sec),
        headers=DEFAULT_HEADERS,
        follow_redirects=True,
    ) as client:
        return client.get(url)


def _require_pdf(body: bytes, content_type: str | None, url: str) -> None:
    if body.startswith(PDF_MAGIC):
        return
    raise ValueError(
        f"not a PDF response for {url!r}: content_type={content_type!r}, "
        f"bytes={len(body)}, magic={body[:8]!r}"
    )


@register
class StaticPdfAdapter(SourceAdapter):
    name = "static_pdf"

    def evaluate(self, target: SourceTarget) -> SourceAssessment:
        resp = _http_get(target.url)
        if resp.status_code >= 400:
            return SourceAssessment(
                adapter=self.name,
                endpoint=target.url,
                viable=False,
                reason=f"HTTP {resp.status_code}",
            )
        try:
            _require_pdf(resp.content, resp.headers.get("content-type"), target.url)
        except ValueError as exc:
            return SourceAssessment(
                adapter=self.name,
                endpoint=target.url,
                viable=False,
                reason=str(exc),
            )
        source_id = target.source_id or _slug_from_url(target.url)
        title = str(target.hints.get("title") or source_id)
        publisher = str(target.hints.get("publisher") or "")
        return SourceAssessment(
            adapter=self.name,
            endpoint=str(resp.url),
            viable=True,
            reason="pdf ok",
            proposed_config=SourceConfig(
                source_id=source_id,
                adapter=self.name,
                endpoint=str(resp.url),
                title=title,
                publisher=publisher,
                interval_hours=int(target.hints.get("interval_hours", 720)),
                commodity=str(target.hints.get("commodity", "crude_oil")),
                region=target.hints.get("region"),
                tier=int(target.hints.get("tier", 1)),
                domain=str(target.hints.get("domain", "trading_mechanics")),
                tags=tuple(target.hints.get("tags", ("methodology", "pricing"))),
                # Human must set these before crawl/enroll (see rag_label_vocab.md).
                label_assignment=target.hints.get("label_assignment"),
                document_type=target.hints.get("document_type"),
                use_for=tuple(target.hints.get("use_for") or ()),
            ),
        )

    def discover(self, config: SourceConfig) -> list[DocRef]:
        return [
            DocRef(
                url=config.endpoint,
                title=config.title or config.source_id,
                content_type="application/pdf",
            )
        ]

    def fetch(self, ref: DocRef, config: SourceConfig) -> DownloadedDoc:
        resp = _http_get(ref.url)
        if resp.status_code >= 400:
            raise RuntimeError(f"HTTP {resp.status_code} for {ref.url}")
        body = resp.content
        if len(body) < MIN_BYTES:
            raise RuntimeError(f"response too small ({len(body)} bytes) for {ref.url}")
        content_type = resp.headers.get("content-type", "application/pdf")
        _require_pdf(body, content_type, ref.url)
        return DownloadedDoc(
            ref=ref,
            body=body,
            content_type=content_type,
            extension=".pdf",
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
            },
        )
