"""The public face of a shared topic (#40): read, and nothing else.

Every other router in this service asks "who are you?" first. This one never
does — that is the point of publishing — so the safety has to come from the
shape of the module instead of from a principal:

  * **Read-only by construction.** Only `@router.get` appears below. There is no
    POST/PATCH/DELETE handler an anonymous caller could reach even in principle,
    so no anonymous request can start a Claude run, a search, or a refresh —
    nothing here spends money. `test_public_sharing.py` asserts this over the
    router's own route table, so adding a write route breaks the build.
  * **Published rows only.** Every handler goes through `_published`, which
    filters on `is_public` in the query rather than loading a row and checking a
    field afterwards. A private topic 404s exactly like a nonexistent one.
  * **No event stream.** The owner API's SSE endpoint holds a DB-polling
    connection open per client; a published topic is frozen, so there would be
    nothing to stream, and an unauthenticated long-poll is a resource tap we do
    not need to open.
  * **Narrow payload.** The listing and detail views deliberately omit
    `owner_user_id`, run ids, and internal error text. What is shared is the
    research, not the plumbing or the person.

This is the one place where the anonymous-read failure of 2026-07-27 (see
`_warn_on_open_topic_api` in app.py) is intentional and scoped: it applies to
rows an owner explicitly published, and only to GETs.
"""

from __future__ import annotations

import uuid
from datetime import timezone
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import ClaudeAgentSettings, get_settings
from .db import session_scope
from .models import Topic, TopicRefreshDelta
from .refresh import list_deltas
from .serving import artifact_response

router = APIRouter(prefix="/v1/public/topics", tags=["public"])

MAX_LIMIT = 100


async def _published(s: AsyncSession, topic_id: uuid.UUID) -> Topic:
    """Load a published topic, or 404.

    The `is_public` predicate lives in the WHERE clause on purpose: there is no
    moment in this function where an unpublished row is in hand and one missing
    `if` would hand it to a stranger.
    """
    row = (await s.execute(
        select(Topic).where(Topic.id == topic_id, Topic.is_public.is_(True))
    )).scalar_one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail="topic not found")
    return row


def _payload(row: Topic) -> dict[str, Any]:
    """What a stranger is allowed to know about a shared topic."""
    return {
        "id": str(row.id),
        "topic": row.topic,
        "state": row.state,
        "published_at": (
            row.published_at.astimezone(timezone.utc).isoformat()
            if row.published_at is not None
            else None
        ),
        "created_at": row.created_at.astimezone(timezone.utc).isoformat(),
        "updated_at": row.updated_at.astimezone(timezone.utc).isoformat(),
        # Read-only, always: it is stated in the payload so a client does not
        # have to infer it from the absence of `available_actions`.
        "read_only": True,
        "has_plan": row.plan_run_id is not None,
        "has_report": row.deliver_run_id is not None,
    }


@router.get("")
async def list_public_topics(limit: int = 50, offset: int = 0, q: str | None = None) -> dict[str, Any]:
    """Everything anyone has published, newest share first.

    `q` is a case-insensitive substring match on the topic text — enough to find
    a shared topic without standing up a search index.
    """
    if limit < 1 or limit > MAX_LIMIT:
        raise HTTPException(status_code=422, detail=f"limit must be between 1 and {MAX_LIMIT}")
    if offset < 0:
        raise HTTPException(status_code=422, detail="offset must be >= 0")

    async with session_scope() as s:
        stmt = select(Topic).where(Topic.is_public.is_(True))
        if q:
            stmt = stmt.where(Topic.topic.ilike(f"%{q}%"))
        rows = (await s.execute(
            stmt.order_by(Topic.published_at.desc(), Topic.created_at.desc())
            .offset(offset)
            .limit(limit)
        )).scalars().all()
        items = [_payload(row) for row in rows]

    return {"items": items, "count": len(items), "limit": limit, "offset": offset, "q": q}


@router.get("/{topic_id}")
async def get_public_topic(topic_id: uuid.UUID) -> dict[str, Any]:
    async with session_scope() as s:
        return _payload(await _published(s, topic_id))


# ---- artifacts -------------------------------------------------------------
#
# Same files the owner sees, same helper, no auth. A published topic is frozen,
# so these bytes cannot change while someone is reading them.


@router.get("/{topic_id}/parsed")
async def get_public_parsed(
    topic_id: uuid.UUID, settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]
):
    async with session_scope() as s:
        row = await _published(s, topic_id)
    return artifact_response(settings, row.topic_id_hash, row.plan_run_id, "parsed.json")


@router.get("/{topic_id}/intro")
async def get_public_intro(
    topic_id: uuid.UUID, settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]
):
    async with session_scope() as s:
        row = await _published(s, topic_id)
    return artifact_response(settings, row.topic_id_hash, row.plan_run_id, "intro.json")


@router.get("/{topic_id}/intro.md")
async def get_public_intro_md(
    topic_id: uuid.UUID, settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]
):
    async with session_scope() as s:
        row = await _published(s, topic_id)
    return artifact_response(settings, row.topic_id_hash, row.plan_run_id, "intro.md")


@router.get("/{topic_id}/news")
async def get_public_news(
    topic_id: uuid.UUID, settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]
):
    async with session_scope() as s:
        row = await _published(s, topic_id)
    return artifact_response(settings, row.topic_id_hash, row.deliver_run_id, "news.json")


@router.get("/{topic_id}/report")
async def get_public_report(
    topic_id: uuid.UUID, settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]
):
    async with session_scope() as s:
        row = await _published(s, topic_id)
    return artifact_response(settings, row.topic_id_hash, row.deliver_run_id, "report.json")


@router.get("/{topic_id}/report.md")
async def get_public_report_md(
    topic_id: uuid.UUID, settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]
):
    async with session_scope() as s:
        row = await _published(s, topic_id)
    return artifact_response(settings, row.topic_id_hash, row.deliver_run_id, "report.md")


# ---- refresh history -------------------------------------------------------
#
# Monitoring is switched off when a topic is published, so this is the record of
# what the topic found while it was still being watched — part of "the actual
# state with all information", and frozen like the rest of it.


@router.get("/{topic_id}/deltas")
async def list_public_deltas(topic_id: uuid.UUID, limit: int = 50) -> dict[str, Any]:
    if limit < 1 or limit > MAX_LIMIT:
        raise HTTPException(status_code=422, detail=f"limit must be between 1 and {MAX_LIMIT}")
    async with session_scope() as s:
        await _published(s, topic_id)
    items = await list_deltas(topic_id, limit=limit)
    return {"deltas": items, "count": len(items)}


async def _public_delta_run_id(topic_id: uuid.UUID, seq: int) -> tuple[str, str]:
    """(topic_id_hash, run_id) for one refresh cycle of a published topic."""
    async with session_scope() as s:
        row = await _published(s, topic_id)
        delta = (await s.execute(
            select(TopicRefreshDelta).where(
                TopicRefreshDelta.topic_id == topic_id,
                TopicRefreshDelta.seq == seq,
            )
        )).scalar_one_or_none()
        if delta is None:
            raise HTTPException(status_code=404, detail="delta not found")
        return row.topic_id_hash, delta.run_id


@router.get("/{topic_id}/deltas/{seq}")
async def get_public_delta(
    topic_id: uuid.UUID, seq: int, settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]
):
    topic_hash, run_id = await _public_delta_run_id(topic_id, seq)
    return artifact_response(settings, topic_hash, run_id, "delta.json")


@router.get("/{topic_id}/deltas/{seq}/news")
async def get_public_delta_news(
    topic_id: uuid.UUID, seq: int, settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]
):
    topic_hash, run_id = await _public_delta_run_id(topic_id, seq)
    return artifact_response(settings, topic_hash, run_id, "news.json")


@router.get("/{topic_id}/deltas/{seq}/report")
async def get_public_delta_report(
    topic_id: uuid.UUID, seq: int, settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]
):
    topic_hash, run_id = await _public_delta_run_id(topic_id, seq)
    return artifact_response(settings, topic_hash, run_id, "report.md")
