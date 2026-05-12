"""Async wrapper around the `claude` CLI binary.

Two modes:

- ``run_claude(...)``  — collect-and-return; ideal for ``--output-format`` of
  ``text`` or ``json``.
- ``stream_claude(...)`` — async iterator over stdout lines; pair with
  ``--output-format stream-json`` for SSE.
"""

from __future__ import annotations

import asyncio
import json
import os
import time
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any

from .config import ClaudeAgentSettings
from .schemas import OutputFormat, PermissionMode, RunRequest, RunResult


@dataclass(slots=True)
class _BuiltCommand:
    argv: list[str]
    env: dict[str, str]
    cwd: str
    output_format: OutputFormat
    timeout_sec: int


class CommandNotAllowedError(ValueError):
    """Raised when a request violates the configured command policy."""


def _resolve_prompt(req: RunRequest, settings: ClaudeAgentSettings) -> str:
    if req.command:
        cmd = req.command.strip()
        if not cmd.startswith("/"):
            cmd = "/" + cmd
        if settings.allowed_commands and cmd not in settings.allowed_commands:
            raise CommandNotAllowedError(
                f"Command {cmd!r} is not in the allowlist: {settings.allowed_commands}"
            )
        args = (req.args or "").strip()
        return f"{cmd} {args}".strip()

    assert req.prompt is not None
    if not settings.allow_freeform_prompts:
        raise CommandNotAllowedError(
            "Free-form prompts are disabled. Use a slash 'command' from the allowlist."
        )
    return req.prompt


def _build_command(req: RunRequest, settings: ClaudeAgentSettings) -> _BuiltCommand:
    prompt = _resolve_prompt(req, settings)

    output_format: OutputFormat = req.output_format
    permission_mode: PermissionMode = (
        req.permission_mode or settings.default_permission_mode  # type: ignore[assignment]
    )
    timeout = min(
        req.timeout_sec or settings.default_timeout_sec,
        settings.max_timeout_sec,
    )

    argv: list[str] = [
        settings.claude_bin,
        "-p",
        "--output-format",
        output_format,
        "--permission-mode",
        permission_mode,
    ]

    if output_format == "stream-json":
        argv.append("--verbose")

    model = req.model or settings.default_model
    if model:
        argv.extend(["--model", model])

    for d in settings.additional_dirs:
        argv.extend(["--add-dir", d])

    argv.append(prompt)

    env = os.environ.copy()
    if req.extra_env:
        env.update(req.extra_env)

    return _BuiltCommand(
        argv=argv,
        env=env,
        cwd=settings.workspace_dir,
        output_format=output_format,
        timeout_sec=timeout,
    )


def _try_parse_json(text: str) -> dict[str, Any] | None:
    text = text.strip()
    if not text:
        return None
    try:
        loaded = json.loads(text)
    except json.JSONDecodeError:
        return None
    return loaded if isinstance(loaded, dict) else {"value": loaded}


async def run_claude(req: RunRequest, settings: ClaudeAgentSettings) -> RunResult:
    """Run the Claude CLI and return when it exits."""
    built = _build_command(req, settings)

    started = time.monotonic()
    proc = await asyncio.create_subprocess_exec(
        *built.argv,
        cwd=built.cwd,
        env=built.env,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    try:
        stdout_b, stderr_b = await asyncio.wait_for(
            proc.communicate(), timeout=built.timeout_sec
        )
    except asyncio.TimeoutError:
        proc.kill()
        with asyncio.timeout(5):
            await proc.wait()
        duration_ms = int((time.monotonic() - started) * 1000)
        return RunResult(
            status="timeout",
            exit_code=None,
            duration_ms=duration_ms,
            error=f"timeout after {built.timeout_sec}s",
        )

    duration_ms = int((time.monotonic() - started) * 1000)
    cap = settings.max_output_bytes
    stdout = stdout_b[:cap].decode(errors="replace")
    stderr = stderr_b[:cap].decode(errors="replace")
    parsed = _try_parse_json(stdout) if built.output_format == "json" else None

    if proc.returncode == 0:
        return RunResult(
            status="succeeded",
            exit_code=0,
            duration_ms=duration_ms,
            stdout=stdout,
            parsed=parsed,
            stderr=stderr or None,
        )

    return RunResult(
        status="failed",
        exit_code=proc.returncode,
        duration_ms=duration_ms,
        stdout=stdout,
        parsed=parsed,
        stderr=stderr,
        error=f"claude exited with {proc.returncode}",
    )


async def stream_claude(
    req: RunRequest, settings: ClaudeAgentSettings
) -> AsyncIterator[str]:
    """Yield stdout lines from the CLI in real time.

    Pair with ``output_format='stream-json'`` to get one JSON object per line.
    The final yielded line is a synthetic JSON: ``{"type":"end","exit_code":N}``.
    """
    forced = req.model_copy(update={"output_format": "stream-json"})
    built = _build_command(forced, settings)

    proc = await asyncio.create_subprocess_exec(
        *built.argv,
        cwd=built.cwd,
        env=built.env,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    assert proc.stdout is not None

    deadline = asyncio.get_running_loop().time() + built.timeout_sec
    try:
        while True:
            remaining = deadline - asyncio.get_running_loop().time()
            if remaining <= 0:
                proc.kill()
                yield json.dumps({"type": "error", "error": "timeout"})
                break
            try:
                line = await asyncio.wait_for(proc.stdout.readline(), timeout=remaining)
            except asyncio.TimeoutError:
                proc.kill()
                yield json.dumps({"type": "error", "error": "timeout"})
                break
            if not line:
                break
            yield line.decode(errors="replace").rstrip("\n")
    finally:
d        # On normal exit the process has already terminated. On cancellation
        # (asyncio.CancelledError thrown into ``await proc.stdout.readline()``)
        # we must kill the subprocess so it doesn't outlive the task. ``kill``
        # on an already-exited process is a no-op.
        if proc.returncode is None:
            try:
                proc.kill()
            except ProcessLookupError:
                pass
        try:
            rc = await asyncio.wait_for(proc.wait(), timeout=5.0)
        except asyncio.TimeoutError:
            rc = -1
        yield json.dumps({"type": "end", "exit_code": rc})


async def claude_version(settings: ClaudeAgentSettings) -> str | None:
    """Return ``claude --version`` output, or None if the binary is missing."""
    try:
        proc = await asyncio.create_subprocess_exec(
            settings.claude_bin,
            "--version",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout_b, _ = await asyncio.wait_for(proc.communicate(), timeout=10)
    except (FileNotFoundError, asyncio.TimeoutError):
        return None
    return stdout_b.decode(errors="replace").strip() or None
