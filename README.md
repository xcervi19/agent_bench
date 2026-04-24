# Agentic Platform — Iteration 1

Reusable multi-agent orchestration framework (`agentic_core`) plus the first
application built on top of it (`Signal Gather`, commodity trading intelligence).

## Layout

```
libs/agentic_core/          ← reusable framework (pip-installable)
apps/signal_gather/       ← first application
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
and the scheduler. Alembic migrations run automatically on API startup.

Then, in another shell:

```bash
docker compose exec api python -m database.seeds.seed_scenario signal_gather_commodity_trading
```

API is available at `http://localhost:8000/docs`.

## Replaying an agent session

```bash
docker compose exec api python scripts/replay_session.py \
  --session-id <uuid> \
  --tenant-id 00000000-0000-0000-0000-000000000001
```

## Writing a new crew

Subclass `agentic_core.agents.BaseCrewWrapper`, implement `build_crew`,
register a task that calls it:

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
- Split by responsibility (one concept per file).
- Tenant isolation via Postgres RLS + `tenant_scope` context manager.
- One Docker image, three entrypoints (api / worker / scheduler).
