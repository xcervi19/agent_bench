"""HTTP API for the claude_agent service."""

from __future__ import annotations

import json
import logging
import traceback
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, status
from fastapi.responses import StreamingResponse

from .config import ClaudeAgentSettings, get_settings
from .jobs import JobManager
from .orchestrator import (
    is_newsfind_request,
    run_newsfind_queries,
    stream_newsfind_queries,
)
from .runner import CommandNotAllowedError, claude_version, run_claude, stream_claude
from .schemas import (
    InfoResponse,
    Job,
    JobCreated,
    JobStatus,
    RunRequest,
    RunResult,
)

logger = logging.getLogger(__name__)


def get_job_manager(request: Request) -> JobManager:
    return request.app.state.job_manager  # type: ignore[no-any-return]


def require_api_key(
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
    x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
) -> None:
    if not settings.api_key:
        return
    if not x_api_key or x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key")


router = APIRouter(
    prefix="/v1/agent",
    tags=["claude-agent"],
    dependencies=[Depends(require_api_key)],
)


@router.get("/info", response_model=InfoResponse)
async def info(
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
) -> InfoResponse:
    return InfoResponse(
        claude_bin=settings.claude_bin,
        claude_version=await claude_version(settings),
        workspace_dir=settings.workspace_dir,
        allowed_commands=settings.allowed_commands,
        allow_freeform_prompts=settings.allow_freeform_prompts,
        default_model=settings.default_model,
        default_permission_mode=settings.default_permission_mode,
        default_output_format=settings.default_output_format,
        default_timeout_sec=settings.default_timeout_sec,
        max_timeout_sec=settings.max_timeout_sec,
        max_concurrent_jobs=settings.max_concurrent_jobs,
    )


@router.post("/run", response_model=RunResult)
async def run_sync(
    body: RunRequest,
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
) -> RunResult:
    """Synchronous run. Blocks until the CLI exits or hits the timeout.

    For ``/newsfind-queries`` we dispatch through the artifact-aware
    orchestrator: cache-hits short-circuit the CLI entirely; cache-misses run
    the CLI in stream-json mode and persist a full reproducible artifact set.
    """
    try:
        if is_newsfind_request(body):
            return await run_newsfind_queries(body, settings)
        return await run_claude(body, settings)
    except CommandNotAllowedError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e
    except Exception as e:  # noqa: BLE001 — surface unexpected errors to the client
        logger.exception("run_sync handler error")
        return RunResult(
            status="failed",
            exit_code=1,
            error=f"server error: {type(e).__name__}: {e}",
            stderr=traceback.format_exc(),
        )


@router.post("/stream")
async def run_stream(
    body: RunRequest,
    settings: Annotated[ClaudeAgentSettings, Depends(get_settings)],
) -> StreamingResponse:
    """SSE stream of stream-json events from the CLI.

    For ``/newsfind-queries`` the orchestrator records the stream into
    ``stream.ndjson`` while it flows, and finalizes ``raw_result.json`` /
    ``parsed.json`` / ``meta.json`` plus ``index.json`` once ``type=result``
    arrives.
    """

    async def _gen():
        try:
            if is_newsfind_request(body):
                async for line in stream_newsfind_queries(body, settings):
                    yield f"data: {line}\n\n"
            else:
                async for line in stream_claude(body, settings):
                    yield f"data: {line}\n\n"
        except CommandNotAllowedError as e:
            payload = json.dumps({
                "type": "error",
                "stage": "auth",
                "error_type": type(e).__name__,
                "error": str(e),
            })
            yield f"data: {payload}\n\n"
            yield f"data: {json.dumps({'type': 'end', 'exit_code': 1})}\n\n"
        except Exception as e:  # noqa: BLE001 — surface as SSE so curl sees the cause
            logger.exception("stream handler error")
            payload = json.dumps({
                "type": "error",
                "stage": "route",
                "error_type": type(e).__name__,
                "error": str(e),
                "traceback": traceback.format_exc(),
            })
            yield f"data: {payload}\n\n"
            yield f"data: {json.dumps({'type': 'end', 'exit_code': 1})}\n\n"

    return StreamingResponse(_gen(), media_type="text/event-stream")


@router.post("/jobs", response_model=JobCreated, status_code=status.HTTP_202_ACCEPTED)
async def submit_job(
    body: RunRequest,
    jm: Annotated[JobManager, Depends(get_job_manager)],
) -> JobCreated:
    job = jm.submit(body)
    return JobCreated(id=job.id, status=job.status)


@router.get("/jobs", response_model=list[Job])
async def list_jobs(
    jm: Annotated[JobManager, Depends(get_job_manager)],
    status_filter: JobStatus | None = Query(default=None, alias="status"),
    limit: int = Query(default=50, ge=1, le=500),
) -> list[Job]:
    return jm.list(status=status_filter, limit=limit)


@router.get("/jobs/{job_id}", response_model=Job)
async def get_job(
    job_id: str,
    jm: Annotated[JobManager, Depends(get_job_manager)],
) -> Job:
    job = jm.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="job not found")
    return job


@router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_job(
    job_id: str,
    jm: Annotated[JobManager, Depends(get_job_manager)],
) -> None:
    if not await jm.cancel(job_id):
        raise HTTPException(status_code=409, detail="job not cancellable")
