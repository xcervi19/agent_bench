"""Weighted aggregation math (category -> layer -> overall)."""

from __future__ import annotations

from eval_framework import default_rubric
from eval_framework.scoring import CategoryScore, aggregate


def _all_scores(rubric, value: float) -> list[CategoryScore]:
    return [CategoryScore(category_id=cid, score=value) for cid in rubric.category_ids]


def test_uniform_scores_propagate():
    r = default_rubric()
    result = aggregate(r, _all_scores(r, 4.0))
    for layer in result.layers:
        assert abs(layer.score - 4.0) < 1e-9
    assert abs(result.overall_score - 4.0) < 1e-9
    assert abs(result.overall_score_100 - 80.0) < 1e-6


def test_layer_weighting_changes_overall():
    r = default_rubric()
    scores = {
        "information_discovery": 5.0,
        "research_quality": 0.0,
        "trading_intelligence": 0.0,
    }
    cats = [
        CategoryScore(category_id=c.id, score=scores[layer.id])
        for layer in r.layers
        for c in layer.categories
    ]
    result = aggregate(r, cats)
    # Only Information Discovery (40%) is non-zero -> overall == 5 * 0.40
    assert abs(result.overall_score - 2.0) < 1e-9
    assert abs(result.layer("information_discovery").score - 5.0) < 1e-9
    assert abs(result.layer("research_quality").score - 0.0) < 1e-9


def test_missing_category_defaults_to_zero():
    r = default_rubric()
    partial = [CategoryScore(category_id="actionability", score=5.0)]
    result = aggregate(r, partial)
    assert result.category("actionability").score == 5.0
    assert result.category("primary_source_discovery").score == 0.0
