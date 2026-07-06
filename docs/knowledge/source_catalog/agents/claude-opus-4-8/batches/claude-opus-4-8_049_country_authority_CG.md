# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_049_country_authority_CG.md  
**Fáze:** country_authority — krok CG (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Kongo-Brazzaville (`CG`), 10 slotů (`ca-CG-{authority}`). **OPEC člen**; **SNPC** NOC; export **Djeno terminál**
(Pointe-Noire). Djeno Blend crude. Opaque, oil-backed dluh. 3 `proposed`, 4 `unverified`, 3 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-CG-ministry_petroleum | ministry_petroleum | Ministry of Hydrocarbons | — | government_regulator | official | production, export_license | unverified |
| ca-CG-noc | noc | SNPC | snpc.cg | noc | official | production, exports | unverified |
| ca-CG-mfa | mfa | Ministry of Foreign Affairs | — | diplomacy | official | sanctions | empty |
| ca-CG-customs_export | customs_export | — | — | — | — | — | empty |
| ca-CG-upstream_regulator | upstream_regulator | Ministry of Hydrocarbons | — | government_regulator | official | production | unverified |
| ca-CG-port_maritime_authority | port_maritime_authority | Port de Pointe-Noire / Djeno terminal | — | infrastructure | official | vessel_loading | unverified |
| ca-CG-national_exchange | national_exchange | — (BVMAC regional) | — | — | — | — | empty |
| ca-CG-central_bank | central_bank | BEAC (regional CEMAC) | beac.int | government_regulator | official | sanctions | proposed |
| ca-CG-environment_regulator | environment_regulator | Ministry of Environment | — | government_regulator | official | refinery_outage | proposed |
| ca-CG-coast_guard_navy | coast_guard_navy | Congolese Navy | — | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-CG-noc (SNPC) | Djeno Blend; OPEC kvóta | oil-backed dluh (Glencore/Trafigura) | Djeno export terminál | unverified |

### Poznámky

- **OPEC člen** → produkce přes OPEC MOMR.
- SNPC (`snpc.cg`) ověřit; export Djeno (Pointe-Noire) → AIS + operátoři (TotalEnergies/Eni/Perenco).
- Prepaid ropné kontrakty s tradery = struktura, ne přímý spot signál.

### Progress po merge

`last_country: CG`, `last_batch_seq: 49`
