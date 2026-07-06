# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_011_country_authority_KW.md  
**Fáze:** country_authority — krok KW (Fáze 2, Kuwait)  
**Datum:** 2026-07-05  

---

## Shrnutí

Sedmá dávka Fáze 2: `KW` × 10 typů autorit podle skeleton dimenze.
Kuwait je desk-critical pro OPEC+ policy, KPC/KOC upstream, Mina al-Ahmadi exports/refining, Gulf shipping risk a customs/payment enforcement.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-KW-ministry_petroleum | KW | — | ministry_petroleum | Kuwait Ministry of Oil | moo.gov.kw | government_regulator | official | production, exports, quota_rhetoric, term_contract | proposed |
| ca-KW-noc | KW | — | noc | Kuwait Petroleum Corporation (KPC) | kpc.com.kw | noc | official | production, exports, force_majeure, term_contract, vessel_loading | proposed |
| ca-KW-mfa | KW | — | mfa | Kuwait Ministry of Foreign Affairs | mofa.gov.kw | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-KW-customs_export | KW | — | customs_export | Kuwait General Administration of Customs | customs.gov.kw | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-KW-upstream_regulator | KW | — | upstream_regulator | Kuwait Ministry of Oil | moo.gov.kw | government_regulator | official | production, force_majeure, quota_rhetoric | proposed |
| ca-KW-port_maritime_authority | KW | — | port_maritime_authority | Kuwait Ports Authority (KPA) | kpa.gov.kw | infrastructure | official | vessel_loading, port_closure, exports | proposed |
| ca-KW-national_exchange | KW | — | national_exchange | Boursa Kuwait | boursakuwait.com.kw | exchange | data_feed | pricing_formula | proposed |
| ca-KW-central_bank | KW | — | central_bank | Central Bank of Kuwait | cbk.gov.kw | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-KW-environment_regulator | KW | — | environment_regulator | Environment Public Authority (EPA Kuwait) | epa.gov.kw | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-KW-coast_guard_navy | KW | — | coast_guard_navy | Kuwait Coast Guard / Ministry of Interior | moi.gov.kw | government_regulator | official | port_closure, vessel_loading, sanctions | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-KW-ministry_petroleum | Primary oil policy and OPEC+ signal. | Sovereign production/export policy channel. | Logistics indirect. | proposed |
| ca-KW-noc | Direct national oil company source for production/export operations. | State strategic entity. | Direct terminal/refinery/export relevance. | proposed |
| ca-KW-customs_export | Customs source for import/export enforcement. | Sanctions/export control relevance. | Direct clearance signal. | proposed |
| ca-KW-port_maritime_authority | Official port authority for Kuwait port system. | Sovereign infrastructure source. | Direct vessel/loading/closure relevance. | proposed |
| ca-KW-coast_guard_navy | Coast guard under Ministry of Interior. | Security and sanctions enforcement relevance. | Direct Gulf maritime/security signal. | proposed |

---

### Unverified / Anti-patterns

- `ca-KW-upstream_regulator` reuses `moo.gov.kw`; Kuwait upstream governance is closely tied to Ministry/KPC/KOC rather than a separate public upstream regulator.
- `Boursa Kuwait` is useful for listed-market context, not physical oil-flow confirmation.
- For operational oil export incidents, cross-check KPC/KOC/KPA with port and tanker data.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 7,
  "last_country": "KW",
  "crosscheck_cursor": 0,
  "last_batch_seq": 11
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_012_country_authority_QA.md` (Fáze 2, Qatar autority).
