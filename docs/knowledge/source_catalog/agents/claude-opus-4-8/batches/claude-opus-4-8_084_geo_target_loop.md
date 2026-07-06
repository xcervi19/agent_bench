# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_084_geo_target_loop.md  
**Fáze:** geo_target — krok loop (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**LOOP (Louisiana Offshore Oil Port)** (`loop`, us_gulf_hub), 12 slotů. Jediný **US hlubokovodní port pro
VLCC** (import i export); **Clovelly Hub** storage = delivery point LOOP Sour. Klíč = **port/terminal
(LOOP LLC)**, **storage (Clovelly)**, **weather (Gulf hurricanes)**. 5 `proposed`, 0 `unverified`, 7 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-loop-port_authority | loop | port_authority | LOOP LLC | loopllc.com | infrastructure | official | port_closure | proposed |
| gt-loop-pipeline_operator | loop | pipeline_operator | LOOP pipelines / Clovelly hub | loopllc.com | infrastructure | official | pipeline_outage | proposed |
| gt-loop-transit_naval | loop | transit_naval | — | — | — | — | — | empty |
| gt-loop-loading_terminal | loop | loading_terminal | LOOP marine terminal (VLCC import/export) | loopllc.com | infrastructure | official | vessel_loading | proposed |
| gt-loop-national_noc | loop | national_noc | — (no NOC) | — | — | — | — | empty |
| gt-loop-shipping_lane | loop | shipping_lane | — (AIS global) | — | — | — | — | empty |
| gt-loop-customs_border | loop | customs_border | — | — | — | — | — | empty |
| gt-loop-insurance_war_risk | loop | insurance_war_risk | — | — | — | — | — | empty |
| gt-loop-storage_operator | loop | storage_operator | Clovelly Hub (LOOP Sour delivery/storage) | loopllc.com | infrastructure | official | storage_levels | proposed |
| gt-loop-pricing_hub | loop | pricing_hub | — (LOOP Sour / LLS — global) | — | — | — | — | empty |
| gt-loop-weather_hazard | loop | weather_hazard | NOAA NHC (Gulf hurricanes) | nhc.noaa.gov | weather | official | hurricane, port_closure | proposed |
| gt-loop-sanctions_enforcement | loop | sanctions_enforcement | — | — | — | — | — | empty |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-loop-loading_terminal | US crude export (VLCC) | US energetická dominance | jediný VLCC-capable US port | proposed |
| gt-loop-storage_operator | LOOP Sour delivery | — | **Clovelly Hub** | proposed |
| gt-loop-weather_hazard | — | — | **Gulf hurricany** (evakuace) | proposed |

### Unverified / Anti-patterns

- pricing_hub `empty`: LOOP Sour/LLS pricing = globální vrstva.
- Jediný US port schopný plně naložit VLCC → klíč pro US crude export arb.
- Hurricany (NHC) = sezónní shut-in Gulf (červen–listopad).

### Progress po merge

`phase: geo_target`, `last_geo_target: loop`, `last_batch_seq: 84`
