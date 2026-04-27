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
