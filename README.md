# Newsfind — topic intelligence monorepo

Shipped product: **Claude Code topic pipeline** (`claude_agent`) with RAG during
plan (`rag_adhoc`) and Lane A evaluation (`eval_framework`).

Legacy **Signal Gather** (CrewAI RSS/signals) is archived — branch
`archive/signal_gather-platform`, see `docs/archive/README.md`.

## Layout

```
libs/agentic_core/          ← auth, DB, health (slim; JWT for #24)
libs/eval_framework/        ← output evaluation
apps/claude_agent/          ← topic pipeline (product)
apps/rag_adhoc/             ← RAG search + documents/events models
database/migrations/        ← Alembic
database/seeds/             ← (no scenarios on slim main)
scripts/utils/replay_session.py   ← debug tool (agent session replay)
source_ingest/              ← preprocess .txt → JSONL; ingest JSONL → Postgres + embeddings
oil_rag_collector/          ← download curated oil/WTI RAG sources (PDF/HTML/API)
docker/                     ← Dockerfiles
docker-compose.yml          ← postgres + rag_adhoc + claude_agent
```

## Quick start

```bash
cp .env.example .env
docker compose up --build postgres rag_adhoc claude_agent
```

Postgres (pgvector), RAG API on `:8001`, Claude agent on `:8002`.

Run migrations:

```bash
docker compose run --rm --no-deps --entrypoint alembic rag_adhoc upgrade head
```

RAG search docs: `http://localhost:8001/docs`. Topic API: `http://localhost:8002/docs` (when DB enabled).

## Oil / WTI RAG source collector

Download Tier 1–2 public sources (IEA, EIA, OPEC, CME PDFs, UNCTAD, terminals, geopolitics) into `artifacts/oil_rag_sources/`:

```bash
export EIA_API_KEY=your_key   # https://www.eia.gov/opendata/
uv run python -m oil_rag_collector -o artifacts/oil_rag_sources --max-tier 2
```

See `oil_rag_collector/README.md` and `docs/knowledge/oil_rag_source_strategy.md`.

### Batch chunk all collected sources (PDF/HTML/JSON → chunks)

```bash
uv run python -m source_ingest.from_collected \
  --sources-dir artifacts/oil_rag_sources \
  --chunks-dir artifacts/chunks \
  --skip-slug oil101
```

Skips `oil101` by default and any slug that already has `artifacts/chunks/<slug>/manifest.json`. Use `--force` to rebuild. Then ingest (see below) or add `--ingest --tenant-id '<uuid>'` with `DATABASE_URL` and `OPENAI_API_KEY` set.

## Local knowledge ingest (preprocess → JSONL → embeddings → Postgres)

Two-stage pipeline under `source_ingest/`: **(1)** normalize + chunk + metadata **without any API calls**;
**(2)** embed with OpenAI `text-embedding-3-small` (1536-dim) and insert `documents` + `events` for `rag_adhoc` search.

### Step 1 — Preprocess a `.txt` book (local only)

From the **repository root**, with `uv` (or your venv):

```bash
uv run python -m source_ingest.preprocess \
  --input local_knowledge_sources/oil101.txt \
  --output-dir artifacts/oil101_run1 \
  --book-title "Oil 101" \
  --author "Morgan Downey" \
  --book-slug oil101 \
  --category energy_education \
  --commodity crude_oil
```

This writes:

- `artifacts/oil101_run1/normalized.txt` — cleaned source text  
- `artifacts/oil101_run1/chunks.jsonl` — one JSON object per chunk (`prefix`, `body`, `location`, `filters`, `entities_extra`)  
- `artifacts/oil101_run1/manifest.json` — `document_id`, book meta, chunk count (needed for ingest)

Tune `--max-chars` (default `1100`) and `--overlap` (default `160`) if needed.

### Step 2 — Inspect artifacts

Open `chunks.jsonl` in an editor or stream:

```bash
head -n 2 artifacts/oil101_run1/chunks.jsonl | python -m json.tool
```

Every line should show chapter/source context in `prefix` and the chunk body in `body`.

### Step 3 — SSH tunnel to Postgres on your VPS

When Postgres listens only on the server (default), open a **local port forward** from your **laptop**, then point `DATABASE_URL` at **localhost**.

Example (replace user, host, key path):

```bash
ssh -i ~/.ssh/your_key -N -L 5433:127.0.0.1:5432 your-user@your-server-ip
```

- Leave this terminal open while ingesting.  
- Remote Postgres is reached as `127.0.0.1:5432` **on the server**; your laptop sees it as **`127.0.0.1:5433`**.

In **another** terminal on your laptop, export an **async** SQLAlchemy URL (match `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`):

```bash
export DATABASE_URL='postgresql+asyncpg://agentic:YOUR_PASSWORD@127.0.0.1:5433/agentic'
export OPENAI_API_KEY='sk-...'
```

Use the **same `tenant_id`** you pass as `X-Tenant-Id` when calling `rag_adhoc` (e.g. from seeded demo data or your registered user).

### Step 4 — Ingest (embed + DB write)

Still from **repo root** (with `PYTHONPATH` so `apps` + `agentic_core` resolve):

```bash
export PYTHONPATH="libs:."
uv run python -m source_ingest.ingest \
  --artifact-dir artifacts/oil101_run1 \
  --tenant-id '00000000-0000-0000-0000-000000000001'
```

Dry-run (calls embedding API but **does not** write rows):

```bash
uv run python -m source_ingest.ingest \
  --artifact-dir artifacts/oil101_run1 \
  --tenant-id '00000000-0000-0000-0000-000000000001' \
  --dry-run
```

Re-running ingest with the same `manifest.json` **creates duplicate events** unless you delete old rows first.

### Rights

Only ingest material you are allowed to copy, embed, and store.

---

## RAG search

Semantic search over ingested `events` rows:

```bash
curl -s -X POST http://localhost:8001/v1/search \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: YOUR-TENANT-UUID" \
  -d '{"query":"Hormuz strait LNG supply"}' | jq
```

## Replaying an agent session

```bash
export PYTHONPATH=libs:.
uv run python scripts/utils/replay_session.py \
  --session-id <uuid> \
  --tenant-id 00000000-0000-0000-0000-000000000001
```

## Principles enforced in the code

- Flat functions, minimal `try/except`.
- Tenant isolation via Postgres RLS + `tenant_scope` context manager.
- Embeddings degrade gracefully without an OpenAI key (semantic search falls back to filters).
