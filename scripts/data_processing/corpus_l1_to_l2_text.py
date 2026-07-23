#!/usr/bin/env python3
"""L1_raw → L2_text: extract clear plain text for every corpus file."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from source_ingest.preprocess_core import normalize_raw_text
from source_ingest.text_extract import extract_text

SKIP_NAMES = {".meta.json"}
CONTENT_SUFFIXES = {".pdf", ".html", ".json", ".txt", ".epub"}


def l2_path_for(l1_path: Path, l1_root: Path, l2_root: Path) -> Path:
    rel = l1_path.relative_to(l1_root)
    return l2_root / rel.with_suffix(".txt")


def iter_l1_files(l1_root: Path) -> list[Path]:
    out: list[Path] = []
    for path in sorted(l1_root.rglob("*")):
        if not path.is_file():
            continue
        if path.name.endswith(".meta.json"):
            continue
        if path.suffix.lower() not in CONTENT_SUFFIXES:
            continue
        out.append(path)
    return out


def load_l1_manifest(corpus_root: Path) -> dict[str, dict]:
    manifest_path = corpus_root / "manifest.json"
    if not manifest_path.is_file():
        return {}
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    by_path: dict[str, dict] = {}
    for row in data.get("sources", []):
        p = row.get("path", "")
        if p.startswith("L1_raw/"):
            by_path[p] = row
    return by_path


def write_l2(
    l1_path: Path,
    l2_path: Path,
    meta: dict,
) -> dict:
    raw = extract_text(l1_path)
    text = normalize_raw_text(raw)
    if len(text) < 100:
        raise ValueError(f"text too short ({len(text)} chars)")

    header_lines = [
        f"source_id: {meta.get('source_id', l1_path.stem)}",
        f"bucket: {meta.get('bucket', '')}",
        f"l1_path: {l1_path}",
    ]
    if meta.get("origin_url"):
        header_lines.append(f"origin_url: {meta['origin_url']}")
    if meta.get("publisher"):
        header_lines.append(f"publisher: {meta['publisher']}")
    if meta.get("domain_cluster"):
        header_lines.append(f"domain: {meta['domain_cluster']}")

    body = "\n".join(header_lines) + "\n\n---\n\n" + text
    l2_path.parent.mkdir(parents=True, exist_ok=True)
    l2_path.write_text(body + "\n", encoding="utf-8")
    return {
        "source_id": meta.get("source_id", l1_path.stem),
        "l1_path": str(l1_path.relative_to(REPO / "corpus")),
        "l2_path": str(l2_path.relative_to(REPO / "corpus")),
        "chars": len(text),
        "status": "ok",
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract L1_raw files to L2_text.")
    ap.add_argument("--corpus-dir", type=Path, default=REPO / "corpus")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    corpus = args.corpus_dir if args.corpus_dir.is_absolute() else REPO / args.corpus_dir
    l1_root = corpus / "L1_raw"
    l2_root = corpus / "L2_text"

    if not l1_root.is_dir():
        raise SystemExit(
            f"L1_raw not found: {l1_root}. Run: uv run python scripts/data_processing/consolidate_corpus_l1.py"
        )

    meta_by_l1 = load_l1_manifest(corpus)
    outcomes: list[dict] = []
    ok = fail = skip = 0

    for l1_path in iter_l1_files(l1_root):
        l2_path = l2_path_for(l1_path, l1_root, l2_root)
        rel_l1 = f"L1_raw/{l1_path.relative_to(l1_root).as_posix()}"
        meta = meta_by_l1.get(rel_l1, {"source_id": l1_path.stem})

        if l2_path.is_file() and not args.force:
            outcomes.append(
                {
                    "source_id": meta.get("source_id"),
                    "l2_path": str(l2_path.relative_to(corpus)),
                    "status": "skipped",
                }
            )
            skip += 1
            continue

        if args.dry_run:
            print(f"would-extract {rel_l1} → {l2_path.relative_to(corpus)}")
            ok += 1
            continue

        try:
            row = write_l2(l1_path, l2_path, meta)
            outcomes.append(row)
            print(f"ok {row['source_id']} chars={row['chars']}")
            ok += 1
        except Exception as exc:
            outcomes.append(
                {
                    "source_id": meta.get("source_id", l1_path.stem),
                    "l1_path": rel_l1,
                    "status": "failed",
                    "error": str(exc),
                }
            )
            print(f"fail {l1_path.name}: {exc}", file=sys.stderr)
            fail += 1

    if not args.dry_run:
        report = {
            "schema_version": 1,
            "pipeline_level": "L2_text",
            "data_cutoff": date.today().isoformat(),
            "stats": {"ok": ok, "failed": fail, "skipped": skip},
            "outcomes": outcomes,
        }
        (corpus / "L2_manifest.json").write_text(
            json.dumps(report, indent=2),
            encoding="utf-8",
        )

    print(f"done ok={ok} failed={fail} skipped={skip} → {l2_root}")
    if fail and ok == 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
