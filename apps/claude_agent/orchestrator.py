"""Stage-aware orchestration for slash commands that produce reusable artifacts.

Today this only handles ``/newsfind-queries`` (Stage 1). The orchestrator:

1. Computes a stable ``input_fingerprint`` from the command, args, command-file
   hash, schema hash, and env/config version.
2. Looks up the topic's ``index.json``; if a successful run with the same
   fingerprint exists, returns the cached ``parsed.json`` instead of calling
   Claude again (the only way to actually save tokens).
3. On a miss, runs the Claude CLI in stream-json mode, captures every event
   into ``stream.ndjson`` as it arrives, and writes ``raw_result.json``,
   ``parsed.json``, ``meta.json`` plus an updated ``index.json`` once the
   ``type=result`` event lands.

Both ``run_newsfind_queries`` (sync wrapper) and ``stream_newsfind_queries``
(SSE generator) record identical artifacts.
"""

from __future__ import annotations

import json
import logging
import time
import traceback
import uuid
from collections.abc import AsyncIterator
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .artifacts import (
    ArtifactStore,
    RunRecorder,
    compute_input_fingerprint,
    file_sha1,
    parse_business_result,
    topic_id_from_args,
)
from .config import ClaudeAgentSettings
from .runner import CommandNotAllowedError, stream_claude
from .schemas import RunRequest, RunResult

NEWSFIND_COMMAND = "/newsfind-queries"
NEWSFIND_STAGE = "newsfind_queries"
NEWSFIND_COMMAND_FILE = ".claude/commands/newsfind-queries.md"
NEWSFIND_SCHEMA_FILE = ".claude/schemas/newsfind-queries.schema.json"

logger = logging.getLogger(__name__)


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def is_newsfind_request(req: RunRequest) -> bool:
    if not req.command:
        return False
    cmd = req.command.strip()
    if not cmd.startswith("/"):
        cmd = "/" + cmd
    return cmd == NEWSFIND_COMMAND


def _build_artifact_store(settings: ClaudeAgentSettings) -> ArtifactStore:
    return ArtifactStore(
        Path(settings.state_dir),
        index_path_prefix=settings.state_index_prefix,
    )


def _compute_fingerprint(
    req: RunRequest, settings: ClaudeAgentSettings, args: str
) -> str:
    workspace = Path(settings.workspace_dir)
    return compute_input_fingerprint(
        command=NEWSFIND_COMMAND,
        args=args,
        command_file_hash=file_sha1(workspace / NEWSFIND_COMMAND_FILE),
        schema_hash=file_sha1(workspace / NEWSFIND_SCHEMA_FILE),
        schema_version=settings.schema_version,
        env_version=settings.env_version,
        model=req.model or settings.default_model,
        permission_mode=req.permission_mode or settings.default_permission_mode,
    )


def _request_payload(req: RunRequest, settings: ClaudeAgentSettings) -> dict[str, Any]:
    timeout = min(
        req.timeout_sec or settings.default_timeout_sec,
        settings.max_timeout_sec,
    )
    return {
        "command": NEWSFIND_COMMAND,
        "args": (req.args or "").strip(),
        "output_format": "stream-json",
        "permission_mode": req.permission_mode or settings.default_permission_mode,
        "model": req.model or settings.default_model,
        "timeout_sec": timeout,
        "force_refresh": bool(req.force_refresh),
    }


def _result_event_summary(raw_result: dict[str, Any] | None) -> tuple[int | None, float | None]:
    if not isinstance(raw_result, dict):
        return None, None
    duration = raw_result.get("duration_ms")
    cost = raw_result.get("total_cost_usd")
    if not isinstance(duration, int):
        duration = None
    if not isinstance(cost, (int, float)):
        cost = None
    return duration, cost


def _cached_run_result(
    cached_meta: dict[str, Any], parsed: dict[str, Any], parsed_path: Path
) -> RunResult:
    return RunResult(
        status="succeeded",
        exit_code=0,
        duration_ms=cached_meta.get("duration_ms"),
        parsed=parsed,
        stdout=None,
        cached=True,
        run_id=cached_meta.get("run_id"),
        topic_id=cached_meta.get("topic_id"),
        parsed_path=str(parsed_path),
        total_cost_usd=cached_meta.get("total_cost_usd"),
    )


async def run_newsfind_queries(
    req: RunRequest, settings: ClaudeAgentSettings
) -> RunResult:
    """Sync entrypoint: returns the parsed business JSON, hitting cache when possible."""
    args = (req.args or "").strip()
    if not args:
        raise CommandNotAllowedError(f"{NEWSFIND_COMMAND} requires non-empty 'args'")

    store = _build_artifact_store(settings)
    topic_id = topic_id_from_args(args)
    fingerprint = _compute_fingerprint(req, settings, args)

    if not req.force_refresh:
        cached = store.find_cached(topic_id, fingerprint)
        if cached is not None:
            logger.info(
                "newsfind_queries cache hit topic_id=%s run_id=%s",
                topic_id,
                cached.run_id,
            )
            return _cached_run_result(cached.meta, cached.parsed, cached.parsed_path)
    else:
        logger.info(
            "newsfind_queries force_refresh=true topic_id=%s — bypassing cache",
            topic_id,
        )

    run_id = str(uuid.uuid4())
    try:
        rec = RunRecorder(
            store, topic=args, topic_id=topic_id, run_id=run_id, stage=NEWSFIND_STAGE
        )
        rec.write_request(_request_payload(req, settings))
        rec.open_stream()
    except Exception as exc:  # noqa: BLE001 — disk/permission failure during setup
        logger.exception(
            "newsfind_queries setup error topic_id=%s run_id=%s state_dir=%s",
            topic_id,
            run_id,
            settings.state_dir,
        )
        return RunResult(
            status="failed",
            exit_code=1,
            error=(
                f"setup error: {type(exc).__name__}: {exc} "
                f"(state_dir={settings.state_dir})"
            ),
            stderr=traceback.format_exc(),
            run_id=run_id,
            topic_id=topic_id,
        )

    streaming_req = req.model_copy(update={"output_format": "stream-json"})
    raw_result: dict[str, Any] | None = None
    error: str | None = None
    error_tb: str | None = None
    started = time.monotonic()
    try:
        async for line in stream_claude(streaming_req, settings):
            rec.append_stream_line(line)
            event = _safe_json_loads(line)
            if isinstance(event, dict) and event.get("type") == "result":
                raw_result = event
            if isinstance(event, dict) and event.get("type") == "error":
                error = str(event.get("error") or "stream error")
    except Exception as exc:  # noqa: BLE001 - record any runner failure
        error = f"runner error: {type(exc).__name__}: {exc}"
        error_tb = traceback.format_exc()
        logger.exception("newsfind_queries runner error")

    parsed = parse_business_result(raw_result)
    duration_ms, total_cost_usd = _result_event_summary(raw_result)
    if duration_ms is None:
        duration_ms = int((time.monotonic() - started) * 1000)
    status: str = "succeeded" if parsed is not None and error is None else "failed"

    rec.finalize(
        status=status,
        raw_result=raw_result,
        parsed=parsed,
        input_fingerprint=fingerprint,
        model=req.model or settings.default_model,
        cached=False,
        duration_ms=duration_ms,
        total_cost_usd=total_cost_usd,
        error=error,
    )

    return RunResult(
        status=status,
        exit_code=0 if status == "succeeded" else 1,
        duration_ms=duration_ms,
        stdout=json.dumps(raw_result, ensure_ascii=False) if raw_result else None,
        parsed=parsed,
        error=error,
        stderr=error_tb,
        cached=False,
        run_id=run_id,
        topic_id=topic_id,
        parsed_path=str(rec.parsed_path) if parsed is not None else None,
        total_cost_usd=total_cost_usd,
    )


async def stream_newsfind_queries(
    req: RunRequest, settings: ClaudeAgentSettings
) -> AsyncIterator[str]:
    """SSE generator: yields raw CLI events, recording artifacts in parallel.

    On a cache hit, emits a synthetic ``cache_hit`` event followed by a
    ``result`` event whose ``result`` field is the cached parsed JSON, then
    ``end``. The shape is intentionally compatible with the live stream so
    downstream consumers do not need to special-case caching.
    """
    args = (req.args or "").strip()
    if not args:
        yield json.dumps({"type": "error", "error": f"{NEWSFIND_COMMAND} requires non-empty 'args'"})
        yield json.dumps({"type": "end", "exit_code": 1})
        return

    store = _build_artifact_store(settings)
    topic_id = topic_id_from_args(args)
    fingerprint = _compute_fingerprint(req, settings, args)

    if not req.force_refresh:
        cached = store.find_cached(topic_id, fingerprint)
        if cached is not None:
            logger.info(
                "newsfind_queries stream cache hit topic_id=%s run_id=%s",
                topic_id,
                cached.run_id,
            )
            yield json.dumps(
                {
                    "type": "cache_hit",
                    "run_id": cached.run_id,
                    "topic_id": topic_id,
                    "parsed_path": str(cached.parsed_path),
                }
            )
            synthetic = {
                "type": "result",
                "subtype": "success",
                "duration_ms": cached.meta.get("duration_ms"),
                "total_cost_usd": cached.meta.get("total_cost_usd"),
                "result": json.dumps(cached.parsed, ensure_ascii=False),
                "cached": True,
            }
            yield json.dumps(synthetic, ensure_ascii=False)
            yield json.dumps({"type": "end", "exit_code": 0})
            return
    else:
        logger.info(
            "newsfind_queries stream force_refresh=true topic_id=%s — bypassing cache",
            topic_id,
        )

    run_id = str(uuid.uuid4())
    try:
        rec = RunRecorder(
            store, topic=args, topic_id=topic_id, run_id=run_id, stage=NEWSFIND_STAGE
        )
        rec.write_request(_request_payload(req, settings))
        rec.open_stream()
    except Exception as exc:  # noqa: BLE001 — disk/permission failure during setup
        logger.exception(
            "newsfind_queries stream setup error topic_id=%s run_id=%s state_dir=%s",
            topic_id,
            run_id,
            settings.state_dir,
        )
        yield json.dumps(
            {
                "type": "error",
                "stage": "setup",
                "topic_id": topic_id,
                "run_id": run_id,
                "input_fingerprint": fingerprint,
                "state_dir": settings.state_dir,
                "error_type": type(exc).__name__,
                "error": str(exc),
                "traceback": traceback.format_exc(),
            }
        )
        yield json.dumps({"type": "end", "exit_code": 1})
        return

    yield json.dumps(
        {
            "type": "run_started",
            "run_id": run_id,
            "topic_id": topic_id,
            "input_fingerprint": fingerprint,
        }
    )

    streaming_req = req.model_copy(update={"output_format": "stream-json"})
    raw_result: dict[str, Any] | None = None
    error: str | None = None
    error_tb: str | None = None
    end_event: str | None = None
    started = time.monotonic()
    try:
        async for line in stream_claude(streaming_req, settings):
            rec.append_stream_line(line)
            event = _safe_json_loads(line)
            if isinstance(event, dict) and event.get("type") == "result":
                raw_result = event
            elif isinstance(event, dict) and event.get("type") == "error":
                error = str(event.get("error") or "stream error")
            elif isinstance(event, dict) and event.get("type") == "end":
                # Hold onto the synthetic end event so we can emit it AFTER
                # artifact_finalized (so consumers see "end" as truly last).
                end_event = line
                continue
            yield line
    except Exception as exc:  # noqa: BLE001
        error = f"runner error: {type(exc).__name__}: {exc}"
        error_tb = traceback.format_exc()
        logger.exception("newsfind_queries stream runner error")
        yield json.dumps(
            {
                "type": "error",
                "stage": "runner",
                "topic_id": topic_id,
                "run_id": run_id,
                "error_type": type(exc).__name__,
                "error": str(exc),
                "traceback": error_tb,
            }
        )

    parsed = parse_business_result(raw_result)
    duration_ms, total_cost_usd = _result_event_summary(raw_result)
    if duration_ms is None:
        duration_ms = int((time.monotonic() - started) * 1000)
    status = "succeeded" if parsed is not None and error is None else "failed"

    rec.finalize(
        status=status,
        raw_result=raw_result,
        parsed=parsed,
        input_fingerprint=fingerprint,
        model=req.model or settings.default_model,
        cached=False,
        duration_ms=duration_ms,
        total_cost_usd=total_cost_usd,
        error=error,
    )

    yield json.dumps(
        {
            "type": "artifact_finalized",
            "run_id": run_id,
            "topic_id": topic_id,
            "status": status,
            "parsed_path": str(rec.parsed_path) if parsed is not None else None,
            "duration_ms": duration_ms,
            "total_cost_usd": total_cost_usd,
        }
    )

    if end_event is not None:
        yield end_event
    else:
        yield json.dumps({"type": "end", "exit_code": 0 if status == "succeeded" else 1})


def _safe_json_loads(line: str) -> Any:
    try:
        return json.loads(line)
    except (json.JSONDecodeError, TypeError):
        return None
