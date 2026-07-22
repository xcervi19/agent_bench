from __future__ import annotations

import pytest

from source_crawler import (
    DocRef,
    DownloadedDoc,
    SourceAdapter,
    SourceAssessment,
    SourceConfig,
    SourceTarget,
    get,
    names,
    register,
)
from source_crawler.registry import clear


class _StubAdapter(SourceAdapter):
    name = "stub"

    def evaluate(self, target: SourceTarget) -> SourceAssessment:
        return SourceAssessment(
            adapter=self.name,
            endpoint=target.url,
            viable=True,
            reason="ok",
            proposed_config=SourceConfig(
                source_id="stub_src",
                adapter=self.name,
                endpoint=target.url,
            ),
        )

    def discover(self, config: SourceConfig) -> list[DocRef]:
        return [DocRef(url=config.endpoint)]

    def fetch(self, ref: DocRef, config: SourceConfig) -> DownloadedDoc:
        return DownloadedDoc(
            ref=ref,
            body=b"hello",
            content_type="text/plain",
            extension=".txt",
        )


@pytest.fixture(autouse=True)
def _clean_registry():
    clear()
    yield
    clear()


def test_register_and_get():
    register(_StubAdapter)
    assert names() == ["stub"]
    adapter = get("stub")
    assessment = adapter.evaluate(SourceTarget(url="https://example.com/feed"))
    assert assessment.viable is True
    assert assessment.proposed_config is not None
    assert assessment.proposed_config.adapter == "stub"


def test_unknown_adapter_fails_fast():
    with pytest.raises(KeyError, match="unknown adapter"):
        get("missing")


def test_duplicate_register_fails_fast():
    register(_StubAdapter)
    with pytest.raises(ValueError, match="already registered"):
        register(_StubAdapter)
