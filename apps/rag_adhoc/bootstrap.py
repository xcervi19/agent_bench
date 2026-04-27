"""Set process env for agentic_core and clear settings/engine caches so embed() and get_db() work."""

import os
from importlib import import_module


def _apply_env() -> None:
    from .config import get_rag_settings

    s = get_rag_settings()
    # RAG adhoc config is the source of truth for the shared Settings/embeddings in this process.
    os.environ["DATABASE_URL"] = s.database_url
    os.environ["OPENAI_API_KEY"] = s.openai_api_key
    os.environ.setdefault("REDIS_URL", s.redis_url)
    os.environ.setdefault("S3_ENDPOINT_URL", s.s3_endpoint_url)
    os.environ.setdefault("S3_ACCESS_KEY", s.s3_access_key)
    os.environ.setdefault("S3_SECRET_KEY", s.s3_secret_key)
    os.environ.setdefault("S3_BUCKET", s.s3_bucket)
    os.environ.setdefault("JWT_SECRET", s.jwt_secret)
    os.environ["APP_ENV"] = s.app_env
    os.environ["LOG_LEVEL"] = s.log_level


def _clear_agentic_caches() -> None:
    cfg = import_module("agentic_core.config")
    dbs = import_module("agentic_core.database.session")
    cfg.get_settings.cache_clear()  # type: ignore[misc]
    dbs.get_engine.cache_clear()  # type: ignore[misc]
    dbs.get_sessionmaker.cache_clear()  # type: ignore[misc]


def bootstrap() -> None:
    """Call before importing any module that uses agentic_core get_settings (e.g. embeddings, DB)."""
    _apply_env()
    _clear_agentic_caches()
