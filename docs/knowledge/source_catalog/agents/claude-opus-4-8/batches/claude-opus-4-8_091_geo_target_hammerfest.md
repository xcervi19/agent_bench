# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_091_geo_target_hammerfest.md  
**Fáze:** geo_target — krok hammerfest (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Hammerfest LNG (Melkøya)** (`hammerfest`, lng_terminal), 12 slotů. **Jediný evropský LNG export
terminál** (Equinor, Snøhvit). Malý objem, ale symbolický pro EU. Klíč = **NOC/terminal (Equinor)**,
**pipeline (Snøhvit)**. Precedent 2020–22 požár. 4 `proposed`, 0 `unverified`, 8 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-hammerfest-port_authority | hammerfest | port_authority | — (Kystverket / via ca-NO) | — | — | — | — | empty |
| gt-hammerfest-pipeline_operator | hammerfest | pipeline_operator | Snøhvit field pipeline (Equinor) | equinor.com | infrastructure | official | pipeline_outage | proposed |
| gt-hammerfest-transit_naval | hammerfest | transit_naval | — | — | — | — | — | empty |
| gt-hammerfest-loading_terminal | hammerfest | loading_terminal | Hammerfest LNG / Melkøya (Equinor) | equinor.com | infrastructure | official | vessel_loading, refinery_outage | proposed |
| gt-hammerfest-national_noc | hammerfest | national_noc | Equinor (state-controlled) | equinor.com | noc | official | production, exports | proposed |
| gt-hammerfest-shipping_lane | hammerfest | shipping_lane | — (AIS global) | — | — | — | — | empty |
| gt-hammerfest-customs_border | hammerfest | customs_border | — | — | — | — | — | empty |
| gt-hammerfest-insurance_war_risk | hammerfest | insurance_war_risk | — | — | — | — | — | empty |
| gt-hammerfest-storage_operator | hammerfest | storage_operator | — | — | — | — | — | empty |
| gt-hammerfest-pricing_hub | hammerfest | pricing_hub | — (TTF — global) | — | — | — | — | empty |
| gt-hammerfest-weather_hazard | hammerfest | weather_hazard | — (Arctic weather) | — | — | — | — | empty |
| gt-hammerfest-sanctions_enforcement | hammerfest | sanctions_enforcement | — | — | — | — | — | empty |
| gt-hammerfest-upstream_context | hammerfest | pricing_hub | Gassco (NO gas system — via ca-NO) | — | — | — | — | empty |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-hammerfest-loading_terminal | jediný EU LNG export | NO jako spolehlivý dodavatel | Melkøya (Snøhvit) | proposed |
| gt-hammerfest-national_noc (Equinor) | malý objem | — | **2020-22 požár = precedent výpadku** | proposed |

### Unverified / Anti-patterns

- Malý objem (~4-5 Mtpa), ale jediný evropský LNG export → symbolická/marginální relevance.
- 2020-22 Melkøya požár = precedent (dlouhý restart).
- Většina slotů `empty`; NO plyn systém (Gassco) pod `ca-NO` — bez duplicity.
- Poznámka: přebytečný řádek `upstream_context` je pouze anotace (empty), ne validní geo_subject.

### Progress po merge

`phase: geo_target`, `last_geo_target: hammerfest`, `last_batch_seq: 91` — LNG terminály 3/4 (zbývá Cove Point)
