# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_035_country_authority_NL.md  
**Fáze:** country_authority — krok NL (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Nizozemsko (`NL`), 10 slotů (`ca-NL-{authority}`). **ARA hub** (Rotterdam = největší EU ropný přístav) +
**TTF benchmark** (ICE Endex Amsterdam = evropský plyn). Groningen pole uzavřeno 2023/24. **EBN** státní E&P.
9 `proposed`, 1 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-NL-ministry_petroleum | ministry_petroleum | Ministry of Climate & Green Growth | rijksoverheid.nl | government_regulator | official | production, imports | proposed |
| ca-NL-noc | noc | EBN (Energie Beheer Nederland) | ebn.nl | noc | official | production, storage_levels | proposed |
| ca-NL-mfa | mfa | Ministry of Foreign Affairs | government.nl | diplomacy | official | sanctions | proposed |
| ca-NL-customs_export | customs_export | Dutch Customs (Douane) | belastingdienst.nl | government_regulator | official | imports, exports | proposed |
| ca-NL-upstream_regulator | upstream_regulator | SodM (State Supervision of Mines) | sodm.nl | government_regulator | official | production | proposed |
| ca-NL-port_maritime_authority | port_maritime_authority | Port of Rotterdam | portofrotterdam.com | infrastructure | official | vessel_loading, port_closure, storage_levels | proposed |
| ca-NL-national_exchange | national_exchange | ICE Endex (TTF gas) | ice.com | exchange | official | pricing_formula | proposed |
| ca-NL-central_bank | central_bank | De Nederlandsche Bank | dnb.nl | government_regulator | official | sanctions | proposed |
| ca-NL-environment_regulator | environment_regulator | ILT / Rijkswaterstaat | ilent.nl | government_regulator | official | refinery_outage | proposed |
| ca-NL-coast_guard_navy | coast_guard_navy | Netherlands Coastguard | kustwacht.nl | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-NL-port_maritime_authority (Rotterdam) | — | EU import gateway | **ARA hub, storage, refining** | proposed — nejvyšší logistics priorita |
| ca-NL-national_exchange (ICE Endex/TTF) | — | — | **TTF = EU gas benchmark** | proposed — Endex Amsterdam |

### Unverified / poznámky

- **Rotterdam** = geo cíl Fáze 3 (`rotterdam`); ARA (`ara`) storage/pricing hub.
- **TTF** klíčový EU gas benchmark; ICE Endex je i v global (`gl-exchange-002` ICE) — zde jako národní kontext.
- Groningen (uzavřeno) → NL z gas exportéra na importéra; strukturální obrat.

### Progress po merge

`last_country: NL`, `last_batch_seq: 35`
