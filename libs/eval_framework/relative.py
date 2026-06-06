"""Relative (pairwise) evaluation and win-rate aggregation.

Mode 2: compare a baseline run against a candidate run and decide whether the
candidate is Better / Equal / Worse — overall, per layer, and per category.
Many pairwise comparisons aggregate into win-rate statistics so we can tell
whether a new agent version improved or degraded system performance.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field

from .scoring import EvaluationResult


class Verdict(StrEnum):
    BETTER = "better"
    EQUAL = "equal"
    WORSE = "worse"


def _verdict(candidate: float, baseline: float, margin: float) -> Verdict:
    diff = candidate - baseline
    if diff > margin:
        return Verdict.BETTER
    if diff < -margin:
        return Verdict.WORSE
    return Verdict.EQUAL


class CategoryDelta(BaseModel):
    category_id: str
    name: str = ""
    layer_id: str = ""
    baseline: float
    candidate: float
    delta: float
    verdict: Verdict


class LayerDelta(BaseModel):
    layer_id: str
    name: str = ""
    baseline: float
    candidate: float
    delta: float
    verdict: Verdict


class PairwiseComparison(BaseModel):
    rubric_name: str = ""
    scale_max: int = 5
    margin: float = 0.2
    baseline_label: str = "baseline"
    candidate_label: str = "candidate"
    topic: str = ""
    overall_baseline: float = 0.0
    overall_candidate: float = 0.0
    overall_delta: float = 0.0
    verdict: Verdict = Verdict.EQUAL
    layer_deltas: list[LayerDelta] = Field(default_factory=list)
    category_deltas: list[CategoryDelta] = Field(default_factory=list)

    def improved_categories(self) -> list[str]:
        return [c.category_id for c in self.category_deltas if c.verdict is Verdict.BETTER]

    def regressed_categories(self) -> list[str]:
        return [c.category_id for c in self.category_deltas if c.verdict is Verdict.WORSE]


def compare(
    baseline: EvaluationResult,
    candidate: EvaluationResult,
    *,
    margin: float = 0.2,
) -> PairwiseComparison:
    """Compare two absolute evaluations into a Better/Equal/Worse verdict."""
    base_cats = {c.category_id: c for layer in baseline.layers for c in layer.categories}
    cand_cats = {c.category_id: c for layer in candidate.layers for c in layer.categories}

    category_deltas: list[CategoryDelta] = []
    for cid, cc in cand_cats.items():
        bc = base_cats.get(cid)
        b_score = bc.score if bc else 0.0
        category_deltas.append(
            CategoryDelta(
                category_id=cid,
                name=cc.name,
                layer_id=cc.layer_id,
                baseline=b_score,
                candidate=cc.score,
                delta=round(cc.score - b_score, 4),
                verdict=_verdict(cc.score, b_score, margin),
            )
        )

    base_layers = {layer.layer_id: layer for layer in baseline.layers}
    layer_deltas: list[LayerDelta] = []
    for layer in candidate.layers:
        b = base_layers.get(layer.layer_id)
        b_score = b.score if b else 0.0
        layer_deltas.append(
            LayerDelta(
                layer_id=layer.layer_id,
                name=layer.name,
                baseline=b_score,
                candidate=layer.score,
                delta=round(layer.score - b_score, 4),
                verdict=_verdict(layer.score, b_score, margin),
            )
        )

    overall_delta = round(candidate.overall_score - baseline.overall_score, 4)
    return PairwiseComparison(
        rubric_name=candidate.rubric_name,
        scale_max=candidate.scale_max,
        margin=margin,
        baseline_label=baseline.label,
        candidate_label=candidate.label,
        topic=candidate.topic or baseline.topic,
        overall_baseline=baseline.overall_score,
        overall_candidate=candidate.overall_score,
        overall_delta=overall_delta,
        verdict=_verdict(candidate.overall_score, baseline.overall_score, margin),
        layer_deltas=layer_deltas,
        category_deltas=category_deltas,
    )


class WinRateStats(BaseModel):
    """Aggregate win-rate over a set of pairwise comparisons."""

    n: int = 0
    better: int = 0
    equal: int = 0
    worse: int = 0
    win_rate: float = 0.0  # better / n
    non_regression_rate: float = 0.0  # (better + equal) / n
    mean_overall_delta: float = 0.0
    per_category_win_rate: dict[str, float] = Field(default_factory=dict)
    per_layer_win_rate: dict[str, float] = Field(default_factory=dict)


def aggregate_win_rate(comparisons: list[PairwiseComparison]) -> WinRateStats:
    """Roll many pairwise comparisons into win-rate statistics."""
    n = len(comparisons)
    if n == 0:
        return WinRateStats()

    better = sum(c.verdict is Verdict.BETTER for c in comparisons)
    equal = sum(c.verdict is Verdict.EQUAL for c in comparisons)
    worse = sum(c.verdict is Verdict.WORSE for c in comparisons)
    mean_delta = round(sum(c.overall_delta for c in comparisons) / n, 4)

    cat_better: dict[str, int] = {}
    cat_total: dict[str, int] = {}
    layer_better: dict[str, int] = {}
    layer_total: dict[str, int] = {}
    for comp in comparisons:
        for cd in comp.category_deltas:
            cat_total[cd.category_id] = cat_total.get(cd.category_id, 0) + 1
            if cd.verdict is Verdict.BETTER:
                cat_better[cd.category_id] = cat_better.get(cd.category_id, 0) + 1
        for ld in comp.layer_deltas:
            layer_total[ld.layer_id] = layer_total.get(ld.layer_id, 0) + 1
            if ld.verdict is Verdict.BETTER:
                layer_better[ld.layer_id] = layer_better.get(ld.layer_id, 0) + 1

    return WinRateStats(
        n=n,
        better=better,
        equal=equal,
        worse=worse,
        win_rate=round(better / n, 4),
        non_regression_rate=round((better + equal) / n, 4),
        mean_overall_delta=mean_delta,
        per_category_win_rate={
            cid: round(cat_better.get(cid, 0) / total, 4) for cid, total in cat_total.items()
        },
        per_layer_win_rate={
            lid: round(layer_better.get(lid, 0) / total, 4) for lid, total in layer_total.items()
        },
    )
