# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_092_geo_target_cove_point.md  
**Fáze:** geo_target — krok cove_point (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Cove Point LNG** (`cove_point`, lng_terminal), 12 slotů. US **východní pobřeží** LNG (Berkshire/Dominion,
Maryland); kontrakty GAIL (Indie) + Sumitomo (Japonsko). Malý objem. Klíč = **loading_terminal + feedgas**.
3 `proposed`, 1 `unverified`, 8 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-cove_point-port_authority | cove_point | port_authority | — (USCG Sector Maryland-NCR) | — | — | — | — | empty |
| gt-cove_point-pipeline_operator | cove_point | pipeline_operator | Cove Point feedgas (Dominion) + FERC filings | dominionenergy.com | infrastructure | official | pipeline_outage | proposed |
| gt-cove_point-transit_naval | cove_point | transit_naval | — | — | — | — | — | empty |
| gt-cove_point-loading_terminal | cove_point | loading_terminal | Cove Point LNG (Berkshire Hathaway Energy) | — | infrastructure | official | vessel_loading | unverified |
| gt-cove_point-national_noc | cove_point | national_noc | — (no NOC) | — | — | — | — | empty |
| gt-cove_point-shipping_lane | cove_point | shipping_lane | — (AIS global) | — | — | — | — | empty |
| gt-cove_point-customs_border | cove_point | customs_border | — | — | — | — | — | empty |
| gt-cove_point-insurance_war_risk | cove_point | insurance_war_risk | — | — | — | — | — | empty |
| gt-cove_point-storage_operator | cove_point | storage_operator | — | — | — | — | — | empty |
| gt-cove_point-pricing_hub | cove_point | pricing_hub | — (Henry Hub linkage global) | — | — | — | — | empty |
| gt-cove_point-weather_hazard | cove_point | weather_hazard | NOAA NHC (Atlantic hurricanes) | nhc.noaa.gov | weather | official | hurricane | proposed |
| gt-cove_point-sanctions_enforcement | cove_point | sanctions_enforcement | FERC/DOE export authorizations | ferc.gov | government_regulator | official | export_license | proposed |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-cove_point-loading_terminal | US East Coast LNG (malý) | GAIL/Sumitomo kontrakty | feedgas nominace | unverified |
| gt-cove_point-pipeline_operator | — | — | Dominion feedgas | proposed |

### Unverified / Anti-patterns

- Malý objem (~5 Mtpa); relevance nižší než Gulf terminály.
- East Coast → nižší hurricane exposure než Gulf, ale existuje.
- pricing `empty`: Henry Hub linkage globální.

### Progress po merge

`phase: geo_target`, `last_geo_target: cove_point`, `last_batch_seq: 92` — LNG terminály KOMPLETNÍ (4/4)
