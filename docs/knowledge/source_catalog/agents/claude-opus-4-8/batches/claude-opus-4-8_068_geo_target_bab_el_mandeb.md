# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_068_geo_target_bab_el_mandeb.md  
**Fáze:** geo_target — krok bab_el_mandeb (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Bab el-Mandeb** (`bab_el_mandeb`, chokepoint), 12 slotů. Vstup do Rudého moře / Suezu; od 2023 **útoky
Húsíů** → přesměrování kolem Mysu Dobré naděje (delší cesty, freight ↑). Klíč = **transit_naval
(EU Aspides / CTF-153)**, **UKMTO**, **Lloyd's JWC**, **OFAC (Húsí designace)**. 5 `proposed`, 1 `unverified`, 6 `empty`.

### Navržené sloty

| id | geo_target | subject | entity | domain | category | type | signals | status |
|----|-----------|---------|--------|--------|----------|------|---------|--------|
| gt-bab_el_mandeb-port_authority | bab_el_mandeb | port_authority | — (strait; Aden/Hodeidah via ca-YE) | — | — | — | — | empty |
| gt-bab_el_mandeb-pipeline_operator | bab_el_mandeb | pipeline_operator | Saudi Petroline (East-West → Yanbu, Red Sea bypass) | aramco.com | infrastructure | official | pipeline_outage | proposed |
| gt-bab_el_mandeb-transit_naval | bab_el_mandeb | transit_naval | EU Op Aspides + US CTF-153 (CMF) | eeas.europa.eu | diplomacy | official | force_majeure, port_closure | proposed |
| gt-bab_el_mandeb-loading_terminal | bab_el_mandeb | loading_terminal | — | — | — | — | — | empty |
| gt-bab_el_mandeb-national_noc | bab_el_mandeb | national_noc | — | — | — | — | — | empty |
| gt-bab_el_mandeb-shipping_lane | bab_el_mandeb | shipping_lane | UKMTO + Ambrey/incident reporting | ukmto.org | shipping | official | force_majeure, port_closure | proposed |
| gt-bab_el_mandeb-customs_border | bab_el_mandeb | customs_border | — | — | — | — | — | empty |
| gt-bab_el_mandeb-insurance_war_risk | bab_el_mandeb | insurance_war_risk | Lloyd's Joint War Committee (Red Sea listed) | lmalloyds.com | industry_body | official | force_majeure | proposed |
| gt-bab_el_mandeb-storage_operator | bab_el_mandeb | storage_operator | — | — | — | — | — | empty |
| gt-bab_el_mandeb-pricing_hub | bab_el_mandeb | pricing_hub | — | — | — | — | — | empty |
| gt-bab_el_mandeb-weather_hazard | bab_el_mandeb | weather_hazard | — (low) | — | — | — | — | empty |
| gt-bab_el_mandeb-sanctions_enforcement | bab_el_mandeb | sanctions_enforcement | US OFAC (Houthi/Ansarallah designation) | ofac.treasury.gov | government_regulator | official | sanctions | unverified |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gt-bab_el_mandeb-transit_naval | Rudé moře / Suez tok | **Húsí útoky (od 2023)** | Aspides eskorty | proposed — aktivní disruption |
| gt-bab_el_mandeb-shipping_lane (UKMTO) | ~12% seaborne obchodu | drony/rakety | přesměrování kolem Afriky | proposed — freight ↑, dny navíc |

### Unverified / Anti-patterns

- OFAC Húsí designace `unverified` — status/scope se mění (re-listing FTO).
- Bab el-Mandeb + Suez propojené: přesměrování zde = pokles Suez tranzitu (batch 069).
- Aden/Hodeidah přístavy pod `ca-YE`, zde ne (bez duplicity).

### Progress po merge

`phase: geo_target`, `last_geo_target: bab_el_mandeb`, `last_batch_seq: 68`
