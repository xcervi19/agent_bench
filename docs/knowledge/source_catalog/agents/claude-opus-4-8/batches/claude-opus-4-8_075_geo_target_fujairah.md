# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_075_geo_target_fujairah.md  
**Fáze:** geo_target — krok fujairah (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Fujairah** (`fujairah`, load_port), 12 slotů. UAE východní pobřeží = **obchvat Hormuz** + bunker hub #3
+ **FEDCom týdenní zásoby produktů**. Klíč = **pipeline (ADNOC Habshan–Fujairah)**, **storage (FEDCom
feed)**, **insurance (2019 sabotáž tankerů)**. 6 `proposed`, 1 `unverified`, 5 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-fujairah-port_authority | fujairah | port_authority | Port of Fujairah | fujairahport.ae | infrastructure | official | port_closure, vessel_loading | proposed |
| gt-fujairah-pipeline_operator | fujairah | pipeline_operator | ADNOC Habshan–Fujairah (Hormuz bypass) | adnoc.ae | infrastructure | official | pipeline_outage | proposed |
| gt-fujairah-transit_naval | fujairah | transit_naval | — | — | — | — | — | empty |
| gt-fujairah-loading_terminal | fujairah | loading_terminal | ADNOC Fujairah crude terminal | adnoc.ae | infrastructure | official | vessel_loading | proposed |
| gt-fujairah-national_noc | fujairah | national_noc | ADNOC | adnoc.ae | noc | official | production, exports | proposed |
| gt-fujairah-shipping_lane | fujairah | shipping_lane | — (AIS global) | — | — | — | — | empty |
| gt-fujairah-customs_border | fujairah | customs_border | — | — | — | — | — | empty |
| gt-fujairah-insurance_war_risk | fujairah | insurance_war_risk | Lloyd's Joint War Committee (Gulf of Oman) | lmalloyds.com | industry_body | official | force_majeure | proposed |
| gt-fujairah-storage_operator | fujairah | storage_operator | FOIZ / FEDCom weekly oil product stocks | fujairahport.ae | infrastructure | data_feed | storage_levels | proposed |
| gt-fujairah-pricing_hub | fujairah | pricing_hub | — (Fujairah bunker/fuel oil via Platts global) | — | — | — | — | empty |
| gt-fujairah-weather_hazard | fujairah | weather_hazard | — (low) | — | — | — | — | empty |
| gt-fujairah-sanctions_enforcement | fujairah | sanctions_enforcement | Iranian oil STS off Fujairah — OFAC/UANI | ofac.treasury.gov | government_regulator | official | sanctions | unverified |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-fujairah-pipeline_operator | Hormuz obchvat (ADNOC) | strategická redundance | Habshan→Fujairah terminál | proposed |
| gt-fujairah-storage_operator | — | — | **FEDCom týdenní zásoby** (klíčový feed) | proposed |
| gt-fujairah-insurance_war_risk | — | 2019 sabotáž tankerů (Golf Ománu) | war-risk premium | proposed |

### Unverified / Anti-patterns

- **FEDCom** týdenní data produktů = high-value storage feed (ověřit URL pod fujairahport.ae).
- Iranian STS off Fujairah `unverified` — přes UANI/TankerTrackers, ne oficiální.
- pricing_hub `empty`: bunker/fuel oil pricing = globální (Platts).

### Progress po merge

`phase: geo_target`, `last_geo_target: fujairah`, `last_batch_seq: 75`
