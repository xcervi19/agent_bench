# Catalog batch

**Agent:** composer-2-5 (Composer 2.5)  
**Soubor:** composer-2-5_007_country_authority_US.md  
**Fáze:** country_authority — krok US (Fáze 2, země 5/64)  
**Datum:** 2026-07-05  

---

## Shrnutí

United States × 10 autorit. **9 proposed**, **1 empty** (noc — USA nemá NOC; sledovat soukromé majory v playbooku).

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-US-ministry_petroleum | US | — | ministry_petroleum | Department of Energy (DOE) | energy.gov | government_regulator | official | production,exports,storage_levels | proposed |
| ca-US-noc | US | — | noc | (no national NOC) | — | noc | — | production,exports | empty |
| ca-US-mfa | US | — | mfa | Department of State | state.gov | diplomacy | official | sanctions,export_license | proposed |
| ca-US-customs_export | US | — | customs_export | Customs and Border Protection (CBP) | cbp.gov | government_regulator | official | exports,export_license,imports | proposed |
| ca-US-upstream_regulator | US | — | upstream_regulator | Bureau of Ocean Energy Management (BOEM) | boem.gov | government_regulator | official | production,term_contract | proposed |
| ca-US-port_maritime_authority | US | — | port_maritime_authority | MARAD | maritime.dot.gov | infrastructure | official | vessel_loading,port_closure | proposed |
| ca-US-national_exchange | US | — | national_exchange | CME Group (NYMEX) | cmegroup.com | exchange | official | pricing_formula,storage_levels | proposed |
| ca-US-central_bank | US | — | central_bank | Federal Reserve | federalreserve.gov | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-US-environment_regulator | US | — | environment_regulator | EPA | epa.gov | government_regulator | official | refinery_outage,production | proposed |
| ca-US-coast_guard_navy | US | — | coast_guard_navy | U.S. Coast Guard | uscg.mil | government_regulator | official | port_closure,vessel_loading | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-US-ministry_petroleum | SPR release announcements, LNG export authorizations | Energy diplomacy, sanctions packages | Export ban / licensing (crude, products) | **proposed** — overlaps global `energy.gov` |
| ca-US-noc | Private producers (Exxon, Chevron, Conoco) | — | No state NOC | **empty** — playbook Tier 1 = private majors + EIA |
| ca-US-mfa | — | Sanctions designations coordination with Treasury | Export control diplomacy | **proposed** |
| ca-US-customs_export | — | Trade enforcement | Border / export clearance | **proposed** |
| ca-US-upstream_regulator | Gulf of Mexico lease sales, drilling permits | Offshore moratorium policy | Offshore production timeline | **proposed** |
| ca-US-port_maritime_authority | — | — | Houston, LOOP, NOLA, West Coast port status | **proposed** — pair USACE district sites in playbook |
| ca-US-national_exchange | WTI / Henry Hub futures | — | Cushing delivery, Gulf Coast diffs | **proposed** — overlaps global CME |
| ca-US-central_bank | — | Sanctions / rate policy | Dollar funding for commodities | **proposed** |
| ca-US-environment_regulator | Refinery compliance, RFS | — | Plant shutdown orders | **proposed** |
| ca-US-coast_guard_navy | — | Gulf / Strait patrol | Port closure, hurricane response | **proposed** |

---

### Unverified / Anti-patterns

| id | issue |
|----|-------|
| ca-US-noc | Matrix slot intentionally **empty** — US model differs from Gulf NOC states |
| ca-US-ministry_petroleum | DOE also covers SPR — distinct from EIA (`eia.gov`, global batch) |

**Playbook extensions (Tier 1, mimo slot):** `eia.gov`, `ferc.gov`, `phmsa.dot.gov`, `treasury.gov` (OFAC), `bsee.gov` (offshore safety), `blm.gov` (onshore federal).

**Desk note:** Tier 1 = **energy.gov + eia.gov + cmegroup.com + uscg.mil**. Hurricane / Gulf outage stack: NHC + BOEM + BSEE.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 6,
  "last_country": "US",
  "crosscheck_cursor": 0,
  "last_batch_seq": 7
}
```

**Další dávka:** `composer-2-5_008_country_authority_AE.md` (UAE × 10 autorit).

### Whitelist kandidáti (Tier 1, po schválení)

`energy.gov`, `state.gov`, `cbp.gov`, `boem.gov`, `maritime.dot.gov`, `cmegroup.com`, `federalreserve.gov`, `epa.gov`, `uscg.mil`
