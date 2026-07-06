# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_029_country_authority_KZ.md  
**Fáze:** country_authority — krok KZ (Fáze 2, Kazakhstan)  
**Datum:** 2026-07-06  

---

## Shrnutí

Dvacátá pátá dávka Fáze 2: `KZ` × 10 typů autorit podle skeleton dimenze.  
Kazakhstan je desk-critical pro CPC/Tengiz/Kashagan flows, Caspian export logistics, Russian transit/sanctions risk, refinery balances and Aktau/Middle Corridor routing.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-KZ-ministry_petroleum | KZ | — | ministry_petroleum | Ministry of Energy of Kazakhstan | gov.kz/memleket/entities/energo | government_regulator | official | production, exports, quota_rhetoric, term_contract | proposed |
| ca-KZ-noc | KZ | — | noc | KazMunayGas | kmg.kz | noc | official | production, exports, force_majeure, term_contract, vessel_loading | proposed |
| ca-KZ-mfa | KZ | — | mfa | Ministry of Foreign Affairs Kazakhstan | gov.kz/memleket/entities/mfa | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-KZ-customs_export | KZ | — | customs_export | State Revenue Committee / Customs | kgd.gov.kz | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-KZ-upstream_regulator | KZ | — | upstream_regulator | Ministry of Energy of Kazakhstan | gov.kz/memleket/entities/energo | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-KZ-port_maritime_authority | KZ | — | port_maritime_authority | Maritime Administration of Ports / Ministry of Transport | gov.kz/memleket/entities/transport | infrastructure | official | vessel_loading, port_closure, exports | unverified |
| ca-KZ-national_exchange | KZ | — | national_exchange | Kazakhstan Stock Exchange (KASE) | kase.kz | exchange | data_feed | pricing_formula | proposed |
| ca-KZ-central_bank | KZ | — | central_bank | National Bank of Kazakhstan | nationalbank.kz | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-KZ-environment_regulator | KZ | — | environment_regulator | Ministry of Ecology and Natural Resources | gov.kz/memleket/entities/ecogeo | government_regulator | official | refinery_outage, force_majeure, port_closure | unverified |
| ca-KZ-coast_guard_navy | KZ | — | coast_guard_navy | Kazakhstan Border Service / Caspian maritime security | gov.kz | government_regulator | official | port_closure, vessel_loading, sanctions | unverified |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-KZ-ministry_petroleum | Primary oil/gas policy and production source. | Russia transit and OPEC+ context. | Logistics indirect. | proposed |
| ca-KZ-noc | KMG is the national oil/gas operator. | Strategic state entity in CPC/Caspian context. | Direct project/export relevance. | proposed |
| ca-KZ-customs_export | Customs source is relevant for export/import enforcement. | Sanctions and transit context. | Trade-flow relevance. | proposed |
| ca-KZ-port_maritime_authority | Caspian/Aktau port source would be valuable. | Middle Corridor and sanctions-route relevance. | Exact official authority path requires validation. | unverified |
| ca-KZ-coast_guard_navy | Maritime security exists in Caspian context but public official source is not clear. | Border/security relevance. | Exact source should be validated before whitelist. | unverified |

---

### Unverified / Anti-patterns

- `ca-KZ-port_maritime_authority`, `ca-KZ-environment_regulator`, and `ca-KZ-coast_guard_navy` are `unverified`: `gov.kz` paths should be validated manually before whitelist.
- Do not treat KMG as a complete proxy for CPC pipeline status; CPC/operator and port evidence belong in geo/logistics phases.
- For Kazakhstan exports, always cross-check with Russian transit, CPC, Caspian port and sanctions context.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 25,
  "last_country": "KZ",
  "crosscheck_cursor": 0,
  "last_batch_seq": 29
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_030_country_authority_AZ.md`.
