"""Request/response models for the claude_agent API."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

OutputFormat = Literal["text", "json", "stream-json"]
PermissionMode = Literal[
    "default",
    "acceptEdits",
    "auto",
    "bypassPermissions",
    "dontAsk",
    "plan",
]
JobStatus = Literal["queued", "running", "succeeded", "failed", "cancelled", "timeout"]


class RunRequest(BaseModel):
    """One of `prompt` or (`command` + optional `args`) is required."""

    prompt: str | None = Field(
        default=None,
        description="Free-form prompt. Disabled by default (see allow_freeform_prompts).",
    )
    command: str | None = Field(
        default=None,
        description="Slash command, e.g. '/trade-update'.",
    )
    args: str | None = Field(default=None, description="Arguments passed to the command.")

    output_format: OutputFormat = "json"
    permission_mode: PermissionMode | None = None
    model: str | None = None
    timeout_sec: int | None = Field(default=None, ge=1)
    extra_env: dict[str, str] | None = Field(
        default=None,
        description="Extra env vars exposed to the CLI process (e.g. RAG_*).",
    )

    @model_validator(mode="after")
    def _exactly_one_input(self) -> "RunRequest":
        if not self.prompt and not self.command:
            raise ValueError("Either 'prompt' or 'command' must be set.")
        if self.prompt and self.command:
            raise ValueError("Provide either 'prompt' or 'command', not both.")
        return self


class RunResult(BaseModel):
    status: JobStatus
    exit_code: int | None = None
    duration_ms: int | None = None
    stdout: str | None = None
    parsed: dict[str, Any] | None = None
    stderr: str | None = None
    error: str | None = None


class Job(BaseModel):
    id: str
    status: JobStatus
    request: RunRequest
    created_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None
    result: RunResult | None = None


class JobCreated(BaseModel):
    id: str
    status: JobStatus


class InfoResponse(BaseModel):
    claude_bin: str
    claude_version: str | None
    workspace_dir: str
    allowed_commands: list[str]
    allow_freeform_prompts: bool
    default_model: str | None
    default_permission_mode: str
    default_output_format: str
    default_timeout_sec: int
    max_timeout_sec: int
    max_concurrent_jobs: int
