# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_089_geo_target_ras_laffan.md  
**Fáze:** geo_target — krok ras_laffan (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Ras Laffan** (`ras_laffan`, lng_terminal), 12 slotů. **Největší LNG export hub světa** (QatarEnergy;
North Field). Klíč = **NOC + loading_terminal (QatarEnergy)**, **pipeline (North Field)**, **insurance
(vše musí přes Hormuz!)**. North Field expansion 2026+. 5 `proposed`, 0 `unverified`, 7 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-ras_laffan-port_authority | ras_laffan | port_authority | Mwani Qatar / Ras Laffan Port | mwani.com.qa | infrastructure | official | port_closure | proposed |
| gt-ras_laffan-pipeline_operator | ras_laffan | pipeline_operator | QatarEnergy North Field pipelines | qatarenergy.qa | infrastructure | official | pipeline_outage | proposed |
| gt-ras_laffan-transit_naval | ras_laffan | transit_naval | — | — | — | — | — | empty |
| gt-ras_laffan-loading_terminal | ras_laffan | loading_terminal | Ras Laffan LNG (QatarEnergy) | qatarenergy.qa | infrastructure | official | vessel_loading | proposed |
| gt-ras_laffan-national_noc | ras_laffan | national_noc | QatarEnergy | qatarenergy.qa | noc | official | production, exports, term_contract | proposed |
| gt-ras_laffan-shipping_lane | ras_laffan | shipping_lane | — (AIS global) | — | — | — | — | empty |
| gt-ras_laffan-customs_border | ras_laffan | customs_border | — | — | — | — | — | empty |
| gt-ras_laffan-insurance_war_risk | ras_laffan | insurance_war_risk | Lloyd's Joint War Committee (Gulf — Hormuz transit) | lmalloyds.com | industry_body | official | force_majeure | proposed |
| gt-ras_laffan-storage_operator | ras_laffan | storage_operator | — | — | — | — | — | empty |
| gt-ras_laffan-pricing_hub | ras_laffan | pricing_hub | — (LNG term/JKM — global) | — | — | — | — | empty |
| gt-ras_laffan-weather_hazard | ras_laffan | weather_hazard | — | — | — | — | — | empty |
| gt-ras_laffan-sanctions_enforcement | ras_laffan | sanctions_enforcement | — | — | — | — | — | empty |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-ras_laffan-national_noc (QatarEnergy) | největší LNG export; North Field expansion | dlouhodobé kontrakty (Asie/EU) | Ras Laffan nakládka | proposed |
| gt-ras_laffan-insurance_war_risk | — | **veškeré qatarské LNG přes Hormuz** | war-risk = klíčová zranitelnost | proposed |

### Unverified / Anti-patterns

- **Hormuz závislost:** 100 % qatarského LNG musí přes Hormuz → přímé propojení s `gt-hormuz`.
- pricing `empty`: LNG většinou term kontrakty (oil-indexed) + JKM spot = globální.
- North Field expansion (2026+) = strukturální supply signál (dlouhodobě medvědí LNG).

### Progress po merge

`phase: geo_target`, `last_geo_target: ras_laffan`, `last_batch_seq: 89`
