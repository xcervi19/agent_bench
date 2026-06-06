#!/usr/bin/env bash
# scripts/evaluate_output.sh — Lane A business-value evaluation (#23)
#
# Thin wrapper over the Trading Intelligence Evaluation Framework
# (libs/eval_framework). Scores a finished run's business_output against the
# rubric and writes quality_review.{json,md} next to the run.
#
# Usage:
#   # Mode 1 — absolute (one run)
#   scripts/evaluate_output.sh absolute --run-dir testing/results/test1/latest
#
#   # Mode 2 — relative (baseline vs candidate)
#   scripts/evaluate_output.sh relative \
#     --baseline testing/results/test1/<older> \
#     --candidate testing/results/test1/latest
#
#   # Use the LLM judge (needs OPENAI_API_KEY)
#   scripts/evaluate_output.sh absolute --run-dir <dir> --evaluator llm
#
# Any extra flags are passed straight through to `python -m eval_framework`.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Pick an interpreter: prefer the project venv, then python3/python.
if [ -x ".venv/bin/python" ]; then
  PY=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PY="python3"
else
  PY="python"
fi

export PYTHONPATH="${REPO_ROOT}/libs${PYTHONPATH:+:${PYTHONPATH}}"
exec "$PY" -m eval_framework "$@"
