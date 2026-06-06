"""Relative evaluation (Mode 2): pairwise verdicts + win-rate aggregation."""

from __future__ import annotations

from pathlib import Path

from eval_framework import Verdict, aggregate_win_rate, compare_runs
from eval_framework.relative import aggregate_win_rate as agg
from eval_framework.relative import compare
from eval_framework.rubric import default_rubric
from eval_framework.scoring import CategoryScore, aggregate


def test_self_comparison_is_equal(good_run: Path):
    comp = compare_runs(str(good_run), str(good_run))
    assert comp.verdict is Verdict.EQUAL
    assert abs(comp.overall_delta) < 1e-9
    assert all(cd.verdict is Verdict.EQUAL for cd in comp.category_deltas)


def test_degraded_candidate_is_worse(good_run: Path, degraded_run: Path):
    comp = compare_runs(str(good_run), str(degraded_run))
    assert comp.verdict is Verdict.WORSE
    assert comp.overall_delta < 0
    assert len(comp.regressed_categories()) >= 3


def test_improved_candidate_is_better(good_run: Path, degraded_run: Path):
    # Swap roles: from a weak baseline to the strong run -> BETTER.
    comp = compare_runs(str(degraded_run), str(good_run))
    assert comp.verdict is Verdict.BETTER
    assert comp.overall_delta > 0


def test_margin_creates_equal_band():
    r = default_rubric()
    base = aggregate(r, [CategoryScore(category_id=c, score=3.0) for c in r.category_ids])
    cand = aggregate(r, [CategoryScore(category_id=c, score=3.1) for c in r.category_ids])
    # Δ = 0.1 < margin 0.2 -> EQUAL
    assert compare(base, cand, margin=0.2).verdict is Verdict.EQUAL
    # Tighter margin flips it to BETTER
    assert compare(base, cand, margin=0.05).verdict is Verdict.BETTER


def test_win_rate_aggregation(good_run: Path, degraded_run: Path):
    wins = compare_runs(str(degraded_run), str(good_run))  # better
    losses = compare_runs(str(good_run), str(degraded_run))  # worse
    ties = compare_runs(str(good_run), str(good_run))  # equal
    stats = aggregate_win_rate([wins, losses, ties])
    assert stats.n == 3
    assert stats.better == 1
    assert stats.worse == 1
    assert stats.equal == 1
    assert abs(stats.win_rate - 1 / 3) < 1e-3
    assert abs(stats.non_regression_rate - 2 / 3) < 1e-3
    # per-layer / per-category win rates are populated
    assert set(stats.per_layer_win_rate) == set(default_rubric().layer_ids)


def test_empty_aggregation_is_safe():
    stats = agg([])
    assert stats.n == 0
    assert stats.win_rate == 0.0
