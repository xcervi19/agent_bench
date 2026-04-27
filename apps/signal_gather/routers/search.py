from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from agentic_core.api import get_db, require_tenant

from ..schemas import SearchRequest, SearchResponse
from ..services import search_events_by_text

router = APIRouter(prefix="/search", tags=["search"])


@router.post("", response_model=SearchResponse)
async def search_events(
    body: SearchRequest,
    tenant_id: UUID = Depends(require_tenant),
    db: AsyncSession = Depends(get_db),
) -> SearchResponse:
    events = await search_events_by_text(
        db,
        tenant_id,
        body.query,
        commodity=body.commodity,
        region=body.region,
        limit=body.limit,
    )
    return SearchResponse(query=body.query, results=events)
