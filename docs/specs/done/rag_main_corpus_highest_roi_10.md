# RAG Main Corpus (Highest ROI) — #10

**Status:** DONE  
**Completed:** 2026-05-22  
**Tenant:** `00000000-0000-0000-0000-000000000001`

---

## Objective

Build a production-ready **main RAG corpus** for senior WTI/crude oil trading: authoritative public sources + desk books, chunked and embedded in Postgres for `rag_adhoc` search.

---

## Outcome

| Metric | Value |
|--------|------:|
| Documents in DB | **66** |
| Events (chunks) | **3,090** |
| Chunk artifact dirs | **65** |
| Downloaded web files (`oil_rag_collector`) | **56** OK (+ 2 failed: OPEC, MDPI) |
| Internet source domains | **18** |
| Local books/corpus (`oil_gas_knowledge`) | **10** chunked + ingested |

**Verdict:** Corpus is **ready for RAG testing**. Not 100% of a theoretical catalog (known gaps below).

---

## What was delivered

### 1. Source collection — `oil_rag_collector/`

- Tiered registry (IEA, EIA, CME, INE, UNCTAD, KPMG, terminals, geopolitics, EIA API JSON, 30 country overviews).
- CLI: `python -m oil_rag_collector` with `EIA_API_KEY`, `--skip-eia-api`, `--max-tier`.
- Output: `artifacts/oil_rag_sources/` + `collection_manifest.json`.

### 2. Batch chunk pipeline — `source_ingest.from_collected`

- Scans folder (PDF/HTML/JSON/TXT) → `normalized.txt` + `chunks.jsonl` + `manifest.json` per source.
- Skip-if-exists (`artifacts/chunks/<slug>/manifest.json`), `--skip-slug oil101`.
- EIA JSON split into row batches (fix for 8192-token embed limit).

### 3. DB ingest — `source_ingest.ingest`

- OpenAI `text-embedding-3-small` → `documents` + `events` (pgvector).
- Batch run via SSH tunnel to VPS Postgres (`127.0.0.1:5433`).
- Report: `artifacts/ingest_report.txt`.

### 4. Prior / parallel corpus

- **Oil 101** — `local_knowledge_sources/oil101.txt` (already in RAG before this ticket).

### 5. Docs

- `docs/knowledge/oil_rag_source_strategy.md`
- `oil_rag_collector/README.md`
- README § Oil / WTI RAG + batch ingest

---

## Domain coverage (RAG clusters)

| Cluster | In corpus |
|---------|-----------|
| `market_price` | EIA pages, 3× EIA API series, CFTC, TU Chemnitz |
| `supply_demand` | IEA OMR×2, EIA STEO/WPSR, 30× country HTML |
| `trading_mechanics` | CME WTI PDF, INE handbook, trading books |
| `maritime_logistics` | UNCTAD, theses, port newsletters |
| `infrastructure` | BTC Ceyhan, Aalborg, OGIM, OCIMF |
| `geopolitics` | KPMG, EUR, GDELT hub, JPM, Farchy, corpus |

---

## Known gaps (phase 2, not blocking test)

| Gap | Reason |
|-----|--------|
| OPEC MOMR, MDPI tail-risk PDF | HTTP 403 from collector |
| `Top100Ports2022_Ebook.pdf` | Not chunked in `oil_gas_knowledge` pass |
| `.epub`, `.7z` in `oil_gas_knowledge` | No extractor / not extracted |
| Oil 101 PDF | Skipped (duplicate of ingested `.txt`) |
| FRED CSV | Optional skip (timeout); EIA API covers WTI/stocks |

---

## How to verify (testing handoff)

```bash
# SSH tunnel (if DB on VPS)
ssh -i ~/.ssh/contabo_ed25519 -N -L 5433:127.0.0.1:5432 root@79.143.179.212

curl -sS -X POST "http://127.0.0.1:8001/v1/search" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: 00000000-0000-0000-0000-000000000001" \
  -H "X-API-Key: $RAG_ADHOC_API_KEY" \
  -d '{"query":"Cushing crude oil inventory weekly","limit":5}'
```

Expect hits from EIA series, WPSR HTML, country overviews, and desk books.

---

## Repo map

| Path | Role |
|------|------|
| `oil_rag_collector/` | Download public sources |
| `artifacts/oil_rag_sources/` | Raw files |
| `artifacts/chunks/` | Per-source chunk artifacts |
| `oil_gas_knowledge/` | Local PDFs (ingested via `from_collected`) |
| `local_knowledge_sources/oil101.txt` | Oil 101 (pre-existing RAG) |
| `source_ingest/` | preprocess, from_collected, ingest |
| `apps/rag_adhoc/` | Search API |

---

## Ticket closure

**#10 RAG main corpus (highest ROI) — FINISHED.**  
Move to **RAG integration / agent testing** (newsfind, trade-intel, `rag_adhoc` queries).
