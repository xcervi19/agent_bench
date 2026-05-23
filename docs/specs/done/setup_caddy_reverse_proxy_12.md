# Setup Caddy reverse proxy — #12

**Status:** done (2026-05-23)  
**Domain:** `particletico.com`  
**Server:** Contabo VPS `79.143.179.212` (`~/agent_bench`)

## Goal

Expose production Docker services over HTTPS on named subdomains instead of raw `IP:port`. Prepare hostname slots for future branch-based test environments (`test1`, `test2`).

Before this ticket, services were reachable as:

- `http://79.143.179.212:8000` — API
- `http://79.143.179.212:8001` — rag_adhoc
- `http://79.143.179.212:8002` — claude_agent

After this ticket, public access goes through **host Caddy** on ports 80/443; app ports bind to `127.0.0.1` only.

## Architecture

```
Internet
   │
   ▼
Caddy (host, :80 / :443, TLS)
   │
   ├── app.particletico.com      → 127.0.0.1:8000  (api)
   ├── agent.particletico.com    → 127.0.0.1:8002  (claude_agent)
   ├── rag.particletico.com      → 127.0.0.1:8001  (rag_adhoc)
   └── particletico.com / www    → redirect → app

Docker Compose (~/agent_bench, project agent_bench)
   postgres / redis / minio / api / rag_adhoc / claude_agent
   (ports published on 127.0.0.1 only via compose overlay)
```

**Why Caddy on the host (not in Docker):** multiple independent compose stacks (prod + future test slots) each expose fixed localhost ports. Host Caddy routes by `Host` header without shared Docker networks.

## Repo artifacts

| Path | Role |
|------|------|
| `infra/caddy/Caddyfile` | Source of truth for vhosts and TLS |
| `infra/caddy/README.md` | Short pointer |
| `infra/docker-compose.vps-bind-local.yml` | Bind service ports to `127.0.0.1` (`!override`) |
| `scripts/vps_deploy_caddy.sh` | Install Caddy (if missing) + deploy config from laptop |
| `docs/ops/vps.md` | Live server inventory and ops runbook |

## Hostname map

| Hostname | Backend | Stack |
|----------|---------|-------|
| `app.particletico.com` | `127.0.0.1:8000` | prod API |
| `agent.particletico.com` | `127.0.0.1:8002` | prod claude_agent |
| `rag.particletico.com` | `127.0.0.1:8001` | prod rag_adhoc |
| `particletico.com`, `www` | redirect | → `https://app.particletico.com` |
| `test1.particletico.com` | `127.0.0.1:8100` | test1 API (`~/agent_bench_test1`) |
| `agent-test1.particletico.com` | `127.0.0.1:8102` | test1 claude_agent |
| `rag-test1.particletico.com` | `127.0.0.1:8101` | test1 rag_adhoc |
| `test2.particletico.com` | `127.0.0.1:8200` | test2 API (`~/agent_bench_test2`) |
| `agent-test2.particletico.com` | `127.0.0.1:8202` | test2 claude_agent |
| `rag-test2.particletico.com` | `127.0.0.1:8201` | test2 rag_adhoc |

Provision test slots: `scripts/vps_setup_test_slot.sh test1|test2 [branch]`

## DNS prerequisites

**A records** — point to `79.143.179.212`:

- `@`, `www`, `app`, `agent`, `rag` (and later `test1`, `agent-test1`, etc.)

**AAAA records:** must point to `2a02:c207:2325:9468::1` (or be removed). Certs issued via Let's Encrypt once AAAA is correct.

## Initial setup (one-time, already run)

### 1. Install Caddy on VPS

Handled by `scripts/vps_deploy_caddy.sh` (official Caddy apt repo, systemd service).

### 2. Deploy Caddyfile

From laptop:

```bash
scripts/vps_deploy_caddy.sh
```

On server, config lives at `/etc/caddy/Caddyfile`.

### 3. Bind Docker ports to localhost

On VPS:

```bash
cd ~/agent_bench
docker compose -f docker-compose.yml -f infra/docker-compose.vps-bind-local.yml up -d \
  postgres redis minio api rag_adhoc claude_agent
```

Use `!override` in the overlay so compose does not merge duplicate port mappings.

### 4. Enable firewall

```bash
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

## Day-to-day operations

### Update Caddy config

1. Edit `infra/caddy/Caddyfile`
2. Run `scripts/vps_deploy_caddy.sh`
3. Smoke test (see below)

### Enable a test slot (when stack exists)

1. Start test compose on ports `810x` or `820x` (separate worktree + `.env`)
2. Uncomment matching block(s) in `infra/caddy/Caddyfile`
3. `scripts/vps_deploy_caddy.sh`

## Verification

### On VPS (always works once stack is up)

```bash
curl -s http://127.0.0.1:8002/readyz
# → {"status":"ready","claude_version":"..."}

curl -sI http://127.0.0.1:8000/docs | head -3
```

### Public HTTP (Caddy redirect)

```bash
curl -4 -sI http://app.particletico.com/
# → 308 Location: https://app.particletico.com/
```

### Public HTTPS (after AAAA fix)

```bash
curl -s https://agent.particletico.com/readyz
curl -sI https://app.particletico.com/docs
curl -sI https://rag.particletico.com/docs
```

### Security check — direct ports blocked

From outside the server:

```bash
curl --max-time 5 http://79.143.179.212:8002/readyz
# → should time out or refuse (not reach the app)
```

## Acceptance criteria (#12)

- [x] Caddy installed on VPS as systemd service
- [x] `infra/caddy/Caddyfile` in repo; deploy script from laptop
- [x] Production subdomains routed: `app`, `agent`, `rag`
- [x] Apex/`www` redirect to `app`
- [x] Docker app ports bound to `127.0.0.1` via compose overlay
- [x] UFW allows only 22, 80, 443
- [x] Test slot hostnames documented and stubbed in Caddyfile (commented)
- [x] HTTPS certificates issued (prod + test1 + test2)
- [x] Test slots `test1` / `test2` deployed (`scripts/vps_setup_test_slot.sh`)

## Related docs

- `docs/ops/vps.md` — server inventory, port map, multi-env plan
- `docs/ops/commands.md` — SSH, deploy, smoke tests

## Follow-up

- Point test1/test2 at feature branches: `scripts/vps_setup_test_slot.sh test1 my-branch`
- Frontend build: deploy static assets or separate compose service per slot as needed
