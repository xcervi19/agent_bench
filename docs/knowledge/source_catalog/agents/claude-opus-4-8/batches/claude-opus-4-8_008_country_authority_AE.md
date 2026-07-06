# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_008_country_authority_AE.md  
**Fáze:** country_authority — krok AE (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-05  

---

## Shrnutí

SAE (`AE`), 10 slotů (`ca-AE-{authority}`). Trading signál: **Murban benchmark** (ICE Futures
Abu Dhabi / IFAD) + **Fujairah** bunkering/storage hub. 8 `proposed`, 2 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-AE-ministry_petroleum | ministry_petroleum | Ministry of Energy & Infrastructure | moei.gov.ae | government_regulator | official | production, export_license | proposed |
| ca-AE-noc | noc | ADNOC | adnoc.ae | noc | official | production, exports, term_contract, pricing_formula | proposed |
| ca-AE-mfa | mfa | Ministry of Foreign Affairs | mofa.gov.ae | diplomacy | official | sanctions | proposed |
| ca-AE-customs_export | customs_export | Federal Customs Authority | fca.gov.ae | government_regulator | official | exports, export_license | proposed |
| ca-AE-upstream_regulator | upstream_regulator | — | — | — | — | — | empty |
| ca-AE-port_maritime_authority | port_maritime_authority | AD Ports Group | adports.ae | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-AE-national_exchange | national_exchange | ICE Futures Abu Dhabi (Murban) | theice.com | exchange | official | pricing_formula, term_contract | proposed |
| ca-AE-central_bank | central_bank | Central Bank of UAE | centralbank.ae | government_regulator | official | sanctions | proposed |
| ca-AE-environment_regulator | environment_regulator | Ministry of Climate Change & Env | moccae.gov.ae | government_regulator | official | refinery_outage | proposed |
| ca-AE-coast_guard_navy | coast_guard_navy | UAE Navy / Coastal Protection | — | diplomacy | official | port_closure | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-AE-noc (ADNOC) | produkce, spare capacity | OPEC+ (kvótový spor 2023) | Fujairah, Ruwais, Jebel Ali | proposed — nejvyšší priorita |
| ca-AE-national_exchange (IFAD) | — | — | Murban benchmark (ICE-operated) | proposed — crude pricing zde, ne ADX |

### Unverified / poznámky

- **`upstream_regulator` = empty:** integrováno pod ADNOC + MoEI.
- **`coast_guard_navy` = empty:** bez oficiálního webu; Hormuz transit přes MFA + AIS.
- **Fujairah** (mimo Hormuz, bunkering/storage) — samostatný geo cíl ve Fázi 3 (`fujairah`).
- ADX (Abu Dhabi Securities Exchange) je finanční; crude pricing přes IFAD/Murban → do slotu IFAD.

### Progress po merge

`last_country: AE`, `last_batch_seq: 8`
