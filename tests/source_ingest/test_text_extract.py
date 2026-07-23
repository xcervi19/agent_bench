from __future__ import annotations

from pathlib import Path

from ebooklib import epub

from source_ingest.text_extract import epub_to_text, extract_text, html_to_text


def _write_minimal_epub(path: Path, chapters: list[tuple[str, str]]) -> None:
    book = epub.EpubBook()
    book.set_identifier("test-epub-001")
    book.set_title("Test Book")
    book.set_language("en")

    spine_items: list[epub.EpubHtml] = []
    toc: list[epub.Link] = []
    for i, (title, body) in enumerate(chapters):
        file_name = f"chap_{i}.xhtml"
        chapter = epub.EpubHtml(title=title, file_name=file_name, lang="en")
        chapter.content = f"<h1>{title}</h1><p>{body}</p>"
        book.add_item(chapter)
        spine_items.append(chapter)
        toc.append(epub.Link(file_name, title, f"chap_{i}"))

    book.toc = tuple(toc)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav", *spine_items]
    epub.write_epub(str(path), book)


def test_html_to_text_strips_script() -> None:
    text = html_to_text("<html><script>x()</script><p>Hello</p></html>")
    assert "Hello" in text
    assert "x()" not in text


def test_epub_to_text_spine_order(tmp_path: Path) -> None:
    path = tmp_path / "sample.epub"
    _write_minimal_epub(
        path,
        [
            ("Intro", "Alpha chapter body for extract."),
            ("Next", "Beta chapter body for extract."),
        ],
    )
    text = epub_to_text(path)
    assert "Alpha chapter body for extract." in text
    assert "Beta chapter body for extract." in text
    assert text.index("Alpha") < text.index("Beta")


def test_extract_text_dispatches_epub(tmp_path: Path) -> None:
    path = tmp_path / "dispatch.epub"
    _write_minimal_epub(
        path,
        [("Only", "Dispatch path works for ebooklib chapters.")],
    )
    text = extract_text(path)
    assert "Dispatch path works" in text
