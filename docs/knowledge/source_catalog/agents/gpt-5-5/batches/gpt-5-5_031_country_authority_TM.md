# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_031_country_authority_TM.md  
**Fáze:** country_authority — krok TM (Fáze 2, Turkmenistan)  
**Datum:** 2026-07-06  

---

## Shrnutí

Dvacátá sedmá dávka Fáze 2: `TM` × 10 typů autorit podle skeleton dimenze.  
Turkmenistan je desk-critical pro Central Asia gas flows, China pipeline supply, Caspian port logistics, opaque state-company tenders, swap flows and sanctions/geopolitical exposure around Iran/Russia/Afghanistan.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-TM-ministry_petroleum | TM | — | ministry_petroleum | Oil and Gas Industry Portal of Turkmenistan | oilgas.gov.tm | government_regulator | official | production, exports, quota_rhetoric, term_contract | proposed |
| ca-TM-noc | TM | — | noc | Turkmengaz / Turkmennebit State Concerns | turkmengaz.gov.tm | noc | official | production, exports, force_majeure, term_contract, vessel_loading | proposed |
| ca-TM-mfa | TM | — | mfa | Ministry of Foreign Affairs Turkmenistan | mfa.gov.tm | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-TM-customs_export | TM | — | customs_export | State Customs Service of Turkmenistan | customs.gov.tm | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-TM-upstream_regulator | TM | — | upstream_regulator | Oil and Gas Industry Portal / state concerns | oilgas.gov.tm | government_regulator | official | production, force_majeure, export_license | unverified |
| ca-TM-port_maritime_authority | TM | — | port_maritime_authority | Turkmenbashi International Seaport | port.com.tm | infrastructure | official | vessel_loading, port_closure, exports | unverified |
| ca-TM-national_exchange | TM | — | national_exchange | State Commodity and Raw Materials Exchange of Turkmenistan | exchange.gov.tm | exchange | data_feed | pricing_formula | unverified |
| ca-TM-central_bank | TM | — | central_bank | Central Bank of Turkmenistan | cbt.tm | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-TM-environment_regulator | TM | — | environment_regulator | Ministry of Agriculture and Environmental Protection | minagri.gov.tm | government_regulator | official | refinery_outage, force_majeure, port_closure | unverified |
| ca-TM-coast_guard_navy | TM | — | coast_guard_navy | Turkmenistan Navy / Defense Ministry | — | government_regulator | official | port_closure, vessel_loading, sanctions | empty |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-TM-noc | Turkmengaz/Turkmennebit are the core state-company sources. | China gas and regional pipeline relevance. | Direct supply/tender relevance, less transparent for cargoes. | proposed |
| ca-TM-customs_export | Customs can support trade-control and border context. | Iran/Russia/Afghanistan exposure. | Trade-flow relevance. | proposed |
| ca-TM-port_maritime_authority | Turkmenbashi port is relevant for Caspian logistics. | Middle Corridor/swap relevance. | Exact official domain needs validation. | unverified |
| ca-TM-upstream_regulator | Public regulator surface is not cleanly separable from state oil/gas portals. | State opacity affects interpretation. | Validate before whitelist. | unverified |
| ca-TM-coast_guard_navy | Public official source is not sufficiently clear. | Security relevance exists. | Leave empty rather than inventing a domain. | empty |

---

### Unverified / Anti-patterns

- Turkmenistan has a constrained public information environment; `unverified` entries need manual domain validation before whitelist.
- `ca-TM-coast_guard_navy` is `empty`: do not invent a public Navy/Coast Guard domain.
- Treat tenders and state concern releases as partial signals; cross-check market-moving gas/export claims with buyer-country data, pipeline operators and customs/logistics evidence.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 27,
  "last_country": "TM",
  "crosscheck_cursor": 0,
  "last_batch_seq": 31
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_032_country_authority_UZ.md` (Fáze 2, Uzbekistan autority).
