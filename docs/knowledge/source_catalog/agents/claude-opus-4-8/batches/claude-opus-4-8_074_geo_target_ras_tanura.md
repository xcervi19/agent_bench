# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_074_geo_target_ras_tanura.md  
**Fáze:** geo_target — krok ras_tanura (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Ras Tanura** (`ras_tanura`, load_port), 12 slotů. **Největší ropný export terminál světa** (Aramco;
Ras Tanura + Ju'aymah VLCC). Klíč = **loading_terminal + national_noc (Aramco)**, **pipeline (Petroline
obchvat)**, **insurance (JWC — 2019 Abqaiq dron)**. 5 `proposed`, 0 `unverified`, 7 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-ras_tanura-port_authority | ras_tanura | port_authority | Saudi Ports Authority (Mawani) | mawani.gov.sa | infrastructure | official | port_closure | proposed |
| gt-ras_tanura-pipeline_operator | ras_tanura | pipeline_operator | Aramco East-West Petroline (→ Yanbu) | aramco.com | infrastructure | official | pipeline_outage | proposed |
| gt-ras_tanura-transit_naval | ras_tanura | transit_naval | Royal Saudi Naval Forces | — | diplomacy | official | port_closure | empty |
| gt-ras_tanura-loading_terminal | ras_tanura | loading_terminal | Saudi Aramco Ras Tanura / Ju'aymah terminals | aramco.com | infrastructure | official | vessel_loading | proposed |
| gt-ras_tanura-national_noc | ras_tanura | national_noc | Saudi Aramco | aramco.com | noc | official | production, exports | proposed |
| gt-ras_tanura-shipping_lane | ras_tanura | shipping_lane | — (tanker AIS — global layer) | — | — | — | — | empty |
| gt-ras_tanura-customs_border | ras_tanura | customs_border | — | — | — | — | — | empty |
| gt-ras_tanura-insurance_war_risk | ras_tanura | insurance_war_risk | Lloyd's Joint War Committee (Gulf) | lmalloyds.com | industry_body | official | force_majeure | proposed |
| gt-ras_tanura-storage_operator | ras_tanura | storage_operator | — (Aramco storage via loading_terminal) | — | — | — | — | empty |
| gt-ras_tanura-pricing_hub | ras_tanura | pricing_hub | — (Aramco OSP — global layer) | — | — | — | — | empty |
| gt-ras_tanura-weather_hazard | ras_tanura | weather_hazard | — (low) | — | — | — | — | empty |
| gt-ras_tanura-sanctions_enforcement | ras_tanura | sanctions_enforcement | — | — | — | — | — | empty |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-ras_tanura-loading_terminal | největší crude export terminál | **2019 Abqaiq/Khurais dron útok** | Ju'aymah VLCC nakládka | proposed — tail-risk supply |
| gt-ras_tanura-pipeline_operator | Petroline obchvat Hormuz | — | Ras Tanura↔Yanbu | proposed |

### Unverified / Anti-patterns

- pricing_hub `empty`: Aramco OSP patří do globální vrstvy (bez duplicity).
- 2019 Abqaiq útok = precedent pro dopad na Ras Tanura/Ju'aymah nakládku (drony/rakety).
- shipping_lane `empty`: tanker AIS je globální feed, ne per-port.

### Progress po merge

`phase: geo_target`, `last_geo_target: ras_tanura`, `last_batch_seq: 74`
