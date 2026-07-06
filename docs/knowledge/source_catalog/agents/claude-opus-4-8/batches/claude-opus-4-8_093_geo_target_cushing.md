# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_093_geo_target_cushing.md  
**Fáze:** geo_target — krok cushing (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Cushing, OK** (`cushing`, storage_pricing_hub), 12 slotů. **WTI fyzický delivery point (NYMEX/CME)**;
**EIA týdenní zásoby** = klíčový US signál. 2020 negativní WTI (plné tanky). Klíč = **storage (EIA) +
pricing_hub (CME WTI)**. 2 `proposed`, 1 `unverified`, 9 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-cushing-port_authority | cushing | port_authority | — (inland) | — | — | — | — | empty |
| gt-cushing-pipeline_operator | cushing | pipeline_operator | — (Seaway/Marketlink/BASIN — mnoho) | — | — | — | — | empty |
| gt-cushing-transit_naval | cushing | transit_naval | — | — | — | — | — | empty |
| gt-cushing-loading_terminal | cushing | loading_terminal | — | — | — | — | — | empty |
| gt-cushing-national_noc | cushing | national_noc | — (no NOC) | — | — | — | — | empty |
| gt-cushing-shipping_lane | cushing | shipping_lane | — (inland; pipeline) | — | — | — | — | empty |
| gt-cushing-customs_border | cushing | customs_border | — | — | — | — | — | empty |
| gt-cushing-insurance_war_risk | cushing | insurance_war_risk | — | — | — | — | — | empty |
| gt-cushing-storage_operator | cushing | storage_operator | EIA Weekly Cushing stocks (+ tank data) | eia.gov | international_agency | data_feed | storage_levels | proposed |
| gt-cushing-pricing_hub | cushing | pricing_hub | NYMEX WTI delivery point (CME) | cmegroup.com | exchange | official | pricing_formula | proposed |
| gt-cushing-weather_hazard | cushing | weather_hazard | — (winter storm — Uri 2021 froze wells) | — | — | — | — | unverified |
| gt-cushing-sanctions_enforcement | cushing | sanctions_enforcement | — | — | — | — | — | empty |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-cushing-pricing_hub (CME WTI) | WTI benchmark | US domácí | **fyzický delivery point** | proposed |
| gt-cushing-storage_operator (EIA) | — | — | **týdenní zásoby = tightness signál** | proposed — 2020 negativní WTI |

### Unverified / Anti-patterns

- **Inland hub:** port/shipping/loading `empty` — Cushing je tankové pole + pipeline uzel.
- EIA středeční zásoby = klíčový US crude balance signál (Cushing draws → backwardation).
- Winter Storm Uri (2021) precedent (mráz → freeze-off produkce) — unverified weather slot.

### Progress po merge

`phase: geo_target`, `last_geo_target: cushing`, `last_batch_seq: 93`
