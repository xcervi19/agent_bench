# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_087_geo_target_freeport.md  
**Fáze:** geo_target — krok freeport (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Freeport LNG** (`freeport`, us_gulf_hub), 12 slotů. US LNG (Texas); **precedent 2022 požár → 8měsíční
výpadek → skok TTF/JKM**. Klíč = **loading_terminal + feedgas (proxy exportu)**, **weather (hurricany)**.
3 `proposed`, 1 `unverified`, 8 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-freeport-port_authority | freeport | port_authority | — (USCG / Port Freeport) | — | — | — | — | empty |
| gt-freeport-pipeline_operator | freeport | pipeline_operator | Freeport LNG feedgas + FERC filings | freeportlng.com | infrastructure | official | pipeline_outage, refinery_outage | proposed |
| gt-freeport-transit_naval | freeport | transit_naval | — | — | — | — | — | empty |
| gt-freeport-loading_terminal | freeport | loading_terminal | Freeport LNG terminal (Quintana Island) | freeportlng.com | infrastructure | official | vessel_loading | proposed |
| gt-freeport-national_noc | freeport | national_noc | — (no NOC) | — | — | — | — | empty |
| gt-freeport-shipping_lane | freeport | shipping_lane | — (AIS global) | — | — | — | — | empty |
| gt-freeport-customs_border | freeport | customs_border | — | — | — | — | — | empty |
| gt-freeport-insurance_war_risk | freeport | insurance_war_risk | — | — | — | — | — | empty |
| gt-freeport-storage_operator | freeport | storage_operator | — | — | — | — | — | empty |
| gt-freeport-pricing_hub | freeport | pricing_hub | — (Henry Hub linkage global) | — | — | — | — | empty |
| gt-freeport-weather_hazard | freeport | weather_hazard | NOAA NHC (Gulf hurricanes) | nhc.noaa.gov | weather | official | hurricane, port_closure | proposed |
| gt-freeport-sanctions_enforcement | freeport | sanctions_enforcement | — (FERC/DOE export authorizations) | ferc.gov | government_regulator | official | export_license | unverified |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-freeport-loading_terminal | ~2 Bcf/d US LNG | EU/Asie energetická jistota | **2022 požár = 8měs. výpadek** | proposed — velký precedent |
| gt-freeport-pipeline_operator | feedgas nominace | — | proxy exportu (train down → feedgas ↓) | proposed |

### Unverified / Anti-patterns

- **2022 Freeport požár** = učebnicový příklad: US LNG výpadek → domácí Henry Hub ↓ + EU/Asie TTF/JKM ↑.
- Feedgas nominace = real-time proxy; FERC filings pro root cause.
- pricing `empty` (Henry Hub global).

### Progress po merge

`phase: geo_target`, `last_geo_target: freeport`, `last_batch_seq: 87`
