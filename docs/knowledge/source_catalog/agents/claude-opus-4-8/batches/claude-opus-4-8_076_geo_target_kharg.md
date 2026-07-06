# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_076_geo_target_kharg.md  
**Fáze:** geo_target — krok kharg (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Kharg Island** (`kharg`, load_port), 12 slotů. **~90 % íránského crude exportu**. Pod sankcemi →
**stínová flotila, AIS spoofing, STS** (Malajsie/Fujairah), teapot rafinerie Shandong. Klíč =
**sanctions_enforcement (OFAC/UANI/TankerTrackers)**, **national_noc (NIOC/NITC)**. 2 `proposed`, 4 `unverified`, 6 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-kharg-port_authority | kharg | port_authority | Ports & Maritime Organization Iran (PMO) | pmo.ir | infrastructure | official | port_closure | unverified |
| gt-kharg-pipeline_operator | kharg | pipeline_operator | — | — | — | — | — | empty |
| gt-kharg-transit_naval | kharg | transit_naval | IRGC Navy | — | diplomacy | official | port_closure | empty |
| gt-kharg-loading_terminal | kharg | loading_terminal | NIOC Kharg terminal | nioc.ir | infrastructure | official | vessel_loading | unverified |
| gt-kharg-national_noc | kharg | national_noc | NIOC / NITC (tanker fleet) | nioc.ir | noc | official | production, exports | unverified |
| gt-kharg-shipping_lane | kharg | shipping_lane | Dark-fleet AIS gaps (TankerTrackers) | tankertrackers.com | shipping | data_feed | vessel_loading, sanctions | proposed |
| gt-kharg-customs_border | kharg | customs_border | — | — | — | — | — | empty |
| gt-kharg-insurance_war_risk | kharg | insurance_war_risk | — (Iranian self-insured / Kish P&I) | — | — | — | — | empty |
| gt-kharg-storage_operator | kharg | storage_operator | — (Kharg / floating storage) | — | — | — | — | empty |
| gt-kharg-pricing_hub | kharg | pricing_hub | — | — | — | — | — | empty |
| gt-kharg-weather_hazard | kharg | weather_hazard | — (low) | — | — | — | — | empty |
| gt-kharg-sanctions_enforcement | kharg | sanctions_enforcement | US OFAC + UANI (Iran crude → Shandong teapots) | ofac.treasury.gov | government_regulator | official | sanctions | proposed |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-kharg-national_noc (NIOC/NITC) | ~90% íránského exportu | **sankce → stínová flotila** | NITC vlastní tankery | unverified |
| gt-kharg-sanctions_enforcement | Iran→Čína toky | OFAC designace, price ceiling | STS off Malajsie/Fujairah | proposed |
| gt-kharg-shipping_lane | — | AIS spoofing/gaps | TankerTrackers rekonstrukce | proposed |

### Unverified / Anti-patterns

- **NIOC/PMO domény (`nioc.ir`/`pmo.ir`)** unverified — dostupnost kolísá pod sankcemi.
- Reálný signál = **UANI/TankerTrackers** rekonstrukce (dark fleet), ne íránské oficiální feedy.
- insurance/pricing `empty`: Iran mimo západní P&I; ceny mimo benchmarky (rabaty pro teapoty).

### Progress po merge

`phase: geo_target`, `last_geo_target: kharg`, `last_batch_seq: 76` — load ports 3/10
