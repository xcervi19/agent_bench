# Topic onboarding loop — turning ad-hoc demo bending into a capability (#46)

**Status:** planned (2026-08-20)
**Lane:** Product / method — *how a new customer topic gets onboarded, measured and tuned*
**Depends on:** #23 (eval framework), #32/#36 (source discover + pipeline), #39 (source authority), #22 (scheduler)
**Blocks:** country #2 and every subsequent demo topic
**Related:** #45 (India — the first topic to run this loop), #44 (insurance sources — the same gap found by accident), #43 (Claude judge), #41 (multi-run baseline), #21 (timeliness metrics)

---

## Why this exists

The product passed the demo stage. It now has to satisfy real desks — traders, business
analysts, risk managers — whose requirements we do not yet know. We are deliberately in an
**ad-hoc mode**: bend the application per customer until the first ones are convinced.
Consolidation into one coherent product comes later.

The risk of that mode is that each demo produces a one-off hack and nothing accumulates.
This ticket defines the loop that makes ad-hoc bending **compound**: every new topic runs
the same five gates, every gap it exposes lands in the same three instrumented places, and
the tuning that follows is measured rather than argued.

India (#45) is the first topic through the loop and is also its test case: the loop is only
real if it can be executed on India end to end.

## What the Hormuz baseline actually proves

Measured on `testing/baselines/hormuz_90d_2026-08-01` (rubric `trading_intelligence`,
heuristic evaluator, overall 3.84/5):

| Layer | Score | Read |
|---|---|---|
| Research Quality (w 0.3) | **4.59** | Entity/relationship/depth all 5.0 — the analyst brain is not the problem |
| Trading Intelligence (w 0.3) | **4.36** | Actionability and market impact 5.0 |
| **Information Discovery (w 0.4)** | **2.90** | The heaviest layer is the weak one |

Inside the weak layer: `primary_source_discovery` **1.75**, `information_latency` **0.0**,
but `non_obvious_source_discovery` **4.59**.

That combination is the whole story, and it is counter-intuitive:

```
24 queries  →  200 results  →  28 kept  →  drops logged: 1
13/24 queries were site:-scoped to official domains
of the 28 kept: 6 primary_official + 1 data_feed, 7 on whitelisted domains
5 of those 6 primaries came from site:-scoped queries (UKMTO, IEA, Treasury,
   Aramco, ADNOC, Port of Fujairah)
4 queries returned 31 results and kept ZERO — q03 shana.ir, q04 pmo.ir,
   q05 mfa.gov.ir, q07 mofa.gov.sa (Iranian and Saudi official sources)
```

Read carefully, this says two things:

**The routing mechanism works.** Playbook → whitelist → `site:` query produced 5 of the 6
primary sources in the report. It does not need replacing. Its **yield is low** — roughly
one kept source per `site:` query — and only ~25 % of the report stands on primary sources.

**The failure is concentrated, not general.** The Iranian and Saudi official sources
returned 31 results and contributed nothing.

**What we cannot say** — and an earlier draft of this ticket overstated it — is *why*.
`results_count` counts search results, not usable articles; a `site:` query against a
Persian ministry routinely returns navigation pages, old PDFs and duplicates, so 200 → 28
is not by itself pathological. Whether those 31 results were junk or were good hits we
discarded is **not determinable from the artifacts**: `drops` is three integers.

That indeterminacy is the actual finding, and it is why Build item 1 comes first. Note also
that this run had **#39 two-tier freshness already live** (`baseline.json`,
`app_commit ab96982`), so the `too_old` mechanism #39 fixed does not explain the zero.

The second finding is structural, not a defect: `information_latency` **0.0** because the
median kept source was ~90 days old — on a deliberately 90-day topic, scored against a
14-day decay curve. India will hit this harder: PPAC is monthly by design, so a
fundamentals topic scored like an event topic is guaranteed to fail that dimension.

## The loop — five gates per new topic

Each gate produces one artifact and is cheap. Gates 1, 3 and 5 are where the human sits;
2 and 4 are mostly machine.

### Gate 1 — Brief

The single largest free lever, and currently unmanaged. Compare:

- Hormuz `topic.txt`: four paragraphs — the desk's **position** ("long Brent, long regional
  refining margins, short freight optionality"), the specific questions, and an explicit
  *what I want out of this*. Scored 4.36 on trading intelligence.
- India as first written: one line of sector names.

The brief drives facets → entities → queries. **Deliverable:** a brief template plus a
short agent-run interview (5 questions: what do you trade / what is your exposure / what
decision does this feed / what would change your mind / how often do you read it) that
emits a Hormuz-shaped brief. Semi-automatic, operator approves.

### Gate 2 — Fundamentals → playbook

The domain encoding, as done by hand for India in #45: balance, demand blocks, drivers,
triggers, cadence, and topic-specific anti-patterns. **Deliverable:** `/playbook-draft`
that drafts from the brief + RAG + web, with **domain verification as code** — reachability
plus page-identity check, the step that kept 12 invented-looking domains honest in #45 and
correctly excluded `fert.gov.in` and `grid-india.in`.

### Gate 3 — Register gap check (highest-value automation)

Deterministic, no LLM. Run `discover_sources_for_topic`, group the resolved primaries by
the brief's facets, and report **which facet has no primary source**.

This check would have caught, before any run: the missing marine-insurance tier (#44,
found by accident after a 1.8/5 score) and the missing Indian gas tier (#45, found by
accident while scoping). Twice by accident is a process defect, not bad luck.

**Deliverable:** `scripts/topic_coverage_report.sh` → per-facet coverage table, exit
non-zero on an uncovered facet.

### Gate 4 — Dry run + measure

Run the topic once. Score with `scripts/evaluate_output.sh absolute`. Read **the funnel
before the score** (see Build item 1). Record cost per cycle.

### Gate 5 — Tune, one change at a time

`scripts/evaluate_output.sh relative --baseline <prev> --candidate <new>`. One variable per
run; the ticket records what moved. No unmeasured tuning.

## Build items — priority order

### 0. Pass the whitelist to WebSearch as `allowed_domains` *(measured 2026-08-21; do this first)*

**The single cheapest, best-evidenced change found so far.** We hold a 622-domain register
and never hand it to the search tool. Domain targeting happens as `site:` text inside the
query string, which the model writes by hand, one domain at a time.

The tool takes a structured domain filter. Its full parameter set is exactly three fields:

```
query            string   (required)
allowed_domains  string[] — only include results from these domains
blocked_domains  string[] — never include results from these domains
```

**There is no result-count parameter.** WebSearch returns ~9–10 links per call regardless;
the API-side `web_search` tool is the same shape (`max_uses` bounds the number of
*searches*, not results per search). More results is only ever more queries — which is why
the domain filter, not query volume, is the lever worth pulling first.

#### The measurement (India, the #45 topic)

Two searches, near-identical wording, run 2026-08-21.

| | Plain query | `allowed_domains` = 10 India primaries |
|---|---|---|
| Links returned | 9 | 10 |
| **Primary/official** | **1** (ppac.gov.in) | **10** |
| The rest | Outlook Business, psuwatch, Mordor Intelligence, verifiedmarketresearch, chemindigest, business-standard | — |

What the filtered search surfaced, none of which the plain search reached:

- `pngrb.gov.in` — *Natural Gas Projections – 2030 Base Case*
- `pngrb.gov.in` — *Rapid Assessment: Natural Gas Demand – 2040 Projections for India*
- `pngrb.gov.in` — *Pathways to Increase Share of Natural Gas*
- `pngrb.gov.in` — *Zonal Study on Natural Gas Pipeline* (2026-05-19)
- `ppac.gov.in` — *Sectoral Consumption*
- `ppac.gov.in` — *Industry Consumption Report POL & NG, Feb 2026*
- `mopng.gov.in` — *City Gas Distribution*
- `petronetlng.in` — *LNG Overview*

**This refutes the premise the topic was scoped on.** The operator's brief said Indian gas is
"data-visible but forecast-poor — there aren't many news items or forecasts". There are. The
regulator publishes its own demand projections to 2030 and 2040 (300 MMSCMD and 423 MMSCMD
base case). They are PDFs on `pngrb.gov.in` that generic search never ranks. The scarcity was
never in the world; it was in the door we were using to reach it.

It also corrected a baseline number: fertilizer offtake is **~58 MMSCMD**, not the ~50 the
brief estimated — now sourced rather than assumed. Update `india_gas_demand.md` accordingly.

#### Why this changes the arithmetic

`site:` in query text is one domain per query. `allowed_domains` is an array:

```
site: in text     →  40 queries = 40 domains per cycle   (~6 % of the register)
allowed_domains   →  40 queries × 6 domains ≈ 240 slots  (most of the register per cycle)
```

Query wording also stops having to be surgical, because the domain filter does that work —
which lowers, not raises, how much a geopolitical knowledge base has to carry.

#### The filter widens the aperture as well as narrowing it (measured 2026-08-23)

WebSearch returns ~9–10 links per call and has no result-count parameter, so the aperture
looks fixed. It is not fixed per *question* — it is fixed per *(question × filter)*. One
India question, asked three ways:

| run | filter | links | primary | overlap with earlier runs |
|---|---|---|---|---|
| 1 | none | 9 | 1 | — |
| 2 | 10 gas/regulator domains | 10 | 10 | **0** |
| 3 | 8 power/refiner domains | 10 | 10 | **0** |

**29 links, zero URL overlap, 20 primary.** Run 3 is where `npp.gov.in`'s monthly
gas-to-power consumption report and CEA's monthly executive summary appeared — recurring
series directly on the operator's power-sector question.

This resolves the apparent conflict between reliability and coverage: the domain filter is
not only a precision instrument, it is how one question reaches more of the web. Plan
several filtered variants of an important question, not one.

#### Batch size: 5–8 peers of the same role, never mixed strength

Search still ranks *inside* the filter, so a dominant domain starves its batch-mates. In
run 2 above, `pngrb.gov.in` took 5 of 10 slots and **six of the ten domains returned
nothing** — `cea.nic.in`, `npp.gov.in`, `powermin.gov.in`, `gailonline.com`, `igxindia.com`,
`dghindia.gov.in`. Run 3 gave five of those six their own batch and they produced 10 good
hits. They were never short of content; they were sitting next to a stronger neighbour.

An earlier draft of this item said "batch up to 10". That is measurably worse. Batch
**5–8 domains of comparable authority and the same role** — which is exactly what
`authority_type` labels (#47) make possible automatically.

#### Two prerequisites, both before the change and not after

1. **`SearchEvidenceRecorder` captures only the query** (`search_evidence.py:91`:
   `self._queries[block["id"]] = block["input"]["query"]`). The moment `allowed_domains` is
   in use, the evidence store can no longer tell which domains were *attempted* — so a
   domain that search never returns becomes indistinguishable from one never asked for.
   That is precisely the Iranian/Saudi question in Build item 1. One-line fix; it must land
   first or we destroy the diagnostic while fixing the yield.
2. **The results are PDFs.** #42 added PDF reading (previously discarded as `unsupported`),
   so this flows into the corpus. Verify on the first run — without it the whole gain stops
   at the titles.

#### Acceptance

- [x] `allowed_domains` recorded alongside `query` — landed as `search_queries` (below)
- [x] Whitelist domains reach WebSearch as `allowed_domains`, batched
- [ ] Batches sized 5–8 by role, not 10 mixed (contract corrected 2026-08-23; unexercised)
- [ ] Cross-country contamination fixed before this ships — **blocked on #47**
- [ ] Rotation across the register over cycles (still open — see Open questions)
- [ ] India run shows primary/official share materially above the Hormuz baseline's ~25 %

#### Delivered 2026-08-22 (both halves, in the order the prerequisite demanded)

**Evidence first.** New table `search_queries` — one row per WebSearch call, **including
the calls that returned nothing**, carrying `query`, `allowed_domains`, `blocked_domains`
and `hit_count`. That second part turned out to matter as much as the domain columns:
`record_hits` used to `return` early on an empty result, so a search that came back with
nothing left no trace at all — making *"we asked and search returned nothing"*
indistinguishable from *"nobody asked"*. Those need opposite fixes, and the Iranian/Saudi
question in Build item 1 is exactly that distinction. `search_observations` gains a
nullable `query_id` FK; existing rows keep NULL.

- `database/migrations/versions/0012_search_queries.py` (head; chain verified
  `0011_refresh_tokens -> 0012_search_queries`, offline SQL generated and cross-checked
  against the model DDL). **Not applied to a real database — Docker was down locally**,
  same gap #42 shipped with. Apply before deploy.
- `apps/claude_agent/topics/search_evidence.py` — `SearchCall` dataclass; `parse_call`
  reads the whole tool input, not just `input["query"]`. `None` (no filter) is kept
  distinct from `[]` (a filter allowing nothing).

**Then the filter.** `allowed_domains` now flows plan → monitoring plan → search:

- `newsfind-plan.md` — queries carry `allowed_domains[]`; domains are **batched up to 10
  per query** (3–5 batched queries preferred over 10 single-domain ones), taken verbatim
  from `known_domains` as bare hosts. `site:` is out of the query text — writing both
  applies the filter twice and collapses the batch to one domain. Some queries stay
  unfiltered on purpose: a filter can only return what the register already knows.
- `refresh.py build_short_term_queries` — the silent one. It rebuilds every entry from
  scratch, so an uncarried field is dropped without error; a dropped filter turns a
  domain-filtered monitoring plan back into open web search. Now carried and normalised to
  bare lowercase hosts (`WWW.PPAC.GOV.IN` → `ppac.gov.in`), omitted rather than nulled when
  absent. Pinned by `tests/topics/test_query_domain_filter.py`.
- `newsfind-deliver.md` / `newsfind-refresh.md` — pass the filter to `WebSearch`; a filtered
  query that returns nothing is recorded, **not silently retried unfiltered**, or the two
  cases collapse again.

Tests 331 → 337, all green; ruff clean on every touched file (the pre-existing I001 in
`models.py`/`refresh.py` is untouched, as in #42).

### 1. Selection audit trail — **already shipped as #42; this item is now a query, not a build**

An earlier draft of this ticket proposed building this. It exists. **#42 Search evidence
capture** (done 2026-08-02, on `main`) records every hit web search returns, and
`3ea0fbe` (2026-08-06) then feeds the captured text back into the report:

- `search_documents` — deduplicated, one row per (topic, URL): what the corpus holds.
- `search_observations` — append-only, one row per (query, run, rank): how search behaved.
- `search_content.py` — background fetcher reading the page behind each hit under a
  self-identifying, robots-respecting client. Outcomes are first-class data, not errors:
  `fetched` / `thin` / `blocked` / `not_found` / `disallowed` / `unsupported` / `error`.
  Accumulates into a **per-domain accessibility map**.
- `evidence_export.py` — the corpus is written into the run dir, one file per document with
  provenance front matter plus an index; the refresh command reads those **before** WebFetch
  and prefers them ("WebFetch returns a model's answer to a prompt, a corpus file is the
  article"). Unreadable documents are counted in the index so absence is not mistaken for
  silence.
- Query plan cap was a literal `12` in three places; now `settings.refresh_max_queries`,
  **default 40**.

Measured in production: search returns **~9 links per query**, we successfully read **~89 %**
of them, and the last pre-change run held **121 documents** averaging ~16k characters. The
`ab6b98f` NUL-byte fix was diagnosed against a 29k-char article **in prod**, so this is
live, not theory.

Note the #42 spec quotes the same funnel this ticket re-derived (24 → 200 → 28, drops = 1,
~171 vanished). The Hormuz baseline (2026-08-01) is the **last run before evidence capture
landed** — which is exactly why its drops are opaque, and why that opacity is no longer the
state of the system.

**So the open question about the Iranian and Saudi zero-yield queries is now answerable from
data, not by building anything:** query `search_observations` for those domains and read
`fetch_status` on the matching documents. Three outcomes, three different fixes:

| What the data shows | Meaning | Fix |
|---|---|---|
| No observations for the domain | Search never returned it | Query formulation / the domain is not indexed |
| Observations exist, `blocked`/`disallowed` | We can never read it | Record in the playbook; stop routing there or find the feed |
| Observations exist, `fetched`, not cited | The analyst discarded readable text | Selection contract — the original hypothesis |

**Acceptance:** run that query against a post-#42 topic and record which of the three it is.

### 1b. What #42 deliberately left open — the judging pass

#42 records without a verdict, by design ("a verdict written at capture time would freeze a
judgement that will not hold"). The pass that reads the corpus and judges it is explicitly
**not designed yet**. That is now the real gap behind "correctly filter" in the business
requirements, and it is where the next build effort belongs — not in capture.

### 2. Per-query yield, surfaced to the operator

`search_observations` is one row per (query, run, rank), and `url_hash` uses the same
`sha1(url)[:16]` convention as `news.json#sources` — so per-query yield joins cleanly to
what was actually cited, with no new capture. (`query_ids` on kept sources gives a cruder
version of the same thing.) On the Hormuz baseline: 5 of 24 queries kept nothing, and
they are precisely the non-English official-source queries.

Surface it in the weekly pile: which queries produced keepers, which produced nothing. The
operator already agreed to a weekly review (#45) — that review becomes the feedback loop
that edits `short_term_queries`. Human-in-the-loop learning at nearly zero engineering cost.

### 3. Topic shape as a first-class field

Two shapes, different physics:

| | **event** (Hormuz) | **standing / fundamentals** (India) |
|---|---|---|
| Value | hours matter | the pile over a week matters |
| Freshness | tight window | must admit a monthly PPAC release |
| Latency scoring | on the report | on the **delta**, not the foundational report |
| Novelty | vs. the news cycle | vs. **what this reader already saw** |

Relevant here: the ~25 % primary share above is the **foundational report**. On the
monitored refresh, #39 moved source mix from 0 % to **80 % primary/official** — the delta
cycle is far better grounded than the report. India's customer value is the weekly pile, so
that is the number to watch, on one measurement so far.

Add `shape` to the topic; let it set freshness defaults (extending #39's two tiers) and
select the evaluation profile. Without this, every fundamentals topic scores 0 on latency
by construction and the number is meaningless.

## Using what we already have — for "unique news" specifically

- **Whitelist composition.** The playbook is the routing layer, the whitelist only the
  register (#44's formulation). Uniqueness comes from reaching sources generic search does
  not rank — the mechanism already scores 4.59 on non-obvious discovery and produced 5 of
  the 6 primary sources in the baseline. It does not need replacing; it needs to be handed
  to the search tool **structurally** rather than typed into query text one domain at a
  time — see Build item 0, where that change took primary share from 1/9 to 10/10 on the
  India topic.
- **RAG.** Two unexploited moves: (a) the customer's own material as topic context — the
  Platts deck for India; (b) storing prior cycles so novelty is judged **per reader**, not
  globally. Refresh currently dedupes on `seen_url_hashes` — URL level. A second article
  about the same PNGRB award is a new URL and an old fact. Novelty belongs at the claim
  level, against the topic knowledge base.
- **Agentic.** `short_term_queries` is the pile engine and is set once at plan time. For a
  standing topic it should be revised by the weekly review (Build item 2) — the query plan
  becomes something the desk owns, which is also the stickiest part of the product.

## Coverage is cumulative, not per-cycle

"Search the whole internet" is not achievable in one run: 40 queries × ~9 links ≈ 360 slots,
and that is the entire aperture. But a standing topic runs weekly for months — 40 × 52 is
over two thousand queries a year. Completeness is a function of **rotation and memory**, not
of one run's breadth.

That became measurable on 2026-08-22: `search_queries` records every call and its filter, so
"what has the register not been asked lately" is now a query rather than a guess. With #47's
labels it becomes an auditable statement — *"of the 10 authority slots for IN, 7 were queried
in the last 4 cycles, 3 were not."* That is "nothing must escape", expressed over time.

**What we should not claim:** complete coverage of the internet — it is unfalsifiable and
untrue. What we can claim, and what a trading desk actually buys, is **auditable coverage of
a defined space plus a measured discovery frontier**: *"47 authorities for Indian gas, all
queried within three cycles; 23 new domains evaluated outside that set, 4 promoted."*
Defensibility, not omniscience.

## What we deliberately do NOT do now

- No feature consolidation — that is post-market-entry.
- #35 graph retrieval: not until a customer's question actually needs it.
- #31 scraping: only when a customer asks for a channel we cannot otherwise reach.
- No new rubric dimensions. Instrument first, then measure, then build.

## Dependency worth naming

If product decisions are steered by the rubric, the judge matters. `--evaluator llm`
currently runs on OpenAI (**#43** migrates it to Claude); the heuristic evaluator is
provider-free and is what every number in this ticket came from. Use heuristic for the
tuning loop until #43 lands, or the loop is tuned against the wrong judge.

## Acceptance criteria

- [ ] Five gates documented and executed **once, end to end, on India (#45)**
- [ ] `scripts/topic_coverage_report.sh` exists; exits non-zero on an uncovered facet; reproduces the #44 and #45 gaps from before-state data
- [ ] `allowed_domains` wired from the whitelist, with the domain list recorded in `search_observations` (Build item 0 — prerequisite 1 lands first)
- [ ] Iranian/Saudi zero-yield settled from `search_observations` + `fetch_status` on a post-#42 run (no build required — see Build item 1)
- [ ] Judging pass over the captured corpus designed (#42's explicit non-scope)
- [ ] Per-query yield computed from existing `query_ids` and shown in the weekly pile
- [ ] `shape` field on topic drives freshness defaults + evaluation profile
- [ ] Brief template + interview produces a Hormuz-shaped brief from a 5-question exchange
- [ ] India re-scored after tuning; `evaluate_output.sh relative` shows the direction of every change made

## Open questions

- **Interview vs. template for Gate 1** — an interview is better input but adds friction to a
  demo. Possibly: template for us, interview for self-serve (#37).
- **Where per-query yield lives** — inside the delta artifact, or a separate ops view (#34)?
- **Claim-level novelty** is the largest item here and may deserve its own ticket once
  Build item 1 shows how much duplication actually reaches the reader.
- **How much of a playbook can be drafted automatically** before the human review stops
  being real review.
- **How to batch and rotate 622 domains across `allowed_domains` calls.** By playbook? By
  facet? By last-yield? The register is bigger than one cycle's queries, so the rotation
  policy is a real design choice, and per-domain yield from `search_observations` is the
  obvious input once Build item 0's prerequisite 1 is recording it.
