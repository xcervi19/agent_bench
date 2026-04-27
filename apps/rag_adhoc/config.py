"""Environment for the RAG adhoc app (prefix RAG_ADHOC_). Kept free of agentic_core imports."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RagAdhocSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "apps/rag_adhoc/.env"),
        env_prefix="RAG_ADHOC_",
        extra="ignore",
        case_sensitive=False,
    )

    database_url: str = Field(
        description="Async SQLAlchemy URL, same as main app (e.g. postgresql+asyncpg://...).",
    )
    openai_api_key: str = Field(default="")

    # Optional: if set, every request must send matching X-API-Key
    api_key: str = Field(default="")

    # Unused by retrieval; required so agentic_core Settings can be satisfied
    redis_url: str = Field(default="redis://127.0.0.1:6379/0")
    s3_endpoint_url: str = Field(default="http://127.0.0.1:9000")
    s3_access_key: str = Field(default="x")
    s3_secret_key: str = Field(default="x")
    s3_bucket: str = Field(default="documents")
    jwt_secret: str = Field(default="not-used")
    app_env: str = Field(default="local")
    log_level: str = Field(default="INFO")


@lru_cache
def get_rag_settings() -> RagAdhocSettings:
    return RagAdhocSettings()  # type: ignore[call-arg]
