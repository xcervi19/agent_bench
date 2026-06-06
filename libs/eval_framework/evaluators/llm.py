"""LLM-as-judge evaluator (Output Quality Curator).

Uses an LLM to apply the rubric as a senior trading analyst would. The model is
given the rubric, the run artifacts, and hard guardrails (judge relevance not
volume; never equate tool_errors==0 or large source counts with quality; cite
the artifact being judged). It returns one 0-5 score + rationale per category.

Requires network access and ``OPENAI_API_KEY``. Offline use should pick the
``heuristic`` evaluator instead.
"""

from __future__ import annotations

import json
import os

from ..artifacts import RunArtifacts
from ..rubric import Rubric
from ..scoring import CategoryScore
from .base import Evaluator

SYSTEM_PROMPT = """\
You are an Output Quality Curator: a senior trading analyst at a professional \
trading organization (energy/commodity trading firm, quant fund, asset manager, \
or market-intelligence desk). You do NOT write the report; you judge it.

Apply the provided rubric strictly. Hard rules:
- Judge RELEVANCE, SPECIFICITY, and DECISION VALUE, never volume.
- NEVER treat zero tool errors or large source counts as evidence of quality.
- The system's most important capability is information DISCOVERY (finding the \
original/primary, fresh, non-obvious sources), not writing.
- Cite the specific artifact/source you are judging; make no unsupported claims.
- Score each category from 0 to 5 (integers or halves). Be calibrated: 5 means a \
genuine information advantage a desk would pay for; 3 is merely adequate.

Return ONLY valid JSON, no prose outside the JSON.
"""


def _build_user_prompt(artifacts: RunArtifacts, rubric: Rubric) -> str:
    cats = []
    for layer in rubric.layers:
        for c in layer.categories:
            cats.append(
                {"id": c.id, "layer": layer.id, "name": c.name, "description": c.description}
            )
    payload = {
        "rubric": {
            "persona": rubric.persona,
            "scale": rubric.scale.model_dump(),
            "categories": cats,
        },
        "run": {
            "topic": artifacts.topic,
            "parsed": artifacts.parsed,
            "news": artifacts.news,
            "report": artifacts.report,
            "report_md": artifacts.report_md[:12000],
            "intro_md": artifacts.intro_md[:4000],
            "evaluation_hints": {
                "note": "metric hints only — never a quality verdict",
                **{
                    k: artifacts.evaluation.get(k)
                    for k in ("plan", "deliver", "refresh", "timing")
                    if k in artifacts.evaluation
                },
            },
        },
        "output_format": {
            "scores": [{"category_id": "<id>", "score": 0, "rationale": "<why>"}],
            "strengths": ["<top strengths>"],
            "gaps": ["<top risks/gaps>"],
            "good_enough_for_pilot": "yes|no|conditional",
        },
    }
    return (
        "Evaluate this trading-intelligence run against the rubric. "
        "Produce a score for every category id.\n\n"
        + json.dumps(payload, ensure_ascii=False, default=str)
    )


class LLMEvaluator(Evaluator):
    name = "llm"

    def __init__(
        self,
        model: str | None = None,
        temperature: float = 0.0,
        client=None,
    ) -> None:
        self.model = model or os.getenv("EVAL_LLM_MODEL") or os.getenv("OPENAI_MODEL") or "gpt-4o"
        self.temperature = temperature
        self._client = client
        self._last_raw: dict | None = None

    def _get_client(self):
        if self._client is not None:
            return self._client
        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover - dependency present in repo
            raise RuntimeError(
                "openai package is required for the LLM evaluator"
            ) from exc
        self._client = OpenAI()
        return self._client

    def _complete(self, system: str, user: str) -> str:
        client = self._get_client()
        resp = client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return resp.choices[0].message.content or "{}"

    def score_categories(self, artifacts: RunArtifacts, rubric: Rubric) -> list[CategoryScore]:
        raw = self._complete(SYSTEM_PROMPT, _build_user_prompt(artifacts, rubric))
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"LLM did not return valid JSON: {raw[:200]}") from exc
        self._last_raw = data

        by_id = {}
        for item in data.get("scores", []):
            cid = item.get("category_id")
            if cid:
                by_id[cid] = item

        out: list[CategoryScore] = []
        for cat_id in rubric.category_ids:
            item = by_id.get(cat_id, {})
            score = item.get("score", 0)
            try:
                score = float(score)
            except (TypeError, ValueError):
                score = 0.0
            out.append(
                CategoryScore(
                    category_id=cat_id,
                    score=max(0.0, min(float(rubric.scale.max), score)),
                    rationale=str(item.get("rationale", "")),
                )
            )
        return out

    def summarize(self, artifacts, result):
        data = self._last_raw or {}
        strengths = [str(x) for x in data.get("strengths", [])][:5]
        gaps = [str(x) for x in data.get("gaps", [])][:5]
        verdict = data.get("good_enough_for_pilot")
        notes = f"good_enough_for_pilot: {verdict}" if verdict else ""
        if not strengths and not gaps:
            return super().summarize(artifacts, result)
        return strengths, gaps, notes
