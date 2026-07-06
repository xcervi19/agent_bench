# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_048_country_authority_GQ.md  
**Fáze:** country_authority — krok GQ (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Rovníková Guinea (`GQ`), 10 slotů (`ca-GQ-{authority}`). **OPEC člen**, klesající produkce (Zafiro/Ceiba);
**LNG Punta Europa** (Bioko). GEPetrol NOC, ministerstvo MMH. Opaque režim. 3 `proposed`, 4 `unverified`, 3 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-GQ-ministry_petroleum | ministry_petroleum | Ministry of Mines & Hydrocarbons | — | government_regulator | official | production, export_license | unverified |
| ca-GQ-noc | noc | GEPetrol | — | noc | official | production, exports | unverified |
| ca-GQ-mfa | mfa | Ministry of Foreign Affairs | — | diplomacy | official | sanctions | empty |
| ca-GQ-customs_export | customs_export | — | — | — | — | — | empty |
| ca-GQ-upstream_regulator | upstream_regulator | Ministry MMH | — | government_regulator | official | production | unverified |
| ca-GQ-port_maritime_authority | port_maritime_authority | Malabo / Punta Europa LNG | — | infrastructure | official | vessel_loading | unverified |
| ca-GQ-national_exchange | national_exchange | — (BVMAC regional) | — | — | — | — | empty |
| ca-GQ-central_bank | central_bank | BEAC (regional CEMAC) | beac.int | government_regulator | official | sanctions | proposed |
| ca-GQ-environment_regulator | environment_regulator | Ministry MMH | — | government_regulator | official | refinery_outage | proposed |
| ca-GQ-coast_guard_navy | coast_guard_navy | Equatoguinean Navy | — | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-GQ-noc (GEPetrol) | Zafiro/Ceiba decline; OPEC | opaque režim | Punta Europa LNG | unverified — nízká transparentnost |

### Poznámky

- **OPEC člen** → produkce/kvóta přes OPEC MOMR, ne národní úřad.
- LNG Punta Europa (feedgas decline) = supply signál; sledovat přes operátory (Marathon/Trident).
- Regionální CEMAC: centrální banka BEAC (`beac.int`), burza BVMAC (empty).

### Progress po merge

`last_country: GQ`, `last_batch_seq: 48`
