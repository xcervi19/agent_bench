"""Pydantic schemas for the /v1/topics/* API."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, HttpUrl

IntroStyle = Literal["raw", "trader", "executive", "analyst"]
StageName = Literal["queries", "intro", "search", "report"]
GateName = Literal["planned_awaiting_review"]
InputKind = Literal["proceed", "focus", "clarify", "constraint"]


class WebhookSpec(BaseModel):
    url: HttpUrl
    secret: str | None = None
    event_filter: list[str] | None = None


class CreateTopicRequest(BaseModel):
    topic: str = Field(min_length=1)
    intro_style: IntroStyle = "raw"
    stages: list[StageName] = Field(
        default_factory=lambda: ["queries", "intro", "search", "report"]
    )
    gates: list[GateName] = Field(
        default_factory=lambda: ["planned_awaiting_review"]
    )
    force_refresh: bool = False
    timeout_sec: int | None = Field(default=None, ge=1)
    model: str | None = None
    webhook: WebhookSpec | None = None


class CreateTopicResponse(BaseModel):
    topic_id: uuid.UUID
    state: str
    events_url: str


class TopicArtifactsLinks(BaseModel):
    parsed: str | None = None
    intro: str | None = None
    intro_md: str | None = None
    news: str | None = None
    report: str | None = None
    report_md: str | None = None


class TopicResponse(BaseModel):
    id: uuid.UUID
    topic: str
    topic_id_hash: str
    state: str
    current_stage: str | None
    stages_done: list[str]
    artifacts: TopicArtifactsLinks
    available_actions: list[str]
    error: str | None
    error_type: str | None
    failed_at_stage: str | None
    created_at: datetime
    updated_at: datetime
    last_event_seq: int


class ProceedRequest(BaseModel):
    from_state: str | None = None


class ActionResponse(BaseModel):
    accepted: bool = True
    new_state: str | None = None
    applies_to_next_stage: str | None = None


class InputRequest(BaseModel):
    kind: InputKind
    payload: dict[str, Any] = Field(default_factory=dict)


class SubscriptionResponse(BaseModel):
    subscription_id: int


class EventOut(BaseModel):
    seq: int
    event_type: str
    event_version: str
    topic_id: uuid.UUID
    created_at: datetime
    payload: dict[str, Any]
