from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass(frozen=True)
class SourceTarget:
    url: str
    source_id: str | None = None
    hints: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SourceAssessment:
    adapter: str
    endpoint: str
    viable: bool
    reason: str
    proposed_config: SourceConfig | None = None


@dataclass(frozen=True)
class SourceConfig:
    source_id: str
    adapter: str
    endpoint: str
    title: str = ""
    publisher: str = ""
    enabled: bool = True
    interval_hours: int = 24
    watermark: str | None = None
    commodity: str = "crude_oil"
    region: str | None = None
    tier: int = 2
    domain: str = "trading_mechanics"
    promote: bool = False
    tags: tuple[str, ...] = ()
    # Human must ack labeling at enroll time (see docs/knowledge/rag_label_vocab.md).
    label_assignment: Literal["human", "agent"] | None = None
    document_type: str | None = None
    use_for: tuple[str, ...] = ()
    extras: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DocRef:
    url: str
    title: str = ""
    published_at: str | None = None
    content_type: str | None = None
    extras: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DownloadedDoc:
    ref: DocRef
    body: bytes
    content_type: str
    extension: str
    meta: dict[str, Any] = field(default_factory=dict)
