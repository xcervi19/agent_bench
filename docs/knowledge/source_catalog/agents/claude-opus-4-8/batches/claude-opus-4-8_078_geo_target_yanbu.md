# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_078_geo_target_yanbu.md  
**Fáze:** geo_target — krok yanbu (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Yanbu** (`yanbu`, load_port), 12 slotů. Saúdský **Rudé moře výstup = konec Petroline (obchvat Hormuz)**
+ rafinérský hub (YASREF). Klíč = **pipeline (Petroline terminus)**, **loading_terminal + NOC (Aramco)**,
**insurance (JWC — Húsí spillover na Yanbu/Jeddah)**. 5 `proposed`, 0 `unverified`, 7 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-yanbu-port_authority | yanbu | port_authority | Saudi Ports Authority (Mawani) / Royal Commission Yanbu | mawani.gov.sa | infrastructure | official | port_closure | proposed |
| gt-yanbu-pipeline_operator | yanbu | pipeline_operator | Aramco Petroline (East-West terminus) | aramco.com | infrastructure | official | pipeline_outage | proposed |
| gt-yanbu-transit_naval | yanbu | transit_naval | — | — | — | — | — | empty |
| gt-yanbu-loading_terminal | yanbu | loading_terminal | Aramco Yanbu crude terminal | aramco.com | infrastructure | official | vessel_loading | proposed |
| gt-yanbu-national_noc | yanbu | national_noc | Saudi Aramco | aramco.com | noc | official | production, exports | proposed |
| gt-yanbu-shipping_lane | yanbu | shipping_lane | — (AIS global) | — | — | — | — | empty |
| gt-yanbu-customs_border | yanbu | customs_border | — | — | — | — | — | empty |
| gt-yanbu-insurance_war_risk | yanbu | insurance_war_risk | Lloyd's Joint War Committee (Red Sea) | lmalloyds.com | industry_body | official | force_majeure | proposed |
| gt-yanbu-storage_operator | yanbu | storage_operator | — | — | — | — | — | empty |
| gt-yanbu-pricing_hub | yanbu | pricing_hub | — (Aramco OSP global) | — | — | — | — | empty |
| gt-yanbu-weather_hazard | yanbu | weather_hazard | — | — | — | — | — | empty |
| gt-yanbu-sanctions_enforcement | yanbu | sanctions_enforcement | — | — | — | — | — | empty |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-yanbu-pipeline_operator | Petroline → Rudé moře (obchvat Hormuz) | strategická redundance | Yanbu terminál/rafinerie | proposed |
| gt-yanbu-insurance_war_risk | — | **Húsí útoky dosáhly Yanbu/Jeddah** (2022 Aramco depot) | war-risk premium | proposed |

### Unverified / Anti-patterns

- pricing_hub `empty`: Aramco OSP = globální vrstva.
- Yanbu = Rudé moře pól obchvatu Hormuz (párně s Fujairah na východě).
- 2022 Húsí útok na Aramco depot v Jeddah = precedent pro Rudé moře war-risk.

### Progress po merge

`phase: geo_target`, `last_geo_target: yanbu`, `last_batch_seq: 78`
