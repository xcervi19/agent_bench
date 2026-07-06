# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_068_country_authority_DK.md  
**Fáze:** country_authority — krok DK (Fáze 2, Denmark)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná dávka Fáze 2 pro `DK` podle skeleton dimenze. Zdroje byly převzaty z referenční auditní dávky `composer-2-5_066_country_authority_DK.md` a zachovávají konzervativní statusy `proposed`, `unverified` a `empty`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-DK-ministry_petroleum | DK | — | ministry_petroleum | Danish Energy Agency | ens.dk | government_regulator | official | production,imports,storage_levels | proposed |
| ca-DK-noc | DK | — | noc | (no NOC — Nordsøfonden state partner) | — | noc | — | production,exports | empty |
| ca-DK-mfa | DK | — | mfa | Ministry of Foreign Affairs | um.dk | diplomacy | official | sanctions,export_license | proposed |
| ca-DK-customs_export | DK | — | customs_export | Danish Customs (Skat) | skat.dk | government_regulator | official | exports,export_license,imports | proposed |
| ca-DK-upstream_regulator | DK | — | upstream_regulator | Danish Energy Agency — Licensing | ens.dk | government_regulator | official | production,term_contract | proposed |
| ca-DK-port_maritime_authority | DK | — | port_maritime_authority | Danish Maritime Authority | dma.dk | infrastructure | official | vessel_loading,port_closure,exports | proposed |
| ca-DK-national_exchange | DK | — | national_exchange | Nasdaq Copenhagen | nasdaq.com | exchange | official | pricing_formula | unverified |
| ca-DK-central_bank | DK | — | central_bank | Danmarks Nationalbank | nationalbanken.dk | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-DK-environment_regulator | DK | — | environment_regulator | Danish Environmental Protection Agency | mst.dk | government_regulator | official | refinery_outage,production | proposed |
| ca-DK-coast_guard_navy | DK | — | coast_guard_navy | Royal Danish Navy | forsvaret.dk | government_regulator | official | port_closure,vessel_loading | proposed |

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
  "phase": "geo_target",
  "phase_index": 0,
  "last_country": "DK",
  "crosscheck_cursor": 0,
  "last_batch_seq": 68
}
```

Po merge této dávky → **další fáze:** `geo_target`, první dávka `gpt-5-5_069_geo_target_hormuz.md`.
