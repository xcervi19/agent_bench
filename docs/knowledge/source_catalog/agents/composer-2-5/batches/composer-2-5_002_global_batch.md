# Catalog batch

**Agent:** composer-2-5 (Composer 2.5)  
**Soubor:** composer-2-5_002_global_batch.md  
**Fáze:** global — krok batch (Fáze 1)  
**Datum:** 2026-07-04  

---

## Shrnutí

115 globálních slotů: agentury (40), burzy (25), weather (15), shipping (20), industry bodies (15).  
**107 proposed**, **6 unverified**, **2 empty** (rezervované sloty bez jasné Tier-1 entity).

---

### Navržené / aktualizované sloty

#### international_agency (40)

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gl-international_agency-001 | — | — | international_agency | IEA | iea.org | international_agency | official | production,exports,storage_levels | proposed |
| gl-international_agency-002 | US | — | international_agency | EIA | eia.gov | international_agency | official | production,exports,imports,storage_levels | proposed |
| gl-international_agency-003 | — | — | international_agency | OPEC | opec.org | international_agency | official | production,quota_rhetoric,exports | proposed |
| gl-international_agency-004 | — | — | international_agency | IEF | ieforum.org | international_agency | official | production,storage_levels | proposed |
| gl-international_agency-005 | — | — | international_agency | JODI | jodidata.org | international_agency | official | production,exports,imports | proposed |
| gl-international_agency-006 | — | — | international_agency | GECF | gecf.org | international_agency | official | production,exports,term_contract | proposed |
| gl-international_agency-007 | — | — | international_agency | OECD | oecd.org | international_agency | official | production,imports,storage_levels | proposed |
| gl-international_agency-008 | — | — | international_agency | Eurostat | ec.europa.eu | international_agency | official | imports,storage_levels | proposed |
| gl-international_agency-009 | — | — | international_agency | UN Comtrade | comtradeplus.un.org | international_agency | official | exports,imports | proposed |
| gl-international_agency-010 | — | — | international_agency | UNCTAD | unctad.org | international_agency | official | exports,imports,vessel_loading | proposed |
| gl-international_agency-011 | — | — | international_agency | EITI | eiti.org | international_agency | official | production,exports | proposed |
| gl-international_agency-012 | — | — | international_agency | IRENA | irena.org | international_agency | official | production | proposed |
| gl-international_agency-013 | — | — | international_agency | UNECE | unece.org | international_agency | official | production,exports | proposed |
| gl-international_agency-014 | — | — | international_agency | ASEAN Centre for Energy | aseanenergy.org | international_agency | official | production,imports | proposed |
| gl-international_agency-015 | US | — | international_agency | US DOE | energy.gov | government_regulator | official | production,exports,storage_levels | proposed |
| gl-international_agency-016 | — | — | international_agency | EU Energy | energy.ec.europa.eu | government_regulator | official | imports,storage_levels,sanctions | proposed |
| gl-international_agency-017 | GB | — | international_agency | NSTA (UK North Sea) | nstauthority.co.uk | government_regulator | official | production,exports | proposed |
| gl-international_agency-018 | CA | — | international_agency | Canada Energy Regulator | cer-rec.gc.ca | government_regulator | official | production,exports,pipeline_outage | proposed |
| gl-international_agency-019 | US | — | international_agency | US FERC | ferc.gov | government_regulator | official | pipeline_outage,exports | proposed |
| gl-international_agency-020 | US | — | international_agency | US BOEM | boem.gov | government_regulator | official | production,term_contract | proposed |
| gl-international_agency-021 | US | — | international_agency | US PHMSA | phmsa.dot.gov | government_regulator | official | pipeline_outage | proposed |
| gl-international_agency-022 | US | — | international_agency | US Treasury OFAC | treasury.gov | government_regulator | official | sanctions,export_license | proposed |
| gl-international_agency-023 | — | — | international_agency | EU Sanctions Map | sanctionsmap.eu | government_regulator | official | sanctions,export_license | proposed |
| gl-international_agency-024 | — | — | international_agency | IMF Primary Commodities | imf.org | international_agency | official | pricing_formula,exports | proposed |
| gl-international_agency-025 | — | — | international_agency | World Bank Open Data | data.worldbank.org | international_agency | official | production,imports | proposed |
| gl-international_agency-026 | AU | — | international_agency | AEMO | aemo.com.au | international_agency | official | production,exports | proposed |
| gl-international_agency-027 | JP | — | international_agency | METI Japan | meti.go.jp | government_regulator | official | production,imports | proposed |
| gl-international_agency-028 | BR | — | international_agency | ANP Brazil | gov.br/anp | government_regulator | official | production,exports | proposed |
| gl-international_agency-029 | MX | — | international_agency | SENER Mexico | gob.mx/sener | government_regulator | official | production,exports | proposed |
| gl-international_agency-030 | CO | — | international_agency | ANH Colombia | anh.gov.co | government_regulator | official | production,exports | proposed |
| gl-international_agency-031 | NO | — | international_agency | Norwegian Petroleum Directorate | npd.no | government_regulator | official | production,exports | proposed |
| gl-international_agency-032 | NL | — | international_agency | SodM Netherlands | sodm.nl | government_regulator | official | production,exports | proposed |
| gl-international_agency-033 | — | — | international_agency | WMO | wmo.int | international_agency | official | hurricane | proposed |
| gl-international_agency-034 | — | — | international_agency | Copernicus Climate | climate.copernicus.eu | international_agency | official | hurricane,production | proposed |
| gl-international_agency-035 | — | — | international_agency | IEA Oil Market Report | iea.org | international_agency | official | production,storage_levels | proposed |
| gl-international_agency-036 | — | — | international_agency | OPEC MOMR | opec.org | international_agency | official | production,quota_rhetoric | proposed |
| gl-international_agency-037 | — | — | international_agency | JODI Gas | jodidata.org | international_agency | official | production,exports,imports | proposed |
| gl-international_agency-038 | — | — | international_agency | UN Security Council | un.org | international_agency | official | sanctions | proposed |
| gl-international_agency-039 | — | — | international_agency | APPEC | appec.org | industry_body | official | production,term_contract | unverified |
| gl-international_agency-040 | — | — | international_agency | (reserved) | — | international_agency | — | — | empty |

#### exchange (25)

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gl-exchange-001 | US | — | exchange | CME Group | cmegroup.com | exchange | official | pricing_formula,storage_levels | proposed |
| gl-exchange-002 | US | — | exchange | ICE | theice.com | exchange | official | pricing_formula,exports | proposed |
| gl-exchange-003 | CN | — | exchange | Shanghai INE | ine.cn | exchange | official | pricing_formula,imports | proposed |
| gl-exchange-004 | JP | — | exchange | TOCOM | tocom.or.jp | exchange | official | pricing_formula | proposed |
| gl-exchange-005 | DE | — | exchange | EEX | eex.com | exchange | official | pricing_formula,storage_levels | proposed |
| gl-exchange-006 | RU | — | exchange | Moex | moex.com | exchange | official | pricing_formula,exports | proposed |
| gl-exchange-007 | SG | — | exchange | SGX | sgx.com | exchange | official | pricing_formula | proposed |
| gl-exchange-008 | HK | — | exchange | HKEX | hkex.com.hk | exchange | official | pricing_formula | proposed |
| gl-exchange-009 | NO | — | exchange | Nord Pool | nordpoolgroup.com | exchange | official | pricing_formula | proposed |
| gl-exchange-010 | US | — | exchange | Nodal Exchange | nodalexchange.com | exchange | official | pricing_formula | proposed |
| gl-exchange-011 | AU | — | exchange | ASX | asx.com.au | exchange | official | pricing_formula | proposed |
| gl-exchange-012 | GB | — | exchange | LME | lme.com | exchange | official | pricing_formula | proposed |
| gl-exchange-013 | NG | — | exchange | NGX | ngxgroup.com | exchange | official | pricing_formula,exports | proposed |
| gl-exchange-014 | MY | — | exchange | Bursa Malaysia | bursamalaysia.com | exchange | official | pricing_formula,exports | proposed |
| gl-exchange-015 | TR | — | exchange | Borsa Istanbul | borsaistanbul.com | exchange | official | pricing_formula | proposed |
| gl-exchange-016 | ZA | — | exchange | JSE | jse.co.za | exchange | official | pricing_formula | proposed |
| gl-exchange-017 | IN | — | exchange | MCX India | mcxindia.com | exchange | official | pricing_formula,imports | proposed |
| gl-exchange-018 | CN | — | exchange | Dalian Commodity Exchange | dce.com.cn | exchange | official | pricing_formula,imports | proposed |
| gl-exchange-019 | CN | — | exchange | Zhengzhou Commodity Exchange | czce.com.cn | exchange | official | pricing_formula | proposed |
| gl-exchange-020 | AE | — | exchange | DGCX Dubai | dgcx.ae | exchange | official | pricing_formula | proposed |
| gl-exchange-021 | TH | — | exchange | TFEX | tfex.co.th | exchange | official | pricing_formula | proposed |
| gl-exchange-022 | KR | — | exchange | Korea Exchange | krx.co.kr | exchange | official | pricing_formula,imports | proposed |
| gl-exchange-023 | US | cushing | exchange | NYMEX WTI (via CME) | cmegroup.com | exchange | official | pricing_formula,storage_levels | proposed |
| gl-exchange-024 | GB | ara | exchange | ICE Brent | theice.com | exchange | official | pricing_formula,exports | proposed |
| gl-exchange-025 | — | — | exchange | (reserved) | — | exchange | — | — | empty |

#### weather (15)

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gl-weather-001 | US | — | weather | NOAA | noaa.gov | weather | official | hurricane,production | proposed |
| gl-weather-002 | US | — | weather | NHC | nhc.noaa.gov | weather | official | hurricane,port_closure | proposed |
| gl-weather-003 | — | — | weather | ECMWF | ecmwf.int | weather | official | hurricane,production | proposed |
| gl-weather-004 | GB | — | weather | UK Met Office | metoffice.gov.uk | weather | official | hurricane | proposed |
| gl-weather-005 | US | — | weather | NOAA CPC | cpc.ncep.noaa.gov | weather | official | hurricane,production | proposed |
| gl-weather-006 | US | — | weather | NWS | weather.gov | weather | official | hurricane,port_closure | proposed |
| gl-weather-007 | CA | — | weather | Environment Canada | weather.gc.ca | weather | official | hurricane,production | proposed |
| gl-weather-008 | AU | — | weather | Bureau of Meteorology | bom.gov.au | weather | official | hurricane,production | proposed |
| gl-weather-009 | JP | — | weather | JMA | jma.go.jp | weather | official | hurricane,imports | proposed |
| gl-weather-010 | — | — | weather | Copernicus CDS | cds.climate.copernicus.eu | weather | official | hurricane | proposed |
| gl-weather-011 | FR | — | weather | Meteo France | meteofrance.com | weather | official | hurricane | proposed |
| gl-weather-012 | DE | — | weather | DWD | dwd.de | weather | official | hurricane | proposed |
| gl-weather-013 | NL | — | weather | KNMI | knmi.nl | weather | official | hurricane | proposed |
| gl-weather-014 | US | us_gulf_hub | weather | NOAA NWS Gulf | weather.gov | weather | official | hurricane,port_closure,refinery_outage | proposed |
| gl-weather-015 | US | — | weather | Colorado State Hurricane Forecast | tropical.colostate.edu | weather | official | hurricane | unverified |

#### shipping (20)

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gl-shipping-001 | — | — | shipping | IMO | imo.org | shipping | official | vessel_loading,port_closure | proposed |
| gl-shipping-002 | US | — | shipping | US MARAD | maritime.dot.gov | shipping | official | vessel_loading,port_closure | proposed |
| gl-shipping-003 | — | — | shipping | EMSA | emsa.europa.eu | shipping | official | vessel_loading,sanctions | proposed |
| gl-shipping-004 | GB | — | shipping | Baltic Exchange | balticexchange.com | shipping | official | vessel_loading,pricing_formula | proposed |
| gl-shipping-005 | US | — | shipping | USCG Navcen | navcen.uscg.gov | shipping | official | port_closure,vessel_loading | proposed |
| gl-shipping-006 | — | — | shipping | IOPC Funds | iopcfunds.org | shipping | official | port_closure | proposed |
| gl-shipping-007 | — | — | shipping | GISIS IMO | gisis.imo.org | shipping | official | vessel_loading | proposed |
| gl-shipping-008 | — | — | shipping | MarineTraffic | marinetraffic.com | shipping | data_feed | vessel_loading,port_closure | proposed |
| gl-shipping-009 | — | — | shipping | VesselFinder | vesselfinder.com | shipping | data_feed | vessel_loading | proposed |
| gl-shipping-010 | NL | rotterdam | shipping | Port of Rotterdam | portofrotterdam.com | infrastructure | official | vessel_loading,storage_levels | proposed |
| gl-shipping-011 | SG | singapore | shipping | MPA Singapore | mpa.gov.sg | infrastructure | official | vessel_loading,port_closure | proposed |
| gl-shipping-012 | PA | panama | shipping | Panama Canal Authority | pancanal.com | infrastructure | official | port_closure,vessel_loading | proposed |
| gl-shipping-013 | EG | suez | shipping | Suez Canal Authority | suezcanal.gov.eg | infrastructure | official | port_closure,vessel_loading | proposed |
| gl-shipping-014 | TR | bospor | shipping | Turkish Straits VTS | uab.gov.tr | infrastructure | official | port_closure,vessel_loading | unverified |
| gl-shipping-015 | — | — | shipping | International Chamber of Shipping | ics-shipping.org | shipping | official | vessel_loading,sanctions | proposed |
| gl-shipping-016 | US | houston_ship_channel | shipping | USACE Galveston | usace.army.mil | infrastructure | official | port_closure,vessel_loading | proposed |
| gl-shipping-017 | — | — | shipping | UNCTAD Review of Maritime Transport | unctad.org | shipping | official | vessel_loading,exports | proposed |
| gl-shipping-018 | — | — | shipping | Lloyd's Register | lr.org | shipping | official | vessel_loading | unverified |
| gl-shipping-019 | — | malacca | shipping | MRCC Singapore | portofsingapore.com | infrastructure | official | port_closure,vessel_loading | unverified |
| gl-shipping-020 | — | — | shipping | Clarksons Research | clarksons.com | shipping | official | vessel_loading,pricing_formula | unverified |

#### industry_body (15)

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gl-industry_body-001 | US | — | industry_body | API | api.org | industry_body | official | production,storage_levels,refinery_outage | proposed |
| gl-industry_body-002 | — | — | industry_body | IGU | igu.org | industry_body | official | production,exports,term_contract | proposed |
| gl-industry_body-003 | — | — | industry_body | IOGP | iogp.org | industry_body | official | production,force_majeure | proposed |
| gl-industry_body-004 | — | — | industry_body | SPE | spe.org | industry_body | official | production | proposed |
| gl-industry_body-005 | — | — | industry_body | WPC Energy | wpcenergy.org | industry_body | official | production,term_contract | proposed |
| gl-industry_body-006 | — | — | industry_body | ARPEL | arpel.org | industry_body | official | production,exports | proposed |
| gl-industry_body-007 | — | — | industry_body | CONCAWE | concawe.eu | industry_body | official | refinery_outage,storage_levels | proposed |
| gl-industry_body-008 | — | — | industry_body | FuelsEurope | fuelseurope.eu | industry_body | official | refinery_outage,imports | proposed |
| gl-industry_body-009 | US | — | industry_body | AFPM | afpm.org | industry_body | official | refinery_outage,production | proposed |
| gl-industry_body-010 | GB | — | industry_body | Energy Institute | energyinst.org | industry_body | official | production,storage_levels | proposed |
| gl-industry_body-011 | AU | — | industry_body | APPEA | appea.com.au | industry_body | official | production,exports | proposed |
| gl-industry_body-012 | CA | — | industry_body | CAPP | capp.ca | industry_body | official | production,exports | proposed |
| gl-industry_body-013 | — | — | industry_body | IPIECA | ipieca.org | industry_body | official | production,force_majeure | proposed |
| gl-industry_body-014 | — | — | industry_body | Gas Infrastructure Europe | gie.eu | industry_body | official | storage_levels,pipeline_outage | proposed |
| gl-industry_body-015 | US | — | industry_body | EIA STEO (industry context) | eia.gov | industry_body | official | production,storage_levels | proposed |

---

### Cross-check (3 perspektivy) — Tier 1 vzorky

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gl-international_agency-001 | IEA OMR, monthly oil stats | IEA emergency stock releases | IEA freight / trade flow reports | **proposed** |
| gl-international_agency-002 | Weekly petroleum status, STEO | US export policy via DOE | Gulf Coast refinery/outage data | **proposed** |
| gl-international_agency-003 | OPEC+ production quotas | Ministerial statements | Member export allocations | **proposed** |
| gl-international_agency-022 | — | OFAC SDN designations, general licenses | Sanctions on shipping/insurance | **proposed** |
| gl-exchange-001 | WTI futures, storage spreads | — | CME delivery logistics Cushing | **proposed** |
| gl-exchange-024 | Brent benchmark | — | Dated Brent cargo assessments | **proposed** |
| gl-weather-002 | Gulf production shut-ins | — | US Gulf port closures | **proposed** |
| gl-shipping-012 | — | Panama transit fees/disruption | Canal queue / draft restrictions | **proposed** |
| gl-shipping-013 | — | Suez security incidents | Canal transit delays | **proposed** |
| gl-industry_body-001 | Weekly stats, refinery surveys | — | Pipeline/refinery ops standards | **proposed** |
| gl-shipping-008 | — | — | AIS vessel positions (commercial feed) | **proposed** (data_feed, not primary anchor alone) |
| gl-shipping-020 | Fleet utilization stats | — | Freight rate indices | **unverified** — commercial; Tier 2 playbook context only |
| gl-international_agency-039 | Conference papers | Producer dialogue | — | **unverified** — industry forum, not regulator |

---

### Unverified / Anti-patterns

| id | issue |
|----|-------|
| gl-international_agency-039 | APPEC — industry conference org, not data publisher; Tier 2 |
| gl-weather-015 | Colorado State — academic forecast, not operational NHC equivalent |
| gl-shipping-014 | Turkish straits VTS domain needs manual validation (uab.gov.tr) |
| gl-shipping-018 | Lloyd's Register — classification society, not flow data |
| gl-shipping-019 | MRCC domain uncertain — portofsingapore.com vs mpa.gov.sg overlap |
| gl-shipping-020 | Clarksons — commercial broker research; exclude from Tier 1 whitelist |
| gl-international_agency-040, gl-exchange-025 | Reserved empty slots — fill in crosscheck or country phase |

**Anti-patterns avoided:** Platts, Argus, Reuters, Bloomberg (secondary confirmation only).

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 1,
  "last_country": null,
  "crosscheck_cursor": 0,
  "last_batch_seq": 2
}
```

Po merge → **115 entries** v `catalog.json`.  
**Další dávka:** `composer-2-5_003_country_authority_SA.md` (Fáze 2, Saudi Arabia × 10 autorit).

### Whitelist kandidáti (po schválení, Tier 1 only)

Top 20 pro ruční validaci #29:  
`iea.org`, `eia.gov`, `opec.org`, `jodidata.org`, `energy.gov`, `treasury.gov`, `cmegroup.com`, `theice.com`, `ine.cn`, `noaa.gov`, `nhc.noaa.gov`, `ecmwf.int`, `imo.org`, `pancanal.com`, `suezcanal.gov.eg`, `mpa.gov.sg`, `portofrotterdam.com`, `api.org`, `ferc.gov`, `cer-rec.gc.ca`
