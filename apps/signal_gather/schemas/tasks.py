from enum import Enum
from typing import Any

from pydantic import BaseModel


class TaskStatus(str, Enum):
    queued = "queued"
    started = "started"
    finished = "finished"
    failed = "failed"
    deferred = "deferred"


class TaskOut(BaseModel):
    task_id: str
    status: TaskStatus
    result: Any | None = None
    error: str | None = None
