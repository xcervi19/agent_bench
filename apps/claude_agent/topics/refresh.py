"""Refresh cycle orchestration for v2 continuous monitoring.

Each refresh:
  1. Acquires the per-topic refresh lock (DB row update guarded by `refresh_locked`).
  2. Materializes a refresh run dir + input.json (short_term_queries, seen_url_hashes,
     since_iso, max_age_hours, plan_run_dir, previous_deliver_run_dir).
  3. Runs `/newsfind-refresh` slash command — it writes news.json (new sources only),
     delta.json, and summary.json to the run dir.
  4. Records a TopicRefreshDelta row and emits `refresh.started` / `refresh.completed`
     events on the topic event log so existing SSE clients see it transparently.
  5. Releases the lock.

Concurrency: per-topic lock prevents overlapping refreshes on the same topic.
Global throttle is provided by FastAPI BackgroundTasks + the existing
`max_concurrent_jobs` budget — fine for 3–6 concurrent users.
"""
from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime, timezone
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from sqlalchemy import desc, select, update

from ..config import ClaudeAgentSettings
from ..schemas import RunRequest
from ..runner import stream_claude
from .db import session_scope
from .models import Topic, TopicRefreshDelta, TopicSubscription
from .pipeline import emit, run_dir

logger = logging.getLogger(__name__)


REFRESH_COMMAND = "/newsfind-refresh"


# ---------------------------------------------------------------------------
# short-term query plan (built once when subscribing)
# ---------------------------------------------------------------------------


def _recency_hint(today_iso: str) -> str:
    return f"latest {today_iso[:7]}"  # e.g. "latest 2026-05"


def build_short_term_queries(
    parsed: dict[str, Any],
    report: dict[str, Any] | None,
    *,
    today_iso: str | None = None,
) -> list[dict[str, Any]]:
    """Synthesize the persistent monitoring query plan from plan + report state.

    Sources, in priority order:
      - `report.next_queries` if present (suggested by the deliver analyst)
      - top-priority `parsed.queries` annotated with a recency hint
      - tier-1 actors × `parsed.monitoring_plan.trigger_terms` as fallback

    Each entry: {id, query, language, priority, source}. IDs are `st01`, `st02`, …
    Capped at 12 queries to keep refresh cost bounded.
    """
    today_iso = today_iso or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    hint = _recency_hint(today_iso)
    out: list[dict[str, Any]] = []

    if isinstance(report, dict):
        for nq in (report.get("next_queries") or [])[:8]:
            q = (nq.get("q") or nq.get("query") or "").strip()
            if not q:
                continue
            text = f"{q} {hint}"
            out.append({
                "query": text,
                "language": nq.get("language", "en"),
                "priority": 1,
                "source": "report.next_queries",
                "rationale": nq.get("rationale") or nq.get("intent"),
            })

    seen = {e["query"].lower() for e in out}
    for q in sorted(parsed.get("queries") or [], key=lambda x: x.get("priority", 3)):
        if len(out) >= 12:
            break
        text = f"{q.get('query','').strip()} {hint}".strip()
        if not text or text.lower() in seen:
            continue
        seen.add(text.lower())
        out.append({
            "query": text,
            "language": q.get("language", "en"),
            "priority": q.get("priority", 2),
            "source": "parsed.queries",
            "rationale": q.get("rationale"),
        })

    if len(out) < 4:
        actors = (parsed.get("entities") or {}).get("actors") or []
        triggers = (parsed.get("monitoring_plan") or {}).get("trigger_terms") or []
        for a in actors[:3]:
            for t in triggers[:3]:
                if len(out) >= 12:
                    break
                text = f"{a.get('name', '')} {t} {hint}".strip()
                if text.lower() in seen:
                    continue
                seen.add(text.lower())
                out.append({
                    "query": text,
                    "language": "en",
                    "priority": 2,
                    "source": "monitoring_plan",
                    "rationale": "actor × trigger_term",
                })

    for i, q in enumerate(out, start=1):
        q["id"] = f"st{i:02d}"
    return out


# ---------------------------------------------------------------------------
# concurrency lock (advisory; DB-enforced)
# ---------------------------------------------------------------------------


async def _try_acquire_lock(subscription_id: int) -> bool:
    async with session_scope() as s:
        result = await s.execute(
            update(TopicSubscription)
            .where(
                TopicSubscription.id == subscription_id,
                TopicSubscription.refresh_locked.is_(False),
                TopicSubscription.status == "active",
            )
            .values(refresh_locked=True)
            .returning(TopicSubscription.id)
        )
        return result.scalar_one_or_none() is not None


async def _release_lock(subscription_id: int) -> None:
    async with session_scope() as s:
        await s.execute(
            update(TopicSubscription)
            .where(TopicSubscription.id == subscription_id)
            .values(refresh_locked=False)
        )


# ---------------------------------------------------------------------------
# refresh entry point (called from BackgroundTasks)
# ---------------------------------------------------------------------------


async def run_refresh(topic_id: uuid.UUID, subscription_id: int, settings: ClaudeAgentSettings) -> None:
    if not await _try_acquire_lock(subscription_id):
        await emit(topic_id, "refresh.skipped", {"reason": "already_running_or_paused"})
        return

    refresh_run_id = str(uuid.uuid4())
    delta_seq: int | None = None
    try:
        async with session_scope() as s:
            sub = await s.get(TopicSubscription, subscription_id)
            topic = await s.get(Topic, topic_id)
            if sub is None or topic is None:
                return
            seq = (sub.refresh_count or 0) + 1
            delta_seq = seq
            sub.last_refresh_run_id = refresh_run_id
            s.add(TopicRefreshDelta(
                topic_id=topic_id,
                subscription_id=subscription_id,
                seq=seq,
                run_id=refresh_run_id,
                status="running",
            ))
            short_term_queries = list(sub.short_term_queries or [])
            max_age_hours = int(sub.max_age_hours or 48)
            since_iso = (
                sub.last_refresh_at.astimezone(timezone.utc).isoformat()
                if sub.last_refresh_at is not None
                else None
            )
            plan_run_id = topic.plan_run_id
            previous_deliver_run_id = topic.deliver_run_id
            topic_hash = topic.topic_id_hash

        plan_dir = run_dir(settings.state_dir, topic_hash, plan_run_id) if plan_run_id else None
        prev_deliver_dir = (
            run_dir(settings.state_dir, topic_hash, previous_deliver_run_id)
            if previous_deliver_run_id
            else None
        )
        refresh_dir = run_dir(settings.state_dir, topic_hash, refresh_run_id)
        refresh_dir.mkdir(parents=True, exist_ok=True)

        seen_url_hashes = _collect_seen_url_hashes(topic_hash, settings, exclude_run_id=refresh_run_id)

        (refresh_dir / "input.json").write_text(
            json.dumps({
                "topic_id": str(topic_id),
                "run_id": refresh_run_id,
                "plan_run_dir": str(plan_dir) if plan_dir else None,
                "previous_deliver_run_dir": str(prev_deliver_dir) if prev_deliver_dir else None,
                "refresh_run_dir": str(refresh_dir),
                "short_term_queries": short_term_queries,
                "since_iso": since_iso,
                "max_age_hours": max_age_hours,
                "seen_url_hashes": sorted(seen_url_hashes),
                "today_iso": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            }),
            encoding="utf-8",
        )

        await emit(topic_id, "refresh.started", {
            "subscription_id": subscription_id,
            "refresh_seq": delta_seq,
            "run_id": refresh_run_id,
            "queries": len(short_term_queries),
        })

        cost, duration_ms, error, summary = await _run_refresh_slash(
            topic_id, refresh_dir, settings
        )

        new_count = 0
        queries_executed = 0
        summary_md: str | None = None
        if error is None and summary is not None:
            new_count = int(summary.get("new_sources_count") or 0)
            queries_executed = int(summary.get("queries_executed") or 0)
            summary_md = summary.get("summary_md")

        async with session_scope() as s:
            await s.execute(
                update(TopicRefreshDelta)
                .where(
                    TopicRefreshDelta.topic_id == topic_id,
                    TopicRefreshDelta.run_id == refresh_run_id,
                )
                .values(
                    status="completed" if error is None else "failed",
                    new_sources_count=new_count,
                    queries_executed=queries_executed,
                    duration_ms=duration_ms,
                    total_cost_usd=cost,
                    summary_md=summary_md,
                    error=error,
                )
            )
            sub = await s.get(TopicSubscription, subscription_id)
            if sub is not None and error is None:
                sub.last_refresh_at = datetime.now(timezone.utc)
                sub.refresh_count = (sub.refresh_count or 0) + 1

        if error is not None:
            await emit(topic_id, "refresh.failed", {
                "subscription_id": subscription_id,
                "refresh_seq": delta_seq,
                "run_id": refresh_run_id,
                "error": error,
            })
        else:
            await emit(topic_id, "refresh.completed", {
                "subscription_id": subscription_id,
                "refresh_seq": delta_seq,
                "run_id": refresh_run_id,
                "new_sources_count": new_count,
                "queries_executed": queries_executed,
                "duration_ms": duration_ms,
                "total_cost_usd": cost,
            })
    finally:
        await _release_lock(subscription_id)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _collect_seen_url_hashes(
    topic_hash: str, settings: ClaudeAgentSettings, *, exclude_run_id: str
) -> set[str]:
    """Union of url_hashes seen across all previous deliver + refresh runs."""
    base = Path(settings.state_dir) / "news" / topic_hash / "runs"
    seen: set[str] = set()
    if not base.exists():
        return seen
    for child in base.iterdir():
        if not child.is_dir() or child.name == exclude_run_id:
            continue
        news = child / "news.json"
        if not news.exists():
            continue
        try:
            doc = json.loads(news.read_text(encoding="utf-8"))
        except (JSONDecodeError, OSError):
            continue
        for src in (doc.get("sources") or []):
            h = src.get("url_hash")
            if isinstance(h, str) and h:
                seen.add(h)
    return seen


async def _run_refresh_slash(
    topic_id: uuid.UUID,
    refresh_dir: Path,
    settings: ClaudeAgentSettings,
) -> tuple[float | None, int | None, str | None, dict[str, Any] | None]:
    """Run /newsfind-refresh, streaming tool_use/tool_result events into the topic log.

    Returns (cost_usd, duration_ms, error, summary_dict).
    """
    req = RunRequest(
        command=REFRESH_COMMAND,
        args=str(refresh_dir),
        output_format="stream-json",
        timeout_sec=settings.max_timeout_sec,
    )
    cost: float | None = None
    duration_ms: int | None = None
    error: str | None = None
    success = False

    async for line in stream_claude(req, settings):
        event = _try_loads(line)
        if not isinstance(event, dict):
            continue
        kind = event.get("type")
        if kind == "assistant":
            for block in event.get("message", {}).get("content", []) or []:
                if block.get("type") == "tool_use":
                    await emit(topic_id, "tool_use", {
                        "tool": block.get("name"),
                        "tool_use_id": block.get("id"),
                        "input_preview": str(block.get("input"))[:400],
                        "phase": "refresh",
                    })
        elif kind == "user":
            for block in event.get("message", {}).get("content", []) or []:
                if block.get("type") == "tool_result":
                    await emit(topic_id, "tool_result", {
                        "tool_use_id": block.get("tool_use_id"),
                        "is_error": bool(block.get("is_error")),
                        "output_preview": _result_preview(block.get("content")),
                        "phase": "refresh",
                    })
        elif kind == "result":
            if event.get("subtype") == "success":
                cost = event.get("total_cost_usd")
                duration_ms = event.get("duration_ms")
                success = True
            else:
                error = f"result subtype={event.get('subtype')}"
        elif kind == "error":
            error = str(event.get("error") or "stream error")

    if error is None and not success:
        error = "agent produced no result event"

    summary: dict[str, Any] | None = None
    if error is None:
        try:
            data = json.loads((refresh_dir / "summary.json").read_text(encoding="utf-8"))
            if isinstance(data, dict):
                summary = data
            else:
                error = "summary.json is not a JSON object"
        except (FileNotFoundError, JSONDecodeError, OSError) as exc:
            error = f"summary.json invalid: {exc}"

    return cost, duration_ms, error, summary


def _try_loads(s: str | None) -> Any:
    if not s:
        return None
    try:
        return json.loads(s)
    except (JSONDecodeError, TypeError):
        return None


def _result_preview(content: Any) -> str:
    if isinstance(content, str):
        return content[:600]
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text", "")))
            else:
                parts.append(str(block))
        return " ".join(parts)[:600]
    return str(content)[:600]


# ---------------------------------------------------------------------------
# read helpers (used by routes)
# ---------------------------------------------------------------------------


async def list_deltas(topic_id: uuid.UUID, limit: int = 50) -> list[dict[str, Any]]:
    async with session_scope() as s:
        rows = (
            await s.execute(
                select(TopicRefreshDelta)
                .where(TopicRefreshDelta.topic_id == topic_id)
                .order_by(desc(TopicRefreshDelta.seq))
                .limit(limit)
            )
        ).scalars().all()
        return [
            {
                "seq": r.seq,
                "run_id": r.run_id,
                "status": r.status,
                "new_sources_count": r.new_sources_count,
                "queries_executed": r.queries_executed,
                "duration_ms": r.duration_ms,
                "total_cost_usd": r.total_cost_usd,
                "summary_md": r.summary_md,
                "error": r.error,
                "created_at": r.created_at.astimezone(timezone.utc).isoformat(),
            }
            for r in rows
        ]
