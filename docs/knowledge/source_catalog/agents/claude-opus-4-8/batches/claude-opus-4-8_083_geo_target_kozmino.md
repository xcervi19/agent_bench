# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_083_geo_target_kozmino.md  
**Fáze:** geo_target — krok kozmino (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Kozmino (ESPO)** (`kozmino`, load_port), 12 slotů. Ruský **tichomořský ESPO výstup** do Asie (čínské
teapoty, Indie). ESPO často **nad price cap** → ruské/dark-fleet pojištění. Klíč = **pipeline (Transneft
ESPO)**, **sanctions (price cap)**, **dark fleet AIS**. 3 `proposed`, 3 `unverified`, 6 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-kozmino-port_authority | kozmino | port_authority | Port of Kozmino (Transneft/Transnefteservis) | — | infrastructure | official | port_closure | unverified |
| gt-kozmino-pipeline_operator | kozmino | pipeline_operator | Transneft ESPO pipeline | transneft.ru | infrastructure | official | pipeline_outage | proposed |
| gt-kozmino-transit_naval | kozmino | transit_naval | — | — | — | — | — | empty |
| gt-kozmino-loading_terminal | kozmino | loading_terminal | Kozmino oil terminal (Transneft) | transneft.ru | infrastructure | official | vessel_loading | unverified |
| gt-kozmino-national_noc | kozmino | national_noc | Transneft | transneft.ru | infrastructure | official | exports | unverified |
| gt-kozmino-shipping_lane | kozmino | shipping_lane | Dark-fleet AIS (ESPO → China/India) | — | shipping | data_feed | vessel_loading, sanctions | proposed |
| gt-kozmino-customs_border | kozmino | customs_border | — | — | — | — | — | empty |
| gt-kozmino-insurance_war_risk | kozmino | insurance_war_risk | — (Pacific; low war-risk) | — | — | — | — | empty |
| gt-kozmino-storage_operator | kozmino | storage_operator | — | — | — | — | — | empty |
| gt-kozmino-pricing_hub | kozmino | pricing_hub | — (ESPO blend — global) | — | — | — | — | empty |
| gt-kozmino-weather_hazard | kozmino | weather_hazard | — | — | — | — | — | empty |
| gt-kozmino-sanctions_enforcement | kozmino | sanctions_enforcement | US OFAC / EU price cap (ESPO above cap) | ofac.treasury.gov | government_regulator | official | sanctions | proposed |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-kozmino-pipeline_operator | ESPO do Asie | ruská pivot na východ | Transneft ESPO → Kozmino | proposed |
| gt-kozmino-sanctions_enforcement | **ESPO nad price cap** | non-Western pojištění | Čína/Indie teapoty | proposed |
| gt-kozmino-shipping_lane | — | dark fleet | AIS rekonstrukce | proposed |

### Unverified / Anti-patterns

- Transneft domény unverified (sankce/dostupnost).
- ESPO se pravidelně obchoduje nad $60 cap → mimo západní služby (indikátor efektivity capu).
- insurance/pricing/weather `empty`: Pacifik nízké war-risk, ESPO pricing globální.

### Progress po merge

`phase: geo_target`, `last_geo_target: kozmino`, `last_batch_seq: 83` — load ports KOMPLETNÍ (10/10)
