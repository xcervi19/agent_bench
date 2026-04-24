#!/usr/bin/env bash
set -euo pipefail
alembic upgrade head
exec uvicorn apps.signal_gather.entrypoints.api:app --host 0.0.0.0 --port 8000
