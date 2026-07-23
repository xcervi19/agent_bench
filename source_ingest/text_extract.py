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


def pdf_to_text(path: Path) -> str:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    pages = [p.extract_text() or "" for p in reader.pages]
    text = "\n\n".join(pages).strip()
    if not text:
        raise ValueError(f"no text extracted from PDF: {path}")
    return text


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
