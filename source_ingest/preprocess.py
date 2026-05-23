"""CLI: raw .txt → normalized text + chunks.jsonl + manifest.json (no API keys needed)."""

from __future__ import annotations

import argparse
from pathlib import Path

from .preprocess_core import write_preprocess_artifacts
from .schemas import BookMeta, ChunkFilters


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser(description="Preprocess book .txt → JSONL artifacts (no embeddings).")
    ap.add_argument("--input", "-i", type=Path, required=True, help="Path to source .txt")
    ap.add_argument("--output-dir", "-o", type=Path, required=True, help="e.g. artifacts/oil101_run1")
    ap.add_argument("--book-title", default="Oil 101")
    ap.add_argument("--author", default="Morgan Downey")
    ap.add_argument("--book-slug", default="oil101", help="Stable id for this source")
    ap.add_argument("--language", default="en")
    ap.add_argument("--isbn", default=None)
    ap.add_argument("--category", default="energy_education", help="events.category (max 64 chars)")
    ap.add_argument("--commodity", default="crude_oil")
    ap.add_argument("--region", default=None)
    ap.add_argument("--max-chars", type=int, default=1100)
    ap.add_argument("--overlap", type=int, default=160)
    args = ap.parse_args()

    raw = args.input.read_text(encoding="utf-8", errors="replace")

    out_dir: Path = args.output_dir
    if not out_dir.is_absolute():
        out_dir = repo_root / out_dir

    book = BookMeta(
        title=args.book_title,
        author=args.author,
        book_slug=args.book_slug,
        language=args.language,
        isbn=args.isbn,
    )
    filters = ChunkFilters(category=args.category[:64], commodity=args.commodity, region=args.region)

    document_id, total = write_preprocess_artifacts(
        raw_text=raw,
        output_dir=out_dir,
        book=book,
        filters=filters,
        source_path=str(args.input.resolve()),
        pipeline="source_ingest.preprocess",
        max_chars=args.max_chars,
        overlap_chars=args.overlap,
    )

    print(f"Wrote {total} chunks → {out_dir / 'chunks.jsonl'}")
    print(f"Manifest → {out_dir / 'manifest.json'}")
    print(f"document_id for ingest: {document_id}")


if __name__ == "__main__":
    main()
