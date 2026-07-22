from __future__ import annotations

import json
from pathlib import Path

from source_crawler.extract import extract_all, extract_one


def _write_collected_txt(
    root: Path,
    source_id: str,
    body: str,
    *,
    digest: str = "digest1",
) -> Path:
    folder = root / source_id
    folder.mkdir(parents=True)
    content = folder / f"{source_id}.txt"
    content.write_text(body, encoding="utf-8")
    meta = {
        "source_id": source_id,
        "title": source_id,
        "sha256": digest,
        "url": "https://example.com/x",
        "tier": 1,
        "domain": "trading_mechanics",
    }
    content.with_suffix(content.suffix + ".meta.json").write_text(
        json.dumps(meta), encoding="utf-8"
    )
    return content


def test_extract_writes_collected_text(tmp_path: Path):
    collected = tmp_path / "collected"
    text_root = tmp_path / "collected_text"
    body = "Chapter 1 Pricing\n\n" + ("Argus methodology text. " * 20)
    src = _write_collected_txt(collected, "demo_src", body)

    result = extract_one(src, text_root)
    assert result.status == "written"
    dest = Path(result.path)
    assert dest.is_file()
    assert "Chapter 1 Pricing" in dest.read_text(encoding="utf-8")
    meta = json.loads(dest.with_suffix(dest.suffix + ".meta.json").read_text())
    assert meta["layer"] == "collected_text"
    assert meta["source_sha256"] == "digest1"
    assert meta["extractor"] == "source_ingest.text_extract"


def test_extract_unchanged_by_source_sha(tmp_path: Path):
    collected = tmp_path / "collected"
    text_root = tmp_path / "collected_text"
    body = "Section A\n\n" + ("enough content here for extraction. " * 10)
    src = _write_collected_txt(collected, "demo_src", body)
    assert extract_one(src, text_root).status == "written"
    assert extract_one(src, text_root).status == "unchanged"


def test_extract_source_id_filter(tmp_path: Path):
    collected = tmp_path / "collected"
    text_root = tmp_path / "collected_text"
    body = "Title\n\n" + ("body text for qa sample. " * 15)
    _write_collected_txt(collected, "keep_me", body)
    _write_collected_txt(collected, "drop_me", body, digest="d2")
    results = extract_all(collected, text_root, source_ids={"keep_me"})
    by_id = {r.source_id: r for r in results}
    assert by_id["keep_me"].status == "written"
    assert by_id["drop_me"].status == "skipped"
