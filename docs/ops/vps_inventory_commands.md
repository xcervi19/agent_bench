# VPS Inventory — copy-paste read commands

Scratch sheet for **inspecting** what exists on the VPS (`79.143.179.212`) and in
each Postgres DB. Everything here is **read-only** (no writes/migrations).
Copy a block, paste in a terminal, run manually.

- SSH key: `~/.ssh/contabo_ed25519`
- Stacks / DBs: `agent_bench`→`agentic` (prod) · `test1`→`agentic_test1` · `test2`→`agentic_test2`
- Artifact layout: `state/news/<topic_id_hash>/index.json` + `runs/<run_id>/{input,parsed,report,news,delta,summary,intro}.{json,md}`

---

## Snapshot (last checked: 2026-06-14)

**Containers:** all 3 stacks up — prod (`api`, `claude_agent`, `rag_adhoc`, `postgres`, `redis`, `minio`), `test1` + `test2` (minimal: `postgres`, `rag_adhoc`, `claude_agent`).

**File artifacts (`/state/news`):**

| Slot | topic-hash dirs | files | Notes |
|------|-----------------|-------|-------|
| prod | 5 | 86 | bind-mounted at `~/agent_bench/state`; only 1 dir has `index.json` |
| test1 | 6 | 50 | docker volume only (not in repo checkout) |
| test2 | 0 | 0 | empty |

**Database:**

| DB | alembic | topics | topic_events | subscriptions | deltas | webhooks | RAG docs | RAG events |
|----|---------|--------|--------------|---------------|--------|----------|----------|------------|
| agentic (prod) | `0004_newsfind_monitoring` | 9 | 745 | 2 | 5 | 0 | 69 | 3138 |
| agentic_test1 | `0004_newsfind_monitoring` | 10 | 428 | 1 | 1 | 1 | 0 | 0 |
| agentic_test2 | `0004_newsfind_monitoring` | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

> **#22 status:** migration `0005_topic_schedule` is **NOT applied** on any DB
> (no `schedule_enabled` / `next_refresh_at` columns yet). This is the pending
> VPS verification step. Prod topics: 4 `reported`, 3 `failed`, 2 `planned_awaiting_review`.

---

## SSH

```bash
# Open shell on VPS
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212

# Postgres tunnel from laptop (prod=5433 below maps to remote 5432)
ssh -i ~/.ssh/contabo_ed25519 -N -L 5433:127.0.0.1:5432 root@79.143.179.212
```

---

## Containers & stacks

```bash
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212 \
  'docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | sort'

# App checkouts
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212 'ls -1d ~/agent_bench*'
```

---

## File artifacts (`state/news`)

```bash
# Per-checkout: branch + state size + run-artifact tree
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212 'for d in agent_bench agent_bench_test1 agent_bench_test2; do
  echo "### ~/$d"; cd ~/$d 2>/dev/null || { echo "(missing)"; continue; }
  git rev-parse --abbrev-ref HEAD
  [ -d state ] && { du -sh state; ls -1 state; } || echo "(no state/)"
done'

# Artifacts that actually live in the running containers (docker volumes)
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212 'for c in agent_bench-claude_agent-1 test1-claude_agent-1 test2-claude_agent-1; do
  echo "--- $c ---"
  docker exec $c sh -lc "find /state/news -maxdepth 2 -type d 2>/dev/null; echo files=\$(find /state -type f 2>/dev/null | wc -l)"
done'

# Drill into one topic: index + run stages (set HASH)
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212 'cd ~/agent_bench
  HASH=2746112916bb146cb56b785ca1c142deaa198c90
  cat state/news/$HASH/index.json
  find state/news/$HASH -maxdepth 2 -type f'

# Read a specific run report
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212 \
  'cat ~/agent_bench/state/news/<HASH>/runs/<RUN_ID>/report.md'
```

---

## Database — quick counts (all DBs)

```bash
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212 'for pair in "agent_bench-postgres-1:agentic" "test1-postgres-1:agentic_test1" "test2-postgres-1:agentic_test2"; do
  c=${pair%%:*}; db=${pair##*:}; echo "### $db"
  docker exec $c psql -U agentic -d $db -c "SELECT
    (SELECT count(*) FROM topics) AS topics,
    (SELECT count(*) FROM topic_events) AS events,
    (SELECT count(*) FROM topic_subscriptions) AS subs,
    (SELECT count(*) FROM topic_refresh_deltas) AS deltas,
    (SELECT count(*) FROM topic_webhooks) AS webhooks;"
done'

# Alembic version per DB (confirms whether 0005 is applied)
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212 'for pair in "agent_bench-postgres-1:agentic" "test1-postgres-1:agentic_test1" "test2-postgres-1:agentic_test2"; do
  c=${pair%%:*}; db=${pair##*:}
  echo -n "$db -> "; docker exec $c psql -U agentic -d $db -t -A -c "SELECT version_num FROM alembic_version;"
done'
```

---

## Database — interactive psql

```bash
# Open psql on a DB (no password needed inside container)
ssh -i ~/.ssh/contabo_ed25519 -t root@79.143.179.212 'docker exec -it agent_bench-postgres-1 psql -U agentic -d agentic'
ssh -i ~/.ssh/contabo_ed25519 -t root@79.143.179.212 'docker exec -it test1-postgres-1 psql -U agentic -d agentic_test1'

# List topic* tables
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212 \
  'docker exec agent_bench-postgres-1 psql -U agentic -d agentic -c "\dt topic*"'
```

### SQL — topic state (run with `psql -c "..."`)

```sql
-- All topics, newest first
SELECT left(id::text,8) AS id, left(topic,42) AS topic, state,
       topic_id_hash, updated_at::date
FROM topics ORDER BY updated_at DESC;

-- Topics grouped by state
SELECT state, count(*) FROM topics GROUP BY state ORDER BY 2 DESC;

-- Monitoring subscriptions (current 0004 schema)
SELECT id, left(topic_id::text,8) AS topic, status, max_age_hours,
       refresh_count, last_refresh_at
FROM topic_subscriptions ORDER BY updated_at DESC;

-- After 0005 is applied, add the schedule columns:
-- SELECT id, left(topic_id::text,8) AS topic, status, schedule_enabled,
--        schedule_interval_hours, next_refresh_at, last_scheduled_refresh_at
-- FROM topic_subscriptions ORDER BY updated_at DESC;

-- Refresh delta history for a topic
SELECT seq, status, new_sources_count, queries_executed,
       duration_ms, total_cost_usd, created_at
FROM topic_refresh_deltas
WHERE topic_id = '<TOPIC_UUID>' ORDER BY seq;

-- Event stream for one topic (last 30)
SELECT seq, event_type, created_at
FROM topic_events
WHERE topic_id = '<TOPIC_UUID>' ORDER BY seq DESC LIMIT 30;

-- Webhooks registered
SELECT id, left(topic_id::text,8) AS topic, url, (secret IS NOT NULL) AS has_secret
FROM topic_webhooks;
```

### SQL — RAG corpus (prod only)

```sql
SET app.tenant_id = '00000000-0000-0000-0000-000000000001';

-- Corpus size
SELECT (SELECT count(*) FROM documents) AS documents,
       (SELECT count(*) FROM events) AS events;

-- Documents overview
SELECT left(id::text,8) AS id, source, left(title,50) AS title,
       language, created_at::date
FROM documents ORDER BY created_at DESC LIMIT 20;

-- Events for one document
SELECT id, category, commodity, region, occurred_at,
       left(summary,120) AS summary_preview
FROM events WHERE document_id = '<DOC_UUID>'
ORDER BY occurred_at NULLS LAST LIMIT 10;
```

### One-liner: run any SQL over SSH

```bash
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212 \
  'docker exec agent_bench-postgres-1 psql -U agentic -d agentic -c "SELECT state, count(*) FROM topics GROUP BY state;"'
```
