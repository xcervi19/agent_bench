# Batch 081 — Geo Target: Fujairah

## Geo significance
**Fujairah** (UAE, East Coast, Gulf of Oman) is the **world's second-largest bunkering hub** (~8–9m tonnes/y) and a critical **crude/product storage and blending hub** (~14m barrels capacity) outside the Strait of Hormuz. It is strategically vital as an **alternative export route** — the Abu Dhabi Crude Oil Pipeline (ADCOP, 1.5 mb/d) connects ADNOC's onshore fields directly to Fujairah, bypassing Hormuz. Fujairah's **oil tank farms** host strategic reserves for UAE + 3rd-party storage. The **Fujairah Bunkering** market is a real-time proxy for Arabian Gulf shipping demand and fuel switching. **FOIZ** (Fujairah Oil Industry Zone) stores up to 25+ products simultaneously. Fujairah data (fuel oil inventory, crude storage, vessel calls) is published weekly by S&P Global / Emirates Data Clearing House (EDSCA).

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gt-fujairah-edsca | AE | fujairah | load_port | EDSCA – Emirates Data Clearing House Association (weekly stocks) | edsca.ae | industry_body | official | storage_levels, exports, vessel_loading | proposed |
| gt-fujairah-adcop | AE | fujairah | load_port | ADNOC – ADCOP pipeline (Abu Dhabi → Fujairah bypass) | adnoc.ae | company | official | exports, pipeline_flow | proposed |
| gt-fujairah-marinetraffic | — | fujairah | load_port | MarineTraffic AIS — Fujairah anchorage feed | marinetraffic.com | shipping | official | vessel_loading, exports | proposed |
| gt-fujairah-vortexa | — | fujairah | load_port | Vortexa — Fujairah crude/products loading | vortexa.com | shipping | official | exports, vessel_loading | proposed |
| gt-fujairah-kpler | — | fujairah | load_port | Kpler — Fujairah storage + export tracking | kpler.com | shipping | official | exports, vessel_loading, storage_levels | proposed |
| gt-fujairah-platts_bunker | — | fujairah | load_port | S&P Global Platts – Fujairah bunker price assessment | spglobal.com | industry_body | official | pricing_formula, vessel_loading | proposed |
| gt-fujairah-port_authority | AE | fujairah | load_port | Fujairah Port Authority | fujairahport.ae | international_agency | official | vessel_loading, port_closure | proposed |
| gt-fujairah-ukmto | — | fujairah | load_port | UKMTO – Gulf of Oman advisories | ukmto.org | shipping | official | force_majeure, port_closure | proposed |
| gt-fujairah-foiz | AE | fujairah | load_port | FOIZ – Fujairah Oil Industry Zone | foiz.gov.ae | international_agency | official | storage_levels, exports | proposed |
| gt-fujairah-lloyds_bunker | — | fujairah | load_port | Lloyd's List – Fujairah bunker market report | lloydslist.com | shipping | official | pricing_formula, vessel_loading | proposed |

## Cross-check

### gt-fujairah-edsca (EDSCA weekly stocks)
- **Supply:** EDSCA publishes weekly Fujairah oil product inventory (light distillates, middle distillates, fuel oils); primary market-moving data point for Gulf product storage; drawdown = regional supply tightness signal
- **Geopolitics:** Fujairah = outside Hormuz = strategic reserve value; ADNOC uses Fujairah as bypass during Hormuz tension; Iran tanker attacks in Gulf of Oman (2019) = Fujairah anchorage risk
- **Logistics:** ~14m bbl storage capacity; ADCOP 1.5 mb/d inflow; ship-to-ship transfers in anchorage; VLCC + Suezmax mix

### gt-fujairah-adcop (ADNOC ADCOP)
- **Supply:** ADCOP (Abu Dhabi Crude Oil Pipeline) 1.5 mb/d capacity; flows Abu Dhabi crude to Fujairah export terminal; bypass = Hormuz-proof Saudi Arabia analog (Ras Tanura → ADCOP+Fujairah switch during crisis)
- **Geopolitics:** UAE strategic decision to expand ADCOP = hedging Hormuz risk; Iran-UAE maritime tension; ADNOC pipeline utilization rate = UAE export strategy signal
- **Logistics:** Fujairah Marine Terminal crude export berths; VLCC Fujairah loading (Arab Extra Light); pipeline injection point at Habshan

## Expansion slots
- gt-fujairah-argus_bunker — Argus Media Fujairah bunker prices
- gt-fujairah-iea_stocks — IEA monthly oil stocks (Fujairah as ME proxy)
- gt-fujairah-fujairah_oil — Fujairah Oil (FO) — spot price assessment

## Anti-patterns
- Skip: Fujairah24.ae (local news, not energy data)
- Skip: fujairahoil.com (commercial broker)
