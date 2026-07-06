# Batch 084 — Geo Target: Yanbu

## Geo significance
**Yanbu** (Saudi Arabia, Red Sea coast) is the western export terminus of the **East-West Crude Pipeline (Petroline, ~5 mb/d capacity)** — the key Hormuz-bypass route for Saudi crude. The **Yanbu Export Terminal** + **Yanbu Aramco Sinopec Refinery (YASREF, 400 kb/d)** + **Petrochem complex** make Yanbu a fully integrated energy hub. In a Hormuz closure scenario, Yanbu becomes the primary alternative Saudi export route to Europe/Mediterranean markets. Current Petroline utilization is partial (~2.5 mb/d). Saudi Aramco and SABIC both have major operations in Yanbu Industrial City (YANBU IC). Yanbu crude exports are primarily delivered to European and US East Coast refineries via **Suez Canal** or Cape of Good Hope.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gt-yanbu-aramco_yanbu | SA | yanbu | load_port | Saudi Aramco – Yanbu Export Terminal | saudiaramco.com | company | official | exports, vessel_loading, pipeline_flow | proposed |
| gt-yanbu-petroline | SA | yanbu | load_port | Saudi Aramco – East-West Crude Pipeline (Petroline) | saudiaramco.com | company | official | pipeline_flow, exports | proposed |
| gt-yanbu-marinetraffic | — | yanbu | load_port | MarineTraffic AIS — Yanbu terminal feed | marinetraffic.com | shipping | official | vessel_loading, exports | proposed |
| gt-yanbu-vortexa | — | yanbu | load_port | Vortexa — Yanbu loading analytics | vortexa.com | shipping | official | exports, vessel_loading | proposed |
| gt-yanbu-kpler | — | yanbu | load_port | Kpler — Yanbu crude export tracking | kpler.com | shipping | official | exports, vessel_loading | proposed |
| gt-yanbu-mopa | SA | yanbu | load_port | Saudi Ports Authority (Mawani) – Yanbu Commercial Port | mawani.gov.sa | international_agency | official | vessel_loading, port_closure | proposed |
| gt-yanbu-yasref | SA | yanbu | load_port | YASREF – Yanbu Aramco Sinopec Refinery (400 kb/d) | yasref.com | company | official | refinery_outage, exports | proposed |
| gt-yanbu-ukmto_red | — | yanbu | load_port | UKMTO – Red Sea / Yanbu area advisories | ukmto.org | shipping | official | force_majeure, port_closure | proposed |
| gt-yanbu-platts | — | yanbu | load_port | S&P Global Platts – Yanbu/Red Sea crude assessment | spglobal.com | industry_body | official | pricing_formula, exports | proposed |
| gt-yanbu-bimco_red | — | yanbu | load_port | BIMCO Red Sea / Yanbu circulars | bimco.org | shipping | industry_body | vessel_loading, port_closure | proposed |

## Cross-check

### gt-yanbu-petroline (East-West Crude Pipeline)
- **Supply:** Petroline 5 mb/d capacity = theoretical full Saudi export bypass of Hormuz; current utilization ~2.5 mb/d; Hormuz closure → Petroline ramp-up = Saudi buffer signal; pipeline maintenance = Yanbu loading reduction
- **Geopolitics:** Petroline was attacked by Houthi drones (May 2019 = Aramco stated "minor damage"); full capacity = Saudi Hormuz independence; US-Saudi agreement on expansion post-2022
- **Logistics:** Yanbu North Terminal (crude) + Yanbu South (products + LPG); VLCC Red Sea loading; Suez Canal access; Houthi Red Sea threat = Yanbu loading premium

### gt-yanbu-ukmto_red (UKMTO Red Sea)
- **Supply:** Red Sea Houthi threat = Yanbu loading disruption; UKMTO advisories for Red Sea approach to Yanbu; armed escort coordination
- **Geopolitics:** Saudi Arabia hosting Yanbu = Red Sea front line; Houthi-Saudi war linkage; Yanbu proximity to Yemen theater
- **Logistics:** Red Sea VLCC routing; Bab el-Mandeb dependency for Yanbu exports to Mediterranean/EU

## Expansion slots
- gt-yanbu-sabic — SABIC Yanbu (petrochemical demand for Yanbu gas/naphtha)
- gt-yanbu-eia_red_sea — EIA Red Sea crude flow analysis
- gt-yanbu-tanker_trackers_rs — Tanker Trackers Red Sea routing (Yanbu vs Ras Tanura split)

## Anti-patterns
- Skip: Arab News energy (secondary Saudi press)
- Skip: Saudi Gazette energy section (state media secondary)
