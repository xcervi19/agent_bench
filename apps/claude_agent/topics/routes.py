import asyncio
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated, Any, Literal

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import CurrentPrincipal, Principal
from ..config import ClaudeAgentSettings, get_settings
from .db import session_scope
from .models import (
    SHARE_FROZEN,
    SHARE_LIVE,
    Topic,
    TopicEvent,
    TopicRefreshDelta,
    TopicSubscription,
    TopicWebhook,
    is_frozen,
)
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
from .refresh import (
    build_short_term_queries,
    list_deltas,
    run_refresh,
    validate_short_term_queries,
)
from .scheduler import compute_next_refresh_at, normalize_interval
from .serving import artifact_response
from .source_quality import SOURCE_MIX_FILENAME


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


class ShareBody(BaseModel):
    """POST/PATCH /publish — how the share should behave for the *owner* (#50).

    `live` (the default) publishes a read-only view and takes nothing away: the
    topic keeps refreshing, monitoring keeps running, and readers see the newest
    completed state. `frozen` is the #40 snapshot — the topic stops for everyone,
    the owner included, until it is unshared or set back to live.
    """

    mode: Literal["live", "frozen"] = SHARE_LIVE


class UpdateMonitorBody(BaseModel):
    """PATCH /monitor — all fields optional; only provided fields change."""

    max_age_hours: int | None = Field(default=None, ge=1, le=720)
    schedule_enabled: bool | None = None
    schedule_interval_hours: int | None = Field(default=None, ge=1)
    short_term_queries: list[dict[str, Any]] | None = Field(
        default=None,
        description=(
            "Replace the persistent monitoring plan. Validated on the shape "
            "`build_short_term_queries` produces, `allowed_domains` included. "
            "Without this the plan is written once at POST /monitor and no query "
            "improvement can ever reach a topic already under monitoring (#51). "
            "*Which* queries to change is a measurement question and belongs to "
            "#46; this is the affordance only."
        ),
    )


router = APIRouter(prefix="/v1/topics", tags=["topics"])


# Declared before /{topic_id} so the literal path wins the match. Corpus-wide and
# therefore service-only: the domain breakdown spans every owner's documents.
@router.get("/search-coverage")
async def search_coverage(principal: CurrentPrincipal) -> dict[str, Any]:
    """Fetch outcomes across the whole evidence corpus — what we can and cannot read."""
    if not principal.is_service:
        raise HTTPException(status_code=403, detail="service principal required")
    from .search_content import coverage

    return await coverage()


async def _owned(s: AsyncSession, topic_id: uuid.UUID, principal: Principal) -> Topic:
    """Load a topic the principal may access. 404 hides other users' topics."""
    row = await s.get(Topic, topic_id)
    if row is None or not (principal.is_service or row.owner_user_id == principal.user_id):
        raise HTTPException(status_code=404, detail="topic not found")
    return row


async def _mutable(s: AsyncSession, topic_id: uuid.UUID, principal: Principal) -> Topic:
    """Load a topic the principal may *change*.

    Sharing does not, by itself, take control away (#50) — a live share is
    read-only to the public and fully owned by its owner. Only a **frozen** share
    pins the topic: what was shared is the state at that moment, so every route
    that could move it refuses until the owner sets it back to live or unshares
    it. Those two writes are the only ones a frozen topic accepts.
    """
    row = await _owned(s, topic_id, principal)
    if is_frozen(row):
        raise HTTPException(
            status_code=409,
            detail=(
                "topic is shared as a frozen snapshot and is read-only; "
                "switch it to live sharing or unpublish it first"
            ),
        )
    return row


async def _load_topic(topic_id: uuid.UUID, principal: Principal) -> Topic:
    async with session_scope() as s:
        return await _owned(s, topic_id, principal)


@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def create_topic(
    body: CreateTopicBody,
    background: BackgroundTasks,
    principal: CurrentPrincipal,
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
) -> dict[str, Any]:
    new_id = uuid.uuid4()
    async with session_scope() as s:
        s.add(Topic(
            id=new_id,
            owner_user_id=principal.user_id,
            topic=body.topic,
            state=STATE_PLANNING,
            topic_id_hash=topic_id_hash(body.topic),
        ))
    await emit(new_id, "topic.created", {"topic": body.topic})
    background.add_task(run_plan, new_id, body.topic, settings)
    return {"topic_id": str(new_id), "state": STATE_PLANNING, "events_url": f"/v1/topics/{new_id}/events"}


@router.get("")
async def list_topics(
    principal: CurrentPrincipal,
    limit: int = 50,
    offset: int = 0,
    state: str | None = None,
) -> dict[str, Any]:
    if limit < 1 or limit > 200:
        raise HTTPException(status_code=422, detail="limit must be between 1 and 200")
    if offset < 0:
        raise HTTPException(status_code=422, detail="offset must be >= 0")

    async with session_scope() as s:
        stmt = select(Topic)
        if not principal.is_service:
            stmt = stmt.where(Topic.owner_user_id == principal.user_id)
        if state:
            stmt = stmt.where(Topic.state == state)
        rows = (await s.execute(
            stmt.order_by(Topic.updated_at.desc(), Topic.created_at.desc()).offset(offset).limit(limit)
        )).scalars().all()

    items = [_summary(row) for row in rows]

    return {"items": items, "count": len(items), "limit": limit, "offset": offset, "state": state}


@router.get("/{topic_id}")
async def get_topic(topic_id: uuid.UUID, principal: CurrentPrincipal) -> dict[str, Any]:
    async with session_scope() as s:
        row = await _owned(s, topic_id, principal)
        return {
            **_summary(row),
            "plan_run_id": row.plan_run_id,
            "deliver_run_id": row.deliver_run_id,
            "error": row.error,
        }


def _summary(row: Topic) -> dict[str, Any]:
    return {
        "id": str(row.id),
        "topic": row.topic,
        "state": row.state,
        "available_actions": _actions(row.state, is_frozen(row)),
        "last_event_seq": row.last_event_seq,
        "created_at": row.created_at.astimezone(timezone.utc).isoformat(),
        "updated_at": row.updated_at.astimezone(timezone.utc).isoformat(),
        **_share_payload(row),
    }


def _share_payload(row: Topic) -> dict[str, Any]:
    return {
        "is_public": bool(row.is_public),
        "published_at": (
            row.published_at.astimezone(timezone.utc).isoformat()
            if row.published_at is not None
            else None
        ),
        # Where anyone — signed in or not — can read this snapshot. Null while
        # private so a client cannot advertise a link that would 404.
        "public_path": f"/v1/public/topics/{row.id}" if row.is_public else None,
        # What sharing does to the owner (#50). Meaningless while private, and
        # reported as such, so a client never shows "live" on an unshared topic.
        "share_mode": row.share_mode if row.is_public else None,
        "frozen_at": (
            row.frozen_at.astimezone(timezone.utc).isoformat()
            if row.is_public and row.frozen_at is not None
            else None
        ),
    }


def _actions(state: str, frozen: bool = False) -> list[str]:
    # A frozen share refuses every action (#40/#50); offering one the API will
    # refuse would only invite a click. A live share changes nothing here — its
    # owner keeps the same controls they had before they shared it.
    if frozen:
        return []
    if state == STATE_PLANNED:
        return ["proceed", "cancel"]
    if state in (STATE_REPORTED, STATE_FAILED, STATE_CANCELLED):
        return []
    return ["cancel"]


# ---- sharing (#40) ---------------------------------------------------------


@router.post("/{topic_id}/publish", status_code=status.HTTP_200_OK)
async def publish_topic(
    topic_id: uuid.UUID, principal: CurrentPrincipal, body: ShareBody | None = None
) -> dict[str, Any]:
    """Share a finished topic: anyone may read it, nobody may change it.

    Two shares, one link (#50):

      * **live** (default) — the public view follows the topic. Monitoring keeps
        running, refresh keeps working, and readers see the newest *completed*
        state. The owner loses nothing; what the public loses is every write, and
        it loses those structurally — the anonymous router has no write route.
      * **frozen** — the #40 snapshot. The topic stops for everyone, monitoring
        pauses, and nothing can spend against it until it is unshared or set
        back to live.

    Only a `reported` topic can be shared either way: sharing means "here is the
    finished picture", and a topic still moving through the pipeline has none.

    Idempotent: publishing an already-published topic keeps the original
    `published_at` and its current mode, so a double click neither drifts the
    date nor silently re-modes the share. Changing mode is PATCH.
    """
    mode = (body or ShareBody()).mode
    async with session_scope() as s:
        row = await _owned(s, topic_id, principal)
        if row.is_public:
            return {**_share_payload(row), "already_published": True, "monitoring_paused": False}
        if row.state != STATE_REPORTED:
            raise HTTPException(
                status_code=409,
                detail=f"cannot publish from state={row.state}; topic must be 'reported'",
            )

        # Pin first: freezing is refused while a cycle is in flight, and a
        # publish that is going to be refused must not have half happened.
        monitoring_paused = await _pin(s, row) if mode == SHARE_FROZEN else False

        row.is_public = True
        row.published_at = datetime.now(timezone.utc)
        row.share_mode = mode
        # A reported topic's deliver run has finished, so it is safe to serve.
        # Older rows predate the pointer; adopt the current run for them here.
        if row.public_deliver_run_id is None:
            row.public_deliver_run_id = row.deliver_run_id
        if row.public_updated_at is None:
            row.public_updated_at = row.updated_at
        payload = _share_payload(row)

    await emit(topic_id, "topic.published", {
        "published_at": payload["published_at"],
        "share_mode": mode,
        "monitoring_paused": monitoring_paused,
    })
    return {**payload, "already_published": False, "monitoring_paused": monitoring_paused}


@router.patch("/{topic_id}/publish", status_code=status.HTTP_200_OK)
async def set_share_mode(
    topic_id: uuid.UUID, body: ShareBody, principal: CurrentPrincipal
) -> dict[str, Any]:
    """Switch a live share to a snapshot, or a snapshot back to live (#50).

    The link is untouched either way — this changes what the owner may do and
    whether the public view is allowed to move, not who can read it.

    Going back to live does **not** resume monitoring. Freezing turned spending
    off; turning it back on is a decision the owner should make deliberately,
    the same argument #40 made for unpublish.
    """
    async with session_scope() as s:
        row = await _owned(s, topic_id, principal)
        if not row.is_public:
            raise HTTPException(status_code=409, detail="topic is not shared; publish it first")
        previous = row.share_mode
        if previous == body.mode:
            return {**_share_payload(row), "changed": False, "monitoring_paused": False}

        monitoring_paused = False
        if body.mode == SHARE_FROZEN:
            monitoring_paused = await _pin(s, row)
        else:
            row.share_mode = SHARE_LIVE
            row.frozen_at = None
        payload = _share_payload(row)

    await emit(topic_id, "topic.share_mode_changed", {
        "from": previous,
        "to": body.mode,
        "monitoring_paused": monitoring_paused,
    })
    return {**payload, "changed": True, "monitoring_paused": monitoring_paused}


async def _pin(s: AsyncSession, row: Topic) -> bool:
    """Freeze a share: stop the topic, and stop it spending. Returns whether
    monitoring was actually paused.

    Refused while a cycle is in flight, because that cycle would finish *after*
    the freeze and move the snapshot readers were promised — `run_refresh` only
    checks the mode on the way in.
    """
    sub = (await s.execute(
        select(TopicSubscription).where(TopicSubscription.topic_id == row.id)
    )).scalar_one_or_none()
    if sub is not None and sub.refresh_locked:
        raise HTTPException(
            status_code=409,
            detail="a refresh is running; freeze once it finishes so the shared state is final",
        )

    row.share_mode = SHARE_FROZEN
    row.frozen_at = datetime.now(timezone.utc)
    if sub is not None and (sub.status == "active" or sub.schedule_enabled):
        sub.status = "paused"
        sub.schedule_enabled = False
        sub.next_refresh_at = None
        return True
    return False


@router.delete("/{topic_id}/publish", status_code=status.HTTP_200_OK)
async def unpublish_topic(topic_id: uuid.UUID, principal: CurrentPrincipal) -> dict[str, Any]:
    """Take a shared topic back. Existing links stop resolving immediately.

    Monitoring is left exactly as it is. After a live share there is nothing to
    restore — it never stopped. After a frozen one it stays paused, because
    freezing turned spending off deliberately and turning it back on is the
    owner's call.
    """
    async with session_scope() as s:
        row = await _owned(s, topic_id, principal)
        if not row.is_public:
            return {**_share_payload(row), "already_private": True}
        row.is_public = False
        row.published_at = None
        row.frozen_at = None
        row.share_mode = SHARE_LIVE
        payload = _share_payload(row)

    await emit(topic_id, "topic.unpublished", {})
    return {**payload, "already_private": False}


# ---- pipeline actions ------------------------------------------------------


@router.post("/{topic_id}/proceed", status_code=status.HTTP_202_ACCEPTED)
async def proceed(
    topic_id: uuid.UUID,
    background: BackgroundTasks,
    principal: CurrentPrincipal,
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
) -> dict[str, Any]:
    async with session_scope() as s:
        row = await _mutable(s, topic_id, principal)
        if row.state != STATE_PLANNED:
            raise HTTPException(status_code=409, detail=f"cannot proceed from state={row.state}")
    background.add_task(run_deliver, topic_id, settings)
    return {"accepted": True}


@router.post("/{topic_id}/cancel", status_code=status.HTTP_202_ACCEPTED)
async def cancel(topic_id: uuid.UUID, principal: CurrentPrincipal) -> dict[str, Any]:
    async with session_scope() as s:
        row = await _mutable(s, topic_id, principal)
        if row.state in (STATE_REPORTED, STATE_FAILED, STATE_CANCELLED):
            return {"accepted": True, "state": row.state}
    await set_state(topic_id, STATE_CANCELLED)
    return {"accepted": True, "state": STATE_CANCELLED}


@router.post("/{topic_id}/subscribe", status_code=status.HTTP_201_CREATED)
async def subscribe(
    topic_id: uuid.UUID, body: WebhookBody, principal: CurrentPrincipal
) -> dict[str, Any]:
    async with session_scope() as s:
        await _mutable(s, topic_id, principal)
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
    principal: CurrentPrincipal,
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
) -> dict[str, Any]:
    """Enable continuous monitoring on a reported topic.

    Generates the persistent short_term_queries plan from parsed.json + report.json
    (unless caller supplies their own). Idempotent: a second call re-activates and
    refreshes the query plan but does not duplicate subscriptions.
    """
    async with session_scope() as s:
        row = await _mutable(s, topic_id, principal)
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
async def get_monitoring(topic_id: uuid.UUID, principal: CurrentPrincipal) -> dict[str, Any]:
    async with session_scope() as s:
        await _owned(s, topic_id, principal)
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
    principal: CurrentPrincipal,
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
) -> dict[str, Any]:
    """Update monitoring settings — notably turn the auto-refresh schedule on/off.

    Only provided fields change. Enabling the schedule requires an interval
    (either supplied here or already stored).
    """
    async with session_scope() as s:
        await _mutable(s, topic_id, principal)
        sub = (await s.execute(
            select(TopicSubscription).where(TopicSubscription.topic_id == topic_id)
        )).scalar_one_or_none()
        if sub is None:
            raise HTTPException(status_code=404, detail="no monitoring subscription")

        if body.max_age_hours is not None:
            sub.max_age_hours = body.max_age_hours

        if body.short_term_queries is not None:
            try:
                sub.short_term_queries = validate_short_term_queries(body.short_term_queries)
            except ValueError as exc:
                raise HTTPException(status_code=422, detail=str(exc)) from exc

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
        queries_count = len(sub.short_term_queries or [])

    await emit(topic_id, "monitor.updated", {
        "subscription_id": payload["subscription_id"],
        "schedule_enabled": payload["schedule_enabled"],
        "schedule_interval_hours": payload["schedule_interval_hours"],
        "max_age_hours": payload["max_age_hours"],
        "queries_count": queries_count,
    })
    return {**payload, "queries_count": queries_count}


@router.delete("/{topic_id}/monitor", status_code=status.HTTP_200_OK)
async def stop_monitoring(topic_id: uuid.UUID, principal: CurrentPrincipal) -> dict[str, Any]:
    async with session_scope() as s:
        await _mutable(s, topic_id, principal)
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
    principal: CurrentPrincipal,
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
) -> dict[str, Any]:
    """Trigger one refresh cycle. Idempotent if a refresh is already running.

    Returns 202 with `{accepted, subscription_id, queued}` immediately; watch
    SSE for `refresh.started` / `refresh.completed` events.
    """
    async with session_scope() as s:
        await _mutable(s, topic_id, principal)
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
async def get_deltas(
    topic_id: uuid.UUID, principal: CurrentPrincipal, limit: int = 50
) -> dict[str, Any]:
    await _load_topic(topic_id, principal)
    items = await list_deltas(topic_id, limit=limit)
    return {"deltas": items, "count": len(items)}


@router.get("/{topic_id}/deltas/{seq}")
async def get_delta(
    topic_id: uuid.UUID,
    seq: int,
    principal: CurrentPrincipal,
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
):
    async with session_scope() as s:
        topic_row = await _owned(s, topic_id, principal)
        row = (await s.execute(
            select(TopicRefreshDelta).where(
                TopicRefreshDelta.topic_id == topic_id,
                TopicRefreshDelta.seq == seq,
            )
        )).scalar_one_or_none()
        if row is None:
            raise HTTPException(status_code=404, detail="delta not found")
    return artifact_response(settings, topic_row.topic_id_hash, row.run_id, "delta.json")


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
    return build_short_term_queries(parsed, report, max_queries=settings.refresh_max_queries)


@router.get("/{topic_id}/events")
async def events(
    topic_id: uuid.UUID, request: Request, principal: CurrentPrincipal, from_seq: int = 0
):
    await _load_topic(topic_id, principal)

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


@router.get("/{topic_id}/parsed")
async def get_parsed(topic_id: uuid.UUID, principal: CurrentPrincipal,
                     settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]):
    row = await _load_topic(topic_id, principal)
    return artifact_response(settings, row.topic_id_hash, row.plan_run_id, "parsed.json")


@router.get("/{topic_id}/intro")
async def get_intro(topic_id: uuid.UUID, principal: CurrentPrincipal,
                    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]):
    row = await _load_topic(topic_id, principal)
    return artifact_response(settings, row.topic_id_hash, row.plan_run_id, "intro.json")


@router.get("/{topic_id}/intro.md")
async def get_intro_md(topic_id: uuid.UUID, principal: CurrentPrincipal,
                       settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]):
    row = await _load_topic(topic_id, principal)
    return artifact_response(settings, row.topic_id_hash, row.plan_run_id, "intro.md")


@router.get("/{topic_id}/news")
async def get_news(topic_id: uuid.UUID, principal: CurrentPrincipal,
                   settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]):
    row = await _load_topic(topic_id, principal)
    return artifact_response(settings, row.topic_id_hash, row.deliver_run_id, "news.json")


@router.get("/{topic_id}/report")
async def get_report(topic_id: uuid.UUID, principal: CurrentPrincipal,
                     settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]):
    row = await _load_topic(topic_id, principal)
    return artifact_response(settings, row.topic_id_hash, row.deliver_run_id, "report.json")


@router.get("/{topic_id}/source-mix")
async def get_source_mix(topic_id: uuid.UUID, principal: CurrentPrincipal,
                         settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]):
    """How authoritative this report's sources are, as the backend counted them (#51).

    404 on a run written before the run started recording it; the UI falls back
    to its own narrower count there and nowhere else.
    """
    row = await _load_topic(topic_id, principal)
    return artifact_response(
        settings, row.topic_id_hash, row.deliver_run_id, SOURCE_MIX_FILENAME
    )


@router.get("/{topic_id}/report.md")
async def get_report_md(topic_id: uuid.UUID, principal: CurrentPrincipal,
                        settings: Annotated[ClaudeAgentSettings, Depends(get_settings)]):
    row = await _load_topic(topic_id, principal)
    return artifact_response(settings, row.topic_id_hash, row.deliver_run_id, "report.md")


@router.get("/{topic_id}/deltas/{seq}/news")
async def get_delta_news(
    topic_id: uuid.UUID,
    seq: int,
    principal: CurrentPrincipal,
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
):
    """Serve news.json (searched sources + dedup stats) from a refresh run."""
    async with session_scope() as s:
        topic_row = await _owned(s, topic_id, principal)
        delta = (await s.execute(
            select(TopicRefreshDelta).where(
                TopicRefreshDelta.topic_id == topic_id,
                TopicRefreshDelta.seq == seq,
            )
        )).scalar_one_or_none()
        if delta is None:
            raise HTTPException(status_code=404, detail="delta not found")
    return artifact_response(settings, topic_row.topic_id_hash, delta.run_id, "news.json")


@router.get("/{topic_id}/deltas/{seq}/source-mix")
async def get_delta_source_mix(
    topic_id: uuid.UUID,
    seq: int,
    principal: CurrentPrincipal,
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
):
    """The same count for one refresh cycle (#51)."""
    async with session_scope() as s:
        topic_row = await _owned(s, topic_id, principal)
        delta = (await s.execute(
            select(TopicRefreshDelta).where(
                TopicRefreshDelta.topic_id == topic_id,
                TopicRefreshDelta.seq == seq,
            )
        )).scalar_one_or_none()
        if delta is None:
            raise HTTPException(status_code=404, detail="delta not found")
    return artifact_response(
        settings, topic_row.topic_id_hash, delta.run_id, SOURCE_MIX_FILENAME
    )


@router.get("/{topic_id}/deltas/{seq}/report")
async def get_delta_report(
    topic_id: uuid.UUID,
    seq: int,
    principal: CurrentPrincipal,
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
):
    """Serve report.md from a refresh run."""
    async with session_scope() as s:
        topic_row = await _owned(s, topic_id, principal)
        delta = (await s.execute(
            select(TopicRefreshDelta).where(
                TopicRefreshDelta.topic_id == topic_id,
                TopicRefreshDelta.seq == seq,
            )
        )).scalar_one_or_none()
        if delta is None:
            raise HTTPException(status_code=404, detail="delta not found")
    return artifact_response(settings, topic_row.topic_id_hash, delta.run_id, "report.md")
