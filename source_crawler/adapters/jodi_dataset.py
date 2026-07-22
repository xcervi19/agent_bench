from __future__ import annotations

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
from .static_file import _normalize_ext, _validate_body, _guess_content_type

FILES_API = "https://api.publisher.jodidata.org/web/files/{kind}"
PUBLISHER_FILE = "https://www.jodidata.org/jodi-publisher/{kind}/{publication_id}/{filename}"
# Classic oil dump when publisher API returns an empty file list.
OIL_FALLBACK_ZIP = (
    "https://www.jodidata.org/_resources/files/downloads/oil-data/world_ext.zip"
)


def _kind(config: SourceConfig | SourceTarget) -> str:
    if isinstance(config, SourceConfig):
        kind = str(config.extras.get("jodi_kind") or "").lower()
    else:
        kind = str(config.hints.get("jodi_kind") or "").lower()
    if kind not in {"oil", "gas"}:
        raise ValueError("extras.jodi_kind must be 'oil' or 'gas'")
    return kind


def _resolve_dataset_url(kind: str) -> tuple[str, str]:
    """Return (download_url, extension) for the latest world CSV dump."""
    resp = http_get(FILES_API.format(kind=kind))
    if resp.status_code >= 400:
        raise RuntimeError(f"JODI files API HTTP {resp.status_code} for {kind}")
    payload = resp.json()
    files = payload.get("files") or []
    publication_id = payload.get("publicationId")
    csv_files = [f for f in files if str(f.get("format", "")).upper() == "CSV"]
    chosen = csv_files[0] if csv_files else (files[0] if files else None)
    if chosen and publication_id:
        filename = str(chosen["filename"])
        url = PUBLISHER_FILE.format(
            kind=kind,
            publication_id=publication_id,
            filename=filename,
        )
        ext = _normalize_ext("." + filename.rsplit(".", 1)[-1].lower())
        return url, ext
    if kind == "oil":
        return OIL_FALLBACK_ZIP, ".zip"
    raise RuntimeError(f"JODI {kind}: no downloadable files in publisher API")


@register
class JodiDatasetAdapter(SourceAdapter):
    """JODI Oil/Gas world CSV dumps (data feed → DB, not RAG)."""

    name = "jodi_dataset"

    def evaluate(self, target: SourceTarget) -> SourceAssessment:
        try:
            kind = str(target.hints.get("jodi_kind") or "").lower()
            if kind not in {"oil", "gas"}:
                raise ValueError("hints.jodi_kind must be 'oil' or 'gas'")
            url, ext = _resolve_dataset_url(kind)
            resp = http_get(
                url,
                referer=f"https://www.jodidata.org/{kind}/database/data-downloads.aspx",
            )
            if resp.status_code >= 400:
                return SourceAssessment(
                    adapter=self.name,
                    endpoint=url,
                    viable=False,
                    reason=f"HTTP {resp.status_code}",
                )
            _validate_body(resp.content, ext, url)
        except Exception as exc:
            return SourceAssessment(
                adapter=self.name,
                endpoint=target.url,
                viable=False,
                reason=str(exc),
            )
        return SourceAssessment(
            adapter=self.name,
            endpoint=url,
            viable=True,
            reason="dataset ok",
            proposed_config=SourceConfig(
                source_id=target.source_id or f"jodi_{kind}",
                adapter=self.name,
                endpoint=url,
                extras={"jodi_kind": kind, "extension": ext, "pipeline": "data_feed"},
            ),
        )

    def discover(self, config: SourceConfig) -> list[DocRef]:
        kind = _kind(config)
        url, ext = _resolve_dataset_url(kind)
        return [
            DocRef(
                url=url,
                title=config.title or config.source_id,
                extras={
                    "extension": ext,
                    "referer": f"https://www.jodidata.org/{kind}/database/data-downloads.aspx",
                },
            )
        ]

    def fetch(self, ref: DocRef, config: SourceConfig) -> DownloadedDoc:
        kind = _kind(config)
        ext = _normalize_ext(
            str(ref.extras.get("extension") or config.extras.get("extension") or ".zip")
        )
        referer = ref.extras.get("referer") or (
            f"https://www.jodidata.org/{kind}/database/data-downloads.aspx"
        )
        resp = http_get(ref.url, referer=str(referer))
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
                "pipeline": "data_feed",
                "skip_rag": True,
                "jodi_kind": kind,
            },
        )
