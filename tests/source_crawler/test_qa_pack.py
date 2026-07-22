from __future__ import annotations

import json
from pathlib import Path

from source_crawler.qa_pack import (
    build_qa_pack,
    ensure_qa_pack,
    packs_needing_qa,
    render_qa_prompt,
    write_qa_prompt,
    qa_audit_path,
)


def _fixture_text() -> str:
    head = "\n".join(f"Heading {i}" for i in range(1, 6))
    body = head + "\n\n" + ("North Sea Dated assessment methodology. " * 80)
    return body


def _write_text_pair(root: Path, source_id: str, text: str, digest: str) -> tuple[Path, Path]:
    folder = root / source_id
    folder.mkdir(parents=True)
    txt = folder / f"{source_id}.txt"
    txt.write_text(text, encoding="utf-8")
    sidecar = txt.with_suffix(txt.suffix + ".meta.json")
    sidecar.write_text(
        json.dumps(
            {
                "source_id": source_id,
                "title": source_id,
                "url": "https://example.com/x.pdf",
                "publisher": "Argus Media",
                "source_sha256": digest,
                "tags": ["methodology"],
            }
        ),
        encoding="utf-8",
    )
    return txt, sidecar


def test_samples_are_deterministic(tmp_path: Path):
    text = _fixture_text()
    digest = "abc" * 20 + "abcd"
    pack_a = build_qa_pack(*_write_text_pair(tmp_path / "a", "src", text, digest))
    pack_b = build_qa_pack(*_write_text_pair(tmp_path / "b", "src", text, digest))
    assert pack_a["samples"] == pack_b["samples"]


def test_ensure_qa_pack_idempotent(tmp_path: Path):
    text = _fixture_text()
    txt, sidecar = _write_text_pair(tmp_path, "demo", text, "digest-demo-1")
    first = ensure_qa_pack(txt, sidecar)
    assert first.status == "written"
    assert (txt.parent / "qa_pack.json").is_file()
    second = ensure_qa_pack(txt, sidecar)
    assert second.status == "unchanged"


def test_write_qa_prompt(tmp_path: Path):
    text = _fixture_text()
    _write_text_pair(tmp_path, "src_a", text, "d1")
    _write_text_pair(tmp_path, "src_b", text, "d2")
    prompt_path = write_qa_prompt(tmp_path)
    body = prompt_path.read_text(encoding="utf-8")
    assert "src_a" in body
    assert "src_b" in body
    assert "qa_audit.json" in body
    assert "Write the audit JSON" in body


def test_packs_needing_qa_skips_current_audit(tmp_path: Path):
    from source_crawler.qa_pack import packs_needing_qa, qa_audit_path

    text = _fixture_text()
    _write_text_pair(tmp_path, "src_a", text, "d1")
    qa_audit_path(tmp_path).write_text(
        json.dumps(
            {
                "schema_version": 1,
                "sources": [
                    {
                        "source_id": "src_a",
                        "source_sha256": "d1",
                        "verdict": "PASS",
                    }
                ],
                "summary": {"safe_to_promote": ["src_a"]},
            }
        ),
        encoding="utf-8",
    )
    assert packs_needing_qa(tmp_path) == []
