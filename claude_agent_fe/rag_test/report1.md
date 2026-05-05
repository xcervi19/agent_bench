# TRADE INTEL: Hormuz Strait Closure — Options to Lower Price — May 2026

---

## Phase 1 — RAG Structural Context

RAG vocabulary extracted. Now Phase 2 mapping, then into Phase 3 reasoning.

---

## Phase 2 — Region & Entity Mapping

**This topic directly affects:**
- **Saudi Arabia** → Petroline/East-West Pipeline (4.8 mb/d capacity, only ~50% used), Yanbu terminal (Red Sea), Ras Tanura (blocked by closure)
- **UAE** → Fujairah terminal (already east-of-Hormuz bypass export point), ADNOC
- **Iraq** → Basra Oil Terminal (inside Gulf, blocked), Ceyhan/Turkey (via Kirkuk pipeline, bypasses Hormuz), SOMO
- **Kuwait** → Mina Al Ahmadi (inside Gulf, blocked), KPC
- **Iran** → Kharg Island (controls Hormuz, initiator of closure), NIOC/SHANA
- **Tanker routes** → TD3 (Ras Tanura→Chiba) disrupted; Cape of Good Hope rerouting adds ~15 days; SUMED pipeline (Egypt, 2.5 mb/d) as European bypass
- **Global** → IEA SPR release, VLCC rerouting, freight rate explosion on TD7/Cape route

---

## Phase 3 — Source Intelligence Reasoning

*No searches yet. Pure reasoning on WHERE signals appear first.*

### 3A — What data moves BEFORE the news story?

| Entity | Leading signal | Where it appears first |
|---|---|---|
| Petroline activation | Saudi Aramco crude nomination changes to Yanbu (Red Sea) vs Ras Tanura | Argus Media grade differentials — Arab Light Red Sea vs Arab Light AG spread blows out |
| Fujairah terminal | VLCC berthing queue at Fujairah grows — vessels diverting from Hormuz anchorage | MarineTraffic AIS: search "Fujairah anchorage" vessel count spike |
| Cape rerouting | TD15 (AG→UK Cont Cape route) freight rate surges vs TD3 collapse | Baltic Exchange daily: TD15 vs TD3 spread |
| SOMO Iraq tenders | Iraq issues emergency crude sell tender from Ceyhan instead of Basra | basraoil.gov.iq + somo.gov.iq tender page in Arabic |
| SPR release | DOE Secretary statement precedes EIA data by 24-48h | energy.gov press releases, DOE Twitter |
| VLCC diversions | Tankers last seen near Hormuz turn AIS off or divert east of cape | VesselFinder / MarineTraffic "dark ship" anomalies near Strait |

### 3B — Local language sources that publish first

- **Arabic/شانا:** `shana.ir` — Iran's oil ministry publishes Farsi statements on Hormuz status hours before any translation reaches Reuters
- **Arabic/SOMO:** `somo.gov.iq` — Iraqi tender changes posted in Arabic before English aggregators
- **Arabic/Saudi:** `al-eqtisadiah.com` — Saudi financial daily, covers Aramco operational decisions before English press
- **Turkish:** Ceyhan terminal operator (Botaş) — Kurdish/Turkish press (Rudaw, Enerji Günlüğü) breaks Ceyhan throughput changes
- **Russian:** `interfax.ru/business/energy` — Any Transneft or Novorossiysk capacity increase (as Russia pivots exports) appears here 12-24h before English

### 3C — Niche specialists with ground reporters

- **Iraq Oil Report** → Basra terminal operational status, SOMO export decisions
- **MEES** → Gulf NOC emergency response decisions (Petroline ramp-up authorization)
- **Hellenic Shipping News** → VLCC fixture activity, Cape route bookings, TD15 rate
- **Rudaw** → Kurdistan/Ceyhan pipeline export status (Iraq northern bypass)
- **Argus Media** → Arab Light FOB Yanbu vs FOB Ras Tanura differential — grade spread signal

### 3D — Scheduled data with known timing advantage

- **API report (Tuesday evening)** → first inventory signal, 12h before EIA Wednesday
- **EIA Wednesday 10:30 EST** → SPR drawdown pace, Cushing levels
- **Baltic Exchange daily 16:00 London** → TD3 collapse + TD15 Cape surge = quantified rerouting signal
- **OPEC OMR** (next release ~May 12) → will include emergency production assessment

---

## Phase 3 Output — Focused Search Queries (ordered by speed advantage)

```
FOCUSED SEARCH QUERIES — ordered by speed advantage:

[1]  site:marinetraffic.com Fujairah anchorage VLCC 2026
     → AIS vessel count at Fujairah bypass terminal (real-time, before any news)

[2]  site:hellenicshippingnews.com TD15 Cape route freight rate 2026
     → Baltic route TD15 surge signals rerouting volume (daily, before aggregators)

[3]  site:somo.gov.iq النفط العراقي تصدير جيهان 2026
     → SOMO Iraq tender from Ceyhan in Arabic (hours before English translation)

[4]  site:aramco.com Yanbu export crude loading 2026
     → Saudi Aramco Yanbu Red Sea liftings signal Petroline activation

[5]  خط الأنابيب الشرق الغرب بترولاين ينبع تشغيل 2026
     → Arabic: East-West Pipeline Petroline Yanbu activation (Saudi local press)

[6]  site:shana.ir تنگه هرمز نفت صادرات 2026
     → Iran oil ministry Farsi: Hormuz/exports status (first official Iranian signal)

[7]  site:adnoc.ae Fujairah terminal exports capacity 2026
     → ADNOC Fujairah bypass export ramp-up announcement

[8]  site:energy.gov strategic petroleum reserve release Hormuz 2026
     → DOE official SPR release authorization (before EIA records it)

[9]  site:iraqoilreport.com Basra Ceyhan export 2026
     → Iraq Oil Report ground-level: which terminal is operational

[10] site:mees.com Petroline East-West Pipeline capacity utilization 2026
     → MEES: Gulf NOC emergency pipeline ramp-up decision

[11] Botaş Ceyhan terminal throughput increase 2026 OR Enerji Günlüğü Ceyhan
     → Turkish: Ceyhan capacity ramp-up (Iraq northern bypass throughput)

[12] site:eia.gov petroleum weekly SPR drawdown barrels 2026
     → EIA scheduled data: SPR release pace vs Hormuz gap arithmetic
```

---

## Phase 4 — Primary Signals Found

| Source | Signal | Language | Published | Aggregators? |
|---|---|---|---|---|
| S&P Global / Aramco CEO | Petroline ramped to **full 7 mb/d** (NGL lines converted to crude) by March 11, 2026 | EN | 10-Mar-26 | Delayed ~48h |
| WorldOil / ADNOC | Fujairah loadings **+57% to 1.9 mb/d** (Habshan–Fujairah pipeline near capacity) | EN | 27-Mar-26 | Delayed ~24h |
| The National / SOMO | Iraq Ceyhan exports restarted at **150–250k b/d**, Basra-Haditha pipeline construction started | EN | 18-Mar-26 | Same day |
| Baltic Exchange TD15 | Cape route WS258 — **+57 pts** in one week, TCE $242k/day | EN | Weekly | Real-time |
| Lloyds List | Fujairah **attacked by Iranian drones**, loadings briefly disrupted | EN | Late-Mar-26 | Same day |
| DOE/Rigzone | SPR 172 mb exchange executing at ~**1.4 mb/d** pace, "swift execution" confirmed May 1 | EN | 1-May-26 | Same day |
| Shafaq News (Iraq) | SOMO requesting **faster loading schedules** after partial Hormuz transit exemption | EN | Recent | Specialist only |

---

## Reasoning Chain

1. **RAG:** Petroline capacity was 4.8 mb/d with only 50% utilised — designed bypass exists but was undersized vs. Hormuz 20 mb/d flow
2. **Primary signal:** Aramco converted NGL lines → crude, reaching **7 mb/d** — beyond what *Oil 101* described as available, meaning Saudi upgraded post-book
3. **Implication:** Petroline + Fujairah (1.9 mb/d) + Ceyhan (250k b/d) + SUMED = **~10–11 mb/d** bypass capacity maximum — covers ~50–55% of pre-war Hormuz flow
4. **Gap:** The missing **~9 mb/d** is covered by: SPR (1.4 mb/d), demand destruction, production cuts already embedded in prices, Cape rerouting delays extending effective supply
5. **Conclusion:** Price stabilisation depends on **ceasefire timeline** — bypasses buy time but cannot replace Hormuz structurally. Any Fujairah attack (already happened once) removes the most critical bypass node

---

## Trading Signal

- **Direction:** Structurally **Bullish** Brent while Hormuz closed; tactical pullbacks on SPR/bypass news
- **Timeframe:** 2–6 months structural; 0–2 weeks tactical on ceasefire signals
- **Key instruments:**
  - Brent front month (outright)
  - TD15 freight (Cape route) long — structural beneficiary
  - TD3 (AG→Asia) short until Hormuz reopens
  - Arab Light FOB Yanbu **premium** vs FOB Ras Tanura (Red Sea loading now preferred)
  - Fujairah bunker stocks — watch weekly S&P data for bypass bottleneck signals
- **Thesis risk:** Ceasefire + Hormuz reopening collapses Brent $15–20/bbl within days; Fujairah pipeline attacked again removes 1.9 mb/d bypass = re-acceleration spike

---

## Information Edge — What Aggregators Are Missing

**Iraq's Basra-Haditha pipeline** (started construction May 1, 2026) is the **most underreported bypass story** — if completed it would add ~300k–500k b/d of southern Iraqi exports directly to Jordan/Red Sea, bypassing both Hormuz and Ceyhan. Reuters has not modelled the timeline. The **Mercuria lawsuit against Baltic Exchange** over broken Hormuz benchmarks signals that existing freight derivatives are mis-priced for this regime — a structural market microstructure story that hasn't reached mainstream coverage yet.

---

## Sources

- [S&P Global — Aramco Petroline hits full capacity](https://www.spglobal.com/energy/en/news-research/latest-news/crude-oil/031026-aramcos-east-west-pipeline-to-hit-full-capacity-in-next-couple-of-days-ceo)
- [WorldOil — UAE boosts Fujairah exports](https://www.worldoil.com/news/2026/3/27/uae-boosts-fujairah-oil-exports-as-hormuz-disruption-redirects-crude-flows/)
- [Lloyd's List — Fujairah loadings disrupted by drone attacks](https://www.lloydslist.com/LL1156639/Fujairah-loadings-plummet-as-drone-attacks-rock-UAE-port-prompting-tanker-rethink)
- [The National — Iraq resumes Ceyhan exports](https://www.thenationalnews.com/business/energy/2026/03/18/iraq-to-resume-oil-exports-via-turkeys-ceyhan-port-amid-regional-tensions/)
- [The National — Iraq Basra-Haditha pipeline construction](https://www.thenationalnews.com/business/energy/2026/05/01/iraq-starts-work-on-basra-haditha-pipeline-for-crude-exports/)
- [Hellenic Shipping News — TD15 Cape freight surge](https://www.hellenicshippingnews.com/soh-update-whats-next-for-tanker-freight/)
- [Rigzone — DOE SPR swift execution May 1](https://www.rigzone.com/news/doe_continues_swift_execution_of_172mm_barrel_spr_exchange-01-may-2026-183592-article/)
- [Shafaq News — SOMO faster loading schedules](https://shafaq.com/en/Economy/Iraq-s-SOMO-urges-faster-crude-loading-schedules-after-Hormuz-transit-exemption)
- [Al Jazeera — Saudi, UAE, Iraq three pipelines](https://www.aljazeera.com/economy/2026/3/27/saudi-uae-iraq-can-three-pipelines-help-oil-escape-strait-of-hormuz)
