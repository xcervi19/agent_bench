from __future__ import annotations

from pathlib import Path

from source_crawler.browser_assist import (
    expected_names,
    import_from_dirs,
    match_score,
    missing_configs,
    normalize_filename,
    resolve_match,
    write_save_guide,
)
from source_crawler.models import SourceConfig
from source_crawler.store import content_path


def _cfg(source_id: str, endpoint: str) -> SourceConfig:
    return SourceConfig(
        source_id=source_id,
        adapter="static_pdf",
        endpoint=endpoint,
        title=source_id,
        label_assignment="human",
        document_type="methodology",
        use_for=("pricing_context",),
    )


PLATTS = _cfg(
    "platts_americas_crude_methodology",
    "https://www.spglobal.com/x/americas-crude-methodology.pdf",
)
OTHER = _cfg(
    "platts_emea_crude_methodology",
    "https://www.spglobal.com/x/emea-crude-methodology.pdf",
)


def test_normalize_strips_duplicate_suffix():
    assert normalize_filename("americas-crude-methodology (1).pdf") == (
        "americas_crude_methodology.pdf"
    )


def test_resolve_match_unique():
    cfg, err = resolve_match("americas-crude-methodology.pdf", [PLATTS, OTHER])
    assert err is None
    assert cfg is not None
    assert cfg.source_id == "platts_americas_crude_methodology"


def test_resolve_match_ambiguous_blocked():
    twin = _cfg(
        "platts_americas_crude_methodology_copy",
        "https://example.com/americas-crude-methodology.pdf",
    )
    cfg, err = resolve_match("americas-crude-methodology.pdf", [PLATTS, twin])
    assert cfg is None
    assert err and "ambiguous" in err


def test_import_writes_collected_layout(tmp_path: Path):
    inbox = tmp_path / "inbox"
    collected = tmp_path / "collected"
    inbox.mkdir()
    body = b"%PDF-1.4\n" + b"x" * 2048
    (inbox / "americas-crude-methodology.pdf").write_bytes(body)

    results = import_from_dirs([inbox], collected, [PLATTS, OTHER], only_missing=True)
    assert results[0].status == "imported"
    dest = content_path(collected, PLATTS, ".pdf")
    assert dest.is_file()
    assert dest.read_bytes() == body
    meta = dest.with_suffix(".pdf.meta.json")
    assert meta.is_file()
    text = meta.read_text(encoding="utf-8")
    assert "platts_americas_crude_methodology" in text
    assert "pricing_context" in text
    # archived
    assert list((inbox / ".imported").glob("*.pdf"))


def test_missing_and_guide(tmp_path: Path):
    collected = tmp_path / "collected"
    collected.mkdir()
    missing = missing_configs(collected, [PLATTS])
    assert [c.source_id for c in missing] == [PLATTS.source_id]
    guide = write_save_guide(tmp_path / "inbox", missing)
    assert guide.is_file()
    body = guide.read_text(encoding="utf-8")
    assert PLATTS.endpoint in body
    assert "americas-crude-methodology.pdf" in expected_names(PLATTS)


def test_match_score_source_id():
    assert match_score("platts_americas_crude_methodology.pdf", PLATTS) >= 70


def test_match_browser_content_disposition_names():
    """S&P often saves as *-specifications.pdf, not URL *-methodology.pdf."""
    from source_crawler.seeds import PRICING_METHODOLOGY_SOURCES

    platts = [c for c in PRICING_METHODOLOGY_SOURCES if c.source_id.startswith("platts_")]
    cases = {
        "america-crude-specifications.pdf": "platts_americas_crude_methodology",
        "emea-crude-specifications (1).pdf": "platts_emea_crude_methodology",
        "apac-me-crude-specifications.pdf": "platts_apag_crude_methodology",
        "refined-products-europe-africa-specifications.pdf": (
            "platts_europe_africa_refined_methodology"
        ),
    }
    for name, expect in cases.items():
        cfg, err = resolve_match(name, platts)
        assert err is None, name
        assert cfg is not None and cfg.source_id == expect
