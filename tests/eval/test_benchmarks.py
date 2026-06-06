"""Pluggable benchmark provider registry + fixture provider."""

from __future__ import annotations

from pathlib import Path

import pytest
from eval_framework import (
    FixtureProvider,
    benchmark_provider,
    compare,
    evaluate_artifacts,
    get_provider,
    list_providers,
    register_provider,
)
from eval_framework.benchmarks import BenchmarkProvider, clear_registry


@pytest.fixture(autouse=True)
def _clean_registry():
    clear_registry()
    yield
    clear_registry()


def test_fixture_provider_produces_artifacts(good_run: Path):
    provider = FixtureProvider("newsfind", str(good_run), kind="agent")
    register_provider(provider)
    assert "newsfind" in list_providers()
    artifacts = get_provider("newsfind").produce("Hormuz")
    assert artifacts.sources, "fixture provider should load sources"
    result = evaluate_artifacts(artifacts)
    assert result.overall_score > 0


def test_decorator_registration_extends_without_core_changes(good_run: Path):
    """A new baseline provider can be added purely by registering it."""

    @benchmark_provider("generic_llm_stub", kind="baseline")
    class _GenericLLM(BenchmarkProvider):
        def produce(self, topic: str, **kwargs):
            # Stub: a no-internet model produces an empty/weak artifact set.
            from eval_framework.artifacts import RunArtifacts

            return RunArtifacts(label="generic_llm_stub", topic=topic)

    assert "generic_llm_stub" in list_providers()
    weak = get_provider("generic_llm_stub").produce("Hormuz")
    assert weak.sources == []


def test_agent_vs_baseline_uses_same_rubric(good_run: Path):
    register_provider(FixtureProvider("newsfind", str(good_run), kind="agent"))

    @benchmark_provider("internet_disabled_stub", kind="baseline")
    class _NoNet(BenchmarkProvider):
        def produce(self, topic: str, **kwargs):
            from eval_framework.artifacts import RunArtifacts

            return RunArtifacts(label="internet_disabled_stub", topic=topic)

    agent = evaluate_artifacts(get_provider("newsfind").produce("Hormuz"), label="agent")
    baseline = evaluate_artifacts(
        get_provider("internet_disabled_stub").produce("Hormuz"), label="baseline"
    )
    comp = compare(baseline, agent)
    # Our agent must beat an internet-disabled baseline on discovery.
    assert comp.overall_candidate > comp.overall_baseline


def test_duplicate_registration_rejected(good_run: Path):
    register_provider(FixtureProvider("dup", str(good_run)))
    with pytest.raises(ValueError):
        register_provider(FixtureProvider("dup", str(good_run)))
