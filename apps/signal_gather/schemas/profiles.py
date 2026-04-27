from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProfileSetupRequest(BaseModel):
    text: str


class ProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    display_name: str | None
    commodities: list[str]
    regions: list[str]
    themes: list[str]
    risk_appetite: str
    alert_channels: list[str]
    briefing_cadence: str
    impact_threshold: float


class ProfileUpdate(BaseModel):
    display_name: str | None = None
    commodities: list[str] | None = None
    regions: list[str] | None = None
    themes: list[str] | None = None
    risk_appetite: str | None = None
    alert_channels: list[str] | None = None
    briefing_cadence: str | None = None
    impact_threshold: float | None = None
