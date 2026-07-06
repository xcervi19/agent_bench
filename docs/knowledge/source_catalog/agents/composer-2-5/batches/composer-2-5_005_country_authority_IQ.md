# Catalog batch

**Agent:** composer-2-5 (Composer 2.5)  
**Soubor:** composer-2-5_005_country_authority_IQ.md  
**Fáze:** country_authority — krok IQ (Fáze 2, země 3/64)  
**Datum:** 2026-07-04  

---

## Shrnutí

Iraq × 10 autorit. **8 proposed**, **2 unverified** (customs domain; national_exchange — equity-only ISX).

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-IQ-ministry_petroleum | IQ | — | ministry_petroleum | Ministry of Oil | oil.gov.iq | government_regulator | official | production,exports,quota_rhetoric | proposed |
| ca-IQ-noc | IQ | — | noc | SOMO (State Organization for Marketing of Oil) | somooil.gov.iq | noc | official | exports,term_contract,pricing_formula | proposed |
| ca-IQ-mfa | IQ | — | mfa | Ministry of Foreign Affairs | mfa.gov.iq | diplomacy | official | sanctions,export_license | proposed |
| ca-IQ-customs_export | IQ | — | customs_export | General Commission for Customs | customs.gov.iq | government_regulator | official | exports,export_license,imports | unverified |
| ca-IQ-upstream_regulator | IQ | — | upstream_regulator | Basra Oil Company (BOC) | oil.gov.iq | government_regulator | official | production,term_contract | proposed |
| ca-IQ-port_maritime_authority | IQ | — | port_maritime_authority | State Company for Iraqi Ports (SCOP) | scop.iq | infrastructure | official | vessel_loading,port_closure,exports | proposed |
| ca-IQ-national_exchange | IQ | — | national_exchange | Iraq Stock Exchange (ISX) | isx-iq.net | exchange | official | pricing_formula | unverified |
| ca-IQ-central_bank | IQ | — | central_bank | Central Bank of Iraq | cbiraq.org | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-IQ-environment_regulator | IQ | — | environment_regulator | Ministry of Environment | moenv.gov.iq | government_regulator | official | refinery_outage,production | proposed |
| ca-IQ-coast_guard_navy | IQ | — | coast_guard_navy | Ministry of Defence (Iraqi Navy) | mod.gov.iq | government_regulator | official | port_closure,vessel_loading | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-IQ-ministry_petroleum | Production targets, field restarts | KRG / federal revenue-sharing disputes | Southern export capacity policy | **proposed** |
| ca-IQ-noc | Official export program, OSP-related marketing | US waiver / sanctions compliance | Basra terminal liftings, cargo allocation | **proposed** |
| ca-IQ-mfa | — | Regional diplomacy, Turkey / Iran transit | Diplomatic incidents at export routes | **proposed** |
| ca-IQ-customs_export | — | Cross-border KRG crude disputes | Clearance at Umm Qasr / border posts | **unverified** — domain needs manual check |
| ca-IQ-upstream_regulator | Southern field ops (Rumaila, West Qurna) | Licensing round / contract stability | BOC-operated terminal feed | **proposed** (shared ministry domain — BOC under MoO) |
| ca-IQ-port_maritime_authority | — | — | Umm Qasr, Khor al-Zubair, Basra Oil Terminal | **proposed** |
| ca-IQ-national_exchange | — | — | No crude futures; equities only | **unverified** — Tier 2 |
| ca-IQ-central_bank | — | FX repatriation rules (CBI auction) | Payment delays affecting export flows | **proposed** |
| ca-IQ-environment_regulator | Flaring / compliance orders | — | Refinery environmental shutdowns | **proposed** |
| ca-IQ-coast_guard_navy | — | Gulf security coordination | Umm Qasr / territorial water protection | **proposed** |

---

### Unverified / Anti-patterns

| id | issue |
|----|-------|
| ca-IQ-customs_export | `customs.gov.iq` — verify live site; alt under Ministry of Finance |
| ca-IQ-national_exchange | ISX — no energy derivatives market |
| ca-IQ-upstream_regulator | BOC shares `oil.gov.iq` with ministry — intentional matrix slot |

**KRG gap:** Kurdistan Regional Government oil exports (MNR knr.krd / KRG Ministry of Natural Resources) — **not in federal matrix**; flag for playbook #30 Iraq/KRG extension.

**Desk note:** Tier 1 = **oil.gov.iq + somooil.gov.iq + scop.iq**. Basra export outages surface on SOMO/MoO before Reuters.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 4,
  "last_country": "IQ",
  "crosscheck_cursor": 0,
  "last_batch_seq": 5
}
```

**Další dávka:** `composer-2-5_006_country_authority_RU.md` (Russia × 10 autorit).

### Whitelist kandidáti (Tier 1, po schválení)

`oil.gov.iq`, `somooil.gov.iq`, `mfa.gov.iq`, `scop.iq`, `cbiraq.org`, `moenv.gov.iq`, `mod.gov.iq`
