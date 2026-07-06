# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_060_country_authority_BD.md  
**Fáze:** country_authority — krok BD (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Bangladéš (`BD`), 10 slotů (`ca-BD-{authority}`). **LNG importér** s domácím plynem v úpadku; Petrobangla,
BPC, Moheshkhali FSRU. FX krize → spot LNG citlivost. 6 `proposed`, 3 `unverified`, 1 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-BD-ministry_petroleum | ministry_petroleum | Ministry of Power, Energy & Mineral Res | mpemr.gov.bd | government_regulator | official | imports, production | proposed |
| ca-BD-noc | noc | Petrobangla / BPC | petrobangla.org.bd | noc | official | production, imports | proposed |
| ca-BD-mfa | mfa | Ministry of Foreign Affairs | mofa.gov.bd | diplomacy | official | sanctions | unverified |
| ca-BD-customs_export | customs_export | National Board of Revenue (Customs) | nbr.gov.bd | government_regulator | official | imports | unverified |
| ca-BD-upstream_regulator | upstream_regulator | BERC / Petrobangla | berc.org.bd | government_regulator | official | pricing_formula | proposed |
| ca-BD-port_maritime_authority | port_maritime_authority | Chittagong Port / Moheshkhali FSRU | cpa.gov.bd | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-BD-national_exchange | national_exchange | — (DSE financial only) | — | — | — | — | empty |
| ca-BD-central_bank | central_bank | Bangladesh Bank | bb.org.bd | government_regulator | official | sanctions | proposed |
| ca-BD-environment_regulator | environment_regulator | Dept of Environment | doe.gov.bd | government_regulator | official | refinery_outage | unverified |
| ca-BD-coast_guard_navy | coast_guard_navy | Bangladesh Coast Guard | coastguard.gov.bd | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-BD-noc (Petrobangla) | domácí plyn decline | **FX krize → spot LNG cancel** | Moheshkhali FSRU (2×) | proposed — price-sensitive kupec |

### Poznámky

- Podobně jako PK: **FX krize** → citlivý spot LNG kupec (JKM demand elasticity).
- Moheshkhali FSRU (Summit/Excelerate) = import kapacita; výpadky = supply signál.
- DSE = jen finanční (empty).

### Progress po merge

`last_country: BD`, `last_batch_seq: 60`
