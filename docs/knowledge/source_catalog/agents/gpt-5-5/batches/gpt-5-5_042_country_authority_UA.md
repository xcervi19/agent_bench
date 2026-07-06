# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_042_country_authority_UA.md  
**Fáze:** country_authority — krok UA (Fáze 2, Ukraine)  
**Datum:** 2026-07-06  

---

## Shrnutí

Třicátá osmá dávka Fáze 2: `UA` × 10 typů autorit podle skeleton dimenze.  
Ukraine je desk-critical pro war-risk energy infrastructure, gas storage, Naftogaz production, Black Sea port risk, sanctions enforcement, refinery/fuel import disruption and Russia-related escalation signals.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-UA-ministry_petroleum | UA | — | ministry_petroleum | Ministry of Energy of Ukraine | mev.gov.ua | government_regulator | official | production, imports, exports, quota_rhetoric | proposed |
| ca-UA-noc | UA | — | noc | Naftogaz | naftogaz.com | noc | official | production, imports, force_majeure, term_contract, vessel_loading | proposed |
| ca-UA-mfa | UA | — | mfa | Ministry of Foreign Affairs Ukraine | mfa.gov.ua | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-UA-customs_export | UA | — | customs_export | State Customs Service of Ukraine | customs.gov.ua | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-UA-upstream_regulator | UA | — | upstream_regulator | National Energy and Utilities Regulatory Commission (NEURC) | nerc.gov.ua | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-UA-port_maritime_authority | UA | — | port_maritime_authority | Ukrainian Sea Ports Authority | uspa.gov.ua | infrastructure | official | vessel_loading, port_closure, exports, imports | unverified |
| ca-UA-national_exchange | UA | — | national_exchange | Ukrainian Exchange / capital-market surface | ux.ua | exchange | data_feed | pricing_formula | unverified |
| ca-UA-central_bank | UA | — | central_bank | National Bank of Ukraine | bank.gov.ua | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-UA-environment_regulator | UA | — | environment_regulator | Ministry of Environmental Protection and Natural Resources | mepr.gov.ua | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-UA-coast_guard_navy | UA | — | coast_guard_navy | Ukrainian Navy / Ministry of Defence | mil.gov.ua | government_regulator | official | port_closure, vessel_loading, sanctions | unverified |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-UA-ministry_petroleum | Primary wartime energy policy and infrastructure source. | Russia escalation and donor-support context. | Logistics indirect. | proposed |
| ca-UA-noc | Naftogaz is central for gas production/storage and state hydrocarbon signals. | Strategic wartime energy actor. | Direct gas/storage relevance. | proposed |
| ca-UA-customs_export | Customs supports import/export and sanctions enforcement. | War/sanctions context. | Trade-flow relevance. | proposed |
| ca-UA-port_maritime_authority | Sea ports authority matters for Black Sea logistics. | War-risk and corridor relevance. | Exact publication surface should be validated. | unverified |
| ca-UA-coast_guard_navy | Navy/defense source matters for Black Sea security. | Direct war/security relevance. | Exact source path should be validated. | unverified |

---

### Unverified / Anti-patterns

- `ca-UA-port_maritime_authority`, `ca-UA-national_exchange`, and `ca-UA-coast_guard_navy` need manual domain/path validation before whitelist.
- Wartime infrastructure claims require high-confidence cross-checking with ministry, Naftogaz, operator, military and shipping/security sources.
- Do not treat capital-market signals as evidence of physical fuel or gas disruption without official and logistics confirmation.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 38,
  "last_country": "UA",
  "crosscheck_cursor": 0,
  "last_batch_seq": 42
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_043_country_authority_YE.md` (Fáze 2, Yemen autority).
