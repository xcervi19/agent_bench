# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_051_country_authority_UA.md  
**Fáze:** country_authority — krok UA (Ukraine)  
**Datum:** 2026-07-06  

---

## Shrnutí

Ukraine = **klíčový tranzitní stát pro ruský plyn** (Ukrainian Gas Transmission System –
GTS = historicky největší underground gas storage v Evropě; ~31 bcm). Post-2022:
GTS ukrainský provoz pokračuje (!), Gazprom-Naftogaz tranzitní smlouva expirovala
31.12.2024. Klíčové signály: **OGTSU (Gas TSO of Ukraine) daily flow data**,
**Naftogaz produkce** (~12 bcm domestic = energy security), **UGS storage fill**
(=evropský barometr). War context = nejvyšší geopolitický risk faktor. 6 proposed, 1 empty, 3 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-UA-ministry_petroleum | UA | — | ministry_petroleum | Ministry of Energy | mev.gov.ua | international_agency | official | policy, import_licensing, quota_rhetoric | proposed |
| ca-UA-noc | UA | — | noc | Naftogaz of Ukraine | naftogaz.com | international_agency | official | production, imports, force_majeure, term_contract | proposed |
| ca-UA-mfa | UA | — | mfa | Ministry of Foreign Affairs | mfa.gov.ua | international_agency | official | sanctions, policy | proposed |
| ca-UA-customs_export | UA | — | customs_export | State Customs Service | customs.gov.ua | international_agency | official | imports, exports | unverified |
| ca-UA-upstream_regulator | UA | — | upstream_regulator | State Service of Geology and Mineral Resources | geology.gov.ua | international_agency | official | production | unverified |
| ca-UA-port_maritime_authority | UA | — | port_maritime_authority | AMPU – Administration of Seaports of Ukraine | uspa.gov.ua | international_agency | official | vessel_loading, port_closure | unverified |
| ca-UA-national_exchange | UA | — | national_exchange | — (commodity exchange minimal relevance) | — | — | — | — | empty |
| ca-UA-central_bank | UA | — | central_bank | National Bank of Ukraine | bank.gov.ua | international_agency | official | sanctions | proposed |
| ca-UA-environment_regulator | UA | — | environment_regulator | Ministry of Environmental Protection and Natural Resources | mepr.gov.ua | international_agency | official | pipeline_outage | proposed |
| ca-UA-gas_tso | UA | — | upstream_regulator | OGTSU – Gas Transmission System Operator of Ukraine | tsoua.com | international_agency | official | pipeline_outage, production | proposed |

---

## ⚠️ Analytická poznámka: Válečný kontext

- OGTSU pokračuje v provozu GTS i během války (částečně NATO logistika)
- Tranzitní smlouva Gazprom–Naftogaz expirovala 31.12.2024 → ruský plyn přes Ukrainu STOP (výjimka: TürkAkım)
- UGS storage fill (OGTSU publikuje denně) = tier-1 signal pro EU zimní zásoby
- Odessa/Pivdenný port = ruské rakety target; každý útok = supply interruption signal
- Hlavní monitoring zdroje: OGTSU (tsoua.com), Naftogaz (naftogaz.com), ENTSO-G

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-UA-gas_tso (OGTSU) | **TIER-1**: OGTSU denní UGS storage fill report = primární EU zimní gas supply signal; 31 bcm UGS capacity = EU's largest underground storage; tranzit přes Ukrainu ukončen 1.1.2025 | Každý ruský úder na GTS infrastructure = European gas supply emergency signal; Balchug/Urengoy-Pomary-Uzhhorod-Baumgarten corridor | Uzhhorod-Baumgarten gas route (Slovakian continuation via Eustream); Ukrainian GTS = physical hedge for EU | **proposed** — tsoua.com aktivní |
| ca-UA-noc (Naftogaz) | Naftogaz = state holding; domestická produkce ~12 bcm/y gas + ~60 kb/d crude (declining); Ukrnafta (Naftogaz subsidiary, crude); Naftogaz = Ukrainian energy sovereignty key | Naftogaz-Gazprom arbitration (Stockholm 2017-2018 = $2.56B award); Naftogaz war bonds; každý Naftogaz production report = Ukrainian energy resilience signal | Kremenchuk refinery (Naftogaz crude; war damage 2022); Odessa LNG terminal (proposed pre-war) | **proposed** — naftogaz.com aktivní |
| ca-UA-port_maritime_authority (AMPU) | AMPU Odessa/Pivdenný/Chornomorsk port complex = Black Sea grain + product export hub; Russia-Ukraine Black Sea grain deal (2022-2023) precedent; Odessa under drone attack | Black Sea corridor = strategic; Ukraine Humanitarian Corridor (BSGI); UN-brokered grain deal (terminated 2023) | Pivdenný (South) port = largest Ukrainian port; crude import capability; Odessa refinery (mothballed) | **unverified** — uspa.gov.ua ověřit; wartime access issues |

### Expansion sloty
- ENTSO-G Ukraine transparency → transparency.entsog.eu (European gas flow including Ukraine entry/exit)
- Ukrtransnafta (crude pipeline operator) → ukrtransnafta.com (Druzhba Ukrainian section)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 37, "last_country": "UA", "last_batch_seq": 51 }
```
