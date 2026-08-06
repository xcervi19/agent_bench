from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path


class _HtmlText(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip = False
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript"}:
            self._skip = True

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"}:
            self._skip = False

    def handle_data(self, data: str) -> None:
        if self._skip:
            return
        t = data.strip()
        if t:
            self._parts.append(t)

    def plain(self) -> str:
        return "\n\n".join(self._parts)


def html_to_text(raw: str) -> str:
    parser = _HtmlText()
    parser.feed(raw)
    parser.close()
    text = parser.plain()
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


class _JsonLdBlocks(HTMLParser):
    """Collects the raw contents of every <script type="application/ld+json">.

    HTMLParser switches to CDATA mode inside <script>, so `handle_data` hands us
    the JSON verbatim — no entity conversion to undo.
    """

    def __init__(self) -> None:
        super().__init__()
        self._capture = False
        self.blocks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "script":
            declared = {v.lower().strip() for k, v in attrs if k == "type" and v}
            self._capture = "application/ld+json" in declared

    def handle_endtag(self, tag: str) -> None:
        if tag == "script":
            self._capture = False

    def handle_data(self, data: str) -> None:
        if self._capture:
            self.blocks.append(data)


# schema.org types whose `text` property is the body copy. `articleBody` is
# unambiguous on its own and is taken from any node.
_ARTICLE_TYPE_HINTS = ("article", "blogposting", "posting", "report", "webpage")


def _is_article_node(node: dict) -> bool:
    declared = node.get("@type", "")
    types = declared if isinstance(declared, list) else [declared]
    return any(
        isinstance(t, str) and any(hint in t.lower() for hint in _ARTICLE_TYPE_HINTS)
        for t in types
    )


def _collect_article_bodies(node: object, out: list[str]) -> None:
    if isinstance(node, dict):
        body = node.get("articleBody")
        if isinstance(body, str) and body.strip():
            out.append(body)
        if _is_article_node(node):
            text = node.get("text")
            if isinstance(text, str) and text.strip():
                out.append(text)
        for value in node.values():
            _collect_article_bodies(value, out)
    elif isinstance(node, list):
        for item in node:
            _collect_article_bodies(item, out)


def jsonld_article_text(raw: str) -> str:
    """The longest article body declared in the page's JSON-LD, as plain text.

    Returns "" when the page publishes none. Bodies routinely carry inline markup
    and entities, so the winner goes back through `html_to_text`.
    """
    parser = _JsonLdBlocks()
    parser.feed(raw)
    parser.close()
    bodies: list[str] = []
    for block in parser.blocks:
        try:
            payload = json.loads(block)
        except ValueError:
            continue
        _collect_article_bodies(payload, bodies)
    if not bodies:
        return ""
    return html_to_text(max(bodies, key=len))


def html_article_text(raw: str) -> str:
    """Readable text for an article page, preferring the publisher's own JSON-LD.

    Publishers emit the full body in JSON-LD for search engines even when the
    rendered HTML carries only a teaser, so whichever of the two is longer wins.
    That is the same copy they hand every crawler — no access decision is being
    worked around, we were simply throwing it away by skipping <script>.
    """
    from_page = html_to_text(raw)
    from_jsonld = jsonld_article_text(raw)
    return from_jsonld if len(from_jsonld) > len(from_page) else from_page


def json_to_text(raw: str, path: Path) -> str:
    payload = json.loads(raw)
    rows = payload.get("response", {}).get("data")
    if not isinstance(rows, list):
        raise ValueError(f"unsupported JSON shape: {path}")
    row_lines: list[str] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        period = row.get("period") or row.get("date") or ""
        value = row.get("value")
        if period or value is not None:
            row_lines.append(f"{period}\t{value}")
    sections: list[str] = [f"Source: {path.name}"]
    batch_size = 350
    for start in range(0, len(row_lines), batch_size):
        block = row_lines[start : start + batch_size]
        if block:
            sections.append("\n".join(block))
    return "\n\n".join(sections)


def pdf_bytes_to_text(data: bytes, label: str = "<bytes>") -> str:
    """Extract text from a PDF already in memory (a fetched response body)."""
    from io import BytesIO

    from pypdf import PdfReader

    reader = PdfReader(BytesIO(data))
    pages = [p.extract_text() or "" for p in reader.pages]
    text = "\n\n".join(pages).strip()
    if not text:
        raise ValueError(f"no text extracted from PDF: {label}")
    return text


def pdf_to_text(path: Path) -> str:
    return pdf_bytes_to_text(path.read_bytes(), str(path))


def epub_to_text(path: Path) -> str:
    import ebooklib
    from ebooklib import epub

    book = epub.read_epub(str(path), options={"ignore_ncx": True})
    parts: list[str] = []
    seen: set[str] = set()

    for idref, _linear in book.spine:
        item = book.get_item_with_id(idref)
        if item is None or item.get_type() != ebooklib.ITEM_DOCUMENT:
            continue
        name = item.get_name() or idref
        if name in seen:
            continue
        seen.add(name)
        raw = item.get_content()
        if not raw:
            continue
        chapter = html_to_text(raw.decode("utf-8", errors="replace"))
        if chapter:
            parts.append(chapter)

    if not parts:
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            name = item.get_name() or item.get_id() or ""
            if name in seen:
                continue
            seen.add(name)
            raw = item.get_content()
            if not raw:
                continue
            chapter = html_to_text(raw.decode("utf-8", errors="replace"))
            if chapter:
                parts.append(chapter)

    text = "\n\n".join(parts).strip()
    if not text:
        raise ValueError(f"no text extracted from EPUB: {path}")
    return text


def detect_kind(raw_bytes: bytes, suffix: str) -> str:
    if suffix == ".epub":
        return "epub"
    head = raw_bytes[:16].lstrip()
    if head.startswith(b"%PDF"):
        return "pdf"
    if head.startswith((b"<!", b"<html", b"<HTML")):
        return "html"
    if suffix == ".json" or head.startswith((b"{", b"[")):
        return "json"
    if suffix == ".html":
        return "html"
    if suffix == ".pdf":
        return "pdf"
    if suffix == ".txt":
        return "txt"
    raise ValueError(f"unknown content kind for {suffix}")


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    raw_bytes = path.read_bytes()
    kind = detect_kind(raw_bytes, suffix)
    if kind == "pdf":
        return pdf_to_text(path)
    if kind == "epub":
        return epub_to_text(path)
    if kind == "html":
        return html_to_text(raw_bytes.decode("utf-8", errors="replace"))
    if kind == "json":
        return json_to_text(raw_bytes.decode("utf-8", errors="replace"), path)
    if kind == "txt":
        return raw_bytes.decode("utf-8", errors="replace")
    raise ValueError(f"unsupported file type: {path}")
