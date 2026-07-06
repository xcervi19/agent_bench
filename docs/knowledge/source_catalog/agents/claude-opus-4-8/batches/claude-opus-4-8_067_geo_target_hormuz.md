# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_067_geo_target_hormuz.md  
**Fáze:** geo_target — krok hormuz (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Strait of Hormuz** (`hormuz`, chokepoint), 12 slotů (`gt-hormuz-{subject}`). ~20 % globálního ropného
tranzitu + katarský LNG. Klíč = **transit_naval (5. flotila/CMF)**, **shipping_lane (UKMTO)**,
**insurance (Lloyd's JWC)**, **bypass pipelines (ADNOC Habshan–Fujairah, Saudi Petroline)**,
**sanctions (OFAC/UANI dark fleet)**. 6 `proposed`, 1 `unverified`, 5 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-hormuz-port_authority | hormuz | port_authority | — (strait, no single port) | — | — | — | — | empty |
| gt-hormuz-pipeline_operator | hormuz | pipeline_operator | ADNOC Habshan–Fujairah + Saudi Petroline (bypass) | adnoc.ae | infrastructure | official | pipeline_outage | proposed |
| gt-hormuz-transit_naval | hormuz | transit_naval | US NAVCENT / 5th Fleet + Combined Maritime Forces (Bahrain) | centcom.mil | diplomacy | official | force_majeure, port_closure | proposed |
| gt-hormuz-loading_terminal | hormuz | loading_terminal | — (see load ports: Ras Tanura/Kharg/Fujairah) | — | — | — | — | empty |
| gt-hormuz-national_noc | hormuz | national_noc | — (multiple: Aramco/ADNOC/NIOC/QatarEnergy) | — | — | — | — | empty |
| gt-hormuz-shipping_lane | hormuz | shipping_lane | UKMTO (UK Maritime Trade Operations) | ukmto.org | shipping | official | force_majeure, port_closure | proposed |
| gt-hormuz-customs_border | hormuz | customs_border | — | — | — | — | — | empty |
| gt-hormuz-insurance_war_risk | hormuz | insurance_war_risk | Lloyd's Joint War Committee (LMA) | lmalloyds.com | industry_body | official | force_majeure | proposed |
| gt-hormuz-storage_operator | hormuz | storage_operator | Port of Fujairah (bypass storage hub) | fujairahport.ae | infrastructure | data_feed | storage_levels | unverified |
| gt-hormuz-pricing_hub | hormuz | pricing_hub | — (Platts Dubai / DME Oman — global layer) | — | — | — | — | empty |
| gt-hormuz-weather_hazard | hormuz | weather_hazard | — (low) | — | — | — | — | empty |
| gt-hormuz-sanctions_enforcement | hormuz | sanctions_enforcement | US OFAC + UANI (dark fleet tracking) | ofac.treasury.gov | government_regulator | official | sanctions | proposed |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-hormuz-transit_naval | ~20% světové ropy | **IRGC uzavírací hrozby** | konvoje/eskorty | proposed — hlavní tail-risk |
| gt-hormuz-pipeline_operator | bypass kapacita ~2,6 mb/d (UAE+SA) | omezuje uzavírací pákový efekt | Fujairah/Yanbu obchvat | proposed |
| gt-hormuz-shipping_lane (UKMTO) | — | incidenty/GPS jamming | real-time hlášení | proposed |

### Unverified / Anti-patterns

- **`fujairahport.ae`** unverified — ověřit doménu FEDCom/storage feed.
- port_authority/loading_terminal/national_noc `empty` — pokryto load-port geo cíli + `ca-*` autoritami (bez duplicity).
- Bypass kapacita (Habshan–Fujairah + Petroline) = klíč: úplné uzavření Hormuz je jen částečně obejitelné.

### Progress po merge

`phase: geo_target`, `last_geo_target: hormuz`, `last_batch_seq: 67`
