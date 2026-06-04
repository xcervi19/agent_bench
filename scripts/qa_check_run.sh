#!/usr/bin/env bash
# scripts/qa_check_run.sh — mechanical PASS/FAIL technical gate for a finished run (ticket #15).
#
# Defines the technical verification contract (Lane B). Validates:
# - required artifacts exist and are non-empty
# - events.tool_errors == 0
# - output thresholds (sources, findings, citations) — from testing/qa_rules.json
# - lifecycle: topic reached expected terminal state (reported), not failed
# - invariants: plan + deliver stages finished; report citations resolve to news sources
#
# Rule catalog + thresholds: testing/qa_rules.json (overridable via flags).
# This script defines WHAT passes; execution wiring (CI/VPS/GitHub checks) is ticket #19.
#
# Usage:
#   scripts/qa_check_run.sh --run-dir testing/results/test1/latest
#   scripts/qa_check_run.sh --run-dir <run_dir> --out <run_dir>/qa_report.json
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

RUN_DIR=""
OUT_FILE=""
RULES_FILE="$REPO_ROOT/testing/qa_rules.json"
MIN_SOURCES=""
MIN_FINDINGS=""
MIN_CITATIONS=""

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
    --rules)
      RULES_FILE="${2:-}"
      shift 2
      ;;
    --min-sources)
      MIN_SOURCES="${2:-}"
      shift 2
      ;;
    --min-findings)
      MIN_FINDINGS="${2:-}"
      shift 2
      ;;
    --min-citations)
      MIN_CITATIONS="${2:-}"
      shift 2
      ;;
    -h|--help)
      cat <<'EOF'
Usage: scripts/qa_check_run.sh --run-dir <path> [--out <path>] [--rules <path>]

Options:
  --run-dir         Run directory that contains evaluation.json and artifacts
  --out             Output report path (default: <run_dir>/qa_report.json)
  --rules           Rule/threshold catalog (default: testing/qa_rules.json)
  --min-sources     Override deliver.sources_total minimum
  --min-findings    Override deliver.key_findings_count minimum
  --min-citations   Override deliver.unique_citations minimum
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

# ── Load thresholds (CLI override > rules file > built-in default) ──────────
EXPECTED_TERMINAL_STATE="reported"
if [[ -f "$RULES_FILE" ]]; then
  [[ -z "$MIN_SOURCES" ]]   && MIN_SOURCES=$(jq -r '.thresholds.min_sources // empty' "$RULES_FILE" 2>/dev/null || true)
  [[ -z "$MIN_FINDINGS" ]]  && MIN_FINDINGS=$(jq -r '.thresholds.min_findings // empty' "$RULES_FILE" 2>/dev/null || true)
  [[ -z "$MIN_CITATIONS" ]] && MIN_CITATIONS=$(jq -r '.thresholds.min_citations // empty' "$RULES_FILE" 2>/dev/null || true)
  ETS=$(jq -r '.expected_terminal_state // empty' "$RULES_FILE" 2>/dev/null || true)
  [[ -n "$ETS" ]] && EXPECTED_TERMINAL_STATE="$ETS"
fi
MIN_SOURCES="${MIN_SOURCES:-5}"
MIN_FINDINGS="${MIN_FINDINGS:-2}"
MIN_CITATIONS="${MIN_CITATIONS:-3}"

EVAL_FILE="$RUN_DIR/evaluation.json"
EVENTS_FILE="$RUN_DIR/agent_log/events_full.ndjson"
TOPIC_FINAL_FILE="$RUN_DIR/agent_log/topic_final.json"
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

# ── Metrics from evaluation.json ────────────────────────────────────────────
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

# ── Lifecycle: terminal state ───────────────────────────────────────────────
final_state=""
if [[ -s "$TOPIC_FINAL_FILE" ]]; then
  final_state=$(jq -r '.state // ""' "$TOPIC_FINAL_FILE" 2>/dev/null || echo "")
fi
[[ "$final_state" == "$EXPECTED_TERMINAL_STATE" ]] && STATE_REPORTED=true || STATE_REPORTED=false
[[ "$final_state" == "failed" ]] && STATE_FAILED=true || STATE_FAILED=false

# ── Invariants: stage progression ───────────────────────────────────────────
STAGE_PLAN=false
STAGE_DELIVER=false
if [[ "$HAS_EVENTS" == "true" ]]; then
  # NDJSON may be compact or spaced; parse with jq (skip malformed lines).
  _stage_seen() {
    jq -R 'fromjson? | select(.event_type == "stage.finished" and .payload.stage == $s)' \
      --arg s "$1" "$EVENTS_FILE" 2>/dev/null | grep -q .
  }
  _stage_seen plan && STAGE_PLAN=true
  _stage_seen deliver && STAGE_DELIVER=true
fi

# ── Invariant: citation integrity ───────────────────────────────────────────
# Every sNN cited in report.md (in [..] brackets or NewsCard source-id) must
# resolve to a news.json sources[].id, and at least one citation must exist.
CITED_IDS=""
if [[ "$HAS_REPORT_MD" == "true" ]]; then
  CITED_IDS=$(
    {
      grep -oE '\[[^]]*\]' "$REPORT_MD_FILE" 2>/dev/null | grep -oE 's[0-9]+' || true
      grep -oE 'source-id="s[0-9]+"' "$REPORT_MD_FILE" 2>/dev/null | grep -oE 's[0-9]+' || true
    } | sort -u || true
  )
fi
NEWS_IDS=""
if [[ "$HAS_NEWS" == "true" ]]; then
  NEWS_IDS=$(jq -r '.sources[]?.id // empty' "$NEWS_FILE" 2>/dev/null | sort -u || true)
fi

CITED_COUNT=0
CITATION_MISSING=""
CITATION_OK=true
if [[ -n "$CITED_IDS" ]]; then
  while IFS= read -r cid; do
    [[ -z "$cid" ]] && continue
    CITED_COUNT=$((CITED_COUNT + 1))
    if ! printf '%s\n' "$NEWS_IDS" | grep -qx "$cid"; then
      CITATION_OK=false
      CITATION_MISSING="${CITATION_MISSING:+$CITATION_MISSING,}$cid"
    fi
  done <<< "$CITED_IDS"
else
  CITATION_OK=false
fi
[[ "$CITED_COUNT" -lt 1 ]] && CITATION_OK=false

# ── Build report ────────────────────────────────────────────────────────────
jq -n \
  --arg run_dir "$RUN_DIR" \
  --arg generated_at "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --arg rules_file "$RULES_FILE" \
  --arg eval_file "$EVAL_FILE" \
  --arg events_file "$EVENTS_FILE" \
  --arg topic_final_file "$TOPIC_FINAL_FILE" \
  --arg parsed_file "$PARSED_FILE" \
  --arg intro_md_file "$INTRO_MD_FILE" \
  --arg news_file "$NEWS_FILE" \
  --arg report_json_file "$REPORT_JSON_FILE" \
  --arg report_md_file "$REPORT_MD_FILE" \
  --arg final_state "$final_state" \
  --arg expected_state "$EXPECTED_TERMINAL_STATE" \
  --arg citation_missing "$CITATION_MISSING" \
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
  --argjson cited_count "$CITED_COUNT" \
  --argjson state_reported "$STATE_REPORTED" \
  --argjson state_failed "$STATE_FAILED" \
  --argjson stage_plan "$STAGE_PLAN" \
  --argjson stage_deliver "$STAGE_DELIVER" \
  --argjson citation_ok "$CITATION_OK" \
  --argjson min_sources "$MIN_SOURCES" \
  --argjson min_findings "$MIN_FINDINGS" \
  --argjson min_citations "$MIN_CITATIONS" \
  '
  {
    run_dir: $run_dir,
    generated_at: $generated_at,
    rules_file: $rules_file,
    thresholds: {min_sources: $min_sources, min_findings: $min_findings, min_citations: $min_citations},
    checks: [
      {id: "artifact_evaluation_json",      category: "artifact",    severity: "error", pass: $has_eval,        actual: $eval_file},
      {id: "artifact_events_full_ndjson",   category: "artifact",    severity: "error", pass: $has_events,      actual: $events_file},
      {id: "artifact_parsed_json",          category: "artifact",    severity: "error", pass: $has_parsed,      actual: $parsed_file},
      {id: "artifact_intro_md",             category: "artifact",    severity: "error", pass: $has_intro_md,    actual: $intro_md_file},
      {id: "artifact_news_json",            category: "artifact",    severity: "error", pass: $has_news,        actual: $news_file},
      {id: "artifact_report_json",          category: "artifact",    severity: "error", pass: $has_report_json, actual: $report_json_file},
      {id: "artifact_report_md",            category: "artifact",    severity: "error", pass: $has_report_md,   actual: $report_md_file},
      {id: "tool_errors_zero",              category: "operational", severity: "error", pass: ($tool_errors == 0), actual: $tool_errors, expected: 0},
      {id: "sources_total_threshold",       category: "threshold",   severity: "error", pass: ($sources_total >= $min_sources),      actual: $sources_total,      expected_min: $min_sources},
      {id: "key_findings_threshold",        category: "threshold",   severity: "error", pass: ($key_findings_count >= $min_findings), actual: $key_findings_count, expected_min: $min_findings},
      {id: "unique_citations_threshold",    category: "threshold",   severity: "error", pass: ($unique_citations >= $min_citations),  actual: $unique_citations,   expected_min: $min_citations},
      {id: "terminal_state_reported",       category: "lifecycle",   severity: "error", pass: $state_reported,  actual: $final_state, expected: $expected_state},
      {id: "no_error_terminal",             category: "lifecycle",   severity: "error", pass: ($state_failed | not), actual: $final_state},
      {id: "stage_progression_plan",        category: "invariant",   severity: "error", pass: $stage_plan},
      {id: "stage_progression_deliver",     category: "invariant",   severity: "error", pass: $stage_deliver},
      {id: "citation_integrity",            category: "invariant",   severity: "error", pass: $citation_ok, actual: {cited: $cited_count, unresolved: $citation_missing}}
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
