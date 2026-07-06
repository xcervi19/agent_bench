# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_050_country_authority_CG.md  
**Fáze:** country_authority — krok CG (Fáze 2, Congo)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná dávka Fáze 2 pro `CG` podle skeleton dimenze. Zdroje byly převzaty z referenční auditní dávky `composer-2-5_048_country_authority_CG.md` a zachovávají konzervativní statusy `proposed`, `unverified` a `empty`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-CG-ministry_petroleum | CG | — | ministry_petroleum | Ministry of Hydrocarbons | hydrocarbures.gouv.cg | government_regulator | official | production,exports,quota_rhetoric | proposed |
| ca-CG-noc | CG | — | noc | SNPC (Société Nationale des Pétroles du Congo) | snpc.cg | noc | official | production,exports,force_majeure,term_contract | proposed |
| ca-CG-mfa | CG | — | mfa | Ministry of Foreign Affairs | diplomatie.gouv.cg | diplomacy | official | sanctions,export_license | proposed |
| ca-CG-customs_export | CG | — | customs_export | Directorate General of Customs | douanes.gouv.cg | government_regulator | official | exports,export_license,imports | unverified |
| ca-CG-upstream_regulator | CG | — | upstream_regulator | Hydrocarbons Licensing Directorate | hydrocarbures.gouv.cg | government_regulator | official | production,term_contract | proposed |
| ca-CG-port_maritime_authority | CG | — | port_maritime_authority | Port Autonome de Pointe-Noire | port-pointenoire.cg | infrastructure | official | vessel_loading,port_closure,exports | proposed |
| ca-CG-national_exchange | CG | — | national_exchange | (none) | — | exchange | — | — | empty |
| ca-CG-central_bank | CG | — | central_bank | BEAC (Central African) | beac.int | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-CG-environment_regulator | CG | — | environment_regulator | Ministry of Environment | environnement.gouv.cg | government_regulator | official | refinery_outage,production | unverified |
| ca-CG-coast_guard_navy | CG | — | coast_guard_navy | Congolese Navy | defense.gouv.cg | government_regulator | official | port_closure,vessel_loading | unverified |

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
  "phase_index": 46,
  "last_country": "CG",
  "crosscheck_cursor": 0,
  "last_batch_seq": 50
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_051_country_authority_GA.md` (Fáze 2, Gabon autority).
