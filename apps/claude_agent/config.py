"""Settings for the claude_agent service. All env vars are prefixed CLAUDE_AGENT_."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ClaudeAgentSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "apps/claude_agent/.env"),
        env_prefix="CLAUDE_AGENT_",
        extra="ignore",
        case_sensitive=False,
    )

    claude_bin: str = Field(
        default="claude",
        description="Path to the Claude Code CLI binary.",
    )
    workspace_dir: str = Field(
        default="/workspace/claude_agent_fe",
        description=(
            "Directory the CLI runs in. Must contain `.claude/commands` to expose "
            "your slash commands."
        ),
    )
    additional_dirs: list[str] = Field(
        default_factory=list,
        description="Extra directories passed via --add-dir (read access).",
    )

    default_model: str | None = Field(
        default=None,
        description="Default model alias (e.g. 'sonnet', 'opus'). None = CLI default.",
    )
    default_permission_mode: str = Field(
        default="bypassPermissions",
        description="default | acceptEdits | auto | bypassPermissions | dontAsk | plan",
    )
    default_output_format: str = Field(default="json")  # text | json | stream-json
    default_timeout_sec: int = Field(default=300)
    max_timeout_sec: int = Field(default=1800)
    max_output_bytes: int = Field(default=4 * 1024 * 1024)

    allowed_commands: list[str] = Field(
        default_factory=lambda: [
            "/trader",
            "/trade-update",
            "/trade-intel",
            "/trade-flash",
            "/trade-situation",
            "/signal-extractor",
            "/rag-search",
            "/rag-query-builder",
            "/newsfind-queries",
            "/newsfind-plan",
            "/newsfind-deliver",
        ],
        description="Allowlist of slash commands. Empty list = allow all.",
    )
    allow_freeform_prompts: bool = Field(
        default=False,
        description="If true, accept arbitrary prompts (not only slash commands).",
    )

    api_key: str = Field(
        default="",
        description="If set, requests must send matching X-API-Key header.",
    )

    log_level: str = Field(default="INFO")
    app_env: str = Field(default="local")

    job_ttl_sec: int = Field(
        default=3600,
        description="How long completed jobs are retained in memory.",
    )
    max_concurrent_jobs: int = Field(default=4)

    # Reproducible run artifacts (per /newsfind-queries run)
    state_dir: str = Field(
        default="/state",
        description=(
            "Directory where per-run artifacts (request, stream, raw_result, "
            "parsed, meta, index) are written. In docker we mount ./state here."
        ),
    )
    state_index_prefix: str = Field(
        default="state",
        description=(
            "Logical prefix used in index.json's parsed_path so upper logic can "
            "resolve the artifact relative to the project root."
        ),
    )
    schema_version: str = Field(
        default="0.2.0",
        description="Newsfind queries business-schema version (folded into input_fingerprint).",
    )
    env_version: str = Field(
        default="1",
        description=(
            "Bump this whenever the agent runtime/env changes in a way that "
            "should invalidate cached newsfind-queries runs."
        ),
    )

    database_url: str = Field(
        default="",
        description=(
            "asyncpg URL for /v1/topics/* state. Empty disables those endpoints."
        ),
    )


@lru_cache
def get_settings() -> ClaudeAgentSettings:
    return ClaudeAgentSettings()  # type: ignore[call-arg]
