# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_029_country_authority_KR.md  
**Fáze:** country_authority — krok KR (South Korea)  
**Datum:** 2026-07-06  

---

## Shrnutí

South Korea = ~3 mb/d crude importer (100% import dependent); 3. největší LNG importér.
Klíčové signály: **KNOC import data**, **SK/GS/Hyundai rafinérie processing rates**
(4 velké privátní refinerské skupiny; Korea je net product exportér), **Korea customs crude
import data** (MoF KCS). Ulsan = světové největší rafinérie hub (~1.9 mb/d v jednom
průmyslovém pásmu). JCC-linked LNG smlouvy. Terminál pro re-export LNG (Boryeong).
9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-KR-ministry_petroleum | KR | — | ministry_petroleum | MOTIE – Ministry of Trade, Industry and Energy | motie.go.kr | international_agency | official | policy, import_licensing, quota_rhetoric | proposed |
| ca-KR-noc | KR | — | noc | KNOC – Korea National Oil Corporation | knoc.or.kr | international_agency | official | production, force_majeure, term_contract | proposed |
| ca-KR-mfa | KR | — | mfa | MOFA Korea | mofa.go.kr | international_agency | official | sanctions, policy | proposed |
| ca-KR-customs_export | KR | — | customs_export | KCS – Korea Customs Service | customs.go.kr | international_agency | official | imports, exports | proposed |
| ca-KR-upstream_regulator | KR | — | upstream_regulator | MOTIE (upstream licensing, dual) | motie.go.kr | international_agency | official | production, refinery_outage | proposed |
| ca-KR-port_maritime_authority | KR | — | port_maritime_authority | MOF – Ministry of Oceans and Fisheries | mof.go.kr | international_agency | official | vessel_loading, port_closure | proposed |
| ca-KR-national_exchange | KR | — | national_exchange | KRX – Korea Exchange | krx.co.kr | exchange | official | pricing_formula | proposed |
| ca-KR-central_bank | KR | — | central_bank | BOK – Bank of Korea | bok.or.kr | international_agency | official | pricing_formula, sanctions | proposed |
| ca-KR-environment_regulator | KR | — | environment_regulator | MOE Korea – Ministry of Environment | me.go.kr | international_agency | official | refinery_outage | proposed |
| ca-KR-coast_guard_navy | KR | — | coast_guard_navy | Republic of Korea Navy | navy.mil.kr | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-KR-customs_export (KCS) | KCS monthly crude import data (zveřejňuje MOTIE/KOSIS); Korea celkový import ~3 mb/d; source composition: Saudi ~25%, Kuwait ~16%, UAE ~13%, US ~12%, Russia ~7% (post-2022 declining); LNG sources: Qatar, Australia, US | Korea = přísný US sanctions follower (THAAD dependency); Iran crude waivers expired 2019; Russia import compliance monitoring | Ulsan VLCC terminals (SK Energy + GS Caltex + Hyundai Oilbank + S-OIL); Yeosu and Daesan secondary crude terminals | **proposed** — customs.go.kr aktivní |
| ca-KR-noc (KNOC) | KNOC = state upstream company (no refining); overseas assets: Kazakhstan (Kashagan), Canada (oil sands), Iraq (West Qurna-2 working interest) | KNOC podléhá MOTIE; each KNOC divestiture or new PSC acquisition = energy policy signal | KNOC data: Korean crude basket reference price | **proposed** — knoc.or.kr aktivní |
| ca-KR-port_maritime_authority | Ulsan Port = world's largest refinery complex (~1.9 mb/d); MOF oversees Ulsan, Pyeongtaek (LNG), Incheon; Korea = largest ship recycling exporter (Hyundai HI, DSME) | Strait of Korea relevance for Tsushima Strait (Japanese connection) | VLCC berthing depths at Ulsan; LNG terminal Incheon + Tongyeong + Boryeong | **proposed** |

### Expansion sloty
- S-OIL (Saudi Aramco 63.4% owned) → s-oil.com (Onsan refinery; Aramco Korean proxy)
- SK Energy → skinnovation.com (largest Korean refiner; ~1 mb/d Ulsan)
- KOGAS – Korea Gas Corporation → kogas.or.kr (LNG import monopoly; key Asian LNG demand)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 28, "last_country": "KR", "last_batch_seq": 29 }
```
