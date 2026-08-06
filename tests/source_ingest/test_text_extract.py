from __future__ import annotations

from pathlib import Path

from ebooklib import epub

from source_ingest.text_extract import (
    epub_to_text,
    extract_text,
    html_article_text,
    html_to_text,
)


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


# --- JSON-LD article bodies -------------------------------------------------
# Publishers ship the full body in JSON-LD for search engines while the rendered
# HTML shows a teaser. `html_to_text` skips <script>, so that copy used to be
# dropped on the floor.

_BODY = "Tanker traffic through the strait fell sharply this week. " * 8

_TEASER_PAGE = f"""
<html><head>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"NewsArticle",
 "headline":"Strait traffic falls","articleBody":"{_BODY}"}}
</script>
</head><body><p>Subscribe to read the full story.</p></body></html>
"""


def test_jsonld_body_is_recovered_from_a_teaser_page():
    assert "Subscribe to read" in html_to_text(_TEASER_PAGE)
    assert len(html_to_text(_TEASER_PAGE)) < 200

    text = html_article_text(_TEASER_PAGE)
    assert "Tanker traffic through the strait" in text
    assert len(text) > 200


def test_jsonld_inside_a_graph_is_found():
    page = f"""
    <html><head><script type="application/ld+json">
    {{"@context":"https://schema.org","@graph":[
      {{"@type":"WebSite","name":"Example"}},
      {{"@type":"BlogPosting","text":"{_BODY}"}}]}}
    </script></head><body><p>Teaser.</p></body></html>
    """
    assert "Tanker traffic" in html_article_text(page)


def test_jsonld_body_keeps_its_markup_out_of_the_text():
    page = (
        '<html><head><script type="application/ld+json">'
        '{"@type":"NewsArticle","articleBody":"<p>Oil &amp; gas fell.</p>"}'
        "</script></head><body><p>x</p></body></html>"
    )
    text = html_article_text(page)
    assert "Oil & gas fell." in text
    assert "<p>" not in text


def test_full_page_wins_when_it_is_longer_than_the_jsonld_stub():
    page = (
        '<html><head><script type="application/ld+json">'
        '{"@type":"NewsArticle","articleBody":"Short stub."}'
        "</script></head><body><p>" + _BODY + "</p></body></html>"
    )
    text = html_article_text(page)
    assert "Tanker traffic" in text
    assert text != "Short stub."


def test_unrelated_jsonld_text_is_not_mistaken_for_a_body():
    page = (
        '<html><head><script type="application/ld+json">'
        '{"@type":"Organization","name":"Example Corp","text":"Cookie notice."}'
        "</script></head><body><p>" + _BODY + "</p></body></html>"
    )
    assert "Cookie notice" not in html_article_text(page)


def test_malformed_jsonld_falls_back_to_the_page():
    page = (
        '<html><head><script type="application/ld+json">{not json,,,}</script>'
        "</head><body><p>" + _BODY + "</p></body></html>"
    )
    assert "Tanker traffic" in html_article_text(page)


def test_page_without_jsonld_is_unchanged():
    page = "<html><body><p>" + _BODY + "</p></body></html>"
    assert html_article_text(page) == html_to_text(page)
