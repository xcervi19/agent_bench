# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_026_country_authority_AU.md  
**Fáze:** country_authority — krok AU (Australia)  
**Datum:** 2026-07-05  

---

## Shrnutí

Australia = klíčový LNG exportér (#2 světově za USA v 2024 s ~80 mtpa): North West Shelf,
Pluto, Gorgon, Ichthys, Darwin LNG, APLNG, Gladstone. Crude produkce ~350 kb/d. Žádný
státní NOC — private sector (Woodside, Santos, Beach Energy). Klíčové signály:
**NOPTA upstream data**, **NOPSEMA incident reports** (offshore safety), **Woodside/Santos
quarterly** (disclosure quality). Cyklonová sezóna (leden–april) = force majeure risk
pro NW Shelf. 9 proposed, 1 empty (noc).

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-AU-ministry_petroleum | AU | — | ministry_petroleum | DISR – Dept. of Industry, Science and Resources | industry.gov.au | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-AU-noc | AU | — | noc | — (no Australian state NOC) | — | — | — | — | empty |
| ca-AU-mfa | AU | — | mfa | DFAT – Dept. of Foreign Affairs and Trade | dfat.gov.au | international_agency | official | sanctions, policy | proposed |
| ca-AU-customs_export | AU | — | customs_export | ABF – Australian Border Force | abf.gov.au | international_agency | official | exports, export_license | proposed |
| ca-AU-upstream_regulator | AU | — | upstream_regulator | NOPTA – National Offshore Petroleum Titles Administrator | nopta.gov.au | international_agency | official | production, force_majeure | proposed |
| ca-AU-port_maritime_authority | AU | — | port_maritime_authority | AMSA – Australian Maritime Safety Authority | amsa.gov.au | international_agency | official | vessel_loading, port_closure | proposed |
| ca-AU-national_exchange | AU | — | national_exchange | ASX – Australian Securities Exchange | asx.com.au | exchange | official | pricing_formula, term_contract | proposed |
| ca-AU-central_bank | AU | — | central_bank | RBA – Reserve Bank of Australia | rba.gov.au | international_agency | official | pricing_formula | proposed |
| ca-AU-environment_regulator | AU | — | environment_regulator | NOPSEMA – National Offshore Petroleum Safety & Environmental Management Authority | nopsema.gov.au | international_agency | official | refinery_outage, force_majeure | proposed |
| ca-AU-coast_guard_navy | AU | — | coast_guard_navy | Royal Australian Navy | navy.gov.au | international_agency | official | port_closure, force_majeure | proposed |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-AU-upstream_regulator (NOPTA) | NOPTA spravuje titulky pro ~300 offshore petroleum titles; produkční data přes OPGGS reports; NW Shelf well completion data = Woodside production leading indicator | NOPTA pod DISR; environmental tie-in s NOPSEMA = dual regulatory gate pro new projects | Offshore NW Shelf platforms: North Rankin A, Goodwyn A; Darwin LNG offshore field Bayu-Undan; Gorgon offshore | **proposed** — nopta.gov.au aktivní |
| ca-AU-environment_regulator (NOPSEMA) | NOPSEMA vydává incident reports; offshore platform accidents = force majeure signal (Montara blowout 2009 precedent); drilling permit approvals = capex leading indicator | NOPSEMA neregistruje geopolitické signály; environmental objections k new drilling (Scarborough EIS) | Offshore NW Shelf safety orders; Darwin FPSO inspection | **proposed** — nopsema.gov.au aktivní |
| ca-AU-noc | Žádný australský státní NOC; privátní sektor: Woodside (~10 mtpa LNG), Santos, ConocoPhillips (APLNG), TotalEnergies (Ichthys) | Commonwealth nemá ownership; federal policy přes DISR + NOPTA + NOPSEMA | Private operators provozují terminály (Karratha Gas Plant, Pluto LNG, Darwin LNG, Gladstone QCLNG/APLNG/GLNG) | **empty** |

### Expansion sloty
- Woodside Energy → woodside.com (North West Shelf, Pluto, Scarborough)
- Santos → santos.com (Darwin LNG, Gladstone LNG)
- APLNG (ConocoPhillips + Origin) → aplng.com.au
- NWS Venture (Woodside/BP/Chevron/Shell/BHP/MIMI) → woodside.com/nws

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 25, "last_country": "AU", "last_batch_seq": 26 }
```
