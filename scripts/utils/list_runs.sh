#!/usr/bin/env bash
# scripts/utils/list_runs.sh
#
# Show the 20 most recent local debug runs under testing/runs/ with a one-line
# summary of each (domain / queries count / actors count). Failed runs (no
# parsed.json) are flagged.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RUNS_DIR="$REPO_ROOT/testing/runs"

if [ ! -d "$RUNS_DIR" ]; then
  echo "no runs dir at $RUNS_DIR" >&2
  exit 0
fi

ls -1t "$RUNS_DIR" 2>/dev/null \
  | head -20 \
  | while read -r d; do
      P="$RUNS_DIR/$d/parsed.json"
      if [ -f "$P" ]; then
        echo "$d"
        jq -r '"  domain=\(.domain // "?") queries=\((.queries // []) | length) actors=\((.entities.actors // []) | length) rag_refs=\((.rag_context_refs // []) | length)"' "$P"
      else
        echo "$d  (no parsed.json — failed run)"
      fi
    done
