# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_079_geo_target_jebel_ali.md  
**Fáze:** geo_target — krok jebel_ali (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Jebel Ali** (`jebel_ali`, load_port), 12 slotů. Největší umělý přístav světa (DP World); bunker/produkty/
kontejnery + **Dubaj re-export hub (sankční sledování)**. **Uvnitř Hormuz** (ne obchvat). Klíč = **port
(DP World)**, **storage/NOC (ENOC)**, **sanctions (re-export)**. 2 `proposed`, 4 `unverified`, 6 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-jebel_ali-port_authority | jebel_ali | port_authority | DP World / Jebel Ali Port | dpworld.com | infrastructure | official | port_closure, vessel_loading | proposed |
| gt-jebel_ali-pipeline_operator | jebel_ali | pipeline_operator | — | — | — | — | — | empty |
| gt-jebel_ali-transit_naval | jebel_ali | transit_naval | — (US Navy port of call) | — | — | — | — | empty |
| gt-jebel_ali-loading_terminal | jebel_ali | loading_terminal | ENOC Jebel Ali products terminal | enoc.com | infrastructure | official | vessel_loading | unverified |
| gt-jebel_ali-national_noc | jebel_ali | national_noc | ENOC (Dubai) | enoc.com | noc | official | refinery_outage | unverified |
| gt-jebel_ali-shipping_lane | jebel_ali | shipping_lane | — (AIS global) | — | — | — | — | empty |
| gt-jebel_ali-customs_border | jebel_ali | customs_border | Dubai Customs | dubaicustoms.gov.ae | government_regulator | official | imports, exports | unverified |
| gt-jebel_ali-insurance_war_risk | jebel_ali | insurance_war_risk | — (inside Hormuz; JWC Gulf) | — | — | — | — | empty |
| gt-jebel_ali-storage_operator | jebel_ali | storage_operator | Jebel Ali storage (ENOC / Vopak Horizon) | — | infrastructure | official | storage_levels | unverified |
| gt-jebel_ali-pricing_hub | jebel_ali | pricing_hub | — | — | — | — | — | empty |
| gt-jebel_ali-weather_hazard | jebel_ali | weather_hazard | — | — | — | — | — | empty |
| gt-jebel_ali-sanctions_enforcement | jebel_ali | sanctions_enforcement | Dubai re-export node — OFAC (evasion watch) | ofac.treasury.gov | government_regulator | official | sanctions | proposed |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-jebel_ali-port_authority (DP World) | produkty/bunker | uvnitř Hormuz (ne obchvat) | největší umělý přístav | proposed |
| gt-jebel_ali-sanctions_enforcement | — | **Dubaj = re-export/evasion uzel** | trade flows | proposed |

### Unverified / Anti-patterns

- ENOC/Dubai Customs/Vopak domény unverified — ověřit.
- **Pozor:** Jebel Ali je uvnitř Hormuz → NENÍ obchvat (na rozdíl od Fujairah). Uzavření Hormuz ho odřízne.
- Hodnota spíš products/bunker/trade než crude export.

### Progress po merge

`phase: geo_target`, `last_geo_target: jebel_ali`, `last_batch_seq: 79`
