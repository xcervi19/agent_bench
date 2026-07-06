# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_024_country_authority_IN.md  
**Fáze:** country_authority — krok IN (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-05  

---

## Shrnutí

Indie (`IN`), 10 slotů (`ca-IN-{authority}`). Velký importér, **kupuje diskontovaný ruský Urals**
(klíčový signál). **PPAC** měsíční data. Rafinerie Jamnagar (Reliance, největší). Burza v global (MCX).
9 `proposed`, 1 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-IN-ministry_petroleum | ministry_petroleum | Ministry of Petroleum & Natural Gas | mopng.gov.in | government_regulator | official | production, imports | proposed |
| ca-IN-noc | noc | ONGC | ongcindia.com | noc | official | production, imports, term_contract | proposed |
| ca-IN-mfa | mfa | Ministry of External Affairs | mea.gov.in | diplomacy | official | sanctions | proposed |
| ca-IN-customs_export | customs_export | CBIC / DGCIS (trade stats) | cbic.gov.in | government_regulator | official | imports, exports | proposed |
| ca-IN-upstream_regulator | upstream_regulator | DGH (Directorate Gen. of Hydrocarbons) | dghindia.gov.in | government_regulator | official | production | proposed |
| ca-IN-port_maritime_authority | port_maritime_authority | Ministry of Ports, Shipping & Waterways | shipmin.gov.in | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-IN-national_exchange | national_exchange | — (MCX in global) | — | — | — | — | empty |
| ca-IN-central_bank | central_bank | Reserve Bank of India (RBI) | rbi.org.in | government_regulator | official | sanctions | proposed |
| ca-IN-environment_regulator | environment_regulator | Ministry of Env, Forest & Climate | moef.gov.in | government_regulator | official | refinery_outage | proposed |
| ca-IN-coast_guard_navy | coast_guard_navy | Indian Coast Guard | indiancoastguard.gov.in | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-IN-customs_export (DGCIS/PPAC) | import mix | **ruský Urals discount** signál | port arrivals | proposed — PPAC (ppac.gov.in) klíč |
| ca-IN-noc (ONGC) | domácí produkce (klesající) | energy security | Jamnagar (private) refining | proposed — IOC/BPCL/HPCL expanze |

### Unverified / poznámky

- **`national_exchange` = empty:** pokryto global (`gl-exchange-010` MCX).
- **PPAC** (ppac.gov.in) — měsíční import/spotřeba data, expanze ministerstva; nejcennější.
- **Expanze NOC:** IOC (iocl.com), BPCL, HPCL — rafinerie; Reliance Jamnagar soukromé (mimo autority).
- Indie = swing kupec ruské ropy; discount/rupee settlement = geopolitický signál.

### Progress po merge

`last_country: IN`, `last_batch_seq: 24`
