"""Capture every hit web search returns, per topic, with no verdict attached.

Quality is judged later by a separate pass, so nothing here filters, scores or
drops. Parsing is strict: if the WebSearch result shape changes, this raises
rather than silently recording nothing.
"""

import hashlib
import json
import uuid
from typing import Any
from urllib.parse import urlparse

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from .db import session_scope
from .models import SearchDocument, SearchObservation

WEB_SEARCH_TOOL = "WebSearch"
LINKS_MARKER = "Links: "


def url_hash(url: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]


def parse_hits(content: Any) -> list[dict[str, Any]]:
    text = _result_text(content)
    marker = text.find(LINKS_MARKER)
    if marker < 0:
        return []
    links, _ = json.JSONDecoder().raw_decode(text[marker + len(LINKS_MARKER):])
    return [link for link in links if link.get("url")]


def _result_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    return "".join(block["text"] for block in content if block.get("type") == "text")


async def record_hits(
    topic_id: uuid.UUID, run_id: str, query: str, hits: list[dict[str, Any]]
) -> None:
    if not hits:
        return
    async with session_scope() as s:
        for rank, hit in enumerate(hits, start=1):
            document_id = await _upsert_document(s, topic_id, hit)
            s.add(
                SearchObservation(
                    topic_id=topic_id,
                    document_id=document_id,
                    run_id=run_id,
                    query=query,
                    rank=rank,
                )
            )


async def _upsert_document(s: AsyncSession, topic_id: uuid.UUID, hit: dict[str, Any]) -> int:
    url = hit["url"]
    stmt = (
        insert(SearchDocument)
        .values(
            topic_id=topic_id,
            url=url,
            url_hash=url_hash(url),
            domain=urlparse(url).netloc,
            title=hit.get("title"),
        )
        .on_conflict_do_update(
            constraint="uq_search_documents_topic_url",
            set_={"last_seen_at": func.now()},
        )
        .returning(SearchDocument.id)
    )
    return (await s.execute(stmt)).scalar_one()


class SearchEvidenceRecorder:
    """Correlates WebSearch tool_use with its tool_result across an agent stream."""

    def __init__(self, topic_id: uuid.UUID, run_id: str) -> None:
        self._topic_id = topic_id
        self._run_id = run_id
        self._queries: dict[str, str] = {}

    def note_tool_use(self, block: dict[str, Any]) -> None:
        if block.get("name") != WEB_SEARCH_TOOL:
            return
        self._queries[block["id"]] = block["input"]["query"]

    async def note_tool_result(self, block: dict[str, Any]) -> None:
        query = self._queries.pop(block.get("tool_use_id"), None)
        if query is None:
            return
        await record_hits(self._topic_id, self._run_id, query, parse_hits(block.get("content")))
