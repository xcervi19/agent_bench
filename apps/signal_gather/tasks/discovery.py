"""Background task: run the discovery crew for a tenant."""

from typing import Any
from uuid import UUID

from agentic_core.agents import CrewRunContext
from agentic_core.workers import task

from ..agents import DiscoveryCrew


@task("signal_gather.discover_market")
async def discover_market(tenant_id: UUID, payload: dict[str, Any]) -> dict[str, Any]:
    ctx = CrewRunContext(tenant_id=tenant_id, inputs=payload)
    result = await DiscoveryCrew().run(ctx)
    return {"session_id": str(result.session_id), "output": result.output}
