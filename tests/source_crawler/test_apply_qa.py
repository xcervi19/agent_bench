from __future__ import annotations

import json
from pathlib import Path

from source_crawler.apply_qa import apply_qa, load_audit, resolve_promote_ids


def _labels(**extra: object) -> dict:
    base = {
        "label_assignment": "human",
        "document_type": "methodology",
        "use_for": ["pricing_context"],
    }
    base.update(extra)
    return base


def _write_collected(
    root: Path,
    source_id: str,
    *,
    digest: str,
    body: bytes = b"%PDF-1.4\n" + b"x" * 100,
    labels: dict | None = None,
) -> Path:
    folder = root / source_id
    folder.mkdir(parents=True)
    content = folder / f"{source_id}.pdf"
    content.write_bytes(body)
    meta = {
        "source_id": source_id,
        "title": source_id,
        "tier": 1,
        "domain": "trading_mechanics",
        "sha256": digest,
        "url": "https://example.com/x.pdf",
        **(labels if labels is not None else _labels()),
    }
    content.with_suffix(content.suffix + ".meta.json").write_text(
        json.dumps(meta), encoding="utf-8"
    )
    return content


def _write_text(root: Path, source_id: str, *, digest: str, text: str) -> None:
    folder = root / source_id
    folder.mkdir(parents=True, exist_ok=True)
    txt = folder / f"{source_id}.txt"
    txt.write_text(text, encoding="utf-8")
    sidecar = txt.with_suffix(txt.suffix + ".meta.json")
    sidecar.write_text(
        json.dumps(
            {
                "source_id": source_id,
                "source_sha256": digest,
                "title": source_id,
                **_labels(),
            }
        ),
        encoding="utf-8",
    )


def _audit(source_id: str, digest: str, **extra: object) -> dict:
    row = {
        "source_id": source_id,
        "source_sha256": digest,
        "verdict": "PASS",
        "confidence": "high",
        "reason": "methodology guide",
        "document_type": "methodology",
        "use_for": ["pricing_context"],
        "proposed_labels": [],
        "signals_found": ["assessment"],
        "red_flags": [],
    }
    row.update(extra)
    return {
        "schema_version": 1,
        "reviewed_at": "2026-01-01T00:00:00+00:00",
        "sources": [row],
        "summary": {
            "overall": "PASS",
            "safe_to_promote": [source_id],
            "block_promote": [],
            "notes": [],
        },
    }


def test_apply_qa_promotes_pass(tmp_path: Path):
    collected = tmp_path / "collected"
    text_root = tmp_path / "collected_text"
    kb = tmp_path / "kb"
    digest = "sha-demo-1"
    _write_collected(collected, "meth_ok", digest=digest)
    _write_text(text_root, "meth_ok", digest=digest, text="methodology " * 50)

    audit_path = text_root / "qa_audit.json"
    audit_path.write_text(json.dumps(_audit("meth_ok", digest)), encoding="utf-8")

    results = apply_qa(audit_path, collected, kb, text_root)
    assert results[0].status == "promoted"
    dest = kb / "methodology" / "tier_1" / "trading_mechanics" / "meth_ok.pdf"
    assert dest.is_file()


def test_apply_qa_blocks_missing_human_labels(tmp_path: Path):
    collected = tmp_path / "collected"
    text_root = tmp_path / "collected_text"
    kb = tmp_path / "kb"
    digest = "d1"
    _write_collected(collected, "meth_ok", digest=digest, labels={})
    _write_text(text_root, "meth_ok", digest=digest, text="methodology " * 50)
    audit_path = text_root / "qa_audit.json"
    audit_path.write_text(json.dumps(_audit("meth_ok", digest)), encoding="utf-8")

    results = apply_qa(audit_path, collected, kb, text_root, dry_run=True)
    assert results[0].status == "blocked"
    assert "label_assignment" in (results[0].reason or "")


def test_apply_qa_agent_labels_from_audit(tmp_path: Path):
    collected = tmp_path / "collected"
    text_root = tmp_path / "collected_text"
    kb = tmp_path / "kb"
    digest = "d2"
    _write_collected(
        collected,
        "book_x",
        digest=digest,
        labels={"label_assignment": "agent"},
    )
    _write_text(text_root, "book_x", digest=digest, text="trading handbook " * 40)
    audit_path = text_root / "qa_audit.json"
    audit_path.write_text(
        json.dumps(
            _audit(
                "book_x",
                digest,
                document_type="education",
                use_for=["trading_knowhow"],
            )
        ),
        encoding="utf-8",
    )
    results = apply_qa(audit_path, collected, kb, text_root)
    assert results[0].status == "promoted"
    sidecar = json.loads(
        (
            kb / "education" / "tier_1" / "trading_mechanics" / "book_x.pdf.meta.json"
        ).read_text(encoding="utf-8")
    )
    assert sidecar["document_type"] == "education"
    assert sidecar["use_for"] == ["trading_knowhow"]


def test_apply_qa_blocks_stale_hash(tmp_path: Path):
    collected = tmp_path / "collected"
    text_root = tmp_path / "collected_text"
    kb = tmp_path / "kb"
    _write_collected(collected, "meth_ok", digest="raw-hash")
    _write_text(text_root, "meth_ok", digest="text-hash", text="methodology " * 50)

    audit_path = text_root / "qa_audit.json"
    audit_path.write_text(json.dumps(_audit("meth_ok", "old-hash")), encoding="utf-8")

    results = apply_qa(audit_path, collected, kb, text_root, dry_run=True)
    assert results[0].status == "blocked"


def test_apply_qa_dry_run(tmp_path: Path):
    collected = tmp_path / "collected"
    text_root = tmp_path / "collected_text"
    kb = tmp_path / "kb"
    digest = "d1"
    _write_collected(collected, "meth_ok", digest=digest)
    _write_text(text_root, "meth_ok", digest=digest, text="methodology " * 50)
    audit_path = text_root / "qa_audit.json"
    audit_path.write_text(json.dumps(_audit("meth_ok", digest)), encoding="utf-8")

    results = apply_qa(audit_path, collected, kb, text_root, dry_run=True)
    assert results[0].status == "planned"
    assert not (kb / "methodology").exists()


def test_resolve_promote_ids(tmp_path: Path):
    text_root = tmp_path / "collected_text"
    _write_text(text_root, "a", digest="h1", text="x " * 60)
    audit = _audit("a", "h1")
    ids, _ = resolve_promote_ids(audit, text_root)
    assert ids == {"a"}


def test_load_audit_schema_version(tmp_path: Path):
    path = tmp_path / "qa_audit.json"
    path.write_text(json.dumps({"schema_version": 99, "sources": [], "summary": {}}))
    import pytest

    from source_crawler.apply_qa import load_audit

    with pytest.raises(ValueError, match="schema_version"):
        load_audit(path)
