"""Worker entrypoint: dispatches RQ jobs to registered task handlers."""

import asyncio
from typing import Any
from uuid import UUID

from rq import Worker

from ..database import tenant_scope
from ..logging import get_logger
from .queue import DEFAULT_QUEUE, get_queue, get_redis
from .registry import TASK_REGISTRY

log = get_logger(__name__)


def dispatch(task_name: str, tenant_id: str, payload: dict[str, Any]) -> Any:
    """Invoked inside the RQ worker. Resolves registered handler and runs it."""
    handler = TASK_REGISTRY[task_name]
    tid = UUID(tenant_id)
    log.info("task.start", task=task_name, tenant_id=tenant_id)

    with tenant_scope(tid):
        result = handler(tid, payload)
        if asyncio.iscoroutine(result):
            result = asyncio.run(result)

    log.info("task.done", task=task_name, tenant_id=tenant_id)
    return result


def run_worker(queues: list[str] | None = None) -> None:
    queue_names = queues or [DEFAULT_QUEUE]
    worker = Worker([get_queue(q) for q in queue_names], connection=get_redis())
    worker.work(with_scheduler=True)
