# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_035_country_authority_DE.md  
**Fáze:** country_authority — krok DE (Fáze 2, Germany)  
**Datum:** 2026-07-06  

---

## Shrnutí

Třicátá první dávka Fáze 2: `DE` × 10 typů autorit podle skeleton dimenze.  
Germany je desk-critical pro European gas/oil demand, sanctions policy, refinery/logistics stress, Rhine and North Sea maritime context, strategic reserves and financial/eurozone signals.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-DE-ministry_petroleum | DE | — | ministry_petroleum | Federal Ministry for Economic Affairs and Energy | bundeswirtschaftsministerium.de | government_regulator | official | production, imports, exports, quota_rhetoric | proposed |
| ca-DE-noc | DE | — | noc | — | — | noc | official | production, exports, force_majeure, term_contract, vessel_loading | empty |
| ca-DE-mfa | DE | — | mfa | Federal Foreign Office | auswaertiges-amt.de | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-DE-customs_export | DE | — | customs_export | German Customs | zoll.de | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-DE-upstream_regulator | DE | — | upstream_regulator | Federal Network Agency (Bundesnetzagentur) | bundesnetzagentur.de | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-DE-port_maritime_authority | DE | — | port_maritime_authority | Federal Maritime and Hydrographic Agency (BSH) | bsh.de | infrastructure | official | vessel_loading, port_closure, exports, imports | proposed |
| ca-DE-national_exchange | DE | — | national_exchange | Deutsche Boerse | deutsche-boerse.com | exchange | data_feed | pricing_formula | proposed |
| ca-DE-central_bank | DE | — | central_bank | Deutsche Bundesbank | bundesbank.de | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-DE-environment_regulator | DE | — | environment_regulator | Federal Environment Agency (UBA) | umweltbundesamt.de | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-DE-coast_guard_navy | DE | — | coast_guard_navy | German Navy | marine.de | government_regulator | official | port_closure, vessel_loading, sanctions | unverified |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-DE-ministry_petroleum | Primary federal energy policy source. | Sanctions, energy-security and EU policy relevance. | Logistics indirect. | proposed |
| ca-DE-customs_export | Customs supports trade-control and sanctions enforcement context. | EU/Russia sanctions relevance. | Trade-flow relevance. | proposed |
| ca-DE-port_maritime_authority | BSH is relevant for maritime/ocean and offshore notices. | North Sea infrastructure relevance. | Direct maritime context, less refinery-specific. | proposed |
| ca-DE-noc | Germany has no direct NOC equivalent. | — | — | empty |
| ca-DE-coast_guard_navy | Navy source can matter for Baltic/North Sea security. | Security relevance. | Domain/path should be validated before whitelist. | unverified |

---

### Unverified / Anti-patterns

- `ca-DE-noc` is `empty`: do not force SEFE, Wintershall Dea, or refiners into a national oil company slot.
- `ca-DE-coast_guard_navy` is `unverified`: validate exact Bundeswehr/Navy source path before whitelist.
- German refinery or Rhine disruption claims need operator, port/waterway and official cross-checks before trading use.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 31,
  "last_country": "DE",
  "crosscheck_cursor": 0,
  "last_batch_seq": 35
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_036_country_authority_NL.md`.
