# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_003_global_expansion.md  
**Fáze:** global — krok expansion (Fáze 1, druhá globální dávka)  
**Datum:** 2026-07-04  

---

## Shrnutí

Třetí dávka rozšiřuje globální vrstvu o dalších 34 slotů po merge core batch `gpt-5-5_002_global_batch.md`.
Priorita: zdroje s přímou cenotvornou nebo logistickou použitelností pro energy desk — další burzy, národní meteorologické služby pro produkční a portovní rizika, oficiální porty / canal / maritime zdroje a industry bodies.

Do `source_whitelist.json` zatím nezapisovat; tato dávka čeká na review a případný merge do `catalog.json`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gl-exchange-009 | RU | — | exchange | Moscow Exchange (MOEX) | moex.com | exchange | data_feed | pricing_formula, sanctions | proposed |
| gl-exchange-010 | IN | — | exchange | Multi Commodity Exchange of India (MCX) | mcxindia.com | exchange | data_feed | pricing_formula, imports | proposed |
| gl-exchange-011 | TR | — | exchange | Borsa Istanbul | borsaistanbul.com | exchange | data_feed | pricing_formula, imports | proposed |
| gl-exchange-012 | NL | — | exchange | ICE Endex | iceendex.com | exchange | data_feed | pricing_formula, storage_levels | proposed |
| gl-exchange-013 | NO | — | exchange | Nord Pool | nordpoolgroup.com | exchange | data_feed | pricing_formula, imports | proposed |
| gl-exchange-014 | US | — | exchange | Nodal Exchange | nodalexchange.com | exchange | data_feed | pricing_formula | proposed |
| gl-exchange-015 | CN | — | exchange | Zhengzhou Commodity Exchange (ZCE) | czce.com.cn | exchange | data_feed | pricing_formula, imports | proposed |
| gl-exchange-016 | CN | — | exchange | Dalian Commodity Exchange (DCE) | dce.com.cn | exchange | data_feed | pricing_formula, imports | proposed |
| gl-weather-009 | CA | — | weather | Environment and Climate Change Canada | canada.ca | weather | data_feed | hurricane, production, port_closure | proposed |
| gl-weather-010 | FR | — | weather | Meteo-France | meteofrance.fr | weather | data_feed | hurricane, imports, port_closure | proposed |
| gl-weather-011 | DE | — | weather | Deutscher Wetterdienst (DWD) | dwd.de | weather | data_feed | imports, storage_levels, port_closure | proposed |
| gl-weather-012 | IN | — | weather | India Meteorological Department (IMD) | imd.gov.in | weather | data_feed | hurricane, imports, port_closure | proposed |
| gl-weather-013 | CN | — | weather | China Meteorological Administration (CMA) | cma.gov.cn | weather | data_feed | hurricane, imports, port_closure | proposed |
| gl-weather-014 | SA | — | weather | Saudi National Center for Meteorology | ncm.gov.sa | weather | data_feed | production, port_closure | proposed |
| gl-weather-015 | KR | — | weather | Korea Meteorological Administration (KMA) | kma.go.kr | weather | data_feed | hurricane, imports, port_closure | proposed |
| gl-weather-016 | SG | singapore | weather | Meteorological Service Singapore | weather.gov.sg | weather | data_feed | port_closure, imports | proposed |
| gl-shipping-009 | AE | fujairah | shipping | Port of Fujairah | fujairahport.ae | shipping | official | vessel_loading, port_closure, storage_levels | proposed |
| gl-shipping-010 | AE | jebel_ali | shipping | DP World UAE Region | dpworld.com | shipping | official | vessel_loading, port_closure | proposed |
| gl-shipping-011 | SA | ras_tanura | shipping | Saudi Ports Authority (Mawani) | mawani.gov.sa | shipping | official | vessel_loading, port_closure | proposed |
| gl-shipping-012 | US | houston_ship_channel | shipping | Port Houston | porthouston.com | shipping | official | vessel_loading, port_closure, refinery_outage | proposed |
| gl-shipping-013 | US | corpus_christi | shipping | Port of Corpus Christi | portofcc.com | shipping | official | vessel_loading, port_closure, exports | proposed |
| gl-shipping-014 | US | loop | shipping | LOOP LLC | loopllc.com | shipping | official | vessel_loading, storage_levels, exports | proposed |
| gl-shipping-015 | GB | — | shipping | UK Maritime and Coastguard Agency | gov.uk | shipping | official | vessel_loading, port_closure, sanctions | proposed |
| gl-shipping-016 | — | — | shipping | International Chamber of Shipping (ICS) | ics-shipping.org | shipping | official | vessel_loading, sanctions | proposed |
| gl-shipping-017 | — | — | shipping | BIMCO | bimco.org | shipping | official | vessel_loading, sanctions, term_contract | proposed |
| gl-shipping-018 | — | — | shipping | Paris MoU on Port State Control | parismou.org | shipping | official | vessel_loading, sanctions | proposed |
| gl-industry_body-009 | — | — | industry_body | WPC Energy | wpcenergy.org | industry_body | official | production, quota_rhetoric | proposed |
| gl-industry_body-010 | US | — | industry_body | Independent Petroleum Association of America (IPAA) | ipaa.org | industry_body | official | production, quota_rhetoric | proposed |
| gl-industry_body-011 | CA | — | industry_body | Canadian Association of Petroleum Producers (CAPP) | capp.ca | industry_body | official | production, exports, pipeline_outage | proposed |
| gl-industry_body-012 | GB | — | industry_body | Offshore Energies UK (OEUK) | oeuk.org.uk | industry_body | official | production, force_majeure | proposed |
| gl-industry_body-013 | NO | — | industry_body | Offshore Norge | offshorenorge.no | industry_body | official | production, force_majeure | proposed |
| gl-industry_body-014 | — | — | industry_body | FuelsEurope | fuelseurope.eu | industry_body | official | refinery_outage, imports, pricing_formula | proposed |
| gl-industry_body-015 | — | — | industry_body | Eurogas | eurogas.org | industry_body | official | imports, storage_levels, term_contract | proposed |
| gl-industry_body-016 | US | — | industry_body | Interstate Natural Gas Association of America (INGAA) | ingaa.org | industry_body | official | pipeline_outage, imports | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| gl-exchange-009 | Russian exchange prices and market functioning context. | Sanctions-sensitive venue; useful for market-access checks. | Logistics indirect. | proposed |
| gl-exchange-010 | India commodity pricing and hedging context. | Importer policy and domestic price sensitivity. | Indirect import-demand signal. | proposed |
| gl-exchange-012 | European gas/power benchmark infrastructure. | EU market stress and policy intervention signal. | Storage and gas hub relevance. | proposed |
| gl-weather-009 | Canadian wildfire, winter and offshore weather risks. | Emergency response and federal advisories. | Port and production disruption relevance. | proposed |
| gl-weather-012 | Monsoon/cyclone risk for Indian ports and demand. | Official national source. | Strong import-terminal disruption path. | proposed |
| gl-shipping-009 | Fujairah oil product and bunker hub operations. | UAE infrastructure policy relevance. | Direct port, storage and loading signal. | proposed |
| gl-shipping-011 | Saudi port authority for Red Sea / Gulf logistics. | Sovereign infrastructure source. | Direct loading/closure signal. | proposed |
| gl-shipping-014 | US offshore crude terminal throughput and storage. | US export infrastructure relevance. | Direct LOOP loading/storage signal. | proposed |
| gl-industry_body-011 | Canadian upstream production and export context. | Pipeline/regulatory advocacy signal. | Export and pipeline bottleneck relevance. | proposed |
| gl-industry_body-013 | Norway offshore industry source for production-impacting labor and policy events. | Relevant to North Sea production policy. | Indirect but useful for outage/strike context. | proposed |

Rows not individually expanded above follow the same rule: `proposed` only where the source is institutionally identifiable and has a direct supply, logistics, pricing, or policy use case.

---

### Unverified / Anti-patterns

- `gl-industry_body-013` domain was checked as `offshorenorge.no`; still validate the specific publication path before whitelist use.
- `gov.uk` is a broad root domain for the UK Maritime and Coastguard Agency; acceptable in catalog, but whitelist entry should use the most stable agency page or GOV.UK organisation path if the whitelist supports paths.
- `dpworld.com` is a global operator domain, not a sovereign authority; keep as `official` operator source, not government confirmation.
- Avoid treating industry bodies as first confirmation for outages or force majeure unless the signal is operational and traceable to members or official releases.

---

### Progress po merge (návrh)

```json
{
  "phase": "global",
  "phase_index": 80,
  "last_country": null,
  "crosscheck_cursor": 0,
  "last_batch_seq": 3
}
```

Po merge této dávky → **další dávka:** buď poslední `global` top-up směrem k plánovaným 115 slotům, nebo uzavřít globální core/expansion a přejít na `country_authority` pro `SA`.
