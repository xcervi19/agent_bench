from pydantic import BaseModel

from .events import EventOut


class SearchRequest(BaseModel):
    query: str
    commodity: str | None = None
    region: str | None = None
    limit: int = 20


class SearchResponse(BaseModel):
    query: str
    results: list[EventOut]
