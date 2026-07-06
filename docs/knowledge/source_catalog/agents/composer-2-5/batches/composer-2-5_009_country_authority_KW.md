# Catalog batch

**Agent:** composer-2-5 (Composer 2.5)  
**Soubor:** composer-2-5_009_country_authority_KW.md  
**Fáze:** country_authority — krok KW (Fáze 2, země 7/64)  
**Datum:** 2026-07-05  

---

## Shrnutí

Kuwait × 10 autorit. **9 proposed**, **1 unverified** (national_exchange — Boursa Kuwait bez energetických derivátů).

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-KW-ministry_petroleum | KW | — | ministry_petroleum | Ministry of Oil | moo.gov.kw | government_regulator | official | production,exports,quota_rhetoric | proposed |
| ca-KW-noc | KW | — | noc | Kuwait Petroleum Corporation (KPC) | kpc.com.kw | noc | official | production,exports,force_majeure,term_contract | proposed |
| ca-KW-mfa | KW | — | mfa | Ministry of Foreign Affairs | mofa.gov.kw | diplomacy | official | sanctions,export_license | proposed |
| ca-KW-customs_export | KW | — | customs_export | Kuwait General Administration of Customs | customs.gov.kw | government_regulator | official | exports,export_license,imports | proposed |
| ca-KW-upstream_regulator | KW | — | upstream_regulator | Kuwait Oil Company (KOC) | kockw.com | government_regulator | official | production,term_contract | proposed |
| ca-KW-port_maritime_authority | KW | — | port_maritime_authority | Kuwait Ports Authority (KPA) | kpa.gov.kw | infrastructure | official | vessel_loading,port_closure,exports | proposed |
| ca-KW-national_exchange | KW | — | national_exchange | Boursa Kuwait | boursakuwait.com.kw | exchange | official | pricing_formula | unverified |
| ca-KW-central_bank | KW | — | central_bank | Central Bank of Kuwait | cbk.gov.kw | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-KW-environment_regulator | KW | — | environment_regulator | Environment Public Authority (EPA) | epa.org.kw | government_regulator | official | refinery_outage,production | proposed |
| ca-KW-coast_guard_navy | KW | — | coast_guard_navy | Ministry of Defence (Kuwait Navy) | mod.gov.kw | government_regulator | official | port_closure,vessel_loading | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-KW-ministry_petroleum | OPEC+ quota compliance | Gulf diplomacy, Iraq border | Export policy via KPC | **proposed** |
| ca-KW-noc | KPC group production, refining, marketing | — | Mina Al Ahmadi, Mina Abdullah exports | **proposed** |
| ca-KW-mfa | — | GCC / Iraq / Iran relations | Strait access diplomacy | **proposed** |
| ca-KW-customs_export | — | Trade enforcement | Port / border clearance | **proposed** |
| ca-KW-upstream_regulator | Burgan / north field output | PSC stability | KOC-operated loading feed | **proposed** |
| ca-KW-port_maritime_authority | — | — | Mina Al Ahmadi, Shuaiba, Doha Link | **proposed** |
| ca-KW-national_exchange | — | — | Equities only | **unverified** — Tier 2 |
| ca-KW-central_bank | — | FX / sovereign wealth linkage | Oil revenue routing | **proposed** |
| ca-KW-environment_regulator | Compliance orders | — | Refinery / industrial permits | **proposed** |
| ca-KW-coast_guard_navy | — | Gulf security | Port / offshore protection | **proposed** |

---

### Unverified / Anti-patterns

| id | issue |
|----|-------|
| ca-KW-national_exchange | Boursa Kuwait — no crude/LNG futures |

**Desk note:** Tier 1 = **kpc.com.kw + moo.gov.kw + kpa.gov.kw + kockw.com**. KPC subsidiary KOTC (`kotc.com.kw`) for tanker fleet — playbook extension.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 8,
  "last_country": "KW",
  "crosscheck_cursor": 0,
  "last_batch_seq": 9
}
```

**Další dávka:** `composer-2-5_010_country_authority_QA.md` (Qatar × 10 autorit).

### Whitelist kandidáti (Tier 1, po schválení)

`moo.gov.kw`, `kpc.com.kw`, `mofa.gov.kw`, `customs.gov.kw`, `kockw.com`, `kpa.gov.kw`, `cbk.gov.kw`, `epa.org.kw`, `mod.gov.kw`
