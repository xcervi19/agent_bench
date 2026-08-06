# Migrate the LLM-as-judge evaluator from OpenAI to Claude — #43

**Status:** planned
**Lane:** Platform / Evaluation
**Depends on:** —
**Blocks:** #42 (search evidence judging pass — must not add a second judge provider), #41 (multi-run evaluation baseline)

---

## Goal / Problem

Project policy: **OpenAI is used only for embeddings. Every other LLM call goes through Claude Code.**

Today the evaluation framework's LLM-as-judge violates this. `libs/eval_framework/evaluators/llm.py` instantiates an `OpenAI()` client directly and calls `chat.completions.create`; the model resolves from `EVAL_LLM_MODEL` / `OPENAI_MODEL` with a `gpt-4o` fallback, and `libs/agentic_core/config.py` carries a separate `openai_model: "gpt-4o-mini"` default. It is reached via `--evaluator llm` on the eval CLI.

This is the one component conceptually closest to the judging pass planned in #42. Leaving it on OpenAI means shipping two quality judges from two providers side by side.

## Solution / What to deliver

Replace the OpenAI call path with a Claude Code slash command, keeping the evaluator interface unchanged.

1. **Slash command** in `claude_agent_fe/.claude/commands/` (e.g. `eval-score.md`), following the `newsfind-queries` pattern: a strict output contract ("stdout MUST be exactly one JSON object"), a JSON schema under `.claude/schemas/`, and no prose outside the JSON. `SYSTEM_PROMPT` and `_build_user_prompt()` from `llm.py` port over as the command body and its argument payload — the rubric semantics do not change.
2. **`ClaudeEvaluator`** implementing the same `Evaluator` interface (`score_categories`, `summarize`), invoking the command through the existing runner rather than a new subprocess wrapper.
3. **Registry + CLI**: register in `evaluators/__init__.py` (`get_evaluator`, `EVALUATORS`) and make it the target of `--evaluator llm`. Keep `heuristic` untouched as the offline default.
4. **Remove the OpenAI judge** once the new one is validated: delete `LLMEvaluator`, drop `openai_model` from `libs/agentic_core/config.py`, and update the `--evaluator llm` help text and `evaluators/__init__.py` docstring, which both still say OpenAI. The `openai` dependency in `pyproject.toml` stays — embeddings still need it.

## Model choice

Start with **Haiku 4.5** — the cheap tier, and the judging payload is a bounded JSON blob (report + news + capped `report_md`/`intro_md`), not an open-ended reasoning task. Escalate only if validation below fails.

Note the payload is trimmed to fit today's limits (`report_md[:12000]`, `intro_md[:4000]`); re-check those caps against the chosen model's context window rather than carrying them over unexamined.

## Validation — the load-bearing part

**Changing the judge silently re-baselines every historical score.** Scores produced by `gpt-4o` and by a Claude model are not comparable, and `testing/baselines/` plus `scripts/compare_evaluations.sh` assume a stable scale.

- Re-score the frozen baseline (`testing/baselines/hormuz_90d_2026-08-01/`) with the new judge and **keep both score sets**, labelled by judge, so trend lines break visibly instead of silently.
- Compare per-category, not just the overall number — a judge swap that holds the average while redistributing categories is still a regression.
- Judge the same run several times and check spread. A judge that is cheap but noisy is not usable for tracking runs over time.
- If Haiku's scores diverge materially or prove unstable, record the finding and escalate the model rather than tuning the rubric to fit.

## Open question

Whether the judging pass in #42 also runs as a slash command, or goes to the API directly for batching. This ticket settles the evaluator only. At the volumes #42 implies (hundreds of documents per run), one CLI process per document is a materially different cost and latency profile than one batched call — decide there, not here.

## Acceptance criteria

- [ ] No OpenAI client remains outside `apps/rag_adhoc/services/embeddings.py`.
- [ ] `--evaluator llm` runs end-to-end through Claude Code and returns one score per rubric category id.
- [ ] Output validates against the committed JSON schema; malformed output fails loudly rather than scoring zeros.
- [ ] The frozen baseline is re-scored, both score sets are committed, and per-category deltas are written up.
- [ ] `evaluators/__init__.py` docstring and CLI help no longer reference OpenAI.
- [ ] Tests cover the evaluator with a stubbed runner (no network), mirroring the existing `client=` injection seam.
