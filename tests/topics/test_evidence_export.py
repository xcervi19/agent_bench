"""The corpus handed to the analyst must be readable and traceable.

The report is otherwise built from search snippets. Exporting the full text we
already fetched is what lets synthesis quote the article — so the files have to
carry enough provenance to cite, and must not be corrupted by odd titles.
"""

from datetime import UTC, datetime
from pathlib import Path

from apps.claude_agent.topics.evidence_export import TRUNCATION_NOTE, write_documents

WHEN = datetime(2026, 8, 6, 6, 24, tzinfo=UTC)


def _row(url_hash, url, title, content, status="fetched", method="http"):
    return (url_hash, url, title, content, status, method, WHEN)


def test_each_document_becomes_a_file_with_citable_provenance(tmp_path: Path):
    rows = [_row("a1b2c3d4", "https://iea.org/omr", "Oil Market Report", "Body text here.")]
    entries = write_documents(rows, tmp_path, 40_000)

    written = (tmp_path / entries[0]["file"]).read_text(encoding="utf-8")
    assert "url: https://iea.org/omr" in written
    assert "url_hash: a1b2c3d4" in written
    assert "title: Oil Market Report" in written
    assert "fetch_method: http" in written
    assert written.rstrip().endswith("Body text here.")


def test_a_multiline_title_cannot_break_the_front_matter(tmp_path: Path):
    rows = [_row("ff00", "https://x.example/a", "Line one\nLine two\r\nLine three", "Body.")]
    write_documents(rows, tmp_path, 40_000)

    written = (tmp_path / "ff00.md").read_text(encoding="utf-8")
    head, _, body = written.partition("\n---\n")
    assert head.count("---") == 1, "front matter must stay a single block"
    assert "title: Line one Line two Line three" in head
    assert body.strip() == "Body."


def test_long_documents_are_truncated_but_marked(tmp_path: Path):
    rows = [_row("beef", "https://x.example/long", "Long", "x" * 5000)]
    entries = write_documents(rows, tmp_path, 1000)

    written = (tmp_path / "beef.md").read_text(encoding="utf-8")
    assert TRUNCATION_NOTE.strip() in written
    assert entries[0]["chars"] == 1000 + len(TRUNCATION_NOTE)


def test_short_documents_are_left_whole(tmp_path: Path):
    rows = [_row("cafe", "https://x.example/s", "Short", "just a little")]
    write_documents(rows, tmp_path, 40_000)
    assert TRUNCATION_NOTE.strip() not in (tmp_path / "cafe.md").read_text(encoding="utf-8")


def test_filenames_stay_path_safe(tmp_path: Path):
    rows = [_row("../../etc/pw", "https://x.example/a", "T", "body")]
    entries = write_documents(rows, tmp_path, 40_000)

    assert "/" not in entries[0]["file"] and ".." not in entries[0]["file"]
    assert (tmp_path / entries[0]["file"]).is_file()
    assert {p.name for p in tmp_path.iterdir()} == {entries[0]["file"]}


def test_every_row_is_exported(tmp_path: Path):
    rows = [_row(f"h{i:04d}", f"https://x.example/{i}", f"T{i}", f"body {i}") for i in range(12)]
    entries = write_documents(rows, tmp_path, 40_000)

    assert len(entries) == 12
    assert len(list(tmp_path.glob("*.md"))) == 12
    assert len({e["file"] for e in entries}) == 12, "filenames must not collide"


def test_a_missing_body_does_not_crash_the_export(tmp_path: Path):
    entries = write_documents([_row("dead", "https://x.example/n", None, None)], tmp_path, 40_000)
    assert entries[0]["chars"] == 0
    assert (tmp_path / "dead.md").is_file()
