# Batch 088 — Geo Target: Novorossiysk

## Geo significance
**Novorossiysk** (Russia, Black Sea coast, Krasnodar Krai) is Russia's primary crude export terminal — handling ~1.4–1.7 mb/d of **Urals blend** (CPC-blend + domestic Urals) through the **Sheskharis** oil terminal. It is also the western terminus of the **CPC Pipeline** (Caspian Pipeline Consortium, 1.3 mb/d, Tengiz + Kashagan Kazakh crude). Novorossiysk sits inside the **Black Sea**, so all exports must transit the **Bosphorus Strait** — Turkey's Kıyı Emniyeti is the downstream constraint. Since Feb 2022, Russia has used Novorossiysk to route Urals crude (G7 price cap ≤$60/bbl) primarily to India and China via shadow fleet. Key monitoring: weather disruptions (Novorossiysk is prone to **Bora winds**, force-8+ storms, 30–40 forced closures/year) and Ukraine drone/missile threat.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gt-novorossiysk-ncsp | RU | novorossiysk | load_port | NCSP – Novorossiysk Commercial Sea Port | nmtp.info | company | official | vessel_loading, exports, port_closure | proposed |
| gt-novorossiysk-cpc | — | novorossiysk | load_port | CPC – Caspian Pipeline Consortium | cpc.ru | company | official | pipeline_flow, exports, vessel_loading | proposed |
| gt-novorossiysk-marinetraffic | — | novorossiysk | load_port | MarineTraffic AIS — Novorossiysk terminal feed | marinetraffic.com | shipping | official | vessel_loading, exports | proposed |
| gt-novorossiysk-tanker_trackers | — | novorossiysk | load_port | Tanker Trackers — Russian crude shadow fleet | tanker-trackers.com | shipping | official | exports, vessel_loading | proposed |
| gt-novorossiysk-vortexa | — | novorossiysk | load_port | Vortexa — Novorossiysk crude loading analytics | vortexa.com | shipping | official | exports, vessel_loading | proposed |
| gt-novorossiysk-kpler | — | novorossiysk | load_port | Kpler — Novorossiysk/Black Sea export tracking | kpler.com | shipping | official | exports, vessel_loading | proposed |
| gt-novorossiysk-weather | — | novorossiysk | load_port | Windy.com / ECMWF — Bora wind forecast (Novorossiysk) | windy.com | weather | official | force_majeure, port_closure | proposed |
| gt-novorossiysk-ukraine_mod | UA | novorossiysk | load_port | Ukraine MoD / GUR drone strike reports | mil.gov.ua | international_agency | official | force_majeure, port_closure | proposed |
| gt-novorossiysk-ofac_russia | US | novorossiysk | load_port | OFAC Russia energy sanctions (NCSP / shadow fleet) | treasury.gov | international_agency | official | sanctions, exports | proposed |
| gt-novorossiysk-lloyds_war | — | novorossiysk | load_port | Lloyd's JWRSG – Black Sea war risk (Novorossiysk) | lloydsmarket.com | shipping | official | force_majeure | proposed |

## Cross-check

### gt-novorossiysk-cpc (Caspian Pipeline Consortium)
- **Supply:** CPC pumps ~1.3 mb/d Tengiz (Chevron op.) + Kashagan (Eni/Shell/Total/CNPC op.) Kazakh crude to Novorossiysk; CPC outage = Kazakh export disruption (Q1 2022 earthquake + storm damage = 2-week suspension); CPC throughput = KZ export rate proxy
- **Geopolitics:** CPC = KZ independence from Russian pipeline monopoly (partly); Russia used CPC maintenance as economic leverage 2022–2023; KZ-Russia tension over Ukraine war = CPC supply risk; Western IOC ownership (Chevron 15%, ExxonMobil 7.5%)
- **Logistics:** Marine terminal Sheskharis SPMs; storm closure (Bora) = CPC backlog; Bosphorus transit constraint downstream

### gt-novorossiysk-ukraine_mod (Ukraine GUR)
- **Supply:** Ukraine drone + missile strikes on Black Sea fleet + Novorossiysk oil terminal infrastructure; Crimea Bridge attack = Russian supply chain signal; terminal damage = loading suspension; Ukraine increasingly targeting Russian energy export infrastructure
- **Geopolitics:** Ukraine asymmetric warfare targeting Russian revenue sources; NATO/US policy on Ukraine striking Russian territory; escalation ladder
- **Logistics:** Ukrainian USV (Magura drones) Black Sea patrol; Novorossiysk harbor approach = target zone

## Expansion slots
- gt-novorossiysk-argus_urals — Argus Media Urals price assessment (Novorossiysk FOB)
- gt-novorossiysk-platts_urals — S&P Global Platts Urals Med differential
- gt-novorossiysk-windward_black — Windward AI Black Sea shadow fleet tracking

## Anti-patterns
- Skip: Russian state TASS/Interfax energy (state propaganda layer; cross-check with Vortexa/Kpler)
- Skip: RBC energy section (Russian commercial press; sanctions-constrained)
