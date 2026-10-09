# India coal — mining, rail movement, power-plant stocks and prices

**Commodity:** thermal (non-coking) coal, as mined, moved and burnt for power; imported coal at the margin  
**Geography:** India — mining belt in Odisha, Chhattisgarh, Jharkhand, Madhya Pradesh, Telangana, Maharashtra, West Bengal; ~190 coal-fired stations nationwide  
**Last reviewed:** 2026-10-09  
**Analyst owner:** India coal customer topic (#56)

## Executive summary

India's coal question is a **stock question**. The country mines most of what it burns,
and Coal India (CIL) mines most of that; the coal then moves to power stations by rail,
and a plant that runs short is flagged by the regulator long before anyone imports a
cargo or a state sheds load. Each link in that chain is published **by the party that
holds the number**: the Ministry of Coal and CIL for mining and despatch, the Ministry's
own rake-loading tables for rail movement, the Central Electricity Authority (CEA) for
what sits at each plant, and CIL's e-auction filings for what non-contracted coal fetches.

The regulator's table is the reason this topic can be done well. CEA's **Daily Coal Stock
Report** lists every coal-fired station with its stock against the stock it must hold,
that day's receipt and burn, and a remark naming who is meant to fix a shortfall. News
reports "N plants critical" once a crisis is a headline; the report has the plant, the
utility and the direction a week earlier.

**Measured from the primaries on 2026-10-09** (each figure from the document named):

- **Power-plant stocks are low and still falling.** CEA, all plants (225 GW): **20.62 Mt
  on 2026-10-08, 33 % of normative**, down from 21.05 Mt on 10-02. Receipts ran below
  burn on **every one of the seven days**. **87 plants critical** (stock < 25 % of
  normative) — 79 of them domestic-coal plants; **8 newly critical within the week**,
  among them NTPC Barh (3.3 GW) and Ramagundem (2.6 GW).
- **Mining is behind last year.** Ministry of Coal, August 2026: national output
  **66.87 Mt, −3.8 % y/y**; April–August **369.2 Mt, −3.2 %**. CIL −5.7 % in August,
  with NCL (−24.8 %) and MCL (−10.0 %) the drag.
- **Despatch is ahead of mining** — the gap is coming out of pithead stocks. August
  national despatch **81.87 Mt, +5.5 % y/y**; to power **65.63 Mt, +3.7 %**. CIL's
  September offtake **61.2 Mt, +12.5 % y/y** against production **53.5 Mt, +9.2 %**.
- **Rail is the binding constraint.** CIL rake loading in August averaged **304.7 rakes a
  day against a plan of 374 (81.5 %)**; to power 280.2 against 332. NCL loaded 31.5 a day
  against 44.0 a year earlier.
- **The domestic spot signal is tightening.** CIL's single-window e-auction cleared
  **94 % above notified price in September 2026**, against **54 %** for April–September;
  72 % of the quantity offered was taken in September, against 40 % for the half-year.

## Price drivers (trader lens)

1. **Power-plant stock and its direction** — total Mt, % of normative, number of critical
   plants, and receipt minus burn. The CEA daily report answers all four. A sustained
   negative receipt-minus-burn is the leading indicator of everything below.
2. **Mining output vs despatch** — when despatch runs ahead of production, pithead stock
   is being drawn; when pithead stock is thin, the next shortfall reaches plants directly.
   Monsoon (June–September) floods open-cast mines and cuts output every year.
3. **Rail rakes** — coal moves by rail; loading against plan, by subsidiary, is the
   transport constraint. A mining region with stock and no rakes is a stranded surplus.
4. **E-auction premium over notified price** — CIL's non-regulated sales; the premium
   widens when plants and industry scramble. India's nearest published domestic spot price.
5. **Imports** — imported-coal-based plants (Mundra, Udupi, coastal IPPs) and blending
   directives; seaborne prices (Indonesian HBA, Newcastle, South African RB) set their cost.
   A blending mandate or Section 11 direction to run imported plants is a demand shock
   for Indonesian and South African coal.
6. **Power demand** — heat, monsoon withdrawal, festival season and industrial load set
   the burn; a demand peak with low stocks is where shortages become load-shedding and
   exchange price spikes (IEX day-ahead and real-time markets).
7. **Policy** — notified price revisions, linkage and e-auction rules, commercial-mine
   auctions and captive-mine output, blending advisories, rail freight priority for coal.
8. **Substitutes at the margin** — gas-fired dispatch when coal is short (see
   `india_gas_demand.md`), hydro after the monsoon, renewables' daytime share.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Ministry of Coal | Policy, notified prices, monthly statistics (production, despatch, rakes, imports), block auctions | Ministry of Coal |
| Coal India Limited (CIL) | ~72 % of output (Apr–Aug 2026, Ministry of Coal); monthly production/offtake and e-auction filings to BSE/NSE | Coal India |
| CIL subsidiaries — MCL, SECL, NCL, CCL, WCL, BCCL, ECL | The mines; production and loading by coalfield | MCL / SECL / NCL / WCL |
| Singareni Collieries (SCCL) | Telangana state-Central producer | SCCL |
| Coal Controller's Organisation | Statutory coal statistics; captive and commercial mine data | Coal Controller |
| Central Electricity Authority (CEA) | **Daily Coal Stock Report** (every coal plant); generation by fuel | CEA / National Power Portal |
| National Power Portal (NPP) | Hosts CEA's daily coal and generation reports | National Power Portal |
| Ministry of Power | Blending advisories, Section 11 directions, power supply position | Ministry of Power |
| NTPC | Largest coal consumer; captive mines | NTPC |
| CERC | Power-market monitoring; exchange price oversight | CERC |
| Indian Energy Exchange (IEX) | Day-ahead and real-time power prices — where a coal shortage becomes a price | IEX |
| MSTC | Government e-auction platform; commercial coal-block auctions | MSTC |
| mjunction | CIL/SCCL e-auction platform; monthly coal import estimates | mjunction |
| DGCI&S / Tradestat | Official import statistics (HS 2701) | DGCI&S / Tradestat |
| Ministry of Ports, Shipping and Waterways | Major-port coal traffic | Ministry of Ports |
| PIB | Government press releases — Ministry of Coal and Railways monthly numbers appear here first | PIB |
| IMD | Monsoon and heat — mine flooding and power demand | IMD |
| Indonesia ESDM | HBA reference price; Indonesian export policy (India's largest supplier) | ESDM |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Ministry of Coal | coal.gov.in | Monthly Statistics at a glance (production, despatch by sector, rakes per day, imports), notified price changes, press releases, block auctions — crawled monthly as a feed | P1 |
| Central Electricity Authority (CEA) | cea.nic.in | **Daily Coal Stock Report** (Fuel Management Division), critical-stock plants, monthly generation by fuel, blending | P1 |
| National Power Portal (India) | npp.gov.in | CEA daily coal stock report files (crawled daily as a feed), daily generation and demand reports | P1 |
| Coal India | coalindia.in | Monthly provisional production and offtake by subsidiary, SWMA e-auction quantity and premium over notified price — both crawled monthly; critical-plant categorisation | P1 |
| Coal Controller's Organisation | coalcontroller.gov.in | Provisional coal statistics, captive/commercial mine production, coal dashboard | P1 |
| Press Information Bureau | pib.gov.in | Ministry of Coal / Railways / Power monthly releases: production, despatch, rake loading, stock | P1 |
| Ministry of Power (India) | powermin.gov.in | Blending advisories, Section 11 directions to imported-coal plants, power supply position | P2 |
| Mahanadi Coalfields (MCL) | mahanadicoal.in | Largest CIL producer (Odisha): production, loading, monsoon disruptions | P2 |
| Northern Coalfields (NCL) | nclcil.in | Singrauli coalfield output; supplies UP/MP pithead plants | P2 |
| South Eastern Coalfields (SECL) | secl-cil.in | Chhattisgarh mega-mines (Gevra, Kusmunda): output and evacuation | P2 |
| Western Coalfields (WCL) | westerncoal.in | Maharashtra/MP output for western plants | P2 |
| Singareni Collieries (SCCL) | scclmines.com | Telangana output and despatch | P2 |
| NTPC | ntpc.co.in | Coal stock at the largest fleet; captive-mine output; import tenders | P2 |
| Indian Energy Exchange (IEX) | iexindia.com | Day-ahead and real-time market prices and volumes during coal stress | P2 |
| Central Electricity Regulatory Commission (CERC) | cercind.gov.in | Market monitoring reports; price-cap orders | P2 |
| DGCI&S Tradestat | tradestat.commerce.gov.in | Coal imports by HS code (2701) and origin | P2 |
| DGCI&S | dgciskol.gov.in | Foreign trade statistics releases | P3 |
| mjunction | mjunction.in | Coal e-auction platform; monthly import estimates widely cited by press | P2 |
| MSTC | mstcecommerce.com | Commercial coal-block auction results; e-auction notices | P3 |
| Ministry of Ports, Shipping and Waterways | shipmin.gov.in | Major-port coal handling; coastal shipping of coal | P3 |
| India Meteorological Department | mausam.imd.gov.in | Monsoon progress over the mining belt; heatwaves driving demand | P3 |
| Ministry of Energy & Mineral Res. (ESDM) | esdm.go.id | Indonesian HBA price, export rules — the import-cost side | P3 |

**Deliberately absent, and why** (checked 2026-10-09 from the operator's machine):

- **`grid-india.in`** (grid operator, daily power supply position) — no response, as on
  #45. Its daily report would be the best demand-side table; re-check before adding.
- **`indianrailways.gov.in`** (Railway Board freight loading) — no response. Rail coal
  loading is reached through the Ministry of Coal's rake tables and PIB instead.
- **`ipa.gov.in`** (Indian Ports Association) — no response.
- **`imports.coal.gov.in`** (Coal Import Monitoring System) — no response.
- **`bcclweb.in`** — Cloudflare challenge; **`easterncoal.nic.in`** — no response;
  **`centralcoalfields.in`** — empty 202. BCCL, ECL and CCL figures come through CIL's
  and the Ministry's tables.
- **`globalcoal.com`** (Newcastle index) — Cloudflare challenge; seaborne prices are
  reached through ESDM's HBA and through press.
- **`commerce.gov.in`** — 403; trade data comes through `tradestat.commerce.gov.in`.

**Known access limits on registered domains.** `coalindia.in` answered **403 from the VPS**
on 2026-10-09 while answering 200 from the operator's machine; CIL's filings themselves are
served from a CloudFront host. `pib.gov.in` and `powermin.gov.in` answer 403 to scripted
fetches; search results from them still carry titles and snippets, and PIB pages were read
in the India gas run. `ntpc.co.in` sits behind a bot check on deeper pages.

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official handle in `source_whitelist.json`; blocked on #31 |

## Infrastructure & logistics

Coal is mined in the east and centre and burnt everywhere, so **rail is the system**: most
coal reaches plants in rakes of roughly 3,500–4,000 t, and loading against plan by subsidiary is the
transport constraint. **Pithead plants** (Singrauli, Korba, Talcher, Anpara, Sasan) hold
fewer normative days because their coal arrives by conveyor or MGR; a pithead plant at low
stock is a mining problem, a distant plant at low stock is a rail problem. Northern and
western state utilities (Haryana, Rajasthan, Punjab, UP, Maharashtra) sit furthest from the
mines and fall critical first. Imported coal lands at west- and east-coast ports (Mundra,
Krishnapatnam, Paradip, Gangavaram, Kandla) for coastal IPPs designed on imported coal; their
stock moves with seaborne prices, not with CIL.

## Geopolitical and market triggers

- **Receipt below burn for a week or more** in the CEA daily report — the leading signal.
- **The count of critical plants rising**, and which utilities they belong to.
- **Monsoon disruption** at MCL, SECL, NCL — output and loading fall together.
- **Rake loading below plan** in the Ministry's monthly tables or a PIB release.
- **E-auction premium widening** month on month.
- **Blending advisory or Section 11 direction** from the Ministry of Power — imported coal
  demand switches on by order.
- **Notified price revision** by CIL — the regulated price of most Indian coal.
- **Power demand peaks** (heat, post-monsoon, festival season) meeting low stocks —
  IEX price spikes, load-shedding reports.
- **Indonesian export policy** (DMO, royalty, HBA) and freight — the cost of the margin.
- **Commercial-mine auctions and captive output** — the slow-moving supply addition.

## Data cadence

| Source | Frequency | Observed lag (2026-10-09) |
|--------|-----------|---------------------------|
| CEA Daily Coal Stock Report (npp.gov.in) | daily | next day — the 10-08 report was generated 10-09 15:04 |
| CIL provisional production and offtake | monthly, filed to BSE/NSE on the 1st | 1 day — September filed 10-01 |
| CIL SWMA e-auction data | monthly, filed on the 1st | 1 day |
| Ministry of Coal Monthly Statistics at a glance | monthly | ~4 weeks — August posted in September |
| PIB releases (Coal, Railways, Power) | event-driven; monthly production on the 1st–2nd | same day |
| IEX market prices | daily | same day |
| DGCI&S trade statistics | monthly | ~6 weeks |
| Coal Controller provisional statistics | annual | months |

**This cadence is the point.** The plant table moves every day; the mine and auction tables
move once a month and arrive on the 1st. A daily cycle reads the stock trend each day and
picks up the monthly filings the day they land.

## Tier 2 context sources

IEA Coal Mid-Year Update and Coal 2025, IEEFA and CEEW analyses of Indian power and coal,
Ember's India electricity data, Argus/Platts/Kpler coverage of Indian coal imports (often
paywalled; cite only what is readable), Reuters and Business Standard reporting on plant
stocks. Useful for framing; not primary scan anchors.

## Anti-patterns

- **Reading "% of normative" as days of stock.** Normative stock is days of requirement at
  85 % PLF (21 days for most plants, fewer for pithead). A plant at 15 % of normative holds
  ~3 days *at 85 % PLF*; at its real burn it may hold more or less. The feed computes stock
  over the day's actual burn — use that.
- **Treating a critical flag as an outage.** A critical plant is still running; it becomes a
  supply loss only if receipts fail for days. Watch receipt minus burn, not the flag alone.
- **Adding plants designed on imported coal into the domestic shortage.** Section B plants
  are short when seaborne coal is dear, not when CIL is late.
- **Comparing production with despatch without the pithead stock.** Despatch above
  production is a draw on stocks, not new supply.
- **Quoting a CIL figure as national.** CIL was 72 % of output in April–August 2026; SCCL and captive/commercial
  mines are the rest, and captive output is the part that grows.
- **Reading the scanned CIL annexure literally.** It is OCR: "8 5" is 8.5; prefer the totals
  row and cross-check with the Ministry's table.
- **Quoting e-auction premium as a price level.** It is a percentage over notified price, by
  subsidiary and grade mix; the mix changes month to month.
- **Inventing ministry or subsidiary domains** not present in `source_whitelist.json`.

## Related playbooks

- india_gas_demand.md — gas-fired dispatch is the substitute when coal runs short
- southeast_asia_lng_imports.md — Indonesia's export balance, India's largest coal supplier
- china_oil_gas_imports.md — the other large seaborne coal buyer
- australia_lng_nws_gorgon.md — Australia, the seaborne thermal coal and LNG exporter

## Changelog

- 2026-10-09 — initial draft for a customer topic (#56). Every primary domain above was
  verified on 2026-10-09 by **reachability plus page identity** from the operator's machine;
  the refusals and access limits are listed above. The numbers in the executive summary
  were **read from the CEA daily reports of 10-02..10-08, the Ministry of Coal's August
  2026 Monthly Statistics, and CIL's September 2026 production and e-auction filings**, not
  estimated.
