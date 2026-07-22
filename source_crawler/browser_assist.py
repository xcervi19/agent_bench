from __future__ import annotations

import logging
import re
import shutil
import time
import webbrowser
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from urllib.parse import unquote, urlparse

from .models import DocRef, DownloadedDoc, SourceConfig
from .store import content_path, sha256_hex, stored_sha256, write_doc

log = logging.getLogger(__name__)

PDF_MAGIC = b"%PDF"
MIN_BYTES = 1024

# Browser Content-Disposition names often differ from URL basename.
_TOKEN_CANON = {
    "america": "americas",
    "americas": "americas",
    "apac": "apag",
    "apag": "apag",
    "specification": "methodology",
    "specifications": "methodology",
    "specs": "methodology",
    "methodology": "methodology",
    "refined": "refined",
    "products": "products",
    "emea": "emea",
    "europe": "europe",
    "africa": "africa",
    "assessments": "assessments",
    "crude": "crude",
}


@dataclass(frozen=True)
class ImportResult:
    source_id: str
    status: Literal["imported", "unchanged", "unmatched", "invalid", "skipped"]
    path: str | None = None
    sha256: str | None = None
    reason: str | None = None
    matched_file: str | None = None


def url_basename(url: str) -> str:
    path = unquote(urlparse(url).path.rstrip("/"))
    name = path.rsplit("/", 1)[-1] or "document.pdf"
    if name.lower().endswith(".ashx"):
        name = name[: -len(".ashx")] + ".pdf"
    return name


def normalize_filename(name: str) -> str:
    stem = Path(name).name
    stem = re.sub(r"\s*\(\d+\)\s*", "", stem)  # file (1).pdf
    stem = re.sub(r"\s+copy\b", "", stem, flags=re.IGNORECASE)
    stem = stem.strip().lower()
    stem = stem.replace(" ", "_").replace("-", "_")
    stem = re.sub(r"_+", "_", stem)
    return stem


def expected_names(config: SourceConfig) -> list[str]:
    names = [
        url_basename(config.endpoint),
        f"{config.source_id}.pdf",
    ]
    aliases = config.extras.get("download_aliases") or []
    if isinstance(aliases, (list, tuple)):
        names.extend(str(a) for a in aliases)
    # unique preserve order
    out: list[str] = []
    seen: set[str] = set()
    for n in names:
        key = normalize_filename(n)
        if key not in seen:
            seen.add(key)
            out.append(n)
    return out


def _canon_tokens(name: str) -> set[str]:
    stem = normalize_filename(name).removesuffix(".pdf")
    # split apac-me / apac_me style compounds
    stem = stem.replace("-", "_")
    raw = [t for t in stem.split("_") if t and t not in {"the", "and", "pdf", "me"}]
    out: set[str] = set()
    for t in raw:
        out.add(_TOKEN_CANON.get(t, t))
        if t.startswith("apac"):
            out.add("apag")
    return out


def _config_tokens(config: SourceConfig) -> set[str]:
    tokens = _canon_tokens(config.source_id)
    tokens |= _canon_tokens(url_basename(config.endpoint))
    for alias in expected_names(config):
        tokens |= _canon_tokens(alias)
    # drop ultra-generic alone; kept for intersection scoring
    return tokens


def match_score(filename: str, config: SourceConfig) -> int:
    """Higher is better. 0 = no match."""
    norm = normalize_filename(filename)
    best = 0
    for expected in expected_names(config):
        exp = normalize_filename(expected)
        if norm == exp:
            best = max(best, 100)
        elif exp in norm or norm in exp:
            best = max(best, 80)

    file_toks = _canon_tokens(filename)
    cfg_toks = _config_tokens(config)
    if not file_toks or not cfg_toks:
        return best

    overlap = file_toks & cfg_toks
    # Distinctive anchors that disambiguate Platts guides
    anchors = {
        "americas",
        "emea",
        "apag",
        "assessments",
        "refined",
        "europe",
        "africa",
        "crude",
        "products",
        "methodology",
    }
    file_anchors = file_toks & anchors
    cfg_anchors = cfg_toks & anchors
    anchor_hit = file_anchors & cfg_anchors

    # Need a region/product anchor + crude/methodology/products signal
    regionish = {"americas", "emea", "apag", "europe", "africa", "assessments"}
    if not (anchor_hit & regionish) and "refined" not in anchor_hit:
        return best

    # Refined products must not steal crude-only files
    if "refined" in cfg_anchors and "refined" not in file_anchors:
        return best
    if "refined" in file_anchors and "refined" not in cfg_anchors:
        return best
    if "assessments" in cfg_anchors and "assessments" not in file_anchors:
        return best
    if "assessments" in file_anchors and "assessments" not in cfg_anchors:
        return best

    # Crude regional guides
    if "crude" in cfg_anchors and "crude" not in file_anchors and "refined" not in cfg_anchors:
        if "assessments" not in cfg_anchors:
            return best

    score = 50 + 10 * len(anchor_hit) + 5 * len(overlap)
    if "methodology" in overlap:
        score += 10
    best = max(best, min(score, 95))
    return best


def resolve_match(
    filename: str, configs: list[SourceConfig]
) -> tuple[SourceConfig | None, str | None]:
    scored = [(match_score(filename, c), c) for c in configs]
    scored = [(s, c) for s, c in scored if s > 0]
    if not scored:
        return None, "no filename match against seed catalog"
    scored.sort(key=lambda x: x[0], reverse=True)
    top_score, top = scored[0]
    ties = [c for s, c in scored if s == top_score]
    if len(ties) > 1:
        ids = ", ".join(c.source_id for c in ties)
        return None, f"ambiguous match ({ids})"
    if top_score < 60:
        return None, f"weak match score={top_score}"
    return top, None


def is_pdf_bytes(body: bytes) -> bool:
    return len(body) >= MIN_BYTES and body.startswith(PDF_MAGIC)


def missing_configs(collected_root: Path, configs: list[SourceConfig]) -> list[SourceConfig]:
    missing: list[SourceConfig] = []
    for cfg in configs:
        dest = content_path(collected_root, cfg, ".pdf")
        if not dest.is_file():
            missing.append(cfg)
    return missing


def write_save_guide(inbox: Path, configs: list[SourceConfig]) -> Path:
    inbox.mkdir(parents=True, exist_ok=True)
    html_path = inbox / "SAVE_THESE.html"
    rows: list[str] = []
    for i, cfg in enumerate(configs, start=1):
        names = ", ".join(f"<code>{n}</code>" for n in expected_names(cfg)[:2])
        rows.append(
            "<li>"
            f"<p><strong>{i}. {cfg.title or cfg.source_id}</strong></p>"
            f'<p><a href="{cfg.endpoint}" target="_blank" rel="noopener">'
            f"Open PDF</a></p>"
            f"<p>Save into this folder as {names}</p>"
            f"<p><small>source_id=<code>{cfg.source_id}</code></small></p>"
            "</li>"
        )
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>Source crawler — save these PDFs</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 720px; margin: 2rem auto; line-height: 1.4; }}
    code {{ background: #f2f2f2; padding: 0.1rem 0.3rem; }}
    li {{ margin: 1.2rem 0; padding-bottom: 1rem; border-bottom: 1px solid #ddd; }}
  </style>
</head>
<body>
  <h1>Save these PDFs</h1>
  <p>For each item: open the link (browser will pass Akamai), then save the file
  into <code>{inbox}</code> using the suggested name.</p>
  <p>Then run: <code>uv run python -m source_crawler import-local</code>
  (or keep <code>browser-fetch --watch</code> running).</p>
  <ol>
    {"".join(rows)}
  </ol>
</body>
</html>
"""
    html_path.write_text(html, encoding="utf-8")
    checklist = inbox / "CHECKLIST.md"
    lines = [
        "# Browser fetch checklist",
        "",
        f"Inbox: `{inbox}`",
        "",
        "1. Open `SAVE_THESE.html` in your browser.",
        "2. For each link: open → download/save into this inbox folder.",
        "3. Suggested filenames below (browser may add ` (1)` — that is OK).",
        "",
    ]
    for cfg in configs:
        lines.append(f"- [ ] `{cfg.source_id}` ← `{url_basename(cfg.endpoint)}`")
    lines.append("")
    checklist.write_text("\n".join(lines), encoding="utf-8")
    return html_path


def open_in_browser(path_or_url: str) -> None:
    webbrowser.open(path_or_url)


def iter_candidate_pdfs(dirs: list[Path]) -> list[Path]:
    files: list[Path] = []
    for d in dirs:
        if not d.is_dir():
            continue
        for path in d.iterdir():
            if not path.is_file():
                continue
            if path.name.startswith("."):
                continue
            if path.suffix.lower() != ".pdf":
                continue
            if path.parent.name in {".imported", ".invalid"}:
                continue
            files.append(path)
    # newest first helps when duplicates exist
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files


def _archive(path: Path, bucket: str) -> Path:
    dest_dir = path.parent / bucket
    dest_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = dest_dir / f"{path.stem}__{stamp}{path.suffix}"
    shutil.move(str(path), str(dest))
    return dest


def import_pdf_file(
    pdf_path: Path,
    collected_root: Path,
    configs: list[SourceConfig],
    *,
    archive: bool = True,
) -> ImportResult:
    body = pdf_path.read_bytes()
    if not is_pdf_bytes(body):
        if archive:
            _archive(pdf_path, ".invalid")
        return ImportResult(
            source_id="?",
            status="invalid",
            reason="not a PDF (missing %PDF magic or too small)",
            matched_file=str(pdf_path),
        )

    cfg, err = resolve_match(pdf_path.name, configs)
    if cfg is None:
        return ImportResult(
            source_id="?",
            status="unmatched",
            reason=err,
            matched_file=str(pdf_path),
        )

    digest = sha256_hex(body)
    prior = stored_sha256(collected_root, cfg, ".pdf")
    if prior == digest and content_path(collected_root, cfg, ".pdf").is_file():
        # still refresh sidecar labels from seed
        from .store import sync_sidecar

        sync_sidecar(
            collected_root,
            cfg,
            digest=digest,
            extension=".pdf",
            content_type="application/pdf",
        )
        if archive:
            _archive(pdf_path, ".imported")
        return ImportResult(
            source_id=cfg.source_id,
            status="unchanged",
            path=str(content_path(collected_root, cfg, ".pdf")),
            sha256=digest,
            matched_file=str(pdf_path),
        )

    dest = write_doc(
        collected_root,
        cfg,
        DownloadedDoc(
            ref=DocRef(url=cfg.endpoint, title=cfg.title, content_type="application/pdf"),
            body=body,
            content_type="application/pdf",
            extension=".pdf",
            meta={"import_source": str(pdf_path.name), "import_mode": "browser_assist"},
        ),
    )
    if archive:
        _archive(pdf_path, ".imported")
    log.info("imported %s ← %s", cfg.source_id, pdf_path.name)
    return ImportResult(
        source_id=cfg.source_id,
        status="imported",
        path=str(dest),
        sha256=digest,
        matched_file=str(pdf_path.name),
    )


def import_from_dirs(
    inbox_dirs: list[Path],
    collected_root: Path,
    configs: list[SourceConfig],
    *,
    only_missing: bool = True,
    archive: bool = True,
) -> list[ImportResult]:
    targets = missing_configs(collected_root, configs) if only_missing else list(configs)
    if not targets:
        return []
    target_ids = {c.source_id for c in targets}
    results: list[ImportResult] = []
    claimed: set[str] = set()

    for pdf in iter_candidate_pdfs(inbox_dirs):
        cfg, err = resolve_match(pdf.name, targets)
        if cfg is None:
            # only report unmatched for files that look seed-related
            if any(match_score(pdf.name, c) > 0 for c in configs):
                results.append(
                    ImportResult(
                        source_id="?",
                        status="unmatched",
                        reason=err,
                        matched_file=str(pdf),
                    )
                )
            continue
        if cfg.source_id in claimed:
            continue
        if cfg.source_id not in target_ids and only_missing:
            continue
        result = import_pdf_file(pdf, collected_root, [cfg], archive=archive)
        results.append(result)
        if result.status in {"imported", "unchanged"}:
            claimed.add(result.source_id)
    return results


def watch_import(
    inbox_dirs: list[Path],
    collected_root: Path,
    configs: list[SourceConfig],
    *,
    timeout_sec: float = 900.0,
    poll_sec: float = 2.0,
) -> list[ImportResult]:
    """Poll inbox until all missing configs are imported or timeout."""
    deadline = time.monotonic() + timeout_sec
    all_results: list[ImportResult] = []
    while time.monotonic() < deadline:
        missing = missing_configs(collected_root, configs)
        if not missing:
            log.info("all target sources present under %s", collected_root)
            break
        batch = import_from_dirs(
            inbox_dirs, collected_root, configs, only_missing=True, archive=True
        )
        all_results.extend(batch)
        still = missing_configs(collected_root, configs)
        log.info(
            "watch: missing=%s imported_this_tick=%s",
            [c.source_id for c in still],
            [r.source_id for r in batch if r.status == "imported"],
        )
        if not still:
            break
        time.sleep(poll_sec)
    return all_results
