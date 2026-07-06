# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_086_geo_target_sabine_pass.md  
**Fáze:** geo_target — krok sabine_pass (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Sabine Pass LNG** (`sabine_pass`, us_gulf_hub), 12 slotů. Vlajkový **US LNG export** (Cheniere).
Klíč = **loading_terminal (Cheniere)**, **pipeline (feedgas nominace = proxy US LNG exportu)**,
**weather (Gulf hurricany)**; FERC výpadkové filings. 3 `proposed`, 1 `unverified`, 8 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-sabine_pass-port_authority | sabine_pass | port_authority | — (Sabine-Neches Waterway / USCG) | — | — | — | — | empty |
| gt-sabine_pass-pipeline_operator | sabine_pass | pipeline_operator | Cheniere feedgas (Creole Trail) + FERC filings | cheniere.com | infrastructure | official | pipeline_outage, refinery_outage | proposed |
| gt-sabine_pass-transit_naval | sabine_pass | transit_naval | — | — | — | — | — | empty |
| gt-sabine_pass-loading_terminal | sabine_pass | loading_terminal | Cheniere Sabine Pass LNG | cheniere.com | infrastructure | official | vessel_loading | proposed |
| gt-sabine_pass-national_noc | sabine_pass | national_noc | — (no NOC) | — | — | — | — | empty |
| gt-sabine_pass-shipping_lane | sabine_pass | shipping_lane | — (AIS global) | — | — | — | — | empty |
| gt-sabine_pass-customs_border | sabine_pass | customs_border | — | — | — | — | — | empty |
| gt-sabine_pass-insurance_war_risk | sabine_pass | insurance_war_risk | — | — | — | — | — | empty |
| gt-sabine_pass-storage_operator | sabine_pass | storage_operator | — | — | — | — | — | empty |
| gt-sabine_pass-pricing_hub | sabine_pass | pricing_hub | — (Henry Hub linkage — global) | — | — | — | — | empty |
| gt-sabine_pass-weather_hazard | sabine_pass | weather_hazard | NOAA NHC (Gulf hurricanes) | nhc.noaa.gov | weather | official | hurricane, port_closure | proposed |
| gt-sabine_pass-sanctions_enforcement | sabine_pass | sanctions_enforcement | — (FERC/DOE export authorizations) | ferc.gov | government_regulator | official | export_license | unverified |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-sabine_pass-pipeline_operator | **feedgas nominace = US LNG export proxy** | US LNG jako EU energetická jistota | Creole Trail feedgas | proposed |
| gt-sabine_pass-loading_terminal | Cheniere kargá | — | LNG nakládka | proposed |
| gt-sabine_pass-weather_hazard | — | — | Gulf hurricany shut-in | proposed |

### Unverified / Anti-patterns

- **Feedgas nominace** (pipeline flow data) = nejlepší real-time proxy US LNG exportu (výpadek train → pokles feedgas).
- FERC/DOE export authorizations = policy vrstva (pause/resume LNG povolení) — unverified mapping na geo_subject.
- pricing `empty`: Henry Hub linkage = globální.

### Progress po merge

`phase: geo_target`, `last_geo_target: sabine_pass`, `last_batch_seq: 86` — US Gulf 2/5 (zbývá Freeport, Corpus Christi)
