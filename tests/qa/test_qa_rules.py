"""Ticket #15 — validate the rule catalog and its alignment with the gate.

Guards against drift between testing/qa_rules.json and the check ids the
gate actually emits on the healthy fixture.
"""

from __future__ import annotations

import json
from pathlib import Path

from .conftest import GOOD_RUN, RULES, run_gate

REQUIRED_THRESHOLDS = {"min_sources", "min_findings", "min_citations"}


def test_rules_file_is_well_formed():
    rules = json.loads(RULES.read_text())
    assert rules["schema_version"]
    assert REQUIRED_THRESHOLDS <= set(rules["thresholds"])
    assert rules["expected_terminal_state"] == "reported"
    ids = [r["id"] for r in rules["rules"]]
    assert len(ids) == len(set(ids)), "duplicate rule ids"
    for rule in rules["rules"]:
        assert rule["severity"] in {"error", "warning", "info"}
        assert rule["category"] in {
            "artifact",
            "operational",
            "threshold",
            "lifecycle",
            "invariant",
        }
        assert rule["description"]


def test_rules_and_gate_check_ids_match(tmp_path: Path):
    """Every rule id is emitted by the gate and vice versa (no orphan rules)."""
    import shutil

    rules = json.loads(RULES.read_text())
    rule_ids = {r["id"] for r in rules["rules"]}

    run_dir = tmp_path / "run"
    shutil.copytree(GOOD_RUN, run_dir)
    report = run_gate(run_dir)
    gate_ids = {c["id"] for c in report["checks"]}

    assert rule_ids == gate_ids, (
        f"rules-only={rule_ids - gate_ids}, gate-only={gate_ids - rule_ids}"
    )


def test_known_bad_catalog_is_represented():
    """Each known-bad regression in the catalog maps to a gating rule."""
    rules = json.loads(RULES.read_text())
    known_bad = {r["known_bad"] for r in rules["rules"] if r.get("known_bad")}
    expected = {
        "Missing required artifact",
        "Broken event log",
        "Tool error regression",
        "Citation integrity break",
        "Stuck lifecycle",
    }
    assert expected <= known_bad
