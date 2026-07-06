# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_096_geo_target_btc.md  
**Fáze:** geo_target — krok btc (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Baku-Tbilisi-Ceyhan** (`btc`, pipeline_entity), 12 slotů. Azeri Light (BTC blend) do **Ceyhan (Středomoří)**
— **obchází Rusko + Hormuz + Bospor**. BP-operated. Klíč = **pipeline_operator (BTC Co) + loading_terminal
(Ceyhan)**; geo riziko Kavkaz. 3 `proposed`, 2 `unverified`, 7 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-btc-port_authority | btc | port_authority | — (Ceyhan via loading_terminal) | — | — | — | — | empty |
| gt-btc-pipeline_operator | btc | pipeline_operator | BTC Co (BP-operated) | bp.com | infrastructure | official | pipeline_outage | proposed |
| gt-btc-transit_naval | btc | transit_naval | — | — | — | — | — | empty |
| gt-btc-loading_terminal | btc | loading_terminal | Ceyhan Marine Terminal (Mediterranean export) | — | infrastructure | official | vessel_loading | unverified |
| gt-btc-national_noc | btc | national_noc | SOCAR (via ca-AZ) | socar.az | noc | official | production, exports | proposed |
| gt-btc-shipping_lane | btc | shipping_lane | — (Med AIS global) | — | — | — | — | empty |
| gt-btc-customs_border | btc | customs_border | — | — | — | — | — | empty |
| gt-btc-insurance_war_risk | btc | insurance_war_risk | Caucasus transit risk (Armenia-Azerbaijan/Georgia) | — | industry_body | official | force_majeure | unverified |
| gt-btc-storage_operator | btc | storage_operator | — | — | — | — | — | empty |
| gt-btc-pricing_hub | btc | pricing_hub | — (Azeri Light — global) | — | — | — | — | empty |
| gt-btc-weather_hazard | btc | weather_hazard | — | — | — | — | — | empty |
| gt-btc-sanctions_enforcement | btc | sanctions_enforcement | — | — | — | — | — | empty |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-btc-pipeline_operator (BP) | Azeri Light do Med | **obchází RU+Hormuz+Bospor** | Baku→Tbilisi→Ceyhan | proposed — strategický obchvat |
| gt-btc-insurance_war_risk | — | Nagorno-Karabakh, Gruzie tranzit | Kavkaz nestabilita | unverified |

### Unverified / Anti-patterns

- Ceyhan terminál doména unverified; SOCAR (`socar.az`) pod `ca-AZ` (dedup, ale relevantní pro BTC).
- **Ceyhan = i terminus KRG/Iraq-Turkey pipeline** (ITP — samostatný, od 2023 stojí); nezaměňovat s BTC.
- Strategická role: jediná velká non-Russian kaspická cesta do Středomoří.

### Progress po merge

`phase: geo_target`, `last_geo_target: btc`, `last_batch_seq: 96` — pipelines 1/3 (zbývá Druzhba, TANAP)
