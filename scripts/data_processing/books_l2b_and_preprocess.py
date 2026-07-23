#!/usr/bin/env python3
"""Light L2b clean + preprocess for licensed books (book RAG metadata)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from source_ingest.preprocess_core import write_preprocess_artifacts
from source_ingest.schemas import BookMeta, ChunkFilters

BOOKS: list[dict] = [
    {
        "slug": "oil_trading_manual",
        "l2": "L2_text/licensed_books/david_long_-_oil_trading_manual__a_comprehensive_guide_to_the_oil_markets_2003_woodhead_publishing_-.txt",
        "title": "Oil Trading Manual",
        "author": "David Long",
        "commodity": "crude_oil",
        "use_for": ["trading_mechanics", "playbook_authoring"],
        "prefix_hint": "Physical + paper oil trading instruments and ops",
    },
    {
        "slug": "energy_trading_investing",
        "l2": "L2_text/licensed_books/davis_edwards_-_energy_trading_investing__trading_risk_management_and_structuring_deals_in_the_energ.txt",
        "title": "Energy Trading & Investing",
        "author": "Davis Edwards",
        "commodity": "multi",
        "use_for": ["trading_mechanics"],
        "prefix_hint": "Energy markets: futures, risk, structuring — not news",
    },
    {
        "slug": "world_for_sale",
        "l2": "L2_text/licensed_books/farchy_jack__blas_javier_-_the_world_for_sale_2021_random_house_-_libgen_li.txt",
        "title": "The World for Sale",
        "author": "Javier Blas, Jack Farchy",
        "commodity": "multi",
        "use_for": ["geopolitics_context", "playbook_authoring"],
        "prefix_hint": "Commodity trading houses history; narrative context",
    },
    {
        "slug": "the_prize",
        "l2": "L2_text/licensed_books/yergin_daniel_-_the_prize__the_epic_quest_for_oil_money_power_2014_free_press_-_libgen_li.txt",
        "title": "The Prize",
        "author": "Daniel Yergin",
        "commodity": "crude_oil",
        "use_for": ["geopolitics_context"],
        "prefix_hint": "Oil geopolitics history; not live signals",
    },
    {
        "slug": "the_new_map",
        "l2": "L2_text/licensed_books/the_new_map_daniel_yergin_2024_114977914_libgen_li.txt",
        "title": "The New Map",
        "author": "Daniel Yergin",
        "commodity": "multi",
        "use_for": ["geopolitics_context"],
        "prefix_hint": "Modern energy geopolitics (shale, LNG, China/RU)",
    },
    {
        "slug": "oil_trader_academy",
        "l2": "L2_text/licensed_books/oil_trader_academy.txt",
        "title": "Oil Trader Academy",
        "author": "Oil Trader Academy",
        "commodity": "crude_oil",
        "use_for": ["trading_mechanics"],
        "prefix_hint": "Training course material",
    },
    {
        "slug": "classic_crude_oil_trades",
        "l2": "L2_text/licensed_books/40_classic_crude_oil_trades__real-life_examples_of_--_owain_johnson_taylor_francis_group_--_routledg.txt",
        "title": "40 Classic Crude Oil Trades",
        "author": "Owain Johnson",
        "commodity": "crude_oil",
        "use_for": ["trading_mechanics", "playbook_authoring"],
        "prefix_hint": "Historical trade case studies; not current market data",
    },
]

HEADER_SPLIT = re.compile(r"\n---\n\n", re.MULTILINE)
TOC_START = re.compile(r"(?im)^(table of contents|contents)\s*$")
APPENDIX_START = re.compile(
    r"(?im)^(bibliography|references|index|notes and references)\s*$"
)
PAGE_ONLY = re.compile(r"^\s*\d{1,4}\s*$")


def split_header_body(raw: str) -> tuple[str, str]:
    parts = HEADER_SPLIT.split(raw, maxsplit=1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1]
    return "", raw


def light_clean(body: str) -> tuple[str, list[str]]:
    notes: list[str] = []
    text = body.replace("\ufeff", "").replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")

    # Drop leading short copyright/ISBN-only blocks (first ~80 lines heuristic).
    start = 0
    for i, line in enumerate(lines[:80]):
        low = line.strip().lower()
        if low.startswith("chapter ") or low.startswith("part "):
            start = i
            notes.append(f"trimmed_front_to_line_{i}")
            break
    lines = lines[start:]

    # Cut trailing bibliography/index if present in last 15% of file.
    cut_at = None
    n = len(lines)
    search_from = int(n * 0.85)
    for i in range(search_from, n):
        if APPENDIX_START.match(lines[i].strip()):
            cut_at = i
            notes.append(f"cut_appendix_at_line_{i}")
            break
    if cut_at is not None:
        lines = lines[:cut_at]

    # Remove isolated page-number lines.
    cleaned: list[str] = []
    removed_pages = 0
    for line in lines:
        if PAGE_ONLY.match(line):
            removed_pages += 1
            continue
        cleaned.append(line)
    if removed_pages:
        notes.append(f"removed_page_number_lines_{removed_pages}")

    text = "\n".join(cleaned)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text, notes


def write_l2b(corpus: Path, book: dict) -> Path:
    l2_path = corpus / book["l2"]
    if not l2_path.is_file():
        raise FileNotFoundError(l2_path)
    raw = l2_path.read_text(encoding="utf-8", errors="replace")
    header, body = split_header_body(raw)
    cleaned, notes = light_clean(body)

    rel = Path(book["l2"]).relative_to("L2_text")
    out = corpus / "L2b_clean" / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    header_lines = [
        f"source_id: {book['slug']}",
        "bucket: licensed_books",
        f"l1_path: (from {book['l2']})",
        "publisher: local",
        "domain: desk",
        f"book_title: {book['title']}",
        f"author: {book['author']}",
    ]
    if header:
        # keep original header as comment block
        pass
    out.write_text("\n".join(header_lines) + "\n\n---\n\n" + cleaned + "\n", encoding="utf-8")

    prov_path = corpus / "L2b_provenance" / f"{rel.as_posix()}.provenance.json"
    prov_path.parent.mkdir(parents=True, exist_ok=True)
    prov = {
        "schema_version": 1,
        "reproducible": False,
        "source_l2": book["l2"],
        "output_l2b": f"L2b_clean/{rel.as_posix()}",
        "book_slug": book["slug"],
        "method": "agent_light_clean",
        "notes": notes,
        "figures": [],
        "l2_chars": len(body),
        "l2b_chars": len(cleaned),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    prov_path.write_text(json.dumps(prov, indent=2), encoding="utf-8")
    return out


def preprocess_book(l2b_path: Path, book: dict, out_root: Path) -> tuple[str, int]:
    # Body after ---
    raw = l2b_path.read_text(encoding="utf-8", errors="replace")
    _, body = split_header_body(raw)
    out_dir = out_root / book["slug"]
    filters = ChunkFilters(
        category="energy_education",
        commodity=book["commodity"],
        region=None,
        document_type="book",
        use_for=list(book["use_for"]),
    )
    meta = BookMeta(
        title=book["title"],
        author=book["author"],
        book_slug=book["slug"],
        language="en",
    )
    doc_id, n = write_preprocess_artifacts(
        raw_text=body,
        output_dir=out_dir,
        book=meta,
        filters=filters,
        source_path=str(l2b_path.resolve()),
        pipeline="source_ingest.preprocess",
        max_chars=1100,
        overlap_chars=160,
        prefix_hint=book["prefix_hint"],
        main_zone_only=True,
    )
    return str(doc_id), n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus-dir", type=Path, default=REPO / "corpus")
    ap.add_argument("--out-root", type=Path, default=REPO / "artifacts" / "books")
    ap.add_argument("--slug", action="append", default=[])
    ap.add_argument("--skip-preprocess", action="store_true")
    args = ap.parse_args()

    corpus = args.corpus_dir if args.corpus_dir.is_absolute() else REPO / args.corpus_dir
    out_root = args.out_root if args.out_root.is_absolute() else REPO / args.out_root
    selected = [b for b in BOOKS if not args.slug or b["slug"] in args.slug]

    state_path = corpus / "L2b_run_state.json"
    completed: list[str] = []
    for book in selected:
        l2b = write_l2b(corpus, book)
        print(f"l2b {book['slug']} → {l2b.relative_to(corpus)} chars={l2b.stat().st_size}")
        completed.append(book["l2"])
        if args.skip_preprocess:
            continue
        doc_id, n = preprocess_book(l2b, book, out_root)
        print(f"preprocess {book['slug']} chunks={n} document_id={doc_id}")

    state = {
        "schema_version": 1,
        "current_batch": {
            "start": selected[0]["l2"] if selected else None,
            "end": selected[-1]["l2"] if selected else None,
            "status": "done",
            "note": "books_l2b_and_preprocess agent run",
        },
        "completed": completed,
        "last_completed": completed[-1] if completed else None,
        "last_updated": datetime.now(timezone.utc).isoformat(),
    }
    state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
    print(f"done books={len(selected)}")


if __name__ == "__main__":
    main()
