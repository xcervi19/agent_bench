from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from source_ingest.preprocess_core import normalize_raw_text
from source_ingest.text_extract import extract_text

from .inventory import iter_content_files, load_sidecar
from .qa_pack import ensure_qa_pack
from .store import sha256_hex

MIN_CHARS = 100
EXTRACTOR = "source_ingest.text_extract"


@dataclass(frozen=True)
class ExtractResult:
    source_id: str
    status: Literal["written", "unchanged", "skipped"]
    path: str | None
    reason: str | None = None


def _safe_id(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", value)[:120] or "source"


def text_paths(text_root: Path, source_id: str) -> tuple[Path, Path]:
    safe = _safe_id(source_id)
    dest = text_root / safe / f"{safe}.txt"
    return dest, dest.with_suffix(dest.suffix + ".meta.json")


def extract_one(content_path: Path, text_root: Path) -> ExtractResult:
    meta = load_sidecar(content_path)
    source_id = str(meta.get("source_id") or content_path.stem)
    if meta.get("skip_rag") or meta.get("pipeline") == "data_feed":
        return ExtractResult(
            source_id=source_id,
            status="skipped",
            path=None,
            reason="data_feed / skip_rag",
        )
    if content_path.suffix.lower() in {".zip", ".csv", ".xlsx", ".xls"}:
        return ExtractResult(
            source_id=source_id,
            status="skipped",
            path=None,
            reason=f"non-text artifact ({content_path.suffix})",
        )

    source_digest = meta.get("sha256")
    if not isinstance(source_digest, str) or not source_digest:
        source_digest = sha256_hex(content_path.read_bytes())

    dest, dest_sidecar = text_paths(text_root, source_id)
    if dest.is_file() and dest_sidecar.is_file():
        existing = json.loads(dest_sidecar.read_text(encoding="utf-8"))
        if existing.get("source_sha256") == source_digest:
            ensure_qa_pack(dest, dest_sidecar)
            return ExtractResult(
                source_id=source_id,
                status="unchanged",
                path=str(dest),
            )

    text = normalize_raw_text(extract_text(content_path))
    if len(text) < MIN_CHARS:
        raise ValueError(
            f"extracted text too short ({len(text)} chars) for {content_path}"
        )

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text + "\n", encoding="utf-8")
    out_meta = {
        "source_id": source_id,
        "title": meta.get("title") or source_id,
        "url": meta.get("url"),
        "publisher": meta.get("publisher"),
        "tier": meta.get("tier"),
        "domain": meta.get("domain"),
        "commodity": meta.get("commodity"),
        "region": meta.get("region"),
        "tags": meta.get("tags") or [],
        "label_assignment": meta.get("label_assignment"),
        "document_type": meta.get("document_type"),
        "use_for": meta.get("use_for") or [],
        "source_path": str(content_path),
        "source_sha256": source_digest,
        "extractor": EXTRACTOR,
        "char_count": len(text),
        "layer": "collected_text",
    }
    dest_sidecar.write_text(json.dumps(out_meta, indent=2), encoding="utf-8")
    ensure_qa_pack(dest, dest_sidecar)
    return ExtractResult(
        source_id=source_id,
        status="written",
        path=str(dest),
    )


def extract_all(
    collected_root: Path,
    text_root: Path,
    *,
    source_ids: set[str] | None = None,
) -> list[ExtractResult]:
    results: list[ExtractResult] = []
    for path in iter_content_files(collected_root):
        meta = load_sidecar(path)
        source_id = str(meta.get("source_id") or path.stem)
        if source_ids is not None and source_id not in source_ids:
            results.append(
                ExtractResult(
                    source_id=source_id,
                    status="skipped",
                    path=None,
                    reason="not in --source-id filter",
                )
            )
            continue
        results.append(extract_one(path, text_root))
    if source_ids is not None:
        found = {r.source_id for r in results}
        missing = source_ids - found
        if missing:
            raise FileNotFoundError(f"source_id not in collected: {sorted(missing)}")
    from .qa_pack import write_qa_prompt

    write_qa_prompt(text_root)
    return results
