from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from source_crawler.adapters.jodi_dataset import JodiDatasetAdapter
from source_crawler.models import SourceConfig
from source_crawler.registry import clear, register
from source_crawler.runner import crawl


class _Resp:
    def __init__(
        self,
        body: bytes,
        status: int = 200,
        url: str = "https://ex.com/x.zip",
        content_type: str = "application/zip",
    ):
        self.content = body
        self.status_code = status
        self.headers = {"content-type": content_type}
        self.url = url

    def json(self):
        return json.loads(self.content.decode("utf-8"))


ZIP = b"PK\x03\x04" + b"0" * 2048


@pytest.fixture(autouse=True)
def _registry():
    clear()
    register(JodiDatasetAdapter)
    yield
    clear()


def test_oil_falls_back_to_world_ext_zip(tmp_path):
    def fake_get(url: str, **_kwargs):
        if "api.publisher.jodidata.org" in url:
            return _Resp(
                json.dumps({"publicationId": 0, "files": []}).encode(),
                content_type="application/json",
                url=url,
            )
        if url.endswith("world_ext.zip"):
            return _Resp(ZIP, url=url)
        return _Resp(b"no", status=404, url=url)

    cfg = SourceConfig(
        source_id="jodi_oil_world",
        adapter="jodi_dataset",
        endpoint="https://www.jodidata.org/oil/database/data-downloads.aspx",
        extras={"jodi_kind": "oil", "extension": ".zip", "pipeline": "data_feed"},
        label_assignment="human",
        document_type="official_data",
        use_for=("facts",),
    )
    with patch("source_crawler.adapters.jodi_dataset.http_get", side_effect=fake_get):
        result = crawl(cfg, tmp_path)
    assert result.status == "written"
    assert result.path and result.path.endswith(".zip")


def test_gas_uses_publisher_csv_zip(tmp_path):
    def fake_get(url: str, **_kwargs):
        if "api.publisher.jodidata.org" in url:
            return _Resp(
                json.dumps(
                    {
                        "publicationId": 24,
                        "files": [
                            {"filename": "GAS_world_NewFormat.zip", "format": "CSV"},
                            {"filename": "ivt.zip", "format": "IVT"},
                        ],
                    }
                ).encode(),
                content_type="application/json",
                url=url,
            )
        if "GAS_world_NewFormat.zip" in url:
            return _Resp(ZIP, url=url)
        return _Resp(b"no", status=404, url=url)

    cfg = SourceConfig(
        source_id="jodi_gas_world",
        adapter="jodi_dataset",
        endpoint="https://www.jodidata.org/gas/database/data-downloads.aspx",
        extras={"jodi_kind": "gas", "extension": ".zip", "pipeline": "data_feed"},
        label_assignment="human",
        document_type="official_data",
        use_for=("facts",),
    )
    with patch("source_crawler.adapters.jodi_dataset.http_get", side_effect=fake_get):
        result = crawl(cfg, tmp_path)
    assert result.status == "written"
    assert "jodi_gas_world.zip" in (result.path or "")
