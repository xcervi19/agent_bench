from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from .apply_qa import apply_qa
from .browser_assist import (
    import_from_dirs,
    missing_configs,
    open_in_browser,
    watch_import,
    write_save_guide,
)
from .extract import extract_all
from .pipeline_log import append_pipeline_step
from .promote import plan_promote, promote_all
from .qa_pack import qa_audit_path, sync_qa_after_extract
from .runner import crawl_many
from .seeds import (
    AGENCY_OIL_DATA_SOURCES,
    LNG_REPORT_SOURCES,
    PRICING_METHODOLOGY_SOURCES,
)

_SEED_CATALOGS = {
    "pricing_methodology": PRICING_METHODOLOGY_SOURCES,
    "lng_reports": LNG_REPORT_SOURCES,
    "agency_oil_data": AGENCY_OIL_DATA_SOURCES,
}
_SEED_CHOICES = tuple(_SEED_CATALOGS)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(name)s: %(message)s",
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _resolve(path: Path | None, default: Path) -> Path:
    root = path or default
    if not root.is_absolute():
        root = repo_root() / root
    return root


def _text_root_default() -> Path:
    return repo_root() / "artifacts" / "collected_text"


def _rag_corpus_default() -> Path:
    """Promoted KB root for RAG ingest (replaces legacy oil_rag_sources/)."""
    return repo_root() / "artifacts" / "rag_corpus"


def _inbox_default() -> Path:
    return repo_root() / "artifacts" / "download_inbox"


def _downloads_dir() -> Path:
    return Path.home() / "Downloads"


def _log_step(command: str, payload: dict, *, text_root: Path | None = None) -> None:
    append_pipeline_step(_resolve(text_root, _text_root_default()), command=command, payload=payload)


def _seed_configs(seed: str, source_ids: list[str]) -> list:
    catalog = _SEED_CATALOGS.get(seed)
    if catalog is None:
        raise SystemExit(f"unknown seed: {seed}")
    configs = list(catalog)
    if not source_ids:
        return configs
    want = set(source_ids)
    configs = [c for c in configs if c.source_id in want]
    missing = want - {c.source_id for c in configs}
    if missing:
        raise SystemExit(f"unknown source_id: {sorted(missing)}")
    return configs


def cmd_crawl(args: argparse.Namespace) -> None:
    configs = _seed_configs(args.seed, args.source_id)
    if args.dry_run:
        for c in configs:
            print(
                json.dumps(
                    {
                        "source_id": c.source_id,
                        "endpoint": c.endpoint,
                        "promote": c.promote,
                    }
                )
            )
        return

    root = _resolve(args.out, repo_root() / "artifacts" / "collected")
    root.mkdir(parents=True, exist_ok=True)
    results = crawl_many(configs, root)
    written = sum(1 for r in results if r.status == "written")
    unchanged = sum(1 for r in results if r.status == "unchanged")
    failed = sum(1 for r in results if r.status == "failed")
    for r in results:
        print(
            json.dumps(
                {
                    "source_id": r.source_id,
                    "status": r.status,
                    "path": r.path,
                    "sha256": r.sha256,
                    "reason": r.reason,
                }
            )
        )
    print(
        f"done written={written} unchanged={unchanged} failed={failed} out={root}"
    )
    _log_step(
        "crawl",
        {
            "written": written,
            "unchanged": unchanged,
            "failed": failed,
            "out": str(root),
            "failures": [
                {"source_id": r.source_id, "reason": r.reason}
                for r in results
                if r.status == "failed"
            ],
        },
    )
    if failed:
        raise SystemExit(1)


def cmd_extract(args: argparse.Namespace) -> None:
    collected = _resolve(args.collected, repo_root() / "artifacts" / "collected")
    text_root = _resolve(args.out, repo_root() / "artifacts" / "collected_text")
    source_ids = set(args.source_id) if args.source_id else None
    if args.dry_run:
        from .inventory import iter_content_files, load_sidecar

        for path in iter_content_files(collected):
            meta = load_sidecar(path)
            sid = meta.get("source_id")
            print(
                json.dumps(
                    {
                        "source_id": sid,
                        "path": str(path),
                        "selected": source_ids is None or sid in source_ids,
                    }
                )
            )
        return

    text_root.mkdir(parents=True, exist_ok=True)
    results = extract_all(collected, text_root, source_ids=source_ids)
    written = sum(1 for r in results if r.status == "written")
    unchanged = sum(1 for r in results if r.status == "unchanged")
    skipped = sum(1 for r in results if r.status == "skipped")
    for r in results:
        print(
            json.dumps(
                {
                    "source_id": r.source_id,
                    "status": r.status,
                    "path": r.path,
                    "reason": r.reason,
                }
            )
        )
    print(
        f"done written={written} unchanged={unchanged} skipped={skipped} out={text_root}"
    )
    print(f"qa_prompt={text_root / 'qa_prompt.md'}")
    _log_step(
        "extract",
        {"written": written, "unchanged": unchanged, "skipped": skipped},
        text_root=text_root,
    )


def cmd_qa_pack(args: argparse.Namespace) -> None:
    text_root = _resolve(args.text_root, _text_root_default())
    results = sync_qa_after_extract(text_root)
    written = sum(1 for r in results if r.status == "written")
    unchanged = sum(1 for r in results if r.status == "unchanged")
    for r in results:
        print(json.dumps({"source_id": r.source_id, "status": r.status}))
    print(f"done written={written} unchanged={unchanged} qa_prompt={text_root / 'qa_prompt.md'}")
    _log_step(
        "qa-pack",
        {"written": written, "unchanged": unchanged},
        text_root=text_root,
    )


def cmd_apply_qa(args: argparse.Namespace) -> None:
    collected = _resolve(args.collected, repo_root() / "artifacts" / "collected")
    text_root = _resolve(args.text_root, _text_root_default())
    kb = _resolve(args.kb, _rag_corpus_default())
    audit = _resolve(args.audit, qa_audit_path(text_root))
    results = apply_qa(
        audit,
        collected,
        kb,
        text_root,
        dry_run=args.dry_run,
    )
    promoted = sum(1 for r in results if r.status == "promoted")
    planned = sum(1 for r in results if r.status == "planned")
    blocked = sum(1 for r in results if r.status == "blocked")
    for r in results:
        print(
            json.dumps(
                {
                    "source_id": r.source_id,
                    "status": r.status,
                    "path": r.path,
                    "reason": r.reason,
                }
            )
        )
    print(
        f"done promoted={promoted} planned={planned} blocked={blocked} "
        f"audit={audit} dry_run={args.dry_run}"
    )
    _log_step(
        "apply-qa",
        {"promoted": promoted, "planned": planned, "blocked": blocked, "dry_run": args.dry_run},
        text_root=text_root,
    )


def cmd_browser_fetch(args: argparse.Namespace) -> None:
    """Semi-auto: open save guide, watch inbox/Downloads, import into collected/."""
    configs = _seed_configs(args.seed, args.source_id)
    collected = _resolve(args.out, repo_root() / "artifacts" / "collected")
    inbox = _resolve(args.inbox, _inbox_default())
    collected.mkdir(parents=True, exist_ok=True)
    inbox.mkdir(parents=True, exist_ok=True)

    targets = missing_configs(collected, configs)
    if args.all:
        targets = list(configs)
    if not targets:
        print("nothing missing — all seed PDFs already in collected/")
        return

    guide = write_save_guide(inbox, targets)
    print(f"missing={len(targets)} inbox={inbox}")
    for cfg in targets:
        print(json.dumps({"source_id": cfg.source_id, "endpoint": cfg.endpoint}))
    print(f"guide={guide}")

    if not args.no_open:
        open_in_browser(guide.resolve().as_uri())
        if args.open_pdfs:
            for cfg in targets:
                open_in_browser(cfg.endpoint)

    scan_dirs = [inbox]
    if not args.no_downloads:
        scan_dirs.append(_downloads_dir())

    if args.dry_run:
        print(json.dumps({"would_watch": [str(p) for p in scan_dirs], "targets": [c.source_id for c in targets]}))
        return

    if args.once:
        results = import_from_dirs(scan_dirs, collected, targets, only_missing=True)
    else:
        print(
            f"watching {scan_dirs} for up to {args.timeout}s — "
            "save each PDF (inbox or ~/Downloads); names may match URL basename"
        )
        results = watch_import(
            scan_dirs,
            collected,
            targets,
            timeout_sec=float(args.timeout),
            poll_sec=float(args.poll),
        )

    imported = sum(1 for r in results if r.status == "imported")
    unchanged = sum(1 for r in results if r.status == "unchanged")
    for r in results:
        print(
            json.dumps(
                {
                    "source_id": r.source_id,
                    "status": r.status,
                    "path": r.path,
                    "sha256": r.sha256,
                    "reason": r.reason,
                    "matched_file": r.matched_file,
                }
            )
        )
    still = [c.source_id for c in missing_configs(collected, targets)]
    print(
        f"done imported={imported} unchanged={unchanged} "
        f"still_missing={still} collected={collected}"
    )
    _log_step(
        "browser-fetch",
        {
            "imported": imported,
            "unchanged": unchanged,
            "still_missing": still,
            "inbox": str(inbox),
        },
    )

    if args.extract and not still:
        extract_args = argparse.Namespace(
            collected=collected,
            out=_text_root_default(),
            source_id=[c.source_id for c in targets],
            dry_run=False,
        )
        cmd_extract(extract_args)

    if still:
        raise SystemExit(1)


def cmd_import_local(args: argparse.Namespace) -> None:
    configs = _seed_configs(args.seed, args.source_id)
    collected = _resolve(args.out, repo_root() / "artifacts" / "collected")
    inbox = _resolve(args.inbox, _inbox_default())
    scan_dirs = [inbox]
    if not args.no_downloads:
        scan_dirs.append(_downloads_dir())
    if args.path:
        scan_dirs.insert(0, _resolve(args.path, inbox))

    results = import_from_dirs(
        scan_dirs,
        collected,
        configs,
        only_missing=not args.all,
        archive=not args.keep,
    )
    for r in results:
        print(
            json.dumps(
                {
                    "source_id": r.source_id,
                    "status": r.status,
                    "path": r.path,
                    "sha256": r.sha256,
                    "reason": r.reason,
                    "matched_file": r.matched_file,
                }
            )
        )
    imported = sum(1 for r in results if r.status == "imported")
    print(f"done imported={imported} scanned={[str(p) for p in scan_dirs]}")
    _log_step("import-local", {"imported": imported, "scanned": [str(p) for p in scan_dirs]})


def cmd_promote(args: argparse.Namespace) -> None:
    collected = _resolve(args.collected, repo_root() / "artifacts" / "collected")
    kb = _resolve(args.kb, _rag_corpus_default())
    source_ids = set(args.source_id) if args.source_id else None
    if args.dry_run:
        for row in plan_promote(collected, source_ids=source_ids):
            print(json.dumps(row))
        return

    kb.mkdir(parents=True, exist_ok=True)
    results = promote_all(collected, kb, source_ids=source_ids)
    promoted = sum(1 for r in results if r.status == "promoted")
    unchanged = sum(1 for r in results if r.status == "unchanged")
    skipped = sum(1 for r in results if r.status == "skipped")
    for r in results:
        print(
            json.dumps(
                {
                    "source_id": r.source_id,
                    "status": r.status,
                    "path": r.path,
                    "reason": r.reason,
                }
            )
        )
    print(
        f"done promoted={promoted} unchanged={unchanged} skipped={skipped} kb={kb}"
    )
    _log_step(
        "promote",
        {"promoted": promoted, "unchanged": unchanged, "skipped": skipped, "kb": str(kb)},
    )


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description="Source crawler: crawl, extract, promote.")
    sub = ap.add_subparsers(dest="command", required=True)

    crawl_p = sub.add_parser("crawl", help="Download enrolled sources into collected/")
    crawl_p.add_argument("--seed", choices=_SEED_CHOICES, default="pricing_methodology")
    crawl_p.add_argument("--out", type=Path, default=None)
    crawl_p.add_argument("--source-id", action="append", default=[])
    crawl_p.add_argument("--dry-run", action="store_true")
    crawl_p.set_defaults(func=cmd_crawl)

    bf = sub.add_parser(
        "browser-fetch",
        help="Semi-auto Platts/Akamai: open save guide, watch inbox, import to collected/",
    )
    bf.add_argument("--seed", choices=_SEED_CHOICES, default="pricing_methodology")
    bf.add_argument("--source-id", action="append", default=[])
    bf.add_argument("--out", type=Path, default=None, help="collected/ root")
    bf.add_argument("--inbox", type=Path, default=None, help="default artifacts/download_inbox")
    bf.add_argument(
        "--once",
        action="store_true",
        help="import once and exit (default is watch until complete/timeout)",
    )
    bf.add_argument("--timeout", type=float, default=900.0)
    bf.add_argument("--poll", type=float, default=2.0)
    bf.add_argument("--no-open", action="store_true", help="do not open browser guide")
    bf.add_argument("--open-pdfs", action="store_true", help="also open each PDF URL tab")
    bf.add_argument("--no-downloads", action="store_true", help="do not scan ~/Downloads")
    bf.add_argument("--all", action="store_true", help="include sources already present")
    bf.add_argument("--extract", action="store_true", help="run extract when all imported")
    bf.add_argument("--dry-run", action="store_true")
    bf.set_defaults(func=cmd_browser_fetch)

    imp = sub.add_parser(
        "import-local",
        help="Import PDFs from inbox/Downloads into collected/ (match by filename)",
    )
    imp.add_argument("--seed", choices=_SEED_CHOICES, default="pricing_methodology")
    imp.add_argument("--source-id", action="append", default=[])
    imp.add_argument("--out", type=Path, default=None)
    imp.add_argument("--inbox", type=Path, default=None)
    imp.add_argument("--path", type=Path, default=None, help="extra directory to scan")
    imp.add_argument("--no-downloads", action="store_true")
    imp.add_argument("--all", action="store_true", help="allow replace/update existing")
    imp.add_argument("--keep", action="store_true", help="do not move files to .imported/")
    imp.set_defaults(func=cmd_import_local)

    extract_p = sub.add_parser(
        "extract",
        help="Transform collected/ raw files into collected_text/ plain text",
    )
    extract_p.add_argument("--collected", type=Path, default=None)
    extract_p.add_argument("--out", type=Path, default=None)
    extract_p.add_argument("--source-id", action="append", default=[])
    extract_p.add_argument("--dry-run", action="store_true")
    extract_p.set_defaults(func=cmd_extract)

    qa_p = sub.add_parser(
        "qa-pack",
        help="Rebuild qa_pack.json + qa_prompt.md from collected_text/",
    )
    qa_p.add_argument("--text-root", type=Path, default=None)
    qa_p.set_defaults(func=cmd_qa_pack)

    apply_p = sub.add_parser(
        "apply-qa",
        help="Promote sources listed in qa_audit.json (PASS + matching source_sha256)",
    )
    apply_p.add_argument("--audit", type=Path, default=None)
    apply_p.add_argument("--collected", type=Path, default=None)
    apply_p.add_argument("--text-root", type=Path, default=None)
    apply_p.add_argument("--kb", type=Path, default=None)
    apply_p.add_argument("--dry-run", action="store_true")
    apply_p.set_defaults(func=cmd_apply_qa)

    promote_p = sub.add_parser(
        "promote",
        help="Copy collected docs into rag_corpus/ (use apply-qa in normal flow)",
    )
    promote_p.add_argument("--collected", type=Path, default=None)
    promote_p.add_argument("--kb", type=Path, default=None)
    promote_p.add_argument(
        "--source-id",
        action="append",
        default=[],
        help="Force-promote these source_ids (manual override; normal path is apply-qa).",
    )
    promote_p.add_argument("--dry-run", action="store_true")
    promote_p.set_defaults(func=cmd_promote)

    args = ap.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
