# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_065_country_authority_EC.md  
**Fáze:** country_authority — krok EC (Fáze 2, Ecuador)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná dávka Fáze 2 pro `EC` podle skeleton dimenze. Zdroje byly převzaty z referenční auditní dávky `composer-2-5_063_country_authority_EC.md` a zachovávají konzervativní statusy `proposed`, `unverified` a `empty`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-EC-ministry_petroleum | EC | — | ministry_petroleum | Ministry of Energy and Non-Renewable Natural Resources | recursosyenergia.gob.ec | government_regulator | official | production,exports,quota_rhetoric | proposed |
| ca-EC-noc | EC | — | noc | Petroecuador | petroecuador.ec | noc | official | production,exports,force_majeure,term_contract | proposed |
| ca-EC-mfa | EC | — | mfa | Ministry of Foreign Affairs | cancilleria.gob.ec | diplomacy | official | sanctions,export_license | proposed |
| ca-EC-customs_export | EC | — | customs_export | SENAE (Customs) | senae.gob.ec | government_regulator | official | exports,export_license,imports | proposed |
| ca-EC-upstream_regulator | EC | — | upstream_regulator | Hydrocarbons Regulation and Control Agency (ARCH) | arch.gob.ec | government_regulator | official | production,term_contract | proposed |
| ca-EC-port_maritime_authority | EC | — | port_maritime_authority | Empresa Pública Fluvial / Maritime Authority | maritima.gob.ec | infrastructure | official | vessel_loading,port_closure,exports | proposed |
| ca-EC-national_exchange | EC | — | national_exchange | Quito Stock Exchange (BVQ) | bvq.com.ec | exchange | official | pricing_formula | unverified |
| ca-EC-central_bank | EC | — | central_bank | Central Bank of Ecuador | bce.fin.ec | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-EC-environment_regulator | EC | — | environment_regulator | Ministry of Environment | ambiente.gob.ec | government_regulator | official | refinery_outage,production | proposed |
| ca-EC-coast_guard_navy | EC | — | coast_guard_navy | Ecuadorian Navy | armada.mil.ec | government_regulator | official | port_closure,vessel_loading | proposed |

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
  "phase_index": 61,
  "last_country": "EC",
  "crosscheck_cursor": 0,
  "last_batch_seq": 65
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_066_country_authority_TT.md` (Fáze 2, Trinidad and Tobago autority).
