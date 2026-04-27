"""Pull RSS feeds for a commodity, ingest new docs, queue extraction per doc."""

from typing import Any
from uuid import UUID

from agentic_core.database import session_scope
from agentic_core.workers import enqueue, task

from ..services import ingest_feed_item
from ..services.discovery import FEEDS_BY_COMMODITY, fetch_feed


@task("signal_gather.discover_market")
async def discover_market(tenant_id: UUID, payload: dict[str, Any]) -> dict[str, Any]:
    commodity = payload.get("commodity", "power")
    feeds = FEEDS_BY_COMMODITY.get(commodity, [])
    items = [item for url in feeds for item in fetch_feed(url)]

    new_doc_ids: list[str] = []
    async with session_scope() as db:
        for item in items:
            doc = await ingest_feed_item(db, tenant_id, item)
            if doc is not None:
                new_doc_ids.append(str(doc.id))

    for doc_id in new_doc_ids:
        enqueue(
            "signal_gather.extract_events",
            tenant_id=tenant_id,
            payload={"document_id": doc_id},
        )

    return {"commodity": commodity, "fetched": len(items), "new": len(new_doc_ids)}
