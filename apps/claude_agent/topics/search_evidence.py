"""Capture every hit web search returns, per topic, with no verdict attached.

Quality is judged later by a separate pass, so nothing here filters, scores or
drops. Parsing is strict: if the WebSearch result shape changes, this raises
rather than silently recording nothing.

Every *call* is recorded too, not only the calls that produced hits. A search
that came back empty used to leave no trace, which made "we asked and search
returned nothing" indistinguishable from "nobody asked" — two problems with
opposite fixes. The call row also carries the domain filter, so once the
whitelist is passed as `allowed_domains` (#46) we can still tell which domains
were reachable in principle from which were never offered to search at all.
"""

import hashlib
import json
import uuid
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from .db import session_scope
from .models import SearchDocument, SearchObservation, SearchQuery

WEB_SEARCH_TOOL = "WebSearch"
LINKS_MARKER = "Links: "


@dataclass(frozen=True, slots=True)
class SearchCall:
    """One WebSearch invocation, as the agent asked for it."""

    query: str
    # None means the call carried no filter, which is not the same as an empty
    # list (a filter that allows nothing). Preserve the distinction.
    allowed_domains: list[str] | None = None
    blocked_domains: list[str] | None = None


def url_hash(url: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]


def parse_call(tool_input: dict[str, Any]) -> SearchCall:
    """Read the whole call, not just its query text."""
    return SearchCall(
        query=tool_input["query"],
        allowed_domains=_domain_list(tool_input.get("allowed_domains")),
        blocked_domains=_domain_list(tool_input.get("blocked_domains")),
    )


def _domain_list(value: Any) -> list[str] | None:
    if value is None:
        return None
    return [str(d) for d in value]


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
    topic_id: uuid.UUID, run_id: str, call: SearchCall, hits: list[dict[str, Any]]
) -> None:
    """Record the call and every hit it returned.

    Unlike the pre-#46 version this does not return early on an empty result:
    the empty search is the observation we were missing.
    """
    async with session_scope() as s:
        query_id = await _insert_query(s, topic_id, run_id, call, len(hits))
        for rank, hit in enumerate(hits, start=1):
            document_id = await _upsert_document(s, topic_id, hit)
            s.add(
                SearchObservation(
                    topic_id=topic_id,
                    document_id=document_id,
                    query_id=query_id,
                    run_id=run_id,
                    query=call.query,
                    rank=rank,
                )
            )


async def _insert_query(
    s: AsyncSession, topic_id: uuid.UUID, run_id: str, call: SearchCall, hit_count: int
) -> int:
    row = SearchQuery(
        topic_id=topic_id,
        run_id=run_id,
        query=call.query,
        allowed_domains=call.allowed_domains,
        blocked_domains=call.blocked_domains,
        hit_count=hit_count,
    )
    s.add(row)
    await s.flush()
    return row.id


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
        self._calls: dict[str, SearchCall] = {}

    def note_tool_use(self, block: dict[str, Any]) -> None:
        if block.get("name") != WEB_SEARCH_TOOL:
            return
        self._calls[block["id"]] = parse_call(block["input"])

    async def note_tool_result(self, block: dict[str, Any]) -> None:
        call = self._calls.pop(block.get("tool_use_id"), None)
        if call is None:
            return
        await record_hits(self._topic_id, self._run_id, call, parse_hits(block.get("content")))
