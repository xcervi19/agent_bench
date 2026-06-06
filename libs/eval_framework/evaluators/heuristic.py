"""Deterministic, offline heuristic evaluator.

Maps measurable signals in the run artifacts to 0-5 scores for each rubric
category. It is intentionally transparent and reproducible (no network, no
randomness) so it can serve as:

  * a baseline / regression anchor in CI,
  * a fast pre-screen before spending tokens on the LLM judge,
  * the reference implementation of what each category *measures*.

The LLM evaluator (``llm.py``) produces richer judgments for the same rubric.
"""

from __future__ import annotations

import statistics
from collections.abc import Iterable

from ..artifacts import RunArtifacts, parse_dt
from ..rubric import Rubric
from ..scoring import CategoryScore
from .base import Evaluator

# ---- source-class taxonomy (matches news.json source_class values) ----

PRIMARY_CLASSES = {
    "primary_official",
    "regulatory",
    "government",
    "exchange",
    "port_authority",
    "grid_operator",
    "tso",
    "official_social",
    "corporate",
    "corporate_communication",
    "official",
}
DATA_FEED_CLASSES = {"data_feed", "dataset", "market_data"}
SPECIALIST_CLASSES = {
    "specialist_outlet",
    "industry_publication",
    "academic",
    "technical_report",
    "local_press",
    "regional_media",
    "regional_social",
}
GENERIC_CLASSES = {"aggregator", "news_aggregator", "blog", "secondary", "wire", "media"}

RELATIONSHIP_TERMS = [
    "depends on",
    "dependency",
    "supply chain",
    "ownership",
    "owned by",
    "subsidiary",
    "route",
    "routing",
    "bypass",
    "offset",
    "replace",
    "linked",
    "relationship",
    "upstream",
    "downstream",
    "exposure",
    "correlat",
    "feeds",
    "connected",
]
CAUSAL_TERMS = [
    "because",
    "due to",
    "leads to",
    "results in",
    "driven by",
    "caused",
    "trigger",
    "consequence",
    "therefore",
    "as a result",
    "spike",
    "would lift",
    "would raise",
    "if ",
    "risk premium",
    "knock-on",
]
IMPACT_TERMS = [
    "price",
    "volatility",
    "supply",
    "demand",
    "risk",
    "premium",
    "spike",
    "disrupt",
    "shock",
    "outage",
    "sanction",
    "embargo",
    "capacity",
    "drawdown",
    "shortage",
    "spread",
]


def _clamp(x: float, lo: float = 0.0, hi: float = 5.0) -> float:
    return max(lo, min(hi, x))


def _to5(fraction: float) -> float:
    """Map a 0..1 fraction onto the 0..5 scale."""
    return _clamp(5.0 * fraction)


def _distinct_term_hits(text: str, terms: Iterable[str]) -> list[str]:
    low = text.lower()
    return [t for t in terms if t in low]


def _r(x: float) -> float:
    return round(x, 3)


class HeuristicEvaluator(Evaluator):
    name = "heuristic"

    def score_categories(self, artifacts: RunArtifacts, rubric: Rubric) -> list[CategoryScore]:
        handlers = {
            "primary_source_discovery": self._primary_source_discovery,
            "information_latency": self._information_latency,
            "source_coverage": self._source_coverage,
            "non_obvious_source_discovery": self._non_obvious_source_discovery,
            "source_authority_assessment": self._source_authority_assessment,
            "entity_discovery": self._entity_discovery,
            "relationship_discovery": self._relationship_discovery,
            "causal_reasoning": self._causal_reasoning,
            "research_depth": self._research_depth,
            "signal_to_noise": self._signal_to_noise,
            "market_relevance": self._market_relevance,
            "actionability": self._actionability,
            "potential_market_impact": self._potential_market_impact,
            "information_edge": self._information_edge,
        }
        out: list[CategoryScore] = []
        for cat_id in rubric.category_ids:
            handler = handlers.get(cat_id)
            if handler is None:
                out.append(
                    CategoryScore(
                        category_id=cat_id,
                        score=2.5,
                        rationale="No heuristic defined; neutral score.",
                    )
                )
                continue
            score, rationale, evidence = handler(artifacts)
            out.append(
                CategoryScore(
                    category_id=cat_id,
                    score=round(_clamp(score), 3),
                    rationale=rationale,
                    evidence=evidence,
                )
            )
        return out

    # ---- helpers ----

    @staticmethod
    def _classes(artifacts: RunArtifacts) -> list[str]:
        return [str(s.get("source_class", "")).lower() for s in artifacts.sources]

    @staticmethod
    def _relevance(artifacts: RunArtifacts) -> list[float]:
        vals = []
        for s in artifacts.sources:
            v = s.get("relevance_score")
            if isinstance(v, (int, float)):
                vals.append(float(v))
        return vals

    # ---- Layer 1: Information Discovery ----

    def _primary_source_discovery(self, a: RunArtifacts):
        classes = self._classes(a)
        if not classes:
            return 0.0, "No sources found.", []
        primary = sum(c in PRIMARY_CLASSES or c in DATA_FEED_CLASSES for c in classes)
        frac = primary / len(classes)
        score = _to5(frac)
        if any(c in PRIMARY_CLASSES for c in classes) and any(
            c in DATA_FEED_CLASSES for c in classes
        ):
            score += 0.5
        return (
            score,
            f"{primary}/{len(classes)} sources are primary/official or data-feed "
            f"(fraction {_r(frac)}).",
            sorted({c for c in classes if c in PRIMARY_CLASSES or c in DATA_FEED_CLASSES}),
        )

    def _information_latency(self, a: RunArtifacts):
        run_dt = a.run_dt
        ages_h: list[float] = []
        for s in a.sources:
            pub = parse_dt(s.get("published_at"))
            if pub and run_dt:
                ages_h.append((run_dt - pub).total_seconds() / 3600.0)
        if not ages_h:
            return 2.5, "No published_at/run timestamp to assess latency; neutral.", []
        median_h = statistics.median(ages_h)
        # Fresh (<=24h) -> 5; degrade to 0 around 14 days (336h).
        score = _to5(1.0 - _clamp(median_h / 336.0, 0.0, 1.0))
        return (
            score,
            f"Median source age {_r(median_h)}h relative to run time "
            f"(fresher surfacing scores higher).",
            [f"median_age_hours={_r(median_h)}", f"n={len(ages_h)}"],
        )

    def _source_coverage(self, a: RunArtifacts):
        classes = [c for c in self._classes(a) if c]
        if not classes:
            return 0.0, "No classified sources.", []
        distinct_classes = set(classes)
        langs = {str(s.get("language", "")).lower() for s in a.sources if s.get("language")}
        class_comp = _to5(min(len(distinct_classes), 6) / 6.0)
        lang_comp = _to5(min(len(langs), 4) / 4.0)
        score = 0.7 * class_comp + 0.3 * lang_comp
        return (
            score,
            f"{len(distinct_classes)} distinct source classes, {len(langs)} languages.",
            sorted(distinct_classes) + sorted(langs),
        )

    def _non_obvious_source_discovery(self, a: RunArtifacts):
        classes = self._classes(a)
        if not classes:
            return 0.0, "No sources found.", []
        non_generic = sum(c not in GENERIC_CLASSES for c in classes)
        frac = non_generic / len(classes)
        score = _to5(frac)
        has_local = any(c in {"local_press", "regional_media", "regional_social"} for c in classes)
        has_non_en = any(
            str(s.get("language", "")).lower() not in ("", "en") for s in a.sources
        )
        if has_local:
            score += 0.3
        if has_non_en:
            score += 0.3
        ev = []
        if has_local:
            ev.append("local/regional sources present")
        if has_non_en:
            ev.append("non-English sources present")
        return (
            score,
            f"{non_generic}/{len(classes)} sources beyond generic aggregators "
            f"(fraction {_r(frac)}).",
            ev,
        )

    def _source_authority_assessment(self, a: RunArtifacts):
        sources = a.sources
        if not sources:
            return 0.0, "No sources to assess authority on.", []
        labelled = sum(
            bool(s.get("source_class")) and ("relevance_score" in s) for s in sources
        )
        label_cov = labelled / len(sources)
        classes = set(self._classes(a))
        has_producer = bool(classes & (PRIMARY_CLASSES | DATA_FEED_CLASSES | SPECIALIST_CLASSES))
        has_consumer = bool(classes & GENERIC_CLASSES)
        score = 4.0 * label_cov + (0.5 if (has_producer and has_consumer) else 0.0)
        return (
            score,
            f"{labelled}/{len(sources)} sources carry source_class + relevance; "
            f"producer/aggregator mix={'yes' if has_producer and has_consumer else 'no'}.",
            sorted(classes),
        )

    # ---- Layer 2: Research Quality ----

    def _entity_discovery(self, a: RunArtifacts):
        entities = a.entities
        n = len({str(e.get("name", "")).lower() for e in entities if e.get("name")})
        score = _to5(min(n, 6) / 6.0)
        return score, f"{n} distinct entities identified in the plan.", [
            str(e.get("name")) for e in entities[:8]
        ]

    def _relationship_discovery(self, a: RunArtifacts):
        hits = _distinct_term_hits(a.report_text, RELATIONSHIP_TERMS)
        multi = sum(len(f.get("source_ids", []) or []) >= 2 for f in a.key_findings)
        term_comp = _to5(min(len(hits), 6) / 6.0)
        cross_comp = _to5(min(multi, 3) / 3.0)
        score = 0.7 * term_comp + 0.3 * cross_comp
        return (
            score,
            f"{len(hits)} relationship cues; {multi} findings cross-link >=2 sources.",
            hits,
        )

    def _causal_reasoning(self, a: RunArtifacts):
        hits = _distinct_term_hits(a.report_text, CAUSAL_TERMS)
        term_comp = _to5(min(len(hits), 5) / 5.0)
        score = term_comp
        if len(a.scenarios) >= 2:
            score += 0.75
        elif len(a.scenarios) == 1:
            score += 0.35
        return (
            score,
            f"{len(hits)} causal cues; {len(a.scenarios)} forward scenarios.",
            hits,
        )

    def _research_depth(self, a: RunArtifacts):
        sources = a.sources
        findings = a.key_findings
        multi = sum(len(f.get("source_ids", []) or []) >= 2 for f in findings)
        sources_comp = _to5(min(len(sources), 8) / 8.0)
        crossval_comp = _to5(min(multi, 3) / 3.0)
        context_comp = _to5(min(len(a.rag_refs), 3) / 3.0)
        scenario_comp = _to5(min(len(a.scenarios), 3) / 3.0)
        score = statistics.mean([sources_comp, crossval_comp, context_comp, scenario_comp])
        return (
            score,
            f"{len(sources)} sources, {multi} cross-validated findings, "
            f"{len(a.rag_refs)} context refs, {len(a.scenarios)} scenarios.",
            [
                f"sources={len(sources)}",
                f"cross_validated={multi}",
                f"context_refs={len(a.rag_refs)}",
            ],
        )

    def _signal_to_noise(self, a: RunArtifacts):
        rel = self._relevance(a)
        if not rel:
            return 2.5, "No relevance scores; neutral.", []
        avg = statistics.mean(rel)
        score = _to5(avg)
        drops = a.news.get("drops") or {}
        if isinstance(drops, dict) and sum(v for v in drops.values() if isinstance(v, int)) > 0:
            score += 0.3
        return (
            score,
            f"Avg source relevance {_r(avg)}; "
            f"{'filtering evident' if drops else 'no drop stats'}.",
            [f"avg_relevance={_r(avg)}"],
        )

    # ---- Layer 3: Trading Intelligence ----

    def _market_relevance(self, a: RunArtifacts):
        rel = self._relevance(a)
        avg = statistics.mean(rel) if rel else 0.5
        score = _to5(avg)
        if a.parsed.get("working_thesis") or a.report.get("thesis_status"):
            score += 0.3
        return score, f"Avg source relevance {_r(avg)}; thesis present.", [
            f"avg_relevance={_r(avg)}"
        ]

    def _actionability(self, a: RunArtifacts):
        scenarios = a.scenarios
        findings = a.key_findings
        scen_prob = (
            sum(bool(s.get("probability")) for s in scenarios) / len(scenarios)
            if scenarios
            else 0.0
        )
        find_conf = (
            sum(bool(f.get("confidence")) for f in findings) / len(findings)
            if findings
            else 0.0
        )
        followups = bool(a.report.get("next_queries") or a.report.get("open_questions"))
        score = 0.4 * _to5(scen_prob) + 0.4 * _to5(find_conf) + (1.0 if followups else 0.0)
        return (
            score,
            f"{len(scenarios)} scenarios (prob coverage {_r(scen_prob)}), "
            f"{len(findings)} findings (confidence coverage {_r(find_conf)}).",
            ["has_followups" if followups else "no_followups"],
        )

    def _potential_market_impact(self, a: RunArtifacts):
        hits = _distinct_term_hits(a.report_text, IMPACT_TERMS)
        score = _to5(min(len(hits), 7) / 7.0)
        return score, f"{len(hits)} market-impact terms (price/supply/risk/...).", hits

    def _information_edge(self, a: RunArtifacts):
        classes = self._classes(a)
        if not classes:
            return 0.0, "No sources; no measurable edge.", []
        novelty = [
            float(s["novelty_score"])
            for s in a.sources
            if isinstance(s.get("novelty_score"), (int, float))
        ]
        novelty_comp = _to5(statistics.mean(novelty)) if novelty else 2.5
        non_generic = sum(c not in GENERIC_CLASSES for c in classes) / len(classes)
        nonobvious_comp = _to5(non_generic)
        non_en = sum(
            1 for s in a.sources if str(s.get("language", "")).lower() not in ("", "en")
        )
        multilang_comp = _to5(min(non_en, 2) / 2.0)
        score = statistics.mean([novelty_comp, nonobvious_comp, multilang_comp])
        return (
            score,
            f"Novelty {_r(novelty_comp)}, non-obvious {_r(nonobvious_comp)}, "
            f"multilingual {_r(multilang_comp)} (edge vs generic workflows).",
            [f"non_english_sources={non_en}"],
        )
