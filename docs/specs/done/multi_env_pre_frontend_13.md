# Multi-env hardening for pre-frontend testing — #13

**Status:** done  
**Depends on:** #12 (Caddy reverse proxy)

## Goal

Three isolated app instances (prod, test1, test2) with:

- Separate DB + RAG + topic state per slot
- **One** Claude subscription (`~/agent_bench/claude_home` shared)
- **Public HTTPS = agent only** (RAG and DB internal)
- **Minimal** test stacks (postgres + rag_adhoc + claude_agent)

## Changes

| Area | Implementation |
|------|----------------|
| Shared Claude auth | `../agent_bench/claude_home` mount in test1/test2 compose |
| Caddy | `agent`, `agent-test1`, `agent-test2` only (+ optional `app`) |
| Minimal stack | `infra/docker-compose.slot-minimal.yml` drops `api` dependency |
| Script | `scripts/vps_setup_test_slot.sh` uses minimal services |
| Docs | `docs/product/README.md`, updated `docs/ops/vps.md` |

## Acceptance criteria

- [x] prod + test1 + test2: own DB + RAG + state
- [x] All `agent*` HTTPS endpoints healthy
- [x] Single `claude_home` for all claude_agent containers
- [x] No public `rag*` / test API hostnames in Caddyfile
- [x] Test slots: 3-service compose profile
- [x] Docs updated

## Smoke test

```bash
for h in agent.particletico.com agent-test1.particletico.com agent-test2.particletico.com; do
  curl -fsS "https://$h/readyz" | jq -c .
done
curl -fsS --max-time 5 https://rag.particletico.com/ && exit 1 || echo "rag correctly unreachable"
```

## Related

- `docs/product/README.md` — product border
- `docs/specs/done/setup_caddy_reverse_proxy_12.md` — #12
