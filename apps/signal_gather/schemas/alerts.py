from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    signal_id: UUID | None
    severity: str
    title: str
    body: str
    channels: list[str]
    delivered: bool
    read: bool
    created_at: datetime


class AlertReadUpdate(BaseModel):
    read: bool
