# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_066_country_authority_TT.md  
**Fáze:** country_authority — krok TT (Fáze 2, Trinidad and Tobago)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná dávka Fáze 2 pro `TT` podle skeleton dimenze. Zdroje byly převzaty z referenční auditní dávky `composer-2-5_064_country_authority_TT.md` a zachovávají konzervativní statusy `proposed`, `unverified` a `empty`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-TT-ministry_petroleum | TT | — | ministry_petroleum | Ministry of Energy and Energy Industries | energy.gov.tt | government_regulator | official | production,exports,quota_rhetoric | proposed |
| ca-TT-noc | TT | — | noc | Heritage Petroleum | heritagepetroleum.co.tt | noc | official | production,exports,force_majeure | proposed |
| ca-TT-mfa | TT | — | mfa | Ministry of Foreign and CARICOM Affairs | foreign.gov.tt | diplomacy | official | sanctions,export_license | proposed |
| ca-TT-customs_export | TT | — | customs_export | Customs and Excise Division | customs.gov.tt | government_regulator | official | exports,export_license,imports | proposed |
| ca-TT-upstream_regulator | TT | — | upstream_regulator | Ministry — Petroleum Affairs | energy.gov.tt | government_regulator | official | production,term_contract | proposed |
| ca-TT-port_maritime_authority | TT | — | port_maritime_authority | Port Authority of Trinidad and Tobago | patnt.com | infrastructure | official | vessel_loading,port_closure,exports | proposed |
| ca-TT-national_exchange | TT | — | national_exchange | Trinidad and Tobago Stock Exchange | stockex.co.tt | exchange | official | pricing_formula | unverified |
| ca-TT-central_bank | TT | — | central_bank | Central Bank of Trinidad and Tobago | central-bank.org.tt | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-TT-environment_regulator | TT | — | environment_regulator | Environmental Management Authority | ema.gov.tt | government_regulator | official | refinery_outage,production | proposed |
| ca-TT-coast_guard_navy | TT | — | coast_guard_navy | Trinidad and Tobago Coast Guard | ttcoastguard.gov.tt | government_regulator | official | port_closure,vessel_loading | proposed |

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
  "phase_index": 62,
  "last_country": "TT",
  "crosscheck_cursor": 0,
  "last_batch_seq": 66
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_067_country_authority_JM.md` (Fáze 2, Jamaica autority).
