"""Rubric structure, weighting, and configurability."""

from __future__ import annotations

from eval_framework import default_rubric


def test_default_rubric_shape():
    r = default_rubric()
    assert r.name == "trading_intelligence"
    assert [layer.id for layer in r.layers] == [
        "information_discovery",
        "research_quality",
        "trading_intelligence",
    ]
    # 5 + 5 + 4 = 14 categories total
    assert len(r.category_ids) == 14
    assert len(set(r.category_ids)) == 14


def test_suggested_layer_weights():
    r = default_rubric()
    lw = r.normalized_layer_weights()
    assert abs(lw["information_discovery"] - 0.40) < 1e-9
    assert abs(lw["research_quality"] - 0.30) < 1e-9
    assert abs(lw["trading_intelligence"] - 0.30) < 1e-9
    assert abs(sum(lw.values()) - 1.0) < 1e-9


def test_category_weights_normalize_within_layer():
    r = default_rubric()
    for layer in r.layers:
        cw = layer.normalized_category_weights()
        assert abs(sum(cw.values()) - 1.0) < 1e-9


def test_weights_are_configurable():
    r = default_rubric().with_weights(
        layer_weights={
            "information_discovery": 0.5,
            "research_quality": 0.25,
            "trading_intelligence": 0.25,
        }
    )
    lw = r.normalized_layer_weights()
    assert abs(lw["information_discovery"] - 0.5) < 1e-9
    # original bundled rubric is untouched
    assert abs(default_rubric().normalized_layer_weights()["information_discovery"] - 0.4) < 1e-9


def test_scale_is_zero_to_five():
    r = default_rubric()
    assert r.scale.min == 0
    assert r.scale.max == 5
