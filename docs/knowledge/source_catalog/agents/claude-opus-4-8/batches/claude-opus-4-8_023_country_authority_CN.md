# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_023_country_authority_CN.md  
**Fáze:** country_authority — krok CN (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-05  

---

## Shrnutí

Čína (`CN`), 10 slotů (`ca-CN-{authority}`). **Největší importér** — **GACC customs** data jsou
klíč pro ruské/íránské toky (dark fleet destinace). Tři NOC (CNPC/Sinopec/CNOOC). SPR/teapot
rafinerie neprůhledné. Burza už v global (INE/SHFE). 8 `proposed`, 2 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-CN-ministry_petroleum | ministry_petroleum | National Energy Administration (NEA) | nea.gov.cn | government_regulator | official | production, imports, storage_levels | proposed |
| ca-CN-noc | noc | CNPC (PetroChina) | cnpc.com.cn | noc | official | production, imports, term_contract | proposed |
| ca-CN-mfa | mfa | Ministry of Foreign Affairs | fmprc.gov.cn | diplomacy | official | sanctions | proposed |
| ca-CN-customs_export | customs_export | General Admin of Customs (GACC) | customs.gov.cn | government_regulator | official | imports, exports | proposed |
| ca-CN-upstream_regulator | upstream_regulator | Ministry of Natural Resources | mnr.gov.cn | government_regulator | official | production | proposed |
| ca-CN-port_maritime_authority | port_maritime_authority | Maritime Safety Admin (MSA) | msa.gov.cn | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-CN-national_exchange | national_exchange | — (INE/SHFE in global) | — | — | — | — | empty |
| ca-CN-central_bank | central_bank | People's Bank of China (PBOC) | pbc.gov.cn | government_regulator | official | sanctions | proposed |
| ca-CN-environment_regulator | environment_regulator | Ministry of Ecology & Environment | mee.gov.cn | government_regulator | official | refinery_outage | proposed |
| ca-CN-coast_guard_navy | coast_guard_navy | China Coast Guard | — | diplomacy | official | port_closure | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-CN-customs_export (GACC) | import objemy | **ruský/íránský crude destinace** | port arrivals | proposed — nejcennější data (cross-check dark fleet) |
| ca-CN-noc (CNPC) | domácí produkce, rafinace | SPR builds (neprůhledné) | Qingdao/Ningbo/Dalian | proposed — Sinopec/CNOOC expanze |

### Unverified / poznámky

- **`national_exchange` = empty:** pokryto global (`gl-exchange-003` INE, `gl-exchange-005` SHFE).
- **`coast_guard_navy` = empty:** bez použitelného webu; JV/SCS geopolitika přes MFA.
- **Expanze NOC:** `ca-CN-noc__sinopec` (sinopec.com), `ca-CN-noc__cnooc` (cnooc.com.cn).
- **NDRC** (ndrc.gov.cn) — cenová/SPR politika, jako expanze ministerstva.
- Teapot rafinerie (Shandong) + neoznámené SPR = klíč pro apparent demand odhady.

### Progress po merge

`last_country: CN`, `last_batch_seq: 23`
