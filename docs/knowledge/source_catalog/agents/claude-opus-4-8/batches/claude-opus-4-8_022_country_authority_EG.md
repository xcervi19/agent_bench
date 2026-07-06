# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_022_country_authority_EG.md  
**Fáze:** country_authority — krok EG (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-05  

---

## Shrnutí

Egypt (`EG`), 10 slotů (`ca-EG-{authority}`). Spíš **tranzit než producent**: **Suez Canal + SUMED**
pipeline (Suez už v global `gl-shipping-005`). Klesající plyn (Zohr) → střídavě LNG importér.
8 `proposed`, 1 `unverified`, 1 pozn (Suez v global).

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-EG-ministry_petroleum | ministry_petroleum | Ministry of Petroleum & Mineral Res. | petroleum.gov.eg | government_regulator | official | production, imports | proposed |
| ca-EG-noc | noc | EGPC / EGAS | egas.com.eg | noc | official | production, imports, term_contract | proposed |
| ca-EG-mfa | mfa | Ministry of Foreign Affairs | mfa.gov.eg | diplomacy | official | sanctions | proposed |
| ca-EG-customs_export | customs_export | Egyptian Customs Authority | customs.gov.eg | government_regulator | official | exports, imports | proposed |
| ca-EG-upstream_regulator | upstream_regulator | Ganope / EGPC (upstream) | ganope.com | government_regulator | official | production | unverified |
| ca-EG-port_maritime_authority | port_maritime_authority | SUMED (Arab Petroleum Pipelines) | — | infrastructure | official | vessel_loading, pipeline_outage | unverified |
| ca-EG-national_exchange | national_exchange | Egyptian Exchange (EGX) | egx.com.eg | exchange | official | pricing_formula | proposed |
| ca-EG-central_bank | central_bank | Central Bank of Egypt | cbe.org.eg | government_regulator | official | sanctions | proposed |
| ca-EG-environment_regulator | environment_regulator | EEAA | eeaa.gov.eg | government_regulator | official | refinery_outage | proposed |
| ca-EG-coast_guard_navy | coast_guard_navy | Egyptian Navy | — | diplomacy | official | port_closure | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-EG-port_maritime_authority (SUMED) | — | Suez alternativa (Sidi Kerir↔Ain Sukhna) | crude transit bypass Suez | unverified — klíč pro transit signál |
| ca-EG-noc (EGAS) | Zohr plyn pokles | Israel gas import (Leviathan) | Idku/Damietta LNG (import i export) | proposed |

### Unverified / poznámky

- **Suez Canal Authority** je už v global (`gl-shipping-005`) — zde neduplikovat; port slot proto SUMED.
- **Unverified:** Ganope (`ganope.com`), SUMED (doména k ověření).
- Egypt = swing tranzit/LNG hub: import izraelského plynu, re-export přes Idku/Damietta když je kapacita.
- Bab el-Mandeb/Red Sea (Houthi) útoky přesměrovávají tankery od Suezu → EG tranzitní příjmy signál.

### Progress po merge

`last_country: EG`, `last_batch_seq: 22`
