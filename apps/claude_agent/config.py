"""Settings for the claude_agent service. All env vars are prefixed CLAUDE_AGENT_."""

import json
from functools import lru_cache
from typing import Annotated

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


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
            "/newsfind-topic-parse",
            "/newsfind-plan",
            "/newsfind-deliver",
            "/newsfind-refresh",
            "/source-qa",
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
    allow_service_key_bypass: bool = Field(
        default=True,
        description=(
            "Topic API (#24): when true, X-API-Key callers act as a service role "
            "with access to every topic (ops smoke, eval harness). When api_key is "
            "empty this leaves the topic API open, as it was before ownership. Set "
            "false in product mode so only a user JWT is accepted."
        ),
    )

    allow_public_registration: bool = Field(
        default=False,
        description=(
            "Mount POST /auth/register. False (default) makes the deployment "
            "invitation-only: accounts are created with scripts/owner/create_user.py "
            "and no stranger can self-register. Enable it on test slots and for the "
            "eval harness, which register throwaway users."
        ),
    )

    # Frontend (#16). The SPA in apps/signalgather_web talks to this service.
    # NoDecode: keep pydantic-settings from JSON-decoding the env value so the
    # validator below can accept a plain comma-separated string.
    cors_origins: Annotated[list[str], NoDecode] = Field(
        default_factory=list,
        description=(
            "Origins allowed to call the API from a browser (comma-separated in "
            "env, e.g. 'http://localhost:5173'). Needed only when the UI is served "
            "from a different origin; the bundled /app mount is same-origin. "
            "'*' allows any origin — never use it in product mode."
        ),
    )
    web_dist: str = Field(
        default="",
        description=(
            "Path to the built SignalGather SPA (apps/signalgather_web/dist). When "
            "set and present, it is served at /app with history fallback so the UI "
            "shares the API origin (no CORS). Empty disables the mount."
        ),
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

    topic_parse_timeout_sec: int = Field(
        default=120,
        ge=10,
        description=(
            "Budget for the topic_parse leg (#38), which restates the topic in "
            "English for source discovery. It does no research, so a run that "
            "reaches this bound is stuck; the pipeline degrades to the "
            "untranslated topic rather than waiting out max_timeout_sec."
        ),
    )

    database_url: str = Field(
        default="",
        description=(
            "asyncpg URL for /v1/topics/* state. Empty disables those endpoints."
        ),
    )

    # Internal topic refresh scheduler (#22). Drives automatic refresh cycles for
    # monitored topics that opted in (schedule_enabled). Off-able at the process
    # level; per-topic scheduling is independently off by default.
    scheduler_enabled: bool = Field(
        default=True,
        description=(
            "Process-level switch for the in-app refresh scheduler loop. When "
            "false, no automatic refreshes fire (manual POST /refresh still works)."
        ),
    )
    scheduler_poll_interval_sec: int = Field(
        default=60,
        ge=5,
        description="How often the scheduler scans for due subscriptions.",
    )
    scheduler_max_concurrent_refreshes: int = Field(
        default=2,
        ge=1,
        description="Max scheduled refreshes dispatched per poll / running at once.",
    )
    # Background article fetcher (#42). Drains the unfetched search_documents
    # queue so the later evaluation pass has text to read; runs independently of
    # any topic run and never feeds the report.
    content_fetch_enabled: bool = Field(
        default=True,
        description="Process-level switch for the background article fetcher loop.",
    )
    content_fetch_poll_interval_sec: int = Field(
        default=300,
        ge=10,
        description="How often the fetcher scans for documents with no fetch outcome yet.",
    )
    content_fetch_batch_size: int = Field(
        default=50,
        ge=1,
        description="Max documents attempted per poll.",
    )
    schedule_min_interval_hours: int = Field(
        default=1,
        ge=1,
        description="Lower bound accepted for schedule_interval_hours.",
    )
    schedule_max_interval_hours: int = Field(
        default=168,
        ge=1,
        description="Upper bound accepted for schedule_interval_hours (default 7d).",
    )


    @field_validator("cors_origins", mode="before")
    @classmethod
    def _split_origins(cls, value: object) -> object:
        """Accept `a,b` from env as well as a JSON list, so ops can write a plain
        comma-separated string in .env like every other origin allowlist."""
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                return []
            if stripped.startswith("["):
                return json.loads(stripped)
            return [part.strip() for part in stripped.split(",") if part.strip()]
        return value


@lru_cache
def get_settings() -> ClaudeAgentSettings:
    return ClaudeAgentSettings()  # type: ignore[call-arg]
