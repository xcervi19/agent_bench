"""Webhook delivery (B2B integrations).

For each event published, we look up active webhook subscribers and POST the
event payload, signed with HMAC-SHA256 if a ``secret`` is configured. Delivery
is best-effort with a small in-process retry budget (no Redis queue in v1);
on persistent failure, we increment ``delivery_failures`` and disable the
subscription past a small threshold.
"""

from __future__ import annotations

import asyncio
import hashlib
import hmac
import json
import logging
import uuid
from datetime import datetime, timezone

import httpx
from sqlalchemy import select, update

from ..config import ClaudeAgentSettings
from .db import session_scope
from .models import TopicWebhook
from .schemas import EventOut

logger = logging.getLogger(__name__)


async def schedule_webhook_delivery(
    topic_id: uuid.UUID,
    event: EventOut,
    settings: ClaudeAgentSettings,
) -> None:
    """Find subscribers and deliver. Errors are logged, never raised."""
    try:
        subs = await _load_active_subscribers(topic_id, event.event_type)
    except Exception:
        logger.exception("webhook_delivery: failed to load subscribers")
        return

    if not subs:
        return

    body = _serialize_event(event)
    body_bytes = body.encode("utf-8")

    async with httpx.AsyncClient(
        timeout=settings.webhook_request_timeout_sec
    ) as client:
        for sub in subs:
            await _deliver_with_retries(
                client,
                sub_id=sub["id"],
                url=sub["url"],
                secret=sub["secret"],
                seq=event.seq,
                body=body,
                body_bytes=body_bytes,
                settings=settings,
            )


async def _load_active_subscribers(
    topic_id: uuid.UUID, event_type: str
) -> list[dict]:
    async with session_scope() as s:
        stmt = select(TopicWebhook).where(
            TopicWebhook.topic_id == topic_id,
            TopicWebhook.disabled_at.is_(None),
        )
        rows = (await s.execute(stmt)).scalars().all()
        out: list[dict] = []
        for w in rows:
            if w.event_filter and event_type not in w.event_filter:
                continue
            out.append(
                {
                    "id": w.id,
                    "url": w.url,
                    "secret": w.secret,
                }
            )
        return out


async def _deliver_with_retries(
    client: httpx.AsyncClient,
    *,
    sub_id: int,
    url: str,
    secret: str | None,
    seq: int,
    body: str,
    body_bytes: bytes,
    settings: ClaudeAgentSettings,
) -> None:
    backoff = settings.webhook_initial_backoff_sec
    last_error: str | None = None
    for attempt in range(settings.webhook_max_retries + 1):
        try:
            headers = {"Content-Type": "application/json"}
            if secret:
                sig = hmac.new(
                    secret.encode("utf-8"), body_bytes, hashlib.sha256
                ).hexdigest()
                headers["X-Signature"] = f"sha256={sig}"
            resp = await client.post(url, content=body_bytes, headers=headers)
            if 200 <= resp.status_code < 300:
                await _record_success(sub_id, seq)
                return
            last_error = f"HTTP {resp.status_code}: {resp.text[:200]}"
        except Exception as exc:  # noqa: BLE001
            last_error = f"{type(exc).__name__}: {exc}"
        if attempt < settings.webhook_max_retries:
            await asyncio.sleep(backoff)
            backoff *= 2
    logger.warning(
        "webhook delivery exhausted retries sub_id=%s seq=%s err=%s",
        sub_id,
        seq,
        last_error,
    )
    await _record_failure(sub_id, max_failures=10)


async def _record_success(sub_id: int, seq: int) -> None:
    async with session_scope() as s:
        await s.execute(
            update(TopicWebhook)
            .where(TopicWebhook.id == sub_id)
            .values(last_delivered_seq=seq, delivery_failures=0)
        )


async def _record_failure(sub_id: int, *, max_failures: int) -> None:
    async with session_scope() as s:
        row = await s.get(TopicWebhook, sub_id)
        if row is None:
            return
        row.delivery_failures += 1
        if row.delivery_failures >= max_failures and row.disabled_at is None:
            row.disabled_at = datetime.now(timezone.utc)


def _serialize_event(event: EventOut) -> str:
    return json.dumps(
        {
            "seq": event.seq,
            "event_type": event.event_type,
            "event_version": event.event_version,
            "topic_id": str(event.topic_id),
            "created_at": event.created_at.astimezone(timezone.utc).isoformat(),
            "payload": event.payload,
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )
