"""Ticket #15 — fixture-based tests for the mechanical QA gate.

Healthy fixture must PASS; each injected-bad variant must FAIL with the
specific check id that maps to the known-bad regression catalog in
docs/specs/done/newsfind_application_verification_15.md.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from .conftest import break_run, failed_ids, run_gate

# kind -> the gating check id that must turn red for that regression.
BAD_CASES = {
    "missing_report_json": "artifact_report_json",
    "tool_errors": "tool_errors_zero",
    "low_sources": "sources_total_threshold",
    "few_citations": "unique_citations_threshold",
    "broken_citation": "citation_integrity",
    "stuck_state": "terminal_state_reported",
    "failed_state": "no_error_terminal",
    "empty_events": "artifact_events_full_ndjson",
    "missing_deliver_stage": "stage_progression_deliver",
}


def test_good_run_passes(good_run: Path):
    report = run_gate(good_run)
    assert report["passed"] is True, report["failed_checks"]
    assert report["returncode"] == 0
    assert report["summary"]["checks_failed"] == 0
    # The gate must actually evaluate the full rule set, not a subset.
    assert report["summary"]["checks_total"] == 16


@pytest.mark.parametrize("kind,expected_check", sorted(BAD_CASES.items()))
def test_injected_bad_run_fails(good_run: Path, kind: str, expected_check: str):
    break_run(good_run, kind)
    report = run_gate(good_run)
    assert report["passed"] is False, f"{kind} should fail the gate"
    assert report["returncode"] == 1
    assert expected_check in failed_ids(report), (
        f"{kind} expected check '{expected_check}' to fail; "
        f"got {sorted(failed_ids(report))}"
    )


def test_broken_citation_reports_unresolved_id(good_run: Path):
    break_run(good_run, "broken_citation")
    report = run_gate(good_run)
    citation = next(c for c in report["checks"] if c["id"] == "citation_integrity")
    assert citation["pass"] is False
    assert "s99" in citation["actual"]["unresolved"]


def test_failed_state_trips_both_lifecycle_checks(good_run: Path):
    break_run(good_run, "failed_state")
    report = run_gate(good_run)
    failed = failed_ids(report)
    assert {"no_error_terminal", "terminal_state_reported"} <= failed


def test_threshold_override_flag_changes_verdict(good_run: Path, tmp_path: Path):
    """CLI override must win over rules-file thresholds."""
    import json
    import subprocess

    out_file = good_run / "qa_report.json"
    # Healthy fixture has 6 sources; demand 99 -> must fail on sources only.
    proc = subprocess.run(
        [
            "bash",
            str(Path(__file__).resolve().parents[2] / "scripts" / "qa_check_run.sh"),
            "--run-dir",
            str(good_run),
            "--out",
            str(out_file),
            "--min-sources",
            "99",
        ],
        capture_output=True,
        text=True,
    )
    report = json.loads(out_file.read_text())
    assert proc.returncode == 1
    assert "sources_total_threshold" in report["failed_checks"]
