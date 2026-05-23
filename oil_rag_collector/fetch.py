from __future__ import annotations

import hashlib
import json
import re
import time
from pathlib import Path
from urllib.parse import urlparse

import httpx

from .models import FetchOutcome, SourceFormat, SourceSpec

USER_AGENT = "OilRagCollector/1.0 (+research; contact=local)"
MIN_BYTES = 512
DOMAIN_DELAY_SEC = 1.2


def _domain(url: str) -> str:
    return urlparse(url).netloc.lower()


def _extension_for(spec: SourceSpec, content_type: str | None, body: bytes) -> str:
    if body[:4] == b"%PDF":
        return ".pdf"
    if spec.format == SourceFormat.PDF:
        return ".pdf"
    if spec.format == SourceFormat.JSON or spec.format == SourceFormat.API:
        return ".json"
    ct = (content_type or "").lower()
    if "pdf" in ct:
        return ".pdf"
    if "json" in ct:
        return ".json"
    if "html" in ct or spec.format == SourceFormat.HTML:
        return ".html"
    return ".bin"


def _target_path(root: Path, spec: SourceSpec, ext: str, suffix: str = "") -> Path:
    safe_id = re.sub(r"[^a-zA-Z0-9_-]+", "_", spec.id)[:120]
    name = f"{safe_id}{suffix}{ext}"
    return root / f"tier_{spec.tier}" / spec.domain.value / name


def fetch_http(
    client: httpx.Client,
    spec: SourceSpec,
    root: Path,
    *,
    url: str | None = None,
    discovered_from: str | None = None,
    suffix: str = "",
    retries: int = 3,
) -> FetchOutcome:
    if spec.format == SourceFormat.METADATA_ONLY:
        return FetchOutcome(source_id=spec.id, status="skipped", error="metadata_only")

    target_url = url or spec.url
    dest = _target_path(root, spec, ".tmp", suffix=suffix)

    last_error: str | None = None
    resp: httpx.Response | None = None
    for attempt in range(retries):
        try:
            resp = client.get(target_url, follow_redirects=True)
            resp.raise_for_status()
            last_error = None
            break
        except httpx.HTTPError as exc:
            last_error = str(exc)
            if attempt + 1 < retries:
                time.sleep(1.5 * (attempt + 1))
    if last_error or resp is None:
        status = "skipped" if spec.optional else "failed"
        return FetchOutcome(
            source_id=spec.id,
            status=status,
            error=last_error,
            discovered_from=discovered_from,
        )

    body = resp.content
    if len(body) < MIN_BYTES:
        return FetchOutcome(
            source_id=spec.id,
            status="failed",
            error=f"response too small ({len(body)} bytes)",
            discovered_from=discovered_from,
        )

    ext = _extension_for(spec, resp.headers.get("content-type"), body)
    dest = _target_path(root, spec, ext, suffix=suffix)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(body)

    sidecar = dest.with_suffix(dest.suffix + ".meta.json")
    sidecar.write_text(
        json.dumps(
            {
                "source_id": spec.id,
                "title": spec.title,
                "url": target_url,
                "publisher": spec.publisher,
                "tier": spec.tier,
                "domain": spec.domain.value,
                "commodity": spec.commodity,
                "region": spec.region,
                "tags": list(spec.tags),
                "content_type": resp.headers.get("content-type"),
                "sha256": hashlib.sha256(body).hexdigest(),
                "discovered_from": discovered_from,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    return FetchOutcome(
        source_id=spec.id,
        status="ok",
        path=str(dest.relative_to(root)),
        bytes=len(body),
        content_type=resp.headers.get("content-type"),
        discovered_from=discovered_from,
    )


class DomainRateLimiter:
    def __init__(self, delay_sec: float = DOMAIN_DELAY_SEC) -> None:
        self._delay = delay_sec
        self._last: dict[str, float] = {}

    def wait(self, url: str) -> None:
        dom = _domain(url)
        now = time.monotonic()
        prev = self._last.get(dom, 0.0)
        gap = self._delay - (now - prev)
        if gap > 0:
            time.sleep(gap)
        self._last[dom] = time.monotonic()


def build_client(timeout_sec: float) -> httpx.Client:
    return httpx.Client(
        timeout=httpx.Timeout(timeout_sec),
        headers={"User-Agent": USER_AGENT},
        follow_redirects=True,
    )
