# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_002_global_batch.md  
**Fáze:** global — krok batch (Fáze 1, celá globální vrstva, 1 dávka)  
**Datum:** 2026-07-04  

---

## Shrnutí

Globální vrstva (Dim 5): mezinárodní agentury, burzy, weather, shipping, industry bodies.
**62 obsazených slotů** z plánovaných 115 — zbytek zůstává `empty` (kvalita nad kvótou,
nedoplňuji halucinované domény). Většina Tier-1 institucí je vysoce ustálená → `proposed`;
komerční / re-brandované subjekty (DME, MarineTraffic, Equasis, KAPSARC) → `unverified`
k ověření domény přes `/source-discover`. Do `source_whitelist.json` nezapisuji.

Rozpad: international_agency 21, exchange 11, weather 11, shipping 9, industry_body 10.

---

### Navržené / aktualizované sloty

#### international_agency (21)

| id | entity | domain | category | type | signals | status |
|----|--------|--------|----------|------|---------|--------|
| gl-international_agency-001 | IEA | iea.org | international_agency | official | production, storage_levels, imports | proposed |
| gl-international_agency-002 | EIA | eia.gov | international_agency | official | production, storage_levels, exports | proposed |
| gl-international_agency-003 | OPEC | opec.org | international_agency | official | production, quota_rhetoric | proposed |
| gl-international_agency-004 | IEF | ief.org | international_agency | official | term_contract | proposed |
| gl-international_agency-005 | JODI | jodidata.org | international_agency | data_feed | production, exports, imports | proposed |
| gl-international_agency-006 | GECF | gecf.org | international_agency | official | production, exports | proposed |
| gl-international_agency-007 | IRENA | irena.org | international_agency | official | — | proposed |
| gl-international_agency-008 | IAEA | iaea.org | international_agency | official | sanctions | proposed |
| gl-international_agency-009 | IMF | imf.org | international_agency | official | pricing_formula | proposed |
| gl-international_agency-010 | World Bank (Pink Sheet) | worldbank.org | international_agency | data_feed | pricing_formula | proposed |
| gl-international_agency-011 | OECD | oecd.org | international_agency | official | — | proposed |
| gl-international_agency-012 | UN Comtrade | comtrade.un.org | international_agency | data_feed | exports, imports | proposed |
| gl-international_agency-013 | Eurostat (energy) | ec.europa.eu/eurostat | international_agency | data_feed | imports, storage_levels | proposed |
| gl-international_agency-014 | ACER | acer.europa.eu | international_agency | official | pricing_formula | proposed |
| gl-international_agency-015 | EU DG ENER | energy.ec.europa.eu | international_agency | official | sanctions, storage_levels | proposed |
| gl-international_agency-016 | US DOE (SPR office) | energy.gov | international_agency | official | storage_levels | proposed |
| gl-international_agency-017 | ENTSOG | entsog.eu | international_agency | data_feed | pipeline_outage, imports | proposed |
| gl-international_agency-018 | ENTSO-E | entsoe.eu | international_agency | data_feed | — | proposed |
| gl-international_agency-019 | GIE AGSI (EU gas storage) | agsi.gie.eu | international_agency | data_feed | storage_levels | proposed |
| gl-international_agency-020 | GIE ALSI (EU LNG) | alsi.gie.eu | international_agency | data_feed | storage_levels, imports | proposed |
| gl-international_agency-021 | KAPSARC | kapsarc.org | international_agency | official | — | unverified |

#### exchange (11)

| id | entity | domain | category | type | signals | status |
|----|--------|--------|----------|------|---------|--------|
| gl-exchange-001 | CME Group (WTI, Henry Hub) | cmegroup.com | exchange | official | pricing_formula, term_contract | proposed |
| gl-exchange-002 | ICE (Brent, TTF) | ice.com | exchange | official | pricing_formula, term_contract | proposed |
| gl-exchange-003 | Shanghai INE (crude) | ine.cn | exchange | official | pricing_formula | proposed |
| gl-exchange-004 | DME / Gulf Mercantile (Oman) | dubaimerc.com | exchange | official | pricing_formula | unverified |
| gl-exchange-005 | Shanghai Futures Exchange | shfe.com.cn | exchange | official | pricing_formula | proposed |
| gl-exchange-006 | Dalian Commodity Exchange | dce.com.cn | exchange | official | pricing_formula | proposed |
| gl-exchange-007 | Zhengzhou Commodity Exchange | czce.com.cn | exchange | official | pricing_formula | proposed |
| gl-exchange-008 | EEX (EU gas / power / EUA) | eex.com | exchange | official | pricing_formula | proposed |
| gl-exchange-009 | JPX / TOCOM | jpx.co.jp | exchange | official | pricing_formula | proposed |
| gl-exchange-010 | MCX India | mcxindia.com | exchange | official | pricing_formula | proposed |
| gl-exchange-011 | Nasdaq Commodities | nasdaq.com | exchange | official | pricing_formula | proposed |

#### weather (11)

| id | entity | domain | category | type | signals | status |
|----|--------|--------|----------|------|---------|--------|
| gl-weather-001 | NOAA | noaa.gov | weather | official | hurricane, storage_levels | proposed |
| gl-weather-002 | National Hurricane Center | nhc.noaa.gov | weather | official | hurricane | proposed |
| gl-weather-003 | US National Weather Service | weather.gov | weather | official | hurricane | proposed |
| gl-weather-004 | NOAA Climate Prediction Center | cpc.ncep.noaa.gov | weather | official | storage_levels | proposed |
| gl-weather-005 | ECMWF | ecmwf.int | weather | official | hurricane | proposed |
| gl-weather-006 | UK Met Office | metoffice.gov.uk | weather | official | — | proposed |
| gl-weather-007 | JMA (Japan) | jma.go.jp | weather | official | hurricane | proposed |
| gl-weather-008 | China Meteorological Admin | cma.gov.cn | weather | official | — | proposed |
| gl-weather-009 | EUMETSAT | eumetsat.int | weather | official | — | proposed |
| gl-weather-010 | Copernicus Climate | climate.copernicus.eu | weather | data_feed | — | proposed |
| gl-weather-011 | WMO | wmo.int | weather | official | — | proposed |

#### shipping (9)

| id | entity | domain | category | type | signals | status |
|----|--------|--------|----------|------|---------|--------|
| gl-shipping-001 | IMO | imo.org | shipping | official | port_closure | proposed |
| gl-shipping-002 | UNCTAD (maritime) | unctad.org | shipping | official | — | proposed |
| gl-shipping-003 | Baltic Exchange (freight) | balticexchange.com | shipping | official | vessel_loading | proposed |
| gl-shipping-004 | EMSA | emsa.europa.eu | shipping | official | — | proposed |
| gl-shipping-005 | Suez Canal Authority | suezcanal.gov.eg | shipping | official | port_closure, vessel_loading | proposed |
| gl-shipping-006 | Panama Canal Authority | pancanal.com | shipping | official | port_closure | proposed |
| gl-shipping-007 | USCG NAVCEN | navcen.uscg.gov | shipping | official | port_closure | proposed |
| gl-shipping-008 | Equasis | equasis.org | shipping | data_feed | — | unverified |
| gl-shipping-009 | MarineTraffic | marinetraffic.com | shipping | data_feed | vessel_loading | unverified |

#### industry_body (10)

| id | entity | domain | category | type | signals | status |
|----|--------|--------|----------|------|---------|--------|
| gl-industry_body-001 | API (weekly inventory) | api.org | industry_body | official | storage_levels | proposed |
| gl-industry_body-002 | IGU | igu.org | industry_body | official | — | proposed |
| gl-industry_body-003 | IOGP | iogp.org | industry_body | official | production | proposed |
| gl-industry_body-004 | IPIECA | ipieca.org | industry_body | official | — | proposed |
| gl-industry_body-005 | GIIGNL (LNG importers) | giignl.org | industry_body | official | imports | proposed |
| gl-industry_body-006 | INTERTANKO | intertanko.com | industry_body | official | force_majeure | proposed |
| gl-industry_body-007 | BIMCO | bimco.org | industry_body | official | — | proposed |
| gl-industry_body-008 | OCIMF (war risk / tanker) | ocimf.org | industry_body | official | force_majeure, port_closure | proposed |
| gl-industry_body-009 | Concawe (EU refining) | concawe.eu | industry_body | official | refinery_outage | proposed |
| gl-industry_body-010 | Eurogas | eurogas.org | industry_body | official | imports | proposed |

---

### Cross-check (3 perspektivy — reprezentativní vzorek)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gl-international_agency-001 (IEA) | OMR: produkce, poptávka, OECD zásoby | koordinace emergency stock release | — | proposed |
| gl-international_agency-002 (EIA) | WPSR týdenní zásoby, produkce | US SPR politika | — | proposed |
| gl-international_agency-003 (OPEC) | MOMR produkce, compliance | quota rétorika, OPEC+ jednání | — | proposed |
| gl-international_agency-019 (AGSI) | — | EU gas security policy | fill-level EU skladů real-time | proposed |
| gl-exchange-002 (ICE) | — | — | Brent/TTF benchmark, contract specs | proposed |
| gl-exchange-004 (DME) | — | — | Oman crude benchmark (Asie) | unverified — re-brand na Gulf Mercantile, ověřit doménu |
| gl-weather-002 (NHC) | shut-in produkce Gulf | — | hurricane track → port/rig closure | proposed |
| gl-shipping-005 (Suez CA) | — | tranzitní riziko, poplatky | denní tranzit, blokace | proposed |
| gl-shipping-009 (MarineTraffic) | — | — | AIS vessel tracking — komerční | unverified — data_feed, ne primární oficiální |
| gl-industry_body-001 (API) | týdenní inventory (předběžný před EIA) | — | — | proposed |

---

### Unverified / Anti-patterns

**Unverified (nutná validace domény přes `/source-discover`):**
- `gl-exchange-004` DME — burza prošla re-brandem (Dubai Mercantile → Gulf Mercantile Exchange); `dubaimerc.com` ověřit vs. nová doména.
- `gl-shipping-008` Equasis, `gl-shipping-009` MarineTraffic — přístup/komerční model; `data_feed`, ne primární oficiální zdroj.
- `gl-international_agency-021` KAPSARC — saudský think-tank, semi-oficiální; užitečný kontext, ne autorita.

**Vědomě vynecháno (anti-pattern — nepatří do global whitelistu jako „primary“):**
- Platts / Argus / OPIS (PRA) — komerční price reporting, sekundární; případně jako `data_feed` po desk rozhodnutí, ne teď.
- Reuters / Bloomberg / Lloyd's List — sekundární potvrzení, ne primární.
- Národní regulátoři (FERC, národní port authorities) — patří do Fáze 2 (country_authority) / Fáze 3 (geo_target), ne do global.

**Nezaplněno:** 62/115 plánovaných global slotů. Zbývajících 53 ponecháno `empty` —
nedoplňuji kvótu halucinovanými doménami.

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

Po merge → **další dávka:** `claude-opus-4-8_003_country_authority_SA.md`
(Fáze 2, první země `SA` = Saudi Arabia: 10 slotů autorit — ministry, Aramco, MFA,
customs, upstream regulator, ports, exchange, central bank, env, coast guard).
