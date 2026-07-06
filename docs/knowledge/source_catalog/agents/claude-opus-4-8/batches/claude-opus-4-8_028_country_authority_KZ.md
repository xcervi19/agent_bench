# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_028_country_authority_KZ.md  
**Fáze:** country_authority — krok KZ (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Kazachstán (`KZ`), 10 slotů (`ca-KZ-{authority}`). Klíč: **CPC pipeline** (Tengiz→Novorossiysk přes
Rusko) = zranitelnost exportu (Rusko může přerušit). Pole Tengiz/Kashagan/Karachaganak (Chevron/Exxon/Eni).
Landlocked (Caspian). 6 `proposed`, 2 `unverified`, 2 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-KZ-ministry_petroleum | ministry_petroleum | Ministry of Energy | energo.gov.kz | government_regulator | official | production, export_license | proposed |
| ca-KZ-noc | noc | KazMunayGas (KMG) | kmg.kz | noc | official | production, exports, term_contract | proposed |
| ca-KZ-mfa | mfa | Ministry of Foreign Affairs | gov.kz | diplomacy | official | sanctions | unverified |
| ca-KZ-customs_export | customs_export | State Revenue Committee | kgd.gov.kz | government_regulator | official | exports | proposed |
| ca-KZ-upstream_regulator | upstream_regulator | — | — | — | — | — | empty |
| ca-KZ-port_maritime_authority | port_maritime_authority | Aktau Port (Caspian) | — | infrastructure | official | vessel_loading, pipeline_outage | unverified |
| ca-KZ-national_exchange | national_exchange | KASE | kase.kz | exchange | official | pricing_formula | proposed |
| ca-KZ-central_bank | central_bank | National Bank of Kazakhstan | nationalbank.kz | government_regulator | official | sanctions | proposed |
| ca-KZ-environment_regulator | environment_regulator | Ministry of Ecology | gov.kz | government_regulator | official | refinery_outage | unverified |
| ca-KZ-coast_guard_navy | coast_guard_navy | — (Caspian, no oil transit navy) | — | — | — | — | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-KZ-noc (KMG) | Tengiz/Kashagan produkce | **CPC přes Rusko** = leverage | CPC → Novorossiysk | proposed — CPC (cpc.ru) klíčová expanze |
| ca-KZ-ministry_petroleum | export routing | KEBCO rebrand (odlišení od ruské ropy) | BTC alternativa | proposed |

### Unverified / poznámky

- **CPC (Caspian Pipeline Consortium, cpc.ru)** = expanze; opakované "údržbové" přerušení Ruskem = price signál.
- **KEBCO** (Kazakhstan Export Blend) — rebrand CPC Blend pro odlišení od sankcionované ruské ropy.
- **Unverified:** MFA/Ecology (gov.kz sub-paths), Aktau port.
- Alternativní export: BTC (přes Ázerbájdžán), trans-Caspian — diversifikační signál.

### Progress po merge

`last_country: KZ`, `last_batch_seq: 28`
