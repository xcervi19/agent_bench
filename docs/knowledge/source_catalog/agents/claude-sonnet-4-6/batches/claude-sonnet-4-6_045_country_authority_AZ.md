# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_045_country_authority_AZ.md  
**Fáze:** country_authority — krok AZ (Azerbaijan)  
**Datum:** 2026-07-06  

---

## Shrnutí

Azerbaijan = **BTC pipeline** (Baku–Tbilisi–Ceyhan; ~1.2 mb/d Azerbaijani + Kazakh crude
→ Ceyhan Turkey) + **TANAP/TAP gas pipeline** (Azerbaijani Shah Deniz gas → Turkey → Greece
→ Italy; ~16 bcm/y, expandable to 32 bcm/y). SOCAR = state NOC.
Post-2022: Azerbaijan jako klíčová EU gas diversifikace od Ruska (Southern Gas Corridor).
ACG (Azeri-Chirag-Gunashli) = offshore mega-field (BP operated, SOCAR + IOC JV).
9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-AZ-ministry_petroleum | AZ | — | ministry_petroleum | Ministry of Energy | minenergy.gov.az | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-AZ-noc | AZ | — | noc | SOCAR – State Oil Company of Azerbaijan | socar.az | international_agency | official | production, exports, force_majeure, term_contract, pricing_formula | proposed |
| ca-AZ-mfa | AZ | — | mfa | Ministry of Foreign Affairs | mfa.gov.az | international_agency | official | sanctions, policy | proposed |
| ca-AZ-customs_export | AZ | — | customs_export | State Customs Committee | customs.gov.az | international_agency | official | exports, export_license | proposed |
| ca-AZ-upstream_regulator | AZ | — | upstream_regulator | SOCAR (upstream licensing, dual role) | socar.az | international_agency | official | production, refinery_outage | proposed |
| ca-AZ-port_maritime_authority | AZ | — | port_maritime_authority | Azerbaijan Caspian Shipping Company | acsc.az | international_agency | official | vessel_loading, port_closure | proposed |
| ca-AZ-national_exchange | AZ | — | national_exchange | BSE – Baku Stock Exchange | bfb.az | exchange | official | pricing_formula | proposed |
| ca-AZ-central_bank | AZ | — | central_bank | CBA – Central Bank of Azerbaijan | cbar.az | international_agency | official | pricing_formula, sanctions | proposed |
| ca-AZ-environment_regulator | AZ | — | environment_regulator | Ministry of Ecology and Natural Resources | eco.gov.az | international_agency | official | refinery_outage | proposed |
| ca-AZ-coast_guard_navy | AZ | — | coast_guard_navy | Azerbaijan State Border Service (Naval Forces) | dsx.gov.az | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-AZ-noc (SOCAR) | SOCAR = state NOC; ACG production (~700 kb/d; BP 30.37% operated; SOCAR 25%); Shah Deniz gas (~26 bcm/y; BP 28.8% operated); BTC crude OSP (Azeri Light = tier-1 Mediterranean blend); každý SOCAR OSP announcement = Ceyhan crude pricing signal | SOCAR = Aliyev family strategic asset; SOCAR Germany, SOCAR Georgia, SOCAR Turkey = international downstream | BTC terminal Ceyhan (~1.2 mb/d); Baku-Tbilisi-Erzurum (BTE) gas pipeline; TANAP Turkish section; TAP Greek-Albanian-Italian section | **proposed** — socar.az aktivní |
| ca-AZ-port_maritime_authority (ACSC) | Azerbaijan Caspian Shipping Company operates Caspian tanker fleet; Sangachal terminal (ACG + Shah Deniz export hub); Baku port Caspian crude loading | BTC + TANAP = Southern Gas Corridor = EU energy security pillar; každé Azerbaijan-Armenia conflict event = potential BTC disruption risk | Sangachal → BTC pump station 1 → Turkey → Ceyhan; Caspian ferry (Baku–Aktau for KZ crude swap) | **proposed** |
| ca-AZ-mfa | Azerbaijan non-aligned stance; Aliyev balances Russia-West-Turkey triangle; Nagorno-Karabakh (2023 resolution) = potential for pipeline stability | MFA Azerbaijan prohlášení o BTC security = tier-1 geo signal; každý Russia-Azerbaijan tension = TANAP/BTC disruption risk | TANAP Compressor Station outages (periodic); TAP Italy landing Melendugno | **proposed** |

### Expansion sloty
- BP ACG → bp.com/azerbaijan (operated; ACG JV = tier-1 Caspian crude)
- TANAP A.Ş. → tanap.com (Trans-Anatolian Pipeline Company; operational data)
- TAP AG → tap-ag.com (Trans-Adriatic Pipeline; Italian section flow data)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 44, "last_country": "AZ", "last_batch_seq": 45 }
```
