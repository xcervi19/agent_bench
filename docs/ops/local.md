# Running SignalGather locally

The full stack on your own machine: topic API, RAG service, Postgres, and the UI.

## What you get, and what you do not

| | Local | prod |
|---|---|---|
| Topic pipeline, gate, report, monitoring | yes | yes |
| Web UI at `/app` | yes | yes |
| **RAG grounding during plan** | **no corpus — 0 documents** | 141 documents |
| Claude CLI | needs your own `claude auth login` | shared subscription |

The RAG gap is the one that matters. A local Postgres starts empty, so the plan
stage's RAG call returns nothing and `parsed.json` gets
`rag_context_refs: []` with a note in `current_state`. The pipeline still runs
end to end; the plan is just less grounded than prod's. Do not use a local run to
judge output quality — use it to develop.

## First run

```bash
cd ~/Documents/projects/agent_bench

# 1. Claude CLI auth — the container mounts this directory as /home/app/.claude
mkdir -p claude_home
CLAUDE_CONFIG_DIR=$PWD/claude_home claude auth login

# 2. Bring up the stack
docker compose up --build postgres rag_adhoc claude_agent

# 3. Migrations (first run only, in another shell)
docker compose run --rm --no-deps --entrypoint alembic rag_adhoc upgrade head
```

`.env` and `/etc/claude-worker.env` are optional; the compose file marks them
`required: false` precisely so a laptop without them boots. `apps/claude_agent/.env`
carries the service config and should exist.

Check it came up:

```bash
curl -s http://localhost:8002/readyz          # {"status":"ready", ...}
open http://localhost:8002/app
```

## Getting an account

Registration is **closed by default** (`CLAUDE_AGENT_ALLOW_PUBLIC_REGISTRATION=false`),
the same as prod. Two options locally:

```bash
# create an account with the operator script
docker compose exec claude_agent \
  python3 scripts/owner/create_user.py you@example.com

# or open self-registration for local convenience
CLAUDE_AGENT_ALLOW_PUBLIC_REGISTRATION=true docker compose up -d claude_agent
```

## Frontend development

The image bakes the built SPA, so a code change needs an image rebuild. For UI
work run Vite instead — hot reload, and it proxies the API to `:8002`:

```bash
cd apps/signalgather_web
npm install
npm run dev            # http://localhost:5173/app/
```

Same origin through the proxy, so no CORS setting is needed. Point it elsewhere
with `SIGNALGATHER_API_URL=https://agent-test1.particletico.com npm run dev`.

## Without Docker

Postgres is the only hard dependency; the API runs from the venv:

```bash
docker compose up -d postgres
CLAUDE_AGENT_DATABASE_URL='postgresql+asyncpg://agentic:agentic@127.0.0.1:5432/agentic' \
CLAUDE_AGENT_WEB_DIST=apps/signalgather_web/dist \
  .venv/bin/python -m uvicorn apps.claude_agent.app:app --port 8002
```

The Claude CLI then runs as *you*, using your own login rather than the mounted
`claude_home`.

## Cost

Local runs bill the same Claude subscription as prod — the CLI is the CLI. A
plan+deliver cycle is roughly the same order as the ~$3.40 a prod run reports.
There is no spend cap anywhere in the app.

## Related

- `AGENT.md` — repo map and quick commands
- `docs/ops/vps.md` — the deployed environments
- `apps/signalgather_web/README.md` — UI stack and scripts
- `scripts/owner/README.md` — accounts, password reset, topic ownership
