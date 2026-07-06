# Batch 076 — Geo Target: Panama Canal

## Geo significance
The **Panama Canal** handles ~5% of global trade — critically important for **US Gulf LNG exports** to Asia (replacing the Cape Horn alternative, saving ~8,000 nm) and **Pacific Basin crude movements** (Ecuador, Colombia → US/Asia; US SPR releases). Capacity: ~36–38 ships/day via new Neopanamax locks (2016). The **2023–2024 drought crisis** (Lake Gatún water levels) forced ACP to cut daily crossings to ~22–24 and require vessels to reduce draft/cargo — the first structural supply-chain disruption from climate (ENSO/El Niño). US LNG carriers received priority booking via transit reservations. The **Panama Canal Authority (ACP)** is the primary signal source for water levels, daily slot auctions, and crossing restrictions.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gt-panama-acp | PA | panama | chokepoint | Panama Canal Authority (ACP) | pancanal.com | international_agency | official | vessel_loading, port_closure, exports | proposed |
| gt-panama-marinetraffic | — | panama | chokepoint | MarineTraffic AIS — Panama Canal feed | marinetraffic.com | shipping | official | vessel_loading, exports | proposed |
| gt-panama-bimco | — | panama | chokepoint | BIMCO Panama Canal circulars | bimco.org | shipping | industry_body | vessel_loading, port_closure | proposed |
| gt-panama-noaa_enso | — | panama | chokepoint | NOAA ENSO monitor (El Niño/La Niña = lake level) | climate.gov | weather | official | force_majeure | proposed |
| gt-panama-vortexa | — | panama | chokepoint | Vortexa — Panama LNG/crude flow analytics | vortexa.com | shipping | official | exports, vessel_loading | proposed |
| gt-panama-kpler | — | panama | chokepoint | Kpler — Panama Canal throughput | kpler.com | shipping | official | exports, vessel_loading | proposed |
| gt-panama-colon_port | PA | panama | chokepoint | Colón Port (Atlantic entrance) | colonport.com | international_agency | official | vessel_loading, port_closure | unverified |
| gt-panama-balboa_port | PA | panama | chokepoint | Balboa Port (Pacific entrance) | portbalboa.com | international_agency | official | vessel_loading, port_closure | unverified |
| gt-panama-lloyds_cargo | — | panama | chokepoint | Lloyd's List Panama congestion index | lloydslist.com | shipping | official | vessel_loading, port_closure | proposed |
| gt-panama-fearnleys | — | panama | chokepoint | Fearnleys LNG freight rate monitor (Panama premium) | fearnleys.com | shipping | official | vessel_loading, exports | proposed |

## Cross-check (key entries)

### gt-panama-acp (Panama Canal Authority)
- **Supply:** ACP publishes daily water levels (Lake Gatún + Alajuela); slot auction clearing prices (drought = $2–4m premium slots for LNG); crossing restrictions by draft; throughput statistics by vessel class
- **Geopolitics:** Panama-China concession (Hutchison Ports Balboa/Cristóbal, politically contested 2025); US LNG export corridor dependency; ACP drought = structurally new climate risk
- **Logistics:** Neopanamax vs Panamax locks; LNG carrier slot priority (US DOE intervention 2024); reservation system auctions; transit time ~10–12h

### gt-panama-noaa_enso (NOAA ENSO)
- **Supply:** La Niña = above-normal Panama rainfall = normal canal ops; El Niño = drought = Lake Gatún low = slot restrictions = LNG premium
- **Geopolitics:** ENSO cycle 18–24 months = predictable risk window; 2023 was strongest El Niño in decades
- **Logistics:** Rolling seasonal forecast = early warning for 2025–2026 potential restrictions; freight rate forward curve impact

## Expansion slots
- gt-panama-xclude — Xclude (slot auction broker / transit reservation)
- gt-panama-acp_stats — ACP monthly traffic statistics (TEU + tanker + LNG/LPG breakdown)
- gt-panama-splash247_pc — Splash 247 Panama Canal coverage

## Anti-patterns
- Skip: Panamá América (local press, secondary)
- Skip: canalpanama.org (unofficial third-party site)
