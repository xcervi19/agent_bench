# Catalog batch

**Agent:** composer-2-5 (Composer 2.5)  
**Soubor:** composer-2-5_011_country_authority_OM.md  
**Fáze:** country_authority — krok OM (Fáze 2, země 9/64)  
**Datum:** 2026-07-05  

---

## Shrnutí

Oman × 10 autorit. **9 proposed**, **1 unverified** (national_exchange).

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-OM-ministry_petroleum | OM | — | ministry_petroleum | Ministry of Energy and Minerals | mem.gov.om | government_regulator | official | production,exports,quota_rhetoric | proposed |
| ca-OM-noc | OM | — | noc | OQ (Oman National Oil Company) | oq.com | noc | official | production,exports,force_majeure,term_contract | proposed |
| ca-OM-mfa | OM | — | mfa | Ministry of Foreign Affairs | mofa.gov.om | diplomacy | official | sanctions,export_license | proposed |
| ca-OM-customs_export | OM | — | customs_export | Royal Oman Police — Customs | rop.gov.om | government_regulator | official | exports,export_license,imports | proposed |
| ca-OM-upstream_regulator | OM | — | upstream_regulator | Petroleum Development Oman (PDO) | pdo.co.om | government_regulator | official | production,term_contract | proposed |
| ca-OM-port_maritime_authority | OM | — | port_maritime_authority | ASYAD (Ports & Logistics) | asyad.om | infrastructure | official | vessel_loading,port_closure,exports | proposed |
| ca-OM-national_exchange | OM | — | national_exchange | Muscat Stock Exchange (MSX) | msx.om | exchange | official | pricing_formula | unverified |
| ca-OM-central_bank | OM | — | central_bank | Central Bank of Oman | cbo.gov.om | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-OM-environment_regulator | OM | — | environment_regulator | Environment Authority | ea.gov.om | government_regulator | official | refinery_outage,production | proposed |
| ca-OM-coast_guard_navy | OM | — | coast_guard_navy | Ministry of Defence (Royal Navy of Oman) | mod.gov.om | government_regulator | official | port_closure,vessel_loading | proposed |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-OM-noc | OQ marketing, refinery runs | Oman neutrality / Iran proximity | Mina Al Fahal, Duqm exports | **proposed** |
| ca-OM-upstream_regulator | PDO field output | Block contract stability | MOL loading, Duqm refinery feed | **proposed** |
| ca-OM-port_maritime_authority | — | — | Salalah, Sohar, Duqm port ops | **proposed** |

**Desk Tier 1:** oq.com + pdo.co.om + asyad.om. Duqm hub — playbook extension.

### Progress po merge (návrh)

`last_country: OM`, `last_batch_seq: 11`. **Další:** NO.
