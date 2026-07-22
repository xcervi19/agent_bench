from __future__ import annotations

import logging
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Literal

from .adapters import (  # noqa: F401 — register adapters
    jodi_dataset as _jodi_dataset,
    opec_assetdb as _opec_assetdb,
    static_file as _static_file,
    static_pdf as _static_pdf,
)
from .labels import validate_config_labels
from .models import SourceConfig
from .registry import get
from .store import content_path, sha256_hex, stored_sha256, sync_sidecar, write_doc

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class CrawlResult:
    source_id: str
    status: Literal["written", "unchanged", "disabled", "failed"]
    path: str | None
    sha256: str | None
    config: SourceConfig
    reason: str | None = None


def _config_extension(config: SourceConfig) -> str:
    ext = config.extras.get("extension")
    if isinstance(ext, str) and ext.strip():
        return ext if ext.startswith(".") else f".{ext}"
    return ".pdf"


def crawl(config: SourceConfig, root: Path) -> CrawlResult:
    if not config.enabled:
        return CrawlResult(
            source_id=config.source_id,
            status="disabled",
            path=None,
            sha256=None,
            config=config,
        )

    validate_config_labels(
        source_id=config.source_id,
        label_assignment=config.label_assignment,
        document_type=config.document_type,
        use_for=config.use_for,
    )

    adapter = get(config.adapter)
    refs = adapter.discover(config)
    if len(refs) != 1:
        raise ValueError(
            f"{config.adapter} discover() must return exactly one DocRef for "
            f"{config.source_id!r}, got {len(refs)}"
        )
    ref = refs[0]
    extension = _config_extension(config)
    if isinstance(ref.extras.get("extension"), str) and ref.extras["extension"].strip():
        extension = (
            ref.extras["extension"]
            if str(ref.extras["extension"]).startswith(".")
            else f".{ref.extras['extension']}"
        )
    local = content_path(root, config, extension)
    prior = config.watermark or stored_sha256(root, config, extension)

    try:
        doc = adapter.fetch(ref, config)
    except Exception as exc:
        reason = str(exc)
        log.warning("crawl fetch failed source_id=%s: %s", config.source_id, reason)
        if local.is_file() and prior:
            sync_sidecar(
                root,
                config,
                digest=prior,
                extension=extension,
                content_type="application/pdf" if extension == ".pdf" else "application/octet-stream",
            )
            return CrawlResult(
                source_id=config.source_id,
                status="unchanged",
                path=str(local),
                sha256=prior,
                config=replace(config, watermark=prior),
                reason=f"fetch failed, kept local + synced labels: {reason}",
            )
        return CrawlResult(
            source_id=config.source_id,
            status="failed",
            path=None,
            sha256=None,
            config=config,
            reason=reason,
        )

    extension = doc.extension or extension
    local = content_path(root, config, extension)
    digest = sha256_hex(doc.body)
    if prior == digest:
        sync_sidecar(
            root,
            config,
            digest=digest,
            extension=extension,
            content_type=doc.content_type,
        )
        log.info("crawl unchanged source_id=%s sha256=%s", config.source_id, digest)
        return CrawlResult(
            source_id=config.source_id,
            status="unchanged",
            path=str(local) if local.is_file() else None,
            sha256=digest,
            config=replace(config, watermark=digest),
        )

    path = write_doc(root, config, doc)
    updated = replace(config, watermark=digest)
    log.info("crawl written source_id=%s path=%s sha256=%s", config.source_id, path, digest)
    return CrawlResult(
        source_id=config.source_id,
        status="written",
        path=str(path),
        sha256=digest,
        config=updated,
    )



def crawl_many(configs: list[SourceConfig], root: Path) -> list[CrawlResult]:
    results: list[CrawlResult] = []
    for cfg in configs:
        log.info("crawl start source_id=%s endpoint=%s", cfg.source_id, cfg.endpoint)
        results.append(crawl(cfg, root))
    return results
