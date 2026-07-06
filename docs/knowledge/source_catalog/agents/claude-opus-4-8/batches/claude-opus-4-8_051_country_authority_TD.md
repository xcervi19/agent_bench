# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_051_country_authority_TD.md  
**Fáze:** country_authority — krok TD (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Čad (`TD`), 10 slotů (`ca-TD-{authority}`). **Landlocked** producent; export **pipeline Čad–Kamerun → Kribi**
(Doba blend). SHT NOC (po odchodu ExxonMobil/Savannah). Opaque. 2 `proposed`, 4 `unverified`, 4 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-TD-ministry_petroleum | ministry_petroleum | Ministry of Petroleum & Energy | — | government_regulator | official | production, export_license | unverified |
| ca-TD-noc | noc | Société des Hydrocarbures du Tchad (SHT) | — | noc | official | production, exports | unverified |
| ca-TD-mfa | mfa | Ministry of Foreign Affairs | — | diplomacy | official | sanctions | empty |
| ca-TD-customs_export | customs_export | — | — | — | — | — | empty |
| ca-TD-upstream_regulator | upstream_regulator | Ministry of Petroleum | — | government_regulator | official | production | unverified |
| ca-TD-port_maritime_authority | port_maritime_authority | — (landlocked; export via Kribi, CM) | — | — | — | — | empty |
| ca-TD-national_exchange | national_exchange | — (BVMAC regional) | — | — | — | — | empty |
| ca-TD-central_bank | central_bank | BEAC (regional CEMAC) | beac.int | government_regulator | official | sanctions | proposed |
| ca-TD-environment_regulator | environment_regulator | Ministry of Environment | — | government_regulator | official | refinery_outage | unverified |
| ca-TD-coast_guard_navy | coast_guard_navy | — (landlocked) | — | — | — | — | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-TD-noc (SHT) | Doba blend | Exxon/Savannah odchod → SHT převzetí | **pipeline přes CM → Kribi** | unverified — export mimo TD |

### Poznámky

- **Landlocked:** port/coast_guard `empty`; export výhradně **Čad–Kamerun pipeline → Kribi (CM)**.
- Pipeline outage / spor s Kamerunem = force majeure signál.
- Nízká transparentnost; sledovat operátory + Kribi terminál (AIS).

### Progress po merge

`last_country: TD`, `last_batch_seq: 51`
