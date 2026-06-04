#!/usr/bin/env bash
# Run full V001 vector + QA gate on test1 (intended ON the VPS worktree via SSH).
#
# Prerequisites on host: bash, curl, jq, bc, git; repo at VPS_REPO_DIR.
# Env (required): TEST1_API, TEST1_CLAUDE_AGENT_API_KEY
# Env (optional): VPS_REPO_DIR, GIT_REF (default: main)
#
# Usage (on VPS):
#   export TEST1_API=https://agent-test1.particletico.com
#   export TEST1_CLAUDE_AGENT_API_KEY=...
#   export VPS_REPO_DIR=$HOME/agent_bench_test1
#   scripts/devops/ci_vps_e2e_test1.sh
#
# Usage (from laptop — SSH):
#   scripts/devops/ci_run_vps_e2e_ssh.sh
set -euo pipefail

REPO_DIR="${VPS_REPO_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
cd "$REPO_DIR"

GIT_REF="${GIT_REF:-main}"

echo "== ci_vps_e2e_test1 =="
echo "  repo: $REPO_DIR"
echo "  ref:  $GIT_REF"

if [[ -d .git ]]; then
  git fetch origin 2>/dev/null || true
  git checkout "$GIT_REF" 2>/dev/null || git checkout "origin/$GIT_REF" 2>/dev/null || true
  git pull --ff-only origin "$GIT_REF" 2>/dev/null || true
  echo "  commit: $(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
fi

export REPO_DIR TEST1_API TEST1_CLAUDE_AGENT_API_KEY
bash "$(dirname "$0")/ci_write_test1_env.sh"

command -v curl jq bc bash >/dev/null

echo "== Health check =="
# shellcheck disable=SC1091
source "$REPO_DIR/testing/.env.test1"
curl -fsS --max-time 15 "$API/readyz" | jq -e '.status == "ready"' >/dev/null
echo "  API ready: $API"

echo "== Vector runner (plan → deliver → refresh) =="
bash "$REPO_DIR/scripts/test_vector_runner.sh" --env test1

RUN_DIR="$REPO_DIR/testing/results/test1/latest"
QA_FILE="$RUN_DIR/qa_report.json"

if [[ ! -f "$QA_FILE" ]]; then
  echo "Missing $QA_FILE" >&2
  exit 1
fi

PASSED=$(jq -r '.passed' "$QA_FILE")
FAILED=$(jq -r '.summary.checks_failed // 0' "$QA_FILE")
VECTOR=$(jq -r '.vector_id // "?"' "$RUN_DIR/evaluation.json" 2>/dev/null || echo "?")

echo "== QA gate =="
echo "  vector: $VECTOR"
echo "  passed: $PASSED"
echo "  failed_checks: $FAILED"

if [[ "$PASSED" != "true" ]]; then
  jq -r '.failed_checks[]?' "$QA_FILE" | sed 's/^/  - /'
  exit 1
fi

echo "QA_GATE_SUMMARY passed=true vector=$VECTOR env=test1 run_dir=$RUN_DIR"
exit 0
