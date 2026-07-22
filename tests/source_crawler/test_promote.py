from __future__ import annotations

import json
from pathlib import Path

from source_crawler.promote import promote_all, promote_one


def _write_collected(
    root: Path,
    source_id: str,
    *,
    promote: bool,
    body: bytes = b"%PDF-1.4\n" + b"x" * 100,
    digest: str = "abc123",
    tier: int = 1,
    domain: str = "trading_mechanics",
    labels: bool = True,
) -> Path:
    folder = root / source_id
    folder.mkdir(parents=True)
    content = folder / f"{source_id}.pdf"
    content.write_bytes(body)
    meta = {
        "source_id": source_id,
        "title": source_id,
        "tier": tier,
        "domain": domain,
        "promote": promote,
        "sha256": digest,
        "url": "https://example.com/x.pdf",
    }
    if labels:
        meta.update(
            {
                "label_assignment": "human",
                "document_type": "methodology",
                "use_for": ["pricing_context"],
            }
        )
    content.with_suffix(content.suffix + ".meta.json").write_text(
        json.dumps(meta), encoding="utf-8"
    )
    return content


def test_promote_gate_and_layout(tmp_path: Path):
    collected = tmp_path / "collected"
    kb = tmp_path / "rag_corpus"
    yes = _write_collected(collected, "meth_yes", promote=True)
    _write_collected(collected, "meth_no", promote=False)

    results = promote_all(collected, kb)
    by_id = {r.source_id: r for r in results}
    assert by_id["meth_yes"].status == "promoted"
    assert by_id["meth_no"].status == "skipped"

    dest = kb / "methodology" / "tier_1" / "trading_mechanics" / "meth_yes.pdf"
    assert dest.is_file()
    assert dest.read_bytes() == yes.read_bytes()
    sidecar = json.loads(dest.with_suffix(".pdf.meta.json").read_text(encoding="utf-8"))
    assert sidecar["promoted"] is True
    assert sidecar["sha256"] == "abc123"
    assert sidecar["document_type"] == "methodology"
    assert sidecar["use_for"] == ["pricing_context"]


def test_promote_blocks_missing_labels(tmp_path: Path):
    collected = tmp_path / "collected"
    kb = tmp_path / "kb"
    path = _write_collected(collected, "nolabel", promote=True, labels=False)
    result = promote_one(path, kb)
    assert result.status == "skipped"
    assert "label_assignment" in (result.reason or "")


def test_promote_unchanged_by_sha(tmp_path: Path):
    collected = tmp_path / "collected"
    kb = tmp_path / "kb"
    path = _write_collected(collected, "meth_yes", promote=True, digest="same")
    first = promote_one(path, kb)
    assert first.status == "promoted"
    second = promote_one(path, kb)
    assert second.status == "unchanged"


def test_force_source_id_bypasses_gate(tmp_path: Path):
    collected = tmp_path / "collected"
    kb = tmp_path / "kb"
    _write_collected(collected, "forced", promote=False)
    results = promote_all(collected, kb, source_ids={"forced"})
    assert results[0].status == "promoted"
