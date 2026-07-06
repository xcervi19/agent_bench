# Batch 091 — Geo Target: Houston Ship Channel

## Geo significance
The **Houston Ship Channel (HSC)** is the **world's largest petrochemical complex corridor** — a 52-mile channel from the Gulf of Mexico to the Port of Houston, handling ~250 mt/y cargo. It is the primary US crude export hub (WTI Houston = benchmark for US export grades), the heart of US **LPG/NGL export infrastructure** (Enterprise, Energy Transfer), and a major refined products corridor. Key terminals: **Enterprise Crude Oil LLC** (Echo pipeline + VLCC-capable terminal at Texas City/Battleground), **Oiltanking Partners**, **Magellan Midstream** (Houston distribution hub), **Kinder Morgan** (product pipelines). HSC is vulnerable to **fog closures** (~30+ days/year), **hurricanes** (Harvey 2017 = $125bn damage, ~30 days closure), and **industrial incidents** (petrochemical fires = regular occurrence). USCG Sector Houston/Galveston manages vessel traffic.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gt-houston-uscg_sector | US | houston_ship_channel | us_gulf_hub | USCG Sector Houston-Galveston (channel closures) | uscg.mil | international_agency | official | port_closure, force_majeure, vessel_loading | proposed |
| gt-houston-marinetraffic | — | houston_ship_channel | us_gulf_hub | MarineTraffic AIS — Houston Ship Channel feed | marinetraffic.com | shipping | official | vessel_loading, exports | proposed |
| gt-houston-vortexa | — | houston_ship_channel | us_gulf_hub | Vortexa — Houston crude/products export analytics | vortexa.com | shipping | official | exports, vessel_loading | proposed |
| gt-houston-kpler | — | houston_ship_channel | us_gulf_hub | Kpler — Houston export tracking | kpler.com | shipping | official | exports, vessel_loading | proposed |
| gt-houston-enterprise | US | houston_ship_channel | us_gulf_hub | Enterprise Products Partners (crude export + NGL) | enterpriseproducts.com | company | official | exports, vessel_loading, pipeline_flow | proposed |
| gt-houston-eia_weekly | US | houston_ship_channel | us_gulf_hub | EIA Weekly Petroleum Status Report (PADD 3 Houston) | eia.gov | international_agency | official | storage_levels, exports, production | proposed |
| gt-houston-noaa_hurricane | — | houston_ship_channel | us_gulf_hub | NOAA NHC – Gulf of Mexico hurricane track | nhc.noaa.gov | weather | official | force_majeure, port_closure | proposed |
| gt-houston-platts_wti_h | — | houston_ship_channel | us_gulf_hub | S&P Global Platts – WTI Houston assessment | spglobal.com | industry_body | official | pricing_formula, exports | proposed |
| gt-houston-port_houston | US | houston_ship_channel | us_gulf_hub | Port Houston Authority | porthouston.com | international_agency | official | vessel_loading, port_closure | proposed |
| gt-houston-tpco | US | houston_ship_channel | us_gulf_hub | Texas Commission on Environmental Quality (TCEQ) | tceq.texas.gov | international_agency | official | refinery_outage, force_majeure | proposed |

## Cross-check

### gt-houston-uscg_sector (USCG Sector Houston-Galveston)
- **Supply:** USCG issues channel closure notices (fog = voluntary, hurricane = mandatory); HSC closure = VLCC loading halt; Harvey 2017 = 1.5 mb/d GOM + refinery shut-in 3–4 weeks; USCG incident log = petrochemical fire/spill/vessel collision
- **Geopolitics:** HSC is US strategic infrastructure; USCG cybersecurity (HSC is critical infrastructure designation); LNG + crude export policy enablement
- **Logistics:** 52-mile channel, 45ft depth; lightering required for VLCC (no fully laden VLCC inside channel); Galveston Offshore Lightering Area (GOLA)

### gt-houston-enterprise (Enterprise Products)
- **Supply:** Enterprise Echo pipeline (Permian → Houston); VLCC-capable dock at Texas City (Battleground); ~1.2 mb/d crude + NGL export capability; propane/butane LPG export = largest US LPG exporter
- **Geopolitics:** Enterprise = bellwether for US crude export infrastructure investment; earnings calls = forward guidance on Permian production/export outlook
- **Logistics:** Echo crude + Seaway pipeline (north-south); Galveston LPG terminal; fractionation trains at Mont Belvieu (world's largest NGL hub)

## Expansion slots
- gt-houston-kinder_morgan — Kinder Morgan Houston products pipelines
- gt-houston-magellan — Magellan Midstream (product terminal Houston)
- gt-houston-mont_belvieu — Mont Belvieu NGL hub (LPG pricing signal)

## Anti-patterns
- Skip: Houston Chronicle energy coverage (secondary local press)
- Skip: bizjournals.com/houston energy section (aggregator)
