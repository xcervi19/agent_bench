# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_056_country_authority_SG.md  
**Fáze:** country_authority — krok SG (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Singapur (`SG`), 10 slotů (`ca-SG-{authority}`). **Není producent**, ale **klíčový trading/refining/bunker hub**
Asie (Platts MOC okno, Jurong Island rafinerie, bunker #1). Malacca chokepoint. 7 `proposed`, 1 `unverified`, 2 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-SG-ministry_petroleum | ministry_petroleum | Ministry of Trade & Industry / EMA | ema.gov.sg | government_regulator | official | imports, storage_levels | proposed |
| ca-SG-noc | noc | — (no NOC; trading hub) | — | — | — | — | empty |
| ca-SG-mfa | mfa | Ministry of Foreign Affairs | mfa.gov.sg | diplomacy | official | sanctions | proposed |
| ca-SG-customs_export | customs_export | Singapore Customs | customs.gov.sg | government_regulator | official | imports, exports | proposed |
| ca-SG-upstream_regulator | upstream_regulator | EMA (Energy Market Authority) | ema.gov.sg | government_regulator | official | pricing_formula | proposed |
| ca-SG-port_maritime_authority | port_maritime_authority | MPA (Maritime & Port Authority) | mpa.gov.sg | infrastructure | official | vessel_loading, port_closure, bunker | proposed |
| ca-SG-national_exchange | national_exchange | SGX (Singapore Exchange) | sgx.com | exchange | official | pricing_formula | proposed |
| ca-SG-central_bank | central_bank | MAS (Monetary Authority) | mas.gov.sg | government_regulator | official | sanctions | proposed |
| ca-SG-environment_regulator | environment_regulator | NEA (National Environment Agency) | nea.gov.sg | government_regulator | official | refinery_outage | unverified |
| ca-SG-coast_guard_navy | coast_guard_navy | Police Coast Guard / RSN | police.gov.sg | diplomacy | official | port_closure | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-SG-port_maritime_authority (MPA) | bunker #1 world, transshipment | **Malacca chokepoint** | Jurong/Pulau Bukom | proposed — hub logistika |
| ca-SG-national_exchange (SGX) | freight/fuel deriváty | — | — | proposed — pricing |

### Poznámky

- **`ca-SG-noc` = empty:** trading hub bez NOC; hodnota = **Platts Singapore MOC okno** (regionální benchmark).
- MPA = klíč pro bunker/transshipment; Jurong Island rafinerie (Shell/ExxonMobil).
- **Malacca** chokepoint (geo layer) — propojit s gt-* geo target.

### Progress po merge

`last_country: SG`, `last_batch_seq: 56`
