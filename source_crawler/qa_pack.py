from __future__ import annotations

import json
import hashlib
import random
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

QA_AUDIT_SCHEMA_VERSION = 1
RUBRIC_ID = "pra_pricing_methodology_v1"
HEAD_LINE_COUNT = 80
SAMPLE_CHAR_COUNT = 400
SAMPLE_COUNT = 3


@dataclass(frozen=True)
class QaPackResult:
    source_id: str
    status: Literal["written", "unchanged"]


def qa_audit_path(text_root: Path) -> Path:
    return text_root / "qa_audit.json"


def _safe_id(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", value)[:120] or "source"


def qa_pack_path(txt_path: Path) -> Path:
    return txt_path.parent / "qa_pack.json"


def text_sha256_by_source(text_root: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for txt, sidecar in iter_text_pairs(text_root):
        meta = json.loads(sidecar.read_text(encoding="utf-8"))
        source_id = str(meta.get("source_id") or txt.stem)
        digest = meta.get("source_sha256")
        if not isinstance(digest, str) or not digest:
            raise ValueError(f"missing source_sha256 in {sidecar}")
        out[source_id] = digest
    return out


def load_audit_if_exists(text_root: Path) -> dict | None:
    path = qa_audit_path(text_root)
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else None


def _head_lines(text: str, count: int = HEAD_LINE_COUNT) -> list[str]:
    lines = text.splitlines()
    return lines[:count]


def _rng_seed(source_sha256: str) -> int:
    return int.from_bytes(hashlib.sha256(source_sha256.encode()).digest()[:8], "big")


def _sample_offsets(text: str, source_sha256: str, count: int = SAMPLE_COUNT) -> list[int]:
    size = SAMPLE_CHAR_COUNT
    if len(text) <= size:
        return [0]
    rng = random.Random(_rng_seed(source_sha256))
    max_start = len(text) - size
    anchors = [0, max_start // 2, max_start]
    offsets = {min(max_start, max(0, a)) for a in anchors}
    while len(offsets) < count:
        offsets.add(rng.randint(0, max_start))
    return sorted(offsets)[:count]


def _samples(text: str, source_sha256: str) -> list[dict]:
    size = SAMPLE_CHAR_COUNT
    out: list[dict] = []
    for offset in _sample_offsets(text, source_sha256):
        out.append({"offset": offset, "text": text[offset : offset + size]})
    return out


def build_qa_pack(txt_path: Path, sidecar_path: Path) -> dict:
    meta = json.loads(sidecar_path.read_text(encoding="utf-8"))
    text = txt_path.read_text(encoding="utf-8")
    source_sha256 = str(meta["source_sha256"])
    return {
        "source_id": meta.get("source_id") or txt_path.stem,
        "source_sha256": source_sha256,
        "title": meta.get("title"),
        "url": meta.get("url"),
        "publisher": meta.get("publisher"),
        "tags": meta.get("tags") or [],
        "label_assignment": meta.get("label_assignment"),
        "document_type": meta.get("document_type"),
        "use_for": meta.get("use_for") or [],
        "char_count": len(text),
        "head_lines": _head_lines(text),
        "samples": _samples(text, source_sha256),
        "rubric_id": RUBRIC_ID,
        "text_path": str(txt_path),
    }


def _pack_is_current(pack_path: Path, source_sha256: str) -> bool:
    if not pack_path.is_file():
        return False
    data = json.loads(pack_path.read_text(encoding="utf-8"))
    return data.get("source_sha256") == source_sha256


def ensure_qa_pack(txt_path: Path, sidecar_path: Path) -> QaPackResult:
    meta = json.loads(sidecar_path.read_text(encoding="utf-8"))
    source_id = str(meta.get("source_id") or txt_path.stem)
    source_sha256 = str(meta["source_sha256"])
    pack_path = qa_pack_path(txt_path)
    if _pack_is_current(pack_path, source_sha256):
        return QaPackResult(source_id=source_id, status="unchanged")
    pack = build_qa_pack(txt_path, sidecar_path)
    pack_path.write_text(json.dumps(pack, indent=2), encoding="utf-8")
    return QaPackResult(source_id=source_id, status="written")


def iter_text_pairs(text_root: Path) -> list[tuple[Path, Path]]:
    if not text_root.is_dir():
        return []
    pairs: list[tuple[Path, Path]] = []
    for folder in sorted(text_root.iterdir()):
        if not folder.is_dir():
            continue
        for txt in sorted(folder.glob("*.txt")):
            sidecar = txt.with_suffix(txt.suffix + ".meta.json")
            if sidecar.is_file():
                pairs.append((txt, sidecar))
                break
    return pairs


def _load_pack(txt: Path, sidecar: Path) -> dict:
    pack_path = qa_pack_path(txt)
    if pack_path.is_file():
        return json.loads(pack_path.read_text(encoding="utf-8"))
    return build_qa_pack(txt, sidecar)


def packs_needing_qa(text_root: Path) -> list[dict]:
    audit = load_audit_if_exists(text_root)
    audit_rows: dict[str, dict] = {}
    if audit and isinstance(audit.get("sources"), list):
        for row in audit["sources"]:
            if isinstance(row, dict) and row.get("source_id"):
                audit_rows[str(row["source_id"])] = row

    pending: list[dict] = []
    for txt, sidecar in iter_text_pairs(text_root):
        pack = _load_pack(txt, sidecar)
        sid = str(pack["source_id"])
        prior = audit_rows.get(sid)
        if prior is None:
            pending.append(pack)
            continue
        if prior.get("source_sha256") != pack["source_sha256"]:
            pending.append(pack)
            continue
        if prior.get("verdict") == "FAIL":
            pending.append(pack)
    return pending


def render_qa_prompt(packs: list[dict], *, audit_path: Path) -> str:
    lines = [
        "You are a source QA reviewer for our oil/gas pricing knowledge base.",
        "",
        "Goal: Verify crawled texts match intended document role, not wrong PDFs,",
        "marketing, paywall stubs, or unrelated content.",
        "",
        "Review ONLY the source packs below (meta, head_lines, samples).",
        "",
        "PASS: content matches pack metadata intent (methodology/spec, education, etc.).",
        "FAIL: wrong document, empty/garbled text, login page, generic news, unrelated.",
        "",
        "Labeling rules (critical):",
        "- Human already set label_assignment on each pack.",
        "- If label_assignment=human: copy document_type + use_for from the pack.",
        "  Do NOT invent or change production labels.",
        "- If label_assignment=agent: you MUST set document_type + use_for from the",
        "  controlled vocab (docs/knowledge/rag_label_vocab.md). Human deferred to you.",
        "- proposed_labels: optional suggestions for NEW vocab entries (not production).",
        "",
        f"Write the audit JSON to: {audit_path}",
        "Overwrite the file. Do not modify any other files. Do not run promote.",
        "",
        "Audit schema (strict JSON object):",
        "{",
        f'  "schema_version": {QA_AUDIT_SCHEMA_VERSION},',
        f'  "reviewed_at": "{datetime.now(timezone.utc).isoformat()}",',
        '  "sources": [',
        "    {",
        '      "source_id": "...",',
        '      "source_sha256": "...",',
        '      "verdict": "PASS|FAIL",',
        '      "confidence": "high|medium|low",',
        '      "reason": "...",',
        '      "document_type": "methodology|education|...",',
        '      "use_for": ["pricing_context"],',
        '      "proposed_labels": [],',
        '      "signals_found": [],',
        '      "red_flags": []',
        "    }",
        "  ],",
        '  "summary": {',
        '    "overall": "PASS|FAIL|PARTIAL",',
        '    "safe_to_promote": ["source_id"],',
        '    "block_promote": ["source_id"],',
        '    "notes": []',
        "  }",
        "}",
        "",
        "Rules:",
        "- Include every source pack listed below in sources[].",
        "- Copy source_sha256 exactly from each pack.",
        "- safe_to_promote may only list source_ids with verdict PASS.",
        "",
        "---",
        "",
    ]
    if not packs:
        lines.extend(
            [
                "No sources need QA review (audit matches current text hashes).",
                "If re-audit is required, delete qa_audit.json and re-run extract/qa-pack.",
                "",
            ]
        )
        return "\n".join(lines).rstrip() + "\n"

    for pack in packs:
        lines.append(f"## {pack['source_id']}")
        lines.append(f"title: {pack.get('title')}")
        lines.append(f"url: {pack.get('url')}")
        lines.append(f"publisher: {pack.get('publisher')}")
        lines.append(f"tags: {pack.get('tags')}")
        lines.append(f"label_assignment: {pack.get('label_assignment')}")
        lines.append(f"document_type: {pack.get('document_type')}")
        lines.append(f"use_for: {pack.get('use_for')}")
        lines.append(f"source_sha256: {pack.get('source_sha256')}")
        lines.append(f"char_count: {pack.get('char_count')}")
        lines.append("")
        lines.append("### head_lines")
        lines.extend(pack.get("head_lines") or [])
        lines.append("")
        lines.append("### samples")
        for i, sample in enumerate(pack.get("samples") or [], start=1):
            lines.append(f"sample_{i} offset={sample.get('offset')}")
            lines.append(sample.get("text", ""))
            lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_qa_prompt(text_root: Path) -> Path:
    audit_path = qa_audit_path(text_root)
    packs = packs_needing_qa(text_root)
    dest = text_root / "qa_prompt.md"
    dest.write_text(render_qa_prompt(packs, audit_path=audit_path), encoding="utf-8")
    return dest


def sync_qa_after_extract(text_root: Path) -> list[QaPackResult]:
    results: list[QaPackResult] = []
    for txt, sidecar in iter_text_pairs(text_root):
        results.append(ensure_qa_pack(txt, sidecar))
    write_qa_prompt(text_root)
    return results
