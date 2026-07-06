# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_009_country_authority_US.md  
**Fáze:** country_authority — krok US (Fáze 2, United States)  
**Datum:** 2026-07-05  

---

## Shrnutí

Pátá dávka Fáze 2: `US` × 10 typů autorit podle skeleton dimenze.
United States je desk-critical pro crude/products inventories, Gulf outages, sanctions enforcement, SPR policy, LNG exports, shipping waivers a benchmark pricing.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-US-ministry_petroleum | US | — | ministry_petroleum | U.S. Department of Energy | energy.gov | government_regulator | official | production, exports, imports, storage_levels, sanctions | proposed |
| ca-US-noc | US | — | noc | — | — | noc | official | — | empty |
| ca-US-mfa | US | — | mfa | U.S. Department of State | state.gov | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-US-customs_export | US | — | customs_export | U.S. Customs and Border Protection (CBP) | cbp.gov | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-US-upstream_regulator | US | — | upstream_regulator | Bureau of Safety and Environmental Enforcement (BSEE) | bsee.gov | government_regulator | official | production, force_majeure, refinery_outage | proposed |
| ca-US-port_maritime_authority | US | houston_ship_channel | port_maritime_authority | U.S. Maritime Administration (MARAD) | maritime.dot.gov | infrastructure | official | vessel_loading, port_closure, exports | proposed |
| ca-US-national_exchange | US | cushing | national_exchange | CME Group | cmegroup.com | exchange | data_feed | pricing_formula, storage_levels | proposed |
| ca-US-central_bank | US | — | central_bank | Federal Reserve | federalreserve.gov | government_regulator | official | sanctions, pricing_formula, imports | proposed |
| ca-US-environment_regulator | US | — | environment_regulator | U.S. Environmental Protection Agency (EPA) | epa.gov | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-US-coast_guard_navy | US | — | coast_guard_navy | U.S. Coast Guard | uscg.mil | government_regulator | official | port_closure, vessel_loading, sanctions | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-US-ministry_petroleum | DOE/EIA/SPR policy and energy emergency authority. | Sanctions and strategic reserve policy relevance. | Indirect, but critical for stocks and emergency response. | proposed |
| ca-US-noc | No federal national oil company equivalent. | N/A. | N/A. | empty |
| ca-US-customs_export | Customs, Jones Act waivers and import/export enforcement. | Sanctions/export enforcement. | Direct port and cargo clearance signal. | proposed |
| ca-US-upstream_regulator | Offshore safety and OCS production oversight. | Federal regulatory signal. | Strong Gulf of Mexico disruption relevance. | proposed |
| ca-US-port_maritime_authority | Maritime policy and advisories. | Federal transport policy. | Direct shipping/logistics signal, often cross-check with USCG/ports. | proposed |
| ca-US-coast_guard_navy | Maritime safety, port conditions, security zones. | Sanctions/enforcement and security relevance. | Direct port closure and vessel movement relevance. | proposed |

---

### Unverified / Anti-patterns

- `ca-US-noc` is intentionally `empty`; do not substitute Exxon/Chevron or another private producer.
- `CME Group` is an exchange/data source, not a government authority.
- For Gulf operational alerts, cross-check MARAD/USCG with local port authorities and NOAA/NHC.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 5,
  "last_country": "US",
  "crosscheck_cursor": 0,
  "last_batch_seq": 9
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_010_country_authority_AE.md`.
