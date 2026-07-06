# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_045_country_authority_SS.md  
**Fáze:** country_authority — krok SS (Fáze 2, South Sudan)  
**Datum:** 2026-07-06  

---

## Shrnutí

Čtyřicátá první dávka Fáze 2: `SS` × 10 typů autorit podle skeleton dimenze.  
South Sudan je desk-critical pro Nile Blend/Dar Blend production, Sudan pipeline/export dependency, Nilepet/SPOC signals, conflict risk, payment arrears and transit disruption through Port Sudan.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-SS-ministry_petroleum | SS | — | ministry_petroleum | Ministry of Petroleum South Sudan | mop.gov.ss | government_regulator | official | production, exports, quota_rhetoric, term_contract | proposed |
| ca-SS-noc | SS | — | noc | Nile Petroleum Corporation (Nilepet) | nilepet.com | noc | official | production, exports, force_majeure, term_contract, vessel_loading | proposed |
| ca-SS-mfa | SS | — | mfa | Ministry of Foreign Affairs and International Cooperation | mofaic.gov.ss | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-SS-customs_export | SS | — | customs_export | South Sudan National Revenue Authority / Customs | nra.gov.ss | government_regulator | official | exports, imports, export_license, sanctions | unverified |
| ca-SS-upstream_regulator | SS | — | upstream_regulator | Ministry of Petroleum / Petroleum Authority | mop.gov.ss | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-SS-port_maritime_authority | SS | — | port_maritime_authority | — | — | infrastructure | official | vessel_loading, port_closure, exports | empty |
| ca-SS-national_exchange | SS | — | national_exchange | — | — | exchange | data_feed | pricing_formula | empty |
| ca-SS-central_bank | SS | — | central_bank | Bank of South Sudan | boss.gov.ss | government_regulator | official | sanctions, pricing_formula, imports, exports | unverified |
| ca-SS-environment_regulator | SS | — | environment_regulator | Ministry of Environment and Forestry South Sudan | moe.gov.ss | government_regulator | official | refinery_outage, force_majeure, port_closure | unverified |
| ca-SS-coast_guard_navy | SS | — | coast_guard_navy | — | — | government_regulator | official | port_closure, vessel_loading, sanctions | empty |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-SS-ministry_petroleum | Primary petroleum policy and production source. | Pipeline/export dependence on Sudan. | Logistics indirect. | proposed |
| ca-SS-noc | Nilepet is the national oil company anchor. | Strategic state entity and joint-venture participant. | Direct production relevance. | proposed |
| ca-SS-upstream_regulator | Petroleum Authority surface is tied to ministry. | Licensing and consortium relevance. | Direct production/project relevance. | proposed |
| ca-SS-port_maritime_authority | Landlocked country; no maritime authority slot. | Export dependency belongs to Sudan/Port Sudan cross-checks. | — | empty |
| ca-SS-coast_guard_navy | Landlocked country; no coast guard/navy maritime slot. | Border/security exists but not this dimension. | — | empty |

---

### Unverified / Anti-patterns

- Validate `nra.gov.ss`, `boss.gov.ss`, and `moe.gov.ss` before whitelist.
- Do not treat South Sudan production claims as complete without Sudan pipeline, Port Sudan and operator cross-checks.
- Keep landlocked maritime slots `empty`; do not invent port or coast-guard equivalents.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 41,
  "last_country": "SS",
  "crosscheck_cursor": 0,
  "last_batch_seq": 45
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_046_country_authority_CO.md`.
