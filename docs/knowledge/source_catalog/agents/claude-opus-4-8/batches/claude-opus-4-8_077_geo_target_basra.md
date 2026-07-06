# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_077_geo_target_basra.md  
**Fáze:** geo_target — krok basra (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Basra / Fao** (`basra`, load_port), 12 slotů. Hlavní irácký export (Basrah Medium/Heavy; SOMO OSP).
Basra Oil Terminal + Khor al-Amaya SPM. Klíč = **national_noc (Basra Oil Co / SOMO)**, **loading_terminal
(SPM)**, **insurance (JWC Gulf)**. KRG-Ceyhan pipeline samostatně (od 2023 stojí). 4 `proposed`, 1 `unverified`, 7 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-basra-port_authority | basra | port_authority | General Company for Ports of Iraq | scpiraq.com | infrastructure | official | port_closure | unverified |
| gt-basra-pipeline_operator | basra | pipeline_operator | — (ITP/KRG-Ceyhan = samostatný cíl) | — | — | — | — | empty |
| gt-basra-transit_naval | basra | transit_naval | — | — | — | — | — | empty |
| gt-basra-loading_terminal | basra | loading_terminal | Basra Oil Terminal (BOT) / Khor al-Amaya SPM | boc.oil.gov.iq | infrastructure | official | vessel_loading | proposed |
| gt-basra-national_noc | basra | national_noc | Basra Oil Company / SOMO | somoil.gov.iq | noc | official | production, exports, term_contract | proposed |
| gt-basra-shipping_lane | basra | shipping_lane | — (tanker AIS global) | — | — | — | — | empty |
| gt-basra-customs_border | basra | customs_border | — | — | — | — | — | empty |
| gt-basra-insurance_war_risk | basra | insurance_war_risk | Lloyd's Joint War Committee (Gulf) | lmalloyds.com | industry_body | official | force_majeure | proposed |
| gt-basra-storage_operator | basra | storage_operator | — | — | — | — | — | empty |
| gt-basra-pricing_hub | basra | pricing_hub | — (Basrah OSP via SOMO — global layer) | — | — | — | — | empty |
| gt-basra-weather_hazard | basra | weather_hazard | — | — | — | — | — | empty |
| gt-basra-sanctions_enforcement | basra | sanctions_enforcement | — | — | — | — | — | empty |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-basra-national_noc (SOMO) | Basrah Medium/Heavy | OPEC+ kvóta compliance | SPM nakládka | proposed |
| gt-basra-loading_terminal | ~irácký hlavní export | jižní stabilita vs KRG | technické/weather výpadky SPM | proposed |

### Unverified / Anti-patterns

- Domény (`scpiraq.com`, `boc.oil.gov.iq`, `somoil.gov.iq`) — ověřit; irácké gov weby kolísají.
- pricing_hub `empty`: Basrah OSP (SOMO) = globální vrstva.
- KRG-Ceyhan pipeline (od března 2023 stojí) = samostatný pipeline geo cíl, ne zde.

### Progress po merge

`phase: geo_target`, `last_geo_target: basra`, `last_batch_seq: 77`
