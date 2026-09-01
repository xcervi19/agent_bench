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
  * **Only finished state.** A shared topic may now be live (#50) — still
    refreshing, still monitored — so what is served has to be state that has
    *completed*: artifacts come from `public_deliver_run_id`, which advances only
    when a run has written its files, and refresh cycles appear only once their
    row reads `completed`. A reader mid-cycle sees the previous whole state, and
    never a 404 on a link that worked a minute ago.
  * **No event stream.** The owner API's SSE endpoint holds a DB-polling
    connection open per client. An unauthenticated long-poll is a resource tap we
    do not need to open: a live share is polled by its readers instead, against
    a cached single-row GET.
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

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import ClaudeAgentSettings, get_settings
from .db import session_scope
from .models import SHARE_LIVE, Topic, TopicRefreshDelta
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


# How long a reader's browser may reuse the detail payload. A live share is
# polled, so this is the difference between one DB read per reader per minute and
# one per reader per poll.
DETAIL_MAX_AGE_SECONDS = 30


def _payload(
    row: Topic, *, update_count: int | None = None, latest_seq: int | None = None
) -> dict[str, Any]:
    """What a stranger is allowed to know about a shared topic."""
    live = row.share_mode == SHARE_LIVE
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
        # Read-only, always — in both share modes. It is stated in the payload
        # so a client does not have to infer it from the absence of
        # `available_actions`.
        "read_only": True,
        "share_mode": row.share_mode,
        "frozen_at": (
            row.frozen_at.astimezone(timezone.utc).isoformat()
            if row.frozen_at is not None
            else None
        ),
        # Freshness, from the reader's side of the link (#50): is this page still
        # moving, and when did it last move? The refresh *schedule* stays private
        # — it is an owner setting and a spend decision, not a finding.
        "updates": {
            "live": live,
            "last_updated_at": (
                row.public_updated_at.astimezone(timezone.utc).isoformat()
                if row.public_updated_at is not None
                else None
            ),
            "update_count": update_count,
            "latest_seq": latest_seq,
        },
        "has_plan": row.plan_run_id is not None,
        # What the *public* view can serve, which is not the same question as
        # whether a deliver run exists — see `public_deliver_run_id`.
        "has_report": row.public_deliver_run_id is not None,
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


async def _completed_cycles(s: AsyncSession, topic_id: uuid.UUID) -> tuple[int, int | None]:
    """(how many refresh cycles finished, the newest one's seq).

    Counted over `completed` rows only, so a cycle that is running right now is
    invisible until it has something to show.
    """
    row = (await s.execute(
        select(func.count(), func.max(TopicRefreshDelta.seq)).where(
            TopicRefreshDelta.topic_id == topic_id,
            TopicRefreshDelta.status == "completed",
        )
    )).one()
    return int(row[0] or 0), row[1]


@router.get("/{topic_id}")
async def get_public_topic(topic_id: uuid.UUID, response: Response) -> dict[str, Any]:
    """The one route a live share's readers poll. Cached briefly on purpose."""
    async with session_scope() as s:
        row = await _published(s, topic_id)
        count, latest = await _completed_cycles(s, topic_id)
        payload = _payload(row, update_count=count, latest_seq=latest)
    response.headers["Cache-Control"] = f"public, max-age={DETAIL_MAX_AGE_SECONDS}"
    return payload


# ---- artifacts -------------------------------------------------------------
#
# Same helper as the owner API, no auth — but a different pointer. The owner
# reads `deliver_run_id`, which is assigned *before* a deliver run writes
# anything, because the owner should see work in flight. A reader must not: they
# would get 404s for the length of the run, and a failed run would leave a link
# already sitting in somebody's inbox permanently broken. So the public side
# reads `public_deliver_run_id`, which only ever names a run that finished.


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
    return artifact_response(settings, row.topic_id_hash, row.public_deliver_run_id, "news.json")


@router.get("/{topic_id}/report")
async def get_public_report(
    topic_id: uuid.UUID, settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]
):
    async with session_scope() as s:
        row = await _published(s, topic_id)
    return artifact_response(settings, row.topic_id_hash, row.public_deliver_run_id, "report.json")


@router.get("/{topic_id}/report.md")
async def get_public_report_md(
    topic_id: uuid.UUID, settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]
):
    async with session_scope() as s:
        row = await _published(s, topic_id)
    return artifact_response(settings, row.topic_id_hash, row.public_deliver_run_id, "report.md")


# ---- refresh history -------------------------------------------------------
#
# On a live share this is the topic still working: each completed cycle is what
# changed since the last one. On a frozen share it is the record of what the
# topic found while it was still being watched.
#
# `completed` only, in both cases. A delta row is inserted when its cycle
# *starts*, so listing anything else would advertise a report that does not
# exist yet, and hand a reader a 404 the moment they clicked it.

PUBLIC_DELTA_STATUSES = ("completed",)


@router.get("/{topic_id}/deltas")
async def list_public_deltas(topic_id: uuid.UUID, limit: int = 50) -> dict[str, Any]:
    if limit < 1 or limit > MAX_LIMIT:
        raise HTTPException(status_code=422, detail=f"limit must be between 1 and {MAX_LIMIT}")
    async with session_scope() as s:
        await _published(s, topic_id)
    items = await list_deltas(topic_id, limit=limit, statuses=PUBLIC_DELTA_STATUSES)
    return {"deltas": items, "count": len(items)}


async def _public_delta_run_id(topic_id: uuid.UUID, seq: int) -> tuple[str, str]:
    """(topic_id_hash, run_id) for one refresh cycle of a published topic."""
    async with session_scope() as s:
        row = await _published(s, topic_id)
        delta = (await s.execute(
            select(TopicRefreshDelta).where(
                TopicRefreshDelta.topic_id == topic_id,
                TopicRefreshDelta.seq == seq,
                TopicRefreshDelta.status.in_(PUBLIC_DELTA_STATUSES),
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
