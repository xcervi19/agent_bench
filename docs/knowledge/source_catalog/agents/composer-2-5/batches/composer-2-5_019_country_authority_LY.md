# Catalog batch

**Agent:** composer-2-5 (Composer 2.5)  
**Soubor:** composer-2-5_019_country_authority_LY.md  
**Fáze:** country_authority — krok LY (Fáze 2, země 17/64)  
**Datum:** 2026-07-05  

---

## Shrnutí

Libya × 10 autorit. **3 proposed**, **5 unverified**, **2 empty** (fragmentovaný stát, dual NOC risk).

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-LY-ministry_petroleum | LY | — | ministry_petroleum | Ministry of Oil and Gas | mog.gov.ly | government_regulator | official | production,exports,quota_rhetoric | unverified |
| ca-LY-noc | LY | — | noc | NOC (National Oil Corporation) | nocl.org.ly | noc | official | production,exports,force_majeure,term_contract | proposed |
| ca-LY-mfa | LY | — | mfa | Ministry of Foreign Affairs | mfa.gov.ly | diplomacy | official | sanctions,export_license | unverified |
| ca-LY-customs_export | LY | — | customs_export | Libyan Customs Authority | customs.gov.ly | government_regulator | official | exports,export_license,imports | unverified |
| ca-LY-upstream_regulator | LY | — | upstream_regulator | NOC — Upstream Operations | nocl.org.ly | government_regulator | official | production,term_contract | proposed |
| ca-LY-port_maritime_authority | LY | — | port_maritime_authority | Libyan Ports Authority | ports.gov.ly | infrastructure | official | vessel_loading,port_closure,exports | unverified |
| ca-LY-national_exchange | LY | — | national_exchange | (none) | — | exchange | — | — | empty |
| ca-LY-central_bank | LY | — | central_bank | Central Bank of Libya | cbl.gov.ly | government_regulator | official | sanctions,pricing_formula | unverified |
| ca-LY-environment_regulator | LY | — | environment_regulator | (unclear authority) | — | government_regulator | — | refinery_outage | empty |
| ca-LY-coast_guard_navy | LY | — | coast_guard_navy | Libyan Navy | navy.gov.ly | government_regulator | official | port_closure,vessel_loading | unverified |

**Dual governance warning:** eastern Libya parallel structures — playbook must split Tripoli vs Benghazi sources; do not whitelist without manual check.

**Desk Tier 1 (best-effort):** nocl.org.ly. Es Sider / Ras Lanuf force majeure — monitor NOC statements + port agents; high unverified rate expected.

**Progress:** `last_country: LY`, `last_batch_seq: 19`. **Další:** DZ.
