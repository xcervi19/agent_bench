from uuid import UUID

from fastapi import APIRouter, Depends

from agentic_core.api import require_tenant
from agentic_core.workers import enqueue

from ..schemas import InsightRequest

router = APIRouter(prefix="/insights", tags=["insights"])


@router.post("", status_code=202)
async def request_insight(
    body: InsightRequest,
    tenant_id: UUID = Depends(require_tenant),
) -> dict[str, str]:
    """Kick off a personalized insight crew. Returns a task id the client can poll."""
    job = enqueue(
        "signal_gather.generate_insight",
        tenant_id=tenant_id,
        payload=body.model_dump(),
    )
    return {"task_id": job.id}
