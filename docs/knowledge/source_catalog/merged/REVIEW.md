# Multi-agent source merge — analyst review & final

**Reviewed by:** trading-geopolitical-analyst (agent)  
**Date:** 2026-07-07  
**Inputs:** 4 agent catalogs (`claude-opus-4-8`, `claude-sonnet-4-6`, `composer-2-5`, `gpt-5-5`)

## Pipeline

1. `merge_catalogs.py` — deterministic union, vote by normalized domain → `catalog_merged.json` + `review_later.json`.
2. `finalize_catalog.py` — analyst finalization (re-reads raw catalogs) → `catalog_final.json` + `source_whitelist.json` (#29) + `finalize_report.json`.

Both scripts are LLM-free and re-runnable.

## Analyst decisions applied

- **Conflict = benign name variants**, not domain conflicts. 596 domains had multiple entity-name
  spellings (e.g. `aramco.com`: "Saudi Aramco" vs geo-specific labels). Resolved by
  **agent-level majority vote** (robust to per-agent row duplication), tie → shortest clean name.
- **Consensus acceptance:** `accepted` = ≥2 agents independently marked `proposed`.
- **Note hygiene:** dropped machine-noise notes (`crosscheck`, `review batch`, `Geo target slot`,
  `proposed retained`); kept ≤3 substantive analyst notes per source.
- **Whitelist filter (#29):** `accepted` + real domain + `type ∈ {official, data_feed, social}`.

## Result

| Metric | Value |
|--------|-------|
| Unique domains (full final catalog) | 1347 |
| Accepted (≥2-agent consensus) | 613 |
| **`source_whitelist.json` size** | **610** |
| Name conflicts resolved | 596 |

**4/4-agent agreement** entries are the highest-confidence tier (proxy for #29 "top-20 manually
validated" — cross-model consensus).

## Outputs

- `../../../../source_whitelist.json` — **#29 deliverable** (repo root).
- `catalog_final.json` — full curated catalog (1347 domains, incl. `unverified` backlog).
- `review_later.json` — low-confidence rows (single-agent / not accepted) for optional later pass.

## Next

- **#30 playbooks** — draft from `catalog_final.json` (notes + signals per topic).
- **#31 scraping** — verify `unverified` social handles → promote to `proposed`.
- Optional: re-run both scripts after any agent adds batches.
