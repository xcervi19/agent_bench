# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_010_country_authority_QA.md  
**Fáze:** country_authority — krok QA (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-05  

---

## Shrnutí

Katar (`QA`), 10 slotů (`ca-QA-{authority}`). Dominantní **LNG** hráč — **QatarEnergy** +
**Ras Laffan** terminal; North Field expansion signál. Ministerstvo energetiky personálně
splývá s QatarEnergy. 8 `proposed`, 1 `unverified`, 1 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-QA-ministry_petroleum | ministry_petroleum | Ministry of Energy Affairs | mopi.gov.qa | government_regulator | official | production, export_license | unverified |
| ca-QA-noc | noc | QatarEnergy | qatarenergy.qa | noc | official | production, exports, term_contract, pricing_formula | proposed |
| ca-QA-mfa | mfa | Ministry of Foreign Affairs | mofa.gov.qa | diplomacy | official | sanctions | proposed |
| ca-QA-customs_export | customs_export | General Authority of Customs | customs.gov.qa | government_regulator | official | exports | proposed |
| ca-QA-upstream_regulator | upstream_regulator | — | — | — | — | — | empty |
| ca-QA-port_maritime_authority | port_maritime_authority | Mwani Qatar | mwani.com.qa | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-QA-national_exchange | national_exchange | Qatar Stock Exchange | qe.com.qa | exchange | official | pricing_formula | proposed |
| ca-QA-central_bank | central_bank | Qatar Central Bank | qcb.gov.qa | government_regulator | official | sanctions | proposed |
| ca-QA-environment_regulator | environment_regulator | Ministry of Environment & Climate Change | mecc.gov.qa | government_regulator | official | refinery_outage | proposed |
| ca-QA-coast_guard_navy | coast_guard_navy | Qatar Coast Guard | — | diplomacy | official | port_closure | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-QA-noc (QatarEnergy) | LNG produkce, North Field expansion | dlouhodobé SPA (Asie/EU) | Ras Laffan loading | proposed — nejvyšší priorita |
| ca-QA-ministry_petroleum | — | — | — | unverified — doména mopi.gov.qa ověřit (splývá s QatarEnergy) |

### Unverified / poznámky

- **`ministry_petroleum` = unverified:** Ministr energetiky je zároveň CEO QatarEnergy; oddělený
  ministerský web (`mopi.gov.qa`) ověřit `/source-discover` — jinak sloučit do NOC.
- **`upstream_regulator` = empty:** integrováno pod QatarEnergy.
- **`coast_guard_navy` = empty:** bez oficiálního webu.
- **Ras Laffan** = samostatný geo cíl Fáze 3 (`ras_laffan`, lng_terminal).

### Progress po merge

`last_country: QA`, `last_batch_seq: 10`
