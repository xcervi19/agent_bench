"""Hand the captured corpus to the agent as files on disk.

The refresh command builds its report from search *snippets* — a sentence or two
per hit — and reaches for WebFetch only when a snippet is too thin. Meanwhile the
evidence store holds the full text of every document we managed to read, averaging
several thousand words each, and nothing consumes it.

Exporting it into the run directory closes that gap without adding a single
network request: the agent reads the article instead of guessing from a snippet,
and grounds the report in text we fetched under our own robots-respecting client
rather than in a model's summary of a page.

Only documents that actually carry text are exported. A blocked or missing
document is a fact about coverage, not something the analyst can read, and the
index records those counts so the agent knows what it is *not* seeing.
"""

from __future__ import annotations

import json
import logging
import uuid
from pathlib import Path

from sqlalchemy import select

from .db import session_scope
from .models import SearchDocument
from .search_content import STATUS_FETCHED, STATUS_THIN

logger = logging.getLogger(__name__)

# A long document is still worth handing over truncated — the opening carries the
# lede and the dateline. The cap keeps one outlier from crowding the run dir.
MAX_CHARS_PER_DOCUMENT = 40_000
TRUNCATION_NOTE = "\n\n[truncated — full text in search_documents.content]"


def _slug(url_hash: str) -> str:
    """Filenames come from url_hash, which is already sha1-derived and path-safe."""
    return "".join(c for c in url_hash if c.isalnum())[:16] or "doc"


def write_documents(rows, destination: Path, max_chars_per_document: int) -> list[dict]:
    """Write one file per document and return the index entries.

    Front matter carries the provenance the analyst needs to cite: which URL this
    text came from, when we first saw it, and by which path we read it.
    """
    destination.mkdir(parents=True, exist_ok=True)
    documents: list[dict] = []
    for url_hash, url, title, content, status, method, first_seen_at in rows:
        text = content or ""
        if len(text) > max_chars_per_document:
            text = text[:max_chars_per_document] + TRUNCATION_NOTE
        name = f"{_slug(url_hash)}.md"
        header = "\n".join(
            [
                "---",
                f"url: {url}",
                f"url_hash: {url_hash}",
                # Newlines in a title would break the front matter block.
                f"title: {' '.join((title or '').split())}",
                f"first_seen_at: {first_seen_at.isoformat() if first_seen_at else ''}",
                f"fetch_status: {status}",
                f"fetch_method: {method or ''}",
                "---",
                "",
            ]
        )
        (destination / name).write_text(header + text, encoding="utf-8")
        documents.append({
            "file": name,
            "url": url,
            "url_hash": url_hash,
            "title": title,
            "chars": len(text),
            "fetch_status": status,
        })
    return documents


async def export_evidence(
    topic_id: uuid.UUID,
    destination: Path,
    *,
    max_documents: int,
    max_chars_per_document: int = MAX_CHARS_PER_DOCUMENT,
) -> dict:
    """Write the topic's readable documents into `destination`. Returns the index.

    Newest first, so a cap keeps the most recent material rather than an arbitrary
    slice. The returned dict is also written as `index.json` beside the documents.
    """
    async with session_scope() as s:
        rows = (
            await s.execute(
                select(
                    SearchDocument.url_hash,
                    SearchDocument.url,
                    SearchDocument.title,
                    SearchDocument.content,
                    SearchDocument.fetch_status,
                    SearchDocument.fetch_method,
                    SearchDocument.first_seen_at,
                )
                .where(
                    SearchDocument.topic_id == topic_id,
                    SearchDocument.fetch_status.in_([STATUS_FETCHED, STATUS_THIN]),
                    SearchDocument.content.is_not(None),
                )
                .order_by(SearchDocument.first_seen_at.desc())
                .limit(max_documents)
            )
        ).all()

        unreadable = (
            await s.execute(
                select(SearchDocument.fetch_status, SearchDocument.domain).where(
                    SearchDocument.topic_id == topic_id,
                    SearchDocument.fetch_status.is_not(None),
                    SearchDocument.fetch_status.notin_([STATUS_FETCHED, STATUS_THIN]),
                )
            )
        ).all()

    documents = write_documents(rows, destination, max_chars_per_document)

    index = {
        "documents": documents,
        "document_count": len(documents),
        # What the agent cannot read, so it does not mistake absence for silence.
        "unreadable_count": len(unreadable),
        "unreadable_domains": sorted({domain for _, domain in unreadable}),
    }
    (destination / "index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")
    logger.info(
        "evidence.exported topic=%s documents=%s unreadable=%s",
        topic_id,
        len(documents),
        len(unreadable),
    )
    return index
