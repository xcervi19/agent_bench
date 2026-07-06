# Catalog batch

**Agent:** composer-2-5 (Composer 2.5)  
**Soubor:** composer-2-5_003_country_authority_SA.md  
**Fáze:** country_authority — krok SA (Fáze 2, země 1/64)  
**Datum:** 2026-07-04  

---

## Shrnutí

Saudi Arabia × 10 autorit. **9 proposed**, **1 unverified** (national_exchange — Tadawul není commodity burza).

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-SA-ministry_petroleum | SA | — | ministry_petroleum | Ministry of Energy | energy.gov.sa | government_regulator | official | production,exports,quota_rhetoric | proposed |
| ca-SA-noc | SA | — | noc | Saudi Aramco | aramco.com | noc | official | production,exports,force_majeure,term_contract | proposed |
| ca-SA-mfa | SA | — | mfa | Ministry of Foreign Affairs | mofa.gov.sa | diplomacy | official | sanctions,export_license | proposed |
| ca-SA-customs_export | SA | — | customs_export | ZATCA (Customs) | zatca.gov.sa | government_regulator | official | exports,export_license,imports | proposed |
| ca-SA-upstream_regulator | SA | — | upstream_regulator | Ministry of Energy — Hydrocarbon Affairs | energy.gov.sa | government_regulator | official | production,term_contract | proposed |
| ca-SA-port_maritime_authority | SA | — | port_maritime_authority | Saudi Ports Authority (Mawani) | mawani.gov.sa | infrastructure | official | vessel_loading,port_closure,exports | proposed |
| ca-SA-national_exchange | SA | — | national_exchange | Saudi Exchange (Tadawul) | saudiexchange.sa | exchange | official | pricing_formula | unverified |
| ca-SA-central_bank | SA | — | central_bank | Saudi Central Bank (SAMA) | sama.gov.sa | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-SA-environment_regulator | SA | — | environment_regulator | National Center for Environmental Compliance | ncec.gov.sa | government_regulator | official | refinery_outage,production | proposed |
| ca-SA-coast_guard_navy | SA | — | coast_guard_navy | Ministry of Defense (Royal Saudi Navy) | mod.gov.sa | government_regulator | official | port_closure,vessel_loading | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-SA-ministry_petroleum | OPEC+ quota compliance statements | Energy minister diplomacy, spare capacity rhetoric | Export program / terminal allocation policy | **proposed** |
| ca-SA-noc | Monthly Official Selling Prices, production updates | CEO/state visits, downstream investment | Ras Tanura / Yanbu / Jubail loading, tanker program | **proposed** |
| ca-SA-mfa | — | Iran/Yemen/Houthi Red Sea statements, US alliance | Diplomatic incidents affecting transit | **proposed** |
| ca-SA-customs_export | — | Export ban enforcement | Customs clearance delays at ports | **proposed** |
| ca-SA-upstream_regulator | Field development approvals | PSC / concession policy | New capacity timeline | **proposed** (same domain as ministry — distinct slot, shared site) |
| ca-SA-port_maritime_authority | — | — | King Fahd Industrial Port, Jeddah, Yanbu, Duba port ops | **proposed** |
| ca-SA-national_exchange | — | — | Equities-only; no crude/LNG futures | **unverified** — Tier 2; desk uses ICE/CME not Tadawul |
| ca-SA-central_bank | — | Sanctions compliance FX rules | Payment routing for oil exports | **proposed** |
| ca-SA-environment_regulator | Environmental compliance shutdowns | — | Refinery/emissions enforcement | **proposed** |
| ca-SA-coast_guard_navy | — | Red Sea / Gulf security operations | Hormuz/Bab el-Mandeb escort, port security | **proposed** |

---

### Unverified / Anti-patterns

| id | issue |
|----|-------|
| ca-SA-national_exchange | Tadawul — national equity exchange; no energy derivatives; slot kept for matrix completeness |
| ca-SA-upstream_regulator | Shares `energy.gov.sa` with ministry slot — intentional; different signal focus |

**Desk note:** For SA oil flows, monitor **Aramco + Ministry of Energy + Mawani** before any media. MFA spikes on Red Sea / Iran tension.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 2,
  "last_country": "SA",
  "crosscheck_cursor": 0,
  "last_batch_seq": 3
}
```

**Další dávka:** `composer-2-5_004_country_authority_IR.md` (Iran × 10 autorit).

### Whitelist kandidáti (Tier 1, po schválení)

`energy.gov.sa`, `aramco.com`, `mofa.gov.sa`, `zatca.gov.sa`, `mawani.gov.sa`, `sama.gov.sa`, `ncec.gov.sa`, `mod.gov.sa`
