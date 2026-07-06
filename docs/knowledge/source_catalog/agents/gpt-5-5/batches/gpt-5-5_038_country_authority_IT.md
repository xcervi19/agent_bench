# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_038_country_authority_IT.md  
**Fáze:** country_authority — krok IT (Fáze 2, Italy)  
**Datum:** 2026-07-06  

---

## Shrnutí

Třicátá čtvrtá dávka Fáze 2: `IT` × 10 typů autorit podle skeleton dimenze.  
Italy je desk-critical pro Mediterranean refinery/product flows, ENI upstream and gas exposure, Libya/North Africa supply risk, Trieste/Genoa logistics, sanctions enforcement and central Mediterranean maritime security.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-IT-ministry_petroleum | IT | — | ministry_petroleum | Ministry of Environment and Energy Security | mase.gov.it | government_regulator | official | production, imports, exports, quota_rhetoric | proposed |
| ca-IT-noc | IT | — | noc | Eni | eni.com | noc | official | production, imports, exports, force_majeure, term_contract, vessel_loading | proposed |
| ca-IT-mfa | IT | — | mfa | Ministry of Foreign Affairs and International Cooperation | esteri.it | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-IT-customs_export | IT | — | customs_export | Italian Customs and Monopolies Agency | adm.gov.it | government_regulator | official | exports, imports, export_license, sanctions | unverified |
| ca-IT-upstream_regulator | IT | — | upstream_regulator | ARERA | arera.it | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-IT-port_maritime_authority | IT | — | port_maritime_authority | Ministry of Infrastructure and Transport / maritime authorities | mit.gov.it | infrastructure | official | vessel_loading, port_closure, exports, imports | proposed |
| ca-IT-national_exchange | IT | — | national_exchange | Borsa Italiana | borsaitaliana.it | exchange | data_feed | pricing_formula | proposed |
| ca-IT-central_bank | IT | — | central_bank | Banca d'Italia | bancaditalia.it | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-IT-environment_regulator | IT | — | environment_regulator | Ministry of Environment and Energy Security | mase.gov.it | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-IT-coast_guard_navy | IT | — | coast_guard_navy | Italian Coast Guard | guardiacostiera.gov.it | government_regulator | official | port_closure, vessel_loading, sanctions | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-IT-ministry_petroleum | Primary hydrocarbons and energy-security policy source. | North Africa and EU sanctions relevance. | Logistics indirect. | proposed |
| ca-IT-noc | Eni is state-influenced and operationally central, but not a classic ministry source. | Libya/East Med/North Africa exposure. | Direct upstream, cargo and contract relevance. | proposed |
| ca-IT-port_maritime_authority | Maritime/transport ministry is relevant for ports and shipping. | Central Med logistics relevance. | Direct notices/logistics value. | proposed |
| ca-IT-coast_guard_navy | Coast Guard is important for central Mediterranean security. | Sanctions/migration/security context. | Maritime signal, not flow proof alone. | proposed |
| ca-IT-customs_export | Customs source is relevant. | EU sanctions enforcement context. | Exact public surface should be validated. | unverified |

---

### Unverified / Anti-patterns

- `ca-IT-customs_export` is `unverified`: validate the exact customs publication surface before whitelist.
- `Eni` should be interpreted as a state-influenced listed energy company, not a pure sovereign regulator.
- Italian refinery or Libya-linked supply claims need operator, customs, port and shipping cross-checks before trading use.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 34,
  "last_country": "IT",
  "crosscheck_cursor": 0,
  "last_batch_seq": 38
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_039_country_authority_FR.md`.
