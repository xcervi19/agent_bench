# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_064_country_authority_PE.md  
**Fáze:** country_authority — krok PE (Fáze 2, Peru)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná dávka Fáze 2 pro `PE` podle skeleton dimenze. Zdroje byly převzaty z referenční auditní dávky `composer-2-5_062_country_authority_PE.md` a zachovávají konzervativní statusy `proposed`, `unverified` a `empty`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-PE-ministry_petroleum | PE | — | ministry_petroleum | MINEM (Ministry of Energy and Mines) | gob.pe/minem | government_regulator | official | production,exports,quota_rhetoric | proposed |
| ca-PE-noc | PE | — | noc | Petroperú | petroperu.com.pe | noc | official | production,exports,force_majeure,term_contract | proposed |
| ca-PE-mfa | PE | — | mfa | Ministry of Foreign Affairs | rree.gob.pe | diplomacy | official | sanctions,export_license | proposed |
| ca-PE-customs_export | PE | — | customs_export | SUNAT (Customs) | sunat.gob.pe | government_regulator | official | exports,export_license,imports | proposed |
| ca-PE-upstream_regulator | PE | — | upstream_regulator | Perupetro | perupetro.com.pe | government_regulator | official | production,term_contract | proposed |
| ca-PE-port_maritime_authority | PE | — | port_maritime_authority | APN (National Port Authority) | gob.pe/apn | infrastructure | official | vessel_loading,port_closure,exports | proposed |
| ca-PE-national_exchange | PE | — | national_exchange | Lima Stock Exchange (BVL) | bvl.com.pe | exchange | official | pricing_formula | unverified |
| ca-PE-central_bank | PE | — | central_bank | Central Reserve Bank of Peru | bcrp.gob.pe | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-PE-environment_regulator | PE | — | environment_regulator | MINAM (Ministry of Environment) | gob.pe/minam | government_regulator | official | refinery_outage,production | proposed |
| ca-PE-coast_guard_navy | PE | — | coast_guard_navy | Peruvian Navy | marina.mil.pe | government_regulator | official | port_closure,vessel_loading | proposed |

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
  "phase_index": 60,
  "last_country": "PE",
  "crosscheck_cursor": 0,
  "last_batch_seq": 64
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_065_country_authority_EC.md` (Fáze 2, Ecuador autority).
