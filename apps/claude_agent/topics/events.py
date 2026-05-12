"""Topic event bus.

Single-process design (Phase 1 of the v1 ticket): publishers (orchestrator,
stage runners) call :func:`emit` which BOTH (a) writes a row to
``topic_events`` and (b) fans out the event to in-memory subscribers via
per-topic ``asyncio.Queue`` instances. SSE consumers pull from those queues.

Durability is on Postgres; in-memory queues are best-effort live feed. SSE
clients that need a guaranteed replay path use ``?from_seq=N`` which reads
from Postgres before tailing.
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Topic, TopicEvent
from .schemas import EventOut

logger = logging.getLogger(__name__)


class EventBus:
    """In-memory fan-out for live SSE consumers.

    One instance lives on the FastAPI app state. Subscribers receive every
    event after their subscription point; they do NOT see history. For
    historical replay use ``EventBus.replay_from_db``.
    """

    def __init__(self) -> None:
        self._subscribers: dict[uuid.UUID, set[asyncio.Queue[EventOut]]] = (
            defaultdict(set)
        )
        self._lock = asyncio.Lock()

    async def subscribe(self, topic_id: uuid.UUID) -> asyncio.Queue[EventOut]:
        q: asyncio.Queue[EventOut] = asyncio.Queue(maxsize=1024)
        async with self._lock:
            self._subscribers[topic_id].add(q)
        return q

    async def unsubscribe(
        self, topic_id: uuid.UUID, q: asyncio.Queue[EventOut]
    ) -> None:
        async with self._lock:
            self._subscribers.get(topic_id, set()).discard(q)

    async def publish(self, event: EventOut) -> None:
        # Snapshot under lock; deliver outside the lock.
        async with self._lock:
            queues = list(self._subscribers.get(event.topic_id, set()))
        for q in queues:
            try:
                q.put_nowait(event)
            except asyncio.QueueFull:
                logger.warning(
                    "topic_event subscriber queue full topic_id=%s seq=%s — dropping",
                    event.topic_id,
                    event.seq,
                )


async def emit(
    session: AsyncSession,
    bus: EventBus,
    *,
    topic_id: uuid.UUID,
    event_type: str,
    payload: dict[str, Any],
    event_version: str = "1",
) -> EventOut:
    """Persist an event AND publish it to live subscribers.

    Caller is responsible for the surrounding transaction; this function
    flushes (so the DB row's id/created_at populate) but does NOT commit.
    """
    # Atomically bump topic.last_event_seq and read the new value.
    new_seq = await _bump_seq(session, topic_id)

    event = TopicEvent(
        topic_id=topic_id,
        seq=new_seq,
        event_type=event_type,
        event_version=event_version,
        payload=payload,
    )
    session.add(event)
    await session.flush()

    out = EventOut(
        seq=new_seq,
        event_type=event_type,
        event_version=event_version,
        topic_id=topic_id,
        created_at=event.created_at or datetime.now(timezone.utc),
        payload=payload,
    )
    await bus.publish(out)
    return out


async def _bump_seq(session: AsyncSession, topic_id: uuid.UUID) -> int:
    """Atomically increment ``topics.last_event_seq`` and return the new value."""
    stmt = (
        update(Topic)
        .where(Topic.id == topic_id)
        .values(last_event_seq=Topic.last_event_seq + 1)
        .returning(Topic.last_event_seq)
    )
    result = await session.execute(stmt)
    new_seq = result.scalar_one()
    return int(new_seq)


async def replay_from_db(
    session: AsyncSession,
    topic_id: uuid.UUID,
    *,
    from_seq: int = 0,
    limit: int = 1000,
) -> list[EventOut]:
    stmt = (
        select(TopicEvent)
        .where(TopicEvent.topic_id == topic_id, TopicEvent.seq > from_seq)
        .order_by(TopicEvent.seq.asc())
        .limit(limit)
    )
    rows = (await session.execute(stmt)).scalars().all()
    return [
        EventOut(
            seq=row.seq,
            event_type=row.event_type,
            event_version=row.event_version,
            topic_id=row.topic_id,
            created_at=row.created_at,
            payload=row.payload or {},
        )
        for row in rows
    ]
