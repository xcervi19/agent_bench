# Agentic Platform — Iteration 1

Reusable multi-agent orchestration framework (`agentic_core`) plus the first
application built on top of it (`Signal Gather`, commodity market intelligence).

## Layout

```
libs/agentic_core/          ← reusable framework (pip-installable)
apps/signal_gather/         ← first application
  agents/                     ← CrewAI crews (discovery, doc intel, signals, briefing, profile setup)
  models/                     ← Document, Event, Signal, UserProfile, Report, Alert
  routers/                    ← /setup /profiles /events /signals /insights /reports /alerts /search /tasks
  services/                   ← embeddings, ingestion, signal rules, briefings, alerts, RSS discovery
  tasks/                      ← background task handlers (RQ)
  scheduler_jobs/             ← periodic discovery / signal sweep / briefing dispatch
  scenarios/                  ← deterministic seed data
database/migrations/        ← Alembic
database/seeds/             ← scenario seeders
scripts/replay_session.py   ← debug tool
source_ingest/              ← preprocess .txt → JSONL; ingest JSONL → Postgres + embeddings
oil_rag_collector/          ← download curated oil/WTI RAG sources (PDF/HTML/API)
docker/                     ← Dockerfile + entrypoints
docker-compose.yml
```

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

That starts Postgres (with `pgvector`), Redis, MinIO (S3), the API, a worker,
and the scheduler. Alembic runs both migrations on API startup.

Seed demo data:

```bash
docker compose exec api python -m database.seeds.seed_scenario signal_gather_commodity_trading
```

API is available at `http://localhost:8000/docs`.

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

## Signal Gather end-to-end flow

1. **Onboard** — `POST /setup` with free-form text:
   ```json
   {"text": "I trade European gas and LNG. Focus on supply disruptions, storage levels, pipeline news, and EU regulations. Morning briefings and instant alerts on high-impact events."}
   ```
   The `ProfileSetupCrew` parses it into a `UserProfile`.

2. **Discover** — Scheduler triggers `signal_gather.discover_market` per commodity every 30 min:
   - Fetches RSS feeds (`services/discovery/feeds.py`)
   - Stores raw item in S3, persists `Document` row, computes embedding
   - Enqueues `signal_gather.extract_events` per new doc

3. **Extract** — `DocumentIntelligenceCrew` turns text into structured `Event` rows.

4. **Detect** — Every 15 min `signal_gather.detect_signals` clusters recent events by
   commodity/region (rule engine), refines each cluster with `SignalEngineCrew`,
   persists `Signal` rows, and fans out `Alert` rows for any user whose
   `impact_threshold` is met.

5. **Briefing** — Cron at 06:00 UTC enqueues `signal_gather.generate_briefing` for
   every profile with `briefing_cadence == "daily"` (07:00 Mon for weekly).
   `BriefingCrew` writes a `Report`.

6. **Ad-hoc insights** — `POST /insights {query, commodity, region}` enqueues
   `signal_gather.generate_insight`; `PersonalizedTraderCrew` answers using
   `pgvector` semantic retrieval over events.

7. **Search** — `POST /search` runs a semantic+filter query and returns events.

## Replaying an agent session

```bash
docker compose exec api python scripts/replay_session.py \
  --session-id <uuid> \
  --tenant-id 00000000-0000-0000-0000-000000000001
```

## Writing a new crew

```python
from agentic_core.agents import BaseCrewWrapper, CrewRunContext
from agentic_core.workers import task

class MyCrew(BaseCrewWrapper):
    name = "my_crew"
    def build_crew(self, ctx: CrewRunContext):
        ...

@task("myapp.do_thing")
async def do_thing(tenant_id, payload):
    return await MyCrew().run(CrewRunContext(tenant_id=tenant_id, inputs=payload))
```

## Principles enforced in the code

- Flat functions, no defensive type checks, minimal `try/except`.
- One concept per file; small `_build_*` helpers per crew/task.
- Tenant isolation via Postgres RLS + `tenant_scope` context manager.
- One Docker image, three entrypoints (api / worker / scheduler).
- Embeddings degrade gracefully without an OpenAI key (semantic search falls back to filters).
