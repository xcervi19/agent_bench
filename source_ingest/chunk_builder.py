"""Parse OCR-style book text into paragraphs with page ranges, then pack chunks."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterator

PAGE_MARK = re.compile(r"^---\s*Page\s+(\d+)\s*---\s*$", re.IGNORECASE)
CHAPTER_LINE = re.compile(
    r"^(?P<h>chapter\s+(?:one|two|three|four|five|six|seven|eight|nine|ten|\d+|[ivxlcdm]+)\b[^\n]*)",
    re.IGNORECASE,
)
PART_LINE = re.compile(
    r"^(?P<h>part\s+(?:one|two|three|four|five|\d+)\b[^\n]*)",
    re.IGNORECASE,
)
TOC_LINE = re.compile(r"^table of contents\s*$", re.IGNORECASE)


@dataclass
class ParagraphSpan:
    page_start: int
    page_end: int
    text: str


@dataclass
class ChapterState:
    part: str | None = None
    chapter_raw: str | None = None


@dataclass
class PackedChunk:
    body: str
    page_start: int
    page_end: int
    content_zone: str
    part: str | None
    chapter_raw: str | None


def iter_paragraph_spans(raw: str) -> Iterator[ParagraphSpan]:
    current_page = 1
    buf_lines: list[str] = []
    buf_pages: list[int] = []

    def flush() -> Iterator[ParagraphSpan]:
        nonlocal buf_lines, buf_pages
        if not buf_lines:
            return
        text = "\n".join(buf_lines).strip()
        if text:
            yield ParagraphSpan(
                page_start=min(buf_pages),
                page_end=max(buf_pages),
                text=text,
            )
        buf_lines = []
        buf_pages = []

    for line in raw.split("\n"):
        stripped = line.strip()
        pm = PAGE_MARK.match(stripped)
        if pm:
            yield from flush()
            current_page = int(pm.group(1))
            continue
        if stripped == "":
            yield from flush()
            continue
        buf_lines.append(line)
        buf_pages.append(current_page)

    yield from flush()


def zone_for_paragraph(p: ParagraphSpan, seen_main_chapter: bool) -> str:
    t = p.text.lower()
    if TOC_LINE.match(p.text.strip()) or "table of contents" in t:
        return "toc"
    if not seen_main_chapter and (
        "does not constitute any offer" in t
        or "wooden table press" in t
        or ("copyright" in t and "2009" in t)
        or re.match(r"^ot:\s*101\s*$", p.text.strip(), re.I)
        or p.text.strip() in {"OIL 101", "Oil 101"}
    ):
        return "front_matter"
    st = p.text.strip().lower()
    if st == "references" or st == "bibliography" or st.startswith("index"):
        return "appendix"
    return "main"


def update_chapter_state(line: str, state: ChapterState) -> None:
    s = line.strip()
    pm = PART_LINE.match(s)
    if pm:
        state.part = pm.group("h").strip()[:200]
        return
    cm = CHAPTER_LINE.match(s)
    if cm:
        state.chapter_raw = cm.group("h").strip()[:300]


def pack_into_chunks(
    paragraphs: list[ParagraphSpan],
    *,
    max_chars: int,
    overlap_chars: int,
) -> list[PackedChunk]:
    state = ChapterState()
    seen_main_chapter = False

    buf: list[str] = []
    buf_pages: list[int] = []
    buf_zones: list[str] = []
    last_state = ChapterState()

    def snapshot_state() -> ChapterState:
        return ChapterState(part=state.part, chapter_raw=state.chapter_raw)

    out: list[PackedChunk] = []

    def flush() -> None:
        nonlocal buf, buf_pages, buf_zones, last_state
        if not buf:
            return
        body = "\n\n".join(buf).strip()
        if not body:
            buf = []
            buf_pages = []
            buf_zones = []
            return
        zone = buf_zones[-1]
        ps, pe = min(buf_pages), max(buf_pages)
        out.append(
            PackedChunk(
                body=body,
                page_start=ps,
                page_end=pe,
                content_zone=zone,
                part=last_state.part,
                chapter_raw=last_state.chapter_raw,
            )
        )
        if overlap_chars > 0 and len(body) > overlap_chars:
            tail = body[-overlap_chars:]
            dot = tail.find(". ")
            if dot != -1 and dot < len(tail) - 40:
                tail = tail[dot + 2 :]
            buf = [tail] if tail.strip() else []
            buf_pages = [pe]
            buf_zones = [zone]
        else:
            buf = []
            buf_pages = []
            buf_zones = []

    for p in paragraphs:
        first_line = p.text.strip().split("\n", 1)[0].strip()
        update_chapter_state(first_line, state)
        update_chapter_state(p.text, state)

        z = zone_for_paragraph(p, seen_main_chapter)
        if z == "main" and state.chapter_raw:
            seen_main_chapter = True

        last_state = snapshot_state()

        candidate_len = sum(len(x) + 2 for x in buf) + len(p.text)
        if buf and candidate_len > max_chars:
            flush()

        buf.append(p.text)
        buf_pages.extend([p.page_start, p.page_end])
        buf_zones.append(z)

    flush()
    return out


def build_embedding_prefix(
    *,
    book_title: str,
    author: str,
    part: str | None,
    chapter_raw: str | None,
    prefix_hint: str | None = None,
) -> str:
    bits: list[str] = []
    if prefix_hint:
        bits.append(prefix_hint.strip())
    bits.append(f"Source: {book_title}" + (f" ({author})" if author else ""))
    if part:
        bits.append(f"Part: {part}")
    if chapter_raw:
        bits.append(f"Chapter: {chapter_raw}")
    elif part:
        bits.append("Chapter: (unspecified)")
    return " | ".join(bits)
