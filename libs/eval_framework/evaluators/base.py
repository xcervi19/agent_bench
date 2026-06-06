"""Evaluator interface.

An evaluator turns a :class:`RunArtifacts` into a list of per-category
:class:`CategoryScore`. Aggregation into layer/overall scores is done by
:func:`eval_framework.scoring.aggregate`, so evaluators only judge categories.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..artifacts import RunArtifacts
from ..rubric import Rubric
from ..scoring import CategoryScore, EvaluationResult, aggregate


class Evaluator(ABC):
    """Base class for all evaluators."""

    name: str = "base"

    @abstractmethod
    def score_categories(
        self, artifacts: RunArtifacts, rubric: Rubric
    ) -> list[CategoryScore]:
        """Produce one :class:`CategoryScore` per rubric category."""

    def summarize(
        self, artifacts: RunArtifacts, result: EvaluationResult
    ) -> tuple[list[str], list[str], str]:
        """Optional: return (strengths, gaps, notes). Default derives from scores."""
        flat = [(c.name, c.score) for layer in result.layers for c in layer.categories]
        flat.sort(key=lambda kv: kv[1], reverse=True)
        strengths = [f"{n} ({s:.1f}/{result.scale_max})" for n, s in flat[:3] if s >= 3.5]
        gaps = [f"{n} ({s:.1f}/{result.scale_max})" for n, s in flat[::-1][:3] if s <= 2.5]
        return strengths, gaps, ""

    def evaluate(self, artifacts: RunArtifacts, rubric: Rubric) -> EvaluationResult:
        """Full absolute evaluation of one run."""
        scores = self.score_categories(artifacts, rubric)
        result = aggregate(
            rubric,
            scores,
            label=artifacts.label,
            run_dir=artifacts.run_dir,
            topic=artifacts.topic,
            evaluator=self.name,
        )
        strengths, gaps, notes = self.summarize(artifacts, result)
        result.strengths = strengths
        result.gaps = gaps
        result.notes = notes
        return result
