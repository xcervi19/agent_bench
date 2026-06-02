# Legacy Scripts

Scripts in this folder are deprecated and kept only as fallback/manual tools.

Primary dev testing flow is:

1. `scripts/test_vector_runner.sh --env test1`
2. `scripts/qa_check_run.sh --run-dir testing/results/test1/latest`
3. `scripts/compare_evaluations.sh <eval_a.json> <eval_b.json>` (optional)

Use legacy scripts only when you explicitly need their old behavior.

Note: `scripts/test_refresh_cycle.sh` and `scripts/test_newsfind.sh` are intentionally **not** in legacy.
They are specialized debug tools and stay at top-level.
