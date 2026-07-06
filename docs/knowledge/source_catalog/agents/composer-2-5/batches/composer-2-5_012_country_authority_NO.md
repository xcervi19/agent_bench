# Catalog batch

**Agent:** composer-2-5 (Composer 2.5)  
**Soubor:** composer-2-5_012_country_authority_NO.md  
**Fáze:** country_authority — krok NO (Fáze 2, země 10/64)  
**Datum:** 2026-07-05  

---

## Shrnutí

Norway × 10 autorit. **10 proposed** (vysoce ověřitelné oficiální domény).

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-NO-ministry_petroleum | NO | — | ministry_petroleum | Ministry of Petroleum and Energy | regjeringen.no | government_regulator | official | production,exports,quota_rhetoric | proposed |
| ca-NO-noc | NO | — | noc | Equinor | equinor.com | noc | official | production,exports,force_majeure,term_contract | proposed |
| ca-NO-mfa | NO | — | mfa | Ministry of Foreign Affairs | regjeringen.no | diplomacy | official | sanctions,export_license | proposed |
| ca-NO-customs_export | NO | — | customs_export | Norwegian Customs (Tolletaten) | toll.no | government_regulator | official | exports,export_license,imports | proposed |
| ca-NO-upstream_regulator | NO | — | upstream_regulator | Norwegian Petroleum Directorate (NPD) | npd.no | government_regulator | official | production,term_contract | proposed |
| ca-NO-port_maritime_authority | NO | — | port_maritime_authority | Norwegian Coastal Administration | kystverket.no | infrastructure | official | vessel_loading,port_closure,exports | proposed |
| ca-NO-national_exchange | NO | — | national_exchange | Euronext Oslo (Oslo Børs) | oslobors.no | exchange | official | pricing_formula | proposed |
| ca-NO-central_bank | NO | — | central_bank | Norges Bank | norges-bank.no | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-NO-environment_regulator | NO | — | environment_regulator | Environment Agency | miljodirektoratet.no | government_regulator | official | refinery_outage,production | proposed |
| ca-NO-coast_guard_navy | NO | — | coast_guard_navy | Royal Norwegian Navy | forsvaret.no | government_regulator | official | port_closure,vessel_loading | proposed |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-NO-upstream_regulator | NPD field/production data | Licensing rounds, tax policy | Johan Sverdrup, Troll, Ormen Lange output | **proposed** |
| ca-NO-noc | Equinor ops updates, maintenance | EU gas supply diplomacy | Mongstad, Kårstø, Hammerfest LNG | **proposed** |
| ca-NO-port_maritime_authority | — | — | Sture, Kårstø, Hammerfest terminal access | **proposed** |

**Desk Tier 1:** npd.no + equinor.com + npd.no production data. NPD monthly stats move European gas balances early.

**Note:** ministry + MFA share `regjeringen.no` — distinct slots, shared portal.

### Progress po merge (návrh)

`last_country: NO`, `last_batch_seq: 12`. **Další:** BR.
