# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_036_country_authority_IT.md  
**Fáze:** country_authority — krok IT (Italy)  
**Datum:** 2026-07-06  

---

## Shrnutí

Italy = **klíčový Středomořský příjemce**: ENI (světová IOC, Italian state ~30%),
Ravenna offshore gas, TAP pipeline příjem (Azerbaijani gas → Puglia). Po 2022 Italy
agresivně diverzifikovala od ruského plynu (Mattei Plan pro Afriku: Algérie, Libye,
Kongo, Mosambik). Piombino FSRU (2023). Klíčové signály: **ENI quarterly**,
**GSE (Gestore Servizi Energetici)** statistiky, **SNAM gas grid**,
**TAP daily flow** (Azerbaijani gas přes Turecko). 9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-IT-ministry_petroleum | IT | — | ministry_petroleum | MASE – Ministry of Environment and Energy Security | mase.gov.it | international_agency | official | policy, import_licensing, quota_rhetoric | proposed |
| ca-IT-noc | IT | — | noc | ENI S.p.A. | eni.com | international_agency | official | production, exports, force_majeure, term_contract, pricing_formula | proposed |
| ca-IT-mfa | IT | — | mfa | Farnesina – Ministry of Foreign Affairs | esteri.it | international_agency | official | sanctions, policy | proposed |
| ca-IT-customs_export | IT | — | customs_export | ADM – Agenzia delle Dogane e dei Monopoli | adm.gov.it | international_agency | official | imports, exports | proposed |
| ca-IT-upstream_regulator | IT | — | upstream_regulator | MASE (upstream licensing, dual) | mase.gov.it | international_agency | official | production, refinery_outage | proposed |
| ca-IT-port_maritime_authority | IT | — | port_maritime_authority | MIT – Ministry of Infrastructure and Transport | mit.gov.it | international_agency | official | vessel_loading, port_closure | proposed |
| ca-IT-national_exchange | IT | — | national_exchange | Borsa Italiana / Euronext Milan | borsaitaliana.it | exchange | official | pricing_formula, term_contract | proposed |
| ca-IT-central_bank | IT | — | central_bank | Banca d'Italia | bancaditalia.it | international_agency | official | pricing_formula | proposed |
| ca-IT-environment_regulator | IT | — | environment_regulator | ISPRA – Institute for Environmental Protection and Research | isprambiente.gov.it | international_agency | official | refinery_outage | proposed |
| ca-IT-coast_guard_navy | IT | — | coast_guard_navy | Marina Militare (Italian Navy) | marina.difesa.it | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-IT-noc (ENI) | ENI = Italian IOC (state 32.4% via CDP+MEF); upstream 1.6 mboed (Congo, Libya, Angola, Algeria, Nigeria, Kazakhstan, UK North Sea, Norway); ENI quarterly = tier-1 African supply signal; každý ENI Libya force majeure = Mediterranean crude disruption | ENI = klíčový pro Mattei Plan (Italy → Afrika diversifikace); ENI-Gazprom gas supply replacement contracts; ENI Congo LNG (Tango FLNG) | Ravenna offshore gas; Brindisi, Augusta, Trieste crude import ports; TAP pipeline příjem Melendugno (Puglia) | **proposed** — eni.com aktivní; tier-1 |
| ca-IT-ministry_petroleum (MASE) | MASE = nové ministerstvo post-2022 (přejmenovalo Ministry of Ecological Transition); ENI Piombino FSRU approval; LNG diversification policy Mattei Plan | Italy = EU energy hub aspirant; Galsi pipeline project (Algeria–Sardinia–Italy); Trans-Adriatic Pipeline governance | SNAM = gas grid operator (GRI/TAP interconnect); FSRU Golar Tundra Piombino | **proposed** |
| ca-IT-coast_guard_navy | Marina Militare patrols Strait of Sicily (migration + tanker routes); ENI Libya field security liaison | Strait of Sicily = chokepoint for Libyan crude → Italy (Augusta refinery); Libya civil war impact on ENI operations | ENI offshore platform Libya (Bahr Essalam gas; Wafa gas); Malta Channel crude movements | **unverified** — marina.difesa.it aktivní; ověřit HTTPS certifikát + content quality |

### Expansion sloty
- SNAM → snam.it (gas transmission; TAP Italian section; FSRU operator)
- Terna → terna.it (electricity grid; LNG demand proxy)
- Saras (Sarroch refinery, Sardinia, ~300 kb/d) → saras.it

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 35, "last_country": "IT", "last_batch_seq": 36 }
```
