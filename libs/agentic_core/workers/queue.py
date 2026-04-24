"""Redis + RQ queue accessors. Tenant id is passed through job metadata."""

from functools import lru_cache
from typing import Any
from uuid import UUID

from redis import Redis
from rq import Queue
from rq.job import Job

from ..config import get_settings

DEFAULT_QUEUE = "default"


@lru_cache
def get_redis() -> Redis:
    return Redis.from_url(get_settings().redis_url)


@lru_cache
def get_queue(name: str = DEFAULT_QUEUE) -> Queue:
    return Queue(name=name, connection=get_redis())


def enqueue(
    task_name: str,
    *,
    tenant_id: UUID,
    payload: dict[str, Any],
    queue: str = DEFAULT_QUEUE,
) -> Job:
    """Enqueue a task by its registered name (resolved worker-side)."""
    q = get_queue(queue)
    return q.enqueue(
        "agentic_core.workers.runner.dispatch",
        task_name,
        str(tenant_id),
        payload,
        job_timeout=600,
    )
