#!/usr/bin/env python3
"""Copy all L1 raw sources into corpus/L1_raw/ with stable names + manifest."""

from __future__ import annotations

import json
import re
import shutil
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "corpus" / "L1_raw"
WEB_SRC = REPO / "artifacts" / "rag_corpus"
if not WEB_SRC.is_dir():
    WEB_SRC = REPO / "artifacts" / "oil_rag_sources"  # legacy
DESK_SRC = REPO / "oil_gas_knowledge"
REF_SRC = REPO / "local_knowledge_sources" / "oil101.txt"
SKIP_SUFFIX = {".meta.json"}
SKIP_NAMES = {"collection_manifest.json", "sources_registry.json"}
DESK_SKIP_SUFFIX = {".epub", ".dmg", ".7z"}


def slugify(value: str, max_len: int = 100) -> str:
    s = re.sub(r"[^a-zA-Z0-9_-]+", "_", value.strip().lower()).strip("_")
    return s[:max_len] or "source"


def load_meta(path: Path) -> dict:
    sidecar = path.with_suffix(path.suffix + ".meta.json")
    if sidecar.is_file():
        return json.loads(sidecar.read_text(encoding="utf-8"))
    return {}


def copy_web() -> list[dict]:
    rows: list[dict] = []
    dest_root = OUT / "official_web"
    if not WEB_SRC.is_dir():
        return rows
    for path in sorted(WEB_SRC.rglob("*")):
        if not path.is_file():
            continue
        if path.name in SKIP_NAMES or path.name.endswith(".meta.json"):
            continue
        if path.suffix.lower() not in {".pdf", ".html", ".json"}:
            continue
        meta = load_meta(path)
        source_id = meta.get("source_id") or slugify(path.stem)
        domain = meta.get("domain") or "general"
        tier = meta.get("tier", "")
        rel = Path(f"tier_{tier}") / domain / f"{source_id}{path.suffix.lower()}"
        dest = dest_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
        sidecar = path.with_suffix(path.suffix + ".meta.json")
        if sidecar.is_file():
            shutil.copy2(sidecar, dest.with_suffix(dest.suffix + ".meta.json"))
        rows.append(
            {
                "layer": "L1_raw",
                "bucket": "official_web",
                "source_id": source_id,
                "path": str(dest.relative_to(REPO / "corpus")),
                "origin_url": meta.get("url"),
                "publisher": meta.get("publisher"),
                "domain_cluster": domain,
                "tier": tier,
            }
        )
    return rows


def copy_desk() -> list[dict]:
    rows: list[dict] = []
    dest_root = OUT / "licensed_books"
    dest_root.mkdir(parents=True, exist_ok=True)
    if not DESK_SRC.is_dir():
        return rows
    for path in sorted(DESK_SRC.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() in DESK_SKIP_SUFFIX:
            continue
        if path.suffix.lower() not in {".pdf", ".txt"}:
            continue
        if "oil 101" in path.name.lower() and path.suffix.lower() == ".pdf":
            continue
        slug = slugify(path.stem)
        dest = dest_root / f"{slug}{path.suffix.lower()}"
        shutil.copy2(path, dest)
        rows.append(
            {
                "layer": "L1_raw",
                "bucket": "licensed_books",
                "source_id": slug,
                "path": str(dest.relative_to(REPO / "corpus")),
                "origin_url": None,
                "publisher": "local",
                "domain_cluster": "desk",
                "tier": None,
            }
        )
    return rows


def copy_reference() -> list[dict]:
    rows: list[dict] = []
    dest_root = OUT / "reference"
    dest_root.mkdir(parents=True, exist_ok=True)
    if not REF_SRC.is_file():
        return rows
    dest = dest_root / "oil101.txt"
    shutil.copy2(REF_SRC, dest)
    rows.append(
        {
            "layer": "L1_raw",
            "bucket": "reference",
            "source_id": "oil101",
            "path": str(dest.relative_to(REPO / "corpus")),
            "origin_url": "local_knowledge_sources/oil101.txt",
            "publisher": "Morgan Downey",
            "domain_cluster": "trading_mechanics",
            "tier": 1,
        }
    )
    return rows


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    rows = copy_web() + copy_desk() + copy_reference()
    manifest = {
        "schema_version": 1,
        "pipeline_level": "L1_raw",
        "data_cutoff": date.today().isoformat(),
        "file_count": len(rows),
        "sources": rows,
    }
    (REPO / "corpus" / "manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    print(f"L1_raw files: {len(rows)}")
    print(f"→ {OUT}")


if __name__ == "__main__":
    main()
