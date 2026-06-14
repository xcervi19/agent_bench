"""In-app topic refresh scheduler (#22).

Fires automatic refresh cycles for monitored topics that opted in
(`schedule_enabled` + `schedule_interval_hours`). It reuses the exact same
``run_refresh`` path as the manual ``POST /refresh`` endpoint, so scheduled and
manual cycles produce identical artifacts and SSE ``refresh.*`` events (only the
``trigger`` field differs).

Design:
  * **Interval-only** cadence (every N hours), not cron — matches the product UX.
  * **Single in-process async loop** started in the app lifespan (no extra
    container, no RQ). Fits the claude_agent single-service architecture.
  * **Default off per topic**; this loop only ever touches subscriptions that
    explicitly enabled scheduling.

The pure helpers (`normalize_interval`, `compute_next_refresh_at`, `is_due`) are
side-effect free and unit-tested offline.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import select

from ..config import ClaudeAgentSettings
from .db import session_scope
from .models import TopicSubscription
from .refresh import run_refresh

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# pure helpers (offline-testable)
# ---------------------------------------------------------------------------


def normalize_interval(hours: int | None, *, lo: int, hi: int) -> int | None:
    """Clamp a requested interval into [lo, hi]. None stays None."""
    if hours is None:
        return None
    return max(lo, min(hi, int(hours)))


def compute_next_refresh_at(now: datetime, interval_hours: int | None) -> datetime | None:
    """Next fire time = now + interval. None interval => no schedule."""
    if not interval_hours or interval_hours <= 0:
        return None
    return now + timedelta(hours=int(interval_hours))


def is_due(next_refresh_at: datetime | None, now: datetime) -> bool:
    """A subscription is due when it has a next time at or before now."""
    if next_refresh_at is None:
        return False
    return next_refresh_at <= now


# ---------------------------------------------------------------------------
# due-selection + dispatch
# ---------------------------------------------------------------------------


async def claim_due_subscriptions(
    now: datetime, limit: int
) -> list[tuple[uuid.UUID, int]]:
    """Atomically pick due subscriptions and advance their next_refresh_at.

    Advancing the timestamp at claim time (rather than after the run) prevents
    the same subscription being re-selected on the next poll while its refresh
    is still in flight. ``run_refresh`` separately holds the per-topic lock, so
    overlap is impossible even if a run outlasts its interval.

    Returns a list of (topic_id, subscription_id).
    """
    if limit <= 0:
        return []
    claimed: list[tuple[uuid.UUID, int]] = []
    async with session_scope() as s:
        rows = (
            await s.execute(
                select(TopicSubscription)
                .where(
                    TopicSubscription.status == "active",
                    TopicSubscription.schedule_enabled.is_(True),
                    TopicSubscription.refresh_locked.is_(False),
                    TopicSubscription.next_refresh_at.is_not(None),
                    TopicSubscription.next_refresh_at <= now,
                )
                .order_by(TopicSubscription.next_refresh_at.asc())
                .limit(limit)
                .with_for_update(skip_locked=True)
            )
        ).scalars().all()
        for sub in rows:
            sub.next_refresh_at = compute_next_refresh_at(now, sub.schedule_interval_hours)
            claimed.append((sub.topic_id, sub.id))
    return claimed


class RefreshScheduler:
    """Owns the polling loop and the set of in-flight scheduled refresh tasks."""

    def __init__(self, settings: ClaudeAgentSettings) -> None:
        self.settings = settings
        self._stop = asyncio.Event()
        self._task: asyncio.Task | None = None
        self._inflight: set[asyncio.Task] = set()

    @property
    def inflight_count(self) -> int:
        return len(self._inflight)

    def start(self) -> None:
        if self._task is not None:
            return
        self._stop.clear()
        self._task = asyncio.create_task(self._loop(), name="topic-refresh-scheduler")
        logger.info(
            "scheduler.started poll_interval=%ss max_concurrent=%s",
            self.settings.scheduler_poll_interval_sec,
            self.settings.scheduler_max_concurrent_refreshes,
        )

    async def stop(self) -> None:
        self._stop.set()
        if self._task is not None:
            await asyncio.gather(self._task, return_exceptions=True)
            self._task = None
        if self._inflight:
            await asyncio.gather(*self._inflight, return_exceptions=True)
        logger.info("scheduler.stopped")

    async def tick(self, now: datetime | None = None) -> int:
        """Run one scheduling pass. Returns number of refreshes dispatched.

        Exposed (besides the loop) so it can be driven deterministically in
        integration tests.
        """
        now = now or datetime.now(UTC)
        budget = self.settings.scheduler_max_concurrent_refreshes - self.inflight_count
        if budget <= 0:
            return 0
        try:
            claimed = await claim_due_subscriptions(now, budget)
        except Exception:  # pragma: no cover - DB hiccup shouldn't kill the loop
            logger.exception("scheduler.claim_failed")
            return 0
        for topic_id, subscription_id in claimed:
            self._dispatch(topic_id, subscription_id)
        return len(claimed)

    def _dispatch(self, topic_id: uuid.UUID, subscription_id: int) -> None:
        task = asyncio.create_task(
            run_refresh(topic_id, subscription_id, self.settings, trigger="scheduled"),
            name=f"scheduled-refresh-{subscription_id}",
        )
        self._inflight.add(task)
        task.add_done_callback(self._inflight.discard)
        logger.info("scheduler.dispatch topic=%s subscription=%s", topic_id, subscription_id)

    async def _loop(self) -> None:
        interval = self.settings.scheduler_poll_interval_sec
        while not self._stop.is_set():
            try:
                await self.tick()
            except Exception:  # pragma: no cover - defensive
                logger.exception("scheduler.tick_failed")
            with contextlib.suppress(TimeoutError):
                await asyncio.wait_for(self._stop.wait(), timeout=interval)
