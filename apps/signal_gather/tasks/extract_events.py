"""Run document intelligence on a stored document and persist extracted events."""

from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import select

from agentic_core.agents import CrewRunContext
from agentic_core.database import session_scope
from agentic_core.workers import task

from ..agents import DocumentIntelligenceCrew
from ..agents.parsing import parse_json_array
from ..models import Document, Event
from ..services.embeddings import embed


@task("signal_gather.extract_events")
async def extract_events(tenant_id: UUID, payload: dict[str, Any]) -> dict[str, Any]:
    document_id = UUID(payload["document_id"])
    document = await _load_document(tenant_id, document_id)
    if document is None or not document.content:
        return {"document_id": str(document_id), "events": 0}

    raw = await _run_extraction_crew(tenant_id, document)
    extracted = parse_json_array(raw)

    persisted = await _persist_events(tenant_id, document, extracted)
    return {"document_id": str(document_id), "events": persisted}


async def _load_document(tenant_id: UUID, document_id: UUID) -> Document | None:
    async with session_scope() as db:
        stmt = select(Document).where(
            Document.tenant_id == tenant_id, Document.id == document_id
        )
        return (await db.execute(stmt)).scalar_one_or_none()


async def _run_extraction_crew(tenant_id: UUID, document: Document) -> Any:
    ctx = CrewRunContext(
        tenant_id=tenant_id,
        inputs={"text": document.content, "title": document.title or ""},
    )
    result = await DocumentIntelligenceCrew().run(ctx)
    return result.output


async def _persist_events(tenant_id: UUID, document: Document, items: list[dict]) -> int:
    if not items:
        return 0
    async with session_scope() as db:
        for item in items:
            db.add(_build_event(tenant_id, document.id, item))
    return len(items)


def _build_event(tenant_id: UUID, document_id: UUID, item: dict) -> Event:
    summary = (item.get("summary") or "").strip()
    return Event(
        id=uuid4(),
        tenant_id=tenant_id,
        document_id=document_id,
        category=item.get("category") or "uncategorized",
        commodity=item.get("commodity"),
        region=item.get("region"),
        occurred_at=None,
        summary=summary,
        entities=item.get("entities") or {},
        impact_score=_to_float(item.get("impact_score")),
        embedding=embed(summary) if summary else None,
    )


def _to_float(value: Any) -> float | None:
    if value is None:
        return None
    return float(value)
