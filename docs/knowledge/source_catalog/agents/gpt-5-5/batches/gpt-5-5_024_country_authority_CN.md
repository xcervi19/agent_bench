# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_024_country_authority_CN.md  
**Fáze:** country_authority — krok CN (Fáze 2, China)  
**Datum:** 2026-07-06  

---

## Shrnutí

Dvacátá dávka Fáze 2: `CN` × 10 typů autorit podle skeleton dimenze.  
China je desk-critical pro crude/import demand, SPR/refinery runs, sanctions enforcement, customs flows, shipping safety, price signals and geopolitical escalation around Taiwan/South China Sea.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-CN-ministry_petroleum | CN | — | ministry_petroleum | National Energy Administration | nea.gov.cn | government_regulator | official | production, imports, quota_rhetoric, refinery_outage | proposed |
| ca-CN-noc | CN | — | noc | China National Petroleum Corporation (CNPC) | cnpc.com.cn | noc | official | production, imports, force_majeure, term_contract, vessel_loading | proposed |
| ca-CN-mfa | CN | — | mfa | Ministry of Foreign Affairs of the PRC | mfa.gov.cn | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-CN-customs_export | CN | — | customs_export | General Administration of Customs of China | customs.gov.cn | government_regulator | official | exports, imports, sanctions, stock_change | proposed |
| ca-CN-upstream_regulator | CN | — | upstream_regulator | National Energy Administration | nea.gov.cn | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-CN-port_maritime_authority | CN | — | port_maritime_authority | Maritime Safety Administration of China | msa.gov.cn | infrastructure | official | vessel_loading, port_closure, exports, imports | proposed |
| ca-CN-national_exchange | CN | — | national_exchange | Shanghai Stock Exchange | sse.com.cn | exchange | data_feed | pricing_formula | proposed |
| ca-CN-central_bank | CN | — | central_bank | People's Bank of China | pbc.gov.cn | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-CN-environment_regulator | CN | — | environment_regulator | Ministry of Ecology and Environment | mee.gov.cn | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-CN-coast_guard_navy | CN | — | coast_guard_navy | China Coast Guard | ccg.gov.cn | government_regulator | official | port_closure, vessel_loading, sanctions | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-CN-ministry_petroleum | NEA is primary energy policy/regulatory source. | Demand, stock and policy signals have global market impact. | Logistics indirect. | proposed |
| ca-CN-customs_export | Customs is critical for import/export flow data. | Sanctions and trade-control context. | Direct cargo-flow relevance via customs data. | proposed |
| ca-CN-port_maritime_authority | MSA is relevant for navigation and port safety. | Sovereign maritime source. | Direct logistics/closure signal. | proposed |
| ca-CN-coast_guard_navy | CCG matters for South China Sea/Taiwan maritime risk. | High geopolitical escalation relevance. | Security signal rather than ordinary port operations. | proposed |
| ca-CN-national_exchange | Exchange is useful for listed-market context. | Limited geopolitical value. | Not physical flow confirmation. | proposed |

---

### Unverified / Anti-patterns

- China has multiple NOCs; `CNPC` is the default national anchor, while Sinopec/CNOOC may need separate slots in global/crosscheck or role-specific expansions.
- Do not treat exchange price moves as evidence of crude flow disruption without customs, port, refinery or official policy confirmation.
- Official Chinese sources can be delayed or political; cross-check market-moving claims with shipping, customs releases, and counterpart-country data.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 20,
  "last_country": "CN",
  "crosscheck_cursor": 0,
  "last_batch_seq": 24
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_025_country_authority_IN.md`.
