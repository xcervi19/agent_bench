# Batch 077 — Geo Target: Malacca Strait

## Geo significance
The **Strait of Malacca** is the world's second most critical chokepoint by volume — ~16–17 mb/d crude + products transit (>80% of China, Japan, South Korea, Taiwan oil imports pass through). At its narrowest (Phillips Channel, Singapore): 2.8 km. Key actors: **Malacca Strait Patrols (MSP)** — trilateral Malaysia-Singapore-Indonesia; **ReCAAP ISC** (piracy reporting, Singapore-based); Singapore MPA (Port of Singapore = world's second busiest). The **Lombok Strait** (deeper, wider) and **Sunda Strait** are alternatives for VLCC/ULCC that exceed Malacca's ~25m draft limit. Geopolitical risk: **US-China Taiwan tension** = Malacca closure scenario (China encirclement = self-harm, rarely credible); **Indonesia-Malaysia maritime disputes** (secondary).

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gt-malacca-recaap | — | malacca | chokepoint | ReCAAP ISC – Regional Cooperation Agreement on Anti-Piracy | recaap.org | international_agency | official | port_closure, force_majeure, vessel_loading | proposed |
| gt-malacca-singapore_mpa | SG | malacca | chokepoint | Maritime and Port Authority of Singapore (MPA) | mpa.gov.sg | international_agency | official | vessel_loading, port_closure | proposed |
| gt-malacca-ukmto | — | malacca | chokepoint | UKMTO – Indian Ocean/SE Asia advisory | ukmto.org | shipping | official | force_majeure, port_closure | proposed |
| gt-malacca-malaysia_mmea | MY | malacca | chokepoint | Malaysian Maritime Enforcement Agency (MMEA) | mmea.gov.my | international_agency | official | port_closure, force_majeure | proposed |
| gt-malacca-indonesia_bakamla | ID | malacca | chokepoint | Bakamla RI – Indonesian Coast Guard | bakamla.go.id | international_agency | official | port_closure, force_majeure | proposed |
| gt-malacca-marinetraffic | — | malacca | chokepoint | MarineTraffic AIS — Malacca Strait feed | marinetraffic.com | shipping | official | vessel_loading, exports | proposed |
| gt-malacca-imb | — | malacca | chokepoint | IMB Piracy Reporting Centre (SE Asia) | icc-ccs.org | shipping | official | force_majeure, port_closure | proposed |
| gt-malacca-vortexa | — | malacca | chokepoint | Vortexa — Malacca/Singapore throughput analytics | vortexa.com | shipping | official | exports, vessel_loading | proposed |
| gt-malacca-kpler | — | malacca | chokepoint | Kpler — Malacca crude flow (China/Japan/Korea import) | kpler.com | shipping | official | exports, vessel_loading | proposed |
| gt-malacca-bimco_sea | — | malacca | chokepoint | BIMCO SE Asia circular advisories | bimco.org | shipping | industry_body | vessel_loading, port_closure | proposed |

## Cross-check (key entries)

### gt-malacca-singapore_mpa (Singapore MPA)
- **Supply:** Singapore MPA manages Port of Singapore (>37m TEU/y; world's largest bunkering hub ~50m tonnes/y); VLCC anchorage (Strait of Singapore); MPA vessel traffic service (VTS) = real-time throughput; MPA Port Marine Circular = incident notifications
- **Geopolitics:** Singapore neutral position = US-China buffer; MPA coordinates with Indonesia + Malaysia on piracy; SG strategic oil reserve (Jurong Island); fire/collision incidents (Singapore Western Anchorage) = disruption signal
- **Logistics:** One-way traffic management in Phillips Channel; draft restrictions <25m = ULCC via Lombok; tanker anchorage at Johor/Batam; bunkering disruption = immediate freight cost signal

### gt-malacca-recaap (ReCAAP ISC)
- **Supply:** ReCAAP incident reports = piracy/robbery activity level; SE Asia sea robbery (boarding at anchorage) is highest globally; weekly situation report = risk assessment
- **Geopolitics:** ASEAN multilateral piracy cooperation; China not a full member (political); Indian Ocean piracy extension to Malacca corridor
- **Logistics:** Malacca anchorage robbery vs high-seas piracy distinction; vessel diversion via Lombok = +300 nm transit

## Expansion slots
- gt-malacca-ifc_singapore — Information Fusion Centre (IFC) Singapore (maritime security)
- gt-malacca-phillips_channel — Phillips Channel VTS data (Singapore VTS real-time)
- gt-malacca-dryad_sea — Dryad Global SE Asia maritime security

## Anti-patterns
- Skip: Straits Times shipping section (secondary, editorial)
- Skip: seaintelligence.com (container-focused; not crude/energy specific)
