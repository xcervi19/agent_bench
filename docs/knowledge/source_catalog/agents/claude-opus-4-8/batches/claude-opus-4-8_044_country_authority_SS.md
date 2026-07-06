# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_044_country_authority_SS.md  
**Fáze:** country_authority — krok SS (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Jižní Súdán (`SS`), 10 slotů (`ca-SS-{authority}`). Landlocked producent; export **jen přes súdánskou
pipeline do Port Sudan** → extrémní závislost + chronické force majeure (súdánská válka). **Nilepet** NOC.
2 `proposed`, 3 `unverified`, 5 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-SS-ministry_petroleum | ministry_petroleum | Ministry of Petroleum | mop.gov.ss | government_regulator | official | production, export_license | unverified |
| ca-SS-noc | noc | Nilepet | — | noc | official | production, exports | unverified |
| ca-SS-mfa | mfa | Ministry of Foreign Affairs | — | diplomacy | official | sanctions | empty |
| ca-SS-customs_export | customs_export | — | — | — | — | — | empty |
| ca-SS-upstream_regulator | upstream_regulator | — | — | — | — | — | empty |
| ca-SS-port_maritime_authority | port_maritime_authority | — (landlocked; uses Port Sudan) | — | — | — | — | empty |
| ca-SS-national_exchange | national_exchange | — | — | — | — | — | empty |
| ca-SS-central_bank | central_bank | Bank of South Sudan | — | government_regulator | official | sanctions | unverified |
| ca-SS-environment_regulator | environment_regulator | — | — | — | — | — | empty |
| ca-SS-coast_guard_navy | coast_guard_navy | — (landlocked) | — | — | — | — | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-SS-noc (Nilepet) | Dar/Nile Blend produkce | závislost na SD pipeline | Port Sudan export (přes SD) | unverified — export mimo kontrolu SS |

### Unverified / poznámky

- **Landlocked:** port/coast_guard `empty`; jediná export cesta = SD pipeline → Port Sudan.
- Súdánská válka opakovaně přerušuje export → SS produkce shut-in = supply signál.
- Data řídká; reálný signál přes operátory (Dar Petroleum/CNPC) + AIS Port Sudan.

### Progress po merge

`last_country: SS`, `last_batch_seq: 44`
