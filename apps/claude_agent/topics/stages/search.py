"""Stage 3 — search. Wraps the new ``/newsfind-search`` slash command.

The slash command runs WebSearch (and optionally WebFetch) over Stage-1's
``queries[]`` and emits ``news.json`` (deduplicated, scored sources). This
runner spawns the Claude CLI in stream-json mode, persists every event to
``stream.ndjson``, and writes the final ``news.json`` artifact.
"""

from __future__ import annotations

import json
import logging
import time
import traceback
import uuid
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

from ...artifacts import (
    ArtifactStore,
    RunRecorder,
    _write_json_atomic,  # type: ignore[attr-defined]
    file_sha1,
    parse_business_result,
)
from ...config import ClaudeAgentSettings
from ...runner import stream_claude
from ...schemas import RunRequest
from .types import StageResult

logger = logging.getLogger(__name__)

NEWSFIND_SEARCH_COMMAND = "/newsfind-search"
NEWSFIND_SEARCH_STAGE = "newsfind_search"
NEWSFIND_SEARCH_COMMAND_FILE = ".claude/commands/newsfind-search.md"
NEWSFIND_SEARCH_SCHEMA_FILE = ".claude/schemas/newsfind-search.schema.json"


def _safe_json_loads(line: str) -> Any:
    try:
        return json.loads(line)
    except (json.JSONDecodeError, TypeError):
        return None


async def run_search_stage(
    *,
    topic_id_hash: str,
    parsed_path: str,
    model: str | None,
    timeout_sec: int | None,
    settings: ClaudeAgentSettings,
    progress: AsyncIterator[dict[str, Any]] | None = None,  # placeholder
) -> StageResult:
    """Run /newsfind-search and capture artifacts. Returns once the CLI exits."""
    started = time.monotonic()

    if not parsed_path or not Path(parsed_path).exists():
        return StageResult(
            status="failed",
            run_id="",
            topic_id_hash=topic_id_hash,
            error=f"parsed_path missing: {parsed_path}",
            error_type="FileNotFoundError",
        )

    run_id = str(uuid.uuid4())
    store = ArtifactStore(
        Path(settings.state_dir),
        index_path_prefix=settings.state_index_prefix,
    )

    workspace = Path(settings.workspace_dir)
    command_file_hash = file_sha1(workspace / NEWSFIND_SEARCH_COMMAND_FILE)
    schema_hash = file_sha1(workspace / NEWSFIND_SEARCH_SCHEMA_FILE)
    if not command_file_hash:
        return StageResult(
            status="failed",
            run_id=run_id,
            topic_id_hash=topic_id_hash,
            error=(
                "newsfind-search slash command missing in workspace "
                f"({workspace / NEWSFIND_SEARCH_COMMAND_FILE})"
            ),
            error_type="FileNotFoundError",
        )

    try:
        rec = RunRecorder(
            store,
            topic=parsed_path,
            topic_id=topic_id_hash,
            run_id=run_id,
            stage=NEWSFIND_SEARCH_STAGE,
        )
        rec.write_request(
            {
                "command": NEWSFIND_SEARCH_COMMAND,
                "args": parsed_path,
                "output_format": "stream-json",
                "model": model or settings.default_model,
                "timeout_sec": timeout_sec or settings.default_timeout_sec,
                "command_file_hash": command_file_hash,
                "schema_hash": schema_hash,
            }
        )
        rec.open_stream()
    except Exception as exc:  # noqa: BLE001
        logger.exception("search setup error topic_id_hash=%s", topic_id_hash)
        return StageResult(
            status="failed",
            run_id=run_id,
            topic_id_hash=topic_id_hash,
            error=f"setup error: {type(exc).__name__}: {exc}",
            error_type=type(exc).__name__,
            traceback=traceback.format_exc(),
        )

    req = RunRequest(
        command=NEWSFIND_SEARCH_COMMAND,
        args=parsed_path,
        model=model,
        timeout_sec=timeout_sec or settings.default_timeout_sec,
        output_format="stream-json",
    )

    raw_result: dict[str, Any] | None = None
    error: str | None = None
    error_tb: str | None = None
    progress_events: list[dict[str, Any]] = []

    # The slash command isn't in the default allowlist — temporarily widen it.
    settings_with_cmd = _maybe_extend_allowlist(settings, NEWSFIND_SEARCH_COMMAND)

    try:
        async for line in stream_claude(req, settings_with_cmd):
            rec.append_stream_line(line)
            event = _safe_json_loads(line)
            if isinstance(event, dict):
                if event.get("type") == "result":
                    raw_result = event
                elif event.get("type") == "error":
                    error = str(event.get("error") or "stream error")
                # Capture {"phase":...} progress markers from Bash echoes.
                phase = event.get("phase")
                if isinstance(phase, str):
                    progress_events.append(
                        {
                            "phase": phase,
                            "status": event.get("status"),
                            "label": event.get("label"),
                        }
                    )
    except Exception as exc:  # noqa: BLE001
        error = f"runner error: {type(exc).__name__}: {exc}"
        error_tb = traceback.format_exc()
        logger.exception("search runner error topic_id_hash=%s", topic_id_hash)

    parsed = parse_business_result(raw_result)
    duration_ms = int((time.monotonic() - started) * 1000)
    if isinstance(raw_result, dict):
        if isinstance(raw_result.get("duration_ms"), int):
            duration_ms = raw_result["duration_ms"]
    total_cost_usd: float | None = None
    if isinstance(raw_result, dict) and isinstance(
        raw_result.get("total_cost_usd"), (int, float)
    ):
        total_cost_usd = float(raw_result["total_cost_usd"])

    status = "succeeded" if parsed is not None and error is None else "failed"

    # Write Stage-3 artifact: news.json (in addition to the standard parsed.json
    # that RunRecorder.finalize will write — we keep both for back-compat).
    news_path: Path | None = None
    if parsed is not None:
        news_path = rec.dir / "news.json"
        _write_json_atomic(news_path, parsed)

    rec.finalize(
        status=status,
        raw_result=raw_result,
        parsed=parsed,
        input_fingerprint=f"search:{command_file_hash}:{schema_hash}:{topic_id_hash}",
        model=model or settings.default_model,
        cached=False,
        duration_ms=duration_ms,
        total_cost_usd=total_cost_usd,
        error=error,
    )

    if status == "succeeded" and news_path is not None:
        _update_index(store, topic_id_hash, news_path)

    return StageResult(
        status=status,
        run_id=run_id,
        topic_id_hash=topic_id_hash,
        artifact_paths={
            "news": str(news_path) if news_path else "",
            "parsed": str(rec.parsed_path) if parsed is not None else "",
        },
        parsed=parsed,
        duration_ms=duration_ms,
        total_cost_usd=total_cost_usd,
        cached=False,
        error=error,
        traceback=error_tb,
        progress_events=progress_events,
    )


def _maybe_extend_allowlist(
    settings: ClaudeAgentSettings, command: str
) -> ClaudeAgentSettings:
    if not settings.allowed_commands or command in settings.allowed_commands:
        return settings
    extended = settings.allowed_commands + [command]
    return settings.model_copy(update={"allowed_commands": extended})


def _update_index(
    store: ArtifactStore, topic_id_hash: str, news_path: Path
) -> None:
    index_path = store.index_path(topic_id_hash)
    if not index_path.exists():
        return
    try:
        idx = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    prefix = f"{store.index_path_prefix}/" if store.index_path_prefix else ""
    rel = (
        f"{prefix}news/{topic_id_hash}/runs/{news_path.parent.name}/news.json"
    )
    idx["latest_news_path"] = rel
    idx["latest_search_run_id"] = news_path.parent.name
    _write_json_atomic(index_path, idx)
