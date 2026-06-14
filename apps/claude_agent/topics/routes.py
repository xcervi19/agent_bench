import asyncio
import json
import uuid
from datetime import datetime, timezone
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
from .scheduler import compute_next_refresh_at, normalize_interval


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
    # Automatic scheduling (#22). Off by default; enabling requires an interval.
    schedule_enabled: bool = Field(default=False)
    schedule_interval_hours: int | None = Field(
        default=None,
        ge=1,
        description="Refresh cadence in hours. Required when schedule_enabled is true.",
    )


class UpdateMonitorBody(BaseModel):
    """PATCH /monitor — all fields optional; only provided fields change."""

    max_age_hours: int | None = Field(default=None, ge=1, le=720)
    schedule_enabled: bool | None = None
    schedule_interval_hours: int | None = Field(default=None, ge=1)


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


@router.get("")
async def list_topics(limit: int = 50, offset: int = 0, state: str | None = None) -> dict[str, Any]:
    if limit < 1 or limit > 200:
        raise HTTPException(status_code=422, detail="limit must be between 1 and 200")
    if offset < 0:
        raise HTTPException(status_code=422, detail="offset must be >= 0")

    async with session_scope() as s:
        stmt = select(Topic)
        if state:
            stmt = stmt.where(Topic.state == state)
        rows = (await s.execute(
            stmt.order_by(Topic.updated_at.desc(), Topic.created_at.desc()).offset(offset).limit(limit)
        )).scalars().all()

    items = [{
        "id": str(row.id),
        "topic": row.topic,
        "state": row.state,
        "available_actions": _actions(row.state),
        "last_event_seq": row.last_event_seq,
        "created_at": row.created_at.astimezone(timezone.utc).isoformat(),
        "updated_at": row.updated_at.astimezone(timezone.utc).isoformat(),
    } for row in rows]

    return {"items": items, "count": len(items), "limit": limit, "offset": offset, "state": state}


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


def _apply_schedule(
    sub: TopicSubscription,
    *,
    enabled: bool,
    interval_hours: int | None,
    settings: ClaudeAgentSettings,
) -> None:
    """Set schedule fields on a subscription, validating + clamping the interval.

    Enabling requires an interval; the value is clamped to the configured
    [min, max] bounds. Disabling clears the next fire time so the scheduler
    skips the topic. Manual POST /refresh stays available either way.
    """
    if enabled:
        if interval_hours is None:
            raise HTTPException(
                status_code=422,
                detail="schedule_interval_hours is required when schedule_enabled is true",
            )
        interval = normalize_interval(
            interval_hours,
            lo=settings.schedule_min_interval_hours,
            hi=settings.schedule_max_interval_hours,
        )
        sub.schedule_enabled = True
        sub.schedule_interval_hours = interval
        sub.next_refresh_at = compute_next_refresh_at(datetime.now(timezone.utc), interval)
    else:
        sub.schedule_enabled = False
        sub.next_refresh_at = None
        if interval_hours is not None:
            sub.schedule_interval_hours = normalize_interval(
                interval_hours,
                lo=settings.schedule_min_interval_hours,
                hi=settings.schedule_max_interval_hours,
            )


def _monitor_payload(sub: TopicSubscription) -> dict[str, Any]:
    def _iso(dt: datetime | None) -> str | None:
        return dt.astimezone(timezone.utc).isoformat() if dt is not None else None

    return {
        "subscription_id": sub.id,
        "status": sub.status,
        "max_age_hours": sub.max_age_hours,
        "refresh_count": sub.refresh_count,
        "refresh_locked": sub.refresh_locked,
        "schedule_enabled": sub.schedule_enabled,
        "schedule_interval_hours": sub.schedule_interval_hours,
        "next_refresh_at": _iso(sub.next_refresh_at),
        "last_refresh_at": _iso(sub.last_refresh_at),
        "last_scheduled_refresh_at": _iso(sub.last_scheduled_refresh_at),
        "last_refresh_run_id": sub.last_refresh_run_id,
    }


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
            _apply_schedule(
                sub,
                enabled=body.schedule_enabled,
                interval_hours=body.schedule_interval_hours,
                settings=settings,
            )
            s.add(sub)
            await s.flush()
            sub_id = sub.id
            created = True
            payload = _monitor_payload(sub)
        else:
            existing.status = "active"
            existing.short_term_queries = queries
            existing.max_age_hours = body.max_age_hours
            _apply_schedule(
                existing,
                enabled=body.schedule_enabled,
                interval_hours=body.schedule_interval_hours,
                settings=settings,
            )
            sub_id = existing.id
            created = False
            payload = _monitor_payload(existing)

    await emit(topic_id, "monitor.started" if created else "monitor.updated", {
        "subscription_id": sub_id,
        "queries_count": len(queries),
        "max_age_hours": body.max_age_hours,
        "schedule_enabled": payload["schedule_enabled"],
        "schedule_interval_hours": payload["schedule_interval_hours"],
    })
    return {**payload, "queries_count": len(queries), "short_term_queries": queries}


@router.get("/{topic_id}/monitor")
async def get_monitoring(topic_id: uuid.UUID) -> dict[str, Any]:
    async with session_scope() as s:
        sub = (await s.execute(
            select(TopicSubscription).where(TopicSubscription.topic_id == topic_id)
        )).scalar_one_or_none()
        if sub is None:
            raise HTTPException(status_code=404, detail="no monitoring subscription")
        return {**_monitor_payload(sub), "short_term_queries": sub.short_term_queries}


@router.patch("/{topic_id}/monitor")
async def update_monitoring(
    topic_id: uuid.UUID,
    body: UpdateMonitorBody,
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
) -> dict[str, Any]:
    """Update monitoring settings — notably turn the auto-refresh schedule on/off.

    Only provided fields change. Enabling the schedule requires an interval
    (either supplied here or already stored).
    """
    async with session_scope() as s:
        sub = (await s.execute(
            select(TopicSubscription).where(TopicSubscription.topic_id == topic_id)
        )).scalar_one_or_none()
        if sub is None:
            raise HTTPException(status_code=404, detail="no monitoring subscription")

        if body.max_age_hours is not None:
            sub.max_age_hours = body.max_age_hours

        if body.schedule_enabled is not None:
            interval = (
                body.schedule_interval_hours
                if body.schedule_interval_hours is not None
                else sub.schedule_interval_hours
            )
            _apply_schedule(
                sub,
                enabled=body.schedule_enabled,
                interval_hours=interval,
                settings=settings,
            )
        elif body.schedule_interval_hours is not None:
            # Interval change only; re-apply current enabled state with new value.
            _apply_schedule(
                sub,
                enabled=sub.schedule_enabled,
                interval_hours=body.schedule_interval_hours,
                settings=settings,
            )

        payload = _monitor_payload(sub)

    await emit(topic_id, "monitor.updated", {
        "subscription_id": payload["subscription_id"],
        "schedule_enabled": payload["schedule_enabled"],
        "schedule_interval_hours": payload["schedule_interval_hours"],
        "max_age_hours": payload["max_age_hours"],
    })
    return payload


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

    background.add_task(run_refresh, topic_id, subscription_id, settings, trigger="manual")
    return {"accepted": True, "subscription_id": subscription_id, "queued": True, "trigger": "manual"}


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
                # Don't terminate during an active refresh — events are still flowing
                if terminal:
                    sub = (await s.execute(
                        select(TopicSubscription).where(
                            TopicSubscription.topic_id == topic_id,
                            TopicSubscription.refresh_locked.is_(True),
                        )
                    )).scalar_one_or_none()
                    if sub is not None:
                        terminal = False
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


@router.get("/{topic_id}/deltas/{seq}/news")
async def get_delta_news(
    topic_id: uuid.UUID,
    seq: int,
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
):
    """Serve news.json (searched sources + dedup stats) from a refresh run."""
    async with session_scope() as s:
        delta = (await s.execute(
            select(TopicRefreshDelta).where(
                TopicRefreshDelta.topic_id == topic_id,
                TopicRefreshDelta.seq == seq,
            )
        )).scalar_one_or_none()
        if delta is None:
            raise HTTPException(status_code=404, detail="delta not found")
        topic_row = await s.get(Topic, topic_id)
    news_path = (
        Path(settings.state_dir) / "news" / topic_row.topic_id_hash
        / "runs" / delta.run_id / "news.json"
    )
    if not news_path.exists():
        raise HTTPException(status_code=404, detail="news.json not produced yet")
    return FileResponse(str(news_path), media_type="application/json")


@router.get("/{topic_id}/deltas/{seq}/report")
async def get_delta_report(
    topic_id: uuid.UUID,
    seq: int,
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
):
    """Serve report.md from a refresh run."""
    async with session_scope() as s:
        delta = (await s.execute(
            select(TopicRefreshDelta).where(
                TopicRefreshDelta.topic_id == topic_id,
                TopicRefreshDelta.seq == seq,
            )
        )).scalar_one_or_none()
        if delta is None:
            raise HTTPException(status_code=404, detail="delta not found")
        topic_row = await s.get(Topic, topic_id)
    report_path = (
        Path(settings.state_dir) / "news" / topic_row.topic_id_hash
        / "runs" / delta.run_id / "report.md"
    )
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="report.md not produced yet")
    return FileResponse(str(report_path), media_type="text/markdown; charset=utf-8")
