# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_016_country_authority_CA.md  
**Fáze:** country_authority — krok CA (Fáze 2, Canada)  
**Datum:** 2026-07-05  

---

## Shrnutí

Dvanáctá dávka Fáze 2: `CA` × 10 typů autorit podle skeleton dimenze.
Canada je desk-critical pro oil sands output, TMX exports, rail/pipeline constraints, wildfire/weather disruptions, sanctions/trade settlement a US-linked crude flows.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-CA-ministry_petroleum | CA | — | ministry_petroleum | Natural Resources Canada | natural-resources.canada.ca | government_regulator | official | production, exports, imports, storage_levels | proposed |
| ca-CA-noc | CA | — | noc | — | — | noc | official | — | empty |
| ca-CA-mfa | CA | — | mfa | Global Affairs Canada | international.gc.ca | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-CA-customs_export | CA | — | customs_export | Canada Border Services Agency (CBSA) | cbsa-asfc.gc.ca | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-CA-upstream_regulator | CA | — | upstream_regulator | Canada Energy Regulator (CER) | cer-rec.gc.ca | government_regulator | official | production, pipeline_outage, exports | proposed |
| ca-CA-port_maritime_authority | CA | — | port_maritime_authority | Transport Canada | tc.canada.ca | infrastructure | official | vessel_loading, port_closure, exports | proposed |
| ca-CA-national_exchange | CA | — | national_exchange | TMX Group | tmx.com | exchange | data_feed | pricing_formula | proposed |
| ca-CA-central_bank | CA | — | central_bank | Bank of Canada | bankofcanada.ca | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-CA-environment_regulator | CA | — | environment_regulator | Environment and Climate Change Canada | canada.ca | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-CA-coast_guard_navy | CA | — | coast_guard_navy | Canadian Coast Guard | dfo-mpo.gc.ca | government_regulator | official | port_closure, vessel_loading, sanctions | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-CA-ministry_petroleum | Natural resources and energy policy source. | Trade and energy security relevance. | Logistics indirect. | proposed |
| ca-CA-noc | No federal national oil company equivalent. | N/A. | N/A. | empty |
| ca-CA-upstream_regulator | CER covers pipelines and energy regulation. | Federal regulatory signal for export infrastructure. | Direct pipeline/export constraint relevance. | proposed |
| ca-CA-port_maritime_authority | Federal transport/marine safety source. | Infrastructure and transport policy relevance. | Direct port/marine operations context. | proposed |
| ca-CA-coast_guard_navy | Coast Guard under Fisheries and Oceans Canada. | Maritime security/search-and-rescue relevance. | Direct port/ice/weather response signal. | proposed |

---

### Unverified / Anti-patterns

- `ca-CA-noc` is intentionally `empty`; do not substitute Suncor/Cenovus/Canadian Natural or other private producers.
- `Environment and Climate Change Canada` is represented by `canada.ca`; preserve the agency path in whitelist notes if path-level sources are supported.
- `TMX Group` is market infrastructure/listed-market context, not physical crude-flow confirmation; pipeline TMX should be handled separately under infrastructure/playbook coverage.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 12,
  "last_country": "CA",
  "crosscheck_cursor": 0,
  "last_batch_seq": 16
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_017_country_authority_MX.md` (Fáze 2, Mexico autority).
