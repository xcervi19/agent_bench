from fastapi import APIRouter, Depends, HTTPException
from rq.exceptions import NoSuchJobError
from rq.job import Job

from agentic_core.api import require_tenant
from agentic_core.workers import get_redis

from ..schemas import TaskOut, TaskStatus

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/{task_id}", response_model=TaskOut)
async def get_task(task_id: str, _=Depends(require_tenant)) -> TaskOut:
    job = _fetch_job(task_id)
    return TaskOut(
        task_id=job.id,
        status=_map_status(job.get_status(refresh=False)),
        result=job.result,
        error=str(job.exc_info) if job.exc_info else None,
    )


def _fetch_job(task_id: str) -> Job:
    try:
        return Job.fetch(task_id, connection=get_redis())
    except NoSuchJobError:
        raise HTTPException(status_code=404, detail="task not found") from None


def _map_status(raw: str) -> TaskStatus:
    mapping = {
        "queued": TaskStatus.queued,
        "started": TaskStatus.started,
        "finished": TaskStatus.finished,
        "failed": TaskStatus.failed,
        "deferred": TaskStatus.deferred,
    }
    return mapping.get(raw, TaskStatus.queued)
