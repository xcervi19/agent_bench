"""Render evaluation verdicts to JSON + Markdown.

Outputs follow the #18 convention: a machine-readable ``quality_review.json``
and a short human-readable ``quality_review.md`` written next to the run.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from .relative import PairwiseComparison, WinRateStats
from .scoring import EvaluationResult


def _now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def absolute_to_dict(result: EvaluationResult) -> dict:
    data = result.model_dump()
    data["mode"] = "absolute"
    data["generated_at"] = _now()
    return data


def comparison_to_dict(comp: PairwiseComparison) -> dict:
    data = comp.model_dump(mode="json")
    data["mode"] = "relative"
    data["generated_at"] = _now()
    return data


def write_json(data: dict, path: str | Path) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return p


def render_absolute_md(result: EvaluationResult) -> str:
    m = result.scale_max
    lines: list[str] = []
    lines.append(f"# Quality Review — {result.label}")
    lines.append("")
    lines.append("- **Mode:** absolute")
    lines.append(f"- **Topic:** {result.topic or 'n/a'}")
    lines.append(f"- **Evaluator:** {result.evaluator}")
    lines.append(f"- **Rubric:** {result.rubric_name}")
    lines.append(
        f"- **Overall:** {result.overall_score:.2f}/{m} "
        f"({result.overall_score_100:.0f}/100)"
    )
    if result.notes:
        lines.append(f"- **Notes:** {result.notes}")
    lines.append("")

    lines.append("## Layer scores")
    lines.append("")
    lines.append("| Layer | Weight | Score |")
    lines.append("|---|---|---|")
    for layer in result.layers:
        lines.append(
            f"| {layer.name} | {layer.weight * 100:.0f}% | {layer.score:.2f}/{m} |"
        )
    lines.append("")

    lines.append("## Category scores")
    lines.append("")
    lines.append("| Layer | Category | Score | Rationale |")
    lines.append("|---|---|---|---|")
    for layer in result.layers:
        for c in layer.categories:
            rationale = c.rationale.replace("|", "\\|")
            lines.append(f"| {layer.name} | {c.name} | {c.score:.1f}/{m} | {rationale} |")
    lines.append("")

    if result.strengths:
        lines.append("## Top strengths")
        lines.append("")
        lines.extend(f"- {s}" for s in result.strengths)
        lines.append("")
    if result.gaps:
        lines.append("## Top gaps / risks")
        lines.append("")
        lines.extend(f"- {g}" for g in result.gaps)
        lines.append("")
    return "\n".join(lines)


def render_comparison_md(comp: PairwiseComparison) -> str:
    m = comp.scale_max
    arrow = {"better": "▲", "equal": "=", "worse": "▼"}
    lines: list[str] = []
    lines.append(f"# Relative Review — {comp.candidate_label} vs {comp.baseline_label}")
    lines.append("")
    lines.append(f"- **Mode:** relative (margin {comp.margin})")
    lines.append(f"- **Topic:** {comp.topic or 'n/a'}")
    lines.append(
        f"- **Overall verdict:** **{comp.verdict.value.upper()}** "
        f"({comp.overall_baseline:.2f} → {comp.overall_candidate:.2f}, "
        f"Δ{comp.overall_delta:+.2f} on /{m})"
    )
    lines.append("")

    lines.append("## Layer deltas")
    lines.append("")
    lines.append("| Layer | Baseline | Candidate | Δ | Verdict |")
    lines.append("|---|---|---|---|---|")
    for ld in comp.layer_deltas:
        lines.append(
            f"| {ld.name} | {ld.baseline:.2f} | {ld.candidate:.2f} | "
            f"{ld.delta:+.2f} | {arrow[ld.verdict.value]} {ld.verdict.value} |"
        )
    lines.append("")

    lines.append("## Category deltas")
    lines.append("")
    lines.append("| Category | Baseline | Candidate | Δ | Verdict |")
    lines.append("|---|---|---|---|---|")
    for cd in comp.category_deltas:
        lines.append(
            f"| {cd.name} | {cd.baseline:.2f} | {cd.candidate:.2f} | "
            f"{cd.delta:+.2f} | {arrow[cd.verdict.value]} {cd.verdict.value} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_winrate_md(stats: WinRateStats) -> str:
    lines: list[str] = []
    lines.append("# Win-rate aggregation")
    lines.append("")
    lines.append(f"- **Comparisons:** {stats.n}")
    lines.append(f"- **Better / Equal / Worse:** {stats.better} / {stats.equal} / {stats.worse}")
    lines.append(f"- **Win rate:** {stats.win_rate * 100:.1f}%")
    lines.append(f"- **Non-regression rate:** {stats.non_regression_rate * 100:.1f}%")
    lines.append(f"- **Mean overall Δ:** {stats.mean_overall_delta:+.3f}")
    lines.append("")
    if stats.per_layer_win_rate:
        lines.append("## Per-layer win rate")
        lines.append("")
        lines.append("| Layer | Win rate |")
        lines.append("|---|---|")
        for lid, wr in sorted(stats.per_layer_win_rate.items()):
            lines.append(f"| {lid} | {wr * 100:.1f}% |")
        lines.append("")
    return "\n".join(lines)
