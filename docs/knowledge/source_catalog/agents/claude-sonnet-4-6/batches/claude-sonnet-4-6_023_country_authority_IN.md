# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_023_country_authority_IN.md  
**Fáze:** country_authority — krok IN (India)  
**Datum:** 2026-07-05  

---

## Shrnutí

India = 3. největší importér ropy (~5 mb/d); domestická produkce ~750 kb/d (klesající).
Klíčové signály: **PPAC import data** (Petroleum Planning and Analysis Cell — publikuje
monthly import volumes a source breakdown), **IOC/HPCL/BPCL processing rates**
(3 státní rafinérie = proxy pro spot demand), **Indian crude basket price** (PPAC weekly),
**Jamnagar** (Reliance; 1.24 mb/d; semi-private ale key flow signal). India nakupuje
ruský Urals za slevu → key sanctions compliance monitoring.
9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-IN-ministry_petroleum | IN | — | ministry_petroleum | Ministry of Petroleum and Natural Gas | petroleum.nic.in | international_agency | official | policy, import_licensing, quota_rhetoric | proposed |
| ca-IN-noc | IN | — | noc | ONGC – Oil and Natural Gas Corporation | ongcindia.com | international_agency | official | production, force_majeure, term_contract | proposed |
| ca-IN-mfa | IN | — | mfa | Ministry of External Affairs | mea.gov.in | international_agency | official | sanctions, policy | proposed |
| ca-IN-customs_export | IN | — | customs_export | CBIC – Central Board of Indirect Taxes and Customs | cbic.gov.in | international_agency | official | imports, exports | proposed |
| ca-IN-upstream_regulator | IN | — | upstream_regulator | DGH – Directorate General of Hydrocarbons | dghindia.gov.in | international_agency | official | production, refinery_outage | proposed |
| ca-IN-port_maritime_authority | IN | — | port_maritime_authority | DG Shipping – Directorate General of Shipping | dgshipping.gov.in | international_agency | official | vessel_loading, port_closure | proposed |
| ca-IN-national_exchange | IN | — | national_exchange | MCX – Multi Commodity Exchange India | mcxindia.com | exchange | official | pricing_formula | proposed |
| ca-IN-central_bank | IN | — | central_bank | RBI – Reserve Bank of India | rbi.org.in | international_agency | official | pricing_formula, sanctions | proposed |
| ca-IN-environment_regulator | IN | — | environment_regulator | MoEFCC – Ministry of Environment, Forest and Climate Change | moef.gov.in | international_agency | official | refinery_outage | proposed |
| ca-IN-coast_guard_navy | IN | — | coast_guard_navy | Indian Navy | indiannavy.nic.in | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-IN-customs_export (CBIC/PPAC) | PPAC (pod Ministry of Petroleum) = primární Indian import data; monthly crude import volumes a source; India >45% z Ruska (2023) = sanctions monitoring signal; sekundárně CBIC customs data | India nakupuje sanctioned crude (Írán waivers, Rusko po 2022) = G7 price cap compliance indicator | Paradip, Haldia, Mundra, JNPT jsou key import terminals; Reliance Jamnagar = privátní import | **proposed** — cbic.gov.in aktivní; PPAC sub-feed: ppac.gov.in |
| ca-IN-noc (ONGC) | ONGC = 60 % indické produkce; Mumbai High offshore (~160 kb/d declining); Videsh (ONGC Videsh) = zahraniční upstream (Rusko, Súdán, Brazílie) | ONGC je state-controlled; politicky pojený s Russian assets (Sakhalin-1, Vankorneft stakes) | Mumbai High FPSO/platform; Hazira gas terminal; KG Basin deep water | **proposed** — ongcindia.com aktivní |
| ca-IN-mfa (MEA) | MEA India = klíčový pro sanctions positioning: India odmítá přijmout G7 pressure na Russian crude; každé MEA prohlášení o energetické suverénitě je proxy pro Indian Urals imports | India-Russia energy pragmatism; India jako Írán waiver recipient 2018-2019; S-400 stíhačka spor s US → complex geopolitik | Hormuz risk premium calculation pro India = tier-1 (India 80 % crude prochází Hormuz) | **proposed** |

### Expansion sloty
- PPAC – Petroleum Planning and Analysis Cell → ppac.gov.in (weekly Indian crude basket price; tier-1 sub-feed)
- IOC – Indian Oil Corporation → iocl.com (largest state refiner; monthly throughput)
- HPCL → hindustanpetroleum.com; BPCL → bharatpetroleum.com
- Reliance Industries (Jamnagar) → ril.com (1.24 mb/d private mega-refinery)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 22, "last_country": "IN", "last_batch_seq": 23 }
```
