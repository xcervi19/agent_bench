from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from .inventory import iter_content_files, load_sidecar
from .labels import LabelError, resolve_promote_labels
from .promote import promote_all
from .qa_pack import QA_AUDIT_SCHEMA_VERSION, text_sha256_by_source

ApplyStatus = Literal["promoted", "unchanged", "skipped", "blocked", "planned"]


@dataclass(frozen=True)
class ApplyQaResult:
    source_id: str
    status: ApplyStatus
    path: str | None = None
    reason: str | None = None


def load_audit(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"qa audit not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"qa audit is not a JSON object: {path}")
    version = data.get("schema_version")
    if version != QA_AUDIT_SCHEMA_VERSION:
        raise ValueError(
            f"unsupported qa audit schema_version={version!r}, "
            f"expected {QA_AUDIT_SCHEMA_VERSION}"
        )
    if "sources" not in data or "summary" not in data:
        raise ValueError(f"qa audit missing sources or summary: {path}")
    return data


def _audit_by_source(audit: dict) -> dict[str, dict]:
    rows = audit.get("sources")
    if not isinstance(rows, list):
        raise ValueError("qa audit sources must be a list")
    out: dict[str, dict] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("qa audit source row must be an object")
        source_id = row.get("source_id")
        if not source_id:
            raise ValueError("qa audit source row missing source_id")
        out[str(source_id)] = row
    return out


def resolve_promote_ids(
    audit: dict,
    text_root: Path,
    *,
    collected_root: Path | None = None,
) -> tuple[set[str], list[ApplyQaResult]]:
    audit_rows = _audit_by_source(audit)
    summary = audit.get("summary")
    if not isinstance(summary, dict):
        raise ValueError("qa audit summary must be an object")
    safe = summary.get("safe_to_promote")
    if not isinstance(safe, list):
        raise ValueError("qa audit summary.safe_to_promote must be a list")

    current_hashes = text_sha256_by_source(text_root)
    collected_meta = _collected_meta_by_source(collected_root) if collected_root else {}
    promote_ids: set[str] = set()
    details: list[ApplyQaResult] = []

    for source_id in safe:
        sid = str(source_id)
        row = audit_rows.get(sid)
        if row is None:
            details.append(
                ApplyQaResult(sid, "blocked", reason="missing sources[] row")
            )
            continue
        if row.get("verdict") != "PASS":
            details.append(
                ApplyQaResult(sid, "blocked", reason=f"verdict={row.get('verdict')!r}")
            )
            continue
        audit_hash = row.get("source_sha256")
        current_hash = current_hashes.get(sid)
        if not current_hash:
            details.append(
                ApplyQaResult(sid, "blocked", reason="source not in collected_text")
            )
            continue
        if audit_hash != current_hash:
            details.append(
                ApplyQaResult(
                    sid,
                    "blocked",
                    reason="source_sha256 mismatch (stale audit)",
                )
            )
            continue
        if collected_meta:
            meta = collected_meta.get(sid)
            if meta is None:
                details.append(
                    ApplyQaResult(sid, "blocked", reason="source not in collected/")
                )
                continue
            try:
                resolve_promote_labels(meta, audit_row=row)
            except LabelError as exc:
                details.append(ApplyQaResult(sid, "blocked", reason=str(exc)))
                continue
        promote_ids.add(sid)
        details.append(ApplyQaResult(sid, "planned"))

    block = summary.get("block_promote") or []
    if isinstance(block, list):
        for source_id in block:
            sid = str(source_id)
            if sid in promote_ids:
                promote_ids.discard(sid)
                details.append(
                    ApplyQaResult(sid, "blocked", reason="listed in block_promote")
                )

    return promote_ids, details


def _collected_meta_by_source(collected_root: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for path in iter_content_files(collected_root):
        meta = load_sidecar(path)
        sid = str(meta.get("source_id") or path.stem)
        out[sid] = meta
    return out


def apply_qa(
    audit_path: Path,
    collected_root: Path,
    kb_root: Path,
    text_root: Path,
    *,
    dry_run: bool = False,
) -> list[ApplyQaResult]:
    audit = load_audit(audit_path)
    promote_ids, details = resolve_promote_ids(
        audit, text_root, collected_root=collected_root
    )
    if dry_run:
        return details

    if not promote_ids:
        return details

    validate_collected_hashes(promote_ids, collected_root, text_root)
    audit_rows = _audit_by_source(audit)
    promote_results = promote_all(
        collected_root,
        kb_root,
        source_ids=promote_ids,
        audit_by_source=audit_rows,
    )
    by_id = {r.source_id: r for r in promote_results}
    merged: list[ApplyQaResult] = []
    for item in details:
        if item.status != "planned":
            merged.append(item)
            continue
        pr = by_id.get(item.source_id)
        if pr is None:
            merged.append(
                ApplyQaResult(item.source_id, "blocked", reason="not in collected/")
            )
            continue
        status: ApplyStatus
        if pr.status == "skipped" and pr.reason:
            status = "blocked"
        else:
            status = pr.status  # type: ignore[assignment]
        merged.append(
            ApplyQaResult(
                source_id=item.source_id,
                status=status,
                path=pr.path,
                reason=pr.reason,
            )
        )
    return merged


def validate_collected_hashes(
    promote_ids: set[str],
    collected_root: Path,
    text_root: Path,
) -> None:
    text_hashes = text_sha256_by_source(text_root)
    for path in iter_content_files(collected_root):
        meta = load_sidecar(path)
        source_id = str(meta.get("source_id") or path.stem)
        if source_id not in promote_ids:
            continue
        raw_hash = meta.get("sha256")
        text_hash = text_hashes.get(source_id)
        if raw_hash != text_hash:
            raise ValueError(
                f"collected/text hash mismatch for {source_id!r}: "
                f"raw={raw_hash!r} text={text_hash!r}"
            )
