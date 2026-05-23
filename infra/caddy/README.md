# Caddy reverse proxy (VPS)

Host Caddy terminates TLS and forwards to Docker stacks bound on `127.0.0.1`.

| File | Purpose |
|------|---------|
| `Caddyfile` | Source config (deploy to `/etc/caddy/Caddyfile`) |
| `../docker-compose.vps-bind-local.yml` | Bind app ports to localhost only |

Deploy from repo root:

```bash
scripts/vps_deploy_caddy.sh
```

After editing `Caddyfile` for a new test slot, redeploy and ensure the test stack is running on the matching port.
