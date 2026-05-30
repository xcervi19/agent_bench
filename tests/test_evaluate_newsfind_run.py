from __future__ import annotations

import importlib.util
import json
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "evaluate_newsfind_run.py"
SPEC = importlib.util.spec_from_file_location("evaluate_newsfind_run", SCRIPT_PATH)
assert SPEC and SPEC.loader
evaluator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(evaluator)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def make_sources(count: int = 12) -> list[dict]:
    classes = ["primary_official", "specialist_outlet", "data_feed", "aggregator"]
    return [
        {
            "id": f"s{i:02d}",
            "url": f"https://example.com/{i}",
            "url_hash": f"hash{i:02d}",
            "title": f"Source {i}",
            "publisher": "Example",
            "published_at": "2026-05-30T00:00:00Z",
            "language": "en",
            "snippet": "Market supply risk and price impact.",
            "query_ids": ["q01"],
            "source_class": classes[i % len(classes)],
            "relevance_score": 0.72,
            "novelty_score": 0.7,
        }
        for i in range(1, count + 1)
    ]


def test_evaluate_scores_demo_ready_run(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    parsed = {
        "queries": [
            {
                "id": f"q{i:02d}",
                "query": f"Hormuz Iran Saudi shipping supply price scenario {i}",
                "language": "en" if i < 8 else "ar",
                "source_class": ["primary_official", "specialist_outlet", "data_feed", "aggregator"][i % 4],
            }
            for i in range(1, 13)
        ],
        "entities": {"actors": [{"name": "Iran"}, {"name": "Saudi"}]},
        "scenarios": [{"id": "base"}, {"id": "shock"}],
        "working_thesis": "Supply disruption may lift price spreads and volatility.",
        "monitoring_plan": {"trigger_terms": ["closure", "shipping", "ceasefire"]},
    }
    news = {
        "executed_queries": [{"id": f"q{i:02d}", "results_count": 3} for i in range(1, 13)],
        "sources": make_sources(),
        "drops": {"deduped": 2, "low_relevance": 1},
    }
    report_md = """
## Snapshot
Supply disruption risk is changing price volatility and flows [s01, s02].

## Evidence highlights
- Inventory, capacity, and shipping flows are the main market mechanism [s03].
- Production outage risk creates upside and downside scenarios for spreads [s04, s05].
- Demand and supply balance remains sensitive to near-term disruption [s06, s07].
- Hedge desks should watch volatility, basis, storage, and probability shifts [s08, s09].

## How news reshapes the working thesis
The thesis is supported because the evidence links disruption, capacity, and price risk [s10].

## Risks & blind spots
- Official confirmation may lag market pricing [s11].
- Source coverage may miss local-language announcements [s12].
""".strip()
    report = {
        "summary_md": "Supply disruption risk is becoming more actionable for traders because sources connect shipping, flows, inventory, capacity, and price volatility.",
        "report_md": report_md,
        "key_findings": [
            {"finding": f"Finding {i}", "confidence": "medium", "source_ids": [f"s{i:02d}"]}
            for i in range(1, 5)
        ],
        "scenario_updates": [
            {"id": "base", "evidence_ids": ["s01"], "verdict": "supports"},
            {"id": "shock", "evidence_ids": ["s02"], "verdict": "supports"},
        ],
        "thesis_status": "supported",
        "thesis_update_md": "Evidence strengthens the near-term supply risk thesis.",
        "open_questions": ["Will official flows confirm the disruption?"],
        "next_queries": [{"q": "official shipping update"}, {"q": "inventory response"}, {"q": "price spread reaction"}],
    }

    write_json(run_dir / "plan" / "abc" / "parsed.json", parsed)
    (run_dir / "plan" / "abc" / "intro.md").write_text("Intro", encoding="utf-8")
    write_json(run_dir / "deliver" / "def" / "news.json", news)
    write_json(run_dir / "deliver" / "def" / "report.json", report)
    (run_dir / "deliver" / "def" / "report.md").write_text(report_md, encoding="utf-8")
    (run_dir / "events.ndjson").write_text(
        '{"event_type":"stage.finished","payload":{"total_cost_usd":0.2}}\n',
        encoding="utf-8",
    )

    result = evaluator.evaluate(run_dir)

    assert result["score"] >= 80
    assert result["verdict"] == "demo_ready"
    assert result["total_cost_usd"] == 0.2
    assert not result["critical_warnings"]


def test_missing_core_artifacts_is_not_demo_ready(tmp_path: Path) -> None:
    run_dir = tmp_path / "empty-run"
    run_dir.mkdir()

    result = evaluator.evaluate(run_dir)

    assert result["verdict"] == "not_demo_ready"
    assert "Missing or invalid parsed.json." in result["critical_warnings"]
    assert result["score"] < 65
