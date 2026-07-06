# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_014_country_authority_CA.md  
**Fáze:** country_authority — krok CA (Canada)  
**Datum:** 2026-07-05  

---

## Shrnutí

Canada = ~5.8 mb/d (2024), dominantně oil sands (Alberta). Klíčové signály:
**CER pipeline data** (Trans Mountain, Keystone capacity = US import signal), **NRCan export
data** (Heavy Canadian crude WCS discount vs WTI), **CAPP quarterly** (oil sands production
forecast), **Trans Mountain expansion** (TMX startup 2024 = Pacific market access). Žádný
státní NOC — empty slot. 9 proposed, 1 empty.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-CA-ministry_petroleum | CA | — | ministry_petroleum | NRCan – Natural Resources Canada | nrcan.gc.ca | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-CA-noc | CA | — | noc | — (no Canadian state NOC; TMC Crown corp for pipeline only) | — | — | — | — | empty |
| ca-CA-mfa | CA | — | mfa | Global Affairs Canada | international.gc.ca | international_agency | official | sanctions, policy | proposed |
| ca-CA-customs_export | CA | — | customs_export | CBSA – Canada Border Services Agency | cbsa-asfc.gc.ca | international_agency | official | exports, export_license | proposed |
| ca-CA-upstream_regulator | CA | — | upstream_regulator | CER – Canada Energy Regulator | cer-rec.gc.ca | international_agency | official | production, pipeline_outage | proposed |
| ca-CA-port_maritime_authority | CA | — | port_maritime_authority | Transport Canada (Marine Safety) | tc.gc.ca | international_agency | official | vessel_loading, port_closure | proposed |
| ca-CA-national_exchange | CA | — | national_exchange | TMX Group – Toronto Stock Exchange | tmx.com | exchange | official | pricing_formula, term_contract | proposed |
| ca-CA-central_bank | CA | — | central_bank | Bank of Canada | bankofcanada.ca | international_agency | official | pricing_formula, sanctions | proposed |
| ca-CA-environment_regulator | CA | — | environment_regulator | Environment and Climate Change Canada | ec.gc.ca | international_agency | official | refinery_outage, pipeline_outage | proposed |
| ca-CA-coast_guard_navy | CA | — | coast_guard_navy | Canadian Coast Guard | ccg-gcc.ca | international_agency | official | port_closure, force_majeure | proposed |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-CA-upstream_regulator (CER) | CER publikuje týdenní pipeline throughput data (Trans Mountain, Keystone, Enbridge Line 5); WCS export volumes = US Gulf heavy crude import signal | CER vydává emergency orders pro pipeline integrity (Enbridge Line 3 spill, TC Energy incidents) | Trans Mountain TMX (2024): zvýšená kapacita 890 kb/d → Westridge Marine Terminal Vancouver; Pacific access | **proposed** — cer-rec.gc.ca aktivní |
| ca-CA-ministry_petroleum (NRCan) | NRCan publikuje Canadian Energy Regulator outlook; oil sands production forecasts; LNG Canada updates (Kitimat terminal) | NRCan koordinuje US-Canada energy policy; Keystone XL cancellation (Biden 2021) byl přímý supply signal | Trans Mountain export licence under NRCan; LNG Canada export licence | **proposed** — nrcan.gc.ca aktivní |
| ca-CA-noc | Trans Mountain Corporation (Crown corp) = pipeline operator only, ne producent; žádný stát NOC | Canadian Feds privatizovaly Petro-Canada (2004); TMC zůstala Crown corp pro TMX pipeline | TMC provozuje Westridge Marine Terminal pro Pacific crude exports (TMX) | **empty** — TMC expansion slot: tmc.ca |

### Expansion sloty
- Trans Mountain Corporation → tmc.ca (pipeline Crown corp)
- Enbridge → enbridge.com (private; Line 5, Line 3; key for US imports)
- TC Energy → tcenergy.com (Keystone, NGTL pipeline)
- CAPP production forecasts → capp.ca/data (sub-feed from gl-industry_body-004)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 13, "last_country": "CA", "last_batch_seq": 14 }
```
