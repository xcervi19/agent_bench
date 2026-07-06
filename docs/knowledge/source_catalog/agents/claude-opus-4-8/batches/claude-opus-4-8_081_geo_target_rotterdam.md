# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_081_geo_target_rotterdam.md  
**Fáze:** geo_target — krok rotterdam (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Rotterdam** (`rotterdam`, load_port), 12 slotů. Největší evropský přístav = jádro **ARA hubu**
(rafinace/skladování/pricing). Klíč = **port_authority (Port of Rotterdam)**, **storage (ARA + Insights
Global týdenní stocks)**, **pipeline (Rotterdam-Rhine → německé rafinerie)**. NL autority pod `ca-NL`. 3 `proposed`, 2 `unverified`, 7 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-rotterdam-port_authority | rotterdam | port_authority | Port of Rotterdam Authority | portofrotterdam.com | infrastructure | official | port_closure, vessel_loading | proposed |
| gt-rotterdam-pipeline_operator | rotterdam | pipeline_operator | Rotterdam-Rhine Pipeline (RRP → DE refineries) | — | infrastructure | official | pipeline_outage | unverified |
| gt-rotterdam-transit_naval | rotterdam | transit_naval | — | — | — | — | — | empty |
| gt-rotterdam-loading_terminal | rotterdam | loading_terminal | — (refineries: Shell Pernis, Gunvor, Esso) | — | — | — | — | empty |
| gt-rotterdam-national_noc | rotterdam | national_noc | — (no NOC) | — | — | — | — | empty |
| gt-rotterdam-shipping_lane | rotterdam | shipping_lane | — (via ca-NL) | — | — | — | — | empty |
| gt-rotterdam-customs_border | rotterdam | customs_border | — (Dutch Customs via ca-NL) | — | — | — | — | empty |
| gt-rotterdam-insurance_war_risk | rotterdam | insurance_war_risk | — | — | — | — | — | empty |
| gt-rotterdam-storage_operator | rotterdam | storage_operator | ARA storage (Vopak/Koole) + Insights Global weekly ARA stocks | insights-global.com | infrastructure | data_feed | storage_levels | proposed |
| gt-rotterdam-pricing_hub | rotterdam | pricing_hub | ARA barge / gasoil hub (ICE Gasoil, Platts) | — | industry_body | data_feed | pricing_formula | unverified |
| gt-rotterdam-weather_hazard | rotterdam | weather_hazard | — (Rhine low-water affects barges) | — | — | — | — | empty |
| gt-rotterdam-sanctions_enforcement | rotterdam | sanctions_enforcement | — | — | — | — | — | empty |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-rotterdam-storage_operator | **Insights Global týdenní ARA stocks** | — | Vopak/Koole tanky | proposed — klíčový EU feed |
| gt-rotterdam-port_authority | NW Evropa import/rafinace | — | největší EU přístav | proposed |
| gt-rotterdam-pipeline_operator | crude do DE rafinerií | — | Rotterdam-Rhine (RRP) | unverified |

### Unverified / Anti-patterns

- **Insights Global (PJK)** týdenní ARA stocks = high-value NW Europe storage feed.
- Rhine low-water (sucho) → omezení barge = logistický signál (weather empty pro teď, sledovat).
- NL autority (customs, MFA, exchange) pod `ca-NL` — bez duplicity.

### Progress po merge

`phase: geo_target`, `last_geo_target: rotterdam`, `last_batch_seq: 81` — load ports 8/10 (zbývá Novorossiysk, Kozmino)
