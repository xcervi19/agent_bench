#!/usr/bin/env bash
# Download latest test1 run artifacts from VPS into a local directory (for GHA upload).
#
# Usage:
#   scripts/devops/ci_fetch_test1_artifacts.sh ./artifacts/test1
set -euo pipefail

DEST="${1:?Usage: $0 <dest-dir>}"
VPS_HOST="${VPS_HOST:-root@79.143.179.212}"
VPS_SSH_KEY="${VPS_SSH_KEY:-$HOME/.ssh/contabo_ed25519}"
VPS_REPO_DIR="${VPS_REPO_DIR:-/root/agent_bench_test1}"
REMOTE_RUN="$VPS_REPO_DIR/testing/results/test1/latest"

SSH_OPTS=(-i "$VPS_SSH_KEY" -o StrictHostKeyChecking=accept-new)

mkdir -p "$DEST"
scp -r "${SSH_OPTS[@]}" "$VPS_HOST:$REMOTE_RUN/"* "$DEST/" 2>/dev/null || \
  scp -r "${SSH_OPTS[@]}" "$VPS_HOST:$REMOTE_RUN/." "$DEST/"

echo "Fetched artifacts to $DEST"
ls -la "$DEST"
