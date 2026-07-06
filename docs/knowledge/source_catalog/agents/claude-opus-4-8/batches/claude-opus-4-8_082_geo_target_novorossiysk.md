# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_082_geo_target_novorossiysk.md  
**Fáze:** geo_target — krok novorossiysk (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Novorossiysk** (`novorossiysk`, load_port), 12 slotů. Ruský Urals + **kazašský CPC blend** (hlavní
export KZ!). Klíč = **pipeline (Transneft + CPC)**, **sanctions (price cap)**, **insurance (JWC Černé
moře)**, **weather (Bora vítr)**, **ukrajinské drony/USV** na přístav+rafinerii. 4 `proposed`, 3 `unverified`, 5 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-novorossiysk-port_authority | novorossiysk | port_authority | Port of Novorossiysk (NCSP Group) | nmtp.info | infrastructure | official | port_closure | unverified |
| gt-novorossiysk-pipeline_operator | novorossiysk | pipeline_operator | Transneft + CPC (Caspian Pipeline Consortium) | cpc.ru | infrastructure | official | pipeline_outage | proposed |
| gt-novorossiysk-transit_naval | novorossiysk | transit_naval | Russian Black Sea Fleet | — | diplomacy | official | port_closure | empty |
| gt-novorossiysk-loading_terminal | novorossiysk | loading_terminal | Sheskharis (Transneft) + CPC marine terminal | cpc.ru | infrastructure | official | vessel_loading | unverified |
| gt-novorossiysk-national_noc | novorossiysk | national_noc | Transneft | transneft.ru | infrastructure | official | exports | unverified |
| gt-novorossiysk-shipping_lane | novorossiysk | shipping_lane | Dark-fleet AIS (Ukraine drone/USV strikes) | — | shipping | data_feed | force_majeure, vessel_loading | proposed |
| gt-novorossiysk-customs_border | novorossiysk | customs_border | — | — | — | — | — | empty |
| gt-novorossiysk-insurance_war_risk | novorossiysk | insurance_war_risk | Lloyd's Joint War Committee (Black Sea) | lmalloyds.com | industry_body | official | force_majeure | proposed |
| gt-novorossiysk-storage_operator | novorossiysk | storage_operator | — | — | — | — | — | empty |
| gt-novorossiysk-pricing_hub | novorossiysk | pricing_hub | — (Urals/CPC blend — global) | — | — | — | — | empty |
| gt-novorossiysk-weather_hazard | novorossiysk | weather_hazard | Bora wind closures | — | weather | official | port_closure | empty |
| gt-novorossiysk-sanctions_enforcement | novorossiysk | sanctions_enforcement | US OFAC / EU price cap (Urals) | ofac.treasury.gov | government_regulator | official | sanctions | proposed |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-novorossiysk-pipeline_operator (CPC) | **kazašský hlavní export** + Urals | Rusko kontroluje KZ export cestu | CPC marine terminál | proposed — KZ zranitelnost |
| gt-novorossiysk-sanctions_enforcement | price cap compliance | válka/drony | dark fleet | proposed |
| gt-novorossiysk-insurance_war_risk | — | **UA drony/USV na přístav+rafinerii (2024-25)** | war-risk premium | proposed |

### Unverified / Anti-patterns

- Ruské domény (`nmtp.info`, `transneft.ru`, `cpc.ru`) — dostupnost/sankce → unverified.
- **CPC klíč:** Novorossiysk = hlavní export kazašské ropy (propojit s `ca-KZ`); ruská kontrola = KZ pákový risk.
- pricing `empty` (Urals/CPC blend global); Bora vítr = pravidelné uzávěry.

### Progress po merge

`phase: geo_target`, `last_geo_target: novorossiysk`, `last_batch_seq: 82`
