# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_088_geo_target_corpus_christi.md  
**Fáze:** geo_target — krok corpus_christi (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Corpus Christi** (`corpus_christi`, us_gulf_hub), 12 slotů. **Největší US crude export přístav**
(Permian light sweet výstup) + Cheniere CC LNG. Klíč = **port (Port of CC)**, **pipeline (Permian:
Cactus/EPIC/Gray Oak + CC feedgas)**, **weather (hurricany)**. 4 `proposed`, 1 `unverified`, 7 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-corpus_christi-port_authority | corpus_christi | port_authority | Port of Corpus Christi Authority | portofcc.com | infrastructure | official | port_closure, vessel_loading | proposed |
| gt-corpus_christi-pipeline_operator | corpus_christi | pipeline_operator | Permian pipes (Cactus/EPIC/Gray Oak) + Cheniere CC feedgas | cheniere.com | infrastructure | official | pipeline_outage | proposed |
| gt-corpus_christi-transit_naval | corpus_christi | transit_naval | — | — | — | — | — | empty |
| gt-corpus_christi-loading_terminal | corpus_christi | loading_terminal | Crude docks + Cheniere Corpus Christi LNG | portofcc.com | infrastructure | official | vessel_loading | proposed |
| gt-corpus_christi-national_noc | corpus_christi | national_noc | — (no NOC) | — | — | — | — | empty |
| gt-corpus_christi-shipping_lane | corpus_christi | shipping_lane | — (AIS global) | — | — | — | — | empty |
| gt-corpus_christi-customs_border | corpus_christi | customs_border | — | — | — | — | — | empty |
| gt-corpus_christi-insurance_war_risk | corpus_christi | insurance_war_risk | — | — | — | — | — | empty |
| gt-corpus_christi-storage_operator | corpus_christi | storage_operator | — (PADD3 via EIA global) | — | — | — | — | empty |
| gt-corpus_christi-pricing_hub | corpus_christi | pricing_hub | — (WTI Midland / MEH — global) | — | — | — | — | empty |
| gt-corpus_christi-weather_hazard | corpus_christi | weather_hazard | NOAA NHC (Gulf hurricanes) | nhc.noaa.gov | weather | official | hurricane, port_closure | proposed |
| gt-corpus_christi-sanctions_enforcement | corpus_christi | sanctions_enforcement | — (FERC LNG for CCL) | ferc.gov | government_regulator | official | export_license | unverified |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-corpus_christi-port_authority | **největší US crude export** (Permian) | US export dominance | WTI Midland výstup | proposed |
| gt-corpus_christi-pipeline_operator | Permian light sweet → dock | — | Cactus/EPIC/Gray Oak | proposed |
| gt-corpus_christi-loading_terminal | + Cheniere CC LNG | — | crude + LNG | proposed |

### Unverified / Anti-patterns

- pricing `empty`: WTI Midland/MEH = globální pricing vrstva.
- Dvojí role: crude export (Permian) + LNG (Cheniere CC) — oba sledovat.
- Permian pipeline takeaway kapacita = strukturální (playbook), ne per-slot.

### Progress po merge

`phase: geo_target`, `last_geo_target: corpus_christi`, `last_batch_seq: 88` — US Gulf KOMPLETNÍ (5/5)
