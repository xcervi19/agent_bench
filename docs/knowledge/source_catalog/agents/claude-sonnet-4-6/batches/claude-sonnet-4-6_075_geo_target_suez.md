# Batch 075 — Geo Target: Suez Canal

## Geo significance
The **Suez Canal** links the Red Sea to the Mediterranean — ~12% of global trade and ~9–10% of crude/products transit (pre-2024 Houthi disruption). Key stats: ~50–55 ships/day normal throughput; ~190 nautical miles length; fully transited in ~12–16 hours. Notable incidents: **Ever Given grounding (March 2021)**, 6-day closure = $10bn/day goods blocked; **Houthi disruption 2023–2024** = transit dropped to ~50% of normal with major shipping diversions. The **Suez Canal Authority (SCA)** is the primary signal source — real-time transit statistics, toll revenue, and incident notices. BYPAC/CONVOY system. Suez premium = basis differential between ICE Brent and WTI + freight.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gt-suez-sca | EG | suez | chokepoint | Suez Canal Authority (SCA) | suezcanal.gov.eg | international_agency | official | vessel_loading, exports, port_closure | proposed |
| gt-suez-ukmto_med | — | suez | chokepoint | UKMTO – Mediterranean/Red Sea corridor advisory | ukmto.org | shipping | official | port_closure, force_majeure | proposed |
| gt-suez-marinetraffic | — | suez | chokepoint | MarineTraffic AIS — Suez Canal feed | marinetraffic.com | shipping | official | vessel_loading, exports | proposed |
| gt-suez-lloyds_war | — | suez | chokepoint | Lloyd's JWRSG – Suez/Red Sea premium | lloydsmarket.com | shipping | official | force_majeure | proposed |
| gt-suez-bimco | — | suez | chokepoint | BIMCO Suez Canal circulars | bimco.org | shipping | industry_body | vessel_loading, port_closure | proposed |
| gt-suez-egypt_mfa | EG | suez | chokepoint | Egyptian Ministry of Foreign Affairs (canal policy) | mfa.gov.eg | international_agency | official | policy, sanctions | proposed |
| gt-suez-vortexa | — | suez | chokepoint | Vortexa — Suez Canal tanker flow analytics | vortexa.com | shipping | official | exports, vessel_loading | proposed |
| gt-suez-kpler | — | suez | chokepoint | Kpler — Suez crude/products throughput | kpler.com | shipping | official | exports, vessel_loading | proposed |
| gt-suez-imo_msc | — | suez | chokepoint | IMO MSC circular advisories (Suez security) | imo.org | international_agency | official | force_majeure, port_closure | proposed |
| gt-suez-port_said | EG | suez | chokepoint | Port Said Port Authority | portsaid-port.com | international_agency | official | vessel_loading, port_closure | unverified |

## Cross-check (key entries)

### gt-suez-sca (Suez Canal Authority)
- **Supply:** SCA publishes daily transit statistics (ship count, DWT, net tonnage); toll revenue = proxy for traffic volume; monthly reports = trend signal; Ever Given-type grounding = immediate global supply shock
- **Geopolitics:** Egypt controls Suez = strategic asset; Houthi-Egypt tension (2024 revenue loss); Israel-Egypt normalization (Abraham Accords) = canal geopolitics; US Egypt military aid linked to canal openness
- **Logistics:** Convoy scheduling (northbound/southbound); SCZONE (Suez Canal Economic Zone); Ismailia/Port Said anchorage; VLCC restrictions (draft limits for laden supertankers)

### gt-suez-vortexa (Vortexa)
- **Supply:** Real-time crude + products flow through Suez by grade/origin/destination; split between laden northbound vs southbound; LNG carrier count; Houthi diversion impact quantified
- **Geopolitics:** Vortexa data widely cited by IEA, Goldman Sachs, trading desks = market-moving
- **Logistics:** Vessel class tracking; VLCC vs Aframax vs Suezmax count; Cape diversion alternative routes

## Expansion slots
- gt-suez-gatewayhouse — India-Suez cargo monitoring (India-bound crude)
- gt-suez-sca_twitter — SCA official X/Twitter feed (real-time incident notifications)
- gt-suez-splash247 — Splash 247 Suez news (specialist maritime media)

## Anti-patterns
- Skip: EgyptToday (SEO aggregator)
- Skip: Wikipedia Suez Canal article updates (unverified)
