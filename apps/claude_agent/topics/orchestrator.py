"""Per-topic asyncio orchestrator.

Drives a single topic forward through Stages 1 → 2 → [GATE] → 3 → 4, emitting
structured events at every transition. Each topic gets one ``asyncio.Task``
managed by :class:`TopicSupervisor`, capped by a global semaphore.

Resumability (Phase 1, single-process):
* On API startup, :meth:`TopicSupervisor.resume_in_flight` scans Postgres for
  topics in ``planning|searching|reporting`` and re-enqueues them. Stage 1 is
  fingerprint-cached, so re-running it is cheap.
* Topics in ``planned_awaiting_review`` simply remain idle; the
  :meth:`proceed` API call wakes them.
"""

from __future__ import annotations

import asyncio
import logging
import traceback
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..artifacts import topic_id_from_args
from ..config import ClaudeAgentSettings
from .db import session_scope
from .events import EventBus, emit
from .models import Topic
from .stages.intro import run_intro_stage
from .stages.queries import run_queries_stage
from .stages.report import run_report_stage
from .stages.search import run_search_stage
from .stages.types import StageResult
from .state import RESUMABLE_STATES, Stage, TopicState, can_transition
from .webhooks import schedule_webhook_delivery

logger = logging.getLogger(__name__)


class TopicSupervisor:
    """Owns the lifecycle of all in-process topic tasks.

    Designed so the API request handlers and the orchestrator share NOTHING
    in memory except this supervisor + the EventBus — everything else flows
    through Postgres. That makes a future Phase 2 (separate worker process)
    a small refactor.
    """

    def __init__(self, settings: ClaudeAgentSettings, bus: EventBus) -> None:
        self.settings = settings
        self.bus = bus
        self._tasks: dict[uuid.UUID, asyncio.Task[None]] = {}
        self._proceed_events: dict[uuid.UUID, asyncio.Event] = {}
        self._semaphore = asyncio.Semaphore(settings.max_concurrent_topics)
        self._lock = asyncio.Lock()

    # ---- public API ----------------------------------------------------

    async def start_topic(self, topic_id: uuid.UUID) -> None:
        """Spawn the orchestration task for a freshly-created topic."""
        async with self._lock:
            if topic_id in self._tasks and not self._tasks[topic_id].done():
                return
            task = asyncio.create_task(
                self._drive_topic(topic_id),
                name=f"topic-{topic_id}",
            )
            self._tasks[topic_id] = task

    async def signal_proceed(self, topic_id: uuid.UUID) -> None:
        """Wake the orchestrator task waiting at the gate."""
        ev = self._proceed_events.get(topic_id)
        if ev is not None:
            ev.set()

    async def cancel(self, topic_id: uuid.UUID) -> bool:
        """Cancel the orchestration task. Returns True if a task was killed."""
        task = self._tasks.get(topic_id)
        if task is None or task.done():
            return False
        task.cancel()
        try:
            await asyncio.wait_for(task, timeout=5.0)
        except (asyncio.CancelledError, asyncio.TimeoutError):
            pass
        return True

    async def shutdown(self) -> None:
        async with self._lock:
            tasks = [t for t in self._tasks.values() if not t.done()]
        for t in tasks:
            t.cancel()
        for t in tasks:
            try:
                await asyncio.wait_for(t, timeout=5.0)
            except (asyncio.CancelledError, asyncio.TimeoutError):
                pass

    async def resume_in_flight(self) -> int:
        """On startup, restart any topic that was mid-pipeline."""
        async with session_scope() as s:
            stmt = select(Topic.id, Topic.state).where(
                Topic.state.in_([str(x) for x in RESUMABLE_STATES])
            )
            rows = (await s.execute(stmt)).all()
        for topic_id, state in rows:
            logger.info("resuming topic id=%s state=%s", topic_id, state)
            await self.start_topic(topic_id)
        return len(rows)

    # ---- core driver ---------------------------------------------------

    async def _drive_topic(self, topic_id: uuid.UUID) -> None:
        async with self._semaphore:
            try:
                await self._run_pipeline(topic_id)
            except asyncio.CancelledError:
                await self._mark_cancelled(topic_id)
                raise
            except Exception as exc:  # noqa: BLE001 — last-ditch failure capture
                logger.exception("topic_supervisor unhandled error topic_id=%s", topic_id)
                await self._mark_failed(
                    topic_id,
                    stage="orchestrator",
                    error_type=type(exc).__name__,
                    error=str(exc),
                    tb=traceback.format_exc(),
                )

    async def _run_pipeline(self, topic_id: uuid.UUID) -> None:
        topic_row = await self._load_topic(topic_id)
        if topic_row is None:
            logger.warning("topic vanished mid-flight topic_id=%s", topic_id)
            return

        request: dict[str, Any] = topic_row.request or {}
        stages_requested: list[str] = request.get("stages") or [
            "queries",
            "intro",
            "search",
            "report",
        ]
        gates_requested: list[str] = request.get("gates") or [
            "planned_awaiting_review"
        ]
        gate_after_intro = "planned_awaiting_review" in gates_requested

        # ----- Stage 1: queries -----
        if "queries" in stages_requested and topic_row.queries_run_id is None:
            await self._transition(topic_id, TopicState.PLANNING, current_stage="queries")
            await self._publish(
                topic_id,
                "stage.started",
                {"stage": Stage.QUERIES, "run_id": None},
            )
            stage_res = await run_queries_stage(
                topic=topic_row.topic,
                model=request.get("model"),
                timeout_sec=request.get("timeout_sec"),
                force_refresh=bool(request.get("force_refresh")),
                settings=self.settings,
            )
            if stage_res.status != "succeeded":
                return await self._handle_stage_failure(
                    topic_id, Stage.QUERIES, stage_res
                )
            await self._record_stage_done(
                topic_id,
                stage=Stage.QUERIES,
                run_id=stage_res.run_id,
                topic_id_hash=stage_res.topic_id_hash,
                artifact_path=stage_res.artifact_paths.get("parsed"),
                cached=stage_res.cached,
                duration_ms=stage_res.duration_ms,
                total_cost_usd=stage_res.total_cost_usd,
            )
            topic_row = await self._load_topic(topic_id)
            assert topic_row is not None

        # ----- Stage 2: intro (pure Python) -----
        if "intro" in stages_requested and topic_row.intro_run_id is None:
            await self._touch_stage(topic_id, "intro")
            await self._publish(
                topic_id,
                "stage.started",
                {"stage": Stage.INTRO, "run_id": topic_row.queries_run_id},
            )
            intro_res = await run_intro_stage(
                topic_id_hash=topic_row.topic_id_hash,
                queries_run_id=topic_row.queries_run_id or "",
                style=str(request.get("intro_style") or "raw"),
                settings=self.settings,
            )
            if intro_res.status != "succeeded":
                return await self._handle_stage_failure(
                    topic_id, Stage.INTRO, intro_res
                )
            await self._record_stage_done(
                topic_id,
                stage=Stage.INTRO,
                run_id=intro_res.run_id,
                topic_id_hash=topic_row.topic_id_hash,
                artifact_path=intro_res.artifact_paths.get("intro_json"),
                duration_ms=intro_res.duration_ms,
                total_cost_usd=intro_res.total_cost_usd,
            )
            await self._publish(
                topic_id,
                "intro.ready",
                {
                    "summary_short": (intro_res.parsed or {}).get("understanding", ""),
                    "highlights": (intro_res.parsed or {}).get("highlights", []),
                },
            )
            topic_row = await self._load_topic(topic_id)
            assert topic_row is not None

        # ----- Gate after Stage 1+2 -----
        if gate_after_intro and topic_row.state == TopicState.PLANNING:
            await self._transition(
                topic_id, TopicState.PLANNED_AWAITING_REVIEW, current_stage=None
            )
            await self._publish(
                topic_id,
                "needs_input",
                {
                    "gate": "planned_awaiting_review",
                    "prompt": "Review the query plan + intro and press Proceed.",
                    "available_inputs": ["proceed", "focus", "clarify", "constraint"],
                },
            )
            await self._wait_for_proceed(topic_id)
            topic_row = await self._load_topic(topic_id)
            if topic_row is None or topic_row.state != TopicState.SEARCHING:
                # User cancelled or state moved sideways — bail out cleanly.
                return

        # ----- Stage 3: search -----
        if "search" in stages_requested and topic_row.search_run_id is None:
            if topic_row.state != TopicState.SEARCHING:
                await self._transition(
                    topic_id, TopicState.SEARCHING, current_stage="search"
                )
            parsed_path = self._resolve_parsed_path(
                topic_row.topic_id_hash, topic_row.queries_run_id or ""
            )
            await self._publish(
                topic_id, "stage.started", {"stage": Stage.SEARCH, "run_id": None}
            )
            search_res = await run_search_stage(
                topic_id_hash=topic_row.topic_id_hash,
                parsed_path=parsed_path,
                model=request.get("model"),
                timeout_sec=request.get("timeout_sec"),
                settings=self.settings,
            )
            if search_res.status != "succeeded":
                return await self._handle_stage_failure(
                    topic_id, Stage.SEARCH, search_res
                )
            await self._record_stage_done(
                topic_id,
                stage=Stage.SEARCH,
                run_id=search_res.run_id,
                topic_id_hash=topic_row.topic_id_hash,
                artifact_path=search_res.artifact_paths.get("news"),
                duration_ms=search_res.duration_ms,
                total_cost_usd=search_res.total_cost_usd,
            )
            news_payload = search_res.parsed or {}
            await self._publish(
                topic_id,
                "news.batch_done",
                {
                    "count": len(news_payload.get("sources") or []),
                    "drops": news_payload.get("drops") or {},
                },
            )
            await self._transition(
                topic_id, TopicState.SEARCHED, current_stage="search"
            )
            topic_row = await self._load_topic(topic_id)
            assert topic_row is not None

        # ----- Stage 4: report -----
        if "report" in stages_requested and topic_row.report_run_id is None:
            await self._transition(
                topic_id, TopicState.REPORTING, current_stage="report"
            )
            parsed_path = self._resolve_parsed_path(
                topic_row.topic_id_hash, topic_row.queries_run_id or ""
            )
            news_path = self._resolve_news_path(
                topic_row.topic_id_hash, topic_row.search_run_id or ""
            )
            await self._publish(
                topic_id, "stage.started", {"stage": Stage.REPORT, "run_id": None}
            )
            report_res = await run_report_stage(
                topic_id_hash=topic_row.topic_id_hash,
                parsed_path=parsed_path,
                news_path=news_path,
                model=request.get("model"),
                timeout_sec=request.get("timeout_sec"),
                settings=self.settings,
            )
            if report_res.status != "succeeded":
                return await self._handle_stage_failure(
                    topic_id, Stage.REPORT, report_res
                )
            await self._record_stage_done(
                topic_id,
                stage=Stage.REPORT,
                run_id=report_res.run_id,
                topic_id_hash=topic_row.topic_id_hash,
                artifact_path=report_res.artifact_paths.get("report_json"),
                duration_ms=report_res.duration_ms,
                total_cost_usd=report_res.total_cost_usd,
            )
            payload = report_res.parsed or {}
            await self._publish(
                topic_id,
                "report.ready",
                {
                    "summary_md": payload.get("summary_md", ""),
                    "thesis_status": payload.get("thesis_status", "inconclusive"),
                },
            )
            await self._transition(
                topic_id, TopicState.REPORTED, current_stage=None
            )

    # ---- gate handling -------------------------------------------------

    async def _wait_for_proceed(self, topic_id: uuid.UUID) -> None:
        """Block until either the proceed event fires or the topic is cancelled."""
        ev = self._proceed_events.setdefault(topic_id, asyncio.Event())
        # Poll DB every few seconds in case the proceed signal came in before
        # the in-memory event was registered (e.g. across a process restart).
        while True:
            try:
                await asyncio.wait_for(ev.wait(), timeout=5.0)
                ev.clear()
            except asyncio.TimeoutError:
                pass
            row = await self._load_topic(topic_id)
            if row is None:
                return
            if row.state == TopicState.SEARCHING:
                return
            if row.state in (TopicState.CANCELLED, TopicState.ARCHIVED):
                return

    # ---- DB helpers ----------------------------------------------------

    async def _load_topic(self, topic_id: uuid.UUID) -> Topic | None:
        async with session_scope() as s:
            return await s.get(Topic, topic_id)

    async def _publish(
        self, topic_id: uuid.UUID, event_type: str, payload: dict[str, Any]
    ) -> None:
        async with session_scope() as s:
            event = await emit(
                s, self.bus, topic_id=topic_id, event_type=event_type, payload=payload
            )
        # Webhook delivery is fire-and-forget so it never blocks the pipeline.
        asyncio.create_task(
            schedule_webhook_delivery(topic_id, event, self.settings),
            name=f"webhook-{event.seq}",
        )

    async def _transition(
        self,
        topic_id: uuid.UUID,
        new_state: TopicState,
        *,
        current_stage: str | None,
    ) -> None:
        async with session_scope() as s:
            row = await s.get(Topic, topic_id)
            if row is None:
                return
            old_state = TopicState(row.state)
            if old_state == new_state:
                return
            if not can_transition(old_state, new_state):
                logger.warning(
                    "illegal transition topic_id=%s from=%s to=%s — coercing",
                    topic_id,
                    old_state,
                    new_state,
                )
            row.state = new_state.value
            row.current_stage = current_stage
            await emit(
                s,
                self.bus,
                topic_id=topic_id,
                event_type="state.changed",
                payload={"from": old_state.value, "to": new_state.value},
            )

    async def _record_stage_done(
        self,
        topic_id: uuid.UUID,
        *,
        stage: Stage,
        run_id: str,
        topic_id_hash: str,
        artifact_path: str | None,
        cached: bool = False,
        duration_ms: int | None = None,
        total_cost_usd: float | None = None,
    ) -> None:
        async with session_scope() as s:
            row = await s.get(Topic, topic_id)
            if row is None:
                return
            if not row.topic_id_hash:
                row.topic_id_hash = topic_id_hash
            if stage == Stage.QUERIES:
                row.queries_run_id = run_id
            elif stage == Stage.INTRO:
                row.intro_run_id = run_id
            elif stage == Stage.SEARCH:
                row.search_run_id = run_id
            elif stage == Stage.REPORT:
                row.report_run_id = run_id
            await emit(
                s,
                self.bus,
                topic_id=topic_id,
                event_type="stage.finished",
                payload={
                    "stage": stage.value,
                    "run_id": run_id,
                    "artifact_path": artifact_path,
                    "cached": cached,
                    "duration_ms": duration_ms,
                    "total_cost_usd": total_cost_usd,
                },
            )

    async def _touch_stage(self, topic_id: uuid.UUID, current_stage: str) -> None:
        async with session_scope() as s:
            row = await s.get(Topic, topic_id)
            if row is None:
                return
            row.current_stage = current_stage

    async def _handle_stage_failure(
        self, topic_id: uuid.UUID, stage: Stage, res: StageResult
    ) -> None:
        await self._mark_failed(
            topic_id,
            stage=stage.value,
            error_type=res.error_type or "StageFailed",
            error=res.error or f"{stage.value} failed",
            tb=res.traceback,
        )

    async def _mark_failed(
        self,
        topic_id: uuid.UUID,
        *,
        stage: str,
        error_type: str,
        error: str,
        tb: str | None,
    ) -> None:
        async with session_scope() as s:
            row = await s.get(Topic, topic_id)
            if row is None:
                return
            row.state = TopicState.FAILED.value
            row.failed_at_stage = stage
            row.error = error
            row.error_type = error_type
            row.traceback = tb
            await emit(
                s,
                self.bus,
                topic_id=topic_id,
                event_type="error",
                payload={
                    "stage": stage,
                    "error_type": error_type,
                    "error": error,
                    "traceback": tb,
                },
            )
            await emit(
                s,
                self.bus,
                topic_id=topic_id,
                event_type="state.changed",
                payload={"from": "*", "to": TopicState.FAILED.value, "reason": error},
            )

    async def _mark_cancelled(self, topic_id: uuid.UUID) -> None:
        async with session_scope() as s:
            row = await s.get(Topic, topic_id)
            if row is None:
                return
            if row.state in (
                TopicState.REPORTED.value,
                TopicState.FAILED.value,
                TopicState.CANCELLED.value,
                TopicState.ARCHIVED.value,
            ):
                return
            old = row.state
            row.state = TopicState.CANCELLED.value
            await emit(
                s,
                self.bus,
                topic_id=topic_id,
                event_type="cancelled",
                payload={"from": old},
            )
            await emit(
                s,
                self.bus,
                topic_id=topic_id,
                event_type="state.changed",
                payload={"from": old, "to": TopicState.CANCELLED.value},
            )

    # ---- artifact path resolvers ---------------------------------------

    def _resolve_parsed_path(self, topic_id_hash: str, run_id: str) -> str:
        return str(
            Path(self.settings.state_dir)
            / "news"
            / topic_id_hash
            / "runs"
            / run_id
            / "parsed.json"
        )

    def _resolve_news_path(self, topic_id_hash: str, run_id: str) -> str:
        return str(
            Path(self.settings.state_dir)
            / "news"
            / topic_id_hash
            / "runs"
            / run_id
            / "news.json"
        )


def topic_id_hash_for(topic: str) -> str:
    return topic_id_from_args(topic)


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
