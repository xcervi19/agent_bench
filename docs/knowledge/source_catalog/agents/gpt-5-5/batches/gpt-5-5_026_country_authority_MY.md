# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_026_country_authority_MY.md  
**Fáze:** country_authority — krok MY (Fáze 2, Malaysia)  
**Datum:** 2026-07-06  

---

## Shrnutí

Dvacátá druhá dávka Fáze 2: `MY` × 10 typů autorit podle skeleton dimenze.  
Malaysia je desk-critical pro PETRONAS LNG/crude, Malaysia-Thailand/JDA and South China Sea risk, Strait of Malacca logistics, customs flows and ringgit/payment context.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-MY-ministry_petroleum | MY | — | ministry_petroleum | Ministry of Economy / energy policy surface | ekonomi.gov.my | government_regulator | official | production, exports, quota_rhetoric, term_contract | proposed |
| ca-MY-noc | MY | — | noc | PETRONAS | petronas.com | noc | official | production, exports, force_majeure, term_contract, vessel_loading | proposed |
| ca-MY-mfa | MY | — | mfa | Ministry of Foreign Affairs Malaysia | kln.gov.my | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-MY-customs_export | MY | — | customs_export | Royal Malaysian Customs Department | customs.gov.my | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-MY-upstream_regulator | MY | — | upstream_regulator | Malaysia Petroleum Management (PETRONAS) | petronas.com/mpm | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-MY-port_maritime_authority | MY | — | port_maritime_authority | Marine Department Malaysia | marine.gov.my | infrastructure | official | vessel_loading, port_closure, exports, imports | unverified |
| ca-MY-national_exchange | MY | — | national_exchange | Bursa Malaysia | bursamalaysia.com | exchange | data_feed | pricing_formula | proposed |
| ca-MY-central_bank | MY | — | central_bank | Bank Negara Malaysia | bnm.gov.my | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-MY-environment_regulator | MY | — | environment_regulator | Department of Environment Malaysia | doe.gov.my | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-MY-coast_guard_navy | MY | — | coast_guard_navy | Malaysian Maritime Enforcement Agency | mmea.gov.my | government_regulator | official | port_closure, vessel_loading, sanctions | unverified |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-MY-noc | PETRONAS is core operational NOC source. | Strategic actor in LNG, South China Sea and JDA context. | Direct cargo/LNG/export relevance. | proposed |
| ca-MY-upstream_regulator | MPM is the upstream resource-management arm under PETRONAS. | Licensing and partner context. | Project/production relevance. | proposed |
| ca-MY-customs_export | Customs is relevant for import/export controls. | Sanctions and trade-control context. | Trade-flow relevance. | proposed |
| ca-MY-port_maritime_authority | Marine Department would be useful for maritime notices. | Sovereign infrastructure source. | Domain/path should be validated before whitelist. | unverified |
| ca-MY-coast_guard_navy | MMEA matters for Malacca/South China Sea security. | Security and enforcement relevance. | Exact official domain should be validated before whitelist. | unverified |

---

### Unverified / Anti-patterns

- `ca-MY-port_maritime_authority` and `ca-MY-coast_guard_navy` are `unverified`: confirm official domains/publication paths before whitelist.
- `PETRONAS`/`MPM` can cover both commercial and statutory upstream roles; keep notes explicit when interpreting regulatory versus corporate signals.
- Do not treat Bursa or ringgit moves as physical oil/LNG flow evidence without PETRONAS, customs, port or shipping confirmation.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 22,
  "last_country": "MY",
  "crosscheck_cursor": 0,
  "last_batch_seq": 26
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_027_country_authority_ID.md` (Fáze 2, Indonesia autority).
