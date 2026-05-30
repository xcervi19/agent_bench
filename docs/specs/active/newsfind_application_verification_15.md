# Newsfind application verification — #15

**Status:** active (queued)  
**Depends on:** #11 (stable run harness), #13 (multi-env)  
**Lane:** B — *Did the application work correctly? Did we break known behavior?*  
**See also:** `docs/specs/active/00_testing_vs_evaluation.md`

## Goal

**Automated PASS/FAIL** after a run (or on CI): confirm the pipeline completed, artifacts are valid, events are healthy, and known operational failures are absent. **No manual diff** required for baseline safety before demo or deploy.

This is **classic application testing** — regression and verification — not judgment of whether the report is insightful for traders.

## Core question (one sentence)

*“Did we break the product’s mechanics and contracts, or reintroduce failures we already know how to detect?”*

## Distinction from #18 (business output evaluation)

| | **#15 (this ticket)** | **#18** |
|--|------------------------|---------|
| Question | Does it **work**? | Is it **useful**? |
| Verdict | PASS / FAIL | Better / weaker / good enough for business |
| Automation | Yes — scripts, CI | Mostly human / evaluator agent + rubric |
| Example pass | `tool_errors == 0`, report has valid `[sN]` | “Findings are specific enough to hedge Hormuz exposure” |

#11 answers: *“What happened in this run?”* (data)  
#15 answers: *“Is the run **valid** for release?”* (gate)  
#18 answers: *“Is the run **valuable** for the user?”* (judgment)

## In scope

### 1. Structural / schema checks

Validate outputs against command contracts (`claude_agent_fe/.claude/commands/`):

- **Plan:** `parsed.json` — `queries[]` shape, ids, languages; `intro.json` / `summary.json` present; `intro.md` non-empty
- **Deliver:** `news.json` — `sources[]` with `url`, `relevance_score`, `source_class`; `report.json` — `key_findings`, scenarios; `report.md` — citation markers `[sN]`
- **Refresh:** `delta.json` / refresh artifacts when monitoring enabled

Use JSON Schema or `jq` assertions; fail with file + field path.

### 2. Threshold gates (hard, not “quality score”)

Extend `vectors.json` — these are **regression guards**, not business excellence:

- Plan: `min_queries`, `max_queries`, `min_rag_refs`
- Deliver: `min_sources`, `min_findings`, `min_scenarios`, `report_min_lines`
- Events: `tool_errors == 0`, topic reaches `reported` (or expected terminal state)
- Cost ceiling (optional per env): `cost.total_usd < max`

Output: `qa_report.json` with `{passed, failures[]}`.

### 3. Event / pipeline invariants

From `agent_log/events_full.ndjson` and `topic_final.json`:

- Required sequence: `topic.created` → `stage.finished` (plan) → `needs_input` → … → `report.ready`
- No `event_type: error` before success
- `state.changed` ends in `reported` (not `failed` / stuck `planning`)
- Stage timing present on `stage.finished`

### 4. Smoke / health vectors

Lightweight vectors in `testing/vectors.json` (e.g. `V000_health`):

- `GET /readyz` only, or minimal topic with short timeout
- Run before/after deploy on `test1` / `test2`

### 5. Known-bad behavior catalog

Documented checks for failures seen in ops (extend over time):

| Check | Example failure |
|-------|-----------------|
| Permission on `/state/news` | Topic stuck `planning`, empty events |
| Empty `events_full.ndjson` | SSE/DB write failure |
| `summary.json` missing after stage | Slash command did not complete |
| Report citations without matching sources | Broken `[sN]` integrity |

*(“All sources undated” may be a **warning** for #18; in #15 only if we define it as a known regression.)*

### 6. Runner integration

- `scripts/qa_check_run.sh <run_dir>` — reads `evaluation.json` + `business_output/` + `agent_log/`, writes `qa_report.json`, exit 1 on fail
- `test_vector_runner.sh` calls it at end of run (after #17 thin gate proves the hook)
- CI: vector on `test1` after deploy → `qa_check_run.sh` → block if fail

### 7. Comparison / baselines (later)

- Store last-known-good `evaluation.json` per env as `testing/baselines/<env>/V001.json`
- Fail if **mechanical** metrics drop below baseline — not “worse writing quality”

## Out of scope (for #15 v1)

- LLM-as-judge business value scoring → **#18**
- Cache-hit / warm-path testing — separate ticket
- Frontend E2E (Playwright) — pre-frontend phase
- Load/stress testing

## Artifacts (planned)

| Path | Role |
|------|------|
| `testing/qa_rules.json` | Machine-readable rules + thresholds per vector |
| `scripts/qa_check_run.sh` | Post-run assertion engine |
| `testing/results/<env>/<ts>/qa_report.json` | PASS/FAIL + failure list |
| `testing/baselines/` | Optional golden **mechanical** metrics per env |

## Acceptance criteria (when implemented)

- [ ] `qa_check_run.sh` fails a run with injected bad artifact (local test)
- [ ] All rules in `qa_rules.json` documented with rationale (operational, not business)
- [ ] V001 full run produces `qa_report.json` with `passed: true` on healthy instance
- [ ] CI hook documented in `testing/README.md` under **Application verification**
- [ ] Docs state clearly: #15 = gate; #18 = business judgment

## Related

- `docs/specs/done/rag_full_stable_evaluation_11.md` — harness (#11)
- `docs/specs/active/business_output_evaluation_18.md` — Lane A
- `testing/vectors.json`, `scripts/test_vector_runner.sh`, `scripts/compare_evaluations.sh`
