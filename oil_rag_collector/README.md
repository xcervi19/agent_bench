# Oil RAG Collector

Standalone downloader for a **senior WTI/crude oil trader** knowledge base. Curates Tier 1–2 public sources (IEA, EIA, OPEC, CME, UNCTAD, terminals, geopolitics PDFs) and excludes broker marketing fluff from your notes.

## Business tiers

| Tier | What you get | RAG role |
|------|----------------|----------|
| **1** | IEA/EIA/OPEC/CME, FRED WTI, EIA API series, UNCTAD maritime, KPMG geopolitics | Ground truth for macro, inventories, contract mechanics |
| **2** | Academic PDFs, port/terminal manuals, OGIM, CFTC COT hub, JPM research landing | Infrastructure, logistics, positioning context |
| **3** | Optional deeper academic HTML | Lower priority; enable with `--max-tier 3` |

**Excluded by design:** Equiti/Vantage/MEXC-style blogs, YouTube, Scribd, Google book search links, paywalled ScienceDirect full text.

**Books:** `The Prize`, `Oil 101`, etc. are registry metadata only — ingest licensed text via `source_ingest.preprocess` (Oil 101 already in `local_knowledge_sources/oil101.txt`).

## Usage

From repo root:

```bash
uv run python -m oil_rag_collector --dry-run
uv run python -m oil_rag_collector --list
export EIA_API_KEY=your_key
uv run python -m oil_rag_collector -o artifacts/oil_rag_sources --max-tier 2
uv run python -m oil_rag_collector --skip-eia-api
```

Outputs:

- `artifacts/oil_rag_sources/sources_registry.json` — full consolidated catalog
- `artifacts/oil_rag_sources/tier_{n}/{domain}/` — raw PDF/HTML/JSON + `.meta.json` sidecars
- `artifacts/oil_rag_sources/collection_manifest.json` — run status per source

## Next step (RAG pipeline)

1. PDF → text (OCR/Textract) → `source_ingest.preprocess` or HTML stripper
2. `source_ingest.ingest` → Postgres + embeddings for `rag_adhoc`

Domain clusters match your schema notes: `market_price`, `supply_demand`, `infrastructure`, `geopolitics`, `maritime_logistics`, `trading_mechanics`.
