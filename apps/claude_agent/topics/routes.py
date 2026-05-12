"""HTTP routes: /v1/topics/* — the topic pipeline API.

Mounted by :mod:`apps.claude_agent.app` alongside the existing
``/v1/agent/*`` endpoints. Returns 503 if no DATABASE_URL is configured.
"""

from __future__ import annotations

import asyncio
import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Header, HTTPException, Path as PathParam, Query, Request, status
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy import select

from ..artifacts import topic_id_from_args
from ..config import ClaudeAgentSettings, get_settings
from .db import DatabaseNotConfigured, is_configured, read_session, session_scope
from .events import emit, replay_from_db
from .models import Topic, TopicInput, TopicWebhook
from .schemas import (
    ActionResponse,
    CreateTopicRequest,
    CreateTopicResponse,
    InputRequest,
    ProceedRequest,
    SubscriptionResponse,
    TopicArtifactsLinks,
    TopicResponse,
    WebhookSpec,
)
from .state import TopicState, available_actions, can_transition

logger = logging.getLogger(__name__)


def require_api_key(
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
    x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
) -> None:
    if not settings.api_key:
        return
    if not x_api_key or x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key")


def require_db(
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
) -> None:
    if not is_configured(settings):
        raise HTTPException(
            status_code=503,
            detail=(
                "Topic API requires CLAUDE_AGENT_DATABASE_URL. "
                "Set it (e.g. postgresql+asyncpg://user:pass@postgres:5432/agentic) "
                "and run 'alembic upgrade head'."
            ),
        )


router = APIRouter(
    prefix="/v1/topics",
    tags=["topics"],
    dependencies=[Depends(require_api_key), Depends(require_db)],
)


# ---- helpers ---------------------------------------------------------------


def _row_to_response(row: Topic, base_url: str = "") -> TopicResponse:
    stages_done: list[str] = []
    if row.queries_run_id:
        stages_done.append("queries")
    if row.intro_run_id:
        stages_done.append("intro")
    if row.search_run_id:
        stages_done.append("search")
    if row.report_run_id:
        stages_done.append("report")

    artifacts = TopicArtifactsLinks(
        parsed=f"/v1/topics/{row.id}/parsed" if row.queries_run_id else None,
        intro=f"/v1/topics/{row.id}/intro" if row.intro_run_id else None,
        intro_md=f"/v1/topics/{row.id}/intro.md" if row.intro_run_id else None,
        news=f"/v1/topics/{row.id}/news" if row.search_run_id else None,
        report=f"/v1/topics/{row.id}/report" if row.report_run_id else None,
        report_md=f"/v1/topics/{row.id}/report.md" if row.report_run_id else None,
    )

    return TopicResponse(
        id=row.id,
        topic=row.topic,
        topic_id_hash=row.topic_id_hash,
        state=row.state,
        current_stage=row.current_stage,
        stages_done=stages_done,
        artifacts=artifacts,
        available_actions=available_actions(TopicState(row.state)),
        error=row.error,
        error_type=row.error_type,
        failed_at_stage=row.failed_at_stage,
        created_at=row.created_at,
        updated_at=row.updated_at,
        last_event_seq=row.last_event_seq,
    )


def _supervisor(request: Request):
    sup = getattr(request.app.state, "topic_supervisor", None)
    if sup is None:
        raise HTTPException(
            status_code=503,
            detail="topic_supervisor not initialized (lifespan failure?)",
        )
    return sup


def _bus(request: Request):
    bus = getattr(request.app.state, "topic_bus", None)
    if bus is None:
        raise HTTPException(status_code=503, detail="topic_bus not initialized")
    return bus


# ---- POST /v1/topics -------------------------------------------------------


@router.post(
    "",
    response_model=CreateTopicResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def create_topic(
    body: CreateTopicRequest,
    request: Request,
) -> CreateTopicResponse:
    sup = _supervisor(request)
    bus = _bus(request)
    new_id = uuid.uuid4()
    topic_id_hash = topic_id_from_args(body.topic)

    request_dump: dict[str, Any] = body.model_dump(mode="json")

    async with session_scope() as s:
        row = Topic(
            id=new_id,
            topic=body.topic,
            topic_id_hash=topic_id_hash,
            state=TopicState.PLANNING.value,
            current_stage="queries",
            request=request_dump,
        )
        s.add(row)
        await s.flush()
        await emit(
            s,
            bus,
            topic_id=new_id,
            event_type="topic.created",
            payload={"topic": body.topic, "request": request_dump},
        )
        if body.webhook is not None:
            s.add(
                TopicWebhook(
                    topic_id=new_id,
                    url=str(body.webhook.url),
                    secret=body.webhook.secret,
                    event_filter=body.webhook.event_filter,
                )
            )
        await emit(
            s,
            bus,
            topic_id=new_id,
            event_type="state.changed",
            payload={"from": TopicState.CREATED.value, "to": TopicState.PLANNING.value},
        )

    await sup.start_topic(new_id)

    return CreateTopicResponse(
        topic_id=new_id,
        state=TopicState.PLANNING.value,
        events_url=f"/v1/topics/{new_id}/events",
    )


# ---- GET /v1/topics/{id} ---------------------------------------------------


@router.get("/{topic_id}", response_model=TopicResponse)
async def get_topic(
    topic_id: Annotated[uuid.UUID, PathParam()],
) -> TopicResponse:
    async with read_session() as s:
        row = await s.get(Topic, topic_id)
        if row is None:
            raise HTTPException(status_code=404, detail="topic not found")
        return _row_to_response(row)


# ---- GET /v1/topics/{id}/events (SSE) --------------------------------------


@router.get("/{topic_id}/events")
async def stream_events(
    topic_id: Annotated[uuid.UUID, PathParam()],
    request: Request,
    from_seq: int = Query(default=0, ge=0),
):
    bus = _bus(request)

    async with read_session() as s:
        row = await s.get(Topic, topic_id)
        if row is None:
            raise HTTPException(status_code=404, detail="topic not found")
        replay = await replay_from_db(s, topic_id, from_seq=from_seq)

    queue = await bus.subscribe(topic_id)

    async def gen():
        try:
            for ev in replay:
                yield _format_sse(ev.seq, ev.event_type, ev)
            last_seq = replay[-1].seq if replay else from_seq
            heartbeat_interval = 15.0
            while True:
                if await request.is_disconnected():
                    break
                try:
                    ev = await asyncio.wait_for(queue.get(), timeout=heartbeat_interval)
                except asyncio.TimeoutError:
                    yield ": heartbeat\n\n"
                    continue
                if ev.seq <= last_seq:
                    continue  # already delivered via replay
                last_seq = ev.seq
                yield _format_sse(ev.seq, ev.event_type, ev)
        finally:
            await bus.unsubscribe(topic_id, queue)

    return StreamingResponse(gen(), media_type="text/event-stream")


def _format_sse(seq: int, event_type: str, ev) -> str:
    payload = {
        "seq": ev.seq,
        "event_type": ev.event_type,
        "event_version": ev.event_version,
        "topic_id": str(ev.topic_id),
        "created_at": ev.created_at.astimezone(timezone.utc).isoformat(),
        "payload": ev.payload,
    }
    return (
        f"id: {seq}\n"
        f"event: {event_type}\n"
        f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"
    )


# ---- POST /v1/topics/{id}/proceed ------------------------------------------


@router.post(
    "/{topic_id}/proceed",
    response_model=ActionResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def proceed_topic(
    topic_id: Annotated[uuid.UUID, PathParam()],
    body: ProceedRequest,
    request: Request,
) -> ActionResponse:
    sup = _supervisor(request)
    bus = _bus(request)
    async with session_scope() as s:
        row = await s.get(Topic, topic_id)
        if row is None:
            raise HTTPException(status_code=404, detail="topic not found")
        if body.from_state and row.state != body.from_state:
            raise HTTPException(
                status_code=409,
                detail=f"current_state={row.state} != from_state={body.from_state}",
            )
        if row.state != TopicState.PLANNED_AWAITING_REVIEW.value:
            raise HTTPException(
                status_code=409,
                detail=f"cannot proceed from state={row.state}",
            )
        if not can_transition(
            TopicState.PLANNED_AWAITING_REVIEW, TopicState.SEARCHING
        ):
            raise HTTPException(status_code=500, detail="state machine misconfigured")
        old = row.state
        row.state = TopicState.SEARCHING.value
        row.current_stage = "search"
        await emit(
            s,
            bus,
            topic_id=topic_id,
            event_type="state.changed",
            payload={"from": old, "to": TopicState.SEARCHING.value, "reason": "user_proceed"},
        )
        await emit(
            s,
            bus,
            topic_id=topic_id,
            event_type="input.received",
            payload={"kind": "proceed", "payload": {}},
        )

    await sup.signal_proceed(topic_id)
    return ActionResponse(new_state=TopicState.SEARCHING.value)


# ---- POST /v1/topics/{id}/inputs -------------------------------------------


@router.post(
    "/{topic_id}/inputs",
    response_model=ActionResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def post_input(
    topic_id: Annotated[uuid.UUID, PathParam()],
    body: InputRequest,
    request: Request,
) -> ActionResponse:
    bus = _bus(request)
    async with session_scope() as s:
        row = await s.get(Topic, topic_id)
        if row is None:
            raise HTTPException(status_code=404, detail="topic not found")
        s.add(
            TopicInput(
                topic_id=topic_id,
                kind=body.kind,
                payload=body.payload,
            )
        )
        await emit(
            s,
            bus,
            topic_id=topic_id,
            event_type="input.received",
            payload={"kind": body.kind, "payload": body.payload},
        )
    # v1 only acts on `proceed`; other kinds are persisted for future stages.
    if body.kind == "proceed":
        sup = _supervisor(request)
        await sup.signal_proceed(topic_id)
    return ActionResponse(applies_to_next_stage="search")


# ---- POST /v1/topics/{id}/cancel -------------------------------------------


@router.post(
    "/{topic_id}/cancel",
    response_model=ActionResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def cancel_topic(
    topic_id: Annotated[uuid.UUID, PathParam()],
    request: Request,
) -> ActionResponse:
    sup = _supervisor(request)
    bus = _bus(request)
    async with session_scope() as s:
        row = await s.get(Topic, topic_id)
        if row is None:
            raise HTTPException(status_code=404, detail="topic not found")
        if row.state in (
            TopicState.REPORTED.value,
            TopicState.FAILED.value,
            TopicState.CANCELLED.value,
            TopicState.ARCHIVED.value,
        ):
            return ActionResponse(new_state=row.state)
        old = row.state
        row.state = TopicState.CANCELLED.value
        await emit(
            s,
            bus,
            topic_id=topic_id,
            event_type="cancelled",
            payload={"from": old},
        )
        await emit(
            s,
            bus,
            topic_id=topic_id,
            event_type="state.changed",
            payload={"from": old, "to": TopicState.CANCELLED.value},
        )
    await sup.cancel(topic_id)
    return ActionResponse(new_state=TopicState.CANCELLED.value)


# ---- POST /v1/topics/{id}/subscribe ----------------------------------------


@router.post(
    "/{topic_id}/subscribe",
    response_model=SubscriptionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def subscribe(
    topic_id: Annotated[uuid.UUID, PathParam()],
    body: WebhookSpec,
) -> SubscriptionResponse:
    async with session_scope() as s:
        row = await s.get(Topic, topic_id)
        if row is None:
            raise HTTPException(status_code=404, detail="topic not found")
        sub = TopicWebhook(
            topic_id=topic_id,
            url=str(body.url),
            secret=body.secret,
            event_filter=body.event_filter,
        )
        s.add(sub)
        await s.flush()
        return SubscriptionResponse(subscription_id=sub.id)


# ---- artifact endpoints ----------------------------------------------------


def _artifact_path(
    settings: ClaudeAgentSettings,
    topic_id_hash: str,
    run_id: str,
    filename: str,
) -> Path:
    return (
        Path(settings.state_dir)
        / "news"
        / topic_id_hash
        / "runs"
        / run_id
        / filename
    )


async def _resolve_topic(topic_id: uuid.UUID) -> Topic:
    async with read_session() as s:
        row = await s.get(Topic, topic_id)
        if row is None:
            raise HTTPException(status_code=404, detail="topic not found")
        return row


def _serve_json_file(path: Path):
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"artifact not produced yet: {path.name}")
    return FileResponse(str(path), media_type="application/json")


def _serve_md_file(path: Path):
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"artifact not produced yet: {path.name}")
    return FileResponse(str(path), media_type="text/markdown; charset=utf-8")


@router.get("/{topic_id}/parsed")
async def get_parsed(
    topic_id: Annotated[uuid.UUID, PathParam()],
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
):
    row = await _resolve_topic(topic_id)
    if not row.queries_run_id:
        raise HTTPException(status_code=404, detail="parsed.json not produced yet")
    return _serve_json_file(
        _artifact_path(settings, row.topic_id_hash, row.queries_run_id, "parsed.json")
    )


@router.get("/{topic_id}/intro")
async def get_intro(
    topic_id: Annotated[uuid.UUID, PathParam()],
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
):
    row = await _resolve_topic(topic_id)
    if not row.intro_run_id:
        raise HTTPException(status_code=404, detail="intro.json not produced yet")
    return _serve_json_file(
        _artifact_path(settings, row.topic_id_hash, row.intro_run_id, "intro.json")
    )


@router.get("/{topic_id}/intro.md")
async def get_intro_md(
    topic_id: Annotated[uuid.UUID, PathParam()],
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
):
    row = await _resolve_topic(topic_id)
    if not row.intro_run_id:
        raise HTTPException(status_code=404, detail="intro.md not produced yet")
    return _serve_md_file(
        _artifact_path(settings, row.topic_id_hash, row.intro_run_id, "intro.md")
    )


@router.get("/{topic_id}/news")
async def get_news(
    topic_id: Annotated[uuid.UUID, PathParam()],
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
):
    row = await _resolve_topic(topic_id)
    if not row.search_run_id:
        raise HTTPException(status_code=404, detail="news.json not produced yet")
    return _serve_json_file(
        _artifact_path(settings, row.topic_id_hash, row.search_run_id, "news.json")
    )


@router.get("/{topic_id}/report")
async def get_report(
    topic_id: Annotated[uuid.UUID, PathParam()],
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
):
    row = await _resolve_topic(topic_id)
    if not row.report_run_id:
        raise HTTPException(status_code=404, detail="report.json not produced yet")
    return _serve_json_file(
        _artifact_path(settings, row.topic_id_hash, row.report_run_id, "report.json")
    )


@router.get("/{topic_id}/report.md")
async def get_report_md(
    topic_id: Annotated[uuid.UUID, PathParam()],
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
):
    row = await _resolve_topic(topic_id)
    if not row.report_run_id:
        raise HTTPException(status_code=404, detail="report.md not produced yet")
    return _serve_md_file(
        _artifact_path(settings, row.topic_id_hash, row.report_run_id, "report.md")
    )
