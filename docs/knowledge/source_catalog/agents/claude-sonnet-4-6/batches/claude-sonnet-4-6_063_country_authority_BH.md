# Batch 063 — Country Authority: BH (Bahrain)

## Country significance
Bahrain is a small but strategically vital Gulf state — home to the **US Fifth Fleet** (Naval Support Activity Bahrain), a historic crude producer (Awali field since 1932), and a major regional **oil refinery hub** (BAPCO Sitra refinery ~267 kb/d capacity). Since domestic production has largely peaked (~45 kb/d), Bahrain relies on the **Abu Saafa shared field with Saudi Arabia** (SA provides ~150 kb/d to BH under 1958 agreement). BAPCO is expanding with the Bapco Modernization Program (BMP) targeting ~360 kb/d capacity. BH is a **GCC/OPEC+ associate** but not a full OPEC member; policy signals originate from Ministry of Oil, BAPCO, and the Saudi Aramco pipeline link.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-BH-ministry_petroleum | BH | — | ministry_petroleum | Ministry of Oil and Environment | moe.gov.bh | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-BH-noc | BH | — | noc | BAPCO – Bahrain Petroleum Company | bapco.net | international_agency | official | production, exports, term_contract, pricing_formula | proposed |
| ca-BH-mfa | BH | — | mfa | Ministry of Foreign Affairs | mofa.gov.bh | international_agency | official | sanctions, policy | proposed |
| ca-BH-customs_export | BH | — | customs_export | Bahrain Customs Affairs | customs.gov.bh | international_agency | official | exports, export_license | proposed |
| ca-BH-upstream_regulator | BH | — | upstream_regulator | NOGA – National Oil and Gas Authority | noga.gov.bh | international_agency | official | production, force_majeure | proposed |
| ca-BH-port_maritime_authority | BH | — | port_maritime_authority | Khalifa Bin Salman Port / APM Terminals | apmterminals.com/bahrain | international_agency | official | vessel_loading, port_closure | proposed |
| ca-BH-national_exchange | BH | — | national_exchange | Bahrain Bourse | bahrainbourse.com | exchange | official | pricing_formula | proposed |
| ca-BH-central_bank | BH | — | central_bank | Central Bank of Bahrain | cbb.gov.bh | international_agency | official | pricing_formula | proposed |
| ca-BH-environment_regulator | BH | — | environment_regulator | Supreme Council for the Environment | sce.gov.bh | international_agency | official | refinery_outage | proposed |
| ca-BH-coast_guard_navy | BH | — | coast_guard_navy | Bahrain Coast Guard | interior.gov.bh/coast-guard | international_agency | official | port_closure, force_majeure | unverified |

## Cross-check (key entries)

### ca-BH-noc (BAPCO)
- **Supply:** BAPCO Sitra refinery 267→360 kb/d (BMP); Abu Saafa crude from Saudi (150 kb/d); product exports to Asia/EU; term contracts via BAPCO Trading
- **Geopolitics:** GCC member; US Fifth Fleet basing = key US-Iran tension indicator; Saudi dependency on Abu Saafa; China BAPCO investment discussions
- **Logistics:** Sitra terminal (crude import + product export); Hidd Industrial Area; VLCC calling via Arabian Gulf

### ca-BH-upstream_regulator (NOGA)
- **Supply:** NOGA issues upstream licenses; Awali legacy field; offshore Bahrain-SA shared zone; BGP exploration
- **Geopolitics:** NOGA coordinates with Saudi Aramco on Abu Saafa; US basing rights vs Iran proximity = upstream risk
- **Logistics:** All Bahrain exports via Sitra terminal; no pipeline to third-party countries

## Expansion slots (10+)
- ca-BH-bapco_trading — BAPCO Trading (London/Dubai)
- ca-BH-gpic — Gulf Petrochemical Industries Company
- ca-BH-aluminium_bahrain — ALBA (aluminium smelter = large energy consumer, power/gas demand indicator)
- ca-BH-eia_monitor — US EIA Bahrain country page
- ca-BH-fifth_fleet_press — US Naval Forces Central Command press releases (strait closure signal)

## Anti-patterns
- Skip: Gulf Daily News (English-language GCC tabloid, no primary data)
- Skip: Bahrain.net (commercial/tourism aggregator)
