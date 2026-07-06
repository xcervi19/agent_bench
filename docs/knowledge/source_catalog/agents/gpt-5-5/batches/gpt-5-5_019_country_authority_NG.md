# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_019_country_authority_NG.md  
**Fáze:** country_authority — krok NG (Fáze 2, Nigeria)  
**Datum:** 2026-07-05  

---

## Shrnutí

Patnáctá dávka Fáze 2: `NG` × 10 typů autorit podle skeleton dimenze.
Nigeria je desk-critical pro Bonny/Forcados/Qua Iboe flows, force majeure, theft/security, NNPC cargoes, FX/payment constraints a upstream regulatory signals.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-NG-ministry_petroleum | NG | — | ministry_petroleum | Federal Ministry of Petroleum Resources | petroleumresources.gov.ng | government_regulator | official | production, exports, quota_rhetoric, term_contract | proposed |
| ca-NG-noc | NG | — | noc | NNPC Limited | nnpcgroup.com | noc | official | production, exports, force_majeure, term_contract, vessel_loading | unverified |
| ca-NG-mfa | NG | — | mfa | Ministry of Foreign Affairs Nigeria | foreignaffairs.gov.ng | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-NG-customs_export | NG | — | customs_export | Nigeria Customs Service | customs.gov.ng | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-NG-upstream_regulator | NG | — | upstream_regulator | Nigerian Upstream Petroleum Regulatory Commission (NUPRC) | nuprc.gov.ng | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-NG-port_maritime_authority | NG | — | port_maritime_authority | Nigerian Ports Authority | nigerianports.gov.ng | infrastructure | official | vessel_loading, port_closure, exports | unverified |
| ca-NG-national_exchange | NG | — | national_exchange | Nigerian Exchange Group | ngxgroup.com | exchange | data_feed | pricing_formula | proposed |
| ca-NG-central_bank | NG | — | central_bank | Central Bank of Nigeria | cbn.gov.ng | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-NG-environment_regulator | NG | — | environment_regulator | NESREA | nesrea.gov.ng | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-NG-coast_guard_navy | NG | — | coast_guard_navy | Nigerian Navy | navy.mil.ng | government_regulator | official | port_closure, vessel_loading, sanctions | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-NG-ministry_petroleum | Primary federal oil policy source. | OPEC+ and fiscal policy channel. | Logistics indirect. | proposed |
| ca-NG-noc | NNPC is operationally central, but exact canonical corporate domain should be validated. | State strategic entity. | Direct cargo/export relevance. | unverified |
| ca-NG-upstream_regulator | Direct upstream regulator and production data source. | Sovereign regulatory signal. | Direct force majeure/production relevance. | proposed |
| ca-NG-port_maritime_authority | Port authority source is relevant, but domain/path needs validation. | Infrastructure policy. | Direct port/logistics signal if confirmed. | unverified |
| ca-NG-coast_guard_navy | Navy source matters for Niger Delta/Gulf of Guinea security. | Security and anti-theft relevance. | Direct maritime security signal. | proposed |

---

### Unverified / Anti-patterns

- `ca-NG-noc` is `unverified`: confirm current canonical NNPC corporate domain before whitelist.
- `ca-NG-port_maritime_authority` is `unverified`: confirm stable official Nigerian Ports Authority domain/path.
- Do not treat local media reports of outages as primary; cross-check with NUPRC, NNPC, terminal operator, and shipping evidence.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 15,
  "last_country": "NG",
  "crosscheck_cursor": 0,
  "last_batch_seq": 19
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_020_country_authority_AO.md`.
