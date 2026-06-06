"""Absolute evaluation (Mode 1) with the offline heuristic evaluator."""

from __future__ import annotations

from pathlib import Path

from eval_framework import default_rubric, evaluate_run, load_run
from eval_framework.evaluators import HeuristicEvaluator


def test_every_category_scored_in_range(good_run: Path):
    result = evaluate_run(str(good_run))
    r = default_rubric()
    scored = result.flat_scores()
    assert set(scored) == set(r.category_ids)
    for cid, score in scored.items():
        assert 0.0 <= score <= 5.0, f"{cid} out of range: {score}"


def test_overall_is_weighted_combo(good_run: Path):
    result = evaluate_run(str(good_run))
    weights = default_rubric().normalized_layer_weights()
    expected = sum(layer.score * weights[layer.layer_id] for layer in result.layers)
    assert abs(result.overall_score - round(expected, 4)) < 1e-3
    assert result.evaluator == "heuristic"


def test_deterministic(good_run: Path):
    a = evaluate_run(str(good_run))
    b = evaluate_run(str(good_run))
    assert a.flat_scores() == b.flat_scores()


def test_good_run_is_reasonably_strong(good_run: Path):
    result = evaluate_run(str(good_run))
    # A healthy multi-source, multi-language, scenario-rich run should land
    # clearly above the midpoint but not be a perfect 5.
    assert 3.0 <= result.overall_score <= 4.8


def test_empty_run_scores_low(tmp_path: Path):
    (tmp_path / "business_output").mkdir()
    result = evaluate_run(str(tmp_path))
    assert result.overall_score < 2.0


def test_information_discovery_emphasis(good_run: Path, degraded_run: Path):
    """Losing primary/non-obvious sources must hurt the discovery layer."""
    good = evaluate_run(str(good_run))
    bad = evaluate_run(str(degraded_run))
    g_disc = good.layer("information_discovery").score
    b_disc = bad.layer("information_discovery").score
    assert b_disc < g_disc


def test_evaluator_class_matches_helper(good_run: Path):
    artifacts = load_run(str(good_run))
    direct = HeuristicEvaluator().evaluate(artifacts, default_rubric())
    via_helper = evaluate_run(str(good_run))
    assert direct.flat_scores() == via_helper.flat_scores()
