#!/usr/bin/env bash
# scripts/compare_evaluations.sh — Compare two evaluation.json files
#
# Usage:
#   scripts/compare_evaluations.sh <eval_a.json> <eval_b.json>
#   scripts/compare_evaluations.sh testing/results/test1/latest/evaluation.json testing/results/test2/latest/evaluation.json
#
# Output: structured diff showing what improved, regressed, or stayed same.
# Also writes comparison.json next to the second evaluation file.

set -uo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: $0 <eval_a.json> <eval_b.json>" >&2
  exit 1
fi

A="$1"
B="$2"

for f in "$A" "$B"; do
  if [ ! -f "$f" ]; then
    echo "File not found: $f" >&2
    exit 1
  fi
done

A_ENV=$(jq -r '.env' "$A")
B_ENV=$(jq -r '.env' "$B")
A_TS=$(jq -r '.timestamp' "$A")
B_TS=$(jq -r '.timestamp' "$B")

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  EVALUATION COMPARISON"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  A: [$A_ENV] $A_TS"
echo "  B: [$B_ENV] $B_TS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

delta() {
  local label="$1" path="$2" unit="${3:-}" better="${4:-higher}"
  local va vb
  va=$(jq -r "$path // 0" "$A" 2>/dev/null)
  vb=$(jq -r "$path // 0" "$B" 2>/dev/null)

  if [ "$va" = "null" ]; then va=0; fi
  if [ "$vb" = "null" ]; then vb=0; fi

  local diff verdict
  diff=$(echo "$vb - $va" | bc 2>/dev/null || echo "?")

  if [ "$diff" = "0" ] || [ "$diff" = "?" ]; then
    verdict="="
  elif [ "$better" = "higher" ]; then
    if echo "$diff > 0" | bc -l 2>/dev/null | grep -q '^1'; then
      verdict="▲"
    else
      verdict="▼"
    fi
  else
    if echo "$diff < 0" | bc -l 2>/dev/null | grep -q '^1'; then
      verdict="▲"
    else
      verdict="▼"
    fi
  fi

  printf "  %-28s  %8s  %8s  %+8s  %s\n" "$label" "${va}${unit}" "${vb}${unit}" "${diff}${unit}" "$verdict"
}

delta_str() {
  local label="$1" path="$2"
  local va vb
  va=$(jq -r "$path // \"n/a\"" "$A" 2>/dev/null)
  vb=$(jq -r "$path // \"n/a\"" "$B" 2>/dev/null)

  local verdict="="
  [ "$va" != "$vb" ] && verdict="~"
  printf "  %-28s  %-20s  %-20s  %s\n" "$label" "${va:0:20}" "${vb:0:20}" "$verdict"
}

printf "  %-28s  %8s  %8s  %8s  %s\n" "" "A" "B" "Delta" ""
echo "  ─────────────────────────────────────────────────────────────"

echo "  TIMING"
delta "Plan"                ".timing.plan_sec"      "s"  "lower"
delta "Deliver"             ".timing.deliver_sec"    "s"  "lower"
delta "Refresh"             ".timing.refresh_sec"    "s"  "lower"
delta "Total"               ".timing.total_sec"      "s"  "lower"
echo

echo "  COST"
delta "Plan"                ".cost.plan_usd"         "$"  "lower"
delta "Deliver"             ".cost.deliver_usd"      "$"  "lower"
delta "Refresh"             ".cost.refresh_usd"      "$"  "lower"
delta "Total"               ".cost.total_usd"        "$"  "lower"
echo

echo "  PLAN"
delta "Queries"             ".plan.queries_count"    ""   "higher"
delta "Languages"           ".plan.language_count"   ""   "higher"
delta "RAG refs"            ".plan.rag_refs_count"   ""   "higher"
delta "Scenarios"           ".plan.scenarios_count"  ""   "higher"
echo

echo "  DELIVER"
delta "Sources"             ".deliver.sources_total"            ""  "higher"
delta "Unique publishers"   ".deliver.sources_unique_publishers" "" "higher"
delta "Avg relevance"       ".deliver.sources_avg_relevance"    ""  "higher"
delta "Key findings"        ".deliver.key_findings_count"       ""  "higher"
delta "Scenarios"           ".deliver.scenarios_count"          ""  "higher"
delta "Report lines"        ".deliver.report_lines"             ""  "higher"
delta "Report words"        ".deliver.report_words"             ""  "higher"
delta "Unique citations"    ".deliver.unique_citations"         ""  "higher"
delta "Open questions"      ".deliver.open_questions_count"     ""  "higher"
delta "Next queries"        ".deliver.next_queries_count"       ""  "higher"
echo

echo "  QUALITY"
delta_str "Thesis status"   ".deliver.thesis_status"
delta "Queries executed"    ".deliver.queries_executed"          "" "higher"
delta "Queries w/ results"  ".deliver.queries_with_results"     "" "higher"
echo

echo "  EVENTS"
delta "Total events"        ".events.total_events"     "" "higher"
delta "Tool calls"          ".events.tool_calls"       "" ""
delta "Tool errors"         ".events.tool_errors"      "" "lower"
echo

echo "  REFRESH"
delta "New sources"         ".refresh.new_sources_count"  "" "higher"
delta "Refresh cost"        ".refresh.cost_usd"           "$" "lower"
echo

# Build comparison.json
COMP_DIR=$(dirname "$B")
jq -nc \
  --slurpfile a "$A" --slurpfile b "$B" \
  --arg a_path "$A" --arg b_path "$B" \
  '{
    compared_at: (now | todate),
    a: {env: $a[0].env, timestamp: $a[0].timestamp, path: $a_path},
    b: {env: $b[0].env, timestamp: $b[0].timestamp, path: $b_path},
    delta: {
      timing: {
        plan_sec: (($b[0].timing.plan_sec // 0) - ($a[0].timing.plan_sec // 0)),
        deliver_sec: (($b[0].timing.deliver_sec // 0) - ($a[0].timing.deliver_sec // 0)),
        total_sec: (($b[0].timing.total_sec // 0) - ($a[0].timing.total_sec // 0))
      },
      cost: {
        total_usd: (($b[0].cost.total_usd // 0) - ($a[0].cost.total_usd // 0))
      },
      deliver: {
        sources: (($b[0].deliver.sources_total // 0) - ($a[0].deliver.sources_total // 0)),
        findings: (($b[0].deliver.key_findings_count // 0) - ($a[0].deliver.key_findings_count // 0)),
        citations: (($b[0].deliver.unique_citations // 0) - ($a[0].deliver.unique_citations // 0)),
        report_words: (($b[0].deliver.report_words // 0) - ($a[0].deliver.report_words // 0))
      }
    }
  }' > "$COMP_DIR/comparison.json"

echo "  comparison.json → $COMP_DIR/comparison.json"
echo
