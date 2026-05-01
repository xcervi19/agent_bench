"""CLI: chunks.jsonl + manifest.json → embed + Postgres documents/events."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from uuid import UUID, uuid4

# Repo root on path
_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))
if str(_REPO / "libs") not in sys.path:
    sys.path.insert(0, str(_REPO / "libs"))


def main() -> None:
    ap = argparse.ArgumentParser(description="Load chunk JSONL into DB with embeddings.")
    ap.add_argument("--artifact-dir", "-a", type=Path, required=True, help="Dir with manifest.json + chunks.jsonl")
    ap.add_argument(
        "--tenant-id",
        "-t",
        type=UUID,
        required=True,
        help="Must match X-Tenant-Id used by rag_adhoc search",
    )
    ap.add_argument("--dry-run", action="store_true", help="Parse + embed count only; no DB writes")
    args = ap.parse_args()

    artifact_dir = args.artifact_dir
    if not artifact_dir.is_absolute():
        artifact_dir = _REPO / artifact_dir

    manifest_path = artifact_dir / "manifest.json"
    chunks_path = artifact_dir / "chunks.jsonl"
    if not manifest_path.is_file() or not chunks_path.is_file():
        raise SystemExit(f"Missing manifest.json or chunks.jsonl under {artifact_dir}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    document_id = UUID(manifest["document_id"])
    book = manifest["book"]
    filters = manifest["filters"]

    lines = chunks_path.read_text(encoding="utf-8").strip().splitlines()
    artifacts = [json.loads(line) for line in lines if line.strip()]

    from source_ingest.env_bootstrap import bootstrap_for_ingest

    bootstrap_for_ingest(_REPO)

    from apps.signal_gather.models import Document, Event
    from apps.signal_gather.services.embeddings import EMBED_DIM, embed
    from agentic_core.database import session_scope, tenant_scope

    async def run() -> None:
        # Document embedding: title + start of first chunk for optional doc-level vector
        first_summary = ""
        if artifacts:
            a0 = artifacts[0]
            first_summary = f"{a0['prefix']}\n\n{a0['body']}"[:2000]
        doc_emb = embed(first_summary) if first_summary else None

        if args.dry_run:
            n = 0
            for art in artifacts:
                s = f"{art['prefix']}\n\n{art['body']}".strip()
                v = embed(s)
                if v is None:
                    raise SystemExit("embed() returned None — check OPENAI_API_KEY")
                if len(v) != EMBED_DIM:
                    raise SystemExit(f"Expected dim {EMBED_DIM}, got {len(v)}")
                n += 1
            print(f"Dry-run OK: {n} chunks embedded; no DB writes.")
            return

        s3_key = f"local:{book['book_slug']}:{document_id}"
        norm_path = artifact_dir / "normalized.txt"
        doc_content = norm_path.read_text(encoding="utf-8") if norm_path.is_file() else None

        with tenant_scope(args.tenant_id):
            async with session_scope() as db:
                doc = Document(
                    id=document_id,
                    tenant_id=args.tenant_id,
                    source="book",
                    url=None,
                    title=book["title"][:512],
                    language=book.get("language"),
                    s3_key=s3_key[:1024],
                    content=doc_content,
                    embedding=doc_emb,
                )
                db.add(doc)
                await db.flush()

        batch_size = 40
        for start in range(0, len(artifacts), batch_size):
            batch = artifacts[start : start + batch_size]
            with tenant_scope(args.tenant_id):
                async with session_scope() as db:
                    for art in batch:
                        summary = f"{art['prefix']}\n\n{art['body']}".strip()
                        vec = embed(summary)
                        loc = art["location"]
                        ent = {
                            "schema_version": art.get("schema_version", 1),
                            "book": art["book"],
                            "location": loc,
                            "content_zone": art["content_zone"],
                            "chunk_index": art["chunk_index"],
                            "chunk_total": art["chunk_total"],
                            "filters": art["filters"],
                            **art.get("entities_extra", {}),
                            "embedding_model": manifest.get("embedding_model", "text-embedding-3-small"),
                        }
                        ev = Event(
                            id=uuid4(),
                            tenant_id=args.tenant_id,
                            document_id=document_id,
                            category=art["filters"]["category"][:64],
                            commodity=(art["filters"].get("commodity") or None),
                            region=(art["filters"].get("region") or None),
                            occurred_at=None,
                            summary=summary,
                            entities=ent,
                            impact_score=None,
                            embedding=vec,
                        )
                        db.add(ev)
                    await db.flush()

        print(f"Ingested document {document_id} with {len(artifacts)} events.")

    asyncio.run(run())


if __name__ == "__main__":
    main()
