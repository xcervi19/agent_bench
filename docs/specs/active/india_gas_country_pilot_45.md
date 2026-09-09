# India gas — country fundamentals pilot topic (#45)

**Status:** in progress — second run + live monitoring on test1 2026-09-10  
**Lane:** Product / business value — *first paying-prospect topic*  
**Depends on:** #30 (playbooks), #32 (source discover), #36 (hybrid pipeline), #39 (source authority), #22 (refresh scheduler)  
**Blocks:** country-fundamentals expansion beyond India
**Blocked by (for the second run):** ~~#51~~ — landed and verified on this ticket's second run, 2026-09-10  
**Related:** #44 (insurance/vessel sources — same inventory+routing failure mode), #20 (monitoring evaluation)

---

## Why this exists

The first customer after the product presentation asked for a **country topic**, not an
event topic. Every topic run so far has been event-shaped (Hormuz closure, sanctions
action). A country topic is a standing question — *"what happened to Indian gas this
week"* — whose output is a **weekly pile the operator reviews**, not a one-shot report.

India was chosen deliberately by the customer: it is **data-visible but forecast-poor**.
The monthly balance is published, but genuine forward views are scarce — which is exactly
where the product should earn its keep. If India works, the pattern generalises to other
countries with different fundamentals.

## Operator brief (fundamentals, verbatim intent)

- India consumes **~200 mcm/d** of natural gas.
- Roughly **half imported LNG, half domestic production**.
- Demand blocks: **fertilizers ~50 mcm/d**, **city gas distribution ~50 mcm/d**,
  **power generation**, **refineries**.
- **Structural growth is city gas** — as new cities are connected to the grid, CGD
  consumption rises.
- Anything touching **Indian electricity in general** is in scope.
- Anything that is a **news item, report or forecast** on the above goes on the pile;
  the operator reviews it **once a week**.

These numbers are the operator's working baseline, not measured values. They are recorded
in the playbook as orders of magnitude to be corrected against PPAC.

## Core question

*"Can a country's fundamentals be encoded once, so that a standing monitored topic keeps
producing a weekly pile an analyst actually wants to read?"*

## What was delivered

### 1) Coverage playbook — the routing layer

`local_knowledge_sources/playbooks/india_gas_demand.md` (56th playbook). Encodes the
balance, the four demand blocks, the CGD growth story, price drivers, geopolitical
triggers, data cadence, and — critically — **anti-patterns specific to this topic**
(PNGRB award ≠ delivered demand; do not attribute a power swing to CGD; mcm/d vs mmscmd
vs mtpa unit discipline).

`india_discounted_crude.md` stays as-is; it covers the crude/refining side of the same
country and the two are cross-linked.

### 2) Whitelist additions — the register

`source_whitelist.json` had **15 India entries and not one gas-demand source**: no PPAC,
no PNGRB, no GAIL, no Petronet, no IGX, no CEA. This is the same failure mode #44 found
for marine insurance — the report would have been forced onto trade press because nothing
authoritative was reachable.

12 entries added (610 → 622), every domain checked for reachability **and page identity**
on 2026-08-20:

| Entity | Domain | Why |
|---|---|---|
| Petroleum Planning & Analysis Cell (PPAC) | ppac.gov.in | **The** monthly gas balance + sector-wise consumption |
| Petroleum and Natural Gas Regulatory Board (PNGRB) | pngrb.gov.in | CGD rounds, geographical-area authorisations, tariffs |
| Central Electricity Authority (CEA) | cea.nic.in | Monthly generation by fuel, gas PLF |
| Ministry of Power (India) | powermin.gov.in | Dispatch policy affecting gas-fired generation |
| National Power Portal (India) | npp.gov.in | Power generation / demand dashboards |
| GAIL (India) | gailonline.com | Transmission network, LNG portfolio |
| Petronet LNG | petronetlng.in | Regas utilisation, term contracts |
| Indian Gas Exchange (IGX) | igxindia.com | Traded domestic gas prices and volumes |
| IndianOil | iocl.com | Refinery runs + CGD arm |
| BPCL | bharatpetroleum.in | Refinery runs + CGD arm |
| HPCL | hindustanpetroleum.com | Refinery runs + CGD arm |
| Gujarat Gas | gujaratgas.com | Largest CGD operator — connection-growth proxy |

**Deliberately excluded:** Department of Fertilizers (`fert.gov.in`) and Grid Controller of
India (`grid-india.in`) were unreachable from the authoring host and are therefore not
whitelisted. The fertilizer block routes through PPAC's sector split and MoPNG until they
can be verified. **This is a known coverage gap on ~25 % of demand** — see Known gaps.

### 3) Topic string

Routing was measured, not guessed. `discover_sources_for_topic` was run over candidate
strings; the chosen one selects both India playbooks plus the competing-Asian-demand
playbook, and pulls all 17 India primary sources:

```
India gas demand: city gas distribution growth, fertilizers, power generation,
refineries; domestic production vs LNG
```

→ `india_discounted_crude.md`, `india_gas_demand.md`, `japan_korea_lng_demand.md`; 32 known sources.

**Correction (2026-08-23) — the wording experiment measured the wrong input.** The variants
above were compared by calling `discover_sources_for_topic` with the bare topic string. In
production the routing input is `discovery_query(facets)` (`topics/facets.py:121`), which
concatenates `canonical_topic_en` + `commodity` + `geo` + `entities` + `signals` + the raw
topic — ~484 characters for this topic, in which the operator's wording is one part among
many. So "adding *Indian electricity* pulls in China" was an artefact of the test, not a
property of the system.

Re-measured against a realistic facets bag:

| input | playbooks | sources | India primaries |
|---|---|---|---|
| bare topic string (what was tested) | 3 | 32 | 17 |
| `discovery_query(facets)` (what runs) | **5** | **53** | **19** |

Also wrong: `MAX_TOPIC_PLAYBOOKS = 3` is not a cap of three. `playbooks_for_topic`
(`sources/playbooks.py:136-143`) takes the top 3 by entity match **and** the top 3 by stem
relevance, then unions them — up to **six**.

The topic string is still the one above and still fine; it simply matters less than claimed,
and the electricity angle is carried by the playbook either way.

### 4) Weekly cadence

Monitoring subscription with `schedule_enabled` and `schedule_interval_hours` set so that
cycles accumulate between the operator's weekly review. The pile is the **delta timeline**
(#22 cadence, #16 monitoring UI). Interval choice is a tuning parameter, not a decision
this ticket freezes — see Open questions.

## Acceptance criteria

- [x] `india_gas_demand.md` exists, follows the playbook template, cross-links `india_discounted_crude.md`
- [x] India gas primary sources present in `source_whitelist.json`, all domains verified reachable + identity-checked
- [x] `discover_sources_for_topic(discovery_query(facets))` returns `india_gas_demand.md` and its primary sources (19 of them)
- [~] Cross-country contamination — the register-level fix is still **#47**, but it does not reach this topic: see the measurement two lines down
- [ ] Playbook preprocessed + ingested with `document_type=playbook`
- [x] Image rebuilt and deployed — **test1** 2026-09-03 (`c07038d`); prod still on `de67d92`
- [x] Topic run end to end — `d19908b3` on test1, `reported`
- [x] Report cites **PPAC** — second run, 2026-09-10, with the monthly sectoral balance quoted sector by sector. It arrived through the feed channel, not through search
- [x] Cross-country contamination measured rather than assumed: `entities: []` and zero `.ir`/`.bd` in both runs' `source_targets.json`
- [~] Monitoring enabled at 24 h collection / 168 h freshness window; **one** cycle so far, so the two-cycle criterion is open
- [ ] Operator review of one weekly pile → tuning list


## First run — test1, 2026-09-03

Topic `d19908b3-8016-4d70-ac1b-e87792a0fa79`, the measured topic string above,
plan `$1.10` / 222 s + deliver `$2.70` / 716 s = **$3.79**.

### The mechanism worked

| | Hormuz baseline (2026-08-01) | India, this run |
|---|---|---|
| `primary_official` share of cited sources | **6 / 28 (21 %)** | **18 / 34 (53 %)** |
| whitelisted | 7 / 28 | 17 / 34 |
| domain targeting | `site:` text, 1 domain/query | `allowed_domains`, **8 of 15 queries, 33 domains, zero `site:`** |

18 search calls recorded, 8 filtered, **none empty** — the fear that a domain
filter returns nothing did not materialise. 149 documents captured, 70+ fetched.
Five of fifteen queries were Hindi from an English brief (#38), the same 33 % as
the Hormuz run. Cited India primaries: `pngrb` ×2, `mopng` ×2, `gailonline` ×2,
`iocl`, `cea.nic`, `powermin`.

### PPAC did not surface — and for the first time we can say why

`ppac.gov.in` contributed **zero** documents. #46's capture makes that
determinate rather than a shrug:

- exactly **one** search call carried `ppac.gov.in` in its filter;
- that call returned a full **10 hits**, none of them from PPAC;
- its three sibling domains in the same filter (`dghindia`, `mopng`, `pngrb`) all
  returned documents.

So the register, the filter and the search all worked. The gap is **query
design**: the only PPAC-filtered query was *"India domestic gas production
licensing rounds allocation priority policy"* — licensing and policy, which is
DGH/MoPNG territory. PPAC's asset is the **monthly consumption balance**, and no
query asked for it. The report reached the same conclusion unprompted, listing
under Risks & blind spots that "independent PPAC primary data was queried but did
not surface a matching monthly release in this pass" — leaving every granular
June-2026 mmscmd figure resting on a single brokerage note republished by one
outlet.

**Tuning item #1 — superseded by the fix below.** The obvious repair was a
monthly-balance query with `ppac.gov.in` in the filter. Probing the source
showed that would still have failed, for a reason no query can fix.

### PPAC probed directly, 2026-09-05 — and now crawled

Reading the site settled what the search evidence could not:

| Check | Result |
|---|---|
| `robots.txt` | none — nothing disallowed |
| Sectoral consumption `.xlsx`, our own UA, one request | **HTTP 200**, 142 KB, `last-modified` **27 Aug 2026** |
| Monthly gas report PDF | **HTTP 200**, 548 KB |
| Domain-filtered search for the monthly balance | reaches PPAC, but the newest report the index served was **December 2024** |
| Format the current numbers are published in | `.xlsx` — which `topics/search_content.py` records as `unsupported` |

So PPAC never fought us. It hands the balance over on the first polite request.
Two things stood between the report and the data, and **neither is a query**:
search returns an index two years stale, and the evidence fetcher cannot read a
spreadsheet.

The conclusion is the one #49 argues for: **we know this URL, so we should ask
for it rather than search for it.** PPAC is now a crawled source, off the search
budget:

- `source_crawler/adapters/landing_link.py` — new adapter for a source whose
  *page* is stable while its *file* is republished under a new timestamped name
  each month. Neither `static_file` (fixed URL) nor `opec_assetdb`
  (`{month}/{year}` template) can express that.
- `source_crawler/seeds/india_gas_official.py` — `ppac_gas_sectoral_consumption`
  (the four demand blocks) and `ppac_gas_lng_import` (import dependence), weekly
  poll, `data_feed` / `skip_rag`.

Verified end to end on 2026-09-05: `crawl --seed india_gas_official` wrote both
files, the re-run reported `unchanged` against the sha256, and the spreadsheet
contains exactly the split the operator brief is built on — **Fertilizer, CGD,
Power, Refinery, Petrochemical, Total, FY 2026-27**.

**Deliberately not seeded:** the `consumption` and `production` pages build their
download links in JavaScript. Those go through the semi-automatic `browser-fetch`
route, where a person saves the file once — defeating a scripted download is out
of scope, and the adapter says so by name when `discover` finds nothing.

### Other findings from the first run

- **China coverage returned almost nothing.** The competing-Asian-demand query
  filtered to `cnpc.com.cn`, `nea.gov.cn`, `customs.gov.cn` and four more
  produced no usable demand or import data — the price-competition side of the
  thesis is unconfirmed. (These `.cn` domains are deliberate scope, not the #47
  contamination; **no Iranian or Bangladeshi domain appeared at all** in this
  run.)
- **Fertilizers** were covered only by an unfiltered Hindi query — the known gap
  from having no fertilizer primary source stands, and shows.
- **Two-tier freshness (#39) held.** Monthly-cadence material survived: the
  report carries June-2026 monthly figures and IEA Q3-2026 projections, which a
  uniform recency window would have deleted. This was the ticket's main worry.
- A PIB release on the 11-A CGD round returned **403** and could not be read.

## Second run — test1, 2026-09-10

Topic `4a6a4504-a7bd-4e0f-ab88-cdff6119d1a6`, same measured topic string, on `50d2a12`.

| | 2026-09-03 | 2026-09-10 |
|---|---|---|
| `primary_official` share of cited sources | 18 / 34 (53 %) | **16 / 25 (64 %)** |
| PPAC in the report | no | **yes, the monthly balance, sector by sector** |
| corpus reaching the analyst | not exported at all | **114 documents** (refresh cycle) |
| official feeds in the run | 0 | **1** (PPAC, 0 days old) |

### The PPAC gap had a second cause, and it was not query design

The first run's diagnosis — the only PPAC-filtered query asked about licensing, which is
DGH/MoPNG territory — was right, and it was not the whole story. `feeds.matches` compared
the seed's `region: IN` against the parse leg's `geo: ["India"]` as plain strings, so the
feed channel **had never selected anything on any run**. Both the unit fixture and the
2026-09-05 in-container verification spelled the country twice, `["IN", "India"]`, which is
an input production does not produce. Fixed in `c0cc930`.

So the crawler, the adapter, the seed and the export were all correct and had never once
delivered a file to an analyst. What made it visible was #51's `feeds.none_matched` warning
naming the facets beside the count of zero — the first run after that warning shipped.

### The pile is running

19 short-term queries, `schedule_enabled` at 24 h, `max_age_hours` 168 — weekly review,
daily collection, which is the conservative-start answer to the Open question below. One
cycle banked at **$2.94 / 605 s**, 6 new sources (3 primary/official). Published
`share_mode=live` at
`https://agent-test1.particletico.com/app/shared/4a6a4504-a7bd-4e0f-ab88-cdff6119d1a6`.

**Cost is the input to the cadence decision:** daily is ~$20/week. One `PATCH /monitor`
moves it to weekly.

### Still open

- The **fertilizer** primary-source gap (~25 % of demand) stands; the second run reaches it
  only through PPAC's sector split, which is now at least present.
- `ppac_gas_lng_import` is a `.xls` — it downloads and does not extract, so the
  import-dependence half of the operator's brief has no series of its own. Needs `xlrd`.
- One more cycle, then the operator review.

## Deploy note

`docker/Dockerfile.claude_agent:49-50` bakes `source_whitelist.json` and `playbooks/` into
the image — there is no volume mount. Both changes in this ticket therefore need a
**rebuild + redeploy**, and must not land on a slot that is about to be demoed. #44 touches
the same two files; batch the rebuilds.

## Known gaps

- **Fertilizer sector has no dedicated primary source** (~25 % of demand). Routes through
  PPAC's sector split. Verify `fert.gov.in` from a host that can reach it and add.
- **Grid-level power data** routes through CEA + National Power Portal; Grid Controller of
  India (`grid-india.in`) unverified.
- **No official social** for any Indian entity — blocked on #31, same as every other playbook.
- The freshness window (#39) matters more here than on an event topic: PPAC is monthly and
  PNGRB is event-driven, so a tight window deletes the entire primary tier. Two-tier
  freshness from #39 should cover this — **verify on the first run**, do not assume.
- Single broad topic vs. one topic per sector is unresolved; see Open questions.

## Open questions

- **One pile or several?** The customer's mental model is one weekly pile. But the plan
  stage may dilute across four sectors in a single run. Start with one; split by sector if
  coverage of the smaller blocks (refineries, power) is thin after two cycles.
- **Refresh interval.** Weekly review does not imply weekly refresh — a daily or 12-hourly
  cadence produces a richer pile at higher cost. Start conservative, measure cost per cycle
  against #39's source mix.
- **Platts input.** The operator has a Platts presentation on the Indian market. Options:
  (a) correct the playbook's baseline numbers from it, (b) ingest it as a RAG document.
  (a) is safe and cheap; (b) is licensed third-party content and needs a licensing call
  before it goes into a shared corpus.
- **Generalisation.** What in this ticket is India-specific and what becomes a reusable
  *country fundamentals* pattern? Answer after the first tuning round, before country #2.

## Out of scope

- Marine insurance / vessel tracking sources (#44)
- Monitoring evaluation rubric (#20), business output rubric (#18)
- Any change to `MAX_TOPIC_PLAYBOOKS` or the routing algorithm (#32/#36 own it)
