# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_002_global_batch.md  
**Fáze:** global — krok batch (Fáze 1, celá fáze najednou)  
**Datum:** 2026-07-04  

---

## Shrnutí

Fáze 1 — globální vrstva. Navrhuje **115 slotů** přes 5 kategorií:
international_agency (40), exchange (25), weather (15), shipping (20), industry_body (15).
Každý slot má doménu a signální tagy. Cross-check aplikován na reprezentativní vzorek
(5 per kategorie) + všechny `unverified` záznamy. Žádný záznam bez zdůvodnění trader relevance.

---

## Navržené / aktualizované sloty

### Kategorie: international_agency (40 slotů)

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gl-international_agency-001 | — | — | global agency | IEA – International Energy Agency | iea.org | international_agency | official | storage_levels, production, imports | proposed |
| gl-international_agency-002 | — | — | global agency | OPEC Secretariat | opec.org | international_agency | official | quota_rhetoric, production, exports | proposed |
| gl-international_agency-003 | — | — | global agency | EIA – US Energy Information Administration | eia.gov | international_agency | official | storage_levels, production, exports | proposed |
| gl-international_agency-004 | — | — | data sub-feed | EIA Weekly Petroleum Status Report | eia.gov/petroleum/supply/weekly | international_agency | data_feed | storage_levels | proposed |
| gl-international_agency-005 | — | — | data sub-feed | IEA Oil Market Report | iea.org/reports/oil-market-report | international_agency | data_feed | production, imports | proposed |
| gl-international_agency-006 | — | — | data sub-feed | OPEC Monthly Oil Market Report (MOMR) | opec.org/publications/momr | international_agency | data_feed | quota_rhetoric, production | proposed |
| gl-international_agency-007 | — | — | global agency | GECF – Gas Exporting Countries Forum | gecf.org | international_agency | official | exports, quota_rhetoric | proposed |
| gl-international_agency-008 | — | — | global agency | IEF – International Energy Forum | ief.org | international_agency | official | pricing_formula | proposed |
| gl-international_agency-009 | — | — | sanctions authority | OFAC – US Treasury Office of Foreign Assets Control | ofac.treas.gov | international_agency | official | sanctions | proposed |
| gl-international_agency-010 | — | — | sanctions authority | EEAS / EU Consolidated Sanctions List | sanctions.ec.europa.eu | international_agency | official | sanctions | proposed |
| gl-international_agency-011 | — | — | sanctions authority | UN Security Council Sanctions Committee | un.org/securitycouncil/sanctions | international_agency | official | sanctions | proposed |
| gl-international_agency-012 | — | — | nuclear / sanctions | IAEA – International Atomic Energy Agency | iaea.org | international_agency | official | sanctions | proposed |
| gl-international_agency-013 | — | — | maritime regulator | IMO – International Maritime Organization | imo.org | international_agency | official | port_closure, vessel_loading | proposed |
| gl-international_agency-014 | — | — | gas TSO network | ENTSO-G – European gas transmission operators | entsog.eu | international_agency | official | pipeline_outage, storage_levels | proposed |
| gl-international_agency-015 | — | — | data sub-feed | GIE AGSI+ – EU Gas Storage Inventory | gie.eu | international_agency | data_feed | storage_levels | proposed |
| gl-international_agency-016 | — | — | energy regulator | ACER – EU Agency for Cooperation of Energy Regulators | acer.europa.eu | international_agency | official | pricing_formula, pipeline_outage | proposed |
| gl-international_agency-017 | — | — | energy ministry | US DOE – Department of Energy | energy.gov | international_agency | official | storage_levels, production, exports | proposed |
| gl-international_agency-018 | — | — | pipeline regulator | FERC – US Federal Energy Regulatory Commission | ferc.gov | international_agency | official | pipeline_outage, exports | proposed |
| gl-international_agency-019 | — | — | maritime advisory | MARAD – US Maritime Administration | maritime.dot.gov | international_agency | official | port_closure, vessel_loading | proposed |
| gl-international_agency-020 | — | — | maritime advisory | UKMTO – UK Maritime Trade Operations | ukmto.org | international_agency | official | port_closure, force_majeure | proposed |
| gl-international_agency-021 | — | — | global agency | UNCTAD – UN Conference on Trade & Development | unctad.org | international_agency | official | shipping, exports | proposed |
| gl-international_agency-022 | — | — | global agency | IGU – International Gas Union | igu.org | international_agency | official | term_contract, exports | proposed |
| gl-international_agency-023 | — | — | global agency | GIIGNL – International Group of LNG Importers | giignl.org | international_agency | official | imports, term_contract | proposed |
| gl-international_agency-024 | — | — | trade / customs | WCO – World Customs Organization | wcoomd.org | international_agency | official | exports, export_license | proposed |
| gl-international_agency-025 | — | — | sanctions authority | G7 Price Cap – US State Department | state.gov | international_agency | official | sanctions | proposed |
| gl-international_agency-026 | — | — | sanctions authority | OFSI – UK Office of Financial Sanctions Implementation | ofsi.blog.gov.uk | international_agency | official | sanctions | unverified |
| gl-international_agency-027 | — | — | sanctions authority | FATF – Financial Action Task Force | fatf-gafi.org | international_agency | official | sanctions | proposed |
| gl-international_agency-028 | — | — | derivatives regulator | CFTC – US Commodity Futures Trading Commission | cftc.gov | international_agency | official | pricing_formula | proposed |
| gl-international_agency-029 | — | — | trade statistics | UN COMTRADE | comtrade.un.org | international_agency | data_feed | exports, imports | proposed |
| gl-international_agency-030 | — | — | energy statistics | Eurostat Energy Statistics | ec.europa.eu/eurostat | international_agency | official | imports, storage_levels | proposed |
| gl-international_agency-031 | — | — | price benchmarks | IMF Primary Commodity Prices | imf.org/en/Research/commodity-prices | international_agency | data_feed | pricing_formula | proposed |
| gl-international_agency-032 | — | — | price benchmarks | World Bank Commodity Markets (Pink Sheet) | worldbank.org/en/research/commodity-markets | international_agency | data_feed | pricing_formula | proposed |
| gl-international_agency-033 | — | — | humanitarian / supply | UN OCHA – ReliefWeb | reliefweb.int | international_agency | official | force_majeure | proposed |
| gl-international_agency-034 | — | — | data sub-feed | IEA Gas Market Report | iea.org/reports/gas-market-report | international_agency | data_feed | exports, imports | proposed |
| gl-international_agency-035 | — | — | data sub-feed | EIA Short-Term Energy Outlook (STEO) | eia.gov/steo | international_agency | data_feed | production, pricing_formula | proposed |
| gl-international_agency-036 | — | — | data sub-feed | OPEC Annual Statistical Bulletin | asb.opec.org | international_agency | data_feed | production, exports | proposed |
| gl-international_agency-037 | — | — | ship registry | IMO GISIS – Global Integrated Shipping Information System | gisis.imo.org | international_agency | data_feed | vessel_loading, port_closure | proposed |
| gl-international_agency-038 | — | — | maritime security | MSCHOA – Maritime Security Centre Horn of Africa | mschoa.org | international_agency | official | port_closure, force_majeure | proposed |
| gl-international_agency-039 | — | — | maritime security | NATO Op. Sea Guardian / Allied Maritime Command | mc.nato.int | international_agency | official | force_majeure | unverified |
| gl-international_agency-040 | — | — | global agency | IRENA – International Renewable Energy Agency | irena.org | international_agency | official | production | proposed |

---

### Kategorie: exchange (25 slotů)

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gl-exchange-001 | — | — | commodity exchange | CME Group / NYMEX | cmegroup.com | exchange | official | pricing_formula, term_contract | proposed |
| gl-exchange-002 | — | — | commodity exchange | ICE Futures Europe | theice.com | exchange | official | pricing_formula, term_contract | proposed |
| gl-exchange-003 | — | — | commodity exchange | DME – Dubai Mercantile Exchange | dubaimerc.com | exchange | official | pricing_formula | proposed |
| gl-exchange-004 | — | — | commodity exchange | Shanghai INE – International Energy Exchange | ine.cn | exchange | official | pricing_formula | proposed |
| gl-exchange-005 | — | — | commodity exchange | SGX – Singapore Exchange | sgx.com | exchange | official | pricing_formula | proposed |
| gl-exchange-006 | — | — | commodity exchange | TOCOM – Tokyo Commodity Exchange | tocom.or.jp | exchange | official | pricing_formula | proposed |
| gl-exchange-007 | — | — | commodity exchange | MCX India – Multi Commodity Exchange | mcxindia.com | exchange | official | pricing_formula | proposed |
| gl-exchange-008 | — | — | energy exchange | EEX – European Energy Exchange | eex.com | exchange | official | pricing_formula | proposed |
| gl-exchange-009 | — | — | power exchange | Nord Pool | nordpoolgroup.com | exchange | official | pricing_formula | proposed |
| gl-exchange-010 | — | — | power exchange | EPEX SPOT | epexspot.com | exchange | official | pricing_formula | proposed |
| gl-exchange-011 | — | — | power exchange | JEPX – Japan Electric Power Exchange | jepx.or.jp | exchange | official | pricing_formula | proposed |
| gl-exchange-012 | — | — | gas hub operator | Gasunie – TTF Virtual Trading Point | gasunie.nl | exchange | official | pricing_formula | proposed |
| gl-exchange-013 | — | — | commodity exchange | DCE – Dalian Commodity Exchange | dce.com.cn | exchange | official | pricing_formula | proposed |
| gl-exchange-014 | — | — | commodity exchange | CZCE – Zhengzhou Commodity Exchange | czce.com.cn | exchange | official | pricing_formula | unverified |
| gl-exchange-015 | — | — | commodity exchange | MOEX – Moscow Exchange (energy desk) | moex.com | exchange | official | pricing_formula | proposed |
| gl-exchange-016 | — | — | metals exchange | LME – London Metal Exchange | lme.com | exchange | official | pricing_formula | proposed |
| gl-exchange-017 | — | — | commodity exchange | ASX – Australian Securities Exchange | asx.com.au | exchange | official | pricing_formula | proposed |
| gl-exchange-018 | — | — | commodity exchange | Borsa Istanbul (energy futures) | borsaistanbul.com | exchange | official | pricing_formula | unverified |
| gl-exchange-019 | — | — | commodity exchange | NCDEX India | ncdex.com | exchange | official | pricing_formula | unverified |
| gl-exchange-020 | — | — | OTC reference | ISDA – swaps / OTC oil definitions | isda.org | exchange | official | pricing_formula, term_contract | proposed |
| gl-exchange-021 | — | — | data sub-feed | ICE JKM LNG Futures | theice.com/lng | exchange | data_feed | pricing_formula | proposed |
| gl-exchange-022 | — | — | data sub-feed | ICE NBP UK Natural Gas | theice.com/uk-natural-gas | exchange | data_feed | pricing_formula | proposed |
| gl-exchange-023 | — | — | data sub-feed | ICE EUA Carbon Allowances | theice.com/carbon | exchange | data_feed | pricing_formula | proposed |
| gl-exchange-024 | — | — | pipeline/pricing data | FERC NatGas Pipeline Tariff Data | ferc.gov/industries-data/natural-gas | exchange | data_feed | pricing_formula, pipeline_outage | proposed |
| gl-exchange-025 | — | — | commodity exchange | HKEX – Hong Kong Exchange (energy products) | hkex.com.hk | exchange | official | pricing_formula | unverified |

---

### Kategorie: weather (15 slotů)

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gl-weather-001 | — | — | met authority | NOAA – National Oceanic and Atmospheric Administration | noaa.gov | weather | official | hurricane, production | proposed |
| gl-weather-002 | — | — | hurricane tracking | NHC – National Hurricane Center | nhc.noaa.gov | weather | official | hurricane | proposed |
| gl-weather-003 | — | — | met authority | ECMWF – European Centre for Medium-Range Weather Forecasts | ecmwf.int | weather | official | hurricane, force_majeure | proposed |
| gl-weather-004 | — | — | met authority | UK Met Office | metoffice.gov.uk | weather | official | force_majeure | proposed |
| gl-weather-005 | — | — | met authority | Norwegian Meteorological Institute | met.no | weather | official | force_majeure, production | proposed |
| gl-weather-006 | — | — | met authority | KNMI – Royal Netherlands Meteorological Institute | knmi.nl | weather | official | force_majeure | proposed |
| gl-weather-007 | — | — | met authority | DWD – Deutscher Wetterdienst | dwd.de | weather | official | force_majeure | proposed |
| gl-weather-008 | — | — | met authority | JMA – Japan Meteorological Agency | jma.go.jp | weather | official | force_majeure | proposed |
| gl-weather-009 | — | — | typhoon tracking | JTWC – Joint Typhoon Warning Center | metoc.navy.mil | weather | official | hurricane, force_majeure | unverified |
| gl-weather-010 | — | — | met authority | Saudi NCM – National Center of Meteorology | ncm.gov.sa | weather | official | force_majeure | proposed |
| gl-weather-011 | — | — | met authority | BoM – Australian Bureau of Meteorology | bom.gov.au | weather | official | force_majeure, production | proposed |
| gl-weather-012 | — | — | met authority | INMET – Brazilian Institute of Meteorology | inmet.gov.br | weather | official | force_majeure, production | proposed |
| gl-weather-013 | — | — | met authority | Météo-France | meteofrance.com | weather | official | force_majeure | proposed |
| gl-weather-014 | — | — | met authority | WMO – World Meteorological Organization | wmo.int | weather | official | hurricane, force_majeure | proposed |
| gl-weather-015 | — | — | met authority | SMHI – Swedish Meteorological & Hydrological Institute | smhi.se | weather | official | force_majeure | proposed |

---

### Kategorie: shipping (20 slotů)

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gl-shipping-001 | — | — | freight benchmark | Baltic Exchange | balticexchange.com | shipping | official | pricing_formula | proposed |
| gl-shipping-002 | — | — | classification society | Lloyd's Register | lr.org | shipping | official | vessel_loading | proposed |
| gl-shipping-003 | — | — | classification society | DNV – Det Norske Veritas | dnv.com | shipping | official | vessel_loading | proposed |
| gl-shipping-004 | — | — | classification society | Bureau Veritas | bureauveritas.com | shipping | official | vessel_loading | proposed |
| gl-shipping-005 | — | — | classification society | ABS – American Bureau of Shipping | eagle.org | shipping | official | vessel_loading | proposed |
| gl-shipping-006 | — | — | ship database | Equasis – EU Port State Control database | equasis.org | shipping | official | vessel_loading, port_closure | proposed |
| gl-shipping-007 | — | — | tanker vetting | OCIMF – Oil Companies Int'l Marine Forum | ocimf.org | shipping | official | vessel_loading | proposed |
| gl-shipping-008 | — | — | tanker operators | Intertanko | intertanko.com | shipping | official | vessel_loading, port_closure | proposed |
| gl-shipping-009 | — | — | shipping body | BIMCO | bimco.org | shipping | official | vessel_loading, term_contract | proposed |
| gl-shipping-010 | — | — | shipping body | ICS – International Chamber of Shipping | ics-shipping.org | shipping | official | port_closure, vessel_loading | proposed |
| gl-shipping-011 | — | — | naval / escort ops | EUNAVFOR Operation Aspides | eunavfor.eu | shipping | official | port_closure, force_majeure | proposed |
| gl-shipping-012 | — | — | labor / strikes | ITF – International Transport Workers' Federation | itf.org | shipping | official | port_closure | proposed |
| gl-shipping-013 | — | — | bunker industry | IBIA – International Bunker Industry Association | ibia.net | shipping | official | vessel_loading | proposed |
| gl-shipping-014 | — | — | war risk / P&I | IUMI – International Union of Marine Insurance | iumi.org | shipping | official | vessel_loading, force_majeure | proposed |
| gl-shipping-015 | — | — | P&I insurer | Gard P&I Club | gard.no | shipping | official | vessel_loading, force_majeure | proposed |
| gl-shipping-016 | — | — | P&I insurer | Skuld P&I Club | skuld.com | shipping | official | vessel_loading, force_majeure | proposed |
| gl-shipping-017 | — | — | P&I insurer | West of England P&I | westpandi.com | shipping | official | vessel_loading, force_majeure | proposed |
| gl-shipping-018 | — | — | maritime security | MSCHOA – EU Horn of Africa maritime security | mschoa.org | shipping | official | port_closure, force_majeure | proposed |
| gl-shipping-019 | — | — | coastal state advisory | USCG – US Coast Guard | uscg.mil | shipping | official | port_closure, vessel_loading | proposed |
| gl-shipping-020 | — | — | shipping body | Intercargo – tanker / bulk operators | intercargo.org | shipping | official | vessel_loading | proposed |

---

### Kategorie: industry_body (15 slotů)

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gl-industry_body-001 | — | — | industry stats | API – American Petroleum Institute | api.org | industry_body | official | storage_levels, production | proposed |
| gl-industry_body-002 | — | — | upstream signal | Baker Hughes Rig Count | bakerhughes.com | industry_body | data_feed | production | proposed |
| gl-industry_body-003 | — | — | upstream / safety | IOGP – Int'l Assoc. of Oil & Gas Producers | iogp.org | industry_body | official | production, force_majeure | proposed |
| gl-industry_body-004 | — | — | country producers | CAPP – Canadian Assoc. of Petroleum Producers | capp.ca | industry_body | official | production, exports | proposed |
| gl-industry_body-005 | — | — | country producers | APPEA – Australian Petroleum Production & Exploration | appea.com.au | industry_body | official | production, exports | proposed |
| gl-industry_body-006 | — | — | country producers | Norog – Norwegian Oil and Gas Association | norog.no | industry_body | official | production, force_majeure | proposed |
| gl-industry_body-007 | — | — | refinery stats | FuelsEurope (formerly Europia) | fuelseurope.eu | industry_body | official | refinery_outage, imports | proposed |
| gl-industry_body-008 | — | — | refinery stats | AFPM – American Fuel & Petrochemical Manufacturers | afpm.org | industry_body | official | refinery_outage, storage_levels | proposed |
| gl-industry_body-009 | — | — | upstream US | IPAA – Independent Petroleum Assoc. of America | ipaa.org | industry_body | official | production | proposed |
| gl-industry_body-010 | — | — | global industry | WPC – World Petroleum Council | world-petroleum.org | industry_body | official | production | proposed |
| gl-industry_body-011 | — | — | drilling market | IADC – Int'l Assoc. of Drilling Contractors | iadc.org | industry_body | official | production | proposed |
| gl-industry_body-012 | — | — | midstream US | GPA Midstream Association | gpamidstream.org | industry_body | official | production, pipeline_outage | proposed |
| gl-industry_body-013 | — | — | market authority | EMA – Energy Market Authority Singapore | ema.gov.sg | industry_body | official | pricing_formula, imports | proposed |
| gl-industry_body-014 | — | — | technical / reserves | SPE – Society of Petroleum Engineers | spe.org | industry_body | official | production | proposed |
| gl-industry_body-015 | — | — | annual stats | Energy Institute (Statistical Review of World Energy) | energyinst.org | industry_body | data_feed | production, exports | proposed |

---

## Cross-check (3 perspektivy) — representativní vzorek + všechny unverified

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gl-international_agency-001 (IEA) | OMR a MTOMR pohybují trh v den publikace — tier 1 supply signal | IEA member-state advisory role; coordinated SPR release 2022 — přímý vliv na ceny | Publikuje LNG trade flow data; OECD inventories | **proposed** |
| gl-international_agency-003 (EIA) | WPSR v úterý pohybuje WTI spready (Cushing build/draw) | STEO = US government supply outlook; price-moving při revision | US import/export data; NatGas pipeline flows | **proposed** |
| gl-international_agency-009 (OFAC) | SDN listingy zastavují tok ropy (Iran, Russia, Venezuela) | Přímý sankční nástroj; každý nový CAATSA/EO → okamžitý price gap | Dark fleet blokáže; insurance void na vessel_loading | **proposed** |
| gl-international_agency-014 (ENTSO-G) | Transparentní platforma: reálné toky plynu do EU | Gazprom flow přes Ukrainu/Nord Stream visible in real-time | Pipeline congestion, reverse flow kapacity | **proposed** |
| gl-international_agency-026 (OFSI) | UK sanctions doplňují OFAC; OFSI finančně zmrazuje EU/UK operace | Koordinované UK-EU sankce; energy sector designation | Insurance/finance block → vessel_loading impact | **unverified** — domain ofsi.blog.gov.uk je starý gov.uk blog; správná adresa může být gov.uk/ofsi; nutná validace |
| gl-international_agency-039 (NATO mc.nato.int) | Omezený přímý supply signal | NATO MSO Sea Guardian vydává maritime advisories pro Středomoří | Pohyb lodí přes Sicilský průliv, Jaderské moře | **unverified** — mc.nato.int je správná doména NATO Maritime Command, ale public advisories mohou být na alliedcommand.nato.int nebo jinde |
| gl-exchange-003 (DME) | Oman crude = klíčový benchmark pro asijská OSP (Aramco, ADNOC) | DME settlement pohybuje Saudi/UAE official selling prices | Ras Tanura a Fujairah loading ceny odvozeny od DME settlement | **proposed** |
| gl-exchange-004 (INE/ine.cn) | Shanghai crude = čínský benchmark; INE open interest proxy čínské poptávky | Čínské regulace INE margin = geopolitický signál o domácí ceně ropy | Import arbitráže Brent–INE spread | **proposed** |
| gl-exchange-014 (CZCE) | Omezenáenergetická komodita; hlavně agri | Omezená geopolitická relevance | Nízká logistická relevance pro crude/LNG | **unverified** — zachovat jako nízká priorita; verifikovat zda CZCE nabízí energy futures |
| gl-exchange-018 (Borsa Istanbul) | TurkStream příjmy linkage; limitované futures | Turecko jako tranzitní hub (geopolitika) | Limitovaný líkvidní trh energie | **unverified** — ověřit zda energetické futures aktivně obchodovány |
| gl-exchange-019 (NCDEX) | Agri-zaměřeno; crude sekundárně | Nízká přímá geopolitická relevance | Nízká | **unverified** — zvážit vypustit z whitelist; zachovat v katalogu jako low priority |
| gl-exchange-025 (HKEX) | HK exchange; CNH oil swap produkty existují | Limitovaná relevance vs INE | Nízká přímá logistická relevance | **unverified** — ověřit specifické energy produkty na HKEX |
| gl-weather-002 (NHC) | Hurikán → US Gulf produkce shut-in (7+ mb/d v peak sezóně) | Vyhlášení Category 3+ uzavírá přístavy – přímý regulatory trigger | GOM platform evacuations → LOOP/Houston Ship Channel uzavření | **proposed** |
| gl-weather-009 (JTWC) | Tajfun = LNG demand spike (Japonsko, Jižní Korea, Tchaj-wan) + produkční výpadek (Malajsie, Indonésie) | US Navy advisory; přesnost < 24 h předpovědi | Malacca průjezd ovlivněn extrémní bouří | **unverified** — JTWC webové sídlo: `www.metoc.navy.mil/jtwc/jtwc.html`; validovat prefix |
| gl-shipping-001 (Baltic Exchange) | BDTI a Suezmax rates = proxy cost of seaborne crude; Aframax critical pro Urals | War risk premium v Baltic Clean Tanker Index → sanctions signal | Freight cost = component of CIF crude delivered price | **proposed** |
| gl-shipping-005 (ABS / eagle.org) | ABS certificate = vetting pre-condition pro tanker loading | Withdrawal of ABS class → vessel untankable (sanctions pressure) | eagle.org je správný domain pro ABS verifier | **proposed** |
| gl-industry_body-001 (API) | API weekly report (úterý 16:30 ET) = leading indicator před EIA WPSR; ±2 mb/d vs odhad pohne WTI | API nemá sankční / policy roli | Cushing stocks + crude imports v reportu | **proposed** |
| gl-industry_body-002 (Baker Hughes) | Rig count (pátek) = lagging upstream capex signal; US shale growth proxy | Nízká přímá geopolitická role | Permian / Eagle Ford active rigs | **proposed** |
| gl-industry_body-015 (Energy Institute) | Nahrazuje BP Statistical Review 2023+; global R/P ratios, capacity | Politicky nezávislá publikace vs NOC data | Globální production/exports benchmarking | **proposed** |

---

## Unverified / Anti-patterns

### Unverified záznamy (nutná ruční validace domén)

| id | entity | domain navržená | problém |
|----|--------|----------------|---------|
| gl-international_agency-026 | OFSI | ofsi.blog.gov.uk | Bloggingová subdoména UK gov.; správná adresa OFSI je gov.uk/government/organisations/office-of-financial-sanctions-implementation |
| gl-international_agency-039 | NATO Op. Sea Guardian | mc.nato.int | mc.nato.int = Allied Maritime Command; public advisories mohou být na odlišné URL; ověřit |
| gl-weather-009 | JTWC | metoc.navy.mil | JTWC je na `metoc.navy.mil/jtwc` — ověřit, zda přímá URL metoc.navy.mil funguje jako vstup |
| gl-exchange-014 | CZCE | czce.com.cn | Doména aktivní; ověřit zda energetické (crude/LNG) futures jsou obchodovány |
| gl-exchange-018 | Borsa Istanbul energy | borsaistanbul.com | Doména správná; ověřit aktivitu energy futures produktů |
| gl-exchange-019 | NCDEX | ncdex.com | Doména aktivní; energetická relevance omezená — nízká priorita pro whitelist |
| gl-exchange-025 | HKEX | hkex.com.hk | Doména správná; ověřit CNH oil swap / energy futures scope |

### Anti-patterns (vyloučeno z batch)

- **Platts / S&P Global, Argus, ICIS, Reuters, Bloomberg** — agregátoři; sekundární zdroje;
  jsou relevantní pro monitoring ale **ne** pro whitelist (primary-first pravidlo).
- **CHIRP Maritime** (chirp.aero) — safety reporting; žádný price-moving signal.
- **OPEC Fund (ofid.org)** — financování, ne tržní signál.
- **NATO UNFIL / UNIFIL** — vojenská operace bez přímého energy signálu.
- **EIA sub-feeds s identickým doménem** (cmegroup.com/markets/energy/...) — zachyceny
  jako data_feed záznamy; duplicitní doménový vstup bez odlišné entity je anti-pattern.

---

## Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 0,
  "last_country": null,
  "crosscheck_cursor": 0,
  "last_batch_seq": 2
}
```

Po merge → **další dávka:** `claude-sonnet-4-6_003_country_authority_SA.md`
(Fáze 2, první země = SA – Saudi Arabia, 10 authority_types).
