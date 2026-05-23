from __future__ import annotations

import re
from pathlib import Path
from uuid import UUID, uuid4

from .chunk_builder import (
    build_embedding_prefix,
    iter_paragraph_spans,
    pack_into_chunks,
)


def normalize_raw_text(raw: str) -> str:
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    raw = re.sub(r"[ \t]+\n", "\n", raw)
    raw = re.sub(r"\n{3,}", "\n\n", raw)
    return raw.strip()
from .schemas import BookMeta, ChunkArtifact, ChunkFilters, ChunkLocation, IngestManifest


def write_preprocess_artifacts(
    *,
    raw_text: str,
    output_dir: Path,
    book: BookMeta,
    filters: ChunkFilters,
    source_path: str,
    pipeline: str,
    max_chars: int,
    overlap_chars: int,
    entities_extra: dict | None = None,
) -> tuple[UUID, int]:
    normalized = normalize_raw_text(raw_text)
    if len(normalized) < 200:
        raise ValueError(f"text too short after normalize ({len(normalized)} chars): {source_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "normalized.txt").write_text(normalized + "\n", encoding="utf-8")

    paragraphs = list(iter_paragraph_spans(normalized))
    packed = pack_into_chunks(
        paragraphs,
        max_chars=max_chars,
        overlap_chars=overlap_chars,
    )
    if not packed:
        raise ValueError(f"no chunks produced: {source_path}")

    document_id = uuid4()
    total = len(packed)
    extra = entities_extra or {}

    with (output_dir / "chunks.jsonl").open("w", encoding="utf-8") as f:
        for idx, pk in enumerate(packed):
            prefix = build_embedding_prefix(
                book_title=book.title,
                author=book.author,
                part=pk.part,
                chapter_raw=pk.chapter_raw,
            )
            art = ChunkArtifact(
                chunk_index=idx,
                chunk_total=total,
                content_zone=pk.content_zone,
                book=book,
                location=ChunkLocation(
                    part=pk.part,
                    chapter_number=None,
                    chapter_title=pk.chapter_raw,
                    page_start=pk.page_start,
                    page_end=pk.page_end,
                ),
                filters=filters,
                prefix=prefix,
                body=pk.body,
                entities_extra={
                    "ingest_pipeline": pipeline,
                    "source_file": source_path,
                    **extra,
                },
            )
            f.write(art.model_dump_json() + "\n")

    manifest = IngestManifest(
        pipeline=pipeline,
        source_path=source_path,
        output_dir=str(output_dir.resolve()),
        document_id=document_id,
        book=book,
        filters=filters,
        chunk_count=total,
    )
    (output_dir / "manifest.json").write_text(
        manifest.model_dump_json(indent=2),
        encoding="utf-8",
    )
    return document_id, total
