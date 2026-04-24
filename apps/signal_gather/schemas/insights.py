from uuid import UUID

from pydantic import BaseModel


class InsightRequest(BaseModel):
    query: str
    commodity: str | None = None
    region: str | None = None


class InsightResponse(BaseModel):
    session_id: UUID
    summary: str
    relevant_event_ids: list[UUID] = []
