from __future__ import annotations

from eval_framework.artifacts import RunArtifacts
from eval_framework.evaluators.heuristic import _scenario_probability


def artifacts(**over) -> RunArtifacts:
    return RunArtifacts(label="t", **over)


def test_scenarios_read_the_key_deliver_actually_writes():
    a = artifacts(report={"scenario_updates": [{"id": "sc1"}, {"id": "sc2"}]})
    assert len(a.scenarios) == 2


def test_scenarios_still_read_the_rubric_key():
    assert len(artifacts(report={"scenarios": [{"id": "sc1"}]}).scenarios) == 1


def test_scenarios_absent_is_empty():
    assert artifacts(report={}).scenarios == []


def test_run_dt_falls_back_to_plan_created_at():
    a = artifacts(parsed={"created_at": "2026-08-01T15:16:42Z"})
    assert a.run_dt is not None


def test_run_timestamp_wins_over_plan_created_at():
    a = artifacts(run_timestamp="2026-07-01T00:00:00Z", parsed={"created_at": "2026-08-01T00:00:00Z"})
    assert a.run_dt.month == 7


def test_run_dt_none_when_neither_present():
    assert artifacts().run_dt is None


def test_scenario_probability_accepts_delivered_keys():
    assert _scenario_probability({"p_after": 0.45}) == 0.45
    assert _scenario_probability({"p_before": 0.2}) == 0.2
    assert _scenario_probability({"probability": 0.3}) == 0.3


def test_scenario_probability_prefers_explicit_probability():
    assert _scenario_probability({"probability": 0.3, "p_after": 0.9}) == 0.3


def test_scenario_probability_none_when_absent():
    assert _scenario_probability({"label": "x"}) is None
