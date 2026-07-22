from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from source_crawler.adapters.static_pdf import StaticPdfAdapter
from source_crawler.models import SourceConfig, SourceTarget
from source_crawler.registry import clear, register
from source_crawler.runner import crawl
from source_crawler.store import sha256_hex


class _Resp:
    def __init__(self, body: bytes, status: int = 200, url: str = "https://ex.com/a.pdf"):
        self.content = body
        self.status_code = status
        self.headers = {"content-type": "application/pdf"}
        self.url = url


PDF = b"%PDF-1.4\n" + b"0" * 2048


@pytest.fixture(autouse=True)
def _registry():
    clear()
    register(StaticPdfAdapter)
    yield
    clear()


def test_fetch_writes_and_skips_unchanged(tmp_path: Path):
    adapter = StaticPdfAdapter()
    config = SourceConfig(
        source_id="demo_meth",
        adapter="static_pdf",
        endpoint="https://ex.com/a.pdf",
        title="Demo",
        publisher="Test",
        tags=("methodology",),
        label_assignment="human",
        document_type="methodology",
        use_for=("pricing_context",),
    )
    with patch(
        "source_crawler.adapters.static_pdf._http_get",
        return_value=_Resp(PDF),
    ):
        first = crawl(config, tmp_path)
        assert first.status == "written"
        assert first.path is not None
        assert Path(first.path).is_file()
        meta = Path(first.path + ".meta.json")
        assert meta.is_file()
        assert '"sha256"' in meta.read_text(encoding="utf-8")

        second = crawl(first.config, tmp_path)
        assert second.status == "unchanged"
        assert second.sha256 == sha256_hex(PDF)

        # CLI-style re-run: watermark only on disk sidecar
        third = crawl(config, tmp_path)
        assert third.status == "unchanged"


def test_evaluate_rejects_non_pdf():
    with patch(
        "source_crawler.adapters.static_pdf._http_get",
        return_value=_Resp(b"<html>nope</html>" + b"x" * 2048, url="https://ex.com/x"),
    ):
        assessment = StaticPdfAdapter().evaluate(SourceTarget(url="https://ex.com/x"))
    assert assessment.viable is False


def test_fetch_http_error_returns_failed(tmp_path: Path):
    config = SourceConfig(
        source_id="blocked",
        adapter="static_pdf",
        endpoint="https://ex.com/blocked.pdf",
        label_assignment="human",
        document_type="methodology",
        use_for=("pricing_context",),
    )
    with patch(
        "source_crawler.adapters.static_pdf._http_get",
        return_value=_Resp(b"", status=403),
    ):
        result = crawl(config, tmp_path)
    assert result.status == "failed"
    assert "HTTP 403" in (result.reason or "")


def test_fetch_error_keeps_local_and_syncs_labels(tmp_path: Path):
    config = SourceConfig(
        source_id="kept_local",
        adapter="static_pdf",
        endpoint="https://ex.com/kept.pdf",
        label_assignment="human",
        document_type="methodology",
        use_for=("pricing_context",),
    )
    with patch(
        "source_crawler.adapters.static_pdf._http_get",
        return_value=_Resp(PDF),
    ):
        first = crawl(config, tmp_path)
    assert first.status == "written"

    with patch(
        "source_crawler.adapters.static_pdf._http_get",
        return_value=_Resp(b"", status=403),
    ):
        second = crawl(config, tmp_path)
    assert second.status == "unchanged"
    assert "kept local" in (second.reason or "")
    meta = json.loads(
        Path(first.path + ".meta.json").read_text(encoding="utf-8")  # type: ignore[arg-type]
    )
    assert meta["document_type"] == "methodology"
    assert meta["label_assignment"] == "human"
