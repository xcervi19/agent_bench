# Batch 079 — Geo Target: Gibraltar

## Geo significance
The **Strait of Gibraltar** is the Atlantic-Mediterranean gateway — ~20 mb/d product + crude flows (European import corridor); width ~14 km. Less vulnerable to closure than other chokepoints (too wide, NATO-controlled waters), but strategically important as: (1) **STS transfer hub** off Ceuta/Gibraltar/Algeciras — Russian shadow fleet blending operations, Iranian crude transfers, and Venezuelan crude-for-refined-product swaps; (2) **European LNG import corridor** (Algeria → Spain pipelines + LNG; Atlantic LNG → Spain/France/Italy); (3) **Morocco-Spain energy crossroads** (Maghreb-Europe Gas Pipeline via Gibraltar). Key signal: ship-to-ship (STS) transfers in the Strait = sanctions evasion / dark fleet signal. Gibraltar Bunkering (world's 4th largest bunker port) = freight cost signal.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gt-gibraltar-marinetraffic | — | gibraltar | chokepoint | MarineTraffic AIS — Gibraltar Strait feed | marinetraffic.com | shipping | official | vessel_loading, exports | proposed |
| gt-gibraltar-tanker_trackers | — | gibraltar | chokepoint | Tanker Trackers — STS/shadow fleet Gibraltar zone | tanker-trackers.com | shipping | official | exports, vessel_loading | proposed |
| gt-gibraltar-port_authority | GI | gibraltar | chokepoint | Gibraltar Port Authority | gibraltarport.com | international_agency | official | vessel_loading, port_closure | proposed |
| gt-gibraltar-spain_maritime | ES | gibraltar | chokepoint | Capitanía Marítima de Algeciras | mitma.gob.es | international_agency | official | vessel_loading, port_closure | proposed |
| gt-gibraltar-morocco_port | MA | gibraltar | chokepoint | Agence Nationale des Ports – Tanger Med | anp.org.ma | international_agency | official | vessel_loading, port_closure | proposed |
| gt-gibraltar-lloyds_war | — | gibraltar | chokepoint | Lloyd's JWRSG – Gibraltar/Med western approach | lloydsmarket.com | shipping | official | force_majeure | proposed |
| gt-gibraltar-vortexa | — | gibraltar | chokepoint | Vortexa — Gibraltar crude/products flow analytics | vortexa.com | shipping | official | exports, vessel_loading | proposed |
| gt-gibraltar-kpler | — | gibraltar | chokepoint | Kpler — Gibraltar/Atlantic-Med throughput | kpler.com | shipping | official | exports, vessel_loading | proposed |
| gt-gibraltar-bimco | — | gibraltar | chokepoint | BIMCO Gibraltar bunkering + STS advisories | bimco.org | shipping | industry_body | vessel_loading, port_closure | proposed |
| gt-gibraltar-windward | — | gibraltar | chokepoint | Windward AI — Dark vessel / STS detection | windward.ai | shipping | official | exports, vessel_loading | proposed |

## Cross-check

### gt-gibraltar-tanker_trackers (STS/shadow fleet)
- **Supply:** STS transfers off Ceuta = Russian Urals → unknown destination blending; Iranian crude STS (ship-to-ship, AIS off) → European or Asian buyers; Venezuelan heavy crude + diluent swaps; 50–80 vessels/month in zone
- **Geopolitics:** EU/US sanctions evasion hub; G7 price cap circumvention; OFAC/EU blacklist vs flag-of-convenience; Morocco Tanger Med increasingly monitoring STS activity
- **Logistics:** STS zone: Algeciras Bay, Ceuta approaches, Gibraltar Bay, Laconia anchorage; Aframax/Suezmax size typical; Gibraltar bunkering (1.8m tonnes/y)

### gt-gibraltar-morocco_port (Tanger Med)
- **Supply:** Tanger Med = North Africa's largest container + LNG terminal; Morocco's Nador West Med LNG expansion; Algeria-Spain GME pipeline (now inactive) alternative supply; fuel supply for African-Atlantic shipping
- **Geopolitics:** Morocco-Spain geopolitics (Ceuta/Melilla disputed territories); Western Sahara = EU-Morocco energy deal complication; Morocco-Algeria zero gas transit (GME cancelled 2021)
- **Logistics:** Tanger Med bunkering expansion; STS monitoring zone off Strait; Algeciras Bay anchorage

## Expansion slots
- gt-gibraltar-ceuta_port — Puerto de Ceuta (Spanish enclave; STS monitoring point)
- gt-gibraltar-bunkernet — BunkerNet Gibraltar (bunkering spot price signal)
- gt-gibraltar-dryad_med — Dryad Global Mediterranean maritime security

## Anti-patterns
- Skip: Gibraltar Chronicle general news (not energy-specific)
- Skip: gib-news.com (local community aggregator)
