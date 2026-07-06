# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_036_country_authority_NL.md  
**Fáze:** country_authority — krok NL (Fáze 2, Netherlands)  
**Datum:** 2026-07-06  

---

## Shrnutí

Třicátá druhá dávka Fáze 2: `NL` × 10 typů autorit podle skeleton dimenze.  
Netherlands je desk-critical pro Rotterdam oil/product logistics, Dutch gas storage and residual production, North Sea regulation, EU sanctions enforcement, TTF/gas-market context and Amsterdam/Rotterdam port disruptions.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-NL-ministry_petroleum | NL | — | ministry_petroleum | Ministry of Economic Affairs / Climate and Green Growth | government.nl | government_regulator | official | production, imports, exports, quota_rhetoric | proposed |
| ca-NL-noc | NL | — | noc | Energie Beheer Nederland (EBN) | ebn.nl | noc | official | production, exports, force_majeure, term_contract, vessel_loading | proposed |
| ca-NL-mfa | NL | — | mfa | Ministry of Foreign Affairs Netherlands | rijksoverheid.nl | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-NL-customs_export | NL | — | customs_export | Dutch Customs | douane.nl | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-NL-upstream_regulator | NL | — | upstream_regulator | State Supervision of Mines (SodM) | sodm.nl | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-NL-port_maritime_authority | NL | — | port_maritime_authority | Port of Rotterdam Authority | portofrotterdam.com | infrastructure | official | vessel_loading, port_closure, exports, imports | proposed |
| ca-NL-national_exchange | NL | — | national_exchange | Euronext Amsterdam | euronext.com | exchange | data_feed | pricing_formula | proposed |
| ca-NL-central_bank | NL | — | central_bank | De Nederlandsche Bank | dnb.nl | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-NL-environment_regulator | NL | — | environment_regulator | Rijkswaterstaat | rijkswaterstaat.nl | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-NL-coast_guard_navy | NL | — | coast_guard_navy | Netherlands Coastguard | kustwacht.nl | government_regulator | official | port_closure, vessel_loading, sanctions | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-NL-ministry_petroleum | Primary policy source for energy and climate/economic policy. | EU sanctions and gas-market context. | Logistics indirect. | proposed |
| ca-NL-noc | EBN is the state energy company, but not a classic integrated NOC. | Domestic gas/storage and state participation relevance. | Useful for upstream/storage context, not cargoes alone. | proposed |
| ca-NL-upstream_regulator | SodM is the mining/upstream supervision source. | Groningen/North Sea regulatory context. | Direct safety/production relevance. | proposed |
| ca-NL-port_maritime_authority | Rotterdam is critical for oil/product logistics. | EU trade and sanctions-route relevance. | Direct logistics relevance. | proposed |
| ca-NL-coast_guard_navy | Coastguard source matters for North Sea incidents. | Security/enforcement relevance. | Maritime signal, not physical flow proof alone. | proposed |

---

### Unverified / Anti-patterns

- `EBN` should be interpreted as state energy company/upstream participation, not as a fully integrated NOC equivalent.
- Port of Rotterdam is a critical logistics source, but refinery/product flow claims still need operator, customs and shipping cross-checks.
- Euronext/TTF-adjacent market moves are not physical disruption evidence without source triangulation.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 32,
  "last_country": "NL",
  "crosscheck_cursor": 0,
  "last_batch_seq": 36
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_037_country_authority_BE.md` (Fáze 2, Belgium autority).
