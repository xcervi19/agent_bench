# Catalog batch

**Agent:** composer-2-5 (Composer 2.5)  
**Soubor:** composer-2-5_008_country_authority_AE.md  
**Fáze:** country_authority — krok AE (Fáze 2, země 6/64)  
**Datum:** 2026-07-05  

---

## Shrnutí

UAE × 10 autorit. **9 proposed**, **1 unverified** (coast_guard_navy — MOD site; federální vs emirát struktura).

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-AE-ministry_petroleum | AE | — | ministry_petroleum | Ministry of Energy and Infrastructure | moei.gov.ae | government_regulator | official | production,exports,quota_rhetoric | proposed |
| ca-AE-noc | AE | — | noc | ADNOC | adnoc.ae | noc | official | production,exports,force_majeure,term_contract | proposed |
| ca-AE-mfa | AE | — | mfa | Ministry of Foreign Affairs (MOFAIC) | mofaic.gov.ae | diplomacy | official | sanctions,export_license | proposed |
| ca-AE-customs_export | AE | — | customs_export | Federal Customs Authority | fcauae.gov.ae | government_regulator | official | exports,export_license,imports | proposed |
| ca-AE-upstream_regulator | AE | — | upstream_regulator | Abu Dhabi Department of Energy | ade.gov.ae | government_regulator | official | production,term_contract | proposed |
| ca-AE-port_maritime_authority | AE | — | port_maritime_authority | Abu Dhabi Ports (AD Ports Group) | adports.ae | infrastructure | official | vessel_loading,port_closure,exports | proposed |
| ca-AE-national_exchange | AE | — | national_exchange | Dubai Mercantile Exchange (DGCX) | dgcx.ae | exchange | official | pricing_formula,exports | proposed |
| ca-AE-central_bank | AE | — | central_bank | Central Bank of the UAE | centralbank.ae | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-AE-environment_regulator | AE | — | environment_regulator | Ministry of Climate Change and Environment | moccae.gov.ae | government_regulator | official | refinery_outage,production | proposed |
| ca-AE-coast_guard_navy | AE | — | coast_guard_navy | Ministry of Defence (UAE Armed Forces) | mod.gov.ae | government_regulator | official | port_closure,vessel_loading | unverified |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-AE-ministry_petroleum | UAE OPEC+ quota statements | Gulf diplomacy, Iran proximity | Export policy coordination with ADNOC | **proposed** |
| ca-AE-noc | Production capacity, OSP, downstream expansion | ADNOC IPO / foreign asset strategy | Ruwais, Fujairah, Jebel Ali export routes | **proposed** |
| ca-AE-mfa | — | Red Sea / Hormuz diplomacy, normalization accords | Sanctions / shipping insurance rhetoric | **proposed** |
| ca-AE-customs_export | — | Re-export hub enforcement | Jebel Ali / free zone clearance | **proposed** |
| ca-AE-upstream_regulator | Abu Dhabi field development | Concession terms | ADNOC capacity ramp | **proposed** — Dubai upstream separate (Dubai Petroleum) |
| ca-AE-port_maritime_authority | — | — | Fujairah bunkering, Ruwais refinery port, Khalifa Port | **proposed** |
| ca-AE-national_exchange | Oman/Dubai crude marker contracts | — | Middle East sour pricing discovery | **proposed** — overlaps global DGCX |
| ca-AE-central_bank | — | Sanctions compliance / correspondent banking | Oil payment settlement | **proposed** |
| ca-AE-environment_regulator | Environmental compliance | — | Refinery / industrial permits | **proposed** |
| ca-AE-coast_guard_navy | — | Gulf naval exercises, Red Sea escort | Strait of Hormuz patrol | **unverified** — `mod.gov.ae` generic MOD portal |

---

### Unverified / Anti-patterns

| id | issue |
|----|-------|
| ca-AE-coast_guard_navy | MOD site — not dedicated navy ops feed |
| ca-AE-upstream_regulator | Abu Dhabi-centric; Dubai `dubai.ae` / ENOC separate emirate layer |

**Playbook extensions:** Fujairah bunkering hub (`fujairah.ae` / port ops), `enoc.com` (Dubai), `dpworld.com` (Jebel Ali operator — logistics context).

**Desk note:** Tier 1 = **adnoc.ae + moei.gov.ae + adports.ae + dgcx.ae**. Fujairah storage/barging signals often precede Gulf diff moves.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 7,
  "last_country": "AE",
  "crosscheck_cursor": 0,
  "last_batch_seq": 8
}
```

**Další dávka:** `composer-2-5_009_country_authority_KW.md` (Kuwait × 10 autorit).

### Whitelist kandidáti (Tier 1, po schválení)

`adnoc.ae`, `moei.gov.ae`, `mofaic.gov.ae`, `fcauae.gov.ae`, `ade.gov.ae`, `adports.ae`, `dgcx.ae`, `centralbank.ae`, `moccae.gov.ae`
