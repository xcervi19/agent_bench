# ─── App ─────────────────────────────────────────────────────────────
APP_NAME=newsfinder
APP_ENV=local
LOG_LEVEL=INFO

# ─── Security ────────────────────────────────────────────────────────
JWT_SECRET=change-me-in-production
JWT_LIFETIME_SECONDS=3600

# ─── Postgres ────────────────────────────────────────────────────────
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=agentic
POSTGRES_USER=agentic
POSTGRES_PASSWORD=agentic
DATABASE_URL=postgresql+asyncpg://agentic:agentic@postgres:5432/agentic

# ─── Redis ───────────────────────────────────────────────────────────
REDIS_URL=redis://redis:6379/0

# ─── Object storage (S3-compatible; MinIO for local) ─────────────────
S3_ENDPOINT_URL=http://minio:9000
S3_REGION=eu-central-1
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET=documents

# ─── LLM (CrewAI) ────────────────────────────────────────────────────
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

# ─── RAG adhoc (apps/rag_adhoc, docker: postgres + rag_adhoc only) ───
# If unset, compose can still pass ${OPENAI_API_KEY} for embeddings.
# Set a long random string in production; clients must send X-API-Key.
# RAG_ADHOC_API_KEY=
