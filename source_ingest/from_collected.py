from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from uuid import UUID

from .preprocess_core import write_preprocess_artifacts
from .schemas import BookMeta, ChunkFilters
from .text_extract import extract_text

SKIP_NAMES = frozenset({"collection_manifest.json", "sources_registry.json"})
CONTENT_SUFFIXES = {".pdf", ".html", ".json", ".txt"}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def slugify(value: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_-]+", "_", value.strip().lower())
    return s[:120] or "source"


def load_sidecar(path: Path) -> dict:
    sidecar = path.with_suffix(path.suffix + ".meta.json")
    if not sidecar.is_file():
        return {}
    return json.loads(sidecar.read_text(encoding="utf-8"))


def category_from_meta(meta: dict) -> str:
    domain = meta.get("domain") or "energy"
    return str(domain).replace("-", "_")[:64]


def iter_source_files(sources_dir: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(sources_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.name in SKIP_NAMES:
            continue
        if path.name.endswith(".meta.json"):
            continue
        if path.suffix.lower() not in CONTENT_SUFFIXES:
            continue
        files.append(path)
    return files


def book_from_path(path: Path, meta: dict, slug: str) -> BookMeta:
    title = meta.get("title") or path.stem
    author = meta.get("publisher") or ""
    return BookMeta(title=str(title)[:512], author=str(author)[:256], book_slug=slug)


def filters_from_meta(meta: dict) -> ChunkFilters:
    use_for = meta.get("use_for") or []
    if isinstance(use_for, str):
        use_for = [use_for]
    return ChunkFilters(
        category=category_from_meta(meta),
        commodity=meta.get("commodity") or "crude_oil",
        region=meta.get("region"),
        document_type=meta.get("document_type"),
        use_for=[str(u) for u in use_for],
    )


def already_chunked(chunks_dir: Path, slug: str) -> bool:
    return (chunks_dir / slug / "manifest.json").is_file()


def run_ingest(artifact_dir: Path, tenant_id: UUID) -> None:
    cmd = [
        sys.executable,
        "-m",
        "source_ingest.ingest",
        "--artifact-dir",
        str(artifact_dir),
        "--tenant-id",
        str(tenant_id),
    ]
    subprocess.run(cmd, check=True, cwd=str(repo_root()))


def main() -> None:
    root = repo_root()
    ap = argparse.ArgumentParser(
        description="Extract + chunk every file under a sources folder.",
    )
    ap.add_argument(
        "--sources-dir",
        type=Path,
        default=root / "artifacts/rag_corpus",
    )
    ap.add_argument(
        "--chunks-dir",
        type=Path,
        default=root / "artifacts/chunks",
    )
    ap.add_argument("--skip-slug", action="append", default=["oil101"])
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--max-chars", type=int, default=1100)
    ap.add_argument("--overlap", type=int, default=160)
    ap.add_argument("--ingest", action="store_true")
    ap.add_argument("--tenant-id", type=UUID, default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    sources_dir = args.sources_dir if args.sources_dir.is_absolute() else root / args.sources_dir
    chunks_dir = args.chunks_dir if args.chunks_dir.is_absolute() else root / args.chunks_dir

    if not sources_dir.is_dir():
        raise SystemExit(f"sources dir not found: {sources_dir}")
    if args.ingest and args.tenant_id is None:
        raise SystemExit("--tenant-id required with --ingest")

    skip_slugs = {slugify(s) for s in args.skip_slug}
    files = iter_source_files(sources_dir)

    ok = 0
    skipped = 0
    failed = 0

    for path in files:
        meta = load_sidecar(path)
        slug = slugify(meta.get("source_id") or path.stem)

        if slug in skip_slugs:
            print(f"skip-slug {slug} ← {path.name}")
            skipped += 1
            continue

        out_dir = chunks_dir / slug
        if already_chunked(chunks_dir, slug) and not args.force:
            print(f"skip-existing {slug}")
            skipped += 1
            continue

        if args.dry_run:
            print(f"would-process {slug} ← {path}")
            ok += 1
            continue

        try:
            text = extract_text(path)
            book = book_from_path(path, meta, slug)
            filters = filters_from_meta(meta)
            doc_id, n_chunks = write_preprocess_artifacts(
                raw_text=text,
                output_dir=out_dir,
                book=book,
                filters=filters,
                source_path=str(path.resolve()),
                pipeline="source_ingest.from_collected",
                max_chars=args.max_chars,
                overlap_chars=args.overlap,
                entities_extra={
                    "collector_tier": meta.get("tier"),
                    "collector_tags": meta.get("tags"),
                    "source_url": meta.get("url"),
                    "label_assignment": meta.get("label_assignment"),
                    "document_type": meta.get("document_type"),
                    "use_for": meta.get("use_for") or [],
                },
            )
            print(f"ok {slug} chunks={n_chunks} document_id={doc_id}")
            ok += 1
        except Exception as exc:
            print(f"fail {slug} ← {path.name}: {exc}", file=sys.stderr)
            failed += 1

    print(f"done ok={ok} skipped={skipped} failed={failed} → {chunks_dir}")

    if args.ingest and not args.dry_run and ok > 0:
        for child in sorted(chunks_dir.iterdir()):
            if not (child / "manifest.json").is_file():
                continue
            slug = child.name
            if slug in skip_slugs:
                continue
            print(f"ingest {slug}")
            run_ingest(child, args.tenant_id)

    if failed and ok == 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
