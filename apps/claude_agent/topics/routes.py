import asyncio
import json
import uuid
from datetime import timezone
from pathlib import Path
from typing import Annotated, Any

from fastapi import APIRouter, BackgroundTasks, Depends, Header, HTTPException, Request, status
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy import select

from ..config import ClaudeAgentSettings, get_settings
from .db import session_scope
from .models import Topic, TopicEvent, TopicWebhook
from .pipeline import (
    STATE_PLANNED,
    STATE_PLANNING,
    STATE_REPORTED,
    STATE_FAILED,
    STATE_CANCELLED,
    emit,
    run_deliver,
    run_plan,
    set_state,
    topic_id_hash,
)


class CreateTopicBody(BaseModel):
    topic: str = Field(min_length=1)


class WebhookBody(BaseModel):
    url: HttpUrl
    secret: str | None = None


def _require_api_key(
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
    x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
) -> None:
    if not settings.api_key:
        return
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="invalid X-API-Key")


router = APIRouter(prefix="/v1/topics", tags=["topics"], dependencies=[Depends(_require_api_key)])


@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def create_topic(
    body: CreateTopicBody,
    background: BackgroundTasks,
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
) -> dict[str, Any]:
    new_id = uuid.uuid4()
    async with session_scope() as s:
        s.add(Topic(
            id=new_id,
            topic=body.topic,
            state=STATE_PLANNING,
            topic_id_hash=topic_id_hash(body.topic),
        ))
    await emit(new_id, "topic.created", {"topic": body.topic})
    background.add_task(run_plan, new_id, body.topic, settings)
    return {"topic_id": str(new_id), "state": STATE_PLANNING, "events_url": f"/v1/topics/{new_id}/events"}


@router.get("/{topic_id}")
async def get_topic(topic_id: uuid.UUID) -> dict[str, Any]:
    async with session_scope() as s:
        row = await s.get(Topic, topic_id)
        if row is None:
            raise HTTPException(status_code=404, detail="topic not found")
        return {
            "id": str(row.id),
            "topic": row.topic,
            "state": row.state,
            "plan_run_id": row.plan_run_id,
            "deliver_run_id": row.deliver_run_id,
            "error": row.error,
            "available_actions": _actions(row.state),
            "last_event_seq": row.last_event_seq,
            "created_at": row.created_at.astimezone(timezone.utc).isoformat(),
            "updated_at": row.updated_at.astimezone(timezone.utc).isoformat(),
        }


def _actions(state: str) -> list[str]:
    if state == STATE_PLANNED:
        return ["proceed", "cancel"]
    if state in (STATE_REPORTED, STATE_FAILED, STATE_CANCELLED):
        return []
    return ["cancel"]


@router.post("/{topic_id}/proceed", status_code=status.HTTP_202_ACCEPTED)
async def proceed(
    topic_id: uuid.UUID,
    background: BackgroundTasks,
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
) -> dict[str, Any]:
    async with session_scope() as s:
        row = await s.get(Topic, topic_id)
        if row is None:
            raise HTTPException(status_code=404, detail="topic not found")
        if row.state != STATE_PLANNED:
            raise HTTPException(status_code=409, detail=f"cannot proceed from state={row.state}")
    background.add_task(run_deliver, topic_id, settings)
    return {"accepted": True}


@router.post("/{topic_id}/cancel", status_code=status.HTTP_202_ACCEPTED)
async def cancel(topic_id: uuid.UUID) -> dict[str, Any]:
    async with session_scope() as s:
        row = await s.get(Topic, topic_id)
        if row is None:
            raise HTTPException(status_code=404, detail="topic not found")
        if row.state in (STATE_REPORTED, STATE_FAILED, STATE_CANCELLED):
            return {"accepted": True, "state": row.state}
    await set_state(topic_id, STATE_CANCELLED)
    return {"accepted": True, "state": STATE_CANCELLED}


@router.post("/{topic_id}/subscribe", status_code=status.HTTP_201_CREATED)
async def subscribe(topic_id: uuid.UUID, body: WebhookBody) -> dict[str, Any]:
    async with session_scope() as s:
        row = await s.get(Topic, topic_id)
        if row is None:
            raise HTTPException(status_code=404, detail="topic not found")
        sub = TopicWebhook(topic_id=topic_id, url=str(body.url), secret=body.secret)
        s.add(sub)
        await s.flush()
        return {"subscription_id": sub.id}


@router.get("/{topic_id}/events")
async def events(topic_id: uuid.UUID, request: Request, from_seq: int = 0):
    async def gen():
        last = from_seq
        while True:
            if await request.is_disconnected():
                return
            async with session_scope() as s:
                row = await s.get(Topic, topic_id)
                if row is None:
                    yield _sse(0, "error", {"error": "topic not found"})
                    return
                rows = (await s.execute(
                    select(TopicEvent)
                    .where(TopicEvent.topic_id == topic_id, TopicEvent.seq > last)
                    .order_by(TopicEvent.seq.asc())
                )).scalars().all()
                terminal = row.state in (STATE_REPORTED, STATE_FAILED, STATE_CANCELLED)
            for ev in rows:
                yield _sse(ev.seq, ev.event_type, {
                    "seq": ev.seq,
                    "event_type": ev.event_type,
                    "topic_id": str(topic_id),
                    "payload": ev.payload,
                })
                last = ev.seq
            if terminal and not rows:
                yield ": done\n\n"
                return
            await asyncio.sleep(0.5)
    return StreamingResponse(gen(), media_type="text/event-stream")


def _sse(seq: int, event_type: str, payload: dict[str, Any]) -> str:
    return f"id: {seq}\nevent: {event_type}\ndata: {json.dumps(payload, ensure_ascii=False)}\n\n"


# ---- artifact serving ------------------------------------------------------


async def _load_topic(topic_id: uuid.UUID) -> Topic:
    async with session_scope() as s:
        row = await s.get(Topic, topic_id)
        if row is None:
            raise HTTPException(status_code=404, detail="topic not found")
        return row


def _artifact(settings: ClaudeAgentSettings, hash_: str, run_id: str | None, filename: str) -> Path:
    if not run_id:
        raise HTTPException(status_code=404, detail=f"{filename} not produced yet")
    path = Path(settings.state_dir) / "news" / hash_ / "runs" / run_id / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"{filename} not produced yet")
    return path


@router.get("/{topic_id}/parsed")
async def get_parsed(topic_id: uuid.UUID, settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]):
    row = await _load_topic(topic_id)
    return FileResponse(str(_artifact(settings, row.topic_id_hash, row.plan_run_id, "parsed.json")),
                        media_type="application/json")


@router.get("/{topic_id}/intro")
async def get_intro(topic_id: uuid.UUID, settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]):
    row = await _load_topic(topic_id)
    return FileResponse(str(_artifact(settings, row.topic_id_hash, row.plan_run_id, "intro.json")),
                        media_type="application/json")


@router.get("/{topic_id}/intro.md")
async def get_intro_md(topic_id: uuid.UUID, settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]):
    row = await _load_topic(topic_id)
    return FileResponse(str(_artifact(settings, row.topic_id_hash, row.plan_run_id, "intro.md")),
                        media_type="text/markdown; charset=utf-8")


@router.get("/{topic_id}/news")
async def get_news(topic_id: uuid.UUID, settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]):
    row = await _load_topic(topic_id)
    return FileResponse(str(_artifact(settings, row.topic_id_hash, row.deliver_run_id, "news.json")),
                        media_type="application/json")


@router.get("/{topic_id}/report")
async def get_report(topic_id: uuid.UUID, settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]):
    row = await _load_topic(topic_id)
    return FileResponse(str(_artifact(settings, row.topic_id_hash, row.deliver_run_id, "report.json")),
                        media_type="application/json")


@router.get("/{topic_id}/report.md")
async def get_report_md(topic_id: uuid.UUID, settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]):
    row = await _load_topic(topic_id)
    return FileResponse(str(_artifact(settings, row.topic_id_hash, row.deliver_run_id, "report.md")),
                        media_type="text/markdown; charset=utf-8")
