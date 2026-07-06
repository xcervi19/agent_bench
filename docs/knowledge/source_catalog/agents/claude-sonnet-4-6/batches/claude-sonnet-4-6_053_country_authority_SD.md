# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_053_country_authority_SD.md  
**Fáze:** country_authority — krok SD (Sudan)  
**Datum:** 2026-07-06  

---

## Shrnutí

Sudan = **post-partition upstream challenge**: po secesi Jižního Súdánu (2011) ztratil
~75 % produkce. Zbývá ~70 kb/d (Blocks 1/2/4 s CNPC, Petronas). Klíčové: **Port Sudan**
= Red Sea crude export terminal (GNPOC / Sudanese pipeline); **Bashir-era Chinese IOC
presence** (CNPC, ONGC). Post-2023: nová občanská válka (SAF vs. RSF) = prakticky nulová
reliable data. 5 proposed, 2 empty, 3 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-SD-ministry_petroleum | SD | — | ministry_petroleum | Ministry of Petroleum and Gas | mpe.gov.sd | international_agency | official | policy, export_license | unverified |
| ca-SD-noc | SD | — | noc | Sudapet – Sudan Petroleum Company | sudapet.sd | international_agency | official | production, exports | unverified |
| ca-SD-mfa | SD | — | mfa | Ministry of Foreign Affairs (SAF, Port Sudan) | mfasudani.gov.sd | international_agency | official | sanctions, policy | proposed |
| ca-SD-customs_export | SD | — | customs_export | Sudan Customs Authority | customs.gov.sd | international_agency | official | exports | unverified |
| ca-SD-upstream_regulator | SD | — | upstream_regulator | Ministry of Petroleum (upstream, dual) | mpe.gov.sd | international_agency | official | production | proposed |
| ca-SD-port_maritime_authority | SD | — | port_maritime_authority | Port Sudan Port Corporation | portsudanport.sd | international_agency | official | vessel_loading, port_closure | proposed |
| ca-SD-national_exchange | SD | — | national_exchange | KSE – Khartoum Stock Exchange | kse.com.sd | exchange | official | pricing_formula | proposed |
| ca-SD-central_bank | SD | — | central_bank | Central Bank of Sudan | cbos.gov.sd | international_agency | official | sanctions | proposed |
| ca-SD-environment_regulator | SD | — | environment_regulator | — (non-functional wartime) | — | — | — | — | empty |
| ca-SD-coast_guard_navy | SD | — | coast_guard_navy | Sudan Navy (SAF) | — | — | — | — | empty |

---

## ⚠️ Analytická poznámka

Post-2023 civil war (SAF vs. RSF): Khartoum = RSF controlled; Port Sudan (Red Sea) = SAF base.
**Prakticky žádná reliable energetická data**. Monitoring přes: UN OCHA Sudan, tanker tracking (Port Sudan), CNPC/Petronas upstream reports.

## Cross-check

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-SD-port_maritime_authority | Port Sudan = jediný Red Sea crude export terminal; GNPOC pipeline (1,600 km z Heglig oilfields); Chinese IOC operations | SAF controls Port Sudan (government HQ); každý Port Sudan attack = export disruption signal | Red Sea proximity = Houthi attack range; Port Sudan drone attack Apr 2024 | **proposed** |
| ca-SD-mfa | SAF government (internationally recognised) vs. RSF (UAE-backed); každá mezinárodní uznávací/sankční zpráva = supply signal | US OFAC Sudan sanctions (pre-2017 lifted, re-applicable); China protects Sudan in UNSC | GNPOC pipeline integrity = primary supply signal | **proposed** |

### Expansion
- CNPC Sudan (GNPOC operator) → cnpc.com.cn/sudan
- ONGC Videsh Sudan → ongcvidesh.com

---
```json
{ "phase": "country_authority", "phase_index": 39, "last_country": "SD", "last_batch_seq": 53 }
```
