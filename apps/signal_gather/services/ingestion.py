"""Persist a discovered item: blob -> S3, metadata -> Postgres, embedding -> pgvector."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from agentic_core.storage import get_object_store

from ..models import Document
from .discovery import FeedItem
from .embeddings import embed


async def ingest_feed_item(
    db: AsyncSession, tenant_id: UUID, item: FeedItem
) -> Document | None:
    if not item.url:
        return None
    if await _already_ingested(db, tenant_id, item.url):
        return None

    s3_key = _store_raw(tenant_id, item)
    document = Document(
        id=uuid4(),
        tenant_id=tenant_id,
        source=item.source,
        url=item.url,
        title=item.title,
        language=item.language,
        s3_key=s3_key,
        content=_text_for_embedding(item),
        embedding=embed(_text_for_embedding(item)),
    )
    db.add(document)
    await db.flush()
    return document


async def _already_ingested(db: AsyncSession, tenant_id: UUID, url: str) -> bool:
    stmt = select(Document.id).where(Document.tenant_id == tenant_id, Document.url == url).limit(1)
    return (await db.execute(stmt)).scalar_one_or_none() is not None


def _store_raw(tenant_id: UUID, item: FeedItem) -> str:
    body = f"{item.title}\n\n{item.summary}".encode("utf-8")
    key = f"raw/{uuid4()}.txt"
    store = get_object_store()
    store.ensure_bucket()
    return store.put(tenant_id, key, body, content_type="text/plain")


def _text_for_embedding(item: FeedItem) -> str:
    return f"{item.title}. {item.summary}".strip()
