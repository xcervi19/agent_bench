# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_085_geo_target_houston_ship_channel.md  
**Fáze:** geo_target — krok houston_ship_channel (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Houston Ship Channel** (`houston_ship_channel`, us_gulf_hub), 12 slotů. Jádro **PADD3 rafinace/exportu**;
klíč = **port_authority (Port Houston)**, **transit/shipping (USCG uzávěry kanálu)**, **weather
(hurricany/mlha)**. MEH pricing point. 3 `proposed`, 0 `unverified`, 9 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-houston_ship_channel-port_authority | houston_ship_channel | port_authority | Port Houston | porthouston.com | infrastructure | official | port_closure, vessel_loading | proposed |
| gt-houston_ship_channel-pipeline_operator | houston_ship_channel | pipeline_operator | — (Enterprise/Magellan — mnoho) | — | — | — | — | empty |
| gt-houston_ship_channel-transit_naval | houston_ship_channel | transit_naval | US Coast Guard Sector Houston-Galveston (channel status) | uscg.mil | shipping | official | port_closure | proposed |
| gt-houston_ship_channel-loading_terminal | houston_ship_channel | loading_terminal | — (Enterprise/Magellan/Moda terminals) | — | — | — | — | empty |
| gt-houston_ship_channel-national_noc | houston_ship_channel | national_noc | — (no NOC) | — | — | — | — | empty |
| gt-houston_ship_channel-shipping_lane | houston_ship_channel | shipping_lane | — (USCG via transit_naval) | — | — | — | — | empty |
| gt-houston_ship_channel-customs_border | houston_ship_channel | customs_border | — | — | — | — | — | empty |
| gt-houston_ship_channel-insurance_war_risk | houston_ship_channel | insurance_war_risk | — | — | — | — | — | empty |
| gt-houston_ship_channel-storage_operator | houston_ship_channel | storage_operator | — (Gulf Coast PADD3 via EIA global) | — | — | — | — | empty |
| gt-houston_ship_channel-pricing_hub | houston_ship_channel | pricing_hub | — (MEH / Magellan East Houston — global) | — | — | — | — | empty |
| gt-houston_ship_channel-weather_hazard | houston_ship_channel | weather_hazard | NOAA NHC (hurricanes/fog closures) | nhc.noaa.gov | weather | official | hurricane, port_closure | proposed |
| gt-houston_ship_channel-sanctions_enforcement | houston_ship_channel | sanctions_enforcement | — | — | — | — | — | empty |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-houston_ship_channel-port_authority | největší US rafinerní region | US energetická dominance | export corridor | proposed |
| gt-houston_ship_channel-transit_naval (USCG) | — | — | **mlha/hurricany → uzávěry kanálu** | proposed |
| gt-houston_ship_channel-weather_hazard | — | — | sezónní hurricany + zimní mlha | proposed |

### Unverified / Anti-patterns

- storage/pricing `empty`: PADD3 zásoby (EIA) a MEH pricing = globální vrstva.
- USCG channel closures (mlha/kolize/hurricany) = pravidelný logistický signál.
- Mnoho terminálů/pipelines → nezachycuji jednotlivě (playbook úroveň).

### Progress po merge

`phase: geo_target`, `last_geo_target: houston_ship_channel`, `last_batch_seq: 85`
