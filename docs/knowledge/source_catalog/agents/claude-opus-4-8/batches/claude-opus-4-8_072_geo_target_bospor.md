# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_072_geo_target_bospor.md  
**Fáze:** geo_target — krok bospor (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Turkish Straits (Bospor + Dardanely)** (`bospor`, chokepoint), 12 slotů. Montreux; **ruská ropa +
CPC z Novorossijsku** tudy proudí. Klíč = **port_authority (Kıyı Emniyeti — tanker scheduling)**,
**weather (mlha → uzávěry)**, **sanctions (turecké pojišťovací kontroly — 2022 tanker jam)**,
**insurance (JWC Černé moře)**. 5 `proposed`, 1 `unverified`, 6 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-bospor-port_authority | bospor | port_authority | Directorate General of Coastal Safety (Kıyı Emniyeti) | kiyiemniyeti.gov.tr | infrastructure | official | port_closure, vessel_loading | proposed |
| gt-bospor-pipeline_operator | bospor | pipeline_operator | — (bypass: BTC/Kirkuk-Ceyhan mimo Bospor) | — | — | — | — | empty |
| gt-bospor-transit_naval | bospor | transit_naval | Turkish Navy | — | diplomacy | official | port_closure | empty |
| gt-bospor-loading_terminal | bospor | loading_terminal | — | — | — | — | — | empty |
| gt-bospor-national_noc | bospor | national_noc | — | — | — | — | — | empty |
| gt-bospor-shipping_lane | bospor | shipping_lane | Turkish Straits VTS + agency (Tribeca) transit reports | kiyiemniyeti.gov.tr | shipping | data_feed | vessel_loading, port_closure | proposed |
| gt-bospor-customs_border | bospor | customs_border | — | — | — | — | — | empty |
| gt-bospor-insurance_war_risk | bospor | insurance_war_risk | Lloyd's Joint War Committee (Black Sea listed) | lmalloyds.com | industry_body | official | force_majeure | proposed |
| gt-bospor-storage_operator | bospor | storage_operator | — | — | — | — | — | empty |
| gt-bospor-pricing_hub | bospor | pricing_hub | — | — | — | — | — | empty |
| gt-bospor-weather_hazard | bospor | weather_hazard | Kıyı Emniyeti (fog/current closures) | kiyiemniyeti.gov.tr | weather | official | port_closure | proposed |
| gt-bospor-sanctions_enforcement | bospor | sanctions_enforcement | Turkish insurance-verification checks + OFAC price cap | ofac.treasury.gov | government_regulator | official | sanctions | unverified |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-bospor-port_authority | ruský Urals + CPC (Novorossiysk) | Montreux; válečné omezení průjezdu | **tanker scheduling/queue** | proposed |
| gt-bospor-weather_hazard | — | — | **mlha → uzávěry, fronty** | proposed — pravidelný delay |
| gt-bospor-sanctions_enforcement | price cap compliance | 2022 turecká pojišťovací kontrola = jam | P&I letter checks | unverified |

### Unverified / Anti-patterns

- Turecké pojišťovací kontroly (2022) způsobily tanker jam → propojeno s price cap; scope se mění → unverified.
- pipeline_operator `empty`: BTC/Kirkuk-Ceyhan obcházejí Bospor (samostatné pipeline geo cíle).
- CPC/Novorossiysk load port = batch dále; zde jen tranzit.

### Progress po merge

`phase: geo_target`, `last_geo_target: bospor`, `last_batch_seq: 72`
