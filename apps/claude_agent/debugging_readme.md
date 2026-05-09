# Claude Agent — Human-Only Notes

Quick recipes + war stories. Not part of the API contract.

---

## Standard rebuild + smoke test (VPS)

```bash
cd ~/agent_bench
docker compose build claude_agent
docker compose up -d claude_agent
docker compose logs -f claude_agent

# Health check
curl -s http://79.143.179.212:8002/readyz
# expect: {"status":"ready","claude_version":"2.x.x ..."}

# Auth/info
curl -s http://localhost:8002/v1/agent/info \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" | jq

# End-to-end ping
curl -s -X POST http://79.143.179.212:8002/v1/agent/run \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -d '{"prompt":"Reply with exactly: HELLO_WORLD_OK","output_format":"json"}'
```

OAuth token must be inside the container:
```bash
docker compose exec claude_agent env | grep CLAUDE_CODE_OAUTH_TOKEN
```

---

## Things we hit while bringing up `/newsfind-queries` (and how we fixed each)

### Problem 1 — `--output-format=stream-json requires --verbose`
**Symptom:** API stream returns `exit_code: 1` immediately.
**Cause:** Claude CLI rejects `-p` with `stream-json` unless `--verbose` is also set.
**Fix:** `runner.py` now appends `--verbose` automatically when output format is `stream-json`.

### Problem 2 — `Unknown command: /newsfind-queries` (CLI direct)
**Symptom:** Running `claude` from `/app` says command not found.
**Cause:** Slash commands are resolved relative to CWD (`.claude/commands/*.md`).
**Fix:** Always run from the workspace dir:
```bash
docker compose exec -w /workspace/claude_agent_fe claude_agent claude ...
```

### Problem 3 — `/newsfind-queries` not in allowlist
**Symptom:** API returns 400 "Command not in allowlist".
**Cause:** `CLAUDE_AGENT_ALLOWED_COMMANDS` in `.env` overrides `config.py` defaults.
**Fix:** Add new commands to **both**:
- `apps/claude_agent/config.py` (default list)
- `apps/claude_agent/.env` (`CLAUDE_AGENT_ALLOWED_COMMANDS=[...]`)

Then `docker compose build claude_agent`.

### Problem 4 — `--dangerously-skip-permissions cannot be used with root/sudo`
**Symptom:** `bypassPermissions` fails inside the container.
**Cause:** Anthropic CLI refuses `bypassPermissions` / WebSearch / Bash when UID 0.
**Fix:** Container now creates a non-root user `app` (UID/GID 1001) and `USER app` is set in the Dockerfile. Bind-mount sources on the host must also be owned by 1001.

### Problem 5 — `Claude configuration file not found at: /home/app/.claude.json`
**Symptom:** CLI prints the warning, falls back to backup, agent runs degraded.
**Cause:** Bind mount `./claude_home → /home/app/.claude` was empty; only `backups/` survived.
**Fix:** Restore from the auto-saved backup (one-off):
```bash
docker compose exec claude_agent bash -c \
  'ls /home/app/.claude/backups/ && \
   cp /home/app/.claude/backups/.claude.json.backup.* /home/app/.claude.json'
```

### Problem 6 — `awk: unknown option -W ignored` on macOS
**Symptom:** macOS `awk` doesn't understand GNU flags used in our SSE stripper.
**Cause:** macOS ships BSD awk.
**Fix:** Use `sed` instead: `sed -e 's/^data: //'`.

---

## Migrating to non-root user (one-time on each environment)

If you change Dockerfile to run as user `app` (UID 1001), the host bind-mount sources MUST be owned by 1001 or the container can't read/write them.

```bash
cd ~/agent_bench

# Find the actual mount source paths
docker inspect agent_bench-claude_agent-1 | grep -A 50 '"Mounts"'
# Look for "Source": "/root/agent_bench/claude_home" and "/root/agent_bench/claude_agent_fe"

# chown both to UID 1001
sudo chown -R 1001:1001 ./claude_home
sudo chown -R 1001:1001 ./claude_agent_fe

# Rebuild with the new Dockerfile
docker compose down claude_agent
docker compose build claude_agent
docker compose up -d claude_agent

# Verify the service runs as user `app`, not root
docker compose exec claude_agent id
# expect: uid=1001(app) gid=1001(app) groups=1001(app)

# Restore Claude config (.claude.json gets recreated per user)
docker compose exec claude_agent bash -c \
  'cp /home/app/.claude/backups/.claude.json.backup.* /home/app/.claude.json 2>/dev/null || true'
```

---

## Debug commands cheat sheet (VPS)

```bash
# What's running?
docker compose ps claude_agent

# Last 50 log lines
docker compose logs --tail=50 claude_agent

# Live logs
docker compose logs -f claude_agent

# Confirm the container's user
docker compose exec claude_agent id

# Confirm allowed commands the running process actually loaded
docker compose logs claude_agent | grep allowed_commands

# Confirm env inside the container
docker compose exec claude_agent env | grep -E 'CLAUDE_AGENT|CLAUDE_CODE_OAUTH'

# Confirm bind-mount source paths and ownership
docker inspect agent_bench-claude_agent-1 | grep -A 50 '"Mounts"'
ls -la ~/agent_bench/claude_home ~/agent_bench/claude_agent_fe

# Direct CLI test inside container (bypasses FastAPI)
docker compose exec -w /workspace/claude_agent_fe claude_agent \
  claude -p --output-format json --permission-mode bypassPermissions \
  "/newsfind-queries Hormuz strait closure options to lower price"
```

---

## End-to-end test through the API (from your Mac)

```bash
cd ~/Documents/projects/agent_bench
source apps/claude_agent/.env
export API="http://79.143.179.212:8002"

# Streaming (live progress)
curl -N -X POST "$API/v1/agent/stream" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -d '{"command":"/newsfind-queries","args":"Hormuz strait closure options to lower price","timeout_sec":900}' \
  | tee ./newsfind.raw.txt

# Extract the final blueprint
cat ./newsfind.raw.txt | grep '"type":"result"' | head -1 \
  | jq -r '.result' \
  | jq '{schema_version, domain, queries_count: (.queries | length), languages: [.queries[].language] | unique}'
```

Expected (after a successful run):
```json
{
  "schema_version": "0.2.0",
  "domain": "...",
  "queries_count": 13,
  "languages": ["ar", "en", "fa", "zh"]
}
```
