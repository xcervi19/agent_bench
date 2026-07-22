"""Pydantic shapes for artifact JSONL (no embeddings) and manifest."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class BookMeta(BaseModel):
    title: str
    author: str = ""
    book_slug: str
    language: str = "en"
    isbn: str | None = None
    edition: str | None = None


class ChunkLocation(BaseModel):
    part: str | None = None
    chapter_number: str | None = None
    chapter_title: str | None = None
    page_start: int | None = None
    page_end: int | None = None


class ChunkFilters(BaseModel):
    category: str = "energy_education"
    commodity: str | None = "crude_oil"
    region: str | None = None
    document_type: str | None = None
    use_for: list[str] = Field(default_factory=list)


class ChunkArtifact(BaseModel):
    """One line in chunks.jsonl — ready to inspect; ingest builds summary + DB rows."""

    schema_version: int = 1
    chunk_index: int
    chunk_total: int | None = None
    content_zone: str = "main"  # front_matter | main | toc | appendix | other

    book: BookMeta
    location: ChunkLocation
    filters: ChunkFilters = Field(default_factory=ChunkFilters)

    prefix: str = Field(description="Lead-in for embedding (chapter/source context)")
    body: str = Field(description="Chunk body only")

    entities_extra: dict[str, Any] = Field(default_factory=dict)

    @property
    def summary_for_embedding(self) -> str:
        return f"{self.prefix}\n\n{self.body}".strip()


class IngestManifest(BaseModel):
    schema_version: int = 1
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    pipeline: str = "source_ingest.preprocess"
    pipeline_version: str = "1"

    source_path: str
    output_dir: str

    document_id: UUID
    book: BookMeta
    filters: ChunkFilters
    chunk_count: int

    embedding_model: str = "text-embedding-3-small"
    embedding_dim: int = 1536
