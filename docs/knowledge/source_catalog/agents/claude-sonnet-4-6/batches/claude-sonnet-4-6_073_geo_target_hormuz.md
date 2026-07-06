# Batch 073 — Geo Target: Hormuz (Strait of Hormuz)

## Geo significance
The **Strait of Hormuz** is the world's most critical oil chokepoint — ~17–20 mb/d crude + condensate transit (~20% of global supply), plus ~4 bcfd LNG (Qatar → Asia). Width narrows to ~3 km shipping lanes. Control contested between **Iran (IRGCN)** and **US Fifth Fleet (NAVCENT)**. Iran has repeatedly threatened closure (2011, 2018, 2023) and seized tankers (Stena Impero 2019, Asphalt Princess 2021, Advantage Sweet 2023). Monitoring entities: UKMTO (primary shipping advisory), NAVCENT (US military), IMO, Oman coast guard (southern shore), Iran Ports & Maritime (northern shore), Lloyd's war risk committee.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gt-hormuz-ukmto | — | hormuz | chokepoint | UKMTO – UK Maritime Trade Operations | ukmto.org | shipping | official | port_closure, force_majeure, vessel_loading | proposed |
| gt-hormuz-navcent | US | hormuz | chokepoint | US Naval Forces Central Command (NAVCENT/5th Fleet) | navcent.navy.mil | international_agency | official | force_majeure, port_closure | proposed |
| gt-hormuz-imb | — | hormuz | chokepoint | IMB Piracy Reporting Centre | icc-ccs.org | shipping | official | port_closure, force_majeure | proposed |
| gt-hormuz-iran_pmo | IR | hormuz | chokepoint | Iran Ports and Maritime Organization (PMO) | pmo.ir | international_agency | official | vessel_loading, port_closure | unverified |
| gt-hormuz-irgcn | IR | hormuz | chokepoint | IRGCN – Islamic Revolutionary Guard Corps Navy | — | international_agency | official | force_majeure, port_closure | proposed |
| gt-hormuz-oman_cg | OM | hormuz | chokepoint | Royal Oman Police Coast Guard | rop.gov.om | international_agency | official | port_closure, force_majeure | proposed |
| gt-hormuz-lloyds_war | — | hormuz | chokepoint | Lloyd's Joint War Risks Study Group (JWRSG) | lloydsmarket.com | shipping | official | force_majeure | proposed |
| gt-hormuz-marinetraffic | — | hormuz | chokepoint | MarineTraffic AIS — Hormuz chokepoint feed | marinetraffic.com | shipping | official | vessel_loading, exports | proposed |
| gt-hormuz-imo_msc | — | hormuz | chokepoint | IMO Maritime Safety Committee advisories | imo.org | international_agency | official | port_closure, force_majeure | proposed |
| gt-hormuz-opec_tanker | — | hormuz | chokepoint | OPEC Monthly Oil Market Report (tanker section) | opec.org | industry_body | official | exports, vessel_loading | proposed |

## Cross-check (key entries)

### gt-hormuz-ukmto (UKMTO)
- **Supply:** UKMTO issues Voluntary Reporting Area (VRA) advisories; vessel registration 24/7; primary alert channel for tanker seizures and drone attacks in Arabian Gulf → direct Hormuz supply disruption signal
- **Geopolitics:** UKMTO = de facto NATO maritime intelligence clearing house for Hormuz/Gulf/Red Sea; reports Iranian IRGCN interdictions; links to Operation Prosperity Guardian
- **Logistics:** AIS transponder gap reports; vessel diversions; VLCC scheduling changes after UKMTO alert = immediate premium signal

### gt-hormuz-irgcn (IRGCN)
- **Supply:** IRGCN seizures halt individual tankers 2–30 days; threat of full Hormuz closure = +$10–30/bbl spike; limpet mine attacks on UAE vessels (2019); Asphalt Princess boarding (2021)
- **Geopolitics:** IRGCN action = Iranian nuclear negotiation leverage; proxy signal for US-Iran tension level; Houthi coordination in Red Sea
- **Logistics:** IRGCN speedboat swarms; helicopter boarding; drone harassment; tanker rerouting via Cape of Good Hope

## Expansion slots
- gt-hormuz-bimco — BIMCO circular advisories (Hormuz risk zones)
- gt-hormuz-vortexa — Vortexa tanker flow analytics (Hormuz throughput real-time)
- gt-hormuz-kpler — Kpler vessel tracking (Hormuz crude flow)

## Anti-patterns
- Skip: geopoliticalfutures.com (paid commentary, no primary data)
- Skip: RedSeaNews.net (SEO aggregator)
