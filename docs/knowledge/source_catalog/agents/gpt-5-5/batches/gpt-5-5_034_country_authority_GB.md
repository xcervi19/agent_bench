# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_034_country_authority_GB.md  
**Fáze:** country_authority — krok GB (Fáze 2, United Kingdom)  
**Datum:** 2026-07-06  

---

## Shrnutí

Třicátá dávka Fáze 2: `GB` × 10 typů autorit podle skeleton dimenze.  
United Kingdom je desk-critical pro North Sea production, NSTA licensing, Forties/Brent-linked signals, sanctions policy, maritime security, UK/Europe gas balances and financial-market context.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-GB-ministry_petroleum | GB | — | ministry_petroleum | Department for Energy Security and Net Zero (DESNZ) | gov.uk/desnz | government_regulator | official | production, exports, imports, quota_rhetoric | proposed |
| ca-GB-noc | GB | — | noc | — | — | noc | official | production, exports, force_majeure, term_contract, vessel_loading | empty |
| ca-GB-mfa | GB | — | mfa | Foreign, Commonwealth and Development Office | gov.uk/fcdo | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-GB-customs_export | GB | — | customs_export | HM Revenue & Customs | gov.uk/hmrc | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-GB-upstream_regulator | GB | — | upstream_regulator | North Sea Transition Authority | nstauthority.co.uk | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-GB-port_maritime_authority | GB | — | port_maritime_authority | Maritime and Coastguard Agency | gov.uk/mca | infrastructure | official | vessel_loading, port_closure, exports, imports | proposed |
| ca-GB-national_exchange | GB | — | national_exchange | London Stock Exchange | londonstockexchange.com | exchange | data_feed | pricing_formula | proposed |
| ca-GB-central_bank | GB | — | central_bank | Bank of England | bankofengland.co.uk | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-GB-environment_regulator | GB | — | environment_regulator | Environment Agency | gov.uk/environment-agency | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-GB-coast_guard_navy | GB | — | coast_guard_navy | Royal Navy | royalnavy.mod.uk | government_regulator | official | port_closure, vessel_loading, sanctions | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-GB-ministry_petroleum | Primary energy policy source. | Sanctions and energy-security policy relevance. | Logistics indirect. | proposed |
| ca-GB-upstream_regulator | NSTA is the North Sea licensing and production regulator. | UKCS policy and decommissioning context. | Direct production/project relevance. | proposed |
| ca-GB-port_maritime_authority | MCA covers maritime safety and notices. | Sovereign maritime source. | Direct maritime/logistics relevance. | proposed |
| ca-GB-coast_guard_navy | Royal Navy matters for maritime security. | Sanctions/security relevance. | Security signal, not physical flow confirmation. | proposed |
| ca-GB-noc | UK has no direct NOC slot equivalent. | — | — | empty |

---

### Unverified / Anti-patterns

- `ca-GB-noc` is `empty`: do not force BP/Shell/Harbour into a national oil company slot.
- For North Sea outages, cross-check NSTA/DESNZ with operators, terminals and shipping evidence.
- London Stock Exchange is market context only, not physical oil/gas flow evidence.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 30,
  "last_country": "GB",
  "crosscheck_cursor": 0,
  "last_batch_seq": 34
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_035_country_authority_DE.md`.
