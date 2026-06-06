"""Evaluator implementations for the Trading Intelligence Evaluation Framework."""

from __future__ import annotations

from .base import Evaluator
from .heuristic import HeuristicEvaluator

__all__ = ["Evaluator", "HeuristicEvaluator", "get_evaluator", "EVALUATORS"]


def get_evaluator(name: str, **kwargs) -> Evaluator:
    """Factory: resolve an evaluator by name.

    ``heuristic`` is deterministic and offline (default). ``llm`` uses an
    LLM-as-judge via OpenAI and requires network + ``OPENAI_API_KEY``.
    """
    key = (name or "heuristic").lower()
    if key == "heuristic":
        return HeuristicEvaluator(**kwargs)
    if key in ("llm", "openai"):
        from .llm import LLMEvaluator

        return LLMEvaluator(**kwargs)
    raise ValueError(f"Unknown evaluator '{name}'. Available: {sorted(EVALUATORS)}")


EVALUATORS = {"heuristic", "llm"}
