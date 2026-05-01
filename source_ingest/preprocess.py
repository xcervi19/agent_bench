"""CLI: raw .txt → normalized text + chunks.jsonl + manifest.json (no API keys needed)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from uuid import uuid4

from .chunk_builder import (
    build_embedding_prefix,
    iter_paragraph_spans,
    pack_into_chunks,
)
from .schemas import BookMeta, ChunkArtifact, ChunkFilters, ChunkLocation, IngestManifest


def normalize_raw_text(raw: str) -> str:
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    raw = re.sub(r"[ \t]+\n", "\n", raw)
    raw = re.sub(r"\n{3,}", "\n\n", raw)
    return raw.strip()


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
    normalized = normalize_raw_text(raw)

    out_dir: Path = args.output_dir
    if not out_dir.is_absolute():
        out_dir = repo_root / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    norm_path = out_dir / "normalized.txt"
    norm_path.write_text(normalized + "\n", encoding="utf-8")

    paragraphs = list(iter_paragraph_spans(normalized))
    packed = pack_into_chunks(
        paragraphs,
        max_chars=args.max_chars,
        overlap_chars=args.overlap,
    )

    book = BookMeta(
        title=args.book_title,
        author=args.author,
        book_slug=args.book_slug,
        language=args.language,
        isbn=args.isbn,
    )
    filters = ChunkFilters(category=args.category[:64], commodity=args.commodity, region=args.region)

    chunks_path = out_dir / "chunks.jsonl"
    total = len(packed)
    document_id = uuid4()

    with chunks_path.open("w", encoding="utf-8") as f:
        for idx, pk in enumerate(packed):
            prefix = build_embedding_prefix(
                book_title=book.title,
                author=book.author,
                part=pk.part,
                chapter_raw=pk.chapter_raw,
            )
            loc = ChunkLocation(
                part=pk.part,
                chapter_number=None,
                chapter_title=pk.chapter_raw,
                page_start=pk.page_start,
                page_end=pk.page_end,
            )
            art = ChunkArtifact(
                chunk_index=idx,
                chunk_total=total,
                content_zone=pk.content_zone,
                book=book,
                location=loc,
                filters=filters,
                prefix=prefix,
                body=pk.body,
                entities_extra={
                    "ingest_pipeline": "source_ingest.preprocess",
                    "source_file": str(args.input.resolve()),
                },
            )
            f.write(art.model_dump_json() + "\n")

    manifest = IngestManifest(
        source_path=str(args.input.resolve()),
        output_dir=str(out_dir.resolve()),
        document_id=document_id,
        book=book,
        filters=filters,
        chunk_count=total,
    )
    (out_dir / "manifest.json").write_text(
        manifest.model_dump_json(indent=2),
        encoding="utf-8",
    )

    print(f"Wrote {total} chunks → {chunks_path}")
    print(f"Manifest → {out_dir / 'manifest.json'}")
    print(f"document_id for ingest: {document_id}")


if __name__ == "__main__":
    main()
