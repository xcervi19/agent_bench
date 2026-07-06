# Batch 090 — Geo Target: LOOP (Louisiana Offshore Oil Port)

## Geo significance
**LOOP** (Louisiana Offshore Oil Port, ~30 miles offshore Port Fourchon, Louisiana) is the **only US deepwater crude import/export terminal** capable of handling **VLCCs** — the only facility in the Western Hemisphere that can fully offload fully-laden supertankers. Capacity ~1.3 mb/d throughput; connected to Clovelly storage hub (80+ mb cavern storage). Since the US shale revolution and crude export liberalization (2015), LOOP has pivoted from predominantly imports to mixed import/export. LOOP is also a **strategic petroleum reserve** (SPR) connection point (Bayou Choctaw SPR). Hurricane season (Jun–Nov) is the primary risk: LOOP suspended operations during Katrina (2005), Ida (2021). LOOP feeds the **Capline pipeline** (northbound to Midwest) and receives offshore deepwater Gulf production (Mars, Thunder Horse, Olympus fields).

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gt-loop-loop_llc | US | loop | us_gulf_hub | LOOP LLC – Louisiana Offshore Oil Port | loopllc.com | company | official | vessel_loading, imports, exports, storage_levels | proposed |
| gt-loop-marinetraffic | — | loop | us_gulf_hub | MarineTraffic AIS — LOOP SPM / Gulf of Mexico feed | marinetraffic.com | shipping | official | vessel_loading, exports | proposed |
| gt-loop-vortexa | — | loop | us_gulf_hub | Vortexa — LOOP crude flow analytics | vortexa.com | shipping | official | exports, imports, vessel_loading | proposed |
| gt-loop-kpler | — | loop | us_gulf_hub | Kpler — LOOP import/export tracking | kpler.com | shipping | official | exports, imports, vessel_loading | proposed |
| gt-loop-eia_weekly | US | loop | us_gulf_hub | EIA Weekly Petroleum Status Report (LOOP/Clovelly) | eia.gov | international_agency | official | storage_levels, imports, exports | proposed |
| gt-loop-noaa_hurricane | — | loop | us_gulf_hub | NOAA National Hurricane Center (Gulf of Mexico) | nhc.noaa.gov | weather | official | force_majeure, port_closure | proposed |
| gt-loop-capline | US | loop | us_gulf_hub | Capline Pipeline (LOOP → Midwest crude) | — | company | official | pipeline_flow, exports | unverified |
| gt-loop-bsee | US | loop | us_gulf_hub | BSEE – Bureau of Safety and Environmental Enforcement | bsee.gov | international_agency | official | production, force_majeure | proposed |
| gt-loop-platts_mars | — | loop | us_gulf_hub | S&P Global Platts – Mars crude assessment (LOOP-linked) | spglobal.com | industry_body | official | pricing_formula, production | proposed |
| gt-loop-doe_spr | US | loop | us_gulf_hub | DOE Strategic Petroleum Reserve (Bayou Choctaw) | energy.gov | international_agency | official | storage_levels, exports | proposed |

## Cross-check

### gt-loop-loop_llc (LOOP LLC)
- **Supply:** LOOP handles ~1.3 mb/d; pivoted post-2015 to mixed import/export; VLCC-capable (only US facility); hurricane evacuation notice = Gulf of Mexico production + LOOP suspension; SPM mooring failure = loading halt
- **Geopolitics:** LOOP = US export capacity signal; crude export policy (DOE authorization); SPR release routing (Bayou Choctaw → LOOP reverse); Gulf of Mexico federal lease moratorium risk
- **Logistics:** 3 SPMs + Clovelly dome storage; Capline northbound + LOCAP southbound pipelines; offshore deepwater connection (Mars, Thunder Horse, Olympus, Jack/St. Malo)

### gt-loop-noaa_hurricane (NHC)
- **Supply:** Gulf of Mexico hurricane = LOOP + Gulf production suspension; Katrina 2005 closed LOOP 6 weeks; Ida 2021 = ~30 mb/d GOM production shut-in; NHC 5-day track = early warning for trader hedging
- **Geopolitics:** US Gulf energy infrastructure vulnerability = strategic asset; SPR release can partially offset hurricane shut-in
- **Logistics:** LOOP offshore location = direct storm path exposure; port fourchon (onshore support base) also Hurricane vulnerable

## Expansion slots
- gt-loop-bsee_incidents — BSEE Gulf of Mexico hurricane production shut-in reports
- gt-loop-port_fourchon — Port Fourchon authority (onshore LOOP support base)
- gt-loop-argus_mars — Argus Media Mars crude differential

## Anti-patterns
- Skip: oilprice.com LOOP commentary (secondary)
- Skip: theadvocate.com Louisiana energy coverage (local press)
