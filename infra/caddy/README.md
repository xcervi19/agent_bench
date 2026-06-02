# Caddy reverse proxy (VPS)

Host Caddy terminates TLS. **Public:** agent APIs only. RAG/Postgres bind to `127.0.0.1`.

Deploy from repo root:

```bash
scripts/devops/vps_deploy_caddy.sh
```

See `docs/ops/vps.md` and `docs/specs/done/multi_env_pre_frontend_13.md`.
