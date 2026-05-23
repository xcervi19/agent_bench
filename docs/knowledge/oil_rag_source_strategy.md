# Oil / WTI RAG — Source Strategy (Senior Trader)

## Product goal

Give agents **ground-truth macro + physical logistics + geopolitical risk** for WTI decisions—not generic “how to trade oil” SEO content.

## Four domain clusters (ingest metadata)

| Cluster | Examples | Trader use |
|---------|----------|------------|
| `market_price` | FRED WTI, EIA prices, CME specs, COT | Timing, vol, positioning |
| `supply_demand` | IEA OMR, OPEC MOMR, EIA WPSR/STEO, country briefs | Inventory builds, Call on OPEC |
| `infrastructure` | Terminals, OGIM, pipelines | Bottlenecks, arb windows |
| `geopolitics` | KPMG, MDPI, GDELT hub, JPM landing | Risk premium narratives |
| `maritime_logistics` | UNCTAD, tanker theses | VLCC flows, chokepoints |
| `trading_mechanics` | CME/INE handbooks | Delivery, grading, spreads |

## Tier policy (business)

- **Tier 1 — always ingest:** Government and exchange primary sources (EIA, IEA hub, OPEC, CME, UNCTAD flagship PDFs).
- **Tier 2 — ingest after Tier 1 stable:** Open academic PDFs, port booklets, OGIM paper, bank research *landing* pages (not paywalled body).
- **Never auto-ingest:** Retail broker blogs, aggregators without primary data, Scribd, YouTube, pirated books.

## Licensed books (manual path)

| Book | Module |
|------|--------|
| The Prize | Geopolitical logic / history |
| Oil 101 | Physical & refining dictionary — **in repo** as `local_knowledge_sources/oil101.txt` |
| King of Oil | Physical trading / arb |
| Trading Natural Gas | Pipeline/storage hedging parallels |

## Automation

Program: `oil_rag_collector` (`python -m oil_rag_collector`).

- **Catalog:** `sources_registry.json`
- **Bulk download:** tier folders + `collection_manifest.json`
- **Discovery:** EIA country briefs, UNCTAD maritime PDFs (bounded `max_discover`)
- **APIs:** `EIA_API_KEY` for WTI spot + U.S./Cushing stocks series

Downstream: PDF/HTML → text → `source_ingest.preprocess` → `source_ingest.ingest` → `rag_adhoc` search.

## Volume target (100+ docs)

1. Run collector Tier 1–2 (~35 seeds + up to 55 discovered EIA/UNCTAD).
2. Add EIA country briefs (40 discover cap).
3. Repeat UNCTAD annual maritime PDF discovery yearly.
4. Licensed books + internal desk notes via preprocess.
