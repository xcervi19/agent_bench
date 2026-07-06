# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_028_country_authority_AU.md  
**Fáze:** country_authority — krok AU (Fáze 2, Australia)  
**Datum:** 2026-07-06  

---

## Shrnutí

Dvacátá čtvrtá dávka Fáze 2: `AU` × 10 typů autorit podle skeleton dimenze.  
Australia je desk-critical pro LNG exports, offshore approvals, condensate flows, Northwest Shelf/Darwin outages, environmental approvals and Indo-Pacific maritime security.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-AU-ministry_petroleum | AU | — | ministry_petroleum | Department of Climate Change, Energy, the Environment and Water / energy.gov.au | energy.gov.au | government_regulator | official | production, exports, quota_rhetoric, term_contract | proposed |
| ca-AU-noc | AU | — | noc | — | — | noc | official | production, exports, force_majeure, term_contract, vessel_loading | empty |
| ca-AU-mfa | AU | — | mfa | Department of Foreign Affairs and Trade | dfat.gov.au | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-AU-customs_export | AU | — | customs_export | Australian Border Force | abf.gov.au | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-AU-upstream_regulator | AU | — | upstream_regulator | National Offshore Petroleum Titles Administrator (NOPTA) | nopta.gov.au | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-AU-port_maritime_authority | AU | — | port_maritime_authority | Australian Maritime Safety Authority | amsa.gov.au | infrastructure | official | vessel_loading, port_closure, exports | proposed |
| ca-AU-national_exchange | AU | — | national_exchange | ASX | asx.com.au | exchange | data_feed | pricing_formula | proposed |
| ca-AU-central_bank | AU | — | central_bank | Reserve Bank of Australia | rba.gov.au | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-AU-environment_regulator | AU | — | environment_regulator | NOPSEMA | nopsema.gov.au | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-AU-coast_guard_navy | AU | — | coast_guard_navy | Royal Australian Navy / Department of Defence | defence.gov.au | government_regulator | official | port_closure, vessel_loading, sanctions | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-AU-ministry_petroleum | Official energy statistics and policy source. | Energy-security and LNG export policy context. | Logistics indirect. | proposed |
| ca-AU-upstream_regulator | NOPTA is core offshore petroleum title source. | Licensing and partner context. | Direct project/production relevance. | proposed |
| ca-AU-environment_regulator | NOPSEMA covers offshore safety/environment plans. | Project approval and disruption relevance. | Useful for offshore operational constraints. | proposed |
| ca-AU-port_maritime_authority | AMSA is the maritime safety authority. | Sovereign maritime source. | Direct notices/safety relevance. | proposed |
| ca-AU-noc | Australia has no direct national oil company equivalent. | — | — | empty |

---

### Unverified / Anti-patterns

- `ca-AU-noc` is `empty`: do not force Woodside/Santos into a national oil company slot.
- For LNG outage trading signals, cross-check government/regulator sources with operator notices and port/shipping evidence.
- ASX is market context only, not physical cargo confirmation.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 24,
  "last_country": "AU",
  "crosscheck_cursor": 0,
  "last_batch_seq": 28
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_029_country_authority_KZ.md`.
