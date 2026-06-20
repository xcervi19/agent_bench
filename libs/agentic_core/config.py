"""Typed application settings loaded from environment variables."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    app_name: str = "newsfinder"
    app_env: str = "local"
    log_level: str = "INFO"

    jwt_secret: str = Field(default="change-me")
    jwt_lifetime_seconds: int = 3600

    database_url: str
    redis_url: str

    s3_endpoint_url: str
    s3_region: str = "eu-central-1"
    s3_access_key: str
    s3_secret_key: str
    s3_bucket: str = "documents"

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
