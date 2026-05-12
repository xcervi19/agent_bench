"""Shared types for stage runners."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class StageResult:
    status: str  # 'succeeded' | 'failed'
    run_id: str
    topic_id_hash: str
    artifact_paths: dict[str, str] = field(default_factory=dict)
    parsed: dict[str, Any] | None = None
    duration_ms: int | None = None
    total_cost_usd: float | None = None
    cached: bool = False
    error: str | None = None
    error_type: str | None = None
    traceback: str | None = None
    progress_events: list[dict[str, Any]] = field(default_factory=list)
