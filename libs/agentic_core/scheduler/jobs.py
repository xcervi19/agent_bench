"""Thin APScheduler wrapper. Jobs enqueue tasks into RQ per tenant."""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from ..logging import get_logger
from ..workers import enqueue

log = get_logger(__name__)


@dataclass
class JobSpec:
    name: str
    task_name: str
    tenant_id: UUID
    cron: str | None = None
    interval_seconds: int | None = None
    payload: dict[str, Any] = field(default_factory=dict)

    def build_trigger(self):
        if self.cron:
            return CronTrigger.from_crontab(self.cron)
        if self.interval_seconds:
            return IntervalTrigger(seconds=self.interval_seconds)
        raise ValueError(f"Job {self.name} needs cron or interval_seconds")


class Scheduler:
    def __init__(self) -> None:
        self._scheduler = BlockingScheduler(timezone="UTC")

    def register(self, spec: JobSpec) -> None:
        self._scheduler.add_job(
            _enqueue_task,
            trigger=spec.build_trigger(),
            id=spec.name,
            name=spec.name,
            replace_existing=True,
            args=[spec.task_name, spec.tenant_id, spec.payload],
        )
        log.info("scheduler.registered", job=spec.name, task=spec.task_name)

    def register_many(self, specs: list[JobSpec]) -> None:
        for spec in specs:
            self.register(spec)

    def register_fn(
        self,
        name: str,
        fn: Callable[..., None],
        *,
        interval_seconds: int | None = None,
        cron: str | None = None,
        args: list | None = None,
    ) -> None:
        """Register a local callable (for non-task periodic work like dispatch fan-outs)."""
        trigger = (
            CronTrigger.from_crontab(cron)
            if cron
            else IntervalTrigger(seconds=interval_seconds or 60)
        )
        self._scheduler.add_job(
            fn, trigger, id=name, name=name, replace_existing=True, args=args or []
        )
        log.info("scheduler.fn_registered", job=name)

    def run(self) -> None:
        log.info("scheduler.start")
        self._scheduler.start()


def _enqueue_task(task_name: str, tenant_id: UUID, payload: dict[str, Any]) -> None:
    enqueue(task_name, tenant_id=tenant_id, payload=payload)
