# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_027_country_authority_AU.md  
**Fáze:** country_authority — krok AU (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-05  

---

## Shrnutí

Austrálie (`AU`), 10 slotů (`ca-AU-{authority}`). **Žádný NOC** (Woodside/Santos soukromé). Hlavní
**LNG exportér** (NWS, Gorgon, Wheatstone, Gladstone CSG-LNG) — konkurent Kataru/USA pro asijský LNG.
**NOPSEMA** offshore regulátor. 8 `proposed`, 2 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-AU-ministry_petroleum | ministry_petroleum | Dept of Industry, Science & Resources | industry.gov.au | government_regulator | official | production, export_license | proposed |
| ca-AU-noc | noc | — | — | — | — | — | empty |
| ca-AU-mfa | mfa | Dept of Foreign Affairs & Trade (DFAT) | dfat.gov.au | diplomacy | official | sanctions | proposed |
| ca-AU-customs_export | customs_export | Australian Border Force | abf.gov.au | government_regulator | official | exports | proposed |
| ca-AU-upstream_regulator | upstream_regulator | NOPSEMA | nopsema.gov.au | government_regulator | official | production, force_majeure | proposed |
| ca-AU-port_maritime_authority | port_maritime_authority | AMSA (Maritime Safety Authority) | amsa.gov.au | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-AU-national_exchange | national_exchange | ASX | asx.com.au | exchange | official | pricing_formula | proposed |
| ca-AU-central_bank | central_bank | Reserve Bank of Australia | rba.gov.au | government_regulator | official | — | proposed |
| ca-AU-environment_regulator | environment_regulator | DCCEEW | dcceew.gov.au | government_regulator | official | refinery_outage | proposed |
| ca-AU-coast_guard_navy | coast_guard_navy | — (ABF Marine covers) | — | — | — | — | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-AU-upstream_regulator (NOPSEMA) | offshore produkce, výpadky | — | NWS, Gorgon, Wheatstone platformy | proposed |
| ca-AU-ministry_petroleum | LNG export objemy | konkurence QA/US pro Asii | Dampier, Gladstone LNG | proposed — ADGSM (domestic gas mechanism) signál |

### Unverified / poznámky

- **`ca-AU-noc` = empty:** žádný NOC; Woodside (woodside.com), Santos (santos.com) soukromé.
- **`ca-AU-coast_guard_navy` = empty:** ABF Maritime + Navy; neduplikovat.
- **NOPTA** (titles administrator) jako expanze upstream regulátoru.
- ADGSM (Australian Domestic Gas Security Mechanism) — export restrikce signál (EU/Asia LNG).
- Gladstone (QLD) CSG-LNG (GLNG/APLNG/QCLNG) = domestic gas tightness driver.

### Progress po merge

`last_country: AU`, `last_batch_seq: 27`
