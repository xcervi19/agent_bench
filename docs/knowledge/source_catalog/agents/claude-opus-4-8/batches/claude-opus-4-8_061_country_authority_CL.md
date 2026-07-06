# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_061_country_authority_CL.md  
**Fáze:** country_authority — krok CL (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Chile (`CL`), 10 slotů (`ca-CL-{authority}`). **Energetický importér** (crude/LNG); ENAP = malý státní
rafinér, žádná ropná produkce. Quintero/Mejillones LNG. Copper-centrická ekonomika. 6 `proposed`, 2 `unverified`, 2 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-CL-ministry_petroleum | ministry_petroleum | Ministry of Energy | energia.gob.cl | government_regulator | official | imports | proposed |
| ca-CL-noc | noc | ENAP (refiner/importer) | enap.cl | noc | official | imports, refinery_outage | proposed |
| ca-CL-mfa | mfa | Ministry of Foreign Affairs | minrel.gob.cl | diplomacy | official | sanctions | proposed |
| ca-CL-customs_export | customs_export | Servicio Nacional de Aduanas | aduana.cl | government_regulator | official | imports | unverified |
| ca-CL-upstream_regulator | upstream_regulator | CNE (Comisión Nacional de Energía) | cne.cl | government_regulator | official | pricing_formula | proposed |
| ca-CL-port_maritime_authority | port_maritime_authority | DIRECTEMAR / Quintero LNG | directemar.cl | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-CL-national_exchange | national_exchange | — | — | — | — | — | empty |
| ca-CL-central_bank | central_bank | Banco Central de Chile | bcentral.cl | government_regulator | official | sanctions | proposed |
| ca-CL-environment_regulator | environment_regulator | SMA (Superintendencia Medio Ambiente) | sma.gob.cl | government_regulator | official | refinery_outage | unverified |
| ca-CL-coast_guard_navy | coast_guard_navy | Armada de Chile / DIRECTEMAR | armada.cl | diplomacy | official | port_closure | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-CL-noc (ENAP) | žádná produkce; import mix | stabilní demokracie | Quintero/Mejillones LNG | proposed — demand signál |

### Poznámky

- Čistý importér; hodnota = demand + LNG import (Quintero/Mejillones), ne supply.
- Historicky argentinský plyn (výpadky) → LNG přechod; sledovat i AR flows.
- Nízká geopolitická rizikovost (stabilní).

### Progress po merge

`last_country: CL`, `last_batch_seq: 61`
