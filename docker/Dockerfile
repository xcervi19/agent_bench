FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential curl libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY libs ./libs
COPY apps ./apps

RUN pip install --upgrade pip && pip install -e .

COPY alembic.ini ./
COPY database ./database
COPY scripts ./scripts
COPY docker ./docker

ENV PYTHONPATH=/app/libs:/app

EXPOSE 8000

CMD ["uvicorn", "apps.signal_gather.entrypoints.api:app", "--host", "0.0.0.0", "--port", "8000"]
