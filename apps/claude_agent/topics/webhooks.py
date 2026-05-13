import asyncio
import hashlib
import hmac
import json
import logging
import uuid
from typing import Any

import httpx
from sqlalchemy import select

from .db import session_scope
from .models import TopicWebhook

logger = logging.getLogger(__name__)


async def deliver_event(topic_id: uuid.UUID, seq: int, event_type: str, payload: dict[str, Any]) -> None:
    async with session_scope() as s:
        subs = (await s.execute(select(TopicWebhook).where(TopicWebhook.topic_id == topic_id))).scalars().all()
        targets = [(w.url, w.secret) for w in subs]

    if not targets:
        return

    body = json.dumps({
        "seq": seq,
        "event_type": event_type,
        "topic_id": str(topic_id),
        "payload": payload,
    }, ensure_ascii=False).encode("utf-8")

    async def _post(url: str, secret: str | None) -> None:
        headers = {"Content-Type": "application/json"}
        if secret:
            headers["X-Signature"] = "sha256=" + hmac.new(
                secret.encode("utf-8"), body, hashlib.sha256
            ).hexdigest()
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, content=body, headers=headers)
            if resp.status_code >= 300:
                logger.warning("webhook %s seq=%s status=%s", url, seq, resp.status_code)

    await asyncio.gather(*[_post(u, s) for u, s in targets], return_exceptions=True)
