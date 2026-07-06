# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_027_country_authority_ID.md  
**Fáze:** country_authority — krok ID (Fáze 2, Indonesia)  
**Datum:** 2026-07-06  

---

## Shrnutí

Dvacátá třetí dávka Fáze 2: `ID` × 10 typů autorit podle skeleton dimenze.  
Indonesia je desk-critical pro Pertamina imports, domestic upstream policy, LNG and refined-product flows, Strait of Malacca/Sunda/Lombok logistics, customs signals and South China Sea/Natuna risk.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-ID-ministry_petroleum | ID | — | ministry_petroleum | Ministry of Energy and Mineral Resources (ESDM) | esdm.go.id | government_regulator | official | production, imports, exports, quota_rhetoric | proposed |
| ca-ID-noc | ID | — | noc | PT Pertamina (Persero) | pertamina.com | noc | official | production, imports, force_majeure, term_contract, vessel_loading | proposed |
| ca-ID-mfa | ID | — | mfa | Ministry of Foreign Affairs Indonesia | kemlu.go.id | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-ID-customs_export | ID | — | customs_export | Directorate General of Customs and Excise | beacukai.go.id | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-ID-upstream_regulator | ID | — | upstream_regulator | SKK Migas | skkmigas.go.id | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-ID-port_maritime_authority | ID | — | port_maritime_authority | Directorate General of Sea Transportation | hubla.dephub.go.id | infrastructure | official | vessel_loading, port_closure, exports, imports | proposed |
| ca-ID-national_exchange | ID | — | national_exchange | Indonesia Stock Exchange | idx.co.id | exchange | data_feed | pricing_formula | proposed |
| ca-ID-central_bank | ID | — | central_bank | Bank Indonesia | bi.go.id | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-ID-environment_regulator | ID | — | environment_regulator | Ministry of Environment and Forestry | menlhk.go.id | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-ID-coast_guard_navy | ID | — | coast_guard_navy | Indonesian Maritime Security Agency (Bakamla) | bakamla.go.id | government_regulator | official | port_closure, vessel_loading, sanctions | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-ID-ministry_petroleum | Primary energy and oil/gas policy source. | OPEC-adjacent policy, subsidy and import context. | Logistics indirect. | proposed |
| ca-ID-noc | Pertamina is core operational/import and domestic fuel source. | Strategic state company and subsidy/import actor. | Direct cargo/refined-product relevance. | proposed |
| ca-ID-upstream_regulator | SKK Migas is the upstream oil/gas regulator/task force. | Licensing and partner context. | Direct production/project relevance. | proposed |
| ca-ID-port_maritime_authority | Sea Transportation directorate is relevant for maritime notices. | Sovereign infrastructure source. | Direct port/navigation relevance. | proposed |
| ca-ID-coast_guard_navy | Bakamla matters for Natuna, Malacca approaches and enforcement. | Maritime security relevance. | Security signal rather than ordinary cargo confirmation. | proposed |

---

### Unverified / Anti-patterns

- `Pertamina` is the NOC/import anchor, but refinery and cargo events still need cross-checks from port, customs, shipping and company-specific notices.
- `hubla.dephub.go.id` is a transport-ministry subdomain; preserve the path/domain detail if whitelist later collapses to a parent government domain.
- Do not treat Indonesia Stock Exchange or rupiah moves as physical oil/LNG flow evidence without official energy, customs, port or shipping confirmation.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 23,
  "last_country": "ID",
  "crosscheck_cursor": 0,
  "last_batch_seq": 27
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_028_country_authority_AU.md` (Fáze 2, Australia autority).
