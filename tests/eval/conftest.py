"""Shared fixtures for the Trading Intelligence Evaluation Framework (#23).

Offline and non-billable: the heuristic evaluator is deterministic and needs no
network. Tests run against the committed ``testing/fixtures/good_run`` plus a
runtime-degraded copy of it.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
LIBS = REPO_ROOT / "libs"
if str(LIBS) not in sys.path:
    sys.path.insert(0, str(LIBS))

GOOD_RUN = REPO_ROOT / "testing" / "fixtures" / "good_run"


@pytest.fixture
def good_run() -> Path:
    return GOOD_RUN


@pytest.fixture
def good_run_copy(tmp_path: Path) -> Path:
    dst = tmp_path / "good"
    shutil.copytree(GOOD_RUN, dst)
    return dst


def _read(path: Path) -> dict:
    return json.loads(path.read_text())


def _write(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2))


@pytest.fixture
def degraded_run(tmp_path: Path) -> Path:
    """A strictly weaker copy: aggregator-only sources, no scenarios/findings.

    Designed so the candidate should score WORSE than the good run across
    multiple categories and overall.
    """
    dst = tmp_path / "degraded"
    shutil.copytree(GOOD_RUN, dst)
    biz = dst / "business_output"

    news = _read(biz / "news.json")
    for s in news["sources"]:
        s["source_class"] = "aggregator"
        s["language"] = "en"
        s["relevance_score"] = 0.4
        s["novelty_score"] = 0.2
    # keep only two aggregator sources to thin coverage
    news["sources"] = news["sources"][:2]
    news.pop("drops", None)
    _write(biz / "news.json", news)

    report = _read(biz / "report.json")
    report["scenarios"] = []
    report["key_findings"] = [
        {"finding": "Prices may move.", "confidence": "", "source_ids": ["s01"]}
    ]
    report["summary_md"] = "Prices may move."
    report.pop("next_queries", None)
    report.pop("open_questions", None)
    _write(biz / "report.json", report)

    (biz / "report.md").write_text("# Update\n\nPrices may move [s01].\n")

    parsed = _read(biz / "parsed.json")
    parsed["entities"] = {"actors": [{"name": "OPEC"}]}
    parsed["queries"] = parsed["queries"][:1]
    parsed["rag_context_refs"] = []
    parsed["working_thesis"] = ""
    _write(biz / "parsed.json", parsed)

    return dst
