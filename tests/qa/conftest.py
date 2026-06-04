"""Shared helpers for ticket #15 technical verification tests.

These tests are non-billable and require no network: they exercise the
mechanical QA gate (``scripts/qa_check_run.sh``) against a committed healthy
run fixture and runtime-mutated broken copies of it. The gate's pass/fail
contract is the unit under test.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
GATE = REPO_ROOT / "scripts" / "qa_check_run.sh"
RULES = REPO_ROOT / "testing" / "qa_rules.json"
GOOD_RUN = REPO_ROOT / "testing" / "fixtures" / "good_run"


def run_gate(run_dir: Path) -> dict:
    """Run qa_check_run.sh against ``run_dir`` and return the parsed report.

    Adds a ``returncode`` key so tests can assert the process exit contract
    (0 = PASS, 1 = FAIL) alongside the JSON verdict.
    """
    out_file = run_dir / "qa_report.json"
    proc = subprocess.run(
        [
            "bash",
            str(GATE),
            "--run-dir",
            str(run_dir),
            "--out",
            str(out_file),
            "--rules",
            str(RULES),
        ],
        capture_output=True,
        text=True,
    )
    assert out_file.exists(), f"gate did not write report\nstdout={proc.stdout}\nstderr={proc.stderr}"
    report = json.loads(out_file.read_text())
    report["returncode"] = proc.returncode
    return report


def failed_ids(report: dict) -> set[str]:
    return set(report.get("failed_checks", []))


@pytest.fixture
def good_run(tmp_path: Path) -> Path:
    """A fresh, writable copy of the healthy run fixture."""
    dst = tmp_path / "run"
    shutil.copytree(GOOD_RUN, dst)
    return dst


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def _write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2))


def break_run(run_dir: Path, kind: str) -> None:
    """Mutate a copied good run to reproduce a known-bad regression case."""
    biz = run_dir / "business_output"
    agent = run_dir / "agent_log"

    if kind == "missing_report_json":
        (biz / "report.json").unlink()

    elif kind == "tool_errors":
        ev = _read_json(run_dir / "evaluation.json")
        ev["events"]["tool_errors"] = 2
        _write_json(run_dir / "evaluation.json", ev)

    elif kind == "low_sources":
        ev = _read_json(run_dir / "evaluation.json")
        ev["deliver"]["sources_total"] = 2
        _write_json(run_dir / "evaluation.json", ev)

    elif kind == "few_citations":
        ev = _read_json(run_dir / "evaluation.json")
        ev["deliver"]["unique_citations"] = 1
        _write_json(run_dir / "evaluation.json", ev)

    elif kind == "broken_citation":
        report_md = biz / "report.md"
        report_md.write_text(report_md.read_text() + "\nDangling claim [s99].\n")

    elif kind == "stuck_state":
        tf = _read_json(agent / "topic_final.json")
        tf["state"] = "delivering"
        _write_json(agent / "topic_final.json", tf)

    elif kind == "failed_state":
        tf = _read_json(agent / "topic_final.json")
        tf["state"] = "failed"
        tf["error"] = "deliver crashed"
        _write_json(agent / "topic_final.json", tf)

    elif kind == "empty_events":
        (agent / "events_full.ndjson").write_text("")

    elif kind == "missing_deliver_stage":
        ev_file = agent / "events_full.ndjson"
        kept = [
            line
            for line in ev_file.read_text().splitlines()
            if not ('"stage.finished"' in line and '"stage":"deliver"' in line)
        ]
        ev_file.write_text("\n".join(kept) + "\n")

    else:  # pragma: no cover - guard against typos in test params
        raise ValueError(f"unknown break kind: {kind}")
