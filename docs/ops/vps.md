# VPS — particletico.com (Contabo)

Single Ubuntu 24.04 server running production Docker Compose stack(s) behind host Caddy (HTTPS).

## Server identity

| Field | Value |
|-------|--------|
| Provider | Contabo |
| Public IPv4 | `79.143.179.212` |
| Public IPv6 | `2a02:c207:2325:9468::1` |
| Hostname | `vmi3259468` |
| OS | Ubuntu 24.04.4 LTS |
| RAM | 12 GB |
| Disk | 193 GB (`/` ~20% used) |
| SSH | `ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212` |
| App checkout | `~/agent_bench` (branch `main`) |

## DNS (particletico.com)

All **A** records point to `79.143.179.212`:

> **TLS:** AAAA records must point to `2a02:c207:2325:9468::1` (or be removed).
> Let's Encrypt certs are active when AAAA is correct.

| Hostname | Purpose | Backend (localhost) |
|----------|---------|---------------------|
| `particletico.com`, `www` | Redirect → `app` | — |
| `app.particletico.com` | Production API (`signal_gather`) | `127.0.0.1:8000` |
| `agent.particletico.com` | Production `claude_agent` | `127.0.0.1:8002` |
| `rag.particletico.com` | Production `rag_adhoc` | `127.0.0.1:8001` |
| `test1.particletico.com` | Test slot 1 (`~/agent_bench_test1`, DB `agentic_test1`) | `127.0.0.1:8100` |
| `agent-test1.particletico.com` | Test slot 1 agent | `127.0.0.1:8102` |
| `rag-test1.particletico.com` | Test slot 1 RAG | `127.0.0.1:8101` |
| `test2.particletico.com` | Test slot 2 (`~/agent_bench_test2`, DB `agentic_test2`) | `127.0.0.1:8200` |
| `agent-test2.particletico.com` | Test slot 2 agent | `127.0.0.1:8202` |
| `rag-test2.particletico.com` | Test slot 2 RAG | `127.0.0.1:8201` |

TLS: Let’s Encrypt via **Caddy** on the host (`/etc/caddy/Caddyfile`, source in `infra/caddy/Caddyfile`).

HTTP (port 80) already redirects to HTTPS. After AAAA is fixed, certs should appear within a minute.

## Production stack (`~/agent_bench`)

Compose project name: `agent_bench`.

| Service | Container | Host port | Notes |
|---------|-----------|-----------|--------|
| `postgres` | `agent_bench-postgres-1` | `127.0.0.1:5432` | pgvector/pg16, DB `agentic` |
| `redis` | `agent_bench-redis-1` | `127.0.0.1:6379` | RQ queue |
| `minio` | `agent_bench-minio-1` | `127.0.0.1:9000`, `9001` | S3-compatible object store |
| `api` | `agent_bench-api-1` | `127.0.0.1:8000` | FastAPI + Alembic on startup |
| `rag_adhoc` | `agent_bench-rag_adhoc-1` | `127.0.0.1:8001` | RAG search API |
| `claude_agent` | `agent_bench-claude_agent-1` | `127.0.0.1:8002` | Claude agent API |
| `worker` | — | — | **Not running** (defined in compose) |
| `scheduler` | — | — | **Not running** (defined in compose) |

Volumes:

- `agent_bench_postgres_data`
- `agent_bench_minio_data`

### Run production on VPS

```bash
cd ~/agent_bench
git pull origin main
docker compose -f docker-compose.yml -f infra/docker-compose.vps-bind-local.yml up -d --build
```

Port overlay (`infra/docker-compose.vps-bind-local.yml`) keeps DB/Redis/MinIO/API off the public internet; only Caddy exposes 80/443.

### Health checks (HTTPS)

```bash
curl -s https://agent.particletico.com/readyz
curl -sI https://app.particletico.com/docs
```

Legacy IP:port URLs still work from localhost on the server; public access should go through HTTPS hostnames.

## Reverse proxy (Caddy)

- **Install / reload from laptop:** `scripts/vps_deploy_caddy.sh`
- **Config on server:** `/etc/caddy/Caddyfile`
- **Service:** `systemctl status caddy`

## Host services (non-Docker)

| Service | Status | Notes |
|---------|--------|-------|
| Caddy 2.11.3 | active | Listens on `:80`, `:443`; admin API on `127.0.0.1:2019` |
| UFW | active | Allows 22, 80, 443 only |
| Docker | active | Compose v5.1.3 |

## Firewall (UFW)

Active rules:

- Allow: `22/tcp`, `80/tcp`, `443/tcp`
- Default: deny incoming

App ports are not opened in UFW; they bind to `127.0.0.1` via compose overlay.

## Postgres tunnel (from laptop)

```bash
ssh -i ~/.ssh/contabo_ed25519 -N -L 5433:127.0.0.1:5432 root@79.143.179.212
export DATABASE_URL='postgresql+asyncpg://agentic:YOUR_PASSWORD@127.0.0.1:5433/agentic'
```

## Test environments

Each slot = git worktree + `COMPOSE_PROJECT_NAME` + isolated DB/volumes:

| Slot | Directory | Compose project | Branch (default) | Postgres DB | API / RAG / Agent |
|------|-----------|-----------------|------------------|-------------|-------------------|
| prod | `~/agent_bench` | `agent_bench` | `main` | `agentic` | 8000 / 8001 / 8002 |
| test1 | `~/agent_bench_test1` | `test1` | `main` | `agentic_test1` | 8100 / 8101 / 8102 |
| test2 | `~/agent_bench_test2` | `test2` | `main` | `agentic_test2` | 8200 / 8201 / 8202 |

Create or refresh a slot from laptop:

```bash
scripts/vps_setup_test_slot.sh test1 main
scripts/vps_setup_test_slot.sh test2 feature/my-branch
```

Uses `infra/docker-compose.test1.yml` / `test2.yml` for ports and separate `claude_home_*` / `state_*` dirs.

## Deploy checklist

1. `git pull` on VPS
2. `docker compose -f docker-compose.yml -f infra/docker-compose.vps-bind-local.yml up -d --build <services>`
3. `docker compose exec api alembic current`
4. `scripts/vps_deploy_caddy.sh` (if Caddyfile changed)
5. Smoke test HTTPS endpoints

See also `docs/ops/commands.md` for day-to-day commands.

Ticket write-up: `docs/specs/done/setup_caddy_reverse_proxy_12.md` (#12).
