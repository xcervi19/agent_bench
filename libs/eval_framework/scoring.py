"""Score models and weighted aggregation (category -> layer -> overall).

All raw category scores live on the rubric scale (0-5). Aggregation produces
weighted layer scores and an overall score on the same scale, plus a 0-100
normalized view for reporting and comparison.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from .rubric import Rubric


class CategoryScore(BaseModel):
    category_id: str
    name: str = ""
    layer_id: str = ""
    score: float  # 0..scale.max
    rationale: str = ""
    evidence: list[str] = Field(default_factory=list)


class LayerScore(BaseModel):
    layer_id: str
    name: str = ""
    weight: float  # normalized layer weight (0..1)
    score: float  # weighted avg of category scores, on rubric scale
    categories: list[CategoryScore] = Field(default_factory=list)


class EvaluationResult(BaseModel):
    """Absolute evaluation of a single run."""

    rubric_name: str
    scale_max: int = 5
    label: str = "run"
    run_dir: str | None = None
    topic: str = ""
    evaluator: str = ""
    overall_score: float = 0.0  # on rubric scale
    overall_score_100: float = 0.0  # normalized 0..100
    layers: list[LayerScore] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    notes: str = ""

    def category(self, category_id: str) -> CategoryScore | None:
        for layer in self.layers:
            for c in layer.categories:
                if c.category_id == category_id:
                    return c
        return None

    def layer(self, layer_id: str) -> LayerScore | None:
        for layer in self.layers:
            if layer.layer_id == layer_id:
                return layer
        return None

    def flat_scores(self) -> dict[str, float]:
        return {c.category_id: c.score for layer in self.layers for c in layer.categories}


def aggregate(
    rubric: Rubric,
    category_scores: list[CategoryScore],
    *,
    label: str = "run",
    run_dir: str | None = None,
    topic: str = "",
    evaluator: str = "",
    strengths: list[str] | None = None,
    gaps: list[str] | None = None,
    notes: str = "",
) -> EvaluationResult:
    """Combine per-category scores into layer + overall scores using rubric weights."""
    by_id = {c.category_id: c for c in category_scores}
    layer_weights = rubric.normalized_layer_weights()
    scale_max = rubric.scale.max

    layer_results: list[LayerScore] = []
    overall = 0.0
    for layer in rubric.layers:
        cat_weights = layer.normalized_category_weights()
        cat_scores: list[CategoryScore] = []
        layer_total = 0.0
        for cat in layer.categories:
            cs = by_id.get(cat.id)
            if cs is None:
                cs = CategoryScore(
                    category_id=cat.id,
                    name=cat.name,
                    layer_id=layer.id,
                    score=0.0,
                    rationale="No score produced for this category.",
                )
            else:
                cs = cs.model_copy(update={"name": cat.name, "layer_id": layer.id})
            cat_scores.append(cs)
            layer_total += cs.score * cat_weights[cat.id]

        layer_results.append(
            LayerScore(
                layer_id=layer.id,
                name=layer.name,
                weight=layer_weights[layer.id],
                score=round(layer_total, 4),
                categories=cat_scores,
            )
        )
        overall += layer_total * layer_weights[layer.id]

    overall = round(overall, 4)
    return EvaluationResult(
        rubric_name=rubric.name,
        scale_max=scale_max,
        label=label,
        run_dir=run_dir,
        topic=topic,
        evaluator=evaluator,
        overall_score=overall,
        overall_score_100=round(100.0 * overall / scale_max, 2) if scale_max else 0.0,
        layers=layer_results,
        strengths=strengths or [],
        gaps=gaps or [],
        notes=notes,
    )
