# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_069_geo_target_suez.md  
**Fáze:** geo_target — krok suez (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Suez Canal** (`suez`, chokepoint), 12 slotů. Evropa↔Asie ropa/produkty/LNG + **SUMED** obchvat.
Klíč = **port_authority (SCA — denní tranzit)**, **pipeline (SUMED)**, **shipping_lane (Leth/SCA)**,
**insurance (Lloyd's JWC)**. Ever Given 2021 precedent; Húsí přesměrování ubírá objem. 4 `proposed`, 2 `unverified`, 6 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-suez-port_authority | suez | port_authority | Suez Canal Authority (SCA) | suezcanal.gov.eg | infrastructure | official | port_closure, vessel_loading | proposed |
| gt-suez-pipeline_operator | suez | pipeline_operator | SUMED (Ain Sokhna–Sidi Kerir, bypass) | apc.com.eg | infrastructure | official | pipeline_outage | unverified |
| gt-suez-transit_naval | suez | transit_naval | Egyptian Navy | — | diplomacy | official | port_closure | empty |
| gt-suez-loading_terminal | suez | loading_terminal | — | — | — | — | — | empty |
| gt-suez-national_noc | suez | national_noc | — (EGPC transit; via ca-EG) | — | — | — | — | empty |
| gt-suez-shipping_lane | suez | shipping_lane | Leth Agencies / SCA daily transit | leth.com | shipping | data_feed | vessel_loading, port_closure | proposed |
| gt-suez-customs_border | suez | customs_border | — | — | — | — | — | empty |
| gt-suez-insurance_war_risk | suez | insurance_war_risk | Lloyd's Joint War Committee (Red Sea approach) | lmalloyds.com | industry_body | official | force_majeure | proposed |
| gt-suez-storage_operator | suez | storage_operator | — | — | — | — | — | empty |
| gt-suez-pricing_hub | suez | pricing_hub | — | — | — | — | — | empty |
| gt-suez-weather_hazard | suez | weather_hazard | — (sandstorm/wind — Ever Given precedent) | — | — | — | — | empty |
| gt-suez-sanctions_enforcement | suez | sanctions_enforcement | — | — | — | — | — | empty |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-suez-port_authority (SCA) | Evropa↔Asie tok | egyptská tranzitní renta | **denní tranzit stats** | proposed — objemový indikátor |
| gt-suez-pipeline_operator (SUMED) | crude bypass při zablokování | — | Ain Sokhna↔Sidi Kerir | unverified — ověřit APC doménu |
| gt-suez-shipping_lane (Leth) | — | Húsí přesměrování ↓ objem | queue/transit data | proposed |

### Unverified / Anti-patterns

- **SUMED (`apc.com.eg`)** unverified — ověřit Arab Petroleum Pipelines Co.
- **Leth Agencies** = desk-trusted tranzit tracker (Tier 2 data_feed), ne oficiální, ale rychlejší než SCA PR.
- Suez objem klesá kvůli Bab el-Mandeb přesměrování (batch 068) — propojené.

### Progress po merge

`phase: geo_target`, `last_geo_target: suez`, `last_batch_seq: 69`
