# Functional regression guardrails — #15

**Status:** active (queued)
**Depends on:** #11 (stable evaluation harness), #13 (multi-env)
**Sibling ticket:** #18 (result quality evaluation — information value)

> **Naming note.** This spec was previously called *“Newsfind QA automation”*. The
> word *QA* turned out to overload two very different concerns. We now split
> them explicitly. This ticket (#15) covers **classic application testing**:
> *“did we break the app?”*. Anything about how *useful* / *informative* /
> *trader-grade* the output is moves to **#18 — Result quality evaluation**.

## Three evaluation axes (read this first)

The Newsfind pipeline produces both **system behavior** (events, tool calls,
state transitions, artifacts) and a **product output** (intro, plan, news,
report, refresh deltas). These two surfaces need very different kinds of
checks. We track them as three separate tickets so neither concern dilutes the
other:

| Axis | Ticket | Question it answers | Mode |
|------|--------|---------------------|------|
| **Explore / compare** | #11 (done) | *How does this run compare to another?* | Descriptive — produces `evaluation.json` with 40+ metrics |
| **Functional regression guardrails** | **#15 (this)** | *Did we break something we already know how to detect?* | Hard pass/fail on **engineering invariants** |
| **Result quality evaluation** | #18 | *Is this output actually useful for a commodity trader?* | Sophisticated review — rubric, LLM-as-judge, human spot-check |

#15 is the **classic test layer**: schema, sequencing, error counts, state
machine, smoke health. It must run cheaply, deterministically, and gate
deployments. It deliberately does **not** look at whether findings are
insightful, whether scenarios are plausible, or whether sources are the
*right* sources — those are #18 concerns.

## Goal

A functional regression layer on top of the existing runner. After each run
(or on CI), assert engineering invariants on artifacts, events, API behavior,
and operational thresholds. Fail fast with a clear report. **No subjective
judgement of content.** No manual diff required for baseline safety.

## In scope (what counts as “functional” here)

A check belongs in #15 **if and only if** failing it means *the application is
broken or behaving incorrectly*, independent of how good the content is. If
the same failure could plausibly be reported as “the report was thin / the
sources were weak / the analysis was shallow”, it belongs in #18.

### 1. Structural / schema checks

Validate outputs against command contracts (`claude_agent_fe/.claude/commands/`):

- **Plan:** `parsed.json` — present, valid JSON, has `queries[]` field with
  the documented shape (id, language, intent), `intro.json` / `summary.json`
  present, `intro.md` non-empty (file exists and > 0 bytes — *not* a
  judgement on writing quality).
- **Deliver:** `news.json` — present, `sources[]` entries have required keys
  (`url`, `relevance_score`, `source_class`), URLs parse; `report.json`
  present with `key_findings` and `scenarios` keys (existence, not depth);
  `report.md` non-empty.
- **Refresh:** `delta.json` / refresh artifacts present and parse when
  monitoring is enabled.
- **Citation integrity (structural):** every `[sN]` marker in `report.md`
  resolves to an `sN` entry in `news.json` and vice-versa. *(Whether the
  citation is the right citation for the claim is #18.)*

Use JSON Schema or `jq` assertions; fail with file + field path.

### 2. Operational threshold gates

Hard gates on **engineering health**, not content depth:

- Events: `tool_errors == 0`
- Events: topic reaches the expected terminal state (`reported`, or
  `completed` for refresh runs); never stuck in `planning` / `delivering`
- Stage timing present on every `stage.finished`
- Cost ceiling per env (`cost.total_usd < max`) — operational guard against
  runaway spend, not a quality signal
- Wall-clock ceiling per stage (`plan_sec`, `deliver_sec`) — catches hangs

> ❌ **Out — moved to #18:** `min_sources`, `min_findings`, `min_scenarios`,
> `min_queries`, `min_rag_refs`, `report_min_lines`, `unique_citations >= N`,
> `sources_avg_relevance >= X`, “sources newer than Y”, etc. These are
> *content quality* claims. They produce a number that means something to a
> trader, not to a service. They live in #18.

### 3. Event / pipeline invariants

From `agent_log/events_full.ndjson` and `topic_final.json`:

- Required sequence: `topic.created` → `stage.finished` (plan) →
  `needs_input` → … → `report.ready`
- No `event_type: error` before success
- `state.changed` ends in `reported` (not `failed`, not stuck `planning`)
- SSE replay invariant: full event log fetched from DB matches live SSE
  stream length within tolerance (catches DB-write failures masked by SSE)

### 4. Smoke / health vectors

Lightweight vectors in `testing/vectors.json` (e.g. `V000_health`):

- `GET /readyz` only, or minimal topic with short timeout
- Run before/after deploy on `test1` / `test2`
- Purpose: *the service is up and routing correctly* — not *the service
  produces good research*.

### 5. Known-bad behavior catalog (engineering failures only)

Documented checks for **operational failures** seen in ops; extended over
time. Each entry must point to a concrete system-level cause:

| Check | Engineering failure detected |
|-------|------------------------------|
| Permission on `/state/news` | Topic stuck `planning`, empty events — disk/permissions |
| Empty `events_full.ndjson` | SSE / DB write pipeline broken |
| `summary.json` missing after stage.finished | Slash command did not complete |
| All sources have `relevance_score == null` | Scoring path bypassed (code regression), **not** “the scores look low” |
| Report citations without matching sources | Broken `[sN]` integrity (template / writer regression) |
| `RAG unavailable — no .env configuration found` in events | Container env-injection regression (see `STATUS.md` known bug) |

> Anything of the form “sources looked weak”, “findings were generic”,
> “scenarios were repetitive” → #18, not here.

### 6. Runner integration

- `scripts/qa_check_run.sh <run_dir>` — reads `evaluation.json` +
  `business_output/` + `agent_log/`, evaluates the rules above, writes
  `qa_report.json`, exit 1 on any failure.
- Optional: `test_vector_runner.sh` calls it at end of STEP 6.
- CI: run vector on `test1` after deploy → `qa_check_run.sh` → block deploy
  if fail.

## Explicitly out of scope (belongs to #18)

- Whether the **report is informative for a trader**
- Whether **sources are primary / recent / diverse** at a quality level
  (structural existence is in scope; “are these the right kind of sources”
  is not)
- Whether **findings are actionable** or **scenarios plausible**
- Whether **citations support the claim they cite** (the link is structural;
  the claim-evidence fit is judgement)
- Quality drift over time (last-known-good metric baselines for content
  depth) — moves to #18’s baselines section
- LLM-as-judge scoring of any kind
- Cross-instance content quality comparison (compare timing/cost/errors here;
  compare content quality in #18)

## Also out of scope (different tickets)

- Cache-hit / warm-path testing (`/newsfind-queries` + `force_refresh: false`)
- Frontend E2E (Playwright) — see #16
- Load / stress testing

## Artifacts (planned)

| Path | Role |
|------|------|
| `testing/qa_rules.json` | Machine-readable functional rules + operational thresholds per vector |
| `scripts/qa_check_run.sh` | Post-run assertion engine (functional only) |
| `testing/results/<env>/<ts>/qa_report.json` | Pass/fail + failure list |
| `testing/regression_known_bad.md` | Living catalog of engineering failure patterns |

## Acceptance criteria (when implemented)

- [ ] `qa_check_run.sh` fails a run with an injected bad artifact (local test)
- [ ] All rules in `qa_rules.json` documented with a one-line **engineering
      rationale** (which code path / regression each rule guards)
- [ ] No rule in `qa_rules.json` makes a content-quality claim. Reviewer
      checklist: every rule must answer “if this fails, what is broken in the
      *system*?” — not “the output looks worse”.
- [ ] V001 full run produces `qa_report.json` with `passed: true` on a
      healthy instance
- [ ] CI hook documented in `testing/README.md`
- [ ] Clear split documented in this file and in #17 / #18 cross-references:
      #11 = explore/compare, **#15 = functional regression**, #18 = quality

## Related

- `docs/specs/done/rag_full_stable_evaluation_11.md` — evaluation harness (#11)
- `docs/specs/active/result_quality_evaluation_18.md` — sibling ticket for
  information-value evaluation (#18)
- `docs/specs/active/pilot_ops_v1_17.md` — uses the thin functional gate from
  this spec
- `docs/specs/done/reproducible_artifacts_and_cache.md` — cache path
- `testing/vectors.json`, `scripts/test_vector_runner.sh`,
  `scripts/compare_evaluations.sh`
