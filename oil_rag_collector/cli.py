from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .collector import run_collection
from .registry import export_registry_json, sources_for_download


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser(
        description="Download curated oil/WTI RAG sources (tiered, senior-trader quality filter).",
    )
    ap.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        default=repo_root / "artifacts" / "oil_rag_sources",
        help="Where raw files and manifests are written",
    )
    ap.add_argument(
        "--max-tier",
        type=int,
        default=2,
        choices=[1, 2, 3],
        help="1=IEA/EIA/OPEC/CME/UNCTAD/KPMG only; 2=add academic/terminals; 3=all enabled",
    )
    ap.add_argument("--timeout", type=float, default=90.0)
    ap.add_argument(
        "--skip-eia-api",
        action="store_true",
        help="Skip EIA v2 series (no EIA_API_KEY needed)",
    )
    ap.add_argument(
        "--list",
        action="store_true",
        help="Print registry and exit",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="List sources that would be fetched",
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any source failed (default: exit 1 only when zero downloads succeeded)",
    )
    args = ap.parse_args()

    if args.list:
        print(json.dumps(export_registry_json(), indent=2))
        return

    specs = sources_for_download(max_tier=args.max_tier)
    if args.dry_run:
        for s in specs:
            print(f"tier={s.tier} fetch={s.fetch} id={s.id} url={s.url}")
        print(f"Total: {len(specs)} sources (max_tier={args.max_tier})")
        return

    out_dir = args.output_dir
    if not out_dir.is_absolute():
        out_dir = repo_root / out_dir

    manifest = run_collection(
        out_dir,
        max_tier=args.max_tier,
        timeout_sec=args.timeout,
        skip_eia_api=args.skip_eia_api,
    )
    stats = manifest.to_dict()["stats"]
    print(f"Done → {out_dir}")
    print(f"ok={stats['ok']} skipped={stats['skipped']} failed={stats['failed']}")
    if stats["failed"]:
        for o in manifest.outcomes:
            if o.status == "failed":
                print(f"  FAIL {o.source_id}: {o.error}", file=sys.stderr)
    if stats["ok"] == 0:
        raise SystemExit(1)
    if args.strict and stats["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
