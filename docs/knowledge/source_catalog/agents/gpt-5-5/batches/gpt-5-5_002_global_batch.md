# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_002_global_batch.md  
**Fáze:** global — krok core (Fáze 1, core global sources)  
**Datum:** 2026-07-04  

---

## Shrnutí

Druhá dávka po merge skeletonu: core globální zdroje, které senior energy desk typicky sleduje před sekundárními headline službami.
Dávka navrhuje 46 ověřitelných slotů napříč `international_agency`, `exchange`, `weather`, `shipping` a `industry_body`.

Do `source_whitelist.json` zatím nezapisovat; po review lze schválené položky mergovat do `catalog.json` a následně připravit whitelist batch.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gl-international_agency-001 | — | — | international_agency | International Energy Agency (IEA) | iea.org | international_agency | data_feed | production, exports, imports, storage_levels, pricing_formula | proposed |
| gl-international_agency-002 | US | — | international_agency | U.S. Energy Information Administration (EIA) | eia.gov | international_agency | data_feed | production, exports, imports, storage_levels, refinery_outage | proposed |
| gl-international_agency-003 | — | — | international_agency | OPEC | opec.org | international_agency | official | production, quota_rhetoric, exports | proposed |
| gl-international_agency-004 | — | — | international_agency | Joint Organisations Data Initiative (JODI) | jodidata.org | international_agency | data_feed | production, exports, imports, storage_levels | proposed |
| gl-international_agency-005 | — | — | international_agency | International Energy Forum (IEF) | ief.org | international_agency | official | production, quota_rhetoric, term_contract | proposed |
| gl-international_agency-006 | — | — | international_agency | Gas Exporting Countries Forum (GECF) | gecf.org | international_agency | official | production, exports, quota_rhetoric, term_contract | proposed |
| gl-international_agency-007 | — | — | international_agency | International Renewable Energy Agency (IRENA) | irena.org | international_agency | official | production, imports, pricing_formula | proposed |
| gl-international_agency-008 | — | — | international_agency | OECD Data / Energy Statistics | oecd.org | international_agency | data_feed | imports, production, storage_levels | proposed |
| gl-international_agency-009 | — | — | international_agency | Eurostat Energy Statistics | ec.europa.eu | international_agency | data_feed | production, imports, storage_levels | proposed |
| gl-international_agency-010 | — | — | international_agency | World Bank Commodity Markets | worldbank.org | international_agency | data_feed | pricing_formula, imports, exports | proposed |
| gl-international_agency-011 | — | — | international_agency | IMF Data / Commodity and macro surveillance | imf.org | international_agency | data_feed | pricing_formula, sanctions | proposed |
| gl-international_agency-012 | — | — | international_agency | UN Comtrade | comtradeplus.un.org | international_agency | data_feed | exports, imports | proposed |
| gl-international_agency-013 | — | — | international_agency | World Trade Organization (WTO) | wto.org | international_agency | official | export_license, sanctions, imports, exports | proposed |
| gl-international_agency-014 | — | — | international_agency | International Atomic Energy Agency (IAEA) | iaea.org | international_agency | official | sanctions, force_majeure | proposed |
| gl-exchange-001 | US | — | exchange | CME Group | cmegroup.com | exchange | data_feed | pricing_formula, storage_levels | proposed |
| gl-exchange-002 | GB | — | exchange | ICE | ice.com | exchange | data_feed | pricing_formula | proposed |
| gl-exchange-003 | CN | — | exchange | Shanghai International Energy Exchange (INE) | ine.cn | exchange | data_feed | pricing_formula, imports | proposed |
| gl-exchange-004 | CN | — | exchange | Shanghai Futures Exchange (SHFE) | shfe.com.cn | exchange | data_feed | pricing_formula, storage_levels | proposed |
| gl-exchange-005 | SG | — | exchange | Singapore Exchange (SGX) | sgx.com | exchange | data_feed | pricing_formula | proposed |
| gl-exchange-006 | JP | — | exchange | Japan Exchange Group (JPX) | jpx.co.jp | exchange | data_feed | pricing_formula | proposed |
| gl-exchange-007 | DE | — | exchange | European Energy Exchange (EEX) | eex.com | exchange | data_feed | pricing_formula, storage_levels | proposed |
| gl-exchange-008 | AE | — | exchange | Dubai Mercantile Exchange (DME) | dubaimerc.com | exchange | data_feed | pricing_formula | proposed |
| gl-weather-001 | US | — | weather | National Oceanic and Atmospheric Administration (NOAA) | noaa.gov | weather | data_feed | hurricane, refinery_outage, port_closure | proposed |
| gl-weather-002 | US | — | weather | National Hurricane Center (NHC) | nhc.noaa.gov | weather | data_feed | hurricane, port_closure, refinery_outage | proposed |
| gl-weather-003 | — | — | weather | ECMWF | ecmwf.int | weather | data_feed | hurricane, production, imports | proposed |
| gl-weather-004 | — | — | weather | World Meteorological Organization (WMO) | wmo.int | weather | official | hurricane, production, imports | proposed |
| gl-weather-005 | — | — | weather | EUMETSAT | eumetsat.int | weather | data_feed | hurricane, port_closure | proposed |
| gl-weather-006 | GB | — | weather | UK Met Office | metoffice.gov.uk | weather | data_feed | hurricane, production, imports | proposed |
| gl-weather-007 | JP | — | weather | Japan Meteorological Agency (JMA) | jma.go.jp | weather | data_feed | hurricane, port_closure | proposed |
| gl-weather-008 | AU | — | weather | Australian Bureau of Meteorology (BoM) | bom.gov.au | weather | data_feed | hurricane, port_closure, production | proposed |
| gl-shipping-001 | — | — | shipping | International Maritime Organization (IMO) | imo.org | shipping | official | vessel_loading, port_closure, sanctions | proposed |
| gl-shipping-002 | EG | suez | shipping | Suez Canal Authority | suezcanal.gov.eg | shipping | official | vessel_loading, port_closure | proposed |
| gl-shipping-003 | — | panama | shipping | Panama Canal Authority | pancanal.com | shipping | official | vessel_loading, port_closure | proposed |
| gl-shipping-004 | SG | singapore | shipping | Maritime and Port Authority of Singapore (MPA) | mpa.gov.sg | shipping | official | vessel_loading, port_closure | proposed |
| gl-shipping-005 | NL | rotterdam | shipping | Port of Rotterdam Authority | portofrotterdam.com | shipping | official | vessel_loading, port_closure, storage_levels | proposed |
| gl-shipping-006 | US | — | shipping | U.S. Coast Guard Navigation Center | navcen.uscg.gov | shipping | official | port_closure, vessel_loading | proposed |
| gl-shipping-007 | — | — | shipping | MarineTraffic | marinetraffic.com | shipping | data_feed | vessel_loading, port_closure | proposed |
| gl-shipping-008 | — | — | shipping | Equasis | equasis.org | shipping | data_feed | vessel_loading | proposed |
| gl-industry_body-001 | US | — | industry_body | American Petroleum Institute (API) | api.org | industry_body | official | storage_levels, production, refinery_outage | proposed |
| gl-industry_body-002 | — | — | industry_body | International Association of Oil & Gas Producers (IOGP) | iogp.org | industry_body | official | production, force_majeure | proposed |
| gl-industry_body-003 | — | — | industry_body | International Gas Union (IGU) | igu.org | industry_body | official | production, exports, term_contract | proposed |
| gl-industry_body-004 | — | — | industry_body | GIIGNL | giignl.org | industry_body | official | exports, imports, term_contract | proposed |
| gl-industry_body-005 | — | — | industry_body | Oil Companies International Marine Forum (OCIMF) | ocimf.org | industry_body | official | vessel_loading, port_closure | proposed |
| gl-industry_body-006 | — | — | industry_body | INTERTANKO | intertanko.com | industry_body | official | vessel_loading, sanctions | proposed |
| gl-industry_body-007 | — | — | industry_body | SIGTTO | sigtto.org | industry_body | official | vessel_loading, exports, imports | proposed |
| gl-industry_body-008 | GB | — | industry_body | Energy Institute | energyinst.org | industry_body | official | production, storage_levels, pricing_formula | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gl-international_agency-001 | Core balances, oil market reports, demand/supply baselines. | Used for policy framing and emergency stock context. | Indirect, supports flow interpretation. | proposed |
| gl-international_agency-002 | Weekly US stocks, refinery runs, production, imports/exports. | US policy relevance via federal data. | Strong US logistics proxy through PADD and storage data. | proposed |
| gl-international_agency-003 | Producer policy and monthly production framing. | Direct OPEC+ rhetoric and quota signal. | Export/logistics mostly indirect. | proposed |
| gl-international_agency-004 | Country-submitted oil/gas balances. | Neutral data chain, useful for dispute checks. | Trade-flow validation. | proposed |
| gl-exchange-001 | Futures/options and storage-linked benchmark signals. | Policy impact expressed through price/volatility. | Cushing and refined product contracts relevant. | proposed |
| gl-exchange-002 | Brent, gasoil, TTF/JCC-linked derivatives. | Sanctions and war-risk price expression. | Seaborne benchmark linkage. | proposed |
| gl-weather-001 | Gulf of Mexico and US production/refinery disruption. | Emergency advisories affect federal response. | Strong port/refinery disruption signal. | proposed |
| gl-weather-002 | Hurricane-specific production/refining risk. | Evacuation and emergency context. | Direct port and offshore disruption signal. | proposed |
| gl-shipping-002 | Canal transit affects crude/products/LNG voyage times. | Sovereign canal authority; disruption can become diplomatic. | Direct chokepoint throughput signal. | proposed |
| gl-shipping-003 | Canal draft/transit restrictions affect flows. | Sovereign infrastructure policy. | Direct chokepoint queue/allocation signal. | proposed |
| gl-shipping-007 | AIS-derived vessel position and loading inference. | Not sovereign; use as data corroboration. | Strong logistics signal, not whitelist as official-only source without review. | proposed |
| gl-industry_body-001 | US inventory and petroleum statistics context. | Domestic industry stance on policy. | Refinery and stocks context. | proposed |
| gl-industry_body-004 | LNG trade and term-flow context. | Contract structure and importer/exporter alignment. | LNG cargo and receiving-market context. | proposed |

Rows not individually expanded above follow the same rule: `proposed` only where supply/geopolitics/logistics perspectives agree that the source is official, institutional, or a desk-useful structured data feed.

---

### Unverified / Anti-patterns

- `MarineTraffic` is a commercial AIS feed, not an official authority; keep as `data_feed` and do not treat as sovereign confirmation.
- `IMF`, `World Bank`, `WTO`, `IRENA`, and `IAEA` are macro/policy context sources; include in global catalog, but do not over-prioritize for intraday crude/LNG flow alerts.
- `noaa.gov` and `nhc.noaa.gov` intentionally coexist because NHC is the faster hurricane-operational path; dedupe policy should be entity + domain, not root domain only.
- Do not add secondary news providers, broker blogs, or SEO commodity summaries as global primary slots.

---

### Progress po merge (návrh)

```json
{
  "phase": "global",
  "phase_index": 46,
  "last_country": null,
  "crosscheck_cursor": 0,
  "last_batch_seq": 2
}
```

Po merge této dávky → **další dávka:** pokračovat v `global` expanzi zbývajících plánovaných slotů, nebo po desk review uzavřít global core a přejít na `country_authority` pro `SA`.
