# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_073_geo_target_gibraltar.md  
**Fáze:** geo_target — krok gibraltar (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Strait of Gibraltar** (`gibraltar`, chokepoint), 12 slotů. Vstup do Středomoří; **bunker hub
(Gibraltar/Algeciras/Ceuta)** + **STS zóna sankcionované ropy**. Nízké uzavírací riziko.
Klíč = **port_authority (bunkering)**, **sanctions (STS Russian/Iranian off Ceuta)**. 3 `proposed`, 2 `unverified`, 7 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-gibraltar-port_authority | gibraltar | port_authority | Gibraltar Port Authority / Algeciras (APBA) | gibraltarport.com | infrastructure | official | vessel_loading | proposed |
| gt-gibraltar-pipeline_operator | gibraltar | pipeline_operator | — | — | — | — | — | empty |
| gt-gibraltar-transit_naval | gibraltar | transit_naval | Royal Navy Gibraltar | — | diplomacy | official | port_closure | empty |
| gt-gibraltar-loading_terminal | gibraltar | loading_terminal | — | — | — | — | — | empty |
| gt-gibraltar-national_noc | gibraltar | national_noc | — | — | — | — | — | empty |
| gt-gibraltar-shipping_lane | gibraltar | shipping_lane | Gibraltar Port Authority (bunkering/Strait VTS) | gibraltarport.com | shipping | official | vessel_loading | proposed |
| gt-gibraltar-customs_border | gibraltar | customs_border | — | — | — | — | — | empty |
| gt-gibraltar-insurance_war_risk | gibraltar | insurance_war_risk | — (low) | — | — | — | — | empty |
| gt-gibraltar-storage_operator | gibraltar | storage_operator | Algeciras/Gibraltar bunker storage (VTTI/Cepsa) | — | infrastructure | official | storage_levels | unverified |
| gt-gibraltar-pricing_hub | gibraltar | pricing_hub | — (bunker prices via Platts global) | — | — | — | — | empty |
| gt-gibraltar-weather_hazard | gibraltar | weather_hazard | Levanter wind (bunkering delays) | — | weather | official | port_closure | unverified |
| gt-gibraltar-sanctions_enforcement | gibraltar | sanctions_enforcement | STS Russian/Iranian oil off Ceuta — OFAC/EU | ofac.treasury.gov | government_regulator | official | sanctions | proposed |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-gibraltar-port_authority | Med vstup | UK/ES suverénní spor | **bunker hub #3 Evropy** | proposed |
| gt-gibraltar-sanctions_enforcement | STS sankcionovaná ropa | Grace 1/Adrian Darya 2019 precedent | STS off Ceuta/Laconia Gulf | proposed |

### Unverified / Anti-patterns

- Bunker storage operátoři (VTTI/Cepsa) doména unverified.
- **Levanter** vítr = bunkering delay signál (unverified feed).
- Nízké uzavírací riziko; hodnota = bunker + STS monitoring, ne closure.

### Progress po merge

`phase: geo_target`, `last_geo_target: gibraltar`, `last_batch_seq: 73` — chokepointy KOMPLETNÍ (7/7)
