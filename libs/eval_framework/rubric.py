"""Rubric definition and loader for the Trading Intelligence Evaluation Framework.

The rubric is data-driven (see ``rubric.json``): three weighted layers, each with
weighted 0-5 categories. Weights are configurable and normalized at runtime, so a
caller can override layer weights (e.g. Information Discovery 40% / Research 30% /
Trading 30%) or category weights without touching code.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field

DEFAULT_RUBRIC_PATH = Path(__file__).parent / "rubric.json"


class Scale(BaseModel):
    min: int = 0
    max: int = 5
    anchors: dict[str, str] = Field(default_factory=dict)


class Category(BaseModel):
    id: str
    name: str
    description: str = ""
    weight: float = 1.0


class Layer(BaseModel):
    id: str
    name: str
    description: str = ""
    weight: float = 1.0
    categories: list[Category]

    @property
    def category_ids(self) -> list[str]:
        return [c.id for c in self.categories]

    def normalized_category_weights(self) -> dict[str, float]:
        """Category weights within this layer, normalized to sum to 1.0."""
        total = sum(c.weight for c in self.categories)
        if total <= 0:
            n = len(self.categories)
            return {c.id: 1.0 / n for c in self.categories}
        return {c.id: c.weight / total for c in self.categories}


class Rubric(BaseModel):
    schema_version: str = "1.0.0"
    name: str
    title: str = ""
    description: str = ""
    persona: str = ""
    scale: Scale = Field(default_factory=Scale)
    relative_margin: float = 0.2
    layers: list[Layer]

    @property
    def layer_ids(self) -> list[str]:
        return [layer.id for layer in self.layers]

    @property
    def category_ids(self) -> list[str]:
        return [c.id for layer in self.layers for c in layer.categories]

    def layer(self, layer_id: str) -> Layer:
        for layer in self.layers:
            if layer.id == layer_id:
                return layer
        raise KeyError(f"Unknown layer: {layer_id}")

    def category(self, category_id: str) -> Category:
        for layer in self.layers:
            for c in layer.categories:
                if c.id == category_id:
                    return c
        raise KeyError(f"Unknown category: {category_id}")

    def layer_of(self, category_id: str) -> Layer:
        for layer in self.layers:
            if category_id in layer.category_ids:
                return layer
        raise KeyError(f"Category not in any layer: {category_id}")

    def normalized_layer_weights(self) -> dict[str, float]:
        """Layer weights normalized to sum to 1.0."""
        total = sum(layer.weight for layer in self.layers)
        if total <= 0:
            n = len(self.layers)
            return {layer.id: 1.0 / n for layer in self.layers}
        return {layer.id: layer.weight / total for layer in self.layers}

    def with_weights(
        self,
        layer_weights: dict[str, float] | None = None,
        category_weights: dict[str, float] | None = None,
    ) -> Rubric:
        """Return a copy of the rubric with overridden weights.

        ``layer_weights`` maps layer id -> weight; ``category_weights`` maps
        category id -> weight. Missing entries keep their current weight.
        """
        data = self.model_dump()
        lw = layer_weights or {}
        cw = category_weights or {}
        for layer in data["layers"]:
            if layer["id"] in lw:
                layer["weight"] = lw[layer["id"]]
            for cat in layer["categories"]:
                if cat["id"] in cw:
                    cat["weight"] = cw[cat["id"]]
        return Rubric.model_validate(data)


def load_rubric(path: str | Path | None = None) -> Rubric:
    """Load a rubric from JSON. Defaults to the bundled trading-intelligence rubric."""
    p = Path(path) if path else DEFAULT_RUBRIC_PATH
    data = json.loads(p.read_text(encoding="utf-8"))
    return Rubric.model_validate(data)


@lru_cache(maxsize=1)
def default_rubric() -> Rubric:
    return load_rubric()
