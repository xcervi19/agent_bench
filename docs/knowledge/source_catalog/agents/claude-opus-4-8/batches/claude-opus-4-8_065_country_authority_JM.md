# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_065_country_authority_JM.md  
**Fáze:** country_authority — krok JM (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Jamajka (`JM`), 10 slotů (`ca-JM-{authority}`). **Malý importér**, bez produkce; LNG (Old Harbour, New Fortress),
Petrojam malá rafinerie. Marginální trading význam. 5 `proposed`, 2 `unverified`, 3 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-JM-ministry_petroleum | ministry_petroleum | Ministry of Science, Energy & Tech | mset.gov.jm | government_regulator | official | imports | proposed |
| ca-JM-noc | noc | Petrojam / PCJ | petrojam.com | noc | official | imports, refinery_outage | unverified |
| ca-JM-mfa | mfa | Ministry of Foreign Affairs | mfaft.gov.jm | diplomacy | official | sanctions | unverified |
| ca-JM-customs_export | customs_export | Jamaica Customs Agency | jacustoms.gov.jm | government_regulator | official | imports | proposed |
| ca-JM-upstream_regulator | upstream_regulator | — (no upstream) | — | — | — | — | empty |
| ca-JM-port_maritime_authority | port_maritime_authority | Port Authority of Jamaica / Old Harbour LNG | portjam.com | infrastructure | official | vessel_loading | proposed |
| ca-JM-national_exchange | national_exchange | — | — | — | — | — | empty |
| ca-JM-central_bank | central_bank | Bank of Jamaica | boj.org.jm | government_regulator | official | sanctions | proposed |
| ca-JM-environment_regulator | environment_regulator | NEPA | nepa.gov.jm | government_regulator | official | refinery_outage | proposed |
| ca-JM-coast_guard_navy | coast_guard_navy | Jamaica Defence Force Coast Guard | — | diplomacy | official | port_closure | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-JM-port_maritime_authority | žádná produkce | stabilní | New Fortress LNG (Old Harbour/Montego Bay) | proposed — marginální demand |

### Poznámky

- **Marginální** význam: čistý importér, malý objem; hodnota = New Fortress LNG kotva (Caribbean).
- `ca-JM-upstream_regulator` = empty (žádný upstream).
- Většina signálu jen lokální; nízká priorita pro global trading.

### Progress po merge

`last_country: JM`, `last_batch_seq: 65`
