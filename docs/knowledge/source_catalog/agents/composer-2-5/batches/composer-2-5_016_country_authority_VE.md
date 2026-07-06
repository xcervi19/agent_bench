# Catalog batch

**Agent:** composer-2-5 (Composer 2.5)  
**Soubor:** composer-2-5_016_country_authority_VE.md  
**Fáze:** country_authority — krok VE (Fáze 2, země 14/64)  
**Datum:** 2026-07-05  

---

## Shrnutí

Venezuela × 10 autorit. **6 proposed**, **4 unverified** (sanctions-era domain reliability).

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-VE-ministry_petroleum | VE | — | ministry_petroleum | Ministry of Petroleum | minpetrolio.gob.ve | government_regulator | official | production,exports,quota_rhetoric | unverified |
| ca-VE-noc | VE | — | noc | PDVSA | pdvsa.com | noc | official | production,exports,force_majeure,term_contract | proposed |
| ca-VE-mfa | VE | — | mfa | Ministry of Foreign Affairs | mppef.gob.ve | diplomacy | official | sanctions,export_license | unverified |
| ca-VE-customs_export | VE | — | customs_export | SENIAT | seniat.gob.ve | government_regulator | official | exports,export_license,imports | proposed |
| ca-VE-upstream_regulator | VE | — | upstream_regulator | PDVSA — Upstream | pdvsa.com | government_regulator | official | production,term_contract | proposed |
| ca-VE-port_maritime_authority | VE | — | port_maritime_authority | Bolipuertos | bolipuertos.gob.ve | infrastructure | official | vessel_loading,port_closure,exports | unverified |
| ca-VE-national_exchange | VE | — | national_exchange | Caracas Stock Exchange (BCV) | bcv.org.ve | exchange | official | pricing_formula | unverified |
| ca-VE-central_bank | VE | — | central_bank | Banco Central de Venezuela | bcv.org.ve | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-VE-environment_regulator | VE | — | environment_regulator | Ministry of Ecosocialism | minec.gob.ve | government_regulator | official | refinery_outage,production | unverified |
| ca-VE-coast_guard_navy | VE | — | coast_guard_navy | Bolivarian Navy (FANB) | milicia.mil.ve | government_regulator | official | port_closure,vessel_loading | unverified |

**Desk Tier 1:** pdvsa.com (primary anchor). Sanctions overlay: OFAC (`treasury.gov`). Many .gob.ve sites unstable — manual validation required (#29).

**Progress:** `last_country: VE`, `last_batch_seq: 16`. **Další:** NG.
