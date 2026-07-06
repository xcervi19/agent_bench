# Batch 078 — Geo Target: Bospor (Bosphorus / Turkish Straits)

## Geo significance
The **Bosphorus Strait** (+ Dardanelles + Sea of Marmara = "Turkish Straits") is the sole maritime exit for Russian Black Sea crude — ~2.5–3.0 mb/d pre-war, now ~1.5–2.0 mb/d of Russian Urals + Kazakh KEBCO + Azerbaijani AZERI LT BTC crude. Width: 700m narrowest. **Turkey (BOTAŞ, Turkish Straits directorate)** controls transit under the 1936 **Montreux Convention**. Turkey has repeatedly invoked environmental/insurance clauses to delay or block tankers lacking P&I cover (Nov 2022 insurance crisis = ~25 ships stuck). Key signal sources: Turkish Coastal Safety authority (SAR/transit data), Tanker Trackers / Vortexa (shadow fleet detection), and Lloyd's (P&I cover verification). Significant Russian shadow fleet (>600 tankers) transiting without western P&I = escalating insurance scrutiny.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gt-bosporus-turkey_directorate | TR | bosporus | chokepoint | Turkish Coastal Safety Directorate (Kıyı Emniyeti) | kiyiemniyeti.gov.tr | international_agency | official | vessel_loading, port_closure, force_majeure | proposed |
| gt-bosporus-marinetraffic | — | bosporus | chokepoint | MarineTraffic AIS — Bosphorus feed | marinetraffic.com | shipping | official | vessel_loading, exports | proposed |
| gt-bosporus-tanker_trackers | — | bosporus | chokepoint | Tanker Trackers (shadow fleet / Russian crude) | tanker-trackers.com | shipping | official | exports, vessel_loading | proposed |
| gt-bosporus-lloyds_pi | — | bosporus | chokepoint | Lloyd's P&I Club – Turkish Straits insurance verification | lloydspandi.com | shipping | official | force_majeure, port_closure | proposed |
| gt-bosporus-vortexa | — | bosporus | chokepoint | Vortexa — Bosphorus crude flow analytics | vortexa.com | shipping | official | exports, vessel_loading | proposed |
| gt-bosporus-kpler | — | bosporus | chokepoint | Kpler — Bosphorus/Black Sea throughput | kpler.com | shipping | official | exports, vessel_loading | proposed |
| gt-bosporus-turkey_mfa | TR | bosporus | chokepoint | Turkish Ministry of Foreign Affairs (Montreux) | mfa.gov.tr | international_agency | official | policy, sanctions | proposed |
| gt-bosporus-turkey_botas | TR | bosporus | chokepoint | BOTAŞ – Turkish Pipeline and Energy Corp | botas.gov.tr | international_agency | official | pipeline_flow, exports | proposed |
| gt-bosporus-imb | — | bosporus | chokepoint | IMB Piracy Reporting Centre (Black Sea) | icc-ccs.org | shipping | official | force_majeure, port_closure | proposed |
| gt-bosporus-lloyds_war | — | bosporus | chokepoint | Lloyd's JWRSG – Black Sea war risk premium | lloydsmarket.com | shipping | official | force_majeure | proposed |

## Cross-check

### gt-bosporus-turkey_directorate (Kıyı Emniyeti)
- **Supply:** Issues transit notifications + waiting lists; environmental clause delays (Nov 2022 = 25 tankers stuck, ~50 mb backlog); SAR coordination; Bosphorus vessel traffic data = Black Sea crude export rate
- **Geopolitics:** Montreux Convention (1936) = Turkey's legal instrument; NATO-Russia tension = Turkey's balance act; Ukraine war = warship transit ban (since Feb 2022); insurance clause = non-NATO P&I pressure
- **Logistics:** ~3 tanker transits/hour each direction; 700m narrowest = single-file; Istanbul traffic separation scheme; fog/current cancellations (~30 days/year)

### gt-bosporus-tanker_trackers (Tanker Trackers)
- **Supply:** Russian shadow fleet identification; AIS manipulation detection; Urals crude export quantification; KEBCO (Kazakh) vs Russian blend identification; CPC pipeline throughput cross-check
- **Geopolitics:** Shadow fleet expansion post-2022 = sanctions evasion signal; G7 price cap compliance monitoring; flag-of-convenience tracking (Gabon, Cameroon, Palau registries)
- **Logistics:** Ship-to-ship (STS) transfers off Ceuta + Laconia + Malta = blending operations; Aframax fleet dark voyages

## Expansion slots
- gt-bosporus-cpc_pipeline — CPC Pipeline (Tengiz-Novorossiysk; Kazakh crude = Bosphorus throughput signal)
- gt-bosporus-novorossiysk_port — Novorossiysk Commercial Sea Port (key Black Sea crude terminal)
- gt-bosporus-windward — Windward AI (shadow fleet detection)

## Anti-patterns
- Skip: Hürriyet Daily News energy (secondary Turkish press)
- Skip: Turkish state TRT World energy coverage (narrative, no primary data)
