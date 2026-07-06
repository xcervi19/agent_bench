# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_080_geo_target_singapore.md  
**Fáze:** geo_target — krok singapore (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Singapore bunkering hub** (`singapore`, load_port), 12 slotů. Většina autorit už pod **`ca-SG`** →
zde jen **ne-duplicitní** vrstvy: **loading_terminal (Jurong/Pulau Bukom)**, **storage (Jurong tank farms +
enterprise onshore stocks)**, **pricing_hub (Platts Singapore MOC = asijský benchmark)**. 3 `proposed`, 1 `unverified`, 8 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-singapore-port_authority | singapore | port_authority | — (MPA via ca-SG) | — | — | — | — | empty |
| gt-singapore-pipeline_operator | singapore | pipeline_operator | — | — | — | — | — | empty |
| gt-singapore-transit_naval | singapore | transit_naval | — | — | — | — | — | empty |
| gt-singapore-loading_terminal | singapore | loading_terminal | Jurong Island / Pulau Bukom (Shell), Universal Terminal | — | infrastructure | official | vessel_loading, refinery_outage | proposed |
| gt-singapore-national_noc | singapore | national_noc | — (no NOC) | — | — | — | — | empty |
| gt-singapore-shipping_lane | singapore | shipping_lane | — (MPA bunker/VTS via ca-SG) | — | — | — | — | empty |
| gt-singapore-customs_border | singapore | customs_border | — (Singapore Customs via ca-SG) | — | — | — | — | empty |
| gt-singapore-insurance_war_risk | singapore | insurance_war_risk | — | — | — | — | — | empty |
| gt-singapore-storage_operator | singapore | storage_operator | Jurong tank farms (Vopak/Universal) + Enterprise SG onshore stocks | — | infrastructure | data_feed | storage_levels | unverified |
| gt-singapore-pricing_hub | singapore | pricing_hub | Platts Singapore MOC window (Asian benchmark) | spglobal.com | industry_body | data_feed | pricing_formula | proposed |
| gt-singapore-weather_hazard | singapore | weather_hazard | — | — | — | — | — | empty |
| gt-singapore-sanctions_enforcement | singapore | sanctions_enforcement | — | — | — | — | — | empty |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-singapore-pricing_hub | — | — | **Platts SG MOC = asijský oil benchmark** | proposed |
| gt-singapore-storage_operator | týdenní onshore stocks (ES) | — | Jurong tank farms | unverified |
| gt-singapore-loading_terminal | rafinerie Bukom/Jurong | — | products/bunker export | proposed |

### Unverified / Anti-patterns

- **Většina slotů `empty`** cíleně — MPA, Customs, EMA, SGX už v `ca-SG` (bez duplicity).
- Enterprise Singapore týdenní onshore stocks = klíčový storage feed (ověřit URL).
- Platts MOC = benchmark; Tier 1 pro asijské pricing.

### Progress po merge

`phase: geo_target`, `last_geo_target: singapore`, `last_batch_seq: 80`
