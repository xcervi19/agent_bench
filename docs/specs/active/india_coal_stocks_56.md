# India coal — mining, rail, prices and power-plant stocks (#56)

**Status:** in progress — deployed to test2 and first report delivered 2026-10-09 (topic `009ff1c4`); published live and monitored daily from 2026-10-10
**Lane:** Product / business value — *a customer's ask, the fourth country topic*
**Depends on:** #53 (feed channel delivering), #54 (refresh keeps official sources), #55 (the method, last repeated)
**Related:** #45 (India gas — same country, the substitute fuel), #46 (the five gates), #22 (scheduler), #47 (routing contamination)

---

## The ask

A trading desk wants Indian coal: **mining, transport, prices, and above all coal
stocks** — "everything a trader would want to know about coal in India". The demo is
a pre-sales hook, so the measure of success is the one the first customer stated on
2026-09-10: **primary, official sources first**, relevance second.

## Could we find primary sources? Not before this ticket

Measured 2026-10-09 against the register and playbooks as they stood on #55:

- `source_whitelist.json` held **no** coal source at all — no Ministry of Coal, no Coal
  India, no Coal Controller. CEA, the National Power Portal and the Ministry of Power
  were the only overlap, registered for gas-fired generation.
- No playbook mentioned Indian coal; the nearest were `india_gas_demand.md` and
  `india_discounted_crude.md`.

A run on that would have been a news report about a coal crunch. So this ticket is the
onboarding, the same shape as #45, #53 and #55.

## What was done

- **Playbook 59** `local_knowledge_sources/playbooks/india_coal_mining_stocks.md`. The
  chain mine → rail → plant stock → price, eight drivers, entity table, 22 primary
  domains, cadence table, anti-patterns. The executive-summary numbers are **read from
  the primaries on 2026-10-09**, not recalled (see "What the primaries already say").
- **Register 651 → 669.** Ministry of Coal, Coal India and four subsidiaries (MCL, NCL,
  SECL, WCL), SCCL, Coal Controller, PIB, NTPC, IEX, CERC, DGCI&S and Tradestat,
  mjunction, MSTC, Ministry of Ports, IMD. Notes extended on CEA, NPP and the Ministry
  of Power. Each verified by reachability plus page identity from the operator's
  machine.
- **A new adapter and daily feed: the CEA Daily Coal Stock Report.**
  `source_crawler/adapters/cea_coal_stock.py`. Every coal-fired station (~190, 225 GW)
  with stock against normative, the day's receipt and burn, a critical flag (< 25 % of
  normative) and CEA's remark naming who is to fix it. The adapter reads the newest
  report and the six before it and writes one ~41 kB text feed: a seven-day trend,
  group totals, the week's largest stock draws, plants newly critical, the critical
  list lowest-first, and every plant.
- **Three monthly feeds through `landing_link`:** the Ministry of Coal's *Monthly
  Statistics at a glance* (production, despatch by sector, rake loading per day,
  imports — every producer); Coal India's provisional production and offtake filing;
  and Coal India's SWMA e-auction filing (quantity offered and allocated, premium over
  notified price). All four in the new seed `india_coal_official`.
- **`coal` synonym group** in `feeds.COMMODITY_SYNONYMS` — `coal` / `thermal coal` /
  `steam coal` / `non-coking coal`. Deliberately **not** joined to `power` (a stock
  table is not evidence for every Indian electricity question) nor to `coking coal`
  (steel's coal, a different good). Pinned in `tests/topics/test_feeds.py`, including
  that the coal feed does not reach the India gas topic and the gas feeds do not reach
  this one.

## Three things the adapter had to get right

1. **The form is not the door.** `npp.gov.in/dailyCoalReports` is a date picker that
   POSTs with a session and a `_csrf` token, and a POST without the session cookie
   302s back to the empty form. The response, once it works, links the files at a
   dated public path — `/public-reports/cea/daily/fuel/08-10-2026/dailyCoal1-2026-10-08.pdf`
   — that a plain GET serves with no session at all. The adapter walks back from today
   (IST) to the newest file that exists; a missing day is skipped, a file that exists
   and does not parse is an error.
2. **PDF, not the `.xls` beside it.** The `.xls` is legacy BIFF from JasperReports and
   the crawler has no reader for it (`extract.py` names `.xls` as a gap). `pypdf`'s
   layout mode keeps each plant on one line with its columns in order: **191 of 191
   plant rows** parse on the 2026-10-08 report, and on all seven reports of the week.
3. **Three row shapes the regex alone does not cover.** A transport mode that wraps in
   its cell arrives as `RAIL-SEA-`; some rows print no mode at all; and NTPC's joint
   ventures print a two-word GENCO, `NTPC JV`, which a naive split files as state
   "Uttar Pradesh NTPC". Each is a fixture line in `tests/source_crawler/test_cea_coal_stock.py`.

## What the primaries already say (2026-10-09)

Read from the four feeds, before any run — the reason this topic is worth a desk's time:

| Signal | Number | Source |
|---|---|---|
| Plant stock, all 225 GW | **20.62 Mt, 33 % of normative** on 10-08, from 21.05 Mt on 10-02 | CEA daily |
| Receipt minus burn | **negative on all seven days** 10-02..10-08 (−4 to −162 kt/day) | CEA daily |
| Critical plants | **87** on 10-08 (79 domestic-coal); **8 newly critical** in the week, incl. NTPC Barh 3.3 GW, Ramagundem 2.6 GW | CEA daily |
| National output, August | **66.87 Mt, −3.8 % y/y**; Apr–Aug −3.2 % | Ministry of Coal |
| National despatch, August | **81.87 Mt, +5.5 % y/y** — despatch ahead of output, drawing pithead stock | Ministry of Coal |
| CIL rake loading, August | **304.7/day vs plan 374 (81.5 %)**; to power 280.2 vs 332 | Ministry of Coal |
| CIL September | production 53.5 Mt (+9.2 %), offtake 61.2 Mt (+12.5 %) | CIL filing |
| E-auction premium | **94 % over notified price in September** vs 54 % Apr–Sep | CIL filing |

That is mining, transport, prices and stocks — the desk's four words — each answered by
the party that holds the number.

## The topic string, and why this one

Measured with `discover_sources_for_topic` against the 22 coal primaries in the playbook:

| Candidate | Sources | Coal primaries | Playbooks |
|---|---|---|---|
| "India coal: mining production, rail transport, coal prices and power plant coal stocks" | 43 | 22 | **brazil_power**, india_coal, india_discounted_crude |
| "India thermal coal: Coal India production and offtake, rail rake loading, e-auction premiums, imports, coal stocks at power plants" | 43 | 22 | **brazil_power**, **china_oil_gas_imports**, india_coal |
| "India coal supply and stocks: … rake loading, e-auction premium, imports — CEA …, Ministry of Coal" | 42 | 22 | **china_oil_gas_imports**, india_coal, **lng_global_supply** |
| **"India coal mining and stocks: production, despatch, rail rakes, e-auction premium, imported coal and critical plant coal stocks — Ministry of Coal, Coal India, CEA daily coal stock report"** | **43** | **22** | india_coal, india_discounted_crude, india_gas_demand |

Every candidate reaches all 22 primaries; the difference is noise. `power` and
`thermal` pull the Brazil playbook (`brazil_power_hydro_thermal`), `imports` pulls China,
`supply` pulls global LNG. The chosen string keeps only Indian playbooks, and the gas
one is a genuine neighbour — gas-fired dispatch is the substitute when coal runs short.

**Known residual risk, the same as #55's.** The parse leg can still write `power` or
`electricity` into the facets and bring Brazil back into the plan. The coal playbook is
the top match either way; check `playbook_refs` on the first plan. The router fix is #47's.

## Access limits found, and recorded rather than worked around

- `coalindia.in` answers **403 from the VPS** (200 from the operator's machine;
  confirmed on both landing pages 2026-10-09), and a failed source fails the whole
  `crawl` — so on the slot's cron it would have taken the daily CEA feed down too.
  The two CIL filings are therefore their own seed, **`india_coal_cil`**, crawled
  where `coalindia.in` answers and copied to the slot (see `docs/ops/commands.md`).
  The files themselves are on CloudFront and download from the VPS; only the page
  that names them is refused.
- Also from the VPS: `mahanadicoal.in` 403, `nclcil.in` and `cercind.gov.in` no
  response, `ntpc.co.in` captcha. Registered anyway — search returns them — with the
  limit in their notes.
- `pib.gov.in`, `powermin.gov.in`, `commerce.gov.in` answer 403 to scripted fetches;
  PIB is registered anyway because search returns its pages and the India gas run read one.
- No response: `grid-india.in` (as on #45), `indianrailways.gov.in`, `ipa.gov.in`,
  `imports.coal.gov.in`, `easterncoal.nic.in`, `industry.gov.au`. Cloudflare challenge:
  `bcclweb.in`, `globalcoal.com`. None registered.

## First run on test2 — 2026-10-09

Topic **`009ff1c4-42d6-4d43-8ee6-e07af34299b4`** on `cbf76c6`. Plan 370 s / $1.37,
deliver 552 s / $3.65 — **$5.02**. `facets_degraded: false`.

- **All four feeds reached the analyst and all four are cited** (`feeds_count: 4`,
  s01–s04): CEA daily stock, CIL production/offtake, CIL e-auction, Ministry of Coal.
  The report's spine — 87 critical plants on 10-08, CIL +9.2 % / +12.5 %, the 94 %
  e-auction premium, domestic-coal plants at 31 % of normative against 60 % for
  imported-coal plants, Torangallu at 0 % — is read from them.
- **Source mix 4/15 authoritative (26.7 %)** — the 4 are the feeds; the other 11 are
  5 specialist outlets, 5 aggregators (four of them stock-quote pages: groww, zerodha,
  tickertape, scanx) and 1 newsletter.
- **Why no searched primary, answered from `search_queries` / `search_documents`, not
  guessed.** The 9 domain-filtered queries each returned ~10 hits, and the official
  documents behind them were **fetched**: coal.gov.in 9, NTPC 9, ESDM 10, cea.nic.in 7,
  DGCI&S 7, CERC 6, Tradestat 3. They were the wrong years — Ministry of Coal monthly
  reports from 2022–2024, CEA stock PDFs from 2020, DGCI&S reviews from 2021, CERC
  orders from 2022–2023. The analyst discarded them as stale, correctly, and said so
  under Risks. It is #45's PPAC finding again: **the index serves the regulator's old
  files; the current ones come only through the feed.** #46's three-way table puts this
  in row 3 (fetched, not cited) with the cause being age, not selection.
- **Routing:** the `source_discover` stage, which routes on facets, listed
  `brazil_power_hydro_thermal.md` and `china_oil_gas_imports.md` — the residual risk
  above fired — but the plan's 22 source targets carry only the coal and gas playbooks,
  and no query went to a Brazilian or Chinese domain.
- **Plan:** 13 queries, 9 domain-filtered, 4 in Hindi.

**Two defects in the report, for the review:**

1. **Rake loading contradicts the feed it had.** The report says CIL rake loading
   "roughly doubled from 19 to 41/day", cited to a stock-quote aggregator. The Ministry
   of Coal feed (s04) gives **304.7 rakes/day in August against a plan of 374**. Whatever
   19→41 measures, it is not that, and the primary was in hand.
2. **The stock trend is missing.** The CEA feed's headline — 20.62 Mt at 33 % of
   normative, receipts below burn on all seven days — is not in the report; it counts
   critical plants from news instead. Nor is the Ministry's August output −3.8 % against
   despatch +5.5 %.

Both are the analyst preferring news over a feed it cited. The fix belongs in the
deliver prompt (a feed figure outranks a secondary one on the same quantity) and in a
`blocked_domains` list for stock-quote pages, which carry no primary content for any topic.

## Build items, in order

1. ~~Playbook, register, adapter, seed, synonyms, tests~~ — done 2026-10-09 (suite 479 passed).
2. ~~Verify from the VPS~~ — done; see "Access limits".
3. ~~Deploy to test2~~ — branch delivered as a git bundle (GitHub push refused the
   local credentials), image rebuilt, four feeds published, cron `30 11 * * *`.
4. ~~Create the topic, deliver, read the source mix~~ — see "First run".
5. ~~Publish (live) and daily monitoring~~ — run by the owner 2026-10-10 09:49 UTC
   (`POST /publish {"mode":"live"}`, `POST /monitor {"max_age_hours":168,
   "schedule_enabled":true,"schedule_interval_hours":24}`); first cycle 2026-10-11 09:50 UTC.
5b. **Fix the two report defects** above — deliver prompt + stock-quote `blocked_domains`.
6. **Two cycles of pile, then the operator review** (#46 Gate 5).
