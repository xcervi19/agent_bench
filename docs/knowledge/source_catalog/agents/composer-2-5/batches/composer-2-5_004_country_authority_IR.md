# Catalog batch

**Agent:** composer-2-5 (Composer 2.5)  
**Soubor:** composer-2-5_004_country_authority_IR.md  
**Fáze:** country_authority — krok IR (Fáze 2, země 2/64)  
**Datum:** 2026-07-04  

---

## Shrnutí

Iran × 10 autorit. **9 proposed**, **1 unverified** (coast_guard_navy — IRGC vs regular navy).

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-IR-ministry_petroleum | IR | — | ministry_petroleum | Ministry of Petroleum | mop.ir | government_regulator | official | production,exports,quota_rhetoric | proposed |
| ca-IR-noc | IR | — | noc | NIOC | nioc.ir | noc | official | production,exports,force_majeure,term_contract | proposed |
| ca-IR-mfa | IR | — | mfa | Ministry of Foreign Affairs | mfa.gov.ir | diplomacy | official | sanctions,export_license | proposed |
| ca-IR-customs_export | IR | — | customs_export | Islamic Republic of Iran Customs (IRICA) | irica.gov.ir | government_regulator | official | exports,export_license,imports | proposed |
| ca-IR-upstream_regulator | IR | — | upstream_regulator | PEDEC (Petroleum Engineering & Development) | pedec.ir | government_regulator | official | production,term_contract | proposed |
| ca-IR-port_maritime_authority | IR | — | port_maritime_authority | Ports & Maritime Organization (PMO) | pmo.ir | infrastructure | official | vessel_loading,port_closure,exports | proposed |
| ca-IR-national_exchange | IR | — | national_exchange | Iran Mercantile Exchange (IME) | ime.co.ir | exchange | official | pricing_formula,exports | proposed |
| ca-IR-central_bank | IR | — | central_bank | Central Bank of Iran | cb.ir | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-IR-environment_regulator | IR | — | environment_regulator | Department of Environment | doe.ir | government_regulator | official | refinery_outage,production | proposed |
| ca-IR-coast_guard_navy | IR | — | coast_guard_navy | Islamic Republic of Iran Navy | navy.ir | government_regulator | official | port_closure,vessel_loading | unverified |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-IR-ministry_petroleum | Production capacity statements, OPEC+ compliance | Nuclear/sanctions diplomacy linkage | Export allocation policy | **proposed** |
| ca-IR-noc | Field output, maintenance, term contracts | — | Kharg Island loading, NITC tanker ops (via NIOC group) | **proposed** |
| ca-IR-mfa | — | Sanctions response, Hormuz closure rhetoric, JCPOA | Diplomatic escalation → insurance / freight | **proposed** |
| ca-IR-customs_export | — | Embargo enforcement | Export clearance delays | **proposed** |
| ca-IR-upstream_regulator | New field / EOR project approvals | Contract model under sanctions | Capacity ramp timelines | **proposed** |
| ca-IR-port_maritime_authority | — | — | Bandar Imam, Kharg, Asaluyeh, Chabahar port status | **proposed** |
| ca-IR-national_exchange | Domestic crude / petrochemical auction prices | — | Physical delivery via IME oil ring | **proposed** — also watch enex.ir for energy-specific ring |
| ca-IR-central_bank | — | FX policy under sanctions (NIMA/SANA) | Payment channel for oil exports | **proposed** |
| ca-IR-environment_regulator | Compliance shutdowns | — | Refinery environmental orders | **proposed** |
| ca-IR-coast_guard_navy | — | Hormuz seizure / escort rhetoric | IRGC Navy often operational lead vs navy.ir | **unverified** — desk also monitors IRGC statements via official press channels |

---

### Unverified / Anti-patterns

| id | issue |
|----|-------|
| ca-IR-coast_guard_navy | `navy.ir` — regular navy site; Hormuz incidents often IRGC-led; no single IRGC official English domain for whitelist |
| ca-IR-national_exchange | `enex.ir` (Iran Energy Exchange) overlaps IME oil ring — consider sub-slot in crosscheck phase |

**Desk note:** Iran desk Tier 1 = **mop.ir + nioc.ir + pmo.ir + mfa.gov.ir**. Sanctions context: pair with OFAC (`treasury.gov`, already in global batch). Kharg / Bandar Imam loading delays hit before newswires.

**Anti-patterns:** aggregators mirroring NIOC data; unofficial Telegram NIOC news mirrors.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 3,
  "last_country": "IR",
  "crosscheck_cursor": 0,
  "last_batch_seq": 4
}
```

**Další dávka:** `composer-2-5_005_country_authority_IQ.md` (Iraq × 10 autorit).

### Whitelist kandidáti (Tier 1, po schválení)

`mop.ir`, `nioc.ir`, `mfa.gov.ir`, `irica.gov.ir`, `pedec.ir`, `pmo.ir`, `ime.co.ir`, `cb.ir`, `doe.ir`
