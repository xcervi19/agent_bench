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
from .models import Topic, TopicEvent, TopicRefreshDelta, TopicSubscription, TopicWebhook
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
from .refresh import build_short_term_queries, list_deltas, run_refresh


class CreateTopicBody(BaseModel):
    topic: str = Field(min_length=1)


class WebhookBody(BaseModel):
    url: HttpUrl
    secret: str | None = None


class MonitorBody(BaseModel):
    max_age_hours: int = Field(default=48, ge=1, le=720)
    short_term_queries: list[dict[str, Any]] | None = Field(
        default=None,
        description="Optional override. If omitted, queries are auto-built from parsed.json + report.json.",
    )


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


# ---- v2: continuous monitoring ---------------------------------------------


@router.post("/{topic_id}/monitor", status_code=status.HTTP_201_CREATED)
async def start_monitoring(
    topic_id: uuid.UUID,
    body: MonitorBody,
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
) -> dict[str, Any]:
    """Enable continuous monitoring on a reported topic.

    Generates the persistent short_term_queries plan from parsed.json + report.json
    (unless caller supplies their own). Idempotent: a second call re-activates and
    refreshes the query plan but does not duplicate subscriptions.
    """
    async with session_scope() as s:
        row = await s.get(Topic, topic_id)
        if row is None:
            raise HTTPException(status_code=404, detail="topic not found")
        if row.state != STATE_REPORTED:
            raise HTTPException(
                status_code=409,
                detail=f"cannot monitor from state={row.state}; topic must be 'reported'",
            )
        plan_run_id = row.plan_run_id
        deliver_run_id = row.deliver_run_id
        topic_hash = row.topic_id_hash

    if body.short_term_queries is not None:
        queries = body.short_term_queries
    else:
        queries = _build_queries_from_disk(settings, topic_hash, plan_run_id, deliver_run_id)

    async with session_scope() as s:
        existing = (await s.execute(
            select(TopicSubscription).where(TopicSubscription.topic_id == topic_id)
        )).scalar_one_or_none()
        if existing is None:
            sub = TopicSubscription(
                topic_id=topic_id,
                status="active",
                short_term_queries=queries,
                max_age_hours=body.max_age_hours,
            )
            s.add(sub)
            await s.flush()
            sub_id = sub.id
            created = True
        else:
            existing.status = "active"
            existing.short_term_queries = queries
            existing.max_age_hours = body.max_age_hours
            sub_id = existing.id
            created = False

    await emit(topic_id, "monitor.started" if created else "monitor.updated", {
        "subscription_id": sub_id,
        "queries_count": len(queries),
        "max_age_hours": body.max_age_hours,
    })
    return {
        "subscription_id": sub_id,
        "status": "active",
        "queries_count": len(queries),
        "max_age_hours": body.max_age_hours,
        "short_term_queries": queries,
    }


@router.get("/{topic_id}/monitor")
async def get_monitoring(topic_id: uuid.UUID) -> dict[str, Any]:
    async with session_scope() as s:
        sub = (await s.execute(
            select(TopicSubscription).where(TopicSubscription.topic_id == topic_id)
        )).scalar_one_or_none()
        if sub is None:
            raise HTTPException(status_code=404, detail="no monitoring subscription")
        return {
            "subscription_id": sub.id,
            "status": sub.status,
            "max_age_hours": sub.max_age_hours,
            "refresh_count": sub.refresh_count,
            "refresh_locked": sub.refresh_locked,
            "last_refresh_at": (
                sub.last_refresh_at.astimezone(timezone.utc).isoformat()
                if sub.last_refresh_at is not None
                else None
            ),
            "last_refresh_run_id": sub.last_refresh_run_id,
            "short_term_queries": sub.short_term_queries,
        }


@router.delete("/{topic_id}/monitor", status_code=status.HTTP_200_OK)
async def stop_monitoring(topic_id: uuid.UUID) -> dict[str, Any]:
    async with session_scope() as s:
        sub = (await s.execute(
            select(TopicSubscription).where(TopicSubscription.topic_id == topic_id)
        )).scalar_one_or_none()
        if sub is None:
            raise HTTPException(status_code=404, detail="no monitoring subscription")
        sub.status = "paused"
    await emit(topic_id, "monitor.stopped", {})
    return {"status": "paused"}


@router.post("/{topic_id}/refresh", status_code=status.HTTP_202_ACCEPTED)
async def trigger_refresh(
    topic_id: uuid.UUID,
    background: BackgroundTasks,
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
) -> dict[str, Any]:
    """Trigger one refresh cycle. Idempotent if a refresh is already running.

    Returns 202 with `{accepted, subscription_id, queued}` immediately; watch
    SSE for `refresh.started` / `refresh.completed` events.
    """
    async with session_scope() as s:
        sub = (await s.execute(
            select(TopicSubscription).where(TopicSubscription.topic_id == topic_id)
        )).scalar_one_or_none()
        if sub is None:
            raise HTTPException(status_code=404, detail="no monitoring subscription; POST /monitor first")
        if sub.status != "active":
            raise HTTPException(status_code=409, detail=f"subscription is {sub.status}")
        if sub.refresh_locked:
            return {"accepted": True, "subscription_id": sub.id, "queued": False, "reason": "refresh already running"}
        subscription_id = sub.id

    background.add_task(run_refresh, topic_id, subscription_id, settings)
    return {"accepted": True, "subscription_id": subscription_id, "queued": True}


@router.get("/{topic_id}/deltas")
async def get_deltas(topic_id: uuid.UUID, limit: int = 50) -> dict[str, Any]:
    items = await list_deltas(topic_id, limit=limit)
    return {"deltas": items, "count": len(items)}


@router.get("/{topic_id}/deltas/{seq}")
async def get_delta(
    topic_id: uuid.UUID,
    seq: int,
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
):
    async with session_scope() as s:
        row = (await s.execute(
            select(TopicRefreshDelta).where(
                TopicRefreshDelta.topic_id == topic_id,
                TopicRefreshDelta.seq == seq,
            )
        )).scalar_one_or_none()
        if row is None:
            raise HTTPException(status_code=404, detail="delta not found")
        topic_row = await s.get(Topic, topic_id)
    delta_path = (
        Path(settings.state_dir) / "news" / topic_row.topic_id_hash / "runs" / row.run_id / "delta.json"
    )
    if not delta_path.exists():
        raise HTTPException(status_code=404, detail="delta artifact not on disk")
    return FileResponse(str(delta_path), media_type="application/json")


def _build_queries_from_disk(
    settings: ClaudeAgentSettings,
    topic_hash: str,
    plan_run_id: str | None,
    deliver_run_id: str | None,
) -> list[dict[str, Any]]:
    if not plan_run_id:
        raise HTTPException(status_code=409, detail="topic has no plan_run_id")
    parsed_path = Path(settings.state_dir) / "news" / topic_hash / "runs" / plan_run_id / "parsed.json"
    if not parsed_path.exists():
        raise HTTPException(status_code=409, detail="parsed.json missing on disk")
    try:
        parsed = json.loads(parsed_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise HTTPException(status_code=500, detail=f"parsed.json unreadable: {exc}") from exc
    report: dict[str, Any] | None = None
    if deliver_run_id:
        report_path = (
            Path(settings.state_dir) / "news" / topic_hash / "runs" / deliver_run_id / "report.json"
        )
        if report_path.exists():
            try:
                report = json.loads(report_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                report = None
    return build_short_term_queries(parsed, report)


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
