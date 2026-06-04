#!/usr/bin/env bash
# Run ci_vps_e2e_test1.sh on the VPS over SSH (local or GitHub Actions driver).
#
# Required env:
#   TEST1_API, TEST1_CLAUDE_AGENT_API_KEY
# Optional:
#   VPS_HOST (default root@79.143.179.212)
#   VPS_SSH_KEY (default ~/.ssh/contabo_ed25519)
#   VPS_REPO_DIR (default /root/agent_bench_test1)
#   GIT_REF (default main)
set -euo pipefail

: "${TEST1_API:?TEST1_API is required}"
: "${TEST1_CLAUDE_AGENT_API_KEY:?TEST1_CLAUDE_AGENT_API_KEY is required}"

VPS_HOST="${VPS_HOST:-root@79.143.179.212}"
VPS_SSH_KEY="${VPS_SSH_KEY:-$HOME/.ssh/contabo_ed25519}"
VPS_REPO_DIR="${VPS_REPO_DIR:-/root/agent_bench_test1}"
GIT_REF="${GIT_REF:-main}"

SSH_OPTS=(-i "$VPS_SSH_KEY" -o StrictHostKeyChecking=accept-new -o ConnectTimeout=30)

echo "== SSH E2E test1 → $VPS_HOST ($VPS_REPO_DIR) =="

ssh "${SSH_OPTS[@]}" "$VPS_HOST" \
  TEST1_API="$(printf '%q' "$TEST1_API")" \
  TEST1_CLAUDE_AGENT_API_KEY="$(printf '%q' "$TEST1_CLAUDE_AGENT_API_KEY")" \
  VPS_REPO_DIR="$(printf '%q' "$VPS_REPO_DIR")" \
  GIT_REF="$(printf '%q' "$GIT_REF")" \
  bash <<'REMOTE'
set -euo pipefail
cd "$VPS_REPO_DIR"
export VPS_REPO_DIR TEST1_API TEST1_CLAUDE_AGENT_API_KEY GIT_REF
if [[ ! -x scripts/devops/ci_vps_e2e_test1.sh ]]; then
  echo "Missing scripts/devops/ci_vps_e2e_test1.sh — run git pull on VPS worktree" >&2
  exit 1
fi
bash scripts/devops/ci_vps_e2e_test1.sh
REMOTE
