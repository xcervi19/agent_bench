from __future__ import annotations

from calendar import month_name
from datetime import date

from ..base import SourceAdapter
from ..models import (
    DocRef,
    DownloadedDoc,
    SourceAssessment,
    SourceConfig,
    SourceTarget,
)
from ..registry import register
from ._http import http_get
from .static_pdf import MIN_BYTES, PDF_MAGIC, _require_pdf

_MONTHS = [m.lower() for m in month_name if m]


def _normalize_ext(value: str | None) -> str:
    if not value:
        return ".pdf"
    return value if value.startswith(".") else f".{value}"


def _candidate_urls(config: SourceConfig, *, max_back: int = 24) -> list[str]:
    """Build dated OPEC assetdb URLs newest-first.

    extras:
      cadence: monthly | yearly
      url_template: must include {month}+{year} (monthly) or {year} (yearly)
    """
    cadence = str(config.extras.get("cadence") or "monthly").lower()
    template = str(config.extras.get("url_template") or "").strip()
    if not template:
        raise ValueError(f"{config.source_id}: extras.url_template is required")

    today = date.today()
    urls: list[str] = []
    if cadence == "yearly":
        for back in range(0, max(max_back, 8)):
            urls.append(template.format(year=today.year - back))
        return urls

    if cadence != "monthly":
        raise ValueError(f"{config.source_id}: unsupported cadence {cadence!r}")

    year, month = today.year, today.month
    for _ in range(max_back):
        urls.append(template.format(month=_MONTHS[month - 1], year=year))
        month -= 1
        if month == 0:
            month = 12
            year -= 1
    return urls


def _probe_pdf_url(url: str) -> str | None:
    """Return final PDF URL if the asset exists (Range probe; full GET in fetch)."""
    from ._http import DEFAULT_HEADERS, USER_AGENT
    import httpx

    headers = {
        **DEFAULT_HEADERS,
        "User-Agent": USER_AGENT,
        "Range": "bytes=0-15",
        "Accept": "application/pdf,*/*",
    }
    with httpx.Client(
        timeout=httpx.Timeout(45.0),
        headers=headers,
        follow_redirects=True,
    ) as client:
        resp = client.get(url)
    if resp.status_code >= 400:
        return None
    body = resp.content
    if not body.startswith(PDF_MAGIC):
        return None
    # Prefer the requested asset URL (redirects may land on a generic 404 page URL).
    final = str(resp.url)
    if final.rstrip("/").endswith(".pdf"):
        return final
    if body.startswith(PDF_MAGIC):
        return url
    return None


def _first_live_pdf_url(urls: list[str]) -> str | None:
    for url in urls:
        hit = _probe_pdf_url(url)
        if hit:
            return hit
    return None



@register
class OpecAssetdbAdapter(SourceAdapter):
    """Discover + fetch dated PDFs from opec.org/assets/assetdb/."""

    name = "opec_assetdb"

    def evaluate(self, target: SourceTarget) -> SourceAssessment:
        cfg = SourceConfig(
            source_id=target.source_id or "opec_assetdb",
            adapter=self.name,
            endpoint=target.url,
            extras=dict(target.hints.get("extras") or target.hints),
        )
        try:
            url = _first_live_pdf_url(_candidate_urls(cfg))
        except ValueError as exc:
            return SourceAssessment(
                adapter=self.name,
                endpoint=target.url,
                viable=False,
                reason=str(exc),
            )
        if not url:
            return SourceAssessment(
                adapter=self.name,
                endpoint=target.url,
                viable=False,
                reason="no dated PDF found in lookback window",
            )
        return SourceAssessment(
            adapter=self.name,
            endpoint=url,
            viable=True,
            reason="pdf ok",
            proposed_config=SourceConfig(
                source_id=cfg.source_id,
                adapter=self.name,
                endpoint=url,
                extras=cfg.extras,
            ),
        )

    def discover(self, config: SourceConfig) -> list[DocRef]:
        url = _first_live_pdf_url(_candidate_urls(config))
        if not url:
            raise RuntimeError(
                f"no OPEC assetdb PDF found for {config.source_id!r} "
                f"(template={config.extras.get('url_template')!r})"
            )
        return [
            DocRef(
                url=url,
                title=config.title or config.source_id,
                content_type="application/pdf",
                extras={"extension": _normalize_ext(config.extras.get("extension"))},
            )
        ]

    def fetch(self, ref: DocRef, config: SourceConfig) -> DownloadedDoc:
        resp = http_get(ref.url)
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
