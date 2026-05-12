"""Stage 4 — report. Wraps the new ``/newsfind-report`` slash command."""

from __future__ import annotations

import json
import logging
import time
import traceback
import uuid
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

NEWSFIND_REPORT_COMMAND = "/newsfind-report"
NEWSFIND_REPORT_STAGE = "newsfind_report"
NEWSFIND_REPORT_COMMAND_FILE = ".claude/commands/newsfind-report.md"
NEWSFIND_REPORT_SCHEMA_FILE = ".claude/schemas/newsfind-report.schema.json"


def _safe_json_loads(line: str) -> Any:
    try:
        return json.loads(line)
    except (json.JSONDecodeError, TypeError):
        return None


async def run_report_stage(
    *,
    topic_id_hash: str,
    parsed_path: str,
    news_path: str,
    model: str | None,
    timeout_sec: int | None,
    settings: ClaudeAgentSettings,
) -> StageResult:
    started = time.monotonic()

    if not parsed_path or not Path(parsed_path).exists():
        return StageResult(
            status="failed",
            run_id="",
            topic_id_hash=topic_id_hash,
            error=f"parsed_path missing: {parsed_path}",
            error_type="FileNotFoundError",
        )
    if not news_path or not Path(news_path).exists():
        return StageResult(
            status="failed",
            run_id="",
            topic_id_hash=topic_id_hash,
            error=f"news_path missing: {news_path}",
            error_type="FileNotFoundError",
        )

    run_id = str(uuid.uuid4())
    store = ArtifactStore(
        Path(settings.state_dir),
        index_path_prefix=settings.state_index_prefix,
    )

    workspace = Path(settings.workspace_dir)
    command_file_hash = file_sha1(workspace / NEWSFIND_REPORT_COMMAND_FILE)
    schema_hash = file_sha1(workspace / NEWSFIND_REPORT_SCHEMA_FILE)
    if not command_file_hash:
        return StageResult(
            status="failed",
            run_id=run_id,
            topic_id_hash=topic_id_hash,
            error=(
                "newsfind-report slash command missing in workspace "
                f"({workspace / NEWSFIND_REPORT_COMMAND_FILE})"
            ),
            error_type="FileNotFoundError",
        )

    args = f"PARSED={parsed_path};NEWS={news_path}"

    try:
        rec = RunRecorder(
            store,
            topic=parsed_path,
            topic_id=topic_id_hash,
            run_id=run_id,
            stage=NEWSFIND_REPORT_STAGE,
        )
        rec.write_request(
            {
                "command": NEWSFIND_REPORT_COMMAND,
                "args": args,
                "output_format": "stream-json",
                "model": model or settings.default_model,
                "timeout_sec": timeout_sec or settings.default_timeout_sec,
                "command_file_hash": command_file_hash,
                "schema_hash": schema_hash,
            }
        )
        rec.open_stream()
    except Exception as exc:  # noqa: BLE001
        logger.exception("report setup error topic_id_hash=%s", topic_id_hash)
        return StageResult(
            status="failed",
            run_id=run_id,
            topic_id_hash=topic_id_hash,
            error=f"setup error: {type(exc).__name__}: {exc}",
            error_type=type(exc).__name__,
            traceback=traceback.format_exc(),
        )

    req = RunRequest(
        command=NEWSFIND_REPORT_COMMAND,
        args=args,
        model=model,
        timeout_sec=timeout_sec or settings.default_timeout_sec,
        output_format="stream-json",
    )

    settings_with_cmd = _maybe_extend_allowlist(settings, NEWSFIND_REPORT_COMMAND)

    raw_result: dict[str, Any] | None = None
    error: str | None = None
    error_tb: str | None = None
    progress_events: list[dict[str, Any]] = []

    try:
        async for line in stream_claude(req, settings_with_cmd):
            rec.append_stream_line(line)
            event = _safe_json_loads(line)
            if isinstance(event, dict):
                if event.get("type") == "result":
                    raw_result = event
                elif event.get("type") == "error":
                    error = str(event.get("error") or "stream error")
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
        logger.exception("report runner error topic_id_hash=%s", topic_id_hash)

    parsed = parse_business_result(raw_result)
    duration_ms = int((time.monotonic() - started) * 1000)
    if isinstance(raw_result, dict) and isinstance(raw_result.get("duration_ms"), int):
        duration_ms = raw_result["duration_ms"]
    total_cost_usd: float | None = None
    if isinstance(raw_result, dict) and isinstance(
        raw_result.get("total_cost_usd"), (int, float)
    ):
        total_cost_usd = float(raw_result["total_cost_usd"])

    status = "succeeded" if parsed is not None and error is None else "failed"

    report_json_path: Path | None = None
    report_md_path: Path | None = None
    if parsed is not None:
        report_json_path = rec.dir / "report.json"
        _write_json_atomic(report_json_path, parsed)
        report_md = parsed.get("report_md") or ""
        if report_md:
            report_md_path = rec.dir / "report.md"
            report_md_path.write_text(report_md, encoding="utf-8")

    rec.finalize(
        status=status,
        raw_result=raw_result,
        parsed=parsed,
        input_fingerprint=f"report:{command_file_hash}:{schema_hash}:{topic_id_hash}",
        model=model or settings.default_model,
        cached=False,
        duration_ms=duration_ms,
        total_cost_usd=total_cost_usd,
        error=error,
    )

    if status == "succeeded" and report_json_path is not None:
        _update_index(store, topic_id_hash, report_json_path, report_md_path)

    return StageResult(
        status=status,
        run_id=run_id,
        topic_id_hash=topic_id_hash,
        artifact_paths={
            "report_json": str(report_json_path) if report_json_path else "",
            "report_md": str(report_md_path) if report_md_path else "",
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
    store: ArtifactStore,
    topic_id_hash: str,
    report_json_path: Path,
    report_md_path: Path | None,
) -> None:
    index_path = store.index_path(topic_id_hash)
    if not index_path.exists():
        return
    try:
        idx = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    prefix = f"{store.index_path_prefix}/" if store.index_path_prefix else ""
    run_dir_name = report_json_path.parent.name
    idx["latest_report_path"] = f"{prefix}news/{topic_id_hash}/runs/{run_dir_name}/report.json"
    if report_md_path is not None:
        idx["latest_report_md_path"] = (
            f"{prefix}news/{topic_id_hash}/runs/{run_dir_name}/report.md"
        )
    idx["latest_report_run_id"] = run_dir_name
    _write_json_atomic(index_path, idx)
