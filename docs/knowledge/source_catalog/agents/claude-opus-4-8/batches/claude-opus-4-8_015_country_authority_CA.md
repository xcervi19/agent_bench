# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_015_country_authority_CA.md  
**Fáze:** country_authority — krok CA (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-05  

---

## Shrnutí

Kanada (`CA`), 10 slotů (`ca-CA-{authority}`). **Žádný NOC** (soukromé: Suncor, CNRL, Cenovus).
Trading: **WCS discount k WTI**, oil sands, **TMX pipeline** (Trans Mountain, spuštěn 2024) změnil
export logistiku k Pacifiku. Regulace federal (CER) + provincial (AER Alberta). 8 `proposed`, 1 `empty`, 1 pozn.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-CA-ministry_petroleum | ministry_petroleum | Natural Resources Canada (NRCan) | natural-resources.canada.ca | government_regulator | official | production, export_license | proposed |
| ca-CA-noc | noc | — | — | — | — | — | empty |
| ca-CA-mfa | mfa | Global Affairs Canada | international.gc.ca | diplomacy | official | sanctions | proposed |
| ca-CA-customs_export | customs_export | Canada Border Services Agency (CBSA) | cbsa-asfc.gc.ca | government_regulator | official | exports | proposed |
| ca-CA-upstream_regulator | upstream_regulator | Canada Energy Regulator (CER) | cer-rec.gc.ca | government_regulator | official | production, pipeline_outage | proposed |
| ca-CA-port_maritime_authority | port_maritime_authority | Transport Canada / Port of Vancouver | portvancouver.com | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-CA-national_exchange | national_exchange | TMX Group / NGX (gas) | tmx.com | exchange | official | pricing_formula | proposed |
| ca-CA-central_bank | central_bank | Bank of Canada | bankofcanada.ca | government_regulator | official | — | proposed |
| ca-CA-environment_regulator | environment_regulator | Environment & Climate Change Canada | canada.ca | government_regulator | official | refinery_outage | proposed |
| ca-CA-coast_guard_navy | coast_guard_navy | Canadian Coast Guard | ccg-gcc.gc.ca | government_regulator | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-CA-upstream_regulator (CER) | export objemy, pipeline capacity | US-CA trade | Enbridge/TMX flows | proposed — AER (aer.ca) jako expanze |
| ca-CA-port_maritime_authority | — | — | Westridge/TMX terminal (Pacifik export) | proposed |

### Unverified / poznámky

- **`ca-CA-noc` = empty:** Kanada nemá NOC; produkce přes EIA/CER + soukromé IOCs.
- **Expanze:** `ca-CA-upstream_regulator__aer` (aer.ca — Alberta Energy Regulator, oil sands data),
  `ca-CA-national_exchange__ngx` (NGX Natural Gas Exchange, součást ICE — AECO gas hub).
- **TMX (Trans Mountain)** 2024 startup → nový Pacifik export, WCS discount narrowing signál.
- ECCC doména `canada.ca` (sub-path); ověřit přesnou stránku při validaci.

### Progress po merge

`last_country: CA`, `last_batch_seq: 15`
