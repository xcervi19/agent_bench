"""In-memory async job manager for Claude CLI runs.

Keeps each job in a process-local dict. A semaphore caps concurrent runs;
queued jobs are admitted as slots free up. Replace with Redis/RQ for
multi-replica deployments — the API surface stays the same.
"""

from __future__ import annotations

import asyncio
import time
import uuid
from datetime import datetime, timezone

from .config import ClaudeAgentSettings
from .runner import CommandNotAllowedError, run_claude
from .schemas import Job, JobStatus, RunRequest, RunResult


def _now() -> datetime:
    return datetime.now(timezone.utc)


class JobManager:
    def __init__(self, settings: ClaudeAgentSettings) -> None:
        self._settings = settings
        self._jobs: dict[str, Job] = {}
        self._tasks: dict[str, asyncio.Task[None]] = {}
        self._sem = asyncio.Semaphore(settings.max_concurrent_jobs)
        self._gc_running = False

    def submit(self, req: RunRequest) -> Job:
        job_id = str(uuid.uuid4())
        job = Job(id=job_id, status="queued", request=req, created_at=_now())
        self._jobs[job_id] = job
        self._tasks[job_id] = asyncio.create_task(
            self._run(job_id), name=f"claude-job:{job_id}"
        )
        if not self._gc_running:
            self._gc_running = True
            asyncio.create_task(self._gc_loop(), name="claude-job-gc")
        return job

    def get(self, job_id: str) -> Job | None:
        return self._jobs.get(job_id)

    def list(self, *, status: JobStatus | None = None, limit: int = 50) -> list[Job]:
        jobs = sorted(self._jobs.values(), key=lambda j: j.created_at, reverse=True)
        if status is not None:
            jobs = [j for j in jobs if j.status == status]
        return jobs[:limit]

    async def cancel(self, job_id: str) -> bool:
        job = self._jobs.get(job_id)
        task = self._tasks.get(job_id)
        if not job or not task or job.status not in ("queued", "running"):
            return False
        task.cancel()
        try:
            await task
        except (asyncio.CancelledError, Exception):
            pass
        if job.status in ("queued", "running"):
            job.status = "cancelled"
            job.finished_at = _now()
            job.result = RunResult(status="cancelled", error="cancelled by user")
        return True

    async def _run(self, job_id: str) -> None:
        job = self._jobs[job_id]
        try:
            async with self._sem:
                if job.status == "cancelled":
                    return
                job.status = "running"
                job.started_at = _now()
                try:
                    result = await run_claude(job.request, self._settings)
                except CommandNotAllowedError as e:
                    result = RunResult(status="failed", error=str(e))
                except Exception as e:  # noqa: BLE001 - surface unexpected errors via API
                    result = RunResult(status="failed", error=f"runner error: {e}")
                job.result = result
                job.status = result.status
                job.finished_at = _now()
        except asyncio.CancelledError:
            job.status = "cancelled"
            job.finished_at = _now()
            job.result = RunResult(status="cancelled", error="cancelled by user")
            raise

    async def _gc_loop(self) -> None:
        ttl = self._settings.job_ttl_sec
        while True:
            await asyncio.sleep(max(60, ttl // 4))
            cutoff = time.time() - ttl
            stale = [
                jid
                for jid, j in self._jobs.items()
                if j.finished_at and j.finished_at.timestamp() < cutoff
            ]
            for jid in stale:
                self._jobs.pop(jid, None)
                self._tasks.pop(jid, None)
