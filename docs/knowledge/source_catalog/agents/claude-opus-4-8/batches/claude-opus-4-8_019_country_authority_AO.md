# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_019_country_authority_AO.md  
**Fáze:** country_authority — krok AO (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-05  

---

## Shrnutí

Angola (`AO`), 10 slotů (`ca-AO-{authority}`). **Opustila OPEC (led 2024)** kvůli kvótovému sporu —
klíčový geopolitický signál. Klesající zralá deepwater produkce. **ANPG** koncesionář/data. 6 `proposed`, 4 `unverified`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-AO-ministry_petroleum | ministry_petroleum | MIREMPET (Min. Mineral Res., Petroleum & Gas) | mirempet.gov.ao | government_regulator | official | production, export_license | proposed |
| ca-AO-noc | noc | Sonangol | sonangol.co.ao | noc | official | production, exports, term_contract | proposed |
| ca-AO-mfa | mfa | Ministry of External Relations (MIREX) | mirex.gov.ao | diplomacy | official | sanctions | unverified |
| ca-AO-customs_export | customs_export | AGT (Administração Geral Tributária) | agt.minfin.gov.ao | government_regulator | official | exports | unverified |
| ca-AO-upstream_regulator | upstream_regulator | ANPG | anpg.co.ao | government_regulator | official | production, export_license | proposed |
| ca-AO-port_maritime_authority | port_maritime_authority | Port of Luanda / IMPA | portoluanda.co.ao | infrastructure | official | vessel_loading, port_closure | unverified |
| ca-AO-national_exchange | national_exchange | BODIVA | bodiva.ao | exchange | official | pricing_formula | unverified |
| ca-AO-central_bank | central_bank | Banco Nacional de Angola | bna.ao | government_regulator | official | sanctions | proposed |
| ca-AO-environment_regulator | environment_regulator | Ministry of Environment | — | government_regulator | official | refinery_outage | empty |
| ca-AO-coast_guard_navy | coast_guard_navy | Angolan Navy | — | diplomacy | official | port_closure | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-AO-noc (Sonangol) | klesající deepwater produkce | **odchod z OPEC 2024** | offshore FPSO loadings | proposed |
| ca-AO-upstream_regulator (ANPG) | produkce, licenční kola | — | — | proposed — koncesionářská data |

### Unverified / poznámky

- **Unverified/empty:** MIREX, AGT, Port of Luanda, BODIVA — nestabilní/nejisté domény.
- Odchod z OPEC = Angola bez kvótových omezení → produkční strategie čistě komerční.
- Deepwater (Girassol, Kaombo) zralá pole, klesající output — dlouhodobý bearish supply.

### Progress po merge

`last_country: AO`, `last_batch_seq: 19`
