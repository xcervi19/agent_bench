# Owner-only scripts

**Product owner / technical lead only.** These scripts are destructive and are not
part of any developer, CI, or agent workflow. Do not call them from other scripts.

## `create_user.py` — issue an invitation-only account

Public registration is off by default
(`CLAUDE_AGENT_ALLOW_PUBLIC_REGISTRATION=false`), so `POST /auth/register` does
not exist on a product deployment. This is how an operator issues an account.

```bash
# on the VPS, inside the running container
docker compose exec claude_agent \
  python3 scripts/owner/create_user.py you@example.com

# non-interactive
docker compose exec -e SIGNALGATHER_PASSWORD='...' claude_agent \
  python3 scripts/owner/create_user.py you@example.com
```

The password comes from a hidden prompt or `SIGNALGATHER_PASSWORD` — never from
argv, so it stays out of shell history and `ps`. Hashing goes through
fastapi-users' own `UserManager`; nothing here hand-rolls crypto.

Each account gets a fresh tenant unless `--tenant-id` names an existing one.
`--superuser` is available but nothing in the product reads it yet.

## `reset_password.py` — a user forgot their password

There is no self-service reset. No email transport is configured, so
`/auth/forgot-password` is deliberately not mounted rather than minting reset
tokens nobody ever receives. On an invitation-only deployment the operator
resets it.

```bash
docker compose exec claude_agent \
  python3 scripts/owner/reset_password.py them@example.com
```

Same password handling as `create_user.py`: hidden prompt or
`SIGNALGATHER_PASSWORD`, never argv. Hand the new password over a channel you
trust and have them change it once they are in.

**Existing sessions survive.** The JWT is stateless, so a token issued before the
reset keeps working until it expires. If you are resetting because an account is
compromised, rotate `JWT_SECRET` as well — that invalidates every token for every
user, so expect to sign everyone back in.

Changing a password you still know is a different thing and needs no operator:
`PATCH /users/me` with `{"password": "..."}` works today for a signed-in user,
though the UI does not expose it yet.

## `assign_topics.py` — hand topics to an account

Topics created before #24, or by the service key, have `owner_user_id = NULL`.
Every topic route filters by owner, so those are invisible in the UI. This
reassigns them.

```bash
docker compose exec claude_agent \
  python3 scripts/owner/assign_topics.py you@example.com --unowned          # dry run
docker compose exec claude_agent \
  python3 scripts/owner/assign_topics.py you@example.com --unowned --apply
```

Scopes are mutually exclusive: `--unowned`, `--all`, or `--from-email X`.
Dry run by default. Child rows (events, subscriptions, deltas, webhooks) resolve
access through `topic_id`, so only `topics` is touched.

## `purge_test_topic_data.sh`

Wipes Newsfind topic test-run data from VPS slots after a testing campaign.
The VPS-side half lives in `_purge_remote.sh`, which is copied to `/tmp` and executed
per slot; do not invoke it directly.

| | |
|---|---|
| **Deletes (DB)** | `topics`, `topic_events`, `topic_subscriptions`, `topic_refresh_deltas`, `topic_webhooks` |
| **Deletes (disk)** | `<slot>/state*/news/*` — run artifacts (`parsed.json`, `report.md`, `delta.json`, streams) |
| **Never touches** | `documents`, `events`, `signals` (RAG corpus + embeddings), `users`, `user_profiles`, `reports`, `alerts`, `agent_sessions`, `agent_events`, `alembic_version`, `local_knowledge_sources/`, `artifacts/`, S3/MinIO, `claude_home/` |

```bash
scripts/owner/purge_test_topic_data.sh --slot test1          # dry run (default)
scripts/owner/purge_test_topic_data.sh --slot test1 --yes    # execute
scripts/owner/purge_test_topic_data.sh --slot all --yes      # prod + test1 + test2
```

### Safety model

1. **Dry run by default** — prints exactly what would be deleted; `--yes` is required to write.
2. **Typed confirmation** — `--yes` prompts for the literal word `PURGE`.
3. **In-flight guard** — aborts if any subscription has `refresh_locked = true`.
4. **Table whitelist** — the SQL names the five topic tables explicitly; no `TRUNCATE CASCADE`, no wildcards.
5. **Protected-count assertion** — row counts of all know-how tables are captured before and after; any drift exits non-zero.
6. **Scoped disk delete** — only `<state dir>/news/*`, never the state dir itself or repo folders.

### When to run

Only when the environment held **test traffic only**. Never with customer data present.
Stop monitoring first (`PATCH /monitor {"schedule_enabled": false}` and
`DELETE /monitor`) so no refresh is running.

Migrations are untouched — the schema stays at its current Alembic head, so topics
can be created again immediately after a purge.
