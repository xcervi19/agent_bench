# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_060_country_authority_VN.md  
**Fáze:** country_authority — krok VN (Fáze 2, Vietnam)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná dávka Fáze 2 pro `VN` podle skeleton dimenze. Zdroje byly převzaty z referenční auditní dávky `composer-2-5_058_country_authority_VN.md` a zachovávají konzervativní statusy `proposed`, `unverified` a `empty`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-VN-ministry_petroleum | VN | — | ministry_petroleum | Ministry of Industry and Trade (MOIT) | moit.gov.vn | government_regulator | official | production,imports,storage_levels | proposed |
| ca-VN-noc | VN | — | noc | PetroVietnam (PVN) | pvn.vn | noc | official | production,exports,force_majeure,term_contract | proposed |
| ca-VN-mfa | VN | — | mfa | Ministry of Foreign Affairs | mofa.gov.vn | diplomacy | official | sanctions,export_license | proposed |
| ca-VN-customs_export | VN | — | customs_export | General Department of Vietnam Customs | customs.gov.vn | government_regulator | official | exports,export_license,imports | proposed |
| ca-VN-upstream_regulator | VN | — | upstream_regulator | Vietnam Oil and Gas Group — Upstream | pvn.vn | government_regulator | official | production,term_contract | proposed |
| ca-VN-port_maritime_authority | VN | — | port_maritime_authority | Vietnam Maritime Administration | vinamarine.gov.vn | infrastructure | official | vessel_loading,port_closure,exports | proposed |
| ca-VN-national_exchange | VN | — | national_exchange | HNX / HOSE (equities) | hnx.vn | exchange | official | pricing_formula | unverified |
| ca-VN-central_bank | VN | — | central_bank | State Bank of Vietnam | sbv.gov.vn | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-VN-environment_regulator | VN | — | environment_regulator | Ministry of Natural Resources and Environment | monre.gov.vn | government_regulator | official | refinery_outage,production | proposed |
| ca-VN-coast_guard_navy | VN | — | coast_guard_navy | Vietnam People's Navy | qdnd.vn | government_regulator | official | port_closure,vessel_loading | unverified |

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
  "phase_index": 56,
  "last_country": "VN",
  "crosscheck_cursor": 0,
  "last_batch_seq": 60
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_061_country_authority_PK.md` (Fáze 2, Pakistan autority).
