# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_060_country_authority_GA.md  
**Fáze:** country_authority — krok GA (Gabon)  
**Datum:** 2026-07-06  

---

## Shrnutí

Gabon = **declining producer** (~200 kb/d crude; klesající z peak ~370 kb/d 2012).
**Gabon Oil Company (GOC)** = státní NOC (ex-Société Equatoriale des Mines et des Pétroles).
**TotalEnergies + Perenco** = dominantní IOC operators. Libreville port = primary export.
Gabon opustilo OPEC v 2023 (vojenský převrat, Brice Clotaire Oligui). Klíčové signály:
**TotalEnergies/Perenco Gabon quarterly**, **GOC OSP**, **Libreville port cargo**.
8 proposed, 1 empty, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-GA-ministry_petroleum | GA | — | ministry_petroleum | Ministry of Petroleum and Hydrocarbons | — | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-GA-noc | GA | — | noc | GOC – Gabon Oil Company | gabonoil.ga | international_agency | official | production, exports, term_contract, pricing_formula | proposed |
| ca-GA-mfa | GA | — | mfa | Ministry of Foreign Affairs | — | international_agency | official | sanctions, policy | proposed |
| ca-GA-customs_export | GA | — | customs_export | Direction Générale des Douanes | douanes.gouv.ga | international_agency | official | exports, export_license | proposed |
| ca-GA-upstream_regulator | GA | — | upstream_regulator | Ministry of Petroleum (upstream, dual) | — | international_agency | official | production, force_majeure | proposed |
| ca-GA-port_maritime_authority | GA | — | port_maritime_authority | Port d'Owendo / OPRAG | portlibreville.com | international_agency | official | vessel_loading, port_closure | proposed |
| ca-GA-national_exchange | GA | — | national_exchange | — (no stock exchange) | — | — | — | — | empty |
| ca-GA-central_bank | GA | — | central_bank | BEAC – Banque des États de l'Afrique Centrale | beac.int | international_agency | official | pricing_formula | proposed |
| ca-GA-environment_regulator | GA | — | environment_regulator | Ministry of Environment | — | international_agency | official | refinery_outage | proposed |
| ca-GA-coast_guard_navy | GA | — | coast_guard_navy | Gabonese Navy | — | — | — | — | unverified |

---

## Cross-check

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-GA-noc (GOC) | GOC = state equity in Gabon blocks; TotalEnergies + Perenco = operators; Rabi, Torpido, Gamba fields (onshore/shallow); Dussafu offshore (BW Energy); GOC OSP = Gabon blend benchmark | Military coup August 2023 (Oligui overthrows Bongo); OPEC exit 2023; TotalEnergies continued operations; each coup/political change = production continuity uncertainty | Libreville/Owendo port crude terminal; Gulf of Guinea VLCC loading; Cap Lopez terminal (TotalEnergies) | **proposed** |
| ca-GA-ministry_petroleum | Post-coup MoPH = transitional government; Oligui pro-Western signals; OPEC exit = production quota freedom signal | Gabon = French historical sphere; TotalEnergies dominant; every political stability update = TotalEnergies Gabon ops signal | Offshore Gabon = Dussafu, Diaba, Tchibala blocks | **proposed** |

### Expansion
- TotalEnergies Gabon → totalenergies.com/gabon (major operator)
- Perenco Gabon → perenco.com (Rabi field; significant onshore operator)
- BW Energy (Dussafu) → bw-energy.com (Oslo Børs listed; Gabon offshore)

---
```json
{ "phase": "country_authority", "phase_index": 46, "last_country": "GA", "last_batch_seq": 60 }
```
