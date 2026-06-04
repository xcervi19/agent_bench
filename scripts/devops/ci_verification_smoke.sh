#!/usr/bin/env bash
# PR-level smoke: healthy fixture PASS, known-bad fixture FAIL (ticket #15 / #19).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"

command -v jq bash >/dev/null

echo "== verification-smoke: good fixture =="
bash scripts/qa_check_run.sh --run-dir testing/fixtures/good_run

echo "== verification-smoke: bad fixture (missing report.json) must FAIL =="
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
cp -R testing/fixtures/good_run/. "$TMP/run/"
rm -f "$TMP/run/business_output/report.json"
if bash scripts/qa_check_run.sh --run-dir "$TMP/run" --out "$TMP/run/qa_report.json"; then
  echo "Expected QA FAIL on broken fixture" >&2
  exit 1
fi
echo "  broken fixture correctly failed"

echo "verification-smoke PASS"
