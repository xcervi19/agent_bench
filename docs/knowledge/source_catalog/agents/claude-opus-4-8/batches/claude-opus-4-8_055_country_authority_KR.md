# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_055_country_authority_KR.md  
**Fáze:** country_authority — krok KR (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Jižní Korea (`KR`), 10 slotů (`ca-KR-{authority}`). **Top LNG + crude importér**, velký rafinér (SK/GS/S-Oil).
MOTIE politika, **KNOC** (SPR), **KOGAS** (LNG monopol importér). Vysoká transparentnost. 8 `proposed`, 1 `unverified`, 1 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-KR-ministry_petroleum | ministry_petroleum | MOTIE (Trade, Industry & Energy) | motie.go.kr | government_regulator | official | imports, storage_levels | proposed |
| ca-KR-noc | noc | KNOC (Korea National Oil Corp; SPR) | knoc.co.kr | noc | official | storage_levels, imports | proposed |
| ca-KR-mfa | mfa | Ministry of Foreign Affairs | mofa.go.kr | diplomacy | official | sanctions | proposed |
| ca-KR-customs_export | customs_export | Korea Customs Service | customs.go.kr | government_regulator | official | imports | proposed |
| ca-KR-upstream_regulator | upstream_regulator | MOTIE / KOGAS (LNG import) | kogas.or.kr | government_regulator | official | imports, storage_levels | proposed |
| ca-KR-port_maritime_authority | port_maritime_authority | Ministry of Oceans & Fisheries (ports) | mof.go.kr | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-KR-national_exchange | national_exchange | Korea Exchange (KRX) | krx.co.kr | exchange | official | pricing_formula | unverified |
| ca-KR-central_bank | central_bank | Bank of Korea | bok.or.kr | government_regulator | official | sanctions | proposed |
| ca-KR-environment_regulator | environment_regulator | Ministry of Environment | me.go.kr | government_regulator | official | refinery_outage | proposed |
| ca-KR-coast_guard_navy | coast_guard_navy | Korea Coast Guard | kcg.go.kr | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-KR-noc (KNOC) | SPR, crude import mix | Hormuz závislost (ME crude) | rafinerie Ulsan/Yeosu | proposed — demand signál |
| ca-KR-upstream_regulator (KOGAS) | LNG import monopol | — | LNG terminály | proposed — LNG demand |

### Poznámky

- Rafinérský export (nafta/benzin) do regionu → crack spread signál; sledovat KNOC/MOTIE data.
- KOGAS = dominantní LNG importér (JKM demand); závislost ME crude přes Hormuz.
- KRX (`krx.co.kr`) finanční, Tier 2 — unverified pro energy relevanci.

### Progress po merge

`last_country: KR`, `last_batch_seq: 55`
