# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_033_country_authority_GB.md  
**Fáze:** country_authority — krok GB (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Velká Británie (`GB`), 10 slotů (`ca-GB-{authority}`). **Žádný NOC** (BP/Shell soukromé). North Sea
pokles + windfall tax (EPL). **Brent benchmark** (ICE London — v global). Sankce přes **OFSI**. 8 `proposed`, 2 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-GB-ministry_petroleum | ministry_petroleum | Dept for Energy Security & Net Zero (DESNZ) | gov.uk | government_regulator | official | production, export_license | proposed |
| ca-GB-noc | noc | — | — | — | — | — | empty |
| ca-GB-mfa | mfa | Foreign, Commonwealth & Dev Office (FCDO) | gov.uk | diplomacy | official | sanctions | proposed |
| ca-GB-customs_export | customs_export | HMRC | gov.uk | government_regulator | official | exports | proposed |
| ca-GB-upstream_regulator | upstream_regulator | North Sea Transition Authority (NSTA) | nstauthority.co.uk | government_regulator | official | production | proposed |
| ca-GB-port_maritime_authority | port_maritime_authority | Maritime & Coastguard Agency (MCA) | gov.uk | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-GB-national_exchange | national_exchange | — (ICE London/Brent in global) | — | — | — | — | empty |
| ca-GB-central_bank | central_bank | Bank of England | bankofengland.co.uk | government_regulator | official | sanctions | proposed |
| ca-GB-environment_regulator | environment_regulator | OPRED / Environment Agency | gov.uk | government_regulator | official | refinery_outage | proposed |
| ca-GB-coast_guard_navy | coast_guard_navy | HM Coastguard (MCA) | gov.uk | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-GB-upstream_regulator (NSTA) | North Sea produkce (klesající) | windfall tax (EPL) investiční signál | Forties/Sullom Voe | proposed |
| ca-GB-mfa (FCDO) | — | sankce (OFSI enforcement) | shadow fleet insurance (P&I London) | proposed |

### Unverified / poznámky

- **`ca-GB-noc` = empty:** žádný NOC (BP/Shell soukromé).
- **`ca-GB-national_exchange` = empty:** Brent na ICE (global `gl-exchange-002`).
- **OFSI** (Office of Financial Sanctions Implementation, Treasury) — sankční enforcement, expanze MFA.
- Londýn = centrum P&I pojištění (shadow fleet compliance) — geo signál.
- Mnoho GB úřadů pod `gov.uk` sub-path — validovat konkrétní stránky.

### Progress po merge

`last_country: GB`, `last_batch_seq: 33`
