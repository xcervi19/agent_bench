# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_051_country_authority_GA.md  
**Fáze:** country_authority — krok GA (Fáze 2, Gabon)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná dávka Fáze 2 pro `GA` podle skeleton dimenze. Zdroje byly převzaty z referenční auditní dávky `composer-2-5_049_country_authority_GA.md` a zachovávají konzervativní statusy `proposed`, `unverified` a `empty`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-GA-ministry_petroleum | GA | — | ministry_petroleum | Ministry of Petroleum and Hydrocarbons | hydrocarbures.ga | government_regulator | official | production,exports,quota_rhetoric | proposed |
| ca-GA-noc | GA | — | noc | Gabon Oil Company (GOC) | gabonoil.ga | noc | official | production,exports,force_majeure,term_contract | proposed |
| ca-GA-mfa | GA | — | mfa | Ministry of Foreign Affairs | diplomatie.ga | diplomacy | official | sanctions,export_license | unverified |
| ca-GA-customs_export | GA | — | customs_export | General Directorate of Customs | douanes.ga | government_regulator | official | exports,export_license,imports | unverified |
| ca-GA-upstream_regulator | GA | — | upstream_regulator | Hydrocarbons Licensing | hydrocarbures.ga | government_regulator | official | production,term_contract | proposed |
| ca-GA-port_maritime_authority | GA | — | port_maritime_authority | Port of Owendo / Libreville | portsgabon.ga | infrastructure | official | vessel_loading,port_closure,exports | proposed |
| ca-GA-national_exchange | GA | — | national_exchange | (none) | — | exchange | — | — | empty |
| ca-GA-central_bank | GA | — | central_bank | BEAC (Central African) | beac.int | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-GA-environment_regulator | GA | — | environment_regulator | Ministry of Environment | environnement.ga | government_regulator | official | refinery_outage,production | unverified |
| ca-GA-coast_guard_navy | GA | — | coast_guard_navy | Gabonese Navy | defense.ga | government_regulator | official | port_closure,vessel_loading | unverified |

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
  "phase_index": 47,
  "last_country": "GA",
  "crosscheck_cursor": 0,
  "last_batch_seq": 51
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_052_country_authority_TD.md` (Fáze 2, Chad autority).
