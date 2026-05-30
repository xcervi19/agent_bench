#!/usr/bin/env python3
"""Evaluate Newsfind run artifacts for business-demo quality.

The evaluator is intentionally deterministic and offline. It does not try to
replace an expert reviewer; it turns the artifacts that the system already
produces into a repeatable scorecard that a trading/NLP reviewer can inspect.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any


JsonObject = dict[str, Any]

SOURCE_CLASSES_HIGH_TRUST = {"primary_official", "specialist_outlet", "data_feed"}
REPORT_SECTIONS = (
    "snapshot",
    "evidence highlights",
    "how news reshapes the working thesis",
    "risks & blind spots",
)
MARKET_IMPACT_TERMS = {
    "price",
    "spread",
    "basis",
    "volatility",
    "supply",
    "demand",
    "capacity",
    "flows",
    "inventory",
    "storage",
    "production",
    "outage",
    "disruption",
    "risk",
    "hedge",
    "short-term",
    "near-term",
    "scenario",
    "probability",
    "bullish",
    "bearish",
    "upside",
    "downside",
}


@dataclass(frozen=True)
class ScoreItem:
    name: str
    score: int
    max_score: int
    checks: list[str]
    warnings: list[str]

    @property
    def pct(self) -> float:
        return round(self.score / self.max_score * 100, 1) if self.max_score else 0.0

    def as_dict(self) -> JsonObject:
        return {
            "name": self.name,
            "score": self.score,
            "max_score": self.max_score,
            "pct": self.pct,
            "checks": self.checks,
            "warnings": self.warnings,
        }


def _read_json(path: Path | None) -> JsonObject:
    if not path:
        return {}
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _read_text(path: Path | None) -> str:
    if not path:
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _as_dict(value: Any) -> JsonObject:
    return value if isinstance(value, dict) else {}


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _slugish(path: Path) -> str:
    return path.name.lower().replace("_", "-")


def _first_existing(root: Path, names: set[str], must_contain: str | None = None) -> Path | None:
    candidates = [p for p in root.rglob("*") if p.is_file() and p.name in names]
    if must_contain:
        candidates = [p for p in candidates if must_contain in _slugish(p.parent)]
    if not candidates:
        return None
    return max(candidates, key=lambda p: (len(p.parts), p.stat().st_mtime))


def discover_artifacts(run_dir: Path) -> dict[str, Path | None]:
    """Find artifacts from both flat test_topic runs and nested full-pipeline runs."""

    return {
        "parsed_json": _first_existing(run_dir, {"parsed.json"}),
        "intro_md": _first_existing(run_dir, {"intro.md"}, "plan")
        or _first_existing(run_dir, {"intro.md"}),
        "news_json": _first_existing(run_dir, {"news.json"}, "deliver")
        or _first_existing(run_dir, {"news.json"}),
        "report_json": _first_existing(run_dir, {"report.json"}, "deliver")
        or _first_existing(run_dir, {"report.json"}),
        "report_md": _first_existing(run_dir, {"report.md"}, "deliver")
        or _first_existing(run_dir, {"report.md"}),
        "events_ndjson": _first_existing(run_dir, {"events.ndjson"}),
        "topic_json": _first_existing(run_dir, {"topic.json"}),
    }


def _actor_names(parsed: JsonObject) -> list[str]:
    entities = _as_dict(parsed.get("entities"))
    actors = _as_list(entities.get("actors"))
    names: list[str] = []
    for actor in actors:
        if isinstance(actor, str):
            names.append(actor)
        elif isinstance(actor, Mapping):
            name = actor.get("name") or actor.get("actor")
            if isinstance(name, str):
                names.append(name)
    return [n.strip() for n in names if n and n.strip()]


def _query_texts(parsed: JsonObject) -> list[str]:
    texts: list[str] = []
    for query in _as_list(parsed.get("queries")):
        if isinstance(query, Mapping):
            text = query.get("query")
            if isinstance(text, str):
                texts.append(text)
    return texts


def _source_ids(news: JsonObject) -> set[str]:
    ids: set[str] = set()
    for source in _as_list(news.get("sources")):
        if isinstance(source, Mapping) and isinstance(source.get("id"), str):
            ids.add(source["id"])
    return ids


def _citation_ids(text: str) -> list[str]:
    ids: list[str] = []
    for bracket in re.findall(r"\[([^\]]+)\]", text):
        for part in re.split(r"[,;\s]+", bracket):
            token = part.strip()
            if re.fullmatch(r"s\d{2,}", token):
                ids.append(token)
    return ids


def _markdown_sections(text: str) -> set[str]:
    sections: set[str] = set()
    for line in text.splitlines():
        match = re.match(r"^#{1,3}\s+(.+)$", line.strip())
        if match:
            sections.add(match.group(1).strip().lower())
    return sections


def _summary_words(report: JsonObject, report_md: str) -> int:
    summary = report.get("summary_md")
    if isinstance(summary, str) and summary.strip():
        return len(summary.split())
    first_para = report_md.split("\n\n", 1)[0] if report_md else ""
    return len(first_para.split())


def _event_cost(events_text: str) -> float:
    total = 0.0
    for line in events_text.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        payload = _as_dict(event.get("payload"))
        if event.get("event_type") == "stage.finished":
            total += _safe_float(payload.get("total_cost_usd"))
    return round(total, 4)


def _add(checks: list[str], warnings: list[str], condition: bool, points: int, ok: str, warn: str) -> int:
    if condition:
        checks.append(ok)
        return points
    warnings.append(warn)
    return 0


def score_plan(parsed: JsonObject) -> ScoreItem:
    checks: list[str] = []
    warnings: list[str] = []
    score = 0
    queries = _as_list(parsed.get("queries"))
    query_texts = _query_texts(parsed)
    actors = _actor_names(parsed)
    languages = {
        q.get("language")
        for q in queries
        if isinstance(q, Mapping) and isinstance(q.get("language"), str)
    }
    source_classes = {
        q.get("source_class")
        for q in queries
        if isinstance(q, Mapping) and isinstance(q.get("source_class"), str)
    }
    scenarios = _as_list(parsed.get("scenarios"))
    monitoring_plan = _as_dict(parsed.get("monitoring_plan"))
    trigger_terms = _as_list(monitoring_plan.get("trigger_terms"))

    score += _add(
        checks,
        warnings,
        10 <= len(queries) <= 15,
        4,
        f"Query count is in target range ({len(queries)}).",
        f"Query count should be 10-15 for the demo; found {len(queries)}.",
    )
    score += _add(
        checks,
        warnings,
        bool(actors),
        3,
        f"Plan identifies {len(actors)} actor(s).",
        "Plan does not identify concrete actors.",
    )
    covered_actors = sum(
        1 for actor in actors if any(actor.lower() in query.lower() for query in query_texts)
    )
    score += _add(
        checks,
        warnings,
        not actors or covered_actors / len(actors) >= 0.5,
        4,
        f"Queries mention {covered_actors}/{len(actors)} actor(s).",
        f"Queries mention only {covered_actors}/{len(actors)} actor(s).",
    )
    score += _add(
        checks,
        warnings,
        len(languages) >= 2 or len(queries) < 10,
        3,
        f"Plan covers {len(languages)} language(s): {', '.join(sorted(languages))}.",
        "Plan is single-language; add local-language searches for non-US/non-UK topics.",
    )
    score += _add(
        checks,
        warnings,
        len(source_classes) >= 3,
        3,
        f"Plan spans {len(source_classes)} source classes.",
        "Plan should mix primary, specialist, aggregator, and data-feed sources.",
    )
    score += _add(
        checks,
        warnings,
        len(scenarios) >= 2,
        3,
        f"Plan has {len(scenarios)} scenario(s).",
        "Plan should frame at least two business scenarios.",
    )
    score += _add(
        checks,
        warnings,
        len(trigger_terms) >= 3,
        3,
        f"Monitoring plan has {len(trigger_terms)} trigger term(s).",
        "Monitoring plan needs concrete trigger terms.",
    )

    return ScoreItem("plan_quality", min(score, 20), 20, checks, warnings)


def score_sources(news: JsonObject) -> ScoreItem:
    checks: list[str] = []
    warnings: list[str] = []
    score = 0
    sources = [s for s in _as_list(news.get("sources")) if isinstance(s, Mapping)]
    executed = [q for q in _as_list(news.get("executed_queries")) if isinstance(q, Mapping)]
    relevance = [_safe_float(s.get("relevance_score")) for s in sources if s.get("relevance_score") is not None]
    high_trust = [
        s for s in sources if isinstance(s.get("source_class"), str) and s["source_class"] in SOURCE_CLASSES_HIGH_TRUST
    ]
    dated = [s for s in sources if s.get("published_at")]
    with_hits = [q for q in executed if _safe_float(q.get("results_count")) > 0]
    drops = _as_dict(news.get("drops"))
    dedup_drops = int(_safe_float(drops.get("deduped")) + _safe_float(drops.get("intra_batch_dup")))

    score += _add(
        checks,
        warnings,
        len(sources) >= 12,
        5,
        f"Collected {len(sources)} sources.",
        f"Collected only {len(sources)} sources; demo reports need breadth.",
    )
    median_relevance = statistics.median(relevance) if relevance else 0.0
    score += _add(
        checks,
        warnings,
        median_relevance >= 0.6,
        4,
        f"Median source relevance is {median_relevance:.2f}.",
        f"Median source relevance is low ({median_relevance:.2f}).",
    )
    high_trust_share = len(high_trust) / len(sources) if sources else 0.0
    score += _add(
        checks,
        warnings,
        high_trust_share >= 0.45,
        4,
        f"High-trust source share is {high_trust_share:.0%}.",
        f"High-trust source share is only {high_trust_share:.0%}; add primary/specialist sources.",
    )
    dated_share = len(dated) / len(sources) if sources else 0.0
    score += _add(
        checks,
        warnings,
        dated_share >= 0.6,
        3,
        f"Dated source share is {dated_share:.0%}.",
        f"Dated source share is only {dated_share:.0%}; freshness is hard to defend.",
    )
    hit_rate = len(with_hits) / len(executed) if executed else 0.0
    score += _add(
        checks,
        warnings,
        hit_rate >= 0.7,
        3,
        f"Executed-query hit rate is {hit_rate:.0%}.",
        f"Executed-query hit rate is {hit_rate:.0%}; plan may be too broad or poorly phrased.",
    )
    score += _add(
        checks,
        warnings,
        dedup_drops > 0 or len(sources) < 2,
        1,
        "Deduplication/filtering evidence is present.",
        "No duplicate drops recorded; verify filtering actually ran.",
    )

    return ScoreItem("evidence_quality", min(score, 20), 20, checks, warnings)


def score_citations(news: JsonObject, report: JsonObject, report_md: str) -> ScoreItem:
    checks: list[str] = []
    warnings: list[str] = []
    score = 0
    valid_source_ids = _source_ids(news)
    cited = _citation_ids(report_md)
    invalid_citations = sorted(set(cited) - valid_source_ids)
    key_findings = [f for f in _as_list(report.get("key_findings")) if isinstance(f, Mapping)]
    findings_with_sources = [
        f for f in key_findings if set(str(s) for s in _as_list(f.get("source_ids"))) <= valid_source_ids and f.get("source_ids")
    ]
    scenario_updates = [
        s
        for s in _as_list(report.get("scenario_updates") or report.get("scenarios"))
        if isinstance(s, Mapping)
    ]
    scenarios_with_evidence = [
        s for s in scenario_updates if _as_list(s.get("evidence_ids") or s.get("source_ids"))
    ]
    citation_density = len(cited) / max(len(report_md.split()), 1) * 100

    score += _add(
        checks,
        warnings,
        len(cited) >= 8,
        5,
        f"Report contains {len(cited)} inline source citation(s).",
        f"Report contains only {len(cited)} inline source citation(s).",
    )
    score += _add(
        checks,
        warnings,
        not invalid_citations and bool(cited),
        5,
        "All markdown citations point to known source IDs.",
        f"Invalid markdown citation IDs: {', '.join(invalid_citations) or 'none found'}.",
    )
    finding_source_rate = len(findings_with_sources) / len(key_findings) if key_findings else 0.0
    score += _add(
        checks,
        warnings,
        finding_source_rate >= 0.9,
        4,
        f"Key-finding source coverage is {finding_source_rate:.0%}.",
        f"Key-finding source coverage is {finding_source_rate:.0%}.",
    )
    scenario_evidence_rate = len(scenarios_with_evidence) / len(scenario_updates) if scenario_updates else 0.0
    score += _add(
        checks,
        warnings,
        not scenario_updates or scenario_evidence_rate >= 0.75,
        3,
        f"Scenario evidence coverage is {scenario_evidence_rate:.0%}.",
        f"Scenario evidence coverage is {scenario_evidence_rate:.0%}.",
    )
    score += _add(
        checks,
        warnings,
        citation_density >= 1.0,
        3,
        f"Citation density is {citation_density:.1f} citations per 100 words.",
        f"Citation density is {citation_density:.1f} per 100 words; factual density may be unsupported.",
    )

    return ScoreItem("citation_integrity", min(score, 20), 20, checks, warnings)


def score_trading_usefulness(parsed: JsonObject, report: JsonObject, report_md: str) -> ScoreItem:
    checks: list[str] = []
    warnings: list[str] = []
    score = 0
    text = " ".join(
        str(value)
        for value in (
            parsed.get("working_thesis"),
            report.get("summary_md"),
            report.get("thesis_update_md"),
            report_md,
        )
        if value
    ).lower()
    terms_present = sorted(term for term in MARKET_IMPACT_TERMS if term in text)
    key_findings = [f for f in _as_list(report.get("key_findings")) if isinstance(f, Mapping)]
    scenario_updates = [
        s
        for s in _as_list(report.get("scenario_updates") or report.get("scenarios"))
        if isinstance(s, Mapping)
    ]
    next_queries = _as_list(report.get("next_queries"))
    open_questions = _as_list(report.get("open_questions"))
    thesis_status = report.get("thesis_status")
    confidence_labels = [
        str(f.get("confidence")).lower()
        for f in key_findings
        if isinstance(f.get("confidence"), str)
    ]

    score += _add(
        checks,
        warnings,
        len(terms_present) >= 8,
        5,
        f"Report uses market-impact vocabulary ({len(terms_present)} terms).",
        "Report lacks concrete market-impact vocabulary.",
    )
    score += _add(
        checks,
        warnings,
        len(key_findings) >= 4,
        4,
        f"Report has {len(key_findings)} key finding(s).",
        "Report should include at least four key findings.",
    )
    score += _add(
        checks,
        warnings,
        len(scenario_updates) >= 2,
        4,
        f"Report updates {len(scenario_updates)} scenario(s).",
        "Report should update business scenarios with evidence.",
    )
    score += _add(
        checks,
        warnings,
        thesis_status in {"supported", "weakened", "invalidated", "inconclusive"},
        3,
        f"Thesis status is explicit: {thesis_status}.",
        "Report lacks a valid thesis_status.",
    )
    score += _add(
        checks,
        warnings,
        len(next_queries) >= 3,
        2,
        f"Report proposes {len(next_queries)} next query/query set(s).",
        "Report should propose at least three next-cycle queries.",
    )
    score += _add(
        checks,
        warnings,
        bool(open_questions),
        1,
        "Report states open questions.",
        "Report should expose remaining blind spots/open questions.",
    )
    score += _add(
        checks,
        warnings,
        bool(confidence_labels) and set(confidence_labels) <= {"high", "medium", "low"},
        1,
        "Key findings use normalized confidence labels.",
        "Key findings should use high/medium/low confidence labels.",
    )

    return ScoreItem("trading_usefulness", min(score, 20), 20, checks, warnings)


def score_structure(report: JsonObject, report_md: str, intro_md: str) -> ScoreItem:
    checks: list[str] = []
    warnings: list[str] = []
    score = 0
    sections = _markdown_sections(report_md)
    missing_sections = [section for section in REPORT_SECTIONS if section not in sections]
    summary_word_count = _summary_words(report, report_md)

    score += _add(
        checks,
        warnings,
        not missing_sections,
        5,
        "Report markdown includes the expected demo sections.",
        f"Report markdown is missing sections: {', '.join(missing_sections)}.",
    )
    score += _add(
        checks,
        warnings,
        20 <= summary_word_count <= 300,
        4,
        f"Executive summary length is {summary_word_count} words.",
        f"Executive summary should be 20-300 words; found {summary_word_count}.",
    )
    score += _add(
        checks,
        warnings,
        bool(report.get("summary_md")) and bool(report.get("report_md") or report_md),
        4,
        "Structured report has summary and report body.",
        "Structured report is missing summary_md or report_md/report.md.",
    )
    score += _add(
        checks,
        warnings,
        bool(intro_md.strip()),
        2,
        "Intro markdown is available for the human gate.",
        "Intro markdown is missing; the demo gate cannot be reviewed.",
    )
    score += _add(
        checks,
        warnings,
        "<newscard" in report_md.lower() or len(_citation_ids(report_md)) >= 8,
        2,
        "Report has source affordances for UI review.",
        "Report should expose source references clearly for UI review.",
    )
    score += _add(
        checks,
        warnings,
        len(report_md.split()) >= 250,
        3,
        "Report is substantial enough for expert review.",
        "Report is too short for a serious trading/NLP demo.",
    )

    return ScoreItem("artifact_structure", min(score, 20), 20, checks, warnings)


def demo_verdict(total_score: int, critical_warnings: Sequence[str]) -> str:
    if critical_warnings:
        return "not_demo_ready"
    if total_score >= 80:
        return "demo_ready"
    if total_score >= 65:
        return "expert_review_required"
    return "not_demo_ready"


def grade(total_score: int) -> str:
    if total_score >= 90:
        return "A"
    if total_score >= 80:
        return "B"
    if total_score >= 70:
        return "C"
    if total_score >= 60:
        return "D"
    return "F"


def evaluate(run_dir: Path) -> JsonObject:
    artifacts = discover_artifacts(run_dir)
    parsed = _read_json(artifacts["parsed_json"])
    news = _read_json(artifacts["news_json"])
    report = _read_json(artifacts["report_json"])
    report_md = _read_text(artifacts["report_md"]) or str(report.get("report_md") or "")
    intro_md = _read_text(artifacts["intro_md"])
    events_text = _read_text(artifacts["events_ndjson"])

    critical_warnings: list[str] = []
    if not parsed:
        critical_warnings.append("Missing or invalid parsed.json.")
    if not news:
        critical_warnings.append("Missing or invalid news.json.")
    if not report and not report_md:
        critical_warnings.append("Missing report.json/report.md.")

    score_items = [
        score_plan(parsed),
        score_sources(news),
        score_citations(news, report, report_md),
        score_trading_usefulness(parsed, report, report_md),
        score_structure(report, report_md, intro_md),
    ]
    total_score = sum(item.score for item in score_items)
    warnings = critical_warnings + [warning for item in score_items for warning in item.warnings]

    return {
        "schema_version": "0.1.0",
        "run_dir": str(run_dir.resolve()),
        "artifact_paths": {
            name: str(path.resolve()) if path else None for name, path in artifacts.items()
        },
        "score": total_score,
        "max_score": 100,
        "grade": grade(total_score),
        "verdict": demo_verdict(total_score, critical_warnings),
        "total_cost_usd": _event_cost(events_text),
        "scorecard": [item.as_dict() for item in score_items],
        "critical_warnings": critical_warnings,
        "warnings": warnings,
        "review_questions": [
            "Does the report identify the concrete market mechanism, not just the news event?",
            "Would a trader know what to monitor next after reading the report?",
            "Are high-impact claims backed by primary/specialist sources?",
            "Are the remaining blind spots explicit enough for an expert reviewer to trust the system?",
        ],
    }


def compare(evaluation: JsonObject, baseline: JsonObject | None) -> JsonObject | None:
    if baseline is None:
        return None
    by_name = {item["name"]: item for item in evaluation.get("scorecard", [])}
    base_by_name = {item["name"]: item for item in baseline.get("scorecard", [])}
    categories = []
    for name, item in by_name.items():
        base_item = base_by_name.get(name, {})
        categories.append(
            {
                "name": name,
                "score_delta": item.get("score", 0) - base_item.get("score", 0),
                "pct_delta": round(item.get("pct", 0.0) - base_item.get("pct", 0.0), 1),
            }
        )
    return {
        "baseline_run_dir": baseline.get("run_dir"),
        "score_delta": evaluation.get("score", 0) - baseline.get("score", 0),
        "grade_delta": f"{baseline.get('grade')} -> {evaluation.get('grade')}",
        "verdict_delta": f"{baseline.get('verdict')} -> {evaluation.get('verdict')}",
        "categories": categories,
    }


def render_markdown(evaluation: JsonObject) -> str:
    lines = [
        "# Newsfind Business Evaluation",
        "",
        f"- Run: `{evaluation['run_dir']}`",
        f"- Score: **{evaluation['score']}/{evaluation['max_score']}** ({evaluation['grade']})",
        f"- Verdict: **{evaluation['verdict']}**",
        f"- Observed cost: `${evaluation['total_cost_usd']}`",
        "",
        "## Scorecard",
        "",
        "| Area | Score | Notes |",
        "|---|---:|---|",
    ]
    for item in evaluation["scorecard"]:
        notes = "; ".join(item["checks"][:2])
        if item["warnings"]:
            notes += (" " if notes else "") + "Warnings: " + "; ".join(item["warnings"][:2])
        lines.append(f"| {item['name']} | {item['score']}/{item['max_score']} | {notes} |")

    if evaluation["critical_warnings"]:
        lines.extend(["", "## Critical warnings", ""])
        lines.extend(f"- {warning}" for warning in evaluation["critical_warnings"])

    if evaluation["warnings"]:
        lines.extend(["", "## All warnings", ""])
        lines.extend(f"- {warning}" for warning in evaluation["warnings"])

    lines.extend(["", "## Expert review questions", ""])
    lines.extend(f"- {question}" for question in evaluation["review_questions"])

    comparison = evaluation.get("comparison")
    if comparison:
        lines.extend(
            [
                "",
                "## Baseline comparison",
                "",
                f"- Baseline: `{comparison['baseline_run_dir']}`",
                f"- Score delta: **{comparison['score_delta']:+}**",
                f"- Grade: {comparison['grade_delta']}",
                f"- Verdict: {comparison['verdict_delta']}",
                "",
                "| Area | Score delta | Percent delta |",
                "|---|---:|---:|",
            ]
        )
        for item in comparison["categories"]:
            lines.append(f"| {item['name']} | {item['score_delta']:+} | {item['pct_delta']:+.1f}% |")

    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Score a completed Newsfind run for trading/NLP demo quality."
    )
    parser.add_argument("run_dir", type=Path, help="Run directory under testing/runs/ or state/news/...")
    parser.add_argument(
        "--baseline-run",
        type=Path,
        help="Optional previous run directory to compare against.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Where to write evaluation.json/evaluation.md. Defaults to <run_dir>/evaluation.",
    )
    parser.add_argument(
        "--fail-under",
        type=int,
        default=0,
        help="Exit non-zero when score is below this threshold.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_dir = args.run_dir.resolve()
    if not run_dir.exists():
        raise SystemExit(f"Run directory not found: {run_dir}")

    evaluation = evaluate(run_dir)
    if args.baseline_run:
        evaluation["comparison"] = compare(evaluation, evaluate(args.baseline_run.resolve()))

    output_dir = (args.output_dir or run_dir / "evaluation").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "evaluation.json").write_text(
        json.dumps(evaluation, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "evaluation.md").write_text(render_markdown(evaluation), encoding="utf-8")

    print(json.dumps({"score": evaluation["score"], "grade": evaluation["grade"], "verdict": evaluation["verdict"], "output_dir": str(output_dir)}, indent=2))
    if args.fail_under and int(evaluation["score"]) < args.fail_under:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
