from uuid import UUID

from fastapi import APIRouter, Depends

from agentic_core.api import get_current_user, require_tenant
from agentic_core.workers import enqueue

from ..schemas import ProfileSetupRequest

router = APIRouter(prefix="/setup", tags=["setup"])


@router.post("", status_code=202)
async def submit_setup(
    body: ProfileSetupRequest,
    user=Depends(get_current_user),
    tenant_id: UUID = Depends(require_tenant),
) -> dict[str, str]:
    job = enqueue(
        "signal_gather.setup_profile",
        tenant_id=tenant_id,
        payload={"text": body.text, "user_id": str(user.id)},
    )
    return {"task_id": job.id}
