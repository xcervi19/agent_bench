# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_064_country_authority_TT.md  
**Fáze:** country_authority — krok TT (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Trinidad & Tobago (`TT`), 10 slotů (`ca-TT-{authority}`). **LNG exportér** (Atlantic LNG) + petrochemie
(čpavek/metanol); plyn v úpadku → **Dragon gas deal s Venezuelou** (přeshraniční, sankční výjimka). 7 `proposed`, 2 `unverified`, 1 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-TT-ministry_petroleum | ministry_petroleum | Ministry of Energy & Energy Industries | energy.gov.tt | government_regulator | official | production, export_license | proposed |
| ca-TT-noc | noc | Heritage Petroleum / NGC | ngc.co.tt | noc | official | production, exports | proposed |
| ca-TT-mfa | mfa | Ministry of Foreign Affairs | foreign.gov.tt | diplomacy | official | sanctions | unverified |
| ca-TT-customs_export | customs_export | Customs & Excise Division | customs.gov.tt | government_regulator | official | exports | unverified |
| ca-TT-upstream_regulator | upstream_regulator | Ministry of Energy (MEEI) | energy.gov.tt | government_regulator | official | production, export_license | proposed |
| ca-TT-port_maritime_authority | port_maritime_authority | Point Fortin (Atlantic LNG) / Pt Lisas | — | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-TT-national_exchange | national_exchange | — | — | — | — | — | empty |
| ca-TT-central_bank | central_bank | Central Bank of Trinidad & Tobago | central-bank.org.tt | government_regulator | official | sanctions | proposed |
| ca-TT-environment_regulator | environment_regulator | Environmental Management Authority | ema.co.tt | government_regulator | official | refinery_outage | proposed |
| ca-TT-coast_guard_navy | coast_guard_navy | TT Coast Guard | — | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-TT-noc (NGC) | plyn decline; LNG/petrochem feedgas | **Dragon gas deal s VE** (OFAC licence) | Atlantic LNG (Point Fortin) | proposed — cross-border VE plyn |

### Poznámky

- **Dragon/Cocuina gas:** dohoda s Venezuelou o dovozu plynu → sankční výjimky OFAC = klíčový geo/supply signál (propojit s VE).
- Plyn decline → Atlantic LNG train utilization, čpavek/metanol feedgas omezení.
- Atlantic LNG (Point Fortin) restrukturalizace = kapacita/export signál.

### Progress po merge

`last_country: TT`, `last_batch_seq: 64`
