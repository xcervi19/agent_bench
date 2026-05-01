"""Load .env and satisfy agentic_core Settings before DB/embed imports."""

from __future__ import annotations

import os
from importlib import import_module
from pathlib import Path


def load_dotenv_file(path: Path) -> None:
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


def bootstrap_for_ingest(repo_root: Path) -> None:
    load_dotenv_file(repo_root / ".env")
    load_dotenv_file(repo_root / ".env.examplesmall")

    db = os.environ.get("DATABASE_URL") or os.environ.get("RAG_ADHOC_DATABASE_URL")
    if not db:
        raise SystemExit(
            "Set DATABASE_URL or RAG_ADHOC_DATABASE_URL "
            "(postgresql+asyncpg:// user:pass@host:port/db)"
        )
    os.environ["DATABASE_URL"] = db
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Set OPENAI_API_KEY before running ingest.")

    os.environ.setdefault("REDIS_URL", "redis://127.0.0.1:6379/0")
    os.environ.setdefault("S3_ENDPOINT_URL", "http://127.0.0.1:9000")
    os.environ.setdefault("S3_ACCESS_KEY", "x")
    os.environ.setdefault("S3_SECRET_KEY", "x")
    os.environ.setdefault("S3_BUCKET", "documents")
    os.environ.setdefault("JWT_SECRET", "ingest-local")
    os.environ.setdefault("APP_ENV", "local")
    os.environ.setdefault("LOG_LEVEL", "INFO")

    cfg = import_module("agentic_core.config")
    dbs = import_module("agentic_core.database.session")
    cfg.get_settings.cache_clear()  # type: ignore[misc]
    dbs.get_engine.cache_clear()  # type: ignore[misc]
    dbs.get_sessionmaker.cache_clear()  # type: ignore[misc]
