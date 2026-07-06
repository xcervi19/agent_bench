# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_044_country_authority_RU.md  
**Fáze:** country_authority — krok RU (Russia)  
**Datum:** 2026-07-06  

---

## Shrnutí

Russia = **nejvýznamnější geopolitický supply risk** v katalogu: ~10 mb/d crude + ~700 bcm/y
gas (pre-2022). Post-2022: Western sanctions, G7 price cap ($60/b), dark fleet tanker operations.
Klíčové signály: **Tanker tracker data** (Vortexa/Kpler) > official Rosstat (unreliable post-war);
**Novorossiysk CPC throughput** (Kazakh + Russian Black Sea), **Primorsk + Ust-Luga Baltic**
loadings, **Kozmino Pacific** export. Rosneft + Gazprom + LUKoil = primární NOC/IOC.
Většina zdrojů je unverified nebo nedůvěryhodná kvůli sankcím a informačním restrikcím.
7 proposed, 0 empty, 3 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-RU-ministry_petroleum | RU | — | ministry_petroleum | Ministry of Energy | minenergo.gov.ru | international_agency | official | policy, quota_rhetoric | unverified |
| ca-RU-noc | RU | — | noc | Rosneft | rosneft.ru | international_agency | official | production, exports, term_contract | unverified |
| ca-RU-mfa | RU | — | mfa | Ministry of Foreign Affairs | mid.ru | international_agency | official | sanctions, policy | proposed |
| ca-RU-customs_export | RU | — | customs_export | Federal Customs Service | customs.ru | international_agency | official | exports | unverified |
| ca-RU-upstream_regulator | RU | — | upstream_regulator | Rosnedra – Federal Agency for Mineral Resources | rosnedra.gov.ru | international_agency | official | production | proposed |
| ca-RU-port_maritime_authority | RU | — | port_maritime_authority | Rosmorrechflot – Federal Agency for Sea and Inland Water Transport | morflot.ru | international_agency | official | vessel_loading, port_closure | proposed |
| ca-RU-national_exchange | RU | — | national_exchange | SPIMEX – St. Petersburg International Mercantile Exchange | spimex.com | international_agency | official | pricing_formula | proposed |
| ca-RU-central_bank | RU | — | central_bank | Bank of Russia (CBR) | cbr.ru | international_agency | official | pricing_formula, sanctions | proposed |
| ca-RU-environment_regulator | RU | — | environment_regulator | Rosprirodnadzor – Federal Service for Supervision of Natural Resources | rpn.gov.ru | international_agency | official | refinery_outage | proposed |
| ca-RU-coast_guard_navy | RU | — | coast_guard_navy | Russian Navy (VMF) | mil.ru | international_agency | official | port_closure, force_majeure | proposed |

---

## ⚠️ Analytická poznámka: Russian source reliability

**KRITICKÉ**: Ruské státní zdroje jsou po 2022 nespolehlivé pro energetická data:
- Rosstat přestal publikovat detailní energetická data (vojenské tajemství od 2022)
- Rosneft/Gazprom výroční zprávy jsou zpožděné a nekompletní
- Hlavní metoda monitoringu = **third-party tanker tracking** (Vortexa, Kpler, TankerTrackers)

Přesto jsou sloty zachovány pro archivní a baseline reference, se statusy `unverified` pro
zdroje kde je kvalita dat pochybná.

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-RU-port_maritime_authority (Rosmorrechflot) | Rosmorrechflot = de-facto data source pro Russian crude loading ports: Primorsk (Baltic, ~1.2 mb/d), Ust-Luga (Baltic, ~0.8 mb/d), Novorossiysk (Black Sea, ~1.2 mb/d CPC+Russian), Kozmino (Pacific, ~0.8 mb/d) | Russian port loading data = partial; supplemented by Kpler/Vortexa satellite AIS tracking; každý CPC pump station issue (2022 Novorossiysk storm) = immediate supply event | Primorsk → EU (pre-2022); post-2022 → India, China, Turkey; Kozmino → China, India | **proposed** |
| ca-RU-noc (Rosneft) | Rosneft = ~40% Russian crude production (~4 mb/d); quarterly/annual reports = officially published but delayed; Rosneft Deutschland under German trustee; Rosneft PCK Schwedt (German refinery supply) | Rosneft CEO Igor Sechin = direct Kremlin link; Rosneft India deals (Nayara Energy); Rosneft China deals | Druzhba pipeline (southern route = Rosneft Ural crude); ESPO pipeline (Kozmino) | **unverified** — rosneft.ru aktivní ale data quality kompromitovaná sankcemi |
| ca-RU-central_bank (CBR) | CBR = klíčový pro tracking Russian petrodollar recycling; RUB/USD managed (CBR suspended free float 2022); každé CBR FX intervention = oil revenue signal | CBR partečně zmrazené rezervy ($300B+); CBR de-facto v izolaci od SWIFT; sanction compliance monitoring | RUB oil settlement (India, China) = alternative payment system signal | **proposed** — cbr.ru částečně dostupné |

### Primární monitoring metody (nad-official-domain)
- **Kpler** → kpler.com: tanker tracking (tier-1 Russian crude export monitoring)
- **Vortexa** → vortexa.com: real-time Russian fleet monitoring
- **TankerTrackers** → tankertracker.com: independent AIS analysis
- **OFAC** → ofac.treas.gov: US sanctions liste (SDN list, Russian oil entities)
- **OFSI** → gov.uk/ofsi: UK sanctions (Russian energy companies)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 43, "last_country": "RU", "last_batch_seq": 44 }
```
