# Batch 086 — Geo Target: Singapore (load port / bunkering hub)

## Geo significance
**Singapore** (Port of Singapore, PSA + Jurong Island) is simultaneously: (1) **world's 2nd largest port** (37m+ TEU/y); (2) **world's largest bunkering hub** (~50m tonnes/y, ~20% global bunker market); (3) **Asia's primary oil refining + trading hub** (ExxonMobil, Shell, BP, Vitol, Trafigura all have Singapore HQ/major ops); (4) **key LNG trading hub** (SGX LNG futures; BW LNG; Pavilion Energy). Singapore's **Jurong Island** hosts major refineries (ExxonMobil 592 kb/d, Shell 237 kb/d, Singapore Refining Company, Chevron). **SGX iron ore + oil futures** are key Asian price benchmarks. The **SGX Platts Singapore** spot market = Asian price formation hub (Dubai crude, 180cst fuel oil, HSFO/VLSFO, naphtha).

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gt-singapore-mpa | SG | singapore | load_port | Maritime and Port Authority of Singapore (MPA) | mpa.gov.sg | international_agency | official | vessel_loading, port_closure, pricing_formula | proposed |
| gt-singapore-platts_sg | — | singapore | load_port | S&P Global Platts – Singapore spot assessments | spglobal.com | industry_body | official | pricing_formula, exports, vessel_loading | proposed |
| gt-singapore-marinetraffic | — | singapore | load_port | MarineTraffic AIS — Singapore anchorage feed | marinetraffic.com | shipping | official | vessel_loading, exports | proposed |
| gt-singapore-vortexa | — | singapore | load_port | Vortexa — Singapore crude/products analytics | vortexa.com | shipping | official | exports, vessel_loading, storage_levels | proposed |
| gt-singapore-kpler | — | singapore | load_port | Kpler — Singapore hub tracking | kpler.com | shipping | official | exports, vessel_loading, storage_levels | proposed |
| gt-singapore-sgx | SG | singapore | load_port | SGX – Singapore Exchange (oil futures) | sgx.com | exchange | official | pricing_formula | proposed |
| gt-singapore-edb | SG | singapore | load_port | Singapore Economic Development Board – refinery stats | edb.gov.sg | international_agency | official | production, exports | proposed |
| gt-singapore-ies | SG | singapore | load_port | Singapore Petroleum Industry Statistics (IES) | ies.org.sg | industry_body | official | storage_levels, production, exports | proposed |
| gt-singapore-argus_bunker | — | singapore | load_port | Argus Media – Singapore bunker prices | argusmedia.com | industry_body | official | pricing_formula, vessel_loading | proposed |
| gt-singapore-recaap | — | singapore | load_port | ReCAAP ISC – Singapore anchorage piracy | recaap.org | international_agency | official | port_closure, force_majeure | proposed |

## Cross-check

### gt-singapore-platts_sg (Platts Singapore)
- **Supply:** Singapore Platts assessments: Dubai crude, naphtha, gasoil, fuel oil (180cst + 380cst + VLSFO), bitumen; Market-on-Close (MOC) process; MPC (Platts) = global benchmark reference for Asian crude + products pricing
- **Geopolitics:** Singapore neutrality = free trade port; US-China tech war = Singapore routing for sensitive energy equipment; MPA = de facto SE Asia maritime governance
- **Logistics:** Western Anchorage (tanker + VLCC); Eastern Anchorage; Jurong Island refinery complex; LNG terminal (Singapore LNG Corp, Jurong); STS off Batam = arbitrage signal

### gt-singapore-ies (IES petroleum stats)
- **Supply:** IES (International Enterprise Singapore / Energy Market Authority affiliate) publishes weekly Singapore oil product stocks; middle distillate draw = Asia demand signal; fuel oil inventory = bunker market proxy
- **Geopolitics:** Singapore stock data referenced by IEA + EIA; market-moving for Asian product spreads
- **Logistics:** Jurong Island tank farms ~147m bbl capacity; Vopak/Universal/Oiltanking storage; weekly stats released Wednesday = trading signal

## Expansion slots
- gt-singapore-ema — Energy Market Authority (gas + power grid = LNG import demand)
- gt-singapore-pavillion_lng — Pavilion Energy (Singapore LNG trader)
- gt-singapore-vitol_sg — Vitol Singapore (largest independent trader; Asia oil flows)

## Anti-patterns
- Skip: Straits Times energy section (secondary local press)
- Skip: channelnewsasia.com energy (general news aggregator)
