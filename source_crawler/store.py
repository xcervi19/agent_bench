from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from .labels import validate_config_labels
from .models import DownloadedDoc, SourceConfig


def sha256_hex(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def _safe_id(source_id: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", source_id)[:120] or "source"


def source_dir(root: Path, config: SourceConfig) -> Path:
    return root / _safe_id(config.source_id)


def content_path(root: Path, config: SourceConfig, extension: str = ".pdf") -> Path:
    return source_dir(root, config) / f"{_safe_id(config.source_id)}{extension}"


def stored_sha256(root: Path, config: SourceConfig, extension: str = ".pdf") -> str | None:
    dest = content_path(root, config, extension)
    sidecar = dest.with_suffix(dest.suffix + ".meta.json")
    if sidecar.is_file():
        data = json.loads(sidecar.read_text(encoding="utf-8"))
        digest = data.get("sha256")
        if isinstance(digest, str) and digest:
            return digest
    if dest.is_file():
        return sha256_hex(dest.read_bytes())
    return None


def build_meta(
    config: SourceConfig,
    *,
    url: str,
    content_type: str,
    digest: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    validate_config_labels(
        source_id=config.source_id,
        label_assignment=config.label_assignment,
        document_type=config.document_type,
        use_for=config.use_for,
    )
    meta: dict[str, Any] = dict(extra or {})
    meta.update(
        {
            "source_id": config.source_id,
            "title": config.title or meta.get("title") or config.source_id,
            "url": url,
            "publisher": config.publisher or meta.get("publisher") or "",
            "tier": config.tier,
            "domain": config.domain,
            "commodity": config.commodity,
            "region": config.region,
            "tags": list(config.tags),
            "label_assignment": config.label_assignment,
            "document_type": config.document_type,
            "use_for": list(config.use_for),
            "promote": config.promote,
            "content_type": content_type,
            "sha256": digest,
        }
    )
    return meta


def write_doc(root: Path, config: SourceConfig, doc: DownloadedDoc) -> Path:
    digest = sha256_hex(doc.body)
    out_dir = source_dir(root, config)
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = content_path(root, config, doc.extension)
    dest.write_bytes(doc.body)
    meta = build_meta(
        config,
        url=doc.ref.url,
        content_type=doc.content_type,
        digest=digest,
        extra=doc.meta,
    )
    sidecar = dest.with_suffix(dest.suffix + ".meta.json")
    sidecar.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return dest


def sync_sidecar(
    root: Path,
    config: SourceConfig,
    *,
    digest: str,
    extension: str,
    content_type: str,
) -> Path:
    dest = content_path(root, config, extension)
    if not dest.is_file():
        raise FileNotFoundError(f"content missing for sidecar sync: {dest}")
    sidecar = dest.with_suffix(dest.suffix + ".meta.json")
    meta = build_meta(
        config,
        url=config.endpoint,
        content_type=content_type,
        digest=digest,
    )
    sidecar.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return sidecar
