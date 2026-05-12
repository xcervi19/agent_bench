"""Stage 1 — queries. Wraps the existing ``run_newsfind_queries`` orchestrator."""

from __future__ import annotations

import json
import traceback
from pathlib import Path

from ...config import ClaudeAgentSettings
from ...orchestrator import run_newsfind_queries
from ...schemas import RunRequest
from .types import StageResult


async def run_queries_stage(
    *,
    topic: str,
    model: str | None,
    timeout_sec: int | None,
    force_refresh: bool,
    settings: ClaudeAgentSettings,
) -> StageResult:
    req = RunRequest(
        command="/newsfind-queries",
        args=topic,
        model=model,
        timeout_sec=timeout_sec,
        force_refresh=force_refresh,
        output_format="stream-json",
    )
    try:
        result = await run_newsfind_queries(req, settings)
    except Exception as exc:  # noqa: BLE001 — preserve full context in StageResult
        return StageResult(
            status="failed",
            run_id="",
            topic_id_hash="",
            error=f"{type(exc).__name__}: {exc}",
            error_type=type(exc).__name__,
            traceback=traceback.format_exc(),
        )

    if result.status != "succeeded" or result.parsed is None:
        return StageResult(
            status="failed",
            run_id=result.run_id or "",
            topic_id_hash=result.topic_id or "",
            error=result.error or "queries stage failed",
            traceback=result.stderr,
        )

    parsed_path = Path(result.parsed_path) if result.parsed_path else None
    return StageResult(
        status="succeeded",
        run_id=result.run_id or "",
        topic_id_hash=result.topic_id or "",
        artifact_paths={
            "parsed": str(parsed_path) if parsed_path else "",
        },
        parsed=result.parsed,
        duration_ms=result.duration_ms,
        total_cost_usd=result.total_cost_usd,
        cached=result.cached,
    )


def load_parsed(parsed_path: str) -> dict | None:
    p = Path(parsed_path)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
