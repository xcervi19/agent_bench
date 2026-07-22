from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from .inventory import iter_content_files, load_sidecar
from .labels import LabelError, resolve_promote_labels


@dataclass(frozen=True)
class PromoteResult:
    source_id: str
    status: Literal["promoted", "unchanged", "skipped"]
    path: str | None
    reason: str | None = None


def _safe_id(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", value)[:120] or "source"


def _safe_segment(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", value)[:64] or "unknown"


def _kb_dest(kb_root: Path, meta: dict, content_path: Path) -> Path:
    """rag_corpus/{document_type}/tier_{n}/{domain}/{source_id}.ext"""
    source_id = _safe_id(str(meta.get("source_id") or content_path.stem))
    tier = int(meta.get("tier", 2))
    domain = _safe_segment(str(meta.get("domain") or "trading_mechanics"))
    doc_type = _safe_segment(str(meta.get("document_type") or "untyped"))
    return (
        kb_root
        / doc_type
        / f"tier_{tier}"
        / domain
        / f"{source_id}{content_path.suffix.lower()}"
    )


def _should_promote(meta: dict, source_ids: set[str] | None) -> bool:
    source_id = str(meta.get("source_id") or "")
    if source_ids is not None:
        return source_id in source_ids
    return meta.get("promote") is True


def promote_one(
    content_path: Path,
    kb_root: Path,
    *,
    source_ids: set[str] | None = None,
    audit_row: dict | None = None,
    label_overrides: dict | None = None,
) -> PromoteResult:
    meta = load_sidecar(content_path)
    source_id = str(meta.get("source_id") or content_path.stem)
    if not _should_promote(meta, source_ids):
        return PromoteResult(
            source_id=source_id,
            status="skipped",
            path=None,
            reason="promote gate closed",
        )

    try:
        labels = label_overrides or resolve_promote_labels(meta, audit_row=audit_row)
    except LabelError as exc:
        return PromoteResult(
            source_id=source_id,
            status="skipped",
            path=None,
            reason=str(exc),
        )

    promoted_meta = {**meta, **labels, "promoted": True}
    dest = _kb_dest(kb_root, promoted_meta, content_path)
    dest_sidecar = dest.with_suffix(dest.suffix + ".meta.json")
    digest = meta.get("sha256")
    if (
        isinstance(digest, str)
        and digest
        and dest.is_file()
        and dest_sidecar.is_file()
    ):
        existing = json.loads(dest_sidecar.read_text(encoding="utf-8"))
        if (
            existing.get("sha256") == digest
            and existing.get("document_type") == promoted_meta.get("document_type")
            and existing.get("use_for") == promoted_meta.get("use_for")
        ):
            return PromoteResult(
                source_id=source_id,
                status="unchanged",
                path=str(dest),
            )

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(content_path, dest)
    dest_sidecar.write_text(json.dumps(promoted_meta, indent=2), encoding="utf-8")
    return PromoteResult(
        source_id=source_id,
        status="promoted",
        path=str(dest),
    )


def promote_all(
    collected_root: Path,
    kb_root: Path,
    *,
    source_ids: set[str] | None = None,
    audit_by_source: dict[str, dict] | None = None,
) -> list[PromoteResult]:
    results: list[PromoteResult] = []
    for path in iter_content_files(collected_root):
        meta = load_sidecar(path)
        source_id = str(meta.get("source_id") or path.stem)
        row = (audit_by_source or {}).get(source_id)
        results.append(
            promote_one(path, kb_root, source_ids=source_ids, audit_row=row)
        )
    if source_ids is not None:
        seen = {r.source_id for r in results}
        missing = source_ids - seen
        if missing:
            raise FileNotFoundError(f"source_id not in collected: {sorted(missing)}")
    return results


def plan_promote(
    collected_root: Path,
    *,
    source_ids: set[str] | None = None,
) -> list[dict]:
    rows: list[dict] = []
    for path in iter_content_files(collected_root):
        meta = load_sidecar(path)
        rows.append(
            {
                "source_id": meta.get("source_id"),
                "promote": meta.get("promote"),
                "would_promote": _should_promote(meta, source_ids),
                "path": str(path),
            }
        )
    return rows
