# Batch 087 — Geo Target: Rotterdam

## Geo significance
**Rotterdam** (Netherlands) is **Europe's largest port** and the **ARA hub** (Amsterdam-Rotterdam-Antwerp) — the reference pricing hub for **European oil products** (gasoil, fuel oil, naphtha, gasoline). Rotterdam hosts ~600m tonnes/y cargo throughput, the **Europoort** crude terminal, **Maasvlakte** (deep-water LNG + crude), the **Rotterdam Energy Hub**, and major refineries (Shell 415 kb/d, BP 377 kb/d, ExxonMobil 191 kb/d, Gunvor). **ARA product stocks** (published by Insights Global / Genscape weekly) are globally market-moving. Rotterdam is also **Europe's primary LNG import hub** (Gate Terminal, 12 bcm/y, Shell-Gasunie JV) and a key indicator for European gas storage levels. Post-Russia Ukraine war, Rotterdam crude imports shifted sharply from Russian Urals to US WTI + Middle Eastern grades.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| gt-rotterdam-portbase | NL | rotterdam | load_port | Portbase – Port of Rotterdam data platform | portbase.com | international_agency | official | vessel_loading, exports, imports | proposed |
| gt-rotterdam-insights_global | — | rotterdam | load_port | Insights Global – ARA weekly product stocks | insightsglobal.com | industry_body | official | storage_levels, pricing_formula | proposed |
| gt-rotterdam-platts_ara | — | rotterdam | load_port | S&P Global Platts – ARA barge assessments | spglobal.com | industry_body | official | pricing_formula, storage_levels | proposed |
| gt-rotterdam-marinetraffic | — | rotterdam | load_port | MarineTraffic AIS — Rotterdam/Europoort feed | marinetraffic.com | shipping | official | vessel_loading, imports | proposed |
| gt-rotterdam-vortexa | — | rotterdam | load_port | Vortexa — Rotterdam crude/products analytics | vortexa.com | shipping | official | imports, vessel_loading, storage_levels | proposed |
| gt-rotterdam-kpler | — | rotterdam | load_port | Kpler — Rotterdam import/export tracking | kpler.com | shipping | official | imports, vessel_loading, storage_levels | proposed |
| gt-rotterdam-gate_terminal | NL | rotterdam | load_port | Gate Terminal – Rotterdam LNG import | gateterminal.nl | company | official | imports, vessel_loading | proposed |
| gt-rotterdam-icis | — | rotterdam | load_port | ICIS – Rotterdam petrochemical + products pricing | icis.com | industry_body | official | pricing_formula, storage_levels | proposed |
| gt-rotterdam-argus_ara | — | rotterdam | load_port | Argus Media – ARA product assessments | argusmedia.com | industry_body | official | pricing_formula, storage_levels | proposed |
| gt-rotterdam-port_authority | NL | rotterdam | load_port | Port of Rotterdam Authority | portofrotterdam.com | international_agency | official | vessel_loading, port_closure | proposed |

## Cross-check

### gt-rotterdam-insights_global (ARA stocks)
- **Supply:** ARA product stocks published Wednesday ~17:30 CET; middle distillates (gasoil) = European heating oil demand signal; gasoline inventory = Atlantic basin blending; fuel oil = bunker market; naphtha = petrochemical feedstock; market-moving for ICE gasoil futures
- **Geopolitics:** Post-Russia sanctions: ARA gasoil shifted from Russian diesel to ME/US origin; ARA stock draws in winter = EU energy security signal; German refinery capacity (Rostock, Karlsruhe) = ARA pipeline demand
- **Logistics:** Maasvlakte crude imports (VLCC + Suezmax); Europoort product berths; Rhine barges (domestic distribution); Gate LNG terminal (12 bcm/y regasification)

### gt-rotterdam-gate_terminal (Gate Terminal)
- **Supply:** Gate Terminal 12 bcm/y regasification; LNG import from Qatar, US, Norway, Algeria; European winter supply buffer; spot cargo procurement by Shell + Gasunie
- **Geopolitics:** Post-NordStream gate throughput surge; EU REPowerEU = Gate capacity expansion; Gate LNG = TTF pricing anchor for spot LNG
- **Logistics:** Maasvlakte 2 berth; send-out to Dutch gas grid + Belgium/Germany interconnections; Gate storage 840k m³ LNG = ~6.7 bcm regasification year

## Expansion slots
- gt-rotterdam-genscape — Wood Mackenzie/Genscape ARA refined products (alternative to Insights Global)
- gt-rotterdam-eurocontrol — EUROCONTROL jet fuel demand (ARA aviation fuel proxy)
- gt-rotterdam-vitol_rot — Vitol Rotterdam (tank farm + barge trading)

## Anti-patterns
- Skip: NOS Nieuws energy (Dutch state news, secondary)
- Skip: Offshore Energy.biz (mix of useful + SEO content; verify per article)
