from __future__ import annotations

from urllib.parse import urlparse

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

MIN_BYTES = 64
_ZIP_MAGIC = b"PK\x03\x04"


def _normalize_ext(value: str | None, *, default: str = ".bin") -> str:
    if not value:
        return default
    return value if value.startswith(".") else f".{value}"


def _ext_from_url(url: str) -> str:
    path = urlparse(url).path
    name = path.rsplit("/", 1)[-1]
    if "." in name:
        return _normalize_ext("." + name.rsplit(".", 1)[-1].lower())
    return ".bin"


def _guess_content_type(ext: str, header: str | None) -> str:
    if header and "html" not in header.lower():
        return header
    return {
        ".zip": "application/zip",
        ".csv": "text/csv",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".pdf": "application/pdf",
    }.get(ext, "application/octet-stream")


def _validate_body(body: bytes, ext: str, url: str) -> None:
    if len(body) < MIN_BYTES:
        raise ValueError(f"response too small ({len(body)} bytes) for {url!r}")
    if body.lstrip().startswith(b"<!") or body.lstrip().lower().startswith(b"<html"):
        raise ValueError(f"HTML error page instead of file for {url!r}")
    if ext == ".zip" and not body.startswith(_ZIP_MAGIC):
        raise ValueError(f"not a ZIP response for {url!r}: magic={body[:8]!r}")
    if ext == ".csv":
        # UTF-8/ASCII tabular dump; reject obvious binary.
        sample = body[:512]
        if b"\x00" in sample:
            raise ValueError(f"binary payload for CSV {url!r}")


@register
class StaticFileAdapter(SourceAdapter):
    """Fixed-URL download for non-PDF artifacts (zip/csv/xlsx). Not for RAG extract."""

    name = "static_file"

    def evaluate(self, target: SourceTarget) -> SourceAssessment:
        ext = _normalize_ext(
            str(target.hints.get("extension") or _ext_from_url(target.url))
        )
        resp = http_get(target.url, referer=str(target.hints.get("referer") or None))
        if resp.status_code >= 400:
            return SourceAssessment(
                adapter=self.name,
                endpoint=target.url,
                viable=False,
                reason=f"HTTP {resp.status_code}",
            )
        try:
            _validate_body(resp.content, ext, target.url)
        except ValueError as exc:
            return SourceAssessment(
                adapter=self.name,
                endpoint=target.url,
                viable=False,
                reason=str(exc),
            )
        source_id = target.source_id or "static_file"
        return SourceAssessment(
            adapter=self.name,
            endpoint=str(resp.url),
            viable=True,
            reason="file ok",
            proposed_config=SourceConfig(
                source_id=source_id,
                adapter=self.name,
                endpoint=str(resp.url),
                extras={"extension": ext},
            ),
        )

    def discover(self, config: SourceConfig) -> list[DocRef]:
        ext = _normalize_ext(
            str(config.extras.get("extension") or _ext_from_url(config.endpoint))
        )
        return [
            DocRef(
                url=config.endpoint,
                title=config.title or config.source_id,
                extras={"extension": ext, "referer": config.extras.get("referer")},
            )
        ]

    def fetch(self, ref: DocRef, config: SourceConfig) -> DownloadedDoc:
        ext = _normalize_ext(
            str(
                ref.extras.get("extension")
                or config.extras.get("extension")
                or _ext_from_url(ref.url)
            )
        )
        referer = ref.extras.get("referer") or config.extras.get("referer")
        resp = http_get(ref.url, referer=str(referer) if referer else None)
        if resp.status_code >= 400:
            raise RuntimeError(f"HTTP {resp.status_code} for {ref.url}")
        body = resp.content
        _validate_body(body, ext, ref.url)
        content_type = _guess_content_type(ext, resp.headers.get("content-type"))
        return DownloadedDoc(
            ref=ref,
            body=body,
            content_type=content_type,
            extension=ext,
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
                "pipeline": config.extras.get("pipeline", "data_feed"),
            },
        )
