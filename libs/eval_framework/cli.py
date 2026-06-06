"""Command-line interface for the Trading Intelligence Evaluation Framework.

Examples::

    # Mode 1 — absolute: score one run, write quality_review.{json,md}
    python -m eval_framework absolute --run-dir testing/results/test1/latest

    # Mode 2 — relative: baseline vs candidate
    python -m eval_framework relative \\
        --baseline testing/results/test1/2026-05-26.../  \\
        --candidate testing/results/test1/latest

    # Aggregate many comparison.json files into win-rate stats
    python -m eval_framework aggregate runs/*/comparison.json

    # Use the LLM judge instead of the offline heuristic
    python -m eval_framework absolute --run-dir <dir> --evaluator llm
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import compare_runs, evaluate_run
from .relative import PairwiseComparison, aggregate_win_rate
from .report import (
    absolute_to_dict,
    comparison_to_dict,
    render_absolute_md,
    render_comparison_md,
    render_winrate_md,
    write_json,
)
from .rubric import load_rubric


def _parse_weight_overrides(items: list[str] | None) -> dict[str, float]:
    out: dict[str, float] = {}
    for item in items or []:
        if "=" not in item:
            raise SystemExit(f"--weight expects id=value, got '{item}'")
        key, val = item.split("=", 1)
        out[key.strip()] = float(val)
    return out


def _add_common(p: argparse.ArgumentParser) -> None:
    p.add_argument("--evaluator", default="heuristic", help="heuristic (default) | llm")
    p.add_argument("--rubric", default=None, help="Path to a rubric JSON (defaults to bundled).")
    p.add_argument(
        "--layer-weight",
        action="append",
        metavar="LAYER_ID=W",
        help="Override a layer weight (repeatable), e.g. information_discovery=0.5",
    )
    p.add_argument(
        "--category-weight",
        action="append",
        metavar="CAT_ID=W",
        help="Override a category weight (repeatable).",
    )
    p.add_argument("--model", default=None, help="LLM model name (llm evaluator only).")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="eval_framework", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_abs = sub.add_parser("absolute", help="Score one run (Mode 1).")
    p_abs.add_argument("--run-dir", required=True)
    p_abs.add_argument("--label", default=None)
    p_abs.add_argument("--out", default=None, help="Output dir (default: <run-dir>/business_output)")
    _add_common(p_abs)

    p_rel = sub.add_parser("relative", help="Compare baseline vs candidate (Mode 2).")
    p_rel.add_argument("--baseline", required=True)
    p_rel.add_argument("--candidate", required=True)
    p_rel.add_argument("--margin", type=float, default=None)
    p_rel.add_argument("--out", default=None, help="Output dir (default: <candidate>/business_output)")
    _add_common(p_rel)

    p_agg = sub.add_parser("aggregate", help="Aggregate comparison.json files into win-rate stats.")
    p_agg.add_argument("comparisons", nargs="+", help="Paths to comparison JSON files.")
    p_agg.add_argument("--out", default=None, help="Where to write winrate.json/.md")

    p_rubric = sub.add_parser("show-rubric", help="Print the active rubric (layers, weights).")
    p_rubric.add_argument("--rubric", default=None)
    return parser


def _default_out(primary: str) -> Path:
    base = Path(primary)
    bo = base / "business_output"
    return bo if bo.is_dir() else base


def _evaluator_kwargs(args) -> dict:
    kwargs: dict = {}
    if getattr(args, "model", None):
        kwargs["model"] = args.model
    return kwargs


def cmd_absolute(args) -> int:
    rubric = load_rubric(args.rubric) if args.rubric else None
    result = evaluate_run(
        args.run_dir,
        label=args.label,
        evaluator=args.evaluator,
        rubric=rubric,
        layer_weights=_parse_weight_overrides(args.layer_weight),
        category_weights=_parse_weight_overrides(args.category_weight),
        **_evaluator_kwargs(args),
    )
    out_dir = Path(args.out) if args.out else _default_out(args.run_dir)
    write_json(absolute_to_dict(result), out_dir / "quality_review.json")
    md_path = out_dir / "quality_review.md"
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(render_absolute_md(result) + "\n", encoding="utf-8")

    print(
        f"[absolute] {result.label}: overall {result.overall_score:.2f}/{result.scale_max} "
        f"({result.overall_score_100:.0f}/100)"
    )
    for layer in result.layers:
        print(f"  {layer.name:<24} {layer.score:.2f}/{result.scale_max} (w {layer.weight:.2f})")
    print(f"  → {out_dir / 'quality_review.json'}")
    print(f"  → {md_path}")
    return 0


def cmd_relative(args) -> int:
    rubric = load_rubric(args.rubric) if args.rubric else None
    comp = compare_runs(
        args.baseline,
        args.candidate,
        evaluator=args.evaluator,
        rubric=rubric,
        margin=args.margin,
        layer_weights=_parse_weight_overrides(args.layer_weight),
        category_weights=_parse_weight_overrides(args.category_weight),
        **_evaluator_kwargs(args),
    )
    out_dir = Path(args.out) if args.out else _default_out(args.candidate)
    write_json(comparison_to_dict(comp), out_dir / "quality_review.json")
    md_path = out_dir / "quality_review.md"
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(render_comparison_md(comp) + "\n", encoding="utf-8")

    print(
        f"[relative] candidate is {comp.verdict.value.upper()} "
        f"({comp.overall_baseline:.2f} → {comp.overall_candidate:.2f}, "
        f"Δ{comp.overall_delta:+.2f})"
    )
    for ld in comp.layer_deltas:
        print(f"  {ld.name:<24} {ld.delta:+.2f}  {ld.verdict.value}")
    print(f"  → {out_dir / 'quality_review.json'}")
    return 0


def cmd_aggregate(args) -> int:
    comps: list[PairwiseComparison] = []
    for path in args.comparisons:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        comps.append(PairwiseComparison.model_validate(data))
    stats = aggregate_win_rate(comps)
    print(render_winrate_md(stats))
    if args.out:
        out_dir = Path(args.out)
        write_json(stats.model_dump(), out_dir / "winrate.json")
        (out_dir / "winrate.md").write_text(render_winrate_md(stats) + "\n", encoding="utf-8")
        print(f"  → {out_dir / 'winrate.json'}")
    return 0


def cmd_show_rubric(args) -> int:
    rubric = load_rubric(args.rubric) if args.rubric else load_rubric()
    lw = rubric.normalized_layer_weights()
    print(f"Rubric: {rubric.name} (scale 0-{rubric.scale.max})")
    for layer in rubric.layers:
        print(f"\n[{layer.name}]  weight {lw[layer.id] * 100:.0f}%")
        for c in layer.categories:
            print(f"  - {c.id}: {c.name}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    dispatch = {
        "absolute": cmd_absolute,
        "relative": cmd_relative,
        "aggregate": cmd_aggregate,
        "show-rubric": cmd_show_rubric,
    }
    return dispatch[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
