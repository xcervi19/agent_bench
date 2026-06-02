# DevOps Scripts

Operational helpers for VPS/test-slot management.

- `vps_setup_test_slot.sh` — create/update `test1` or `test2` slot (worktree + compose)
- `vps_deploy_caddy.sh` — deploy/reload host Caddy configuration

Use from repo root, for example:

```bash
scripts/devops/vps_setup_test_slot.sh test1 main
scripts/devops/vps_deploy_caddy.sh
```
