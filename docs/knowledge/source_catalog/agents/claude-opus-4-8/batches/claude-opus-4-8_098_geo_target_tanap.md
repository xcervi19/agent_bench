# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_098_geo_target_tanap.md  
**Fáze:** geo_target — krok tanap (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**TANAP** (`tanap`, pipeline_entity), 12 slotů. Součást **Southern Gas Corridor**: ázerbájdžánský plyn
(Shah Deniz II) → TANAP → TAP → EU = **non-Russian plyn diverzifikace**. Klíč = **pipeline_operator
(SOCAR/BOTAŞ)**, **NOC (SOCAR)**. 2 `proposed`, 0 `unverified`, 10 `empty`.

### Navržené sloty (klíčové)

| id | subject | entity | domain | category | signals | status |
|----|---------|--------|--------|----------|---------|--------|
| gt-tanap-pipeline_operator | pipeline_operator | TANAP (SOCAR/BOTAŞ) — Southern Gas Corridor | tanap.com | infrastructure | pipeline_outage | proposed |
| gt-tanap-national_noc | national_noc | SOCAR (Shah Deniz op. BP; via ca-AZ) | socar.az | noc | production, exports | proposed |

### Poznámky

- Shah Deniz II → TANAP → TAP → Itálie/EU = klíčová non-Russian plyn cesta (EU diverzifikace po 2022).
- Ostatní sloty `empty` (gas pipeline; pricing hub-linked globální; Kavkaz proximity).
- Propojení s `ca-AZ` (SOCAR) a `gt-btc` (stejný koridor, ropa vs plyn).

### Progress po merge

`phase: geo_target`, `last_geo_target: tanap`, `last_batch_seq: 98` — **Fáze 3 (geo_target) KOMPLETNÍ (32/32)**
