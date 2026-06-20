"""RAG adhoc API: same Postgres as main app, same retrieval; header-based tenant (no JWT).

Run:  uvicorn apps.rag_adhoc.app:app --host 0.0.0.0 --port 8001
Env:  RAG_ADHOC_DATABASE_URL, optional RAG_ADHOC_OPENAI_API_KEY, optional RAG_ADHOC_API_KEY
"""

from .bootstrap import bootstrap

bootstrap()

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from agentic_core.api.health import router as health_router
from agentic_core.database import current_tenant_id
from agentic_core.api.middleware import register_middleware
from agentic_core.logging import configure_logging

from .schemas import SearchRequest, SearchResponse
from .services import search_events_by_text

from .deps import get_adhoc_db

router = APIRouter(prefix="/v1", tags=["retrieval"])


@router.post("/search", response_model=SearchResponse)
async def search(
    body: SearchRequest,
    db: AsyncSession = Depends(get_adhoc_db),
) -> SearchResponse:
    tid = current_tenant_id()
    if tid is None:
        raise HTTPException(status_code=500, detail="Tenant context not set")
    events = await search_events_by_text(
        db,
        tid,
        body.query,
        commodity=body.commodity,
        region=body.region,
        limit=body.limit,
    )
    return SearchResponse(query=body.query, results=events)


def build_app() -> FastAPI:
    configure_logging()
    app = FastAPI(
        title="RAG adhoc (retrieval)",
        description="Semantic search over events; uses main DB + X-Tenant-Id + optional X-API-Key.",
    )
    register_middleware(app)
    app.include_router(health_router)
    app.include_router(router)
    return app


app = build_app()
