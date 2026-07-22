from __future__ import annotations

from unittest.mock import patch

import pytest

from source_crawler.adapters.opec_assetdb import OpecAssetdbAdapter
from source_crawler.models import SourceConfig
from source_crawler.registry import clear, register


@pytest.fixture(autouse=True)
def _registry():
    clear()
    register(OpecAssetdbAdapter)
    yield
    clear()


def test_discover_picks_newest_live_monthly_pdf():
    calls: list[str] = []

    def fake_probe(url: str):
        calls.append(url)
        if "momr-june-2026.pdf" in url:
            return url
        return None

    cfg = SourceConfig(
        source_id="opec_momr",
        adapter="opec_assetdb",
        endpoint="https://www.opec.org/monthly-oil-market-report.html",
        extras={
            "cadence": "monthly",
            "url_template": "https://www.opec.org/assets/assetdb/momr-{month}-{year}.pdf",
        },
        label_assignment="human",
        document_type="official_data",
        use_for=("facts",),
    )

    class _D:
        year = 2026
        month = 7
        day = 22

    with patch("source_crawler.adapters.opec_assetdb.date") as mock_date, patch(
        "source_crawler.adapters.opec_assetdb._probe_pdf_url",
        side_effect=fake_probe,
    ):
        mock_date.today.return_value = _D()
        refs = OpecAssetdbAdapter().discover(cfg)

    assert len(refs) == 1
    assert refs[0].url.endswith("momr-june-2026.pdf")
    assert any("momr-july-2026.pdf" in u for u in calls)


def test_discover_yearly_asb():
    def fake_probe(url: str):
        if "asb-2025.pdf" in url:
            return url
        return None

    cfg = SourceConfig(
        source_id="opec_asb",
        adapter="opec_assetdb",
        endpoint="https://www.opec.org/annual-statistical-bulletin.html",
        extras={
            "cadence": "yearly",
            "url_template": "https://www.opec.org/assets/assetdb/asb-{year}.pdf",
        },
        label_assignment="human",
        document_type="official_data",
        use_for=("facts",),
    )

    class _D:
        year = 2026
        month = 7
        day = 22

    with patch("source_crawler.adapters.opec_assetdb.date") as mock_date, patch(
        "source_crawler.adapters.opec_assetdb._probe_pdf_url",
        side_effect=fake_probe,
    ):
        mock_date.today.return_value = _D()
        refs = OpecAssetdbAdapter().discover(cfg)

    assert refs[0].url.endswith("asb-2025.pdf")
