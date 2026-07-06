# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_090_geo_target_yamal.md  
**Fáze:** geo_target — krok yamal (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Yamal LNG** (`yamal`, lng_terminal), 12 slotů. Ruský **arktický LNG** (Novatek, Sabetta) přes
**Severní mořskou cestu**. Klíč = **loading_terminal/NOC (Novatek)**, **shipping (NSR / led-třídní tankery)**,
**sanctions (Arctic LNG 2 pod sankcemi)**, **weather (arktický led)**. 3 `proposed`, 3 `unverified`, 6 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-yamal-port_authority | yamal | port_authority | Sabetta port | — | infrastructure | official | port_closure | unverified |
| gt-yamal-pipeline_operator | yamal | pipeline_operator | — (field-integrated) | — | — | — | — | empty |
| gt-yamal-transit_naval | yamal | transit_naval | — | — | — | — | — | empty |
| gt-yamal-loading_terminal | yamal | loading_terminal | Yamal LNG (Novatek) — Sabetta | novatek.ru | infrastructure | official | vessel_loading | unverified |
| gt-yamal-national_noc | yamal | national_noc | Novatek | novatek.ru | noc | official | production, exports | unverified |
| gt-yamal-shipping_lane | yamal | shipping_lane | Northern Sea Route Admin + ice-class tanker AIS | nsra.ru | shipping | data_feed | vessel_loading, force_majeure | proposed |
| gt-yamal-customs_border | yamal | customs_border | — | — | — | — | — | empty |
| gt-yamal-insurance_war_risk | yamal | insurance_war_risk | — | — | — | — | — | empty |
| gt-yamal-storage_operator | yamal | storage_operator | — (Zeebrugge/Montoir transshipment) | — | — | — | — | empty |
| gt-yamal-pricing_hub | yamal | pricing_hub | — (TTF/JKM — global) | — | — | — | — | empty |
| gt-yamal-weather_hazard | yamal | weather_hazard | Arctic ice / NSR season window | nsra.ru | weather | official | force_majeure | proposed |
| gt-yamal-sanctions_enforcement | yamal | sanctions_enforcement | US OFAC (Arctic LNG 2 sanctioned; Yamal operational) | ofac.treasury.gov | government_regulator | official | sanctions | proposed |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-yamal-national_noc (Novatek) | arktický LNG | **Arctic LNG 2 pod sankcemi** (Yamal běží) | Sabetta/NSR | unverified |
| gt-yamal-shipping_lane | — | led-třídní flotila (nedostatek) | NSR sezónní okno | proposed |
| gt-yamal-weather_hazard | — | — | led → letní/zimní routing (Asie vs EU) | proposed |

### Unverified / Anti-patterns

- Novatek/Sabetta domény unverified (sankce/dostupnost).
- **Arctic LNG 2** pod sankcemi (stagnuje) vs Yamal LNG (funkční) — rozlišovat.
- NSR sezónnost: v létě na východ (Asie), v zimě na západ (EU) → transshipment Zeebrugge/Montoir.

### Progress po merge

`phase: geo_target`, `last_geo_target: yamal`, `last_batch_seq: 90`
