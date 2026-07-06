# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_039_country_authority_ES.md  
**Fáze:** country_authority — krok ES (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Španělsko (`ES`), 10 slotů (`ca-ES-{authority}`). **Největší EU LNG import kapacita** (6 terminálů) +
**Enagás** (gas TSO) + **MIBGAS** (iberský gas hub). Medgaz z Alžírska. Omezené propojení do zbytku EU
(MidCat/BarMar). Žádný NOC (Repsol soukromé). 9 `proposed`, 1 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-ES-ministry_petroleum | ministry_petroleum | Ministry for Ecological Transition (MITECO) | miteco.gob.es | government_regulator | official | imports | proposed |
| ca-ES-noc | noc | — | — | — | — | — | empty |
| ca-ES-mfa | mfa | Ministry of Foreign Affairs | exteriores.gob.es | diplomacy | official | sanctions | proposed |
| ca-ES-customs_export | customs_export | Agencia Tributaria (Aduanas) | agenciatributaria.es | government_regulator | official | imports, exports | proposed |
| ca-ES-upstream_regulator | upstream_regulator | CNMC (regulator) | cnmc.es | government_regulator | official | pricing_formula | proposed |
| ca-ES-port_maritime_authority | port_maritime_authority | Puertos del Estado / Enagás | enagas.es | infrastructure | official | vessel_loading, storage_levels | proposed |
| ca-ES-national_exchange | national_exchange | MIBGAS (Iberian gas market) | mibgas.es | exchange | official | pricing_formula, storage_levels | proposed |
| ca-ES-central_bank | central_bank | Banco de España | bde.es | government_regulator | official | sanctions | proposed |
| ca-ES-environment_regulator | environment_regulator | MITECO | miteco.gob.es | government_regulator | official | refinery_outage | proposed |
| ca-ES-coast_guard_navy | coast_guard_navy | Salvamento Marítimo | salvamentomaritimo.es | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-ES-port_maritime_authority (Enagás) | — | EU LNG gateway | **6 LNG terminálů, regas send-out** | proposed — nejcennější |
| ca-ES-national_exchange (MIBGAS) | — | — | iberský gas benchmark | proposed |

### Unverified / poznámky

- **`ca-ES-noc` = empty:** Repsol soukromé.
- **MidCat/BarMar** (H2Med) — chybějící propojení ES→FR limituje ES jako EU gas gateway (geopolitický signál).
- Medgaz (Alžírsko→ES) = pipeline; Gibraltar geo blízko (`gibraltar`).
- Enagás = gas TSO (storage, LNG) — vysoká data hodnota.

### Progress po merge

`last_country: ES`, `last_batch_seq: 39`
