#!/usr/bin/env bash
# Remote half of purge_test_topic_data.sh. Runs ON the VPS; not called directly.
# Args: <pg_container> <db> <state_rel_path> <apply:yes|no> <purge_tables> <protected_tables>
set -euo pipefail

CONTAINER=$1
DB=$2
STATE_DIR="$HOME/$3"
APPLY=$4
PURGE=$5
PROTECTED=$6

q() {
  docker exec "$CONTAINER" psql -U agentic -d "$DB" -tA -v ON_ERROR_STOP=1 -c "$1" </dev/null
}

counts() {
  local table
  for table in $1; do
    printf '  %-22s %s\n' "$table" "$(q "SELECT count(*) FROM $table;")"
  done
}

locked=$(q "SELECT count(*) FROM topic_subscriptions WHERE refresh_locked;")
if [[ "$locked" != "0" ]]; then
  echo "ABORT: $locked refresh(es) in flight. Stop monitoring first." >&2
  exit 1
fi

echo "-- topic data to delete:"
counts "$PURGE"
echo "-- artifacts: $STATE_DIR/news"
du -sh "$STATE_DIR/news" 2>/dev/null || echo "  (none)"
echo "-- protected (must stay unchanged):"
counts "$PROTECTED"

if [[ "$APPLY" != "yes" ]]; then
  echo "-- DRY RUN, nothing deleted."
  exit 0
fi

before=$(counts "$PROTECTED")

q "DELETE FROM topic_refresh_deltas;
   DELETE FROM topic_webhooks;
   DELETE FROM topic_subscriptions;
   DELETE FROM topic_events;
   DELETE FROM topics;" >/dev/null

if [[ -d "$STATE_DIR/news" ]]; then
  rm -rf "${STATE_DIR:?}/news"/*
fi

after=$(counts "$PROTECTED")
if [[ "$before" != "$after" ]]; then
  echo "FATAL: protected tables changed during purge." >&2
  diff <(echo "$before") <(echo "$after") >&2 || true
  exit 1
fi

echo "-- purged, remaining topic data:"
counts "$PURGE"
echo "-- protected intact:"
echo "$after"
