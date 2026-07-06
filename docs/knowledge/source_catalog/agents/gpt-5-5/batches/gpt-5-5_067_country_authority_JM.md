# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_067_country_authority_JM.md  
**Fáze:** country_authority — krok JM (Fáze 2, Jamaica)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná dávka Fáze 2 pro `JM` podle skeleton dimenze. Zdroje byly převzaty z referenční auditní dávky `composer-2-5_065_country_authority_JM.md` a zachovávají konzervativní statusy `proposed`, `unverified` a `empty`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-JM-ministry_petroleum | JM | — | ministry_petroleum | Ministry of Science, Energy and Technology | mset.gov.jm | government_regulator | official | production,imports,storage_levels | proposed |
| ca-JM-noc | JM | — | noc | Petrojam (refining) / PCJ | pcj.com | noc | official | production,imports,refinery_outage | proposed |
| ca-JM-mfa | JM | — | mfa | Ministry of Foreign Affairs and Foreign Trade | mfaft.gov.jm | diplomacy | official | sanctions,export_license | proposed |
| ca-JM-customs_export | JM | — | customs_export | Jamaica Customs Agency | jacustoms.gov.jm | government_regulator | official | exports,export_license,imports | proposed |
| ca-JM-upstream_regulator | JM | — | upstream_regulator | Petroleum Corporation of Jamaica | pcj.com | government_regulator | official | production,term_contract | proposed |
| ca-JM-port_maritime_authority | JM | — | port_maritime_authority | Port Authority of Jamaica | portjam.com | infrastructure | official | vessel_loading,port_closure,imports | proposed |
| ca-JM-national_exchange | JM | — | national_exchange | Jamaica Stock Exchange | jamstockex.com | exchange | official | pricing_formula | unverified |
| ca-JM-central_bank | JM | — | central_bank | Bank of Jamaica | boj.org.jm | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-JM-environment_regulator | JM | — | environment_regulator | National Environment and Planning Agency | nepa.gov.jm | government_regulator | official | refinery_outage,production | proposed |
| ca-JM-coast_guard_navy | JM | — | coast_guard_navy | Jamaica Defence Force Coast Guard | jdf.gov.jm | government_regulator | official | port_closure,vessel_loading | proposed |

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
  "phase_index": 63,
  "last_country": "JM",
  "crosscheck_cursor": 0,
  "last_batch_seq": 67
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_068_country_authority_DK.md` (Fáze 2, Denmark autority).
