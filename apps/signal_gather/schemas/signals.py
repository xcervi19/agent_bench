from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SignalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    kind: str
    commodity: str | None
    region: str | None
    direction: str
    confidence: float
    rationale: str
