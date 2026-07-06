# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_063_country_authority_CL.md  
**Fáze:** country_authority — krok CL (Fáze 2, Chile)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná dávka Fáze 2 pro `CL` podle skeleton dimenze. Zdroje byly převzaty z referenční auditní dávky `composer-2-5_061_country_authority_CL.md` a zachovávají konzervativní statusy `proposed`, `unverified` a `empty`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-CL-ministry_petroleum | CL | — | ministry_petroleum | Ministry of Energy | energia.gob.cl | government_regulator | official | production,imports,storage_levels | proposed |
| ca-CL-noc | CL | — | noc | ENAP (Empresa Nacional del Petróleo) | enap.cl | noc | official | production,exports,force_majeure,term_contract | proposed |
| ca-CL-mfa | CL | — | mfa | Ministry of Foreign Affairs | minrel.gob.cl | diplomacy | official | sanctions,export_license | proposed |
| ca-CL-customs_export | CL | — | customs_export | National Customs Service | aduana.cl | government_regulator | official | exports,export_license,imports | proposed |
| ca-CL-upstream_regulator | CL | — | upstream_regulator | National Hydrocarbons Commission (CNH) | cnh.gob.cl | government_regulator | official | production,term_contract | proposed |
| ca-CL-port_maritime_authority | CL | — | port_maritime_authority | Directemar (Maritime Authority) | directemar.cl | infrastructure | official | vessel_loading,port_closure,exports | proposed |
| ca-CL-national_exchange | CL | — | national_exchange | Santiago Stock Exchange (BCS) | bcs.cl | exchange | official | pricing_formula | unverified |
| ca-CL-central_bank | CL | — | central_bank | Central Bank of Chile | bcentral.cl | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-CL-environment_regulator | CL | — | environment_regulator | Ministry of Environment (MMA) | mma.gob.cl | government_regulator | official | refinery_outage,production | proposed |
| ca-CL-coast_guard_navy | CL | — | coast_guard_navy | Chilean Navy | armada.cl | government_regulator | official | port_closure,vessel_loading | proposed |

---

### Cross-check (3 perspektivy)

- Supply: prioritizovat ministerstvo, NOC/upstream regulator a produkční/exportní signály.
- Geopolitics: používat MFA, customs a central bank jako sankční, licenční a platební kontext.
- Logistics: port/coast guard sloty používat jen po ověření domény; `empty` sloty nevynucovat náhradními komerčními zdroji.

---

### Unverified / Anti-patterns

- `unverified` položky před whitelistem ručně validovat proti oficiálním doménám a aktuální dostupnosti.
- `empty` položky neplnit soukromými firmami, pokud chybí přímý státní/NOC nebo maritime ekvivalent.
- Market/exchange zdroje nejsou důkaz fyzických toků bez triangulace s official, operator, port a shipping zdroji.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 59,
  "last_country": "CL",
  "crosscheck_cursor": 0,
  "last_batch_seq": 63
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_064_country_authority_PE.md` (Fáze 2, Peru autority).
