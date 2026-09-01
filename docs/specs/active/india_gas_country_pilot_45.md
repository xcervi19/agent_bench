# India gas — country fundamentals pilot topic (#45)

**Status:** in progress (2026-08-20)  
**Lane:** Product / business value — *first paying-prospect topic*  
**Depends on:** #30 (playbooks), #32 (source discover), #36 (hybrid pipeline), #39 (source authority), #22 (refresh scheduler)  
**Blocks:** country-fundamentals expansion beyond India  
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
- [ ] Cross-country contamination removed from the routed set — `mop.ir` (Iran) and two Bangladeshi power ministries currently match this topic; blocked on **#47**
- [ ] Playbook preprocessed + ingested with `document_type=playbook`
- [ ] Image rebuilt and deployed (whitelist + playbooks are **baked in**, see Deploy note)
- [ ] Topic run end to end; report cites PPAC / PNGRB / CEA, not only trade press
- [ ] Monitoring enabled with a weekly-review cadence; two cycles produce a non-empty, non-duplicative pile
- [ ] Operator review of one weekly pile → tuning list

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
