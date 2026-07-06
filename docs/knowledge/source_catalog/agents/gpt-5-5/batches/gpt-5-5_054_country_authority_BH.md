# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_054_country_authority_BH.md  
**Fáze:** country_authority — krok BH (Fáze 2, Bahrain)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná dávka Fáze 2 pro `BH` podle skeleton dimenze. Zdroje byly převzaty z referenční auditní dávky `composer-2-5_052_country_authority_BH.md` a zachovávají konzervativní statusy `proposed`, `unverified` a `empty`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-BH-ministry_petroleum | BH | — | ministry_petroleum | Ministry of Oil and Environment | moe.gov.bh | government_regulator | official | production,exports,quota_rhetoric | proposed |
| ca-BH-noc | BH | — | noc | Bapco Energies (incl. Bapco, Tatweer) | bapcoenergies.com | noc | official | production,exports,force_majeure,term_contract | proposed |
| ca-BH-mfa | BH | — | mfa | Ministry of Foreign Affairs | mofa.gov.bh | diplomacy | official | sanctions,export_license | proposed |
| ca-BH-customs_export | BH | — | customs_export | Customs Affairs | customs.gov.bh | government_regulator | official | exports,export_license,imports | proposed |
| ca-BH-upstream_regulator | BH | — | upstream_regulator | Tatweer Petroleum (upstream operator) | tatweerpetroleum.com | government_regulator | official | production,term_contract | proposed |
| ca-BH-port_maritime_authority | BH | — | port_maritime_authority | General Organisation of Sea Ports | ports.gov.bh | infrastructure | official | vessel_loading,port_closure,exports | proposed |
| ca-BH-national_exchange | BH | — | national_exchange | Bahrain Bourse | bahrainbourse.com | exchange | official | pricing_formula | unverified |
| ca-BH-central_bank | BH | — | central_bank | Central Bank of Bahrain | cbb.gov.bh | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-BH-environment_regulator | BH | — | environment_regulator | Supreme Council for the Environment | sce.gov.bh | government_regulator | official | refinery_outage,production | proposed |
| ca-BH-coast_guard_navy | BH | — | coast_guard_navy | Bahrain Defence Force Naval | bdf.bh | government_regulator | official | port_closure,vessel_loading | proposed |

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
  "phase_index": 50,
  "last_country": "BH",
  "crosscheck_cursor": 0,
  "last_batch_seq": 54
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_055_country_authority_IL.md` (Fáze 2, Israel autority).
