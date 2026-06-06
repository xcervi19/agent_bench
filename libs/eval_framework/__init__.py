"""Trading Intelligence Evaluation Framework.

A configurable, repeatable framework for judging whether the Newsfind agent
produces valuable trading intelligence — emphasizing information *discovery*
quality, not writing quality.

Two evaluation modes:

* **Absolute** — score one run against the rubric (3 weighted layers, 14
  categories, 0-5 each).
* **Relative** — compare a baseline vs a candidate run (Better/Equal/Worse,
  with win-rate aggregation across many comparisons).

Quick start::

    from eval_framework import evaluate_run, compare_runs

    result = evaluate_run("testing/results/test1/latest")
    print(result.overall_score, result.overall_score_100)

    comp = compare_runs("runs/baseline", "runs/candidate")
    print(comp.verdict)
"""

from __future__ import annotations

from .artifacts import RunArtifacts, load_run
from .benchmarks import (
    BenchmarkProvider,
    FixtureProvider,
    benchmark_provider,
    get_provider,
    list_providers,
    register_provider,
)
from .evaluators import Evaluator, HeuristicEvaluator, get_evaluator
from .relative import (
    PairwiseComparison,
    Verdict,
    WinRateStats,
    aggregate_win_rate,
    compare,
)
from .rubric import Rubric, default_rubric, load_rubric
from .scoring import CategoryScore, EvaluationResult, LayerScore, aggregate

__all__ = [
    "RunArtifacts",
    "load_run",
    "Rubric",
    "load_rubric",
    "default_rubric",
    "CategoryScore",
    "LayerScore",
    "EvaluationResult",
    "aggregate",
    "Evaluator",
    "HeuristicEvaluator",
    "get_evaluator",
    "PairwiseComparison",
    "WinRateStats",
    "Verdict",
    "compare",
    "aggregate_win_rate",
    "BenchmarkProvider",
    "FixtureProvider",
    "register_provider",
    "benchmark_provider",
    "get_provider",
    "list_providers",
    "evaluate_run",
    "evaluate_artifacts",
    "compare_runs",
]


def evaluate_artifacts(
    artifacts: RunArtifacts,
    *,
    label: str | None = None,
    evaluator: str = "heuristic",
    rubric: Rubric | None = None,
    layer_weights: dict[str, float] | None = None,
    category_weights: dict[str, float] | None = None,
    **evaluator_kwargs,
) -> EvaluationResult:
    """Absolute evaluation of already-loaded artifacts."""
    if label:
        artifacts.label = label
    rb = rubric or default_rubric()
    if layer_weights or category_weights:
        rb = rb.with_weights(layer_weights, category_weights)
    ev = get_evaluator(evaluator, **evaluator_kwargs)
    return ev.evaluate(artifacts, rb)


def evaluate_run(
    run_dir: str,
    *,
    label: str | None = None,
    evaluator: str = "heuristic",
    rubric: Rubric | None = None,
    layer_weights: dict[str, float] | None = None,
    category_weights: dict[str, float] | None = None,
    **evaluator_kwargs,
) -> EvaluationResult:
    """Absolute evaluation of a run directory (Mode 1)."""
    artifacts = load_run(run_dir, label=label)
    return evaluate_artifacts(
        artifacts,
        evaluator=evaluator,
        rubric=rubric,
        layer_weights=layer_weights,
        category_weights=category_weights,
        **evaluator_kwargs,
    )


def compare_runs(
    baseline_dir: str,
    candidate_dir: str,
    *,
    evaluator: str = "heuristic",
    rubric: Rubric | None = None,
    margin: float | None = None,
    layer_weights: dict[str, float] | None = None,
    category_weights: dict[str, float] | None = None,
    **evaluator_kwargs,
) -> PairwiseComparison:
    """Relative evaluation of two run directories (Mode 2)."""
    rb = rubric or default_rubric()
    if layer_weights or category_weights:
        rb = rb.with_weights(layer_weights, category_weights)
    base = evaluate_run(
        baseline_dir, label="baseline", evaluator=evaluator, rubric=rb, **evaluator_kwargs
    )
    cand = evaluate_run(
        candidate_dir, label="candidate", evaluator=evaluator, rubric=rb, **evaluator_kwargs
    )
    return compare(base, cand, margin=margin if margin is not None else rb.relative_margin)
