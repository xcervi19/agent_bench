# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_005_country_authority_SA.md  
**Fáze:** country_authority — krok SA (Fáze 2, Saudi Arabia)  
**Datum:** 2026-07-05  

---

## Shrnutí

První dávka Fáze 2: `SA` × 10 typů autorit podle skeleton dimenze.
Saudi Arabia je desk-critical producent; priorita je přímý řetězec ministerstvo → NOC → export/customs/ports → policy/sanctions/FX/logistics.

Do `source_whitelist.json` zatím nezapisovat; tato dávka čeká na review a případný merge do `catalog.json`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-SA-ministry_petroleum | SA | — | ministry_petroleum | Saudi Ministry of Energy | moenergy.gov.sa | government_regulator | official | production, exports, quota_rhetoric, term_contract | proposed |
| ca-SA-noc | SA | — | noc | Saudi Aramco | aramco.com | noc | official | production, exports, force_majeure, term_contract, vessel_loading | proposed |
| ca-SA-mfa | SA | — | mfa | Ministry of Foreign Affairs of Saudi Arabia | mofa.gov.sa | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-SA-customs_export | SA | — | customs_export | Zakat, Tax and Customs Authority (ZATCA) | zatca.gov.sa | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-SA-upstream_regulator | SA | — | upstream_regulator | Saudi Ministry of Energy | moenergy.gov.sa | government_regulator | official | production, force_majeure, quota_rhetoric | proposed |
| ca-SA-port_maritime_authority | SA | ras_tanura | port_maritime_authority | Saudi Ports Authority (Mawani) | mawani.gov.sa | infrastructure | official | vessel_loading, port_closure, exports | proposed |
| ca-SA-national_exchange | SA | — | national_exchange | Saudi Exchange | saudiexchange.sa | exchange | data_feed | pricing_formula | proposed |
| ca-SA-central_bank | SA | — | central_bank | Saudi Central Bank (SAMA) | sama.gov.sa | government_regulator | official | sanctions, pricing_formula, imports | proposed |
| ca-SA-environment_regulator | SA | — | environment_regulator | National Center for Environmental Compliance (NCEC) | ncec.gov.sa | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-SA-coast_guard_navy | SA | — | coast_guard_navy | General Directorate of Border Guard | moi.gov.sa | government_regulator | official | port_closure, vessel_loading, sanctions | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-SA-ministry_petroleum | Primary policy source for production capacity, OPEC+ stance, energy strategy. | Direct sovereign signal for quota rhetoric and bilateral energy policy. | Logistics indirect; useful for upstream/export policy framing. | proposed |
| ca-SA-noc | Direct operator source for production, downstream, loading, project and force majeure context. | State-owned NOC statements often carry policy signal. | Direct crude/product/LNG-related operational relevance via terminals and shipping updates. | proposed |
| ca-SA-mfa | Not a supply source. | Primary diplomatic source for sanctions, conflict and bilateral statements affecting flows. | Logistics indirect except crisis/diplomatic channel closures. | proposed |
| ca-SA-customs_export | Customs and trade procedures can affect export/import clearance. | Sanctions/export controls and customs enforcement path. | Direct clearance and port/customs operations relevance. | proposed |
| ca-SA-upstream_regulator | Ministry oversees sector policy and regulation. | Same sovereign source as ministry; no separate upstream regulator found for oil. | Logistics indirect. | proposed |
| ca-SA-port_maritime_authority | Port throughput and closure information relevant to exports. | Sovereign infrastructure authority. | Direct port/logistics signal for Saudi export corridors. | proposed |
| ca-SA-national_exchange | Equity/debt market data, not physical energy. | Useful for listed Saudi energy names and market stress. | Logistics indirect. | proposed |
| ca-SA-central_bank | FX, liquidity and macro stability data. | Sanctions/payment-channel relevance. | Logistics indirect but relevant to trade settlement conditions. | proposed |
| ca-SA-environment_regulator | Environmental permits/compliance can constrain industrial/refinery activity. | Government enforcement signal. | Relevant to outages, closures and compliance-driven constraints. | proposed |
| ca-SA-coast_guard_navy | Maritime border/coast guard source for security incidents. | Security/sanctions enforcement through Ministry of Interior portal. | Direct coastal patrol, port approach and maritime incident relevance. | proposed |

---

### Unverified / Anti-patterns

- `ca-SA-upstream_regulator` intentionally reuses `moenergy.gov.sa`: Saudi oil upstream regulation appears ministerial; do not invent a separate upstream regulator domain.
- `ca-SA-coast_guard_navy` uses the Ministry of Interior root `moi.gov.sa` because the Border Guard section is hosted under the MOI portal; whitelist notes should preserve the Border Guard path if path-level sources are supported.
- `ca-SA-national_exchange` is useful for listed-market and pricing context, but not a physical crude-flow source.
- Do not treat Aramco commercial pages as official sovereign policy unless cross-checked with Ministry of Energy or SPA/MFA channels.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 1,
  "last_country": "SA",
  "crosscheck_cursor": 0,
  "last_batch_seq": 5
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_006_country_authority_IR.md` (Fáze 2, Iran autority).
