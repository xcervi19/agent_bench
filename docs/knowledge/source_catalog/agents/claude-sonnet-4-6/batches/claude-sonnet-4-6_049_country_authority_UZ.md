# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_049_country_authority_UZ.md  
**Fáze:** country_authority — krok UZ (Uzbekistan)  
**Datum:** 2026-07-06  

---

## Shrnutí

Uzbekistan = **střední energetický producent** (~100 kb/d crude + ~57 bcm/y gas; klesající).
Klíčové: **Uzbekneftegaz** (state NOC), **Central Asia-China gas pipeline** (CAGP přes UZ
do Číny; UZ je transit stát i producer), **Kandym gas complex** (Lukoil operated).
Post-2022: Uzbekistan zvyšuje vztahy se Západem; Mirziyoyev reforma éra = více IOC přítomnosti
(TotalEnergies, Shell, Lukoil). 7 proposed, 1 empty, 2 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-UZ-ministry_petroleum | UZ | — | ministry_petroleum | Ministry of Energy | minenergy.uz | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-UZ-noc | UZ | — | noc | Uzbekneftegaz JSC | ung.uz | international_agency | official | production, exports, term_contract | proposed |
| ca-UZ-mfa | UZ | — | mfa | Ministry of Foreign Affairs | mfa.uz | international_agency | official | sanctions, policy | proposed |
| ca-UZ-customs_export | UZ | — | customs_export | State Customs Committee | customs.uz | international_agency | official | exports | proposed |
| ca-UZ-upstream_regulator | UZ | — | upstream_regulator | Uzbekneftegaz (upstream licensing, dual) | ung.uz | international_agency | official | production, refinery_outage | proposed |
| ca-UZ-port_maritime_authority | UZ | — | port_maritime_authority | — (landlocked; no port authority) | — | — | — | — | empty |
| ca-UZ-national_exchange | UZ | — | national_exchange | RSE – Republican Stock Exchange Toshkent | uzse.uz | exchange | official | pricing_formula | unverified |
| ca-UZ-central_bank | UZ | — | central_bank | Central Bank of Uzbekistan | cbu.uz | international_agency | official | pricing_formula, sanctions | proposed |
| ca-UZ-environment_regulator | UZ | — | environment_regulator | State Committee for Ecology and Environmental Protection | ecologiya.uz | international_agency | official | refinery_outage | proposed |
| ca-UZ-coast_guard_navy | UZ | — | coast_guard_navy | — (landlocked; no naval forces) | — | — | — | — | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-UZ-noc (Uzbekneftegaz) | Uzbekneftegaz = upstream + midstream; Kandym gas complex (Lukoil operated, ~$4B investment; 8 bcm/y); Shurtan, Mubarek gas fields; declining production trend; reforming governance post-Mirziyoyev | Uzbekneftegaz IPO discussions; Mirziyoyev reform = TotalEnergies, Shell upstream entry; každý Uzbekneftegaz production report = CAC pipeline supply signal | CAGP Line D (Uzbekistan section); Shymkent pipeline (UZ→KZ→Russia/China junction) | **proposed** — ung.uz aktivní |
| ca-UZ-mfa | Uzbekistan non-aligned; G5 Central Asia format; Mirziyoyev pro-reform Western engagement; každá UZ diplomatic statement o energy cooperation = new IOC entry signal | UZ Russia sanctions = complex (Russia is neighbour, key trading partner); UZ-EU Enhanced Partnership Agreement negotiations | Fergana Valley refinery (AGMK; Shurtan gas chemical complex) | **proposed** |
| ca-UZ-upstream_regulator | Dual domain s NOC; Uzbekneftegaz = licensor + operator; Lukoil Uzbekistan (Kandym, Gissar) = key IOC; TotalEnergies Aral blocks | Uzbekistan reform: unbundling Uzbekneftegaz (gas TSO → Uztransgaz separated) | Shurtan gas processing; Mubarek gas plant; Fergana refinery | **proposed** |

### Expansion sloty
- Lukoil Uzbekistan → lukoil.uz (Kandym operated; major IOC signal)
- Uztransgaz (gas TSO, separated from UNG) → uztransgaz.uz
- CAGP Line D (UZ section) → no dedicated domain; monitor via CNPC/UNG reports

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 27, "last_country": "UZ", "last_batch_seq": 49 }
```
