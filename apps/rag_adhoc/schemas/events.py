from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class EventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    category: str
    commodity: str | None
    region: str | None
    occurred_at: datetime | None
    summary: str
    impact_score: float | None
