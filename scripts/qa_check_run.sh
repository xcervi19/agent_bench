#!/usr/bin/env bash
# scripts/qa_check_run.sh — thin mechanical PASS/FAIL gate for a finished run.
#
# Validates:
# - required artifacts exist
# - events.tool_errors == 0
# - basic output thresholds (sources, findings, citations)
#
# Usage:
#   scripts/qa_check_run.sh --run-dir testing/results/test1/latest
#   scripts/qa_check_run.sh --run-dir <run_dir> --out <run_dir>/qa_report.json
set -euo pipefail

RUN_DIR=""
OUT_FILE=""
MIN_SOURCES=5
MIN_FINDINGS=2
MIN_CITATIONS=3

while [[ $# -gt 0 ]]; do
  case "$1" in
    --run-dir)
      RUN_DIR="${2:-}"
      shift 2
      ;;
    --out)
      OUT_FILE="${2:-}"
      shift 2
      ;;
    --min-sources)
      MIN_SOURCES="${2:-5}"
      shift 2
      ;;
    --min-findings)
      MIN_FINDINGS="${2:-2}"
      shift 2
      ;;
    --min-citations)
      MIN_CITATIONS="${2:-3}"
      shift 2
      ;;
    -h|--help)
      cat <<'EOF'
Usage: scripts/qa_check_run.sh --run-dir <path> [--out <path>]

Options:
  --run-dir         Run directory that contains evaluation.json and artifacts
  --out             Output report path (default: <run_dir>/qa_report.json)
  --min-sources     Minimum deliver.sources_total (default: 5)
  --min-findings    Minimum deliver.key_findings_count (default: 2)
  --min-citations   Minimum deliver.unique_citations (default: 3)
EOF
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

if [[ -z "$RUN_DIR" ]]; then
  echo "Error: --run-dir is required" >&2
  exit 2
fi

if [[ ! -d "$RUN_DIR" ]]; then
  echo "Error: run directory not found: $RUN_DIR" >&2
  exit 2
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "Error: missing dependency: jq" >&2
  exit 2
fi

if [[ -z "$OUT_FILE" ]]; then
  OUT_FILE="$RUN_DIR/qa_report.json"
fi

EVAL_FILE="$RUN_DIR/evaluation.json"
EVENTS_FILE="$RUN_DIR/agent_log/events_full.ndjson"
PARSED_FILE="$RUN_DIR/business_output/parsed.json"
INTRO_MD_FILE="$RUN_DIR/business_output/intro.md"
NEWS_FILE="$RUN_DIR/business_output/news.json"
REPORT_JSON_FILE="$RUN_DIR/business_output/report.json"
REPORT_MD_FILE="$RUN_DIR/business_output/report.md"

check_file() {
  local path="$1"
  [[ -s "$path" ]] && echo "true" || echo "false"
}

HAS_EVAL=$(check_file "$EVAL_FILE")
HAS_EVENTS=$(check_file "$EVENTS_FILE")
HAS_PARSED=$(check_file "$PARSED_FILE")
HAS_INTRO_MD=$(check_file "$INTRO_MD_FILE")
HAS_NEWS=$(check_file "$NEWS_FILE")
HAS_REPORT_JSON=$(check_file "$REPORT_JSON_FILE")
HAS_REPORT_MD=$(check_file "$REPORT_MD_FILE")

tool_errors=0
sources_total=0
key_findings_count=0
unique_citations=0

if [[ "$HAS_EVAL" == "true" ]]; then
  tool_errors=$(jq -r '.events.tool_errors // 0' "$EVAL_FILE" 2>/dev/null || echo 0)
  sources_total=$(jq -r '.deliver.sources_total // 0' "$EVAL_FILE" 2>/dev/null || echo 0)
  key_findings_count=$(jq -r '.deliver.key_findings_count // 0' "$EVAL_FILE" 2>/dev/null || echo 0)
  unique_citations=$(jq -r '.deliver.unique_citations // 0' "$EVAL_FILE" 2>/dev/null || echo 0)
fi

jq -n \
  --arg run_dir "$RUN_DIR" \
  --arg generated_at "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --arg eval_file "$EVAL_FILE" \
  --arg events_file "$EVENTS_FILE" \
  --arg parsed_file "$PARSED_FILE" \
  --arg intro_md_file "$INTRO_MD_FILE" \
  --arg news_file "$NEWS_FILE" \
  --arg report_json_file "$REPORT_JSON_FILE" \
  --arg report_md_file "$REPORT_MD_FILE" \
  --argjson has_eval "$HAS_EVAL" \
  --argjson has_events "$HAS_EVENTS" \
  --argjson has_parsed "$HAS_PARSED" \
  --argjson has_intro_md "$HAS_INTRO_MD" \
  --argjson has_news "$HAS_NEWS" \
  --argjson has_report_json "$HAS_REPORT_JSON" \
  --argjson has_report_md "$HAS_REPORT_MD" \
  --argjson tool_errors "$tool_errors" \
  --argjson sources_total "$sources_total" \
  --argjson key_findings_count "$key_findings_count" \
  --argjson unique_citations "$unique_citations" \
  --argjson min_sources "$MIN_SOURCES" \
  --argjson min_findings "$MIN_FINDINGS" \
  --argjson min_citations "$MIN_CITATIONS" \
  '
  {
    run_dir: $run_dir,
    generated_at: $generated_at,
    checks: [
      {id: "artifact_evaluation_json", pass: $has_eval, actual: $eval_file},
      {id: "artifact_events_full_ndjson", pass: $has_events, actual: $events_file},
      {id: "artifact_parsed_json", pass: $has_parsed, actual: $parsed_file},
      {id: "artifact_intro_md", pass: $has_intro_md, actual: $intro_md_file},
      {id: "artifact_news_json", pass: $has_news, actual: $news_file},
      {id: "artifact_report_json", pass: $has_report_json, actual: $report_json_file},
      {id: "artifact_report_md", pass: $has_report_md, actual: $report_md_file},
      {id: "tool_errors_zero", pass: ($tool_errors == 0), actual: $tool_errors, expected: 0},
      {id: "sources_total_threshold", pass: ($sources_total >= $min_sources), actual: $sources_total, expected_min: $min_sources},
      {id: "key_findings_threshold", pass: ($key_findings_count >= $min_findings), actual: $key_findings_count, expected_min: $min_findings},
      {id: "unique_citations_threshold", pass: ($unique_citations >= $min_citations), actual: $unique_citations, expected_min: $min_citations}
    ]
  }
  | .failed_checks = [.checks[] | select(.pass == false) | .id]
  | .summary = {
      checks_total: (.checks | length),
      checks_failed: (.failed_checks | length),
      passed: ((.failed_checks | length) == 0)
    }
  | .passed = .summary.passed
  ' > "$OUT_FILE"

PASSED=$(jq -r '.passed' "$OUT_FILE")
FAILED=$(jq -r '.summary.checks_failed' "$OUT_FILE")

if [[ "$PASSED" == "true" ]]; then
  echo "QA PASS ($FAILED failed checks)"
  exit 0
fi

echo "QA FAIL ($FAILED failed checks)"
jq -r '.failed_checks[]' "$OUT_FILE" | sed 's/^/ - /'
exit 1
