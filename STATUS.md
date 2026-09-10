# Development Status

_Update this file as work progresses. The agent reads it every session to understand current context._

**Ticket numbers:** `docs/specs/TICKET_REGISTRY.md` (next: **#51**).  
**How to create / prioritize tickets:** `AGENT.md` → Creating a new ticket, Build queue.

---

## ⛔ SLOT POLICY — test1 is frozen, work happens on test2

**Set by the product owner 2026-09-10, after the first customer's positive feedback on the
India demo.** The rule is in `AGENT.md` too, because it governs every session:

> No change reaches test1 without the product owner's explicit approval, per instance.

| Slot | Commit | Role now |
|---|---|---|
| **test1** — `agent-test1.particletico.com` | tag **`test1-stable-2026-09-10`** (`c772df6`) | **Frozen.** The approved India demo, presented again from here. Read it freely; change nothing |
| **test2** — `agent-test2.particletico.com` | `main` @ `de67d92` | **Where development goes.** Currently far behind and with an empty RAG — see #52 |
| **prod** — `agent.particletico.com` | `de67d92` | Untouched since 2026-08-11. Holds the 141/9519 RAG corpus |

Approval is per change, not standing: an earlier "yes" does not cover the next deploy, and
neither does a fix being small, urgent, or obviously right. If something on test1 looks bad
enough to warrant an exception, ask — do not deploy and report afterwards.

Frozen covers anything that alters what test1 serves: `git pull` there, a rebuild or
restart, an `.env` edit, a migration on `agentic_test1`, an edit to the bind-mounted
`claude_agent_fe/` prompts, or publishing/unpublishing its shared topics. **Not** frozen:
the India topic's own monitoring cycle, which is the product working rather than a change —
it runs every 24 h at roughly $2.94 a cycle, ~$20/week, and one `PATCH /monitor` makes it
weekly if that is not worth it.

**Verify before assuming** — and note the `^{commit}`, which is not optional:

```bash
git rev-parse --short 'test1-stable-2026-09-10^{commit}'          # c772df6
ssh … 'cd ~/agent_bench_test1 && git rev-parse --short HEAD'      # c772df6
```

Without `^{commit}` the first command prints the **annotated tag object's** SHA (`2f48fe8`),
which matches nothing on the box and reads exactly like a drifted slot. Checked 2026-09-10:
the two agree.
The application still does not report its own build (`GET /v1/agent/info` returns no commit
SHA), so this comparison is the only check there is — the same half-an-anchor problem the
previous rollback section recorded twice, now against a slot that must not move.

### The old rollback anchor is retired

It read *"we are deliberately breaking a working, demoed system — roll back to `de67d92`"*.
That worry is answered: the breaking change shipped, ran, and the customer preferred the
result. `de67d92` is still what prod runs and is still reachable, but it is no longer the
state to protect. **`test1-stable-2026-09-10` is.**

---

## What the customer actually valued (2026-09-10)

First feedback on the India demo was positive, and the *shape* of it matters more than the
verdict:

- **The primary sources were the most interesting part — including one the system had
  ranked low on relevance.**
- **A Bloomberg article was less interesting, because it is not an official source.**

Read that against what we optimise. `primary_official` share is a counter we report;
**relevance** is what orders `news.json` and what `next_queries` tunes toward. The customer
ordered the same set differently: publisher class first, relevance second. A low-relevance
ministry page beat a high-relevance wire story.

Three consequences, none of them "raise the primary share" — that number is already moving:

1. **#46 (per-query yield)** — yield must be counted in *primary* documents, not documents.
   A query that returns ten well-matched secondary hits is close to worthless to this
   customer, and today it scores the same as one that surfaces a regulator's PDF.
2. **#23 (rubric)** — `information_discovery` weights relevance and authority as separate
   categories. The customer's ordering says authority dominates for a country-fundamentals
   topic. Before tuning against the rubric, check the rubric agrees with the buyer.
3. **#49 (discovery lane + promotion)** — the strongest argument yet for the unfiltered
   discovery budget: the value is in official sources we do not yet know about, and a
   closed register cannot find them. Promotion criteria should weight *class*, not clicks.

**Caveat, stated because it is one customer and one topic:** this is a preference expressed
once, about one country topic, by one desk. It is a hypothesis about what to optimise, not a
measured law — and it is exactly what the three-slot comparison (#52) exists to test.

---

## Build queue — Platform / Data (source pipeline)

_Order for improving search reliability and grounding. Separate from the V1 UI queue below; execute when platform work is the priority._

| Order | Ticket | Why now | Unblocks |
|------|--------|---------|----------|
| 1 | **#47** Register labels | The register carries no country, so `entities_named_in` routes an India topic into Iranian and Bangladeshi ministries. Makes selection a set query instead of a lexical guess | #46 Gate 3, #48, #49, safe `allowed_domains` |
| 2 | **#49** Discovery lane + promotion | A domain filter is a closed world; without a reserved unfiltered budget and a promotion path the register can never grow | Register growth, third channel |
| 3 | **#48** Topic bootstrap job | The India onboarding, automated — the work that recurs for every customer topic | Country #2 at acceptable cost |
| 4 | **#31** Scraping infrastructure | Social channel reads; the unbuilt half of #36's `execute_search` | Live social in deliver/refresh |

**Shipped:** **#29** whitelist (622 entries), **#30** playbooks (57), **#32** `apps/claude_agent/sources` + `/source-discover`, **#36** hybrid pipeline (`source_discover` pre-plan stage; `execute_search` documented, not built), **#42** search evidence capture + content fetcher, **#38** multilingual grounding, **#39** source authority.

**Retired 2026-09-08:** **#33** (superseded by #36) and **#35** (graph retrieval — the relational-retrieval problem is being answered as a labelled set query by #47 + #49, and #35's own start condition was never met). See the registry's Retired table.

**Dependency sketch (platform):**

```
#29 (done) ──► #30 (done) ──► #32 (done) ──► #36 (done) ──► #42 (done)
                                                  └──► #31 (scraping) ──► #36 execute_search
#47 (labels) ──► #48 (bootstrap) ──► country #2
            └──► #49 (discovery lane + promotion)
```

---

## Build queue (prioritized)

_Order for completing the **shipped V1 application** (Newsfind + UI + eval). Recompute with **technical-architect** when scope or business priority changes; ticket `#` is an ID, not priority._

| Order | Ticket | Why now | Unblocks |
|------|--------|---------|----------|
| — | ~~**#51** Report grounding~~ | **Shipped and verified on test1 2026-09-10.** Four defects surfaced on the first live run — the feed channel had never matched anything, deliver's corpus was 5 documents of 149, a PDF behind a download script was discarded, and the prompt matched the corpus on a key the agent cannot compute. All four fixed and redeployed | A report written from what we actually hold |
| 1 | **#45** India gas pilot | Second run delivered on test1 2026-09-10 with monitoring live and a shared link out. Remaining: two cycles of pile, then the operator review that turns it into a tuning list | Country-fundamentals expansion |
| 2 | **#52** Three-slot business comparison | The owner's next strategy. **test2 has no RAG (0/0 against 141/9519)**, so nothing can be compared until it does — that is item 1 of the ticket, and it is a prerequisite, not a step | A defensible "are we getting better?" answer |
| 3 | **#47** Register labels | **Demoted from demo-critical 2026-09-10.** Measured on both India runs' own `source_targets.json`: `entities: []` and **zero** `.ir`/`.bd` domains. The contamination needs an entity phrase this topic's parse leg does not emit — still the right fix, no longer in front of the demo | Safe `allowed_domains`, #46, #48, #49 |
| 4 | **#16** SignalGather frontend V1 *(16a–d verified through the API — **browser smoke pending**)* | A demo is a browser, and nothing in the UI has been driven in one | Pilot flow without curl; #37 |
| 5 | **#50** Live public sharing | A link that keeps updating is the cheapest demo we have. Implemented; needs prod migration + the logged-out browser pass | #37, public demos |
| 6 | **#22** Topic refresh scheduler *(code done, scheduled path never fired)* | The weekly pile is the product for a country topic | #16 monitoring, #20 |
| 7 | **#37** Pilot first-use experience | Make the journey self-explanatory before broad pilot acquisition | Self-serve onboarding |
| 8 | **#43** Claude LLM judge | Until this lands, no `--evaluator llm` number is worth tuning against | #23, #41 |
| 9 | **#23** Trading Intelligence Evaluation Framework | Lane A framework shipped; needs one live write-up. **Absorbs #18** | Pilot go/no-go narrative |
| 10 | **#21** Timeliness & channel metrics | Measurable inputs for the eval lanes | #23, #20 |
| 11 | **#20** Continuous monitoring evaluation | Lane A over time — needs #22 firing scheduled and #23's rubric | Longitudinal product proof |

**Suggested next pick:** **let the pile accumulate, then read it with the operator.** The India topic (`4a6a4504` on test1) is monitored at a 24 h cadence with a 7-day freshness window and one cycle already banked; #45's open acceptance criterion is *two* cycles that are non-empty and non-duplicative, and the criterion after that is the operator review — the one thing no counter substitutes for. **Cost check while it runs:** the first cycle was **$2.94**, so a daily cadence is ~$20/week; one `PATCH /monitor` moves it to weekly if that is not worth it. Then **#16**'s remaining browser pass — two of its gaps were closed on 2026-09-10 by opening the shared link (see below), but §5 (reconnect) and §11 (responsive) are still unexercised. **CI:** add GitHub secrets (`.github/README.md`) then run workflow "VPS E2E test1" for a live green artifact.

**Parallel (when deps met):** #21 after harness artifacts (#11); #23's write-up can start on `testing/results/test1/latest` with the heuristic evaluator; do not start #20 until **#22** has fired a scheduled cycle and **#23** has a rubric write-up.

**Dependency sketch:**

```
#11,#13,#15,#17,#19,#24,#40 (done) ──► #16 (16a–d built) ──► #37 ──► pilot acquisition
                            └──► #50 (implemented) ──► #37
#42,#38,#39 (done) ──► #45 (India) ──► #46 (loop) ──► #48 ──► country #2
                  └──► #47 (labels) ──┘        └──► #49
#22 ──► #16 monitoring · #20
#43 ──► #23 ──► #20 ;  #21 ──► #23, #20
```

---

## In Progress

### test1 slot — refreshed and verified 2026-09-01
- **Why:** test1 is where the current code gets judged, and it was judging nothing: the slot ran `feature/report-from-evidence` (`3ea0fbe`), schema stood at `0010`, and every relevant change (#45 encoding, #46 build item 0, #50) existed only in a local working tree.
- **The task shrank on inspection.** The RAG mirror was already done and still holds — prod and test1 agree byte for byte (`events_md5=8c74ea92…`, `summary_md5=76d06dd1…`, `docs_md5=1729f9b9…`, 141/9519 rows, tenant `0000…0001`, `ivfflat.probes=10`). Nothing was copied; the gap was code and schema.
- **Branch:** `feat/india-pilot-and-live-sharing` (`26d66fb` #45/#46, `c07038d` #50), pushed and checked out in `~/agent_bench_test1`. `main` untouched; prod untouched.
- **Schema:** `0010 → 0011 → 0012 → 0013`. **`0012_search_queries` and `0013_topic_share_mode` had never run on any database** — test1 is their first real application, and both applied clean. Corpus checksums are unchanged after the migrations, so nothing touched the corpus.
- **Env fixes on the slot** (`apps/claude_agent/.env`, backup at `.env.bak_before_test1_refresh`): `/newsfind-topic-parse` added to `CLAUDE_AGENT_ALLOWED_COMMANDS` (the #38 grounding gap noted during the #40 deploy — closed), `CLAUDE_AGENT_SCHEDULER_ENABLED=true`, and `CLAUDE_AGENT_DATABASE_URL` repointed from `agentic` to `agentic_test1`. **That third one was a live landmine:** the slot's env file named the *production* database and only the compose `environment:` block, which overrides `env_file:`, kept the app off it.
- **Ordering that matters for every future slot deploy:** `docker/Dockerfile` does `COPY database ./database`, so migrations are baked into the `rag_adhoc` image — **build before `alembic upgrade`**, or the upgrade silently sees only the migrations of the old image. That is why test1 sat at `0010`. Also: `scripts/devops/vps_setup_test_slot.sh` is **not** the tool for this — it overwrites `apps/claude_agent/.env` from prod and its `up -d` carries no `--build`.
- **Verified on the slot:** `alembic current = 0013`; `/readyz` ready (claude 2.1.197); `scheduler.started` in the boot log; RAG returns rows for an India query through `$RAG_BASE_URL` with the tenant header (proves corpus + tenant + embeddings together); `discover_sources_for_topic` **inside the deployed image** returns 32 known sources with all 9 India primaries and the `india_gas_demand.md` playbook; `/v1/agent/info` lists `/newsfind-topic-parse`; `/app`, `/app/shared`, `/app/shared/<id>` and public `report.md` all 200; anonymous `GET /v1/topics` 401 and every write verb on the public router 405.
- **#50 proven against real data, without spending:** the 0013 backfill flipped `9f2607da` to `share_mode=frozen` (it was shared under a fixed-state promise), the same owner call answers **409 while frozen and 200 while live**, and the public payload carries `share_mode` + `updates` with `cache-control: public, max-age=30` on GET (HEAD is 405 — the router is GET-only by construction). The topic is left **live** for the #40/#50 browser pass: `https://agent-test1.particletico.com/app/shared/9f2607da-4a94-494d-83bc-2af3ad9a8842`.
- **Correction to the plan's own expectation:** `available_actions` stays `[]` on a live share — `_actions()` returns `[]` for any `reported` topic, shared or not. The flip that actually proves control returned is the 409 → 200 on an owner write, which is what was measured.
- **Backup before the work:** `~/backups/agentic_test1_20260901_1627.dump` (78 MB, `pg_dump -Fc`).
- **Not done, deliberately:** no India topic has been run — that costs real money and is a separate decision. Prod is still at `0011` and does not have #45/#46/#50.
- **Next step:** run the India topic on test1 and read the source mix before touching anything else (`#45` next step), or drive `testing/ui_smoke_16.md` §7e against the live share.

### Report grounding (#51) — code shipped 2026-09-09, **not yet on a slot**
- **Spec:** `docs/specs/done/report_grounding_completion_51.md` · **Status:** done offline; slot verification open
- **What changed:** `run_deliver` exports the #42 evidence corpus the way `run_refresh` always did and passes `evidence_dir` / `evidence_count` / `evidence_unreadable_count`; `newsfind-deliver.md` reads the index before searching, prefers a corpus file over `WebFetch`, and keeps `current_state` + `rag_context_refs` as background that can never stand in for a citation; `search_content.py` reads `.xlsx`; feeds carry `collected_at` / `age_days` / `stale`; both legs emit `evidence_count`, `evidence_unreadable_count`, `feeds_count`, `facets_degraded`; `source_mix.json` is written and served so the UI stops computing a narrower figure of its own; `PATCH /monitor` can replace `short_term_queries`.
- **Two edits batched in, because they touch the same two prompt files:** #39's `thesis_status` divergence rule, reworded to stand on its own; and #46 build item 0's `next_queries` contract, which now carries `allowed_domains` so a filtered query does not lose its filter on the way into the monitoring plan.
- **One thing the ticket had wrong, and it mattered.** Item 5 said to key the signal on the facets' `degraded` flag. That flag never reaches the deliver leg: `run_topic_parse` writes the cache *only* on success, so a degraded parse arrives as a **missing** cache — and a parse that succeeds while naming neither a commodity nor a region blinds the feed channel just as completely without being flagged at all. `facets.feed_selection_blind()` covers all three.
- **Deploy note:** the prompt files are bind-mounted (`claude_agent_fe/`) and need no rebuild; `search_content.py` is baked into `docker/Dockerfile.claude_agent` and does. Build before restart.
- **Next step:** deploy to test1, run one India deliver, and read `stage.finished` for a non-zero `evidence_count` plus the expected `feeds_count`. Then the report itself: one quantitative claim citing a feed, one finding citing a document in `evidence_dir`. Do not deploy to the slot a customer is shown until a full topic has run on test1 and been read.

### Register labels (#47) — blocker for `allowed_domains`
- **Spec:** `docs/specs/active/register_labels_47.md`
- **Why:** `entities_named_in` matches on the **entity name** and never looks at the domain, so it cannot know a country exists. Iran's `mop.ir` matches an India topic because "Ministry of Petroleum" is a token-subset of "Ministry of Petroleum and Natural Gas"; Bangladesh's `mpemr.gov.bd` matches because `_name_variants` splits its name at the comma down to "Ministry of Power", and the topic supplies `ministry` (from the *petroleum* ministry) and `power` (from "power generation") **115 characters apart** — the phrase "Ministry of Power" never appears. `covers` is a set operation with no phrase structure.
- **Root cause is not the matcher:** the catalog (`docs/knowledge/source_catalog`, 1139 entries) carries `country` / `authority_type` / `signals`; `source_whitelist.json` kept only entity/domain/type/category/notes/agreement_count. **The labels were annotated and dropped at merge.** The matcher guesses lexically because the structured answer was taken from it.
- **Mostly free:** 527/622 whitelist domains rejoin the catalog by domain (495 with country, 443 authority_type, 527 signals). ~95 + the 12 India gas entries need hand-labelling. **213 catalog domains never merged at all.**
- **Then:** selection becomes a set query (`country=IN AND sector IN {gas,power}`) — deterministic and *enumerable*, which is what makes #46's Gate 3 possible. Playbooks declare label selectors instead of enumerating domains, so a new register entry is reachable immediately.
- **Next step:** write the rejoin script, triage the 213, then replace `entities_named_in` as the routing mechanism.

### Topic bootstrap job (#48) — the India onboarding, automated
- **Spec:** `docs/specs/active/topic_bootstrap_job_48.md` · **Needs #47 first**
- **Why:** onboarding India took a person plus an agent. That work recurs for every customer topic. It has been done twice before — the authority catalog and the 55 playbooks — both as one-offs for the whole world; this runs the same three legs for **one topic, on demand**.
- **The RAG leg is empty and nobody noticed.** The corpus is Yergin, *Oil Trading Manual*, *Petroleum Refining*, *Commodities Demystified*, OIES. **Not one document about how Indian gas works.** So #46's Gate 2 "draft from brief + RAG + web" has no RAG for any new topic. The job must acquire 5–15 explainers (IEA India Gas Market Report, PNGRB projections, PPAC methodology, the customer's Platts deck) and ingest them.
- **The authority skeleton is commodity-shaped, and ours is crude.** The catalog's 10 slots have nothing for demand statistics (PPAC), downstream regulation (PNGRB), transmission (GAIL), import terminals (Petronet), power dispatch (CEA/NPP) or consuming ministries. That is why India's catalog batch existed and was useless here. Roles must be derived from the value chain per topic.
- **Verification stays code, not judgment** — reachability + page identity, the step that refused `fert.gov.in` and `grid-india.in`.
- **Highest leverage and highest risk in the whole set** — every leg is generative. Guards: verify in code, `status: proposed` until a human signs, and **measure by the next run's primary share, not by how good the list reads.**

### Discovery lane and source promotion (#49) — so the register does not close in on itself
- **Spec:** `docs/specs/active/discovery_lane_and_promotion_49.md`
- **Why:** `allowed_domains` is a closed world. Reliable and, left alone, permanently blind — a source outside the register can never be found, so the register never grows. Unfiltered queries exist today **by accident**; they need a reserved budget (~25–30 %) and their own metric (**new-domain discovery rate**, not citations, or they get starved).
- **Nothing currently learns.** A brilliant unknown source is cited once and forgotten. But the evidence to judge it is **already stored** by #42 — `search_observations` (how many distinct queries, what rank, how many cycles), `search_queries` (did it appear *without* a filter), `fetch_status` (can we read it), `news.json#sources` + `source_quality.py` (was it cited, what class). Promotion needs **no new capture**.
- **Third channel, biggest lever:** known sources should not consume the search aperture at all. We know the ministry's URL — we need to poll it. #42's robots-respecting fetcher exists; it only lacks a second writer into `SearchDocument` (`search_evidence.py:66` is the only one, fed solely by WebSearch). That frees the whole budget for discovery.
- **Poisoning defence:** the model writes the summary, the **signals** decide — deterministic class, `fetch_status`, and repeated independent surfacing. Human gate on promotion; demotion recorded with a reason.


### Topic onboarding loop (#46) — the method for the ad-hoc phase
- **Spec:** `docs/specs/active/topic_onboarding_loop_46.md`
- **Lane:** Product / method — *how a new customer topic gets onboarded, measured and tuned*
- **Why:** we are deliberately bending the app per customer until the first desks are convinced. Without a loop, each demo produces a one-off hack and nothing accumulates. Five gates per topic (brief -> playbook -> register gap check -> dry run + measure -> tune one variable), three build items behind them.
- **The finding that drives it** (from `testing/baselines/hormuz_90d_2026-08-01`, #39 already live): Research Quality **4.59**, Trading Intelligence **4.36**, Information Discovery **2.90** — the heaviest-weighted layer is the weak one. Inside it, `non_obvious_source_discovery` **4.59** but `primary_source_discovery` **1.75**. Only **6/28** kept sources are `primary_official` (7/28 whitelisted) — but **5 of those 6 came from `site:`-scoped queries**, so the routing mechanism works and is merely low-yield. The failure is concentrated: 4 queries into Iranian/Saudi official sources (shana.ir, pmo.ir, mfa.gov.ir, mofa.gov.sa) returned 31 results and kept **zero**. **Whether that was junk or wrongly discarded is not determinable** — `drops` is three integers. That indeterminacy is the finding. Note the report is ~25 % primary while the #39 **refresh** hit 80 % — the delta cycle is better grounded than the foundational report, which matters because the pile is what the customer reads.
- **Build item 0, measured 2026-08-21 — the cheapest change found so far:** WebSearch takes a structured `allowed_domains` array (its only params are `query` / `allowed_domains` / `blocked_domains` — **there is no result-count parameter**, ~9-10 links per call regardless). We hold 622 domains and never pass them; domain targeting happens as hand-written `site:` text, one domain per query. Two near-identical India searches: plain → 9 links, **1 primary**; with `allowed_domains` on 10 India primaries → 10 links, **10 primary**, including PNGRB's own 2030/2040 demand projections, PPAC sectoral consumption and the Feb-26 industry consumption report. **This refutes the premise #45 was scoped on** — the operator's brief said Indian gas is forecast-poor; the regulator publishes projections to 2040, as PDFs generic search never ranks. Arithmetic: `site:` = 40 domains/cycle (~6 % of the register); `allowed_domains` = 40 × 10 = the whole register. **Prerequisite:** `search_evidence.py:91` recorded only the query — the domain list had to be captured *first*, or a domain search never returns becomes indistinguishable from one never asked for.
- **Build item 0 IMPLEMENTED 2026-08-22, in that order.** (1) New table `search_queries`: one row per WebSearch call **including empty ones** (`record_hits` used to return early on no hits, so a search that found nothing left no trace — "we asked and got nothing" looked exactly like "nobody asked"), with `allowed_domains` / `blocked_domains` / `hit_count`; `search_observations` gains nullable `query_id`. Migration `0012_search_queries` is head, chain verified, offline SQL cross-checked against the model DDL — **not applied to a real DB, Docker down locally** (same gap #42 shipped with). (2) `allowed_domains` flows plan -> monitoring plan -> search: `newsfind-plan.md` batches up to 10 domains per query and drops `site:` from query text, `build_short_term_queries` now carries + normalises the filter (it rebuilds entries from scratch, so it was silently dropping it), deliver/refresh pass it to WebSearch and record an empty filtered result instead of retrying unfiltered. Tests 331 -> 337 green. **Next: apply `0012` on a real DB, rebuild, run India (#45) and read the primary share.**
- **Build items, revised after finding #42 already shipped:** (1) ~~selection audit trail~~ **exists** — see the #42 entry below; the Iranian/Saudi zero-yield is now a *query* against `search_observations` + `fetch_status`, not a build. (2) **per-query yield** — join `search_observations` to cited `url_hash`; surface in the weekly pile so the operator's review edits `short_term_queries`. (3) **topic `shape`** (event vs standing) driving freshness defaults + evaluation profile. (4) **the judging pass over the captured corpus** — #42's explicit non-scope, and now the real gap behind "correctly filter".
- **Second structural finding:** `information_latency` **0.0** is not a defect — a 90-day topic scored on a 14-day decay curve. India is worse (PPAC is monthly by design). Fundamentals topics must be scored on the **delta**, not the foundational report.
- **Caveat on measurement:** every number above is the **heuristic** evaluator (provider-free). `--evaluator llm` still runs on OpenAI until **#43**; do not tune against it before then.
- **Next step:** run the five gates once, end to end, on India (#45) — the loop is only real if it survives its first topic.

### India gas — country fundamentals pilot (#45) — first run delivered on test1 2026-09-03
- **Spec:** `docs/specs/active/india_gas_country_pilot_45.md`
- **Lane:** Product / business value — *the first topic a paying prospect asked for*
- **Why:** first customer after the presentation asked for a **country** topic, not an event topic. Every run so far has been event-shaped (Hormuz). A country topic is a standing question whose output is a **weekly pile**, not a one-shot report. India was picked because it is data-visible but forecast-poor — the monthly balance is published, genuine forward views are scarce.
- **Operator brief:** ~200 mcm/d, roughly half LNG / half domestic; fertilizers ~50, city gas ~50, power generation, refineries; **city gas is the structural growth story** as new cities connect to the grid; Indian electricity generally is in scope.
- **Found while scoping — the #44 failure mode again:** `source_whitelist.json` held **15 India entries and not one gas-demand source** (no PPAC, no PNGRB, no GAIL, no Petronet, no IGX, no CEA). The gas story would have been answered from trade press because nothing authoritative was reachable.
- **What's done:** `local_knowledge_sources/playbooks/india_gas_demand.md` (56th playbook — balance, four demand blocks, CGD growth, triggers, cadence, topic-specific anti-patterns); **12 whitelist entries added (610 -> 622)**, every domain reachability- and identity-checked on 2026-08-20; topic string chosen by **measuring** `discover_sources_for_topic`, not guessing.
- **Topic string:** `India gas demand: city gas distribution growth, fertilizers, power generation, refineries; domestic production vs LNG` -> routes to `india_discounted_crude.md` + `india_gas_demand.md` + `japan_korea_lng_demand.md`, 32 known sources, all 17 India primaries reachable. Adding "Indian electricity" or "LNG imports" to the string displaces an India playbook with `china_oil_gas_imports.md` (`MAX_TOPIC_PLAYBOOKS = 3`) — the electricity angle is carried by the playbook, not the string.
- **What's missing:** playbook ingest (`document_type=playbook`); **image rebuild** (`docker/Dockerfile.claude_agent:49-50` bakes whitelist + playbooks, no volume mount — batch with #44); first end-to-end run; monitoring enabled at a weekly-review cadence; operator review of one pile -> tuning list.
- **Watch on the first run:** #39's two-tier freshness. PPAC is **monthly** and PNGRB event-driven, so a uniform window would delete the whole primary tier — the exact structural bug #39 fixed, and this topic is the first to stress it hard.
- **Known gap:** no dedicated fertilizer source (~25 % of demand) — `fert.gov.in` and `grid-india.in` were unreachable from the authoring host and were deliberately **not** whitelisted; fertilizer routes through PPAC's sector split until verified.
- **FIRST RUN, test1 2026-09-03** — topic `d19908b3`, plan $1.10 / 222 s + deliver $2.70 / 716 s = **$3.79**. Thesis `supported`, 8 key findings, 34 cited sources.
- **The mechanism moved the number it was built to move.** `primary_official` share of cited sources went from the Hormuz baseline's **6/28 (21 %)** to **18/34 (53 %)**; whitelisted 7/28 -> 17/34. The plan emitted 15 queries, **8 carrying `allowed_domains` (33 distinct domains) and zero using `site:` text** — the old mechanism is gone. 18 search calls recorded, 8 filtered, **none empty**: the standing worry that a domain filter returns nothing did not happen. 149 documents captured. 5 of 15 queries Hindi from an English brief (#38), same 33 % as Hormuz.
- **PPAC contributed zero sources — and #46's capture makes that determinate instead of a shrug.** Exactly one search call carried `ppac.gov.in`; it returned a full 10 hits, none from PPAC, while its three sibling domains in the same filter all returned documents. So register, filter and search all worked: the gap is **query design** — the only PPAC-filtered query was about *licensing rounds and policy* (DGH/MoPNG territory), and nothing asked for the **monthly consumption balance**, which is PPAC's actual asset. The report reached the same conclusion by itself, flagging under Risks that PPAC "was queried but did not surface a matching monthly release", leaving every granular June-2026 mmscmd figure resting on one brokerage note. **This is the first tuning item, and exactly the one-variable loop #46 exists to run.**
- **#39 two-tier freshness held** — the ticket's main worry. Monthly-cadence material survived: June-2026 monthly figures and IEA Q3-2026 projections are both in the report, which a uniform recency window would have deleted.
- **No #47 contamination in this run** — no Iranian or Bangladeshi domain appeared. The seven `.cn` domains are deliberate scope (competing Asian LNG demand sets the price India pays), and that query returned almost nothing usable, which is its own finding.
- **PPAC PROBED AND CRAWLED, 2026-09-05.** Reading the site changed the diagnosis. PPAC never fought us: `robots.txt` absent, and the sectoral-consumption `.xlsx` came back **HTTP 200, 142 KB, last-modified 27 Aug 2026** on one polite request with our own UA. Two things stood between the report and that data, and **neither is a query** — a domain-filtered search *does* reach ppac.gov.in but the index served **December 2024** as its newest monthly report, and the current numbers are `.xlsx`, which `search_content.py` records as `unsupported`. So the fix is #49's third channel: **we know the URL, so ask for it instead of searching for it.**
- **Built, not duplicated.** `source_crawler` already had the semi-automatic path (`browser-fetch` for CDN-blocked sources), `.xlsx` download support in `static_file.py`, and a JODI adapter for exactly this class of statistical agency. What was missing was one strategy: a source whose **page** is stable while its **file** is republished under a new timestamped name monthly — `static_file` needs a fixed URL, `opec_assetdb` needs a `{month}/{year}` template, and PPAC fits neither. New `adapters/landing_link.py` (~190 lines) plus `seeds/india_gas_official.py`. Verified end to end: `crawl --seed india_gas_official` wrote both files, re-run reported `unchanged` on the sha256, and the spreadsheet holds exactly the operator's demand split — **Fertilizer, CGD, Power, Refinery, Petrochemical, FY 2026-27**. 9 tests, full suite 371 green, ruff clean.
- **Not seeded on purpose:** PPAC's `consumption` and `production` pages build download links in JavaScript. They go through `browser-fetch`, where a person saves the file once — the adapter names that route when `discover` finds nothing, rather than guessing at a scripted download.
- **CONNECTED 2026-09-05.** The crawled workbook now reaches the analyst. Four pieces: `text_extract.xlsx_bytes_to_text` (openpyxl, **newly declared in `pyproject.toml`** — it was only ever a transitive dep, so the image would not have had it) and `spreadsheet` as a kind in `detect_kind`/`extract_text`; `source_crawler/extract.py` stops skipping `.xlsx`; new `topics/feeds.py` selects feeds per topic and copies them into the run dir; `feeds_dir` + `feeds_count` in **both** deliver and refresh `input.json`, with the two slash commands told to read them first.
- **Selection is a set comparison, not a judgement:** feed `commodity`/`region` against topic facets. A feed with no region is global (JODI); a topic with no facets gets **nothing**, because handing every feed to every run is how India gas tables end up sourcing a Hormuz question. 13 tests cover the negative cases.
- **`feeds_dir` had to be added to deliver, not just refresh** — the India report was a *deliver* run, and deliver never had `evidence_dir` either. That is a second, separate gap now visible: the foundational report is the one leg that reads neither the captured corpus nor (until now) anything we already hold.
- **Feeds live in `<state_dir>/feeds`, not the image.** `/state` is a bind-mounted volume, so the crawler can publish into it without a rebuild — right for monthly data, where an image rebuild is the wrong unit of freshness. `source_crawler` is deliberately **not** added to the runtime image; it stays an operator tool whose output the agent reads.
- **Still open:** `.xls` (pre-2007 OLE) has no converter, so `ppac_gas_lng_import` downloads but does not extract — recorded as `skipped: no converter for .xls`, not silently lost. Would need a second library (`xlrd`).
- **DEPLOYED TO test1 2026-09-05 (`41741ea`).** Image rebuilt (openpyxl present), crawl + extract + publish run in a container with the worktree mounted, `/state/feeds` holds the PPAC series (53.6 kB), boot clean with `scheduler.started`, `/readyz` ready. Verified **inside the container**: `export_feeds` selects the feed for an India-gas facet bag and **rejects it for a Hormuz-crude one** — the leak case, checked on the real slot rather than only in tests.
- **Two operational snags worth remembering:** the container runs as **uid 1001**, so `artifacts/` and `state_test1/feeds` must be chowned to it or crawl and publish both die on `PermissionError`; and `source_crawler` is in no image by design, so it runs via `docker compose run` with `-v $PWD/source_crawler:/app/source_crawler:ro`. Both are written up in `docs/ops/commands.md`.
- **SECOND RUN, test1 2026-09-10 — the chain finally runs end to end.** New topic `4a6a4504`, same measured topic string, on `50d2a12`. Plan 13 queries (8 domain-filtered, PPAC in one of them), deliver 11 min, **`primary_official` 16/25 (64 %)** against 18/34 (53 %) on 2026-09-03 and 6/28 (21 %) on Hormuz. Then one refresh cycle at **$2.94 / 605 s** with `evidence_count: 114` and `feeds_count: 1`, whose delta opens: *"PPAC's own sectoral-consumption feed (updated 27 Aug 2026) shows fertiliser gas use rising from 1399.7 to 1773.7 MMSCM and CGD from 1481.6 to 1780.1 MMSCM between April and August 2026"*. The monthly balance the operator brief is built on is in the output for the first time, and it came from the feed rather than a search.
- **The feed channel had never once matched.** PPAC's sidecar files the series `region: IN`; the parse leg writes `geo: ["India"]`; `feeds.matches` compared them as strings. Both the unit fixture and the 2026-09-05 in-container check spelled the country **twice** (`["IN", "India"]`), so every test passed against an input production never produces. Fixed in `c0cc930` (`REGION_SYNONYMS`, country codes only — a country is deliberately *not* widened into a macro region). **The 2026-09-03 run's missing PPAC therefore had two independent causes, not one:** query design, which #45 diagnosed correctly, and this, which no amount of query tuning would have reached.
- **`entities: []` on both runs — #47 is not demo-blocking.** The contamination in the rollback-anchor section needs the parse leg to emit "Ministry of Petroleum and Natural Gas"; on this topic string it emits no entities at all, and both runs' `source_targets.json` carry **zero** `.ir`/`.bd` domains. Still worth fixing, no longer in front of a customer.
- **Deliver's corpus was 5 documents out of 149.** The fetcher polls in the background and deliver starts seconds after the plan finishes, so `export_evidence` ran against a queue that had barely started; half an hour later the same topic held 108 fetched. Refresh never had the problem because a monitored topic's corpus was fetched during earlier cycles — which is why #51 shipped with it. `50d2a12` waits for the topic's own queue to drain (`deliver_corpus_wait_sec`, default 300) before exporting; every failure path still delivers a report.
- **PPAC's monthly report was being thrown away at the door.** `download.php?file=…ICR_OCT_25.pdf` is served as `application/octet-stream`, and `classify` believed the label — the publisher's own report recorded `unsupported` beside a PDF reader. `41f266a` sniffs the body when the declared type is ambiguous, with the URL's named extension as the second signal for workbooks.
- **Monitoring is live and the report is shared.** 19 short-term queries, `schedule_enabled` at 24 h with a 168 h freshness window (weekly review, daily collection), one cycle banked. Published `share_mode=live`: **https://agent-test1.particletico.com/app/shared/4a6a4504-a7bd-4e0f-ab88-cdff6119d1a6** — read-only, anonymous, and it keeps up as the topic does. Anonymous writes still 401.
- **Two frontend defects found by opening that link in a browser**, which is the check #16 has been missing. `89b5311`: the public client built URLs with `apiUrl`, so a shared link resolved against whatever slot the reader's browser had last picked — it breaks for exactly the colleagues most likely to be sent one. `c772df6`: `usePublicTopic` gated the *first* load behind tab visibility, so a link opened in a background tab showed a permanent skeleton.
- **Still open on this ticket:** a second cycle (the pile is one entry so far), the operator review that turns it into a tuning list, the fertilizer primary-source gap (~25 % of demand), and `ppac_gas_lng_import` — a `.xls`, so it downloads and does not extract, which leaves the import-dependence half of the brief without its own series.
- **Next step:** let one more cycle run, then put the pile in front of the operator. Cost is the input to the cadence decision: $2.94/cycle daily is ~$20/week, one `PATCH /monitor` from weekly.

### SignalGather frontend V1 (#16) — 16a–d built, unverified on a live agent
- **Spec:** `docs/specs/active/signalgather_frontend_v1_16.md` · **App:** `apps/signalgather_web/README.md`
- **Lane:** Product / frontend — *the user-facing topic journey on the shipped API*
- **What's done (code):** React 19 + TS + Vite + Tailwind SPA at `apps/signalgather_web/`, served by `claude_agent` at **`/app`** (same origin → no CORS in the deployed path).
  - **16a** JWT sign-in + self-register (#24), env picker, owner-scoped topic list, NL create, workspace status bar, live activity feed, plan review + Proceed/Cancel. Fetch-based SSE reader (`EventSource` can't send `Authorization`) with `from_seq` resume, backoff, `: done` = clean close.
  - **16b** Report reader (summary, thesis badge, body, thesis update, open questions, next queries), sources panel with relevance/class/sort/filter, `[s01]` citations resolved to links, and the **adaptive widget registry** — the agent declares presentation, the frontend needs no change per output type.
  - **16c** Monitoring panel (subscription vs schedule kept separate, freshness window, interval, pause/resume, manual refresh) and delta timeline with per-cycle detail loaded on open.
  - **16d** New-since-last-visit badge, per-group skeletons, retryable errors, responsive pass.
  - Artifacts are grouped (plan/report/monitor/deltas) with per-group event invalidation; nothing polls. Prose sanitized with DOMPurify.
  - Backend: `_mount_cors` / `_mount_web` + `CLAUDE_AGENT_CORS_ORIGINS` / `CLAUDE_AGENT_WEB_DIST`; `web` build stage in `docker/Dockerfile.claude_agent`; repo-root `.dockerignore`.
  - Agent contract: `claude_agent_fe/.claude/widgets.md`; plan/deliver/refresh prompts now emit fenced `markdown-ui-widget` blocks. Legacy `<EntityChips>`/`<Highlights>`/`<NewsCard/>` in artifacts already on disk still render.
  - Tests: 178 frontend (vitest) + 12 backend (`tests/topics/test_web_hosting.py`); typecheck, lint, build green.
- **Verified live on prod 2026-07-31.** Full journey exercised via API: topic created (JWT path), plan 375 s -> gate -> deliver 435 s -> `reported`, then two monitored refresh cycles. Widgets landed on the first run (5 fenced, 0 legacy, all types registered, all `news-card` ids resolving); all 25 report citations resolved against `news.json`; 33 % of plan queries were non-English from an English brief; the addendum provably did not modify the original report (byte-identical). Costs: report $3.36, refresh $1.41 / $1.86.
- **What is still unexercised:** the UI itself. Everything above went through the API. Nobody has driven `testing/ui_smoke_16.md` in a browser — §5 (reconnect) and §11 (responsive) remain the criteria no automated check can close. Scheduled refresh is also unexercised: `CLAUDE_AGENT_SCHEDULER_ENABLED=false` on prod, so only the manual path has run (same `run_refresh` code, differing only in `trigger`).
- **Also:** set `CLAUDE_AGENT_ALLOW_SERVICE_KEY_BYPASS=false` on any slot used as a real product surface — with the harness default an unauthenticated browser is the service role and sees every topic.
- **DEPLOYED TO PROD 2026-07-27** (commit `1672fe9`, `agent.particletico.com`): image builds the SPA, `/app` serves it over HTTPS, anonymous `/v1/topics` is 401, service key still 200, `readyz` ready. Deployed to **prod rather than test1** deliberately — at the time test1's RAG corpus was empty (0 documents vs 141 on prod). **No longer true (verified 2026-09-01):** test1 mirrors prod exactly — 141 documents / 9519 events, identical `md5` over both ids and summaries, same tenant `0000…0001`, same `ivfflat.probes = 10`. The RAG-grounded plan stage is exercisable on test1.
- **Two problems surfaced by the deploy, both fixed:** the anonymous-read exposure above, and `/newsfind-topic-parse` missing from prod's `CLAUDE_AGENT_ALLOWED_COMMANDS` (which would have silently degraded #38's grounding leg — caught by the boot warning added in this same work).
- **Still not exercised:** no topic has been run end to end on the new build. `CLAUDE_AGENT_SCHEDULER_ENABLED=false` on prod, so 16c's *scheduled* refresh path cannot be tested there until that is flipped (no subscription currently has `schedule_enabled`, so flipping it is safe); manual refresh works.
- **Next step:** work `testing/ui_smoke_16.md` end to end against `https://agent.particletico.com/app` — §7b (widgets), §7d (monitoring/deltas), §5 (reconnect) and §11 (responsive) are what unit tests cannot close.

### Live public sharing (#50) — implemented 2026-09-01, awaiting migration + deploy
- **Spec:** `docs/specs/active/live_public_sharing_50.md`
- **Lane:** Product / API + frontend — *a shared report that keeps up with its topic*
- **Why:** #40 made a topic shareable by making it dead. Publishing sets `is_public`, and from that instant `_mutable()` 409s proceed/cancel/subscribe/monitor/refresh **for the owner too**, monitoring is paused, its schedule cleared, and the scheduler + `run_refresh` skip the row. So the moment a report is good enough to show someone, it stops being current. The requirement is the opposite of a handover: public = **read-only presentation of the live state**, ownership and every control stay with the owner.
- **What changes:** `topics.share_mode` (`live` default | `frozen`), and the freeze becomes mode-scoped instead of publish-scoped — `_mutable`, `_actions`, the monitoring pause, the `refresh_locked` 409, the scheduler due-query and `run_refresh`'s skip all test `share_mode='frozen'` rather than `is_public`. Mode is picked at `POST /publish` and switched with a new `PATCH /publish`. Snapshot sharing survives for "as of the day we signed".
- **What must NOT change:** `is_public` stays the single predicate the anonymous router consults (the `1672fe9` analysis holds unchanged), and the public router stays GET-only — that, not the freeze, is what guarantees no anonymous request can cause a run. The guarantee is restated, narrower: a **frozen** shared topic can never spend; a **live** one spends only what its owner's own monitoring already spends; anonymous readers contribute to neither.
- **The real work — consistent live reads:** freezing gave read consistency for free. Two hazards replace it. (a) `run_deliver` sets `deliver_run_id` *before* the run writes anything (`pipeline.py:240`), so a re-run would 404 every public artifact for its duration and a failure would break the link permanently. (b) `run_refresh` inserts the delta row as `status="running"`, so the public listing would advertise a cycle minutes before its `report.md` exists. Rule: **the public view resolves only finished state** — a `public_deliver_run_id` pointer advanced (with `public_updated_at`) solely on successful completion, and public delta routes filtered to `completed`. A live report then advances atomically at cycle boundaries; the owner's routes keep reading `deliver_run_id` and still see work in flight.
- **Reader side:** public payload gains `share_mode` + `updates{live,last_updated_at,update_count,latest_seq}`; the refresh *schedule* stays private (a spend decision, not a finding). `/app/shared/<id>` polls the detail route every 60 s, only in live mode, only while the tab is visible, re-fetching artifacts only when the stamp moves — short cached GETs, not the anonymous long-poll #40 refused.
- **Shipped (code):** migration `0013_topic_share_mode` (`share_mode` default `live`, `public_deliver_run_id`, `public_updated_at`, `frozen_at`, check constraint, backfill); `models.is_frozen()` as the single "pinned" predicate; `POST /publish {mode}` + new `PATCH /publish {mode}`; `_mutable`/`_actions`/the monitoring pause/the `refresh_locked` 409 all keyed on frozen rather than shared; scheduler due-query and `run_refresh` skip frozen only (`refresh.skipped {reason: topic_frozen}`); `serving.advance_public_view()` as the one place the public pointer and stamp move, called from `run_deliver` and a completed refresh cycle; public payload gains `share_mode` + `updates{live,last_updated_at,update_count,latest_seq}` and serves artifacts through `public_deliver_run_id` with completed-only deltas and a 30 s `Cache-Control`. Frontend: visibility-gated 60 s poll in `usePublicTopic` that re-downloads research only when the stamp moves, mode choice + pin/unpin in `SharePanel`, Live/Snapshot badge and "N updates since you opened this" on the public pages, and owner-side copy that no longer claims a lockout on a live share.
- **Verified locally:** `pytest tests` 362 passed (50 in `test_public_sharing.py`), `vitest` 239 passed, `tsc` + `eslint` clean.
- **What's missing:** migration applied on test1/prod, and the browser pass — publish live → refresh as owner → logged-out tab picks the cycle up → pin → it stops moving → unpublish → 404.
- **Watch out on deploy:** the migration backfills existing published rows to `frozen` — test1's `9f2607da` was shared under a promise of "this exact state". Prod has nothing published, so there it is a no-op. Apply the migration **before** the restart, as #40 did: `0012_search_queries` → `0013_topic_share_mode`.

### Insurance & vessel-tracking source branch (#44) — planned
- **Spec:** `docs/specs/active/insurance_vessel_tracking_sources_44.md`
- **Lane:** Product / quality — *whether the report can answer the question it was asked*
- **Why:** the Hormuz baseline scores `primary_source_discovery` **1.8/5**, and the brief explicitly asks about war-risk premiums and whether underwriters withdrew cover. `source_whitelist.json` contains **no marine-insurance body at all** (602 `official` + 8 `data_feed`, none underwriting), and `strait_of_hormuz.md` names war-risk premiums as price driver #4 while routing them to *navies*. So the report answered the insurance question from trade press because nothing else was reachable.
- **Two causes, both must be fixed:** inventory (no such source in the whitelist) *and* routing — `entities_named_in` (`sources/whitelist.py:82-95`) only matches entities **literally named in the brief**, so a whitelist entry not referenced by a matched playbook is unreachable. **The playbook is the routing layer; the whitelist is only the register.**
- **Confirmed live 2026-08-10:** LMA states war cover *is* available (88 % of the Lloyd's marine war market still writing hull war risks) and that reduced traffic is driven by crew/vessel safety, not insurance availability; Lloyd's List separately debunks the "P&I clubs cancelled war risk cover" story (it was charterers' liability extensions only). The report's conclusion was right but undefendable on its own sourcing — exactly the gap #44 closes.
- **Also in scope:** demote/drop `nioc.ir` (P1 in the playbook, `site:nioc.ir` returned 0 across both #39 cycles); record the empty official-social section as blocked on #31.
- **Not a hot config change:** `docker/Dockerfile.claude_agent:49-50` bakes `source_whitelist.json` and `playbooks/` into the image (no volume mount), so this needs a rebuild + redeploy — do not land it on a slot about to be demoed.
- **Next step:** pick the free-publishing insurance tier (JWC/LMA, IG P&I, IUMI, IMB), wire it into the playbook, rebuild, then re-run `topic.txt` verbatim and compare with `scripts/evaluate_output.sh relative`.

### Topic refresh scheduler (#22)
- **Spec:** `docs/specs/active/topic_refresh_scheduler_22.md`
- **Lane:** Product / backend — *automatic refresh cadence per monitored topic*
- **What's done (code):** schedule fields on `TopicSubscription` + migration `0005_topic_schedule`; in-app async scheduler (`apps/claude_agent/topics/scheduler.py`) reusing `run_refresh`; `trigger` (`manual|scheduled`) on all `refresh.*` events; `POST`/`PATCH /monitor` schedule on/off + interval (default OFF, clamped to bounds); `GET /monitor` exposes `schedule_enabled`/`interval`/`next_refresh_at`/`last_scheduled_refresh_at`; lifespan start/stop gated by `CLAUDE_AGENT_SCHEDULER_ENABLED` + DB; 8 offline tests in `tests/topics/`; docs (testing README, scenario §7.2a, ops vps.md)
- **What's missing:** live VPS verification (scheduled refresh fires without manual POST on test1); optional `--scheduled` flag in `scripts/test_vector_runner.sh` / `test_refresh_cycle.sh`; enable on test1/prod
- **Next step:** Deploy to test1, run migration `0005`, set a 1h schedule on V001, confirm `scheduler.dispatch` + a `refresh.completed` with `trigger=scheduled`

### Trading Intelligence Evaluation Framework (#23)
- **Spec:** `docs/specs/active/trading_intelligence_evaluation_23.md`
- **Lane:** A — *Is the deliverable valuable for users' business decisions?* (**absorbs #18**, retired 2026-09-08)
- **What's done:** `libs/eval_framework/` package — configurable 3-layer/14-category rubric (Information Discovery 40% / Research 30% / Trading 30%, 0–5), absolute + relative (Better/Equal/Worse) modes, win-rate aggregation, offline deterministic `HeuristicEvaluator` + `LLMEvaluator` (Output Quality Curator), pluggable benchmark-provider registry, `quality_review.{json,md}` rendering, CLI (`python -m eval_framework`) + `scripts/evaluate_output.sh`, rubric doc (`testing/output_evaluation_rubric.md`), 25 offline tests in `tests/eval/`
- **What's missing:** one **LLM-judge** write-up on `test1/latest` referencing a #15 PASS; adoption in pilot go/no-go; optional #21 timeliness/channel hints wired into latency scoring
- **Next step:** Run `scripts/evaluate_output.sh absolute --run-dir testing/results/test1/latest --evaluator llm` on a technically-passing run and attach the verdict to the pilot checklist

### Continuous monitoring evaluation & valuable-update feedback (#20)
- **Spec:** `docs/specs/active/continuous_monitoring_evaluation_20.md`
- **Lane:** A — *monitoring-over-time variant of #23* (#18 retired 2026-09-08, absorbed by #23)
- **What's done:** Gap framed; two modes (A: `/refresh` smoke, B: scheduler window + timeline + retrospective P4); `monitoring_timeline.json` + evaluator bundle specified
- **What's missing:** Timeline assembly, Mode B harness, monitoring-quality rubric, valuable-update labels, one retrospective evaluator run
- **Next step:** After #22 cadence exists, run one monitoring window on test1 → assemble timeline → P4 evaluator review

### Timeliness & source-channel coverage metrics (#21)
- **Spec:** `docs/specs/active/timeliness_channel_metrics_21.md`
- **Lane:** Instrumentation — *feeds #15, #23, #20*
- **What's done:** Gap framed (no time-to-surface or channel-coverage metrics today); metric definitions drafted
- **What's missing:** `timeliness`/`channels` blocks in `evaluation.json`, field docs, verification on a real run
- **Next step:** Implement metric calculators in `scripts/test_vector_runner.sh` and document fields in `testing/README.md`

### Multi-run evaluation baseline (#41)
- **Spec:** `docs/specs/active/multi_run_evaluation_baseline_41.md`
- **Lane:** A — *methodology for #23*
- **Why:** `testing/baselines/hormuz_90d_2026-08-01` is one run of one topic against a pipeline that searches the live web. The variance was never measured, so a future ±0.3 delta cannot be attributed to the code rather than the news cycle. Worse, four of the five categories carrying 40 % of the rubric weight are web-dependent, and `information_latency` is scored against run time so every later run is penalised for existing later.
- **What's needed:** noise floor from N≥3 repeat runs; baseline as M topics × N runs seeded from `testing/vectors.json`; verdict by `aggregate` win rate rather than single delta; a decision on the time-coupled latency category; structural vs discovery quality reported separately; prod runs written to `testing/results/prod/<timestamp>/` without hand-assembly.
- **Cost:** ~14 min and ~$3.40-equivalent per run; a 3×3 set is ~9 runs, ~2 h.
- **Next step:** Not started by request — build the testing later.

**Execution rule:** Agents execute only `docs/specs/active/*_<n>.md` tickets. Move completed tickets to `docs/specs/done/`.

---

## Known Bugs

### RESOLVED 2026-07-27 — topic API was readable without credentials on prod
- **Symptom:** `GET https://agent.particletico.com/v1/topics` returned all 6 topics to any caller, no credentials.
- **Cause:** `docker-compose.yml` listed `CLAUDE_AGENT_API_KEY: ${CLAUDE_AGENT_API_KEY:-}` under `environment:`, which **overrides `env_file:`**. The root `.env` never defined it, so the key set in `apps/claude_agent/.env` was replaced with `""`. `_service_key_accepted` treats an empty key as "accept everyone" while the bypass is on, so every anonymous request became the service principal — which by design sees every topic. Nothing failed or 500'd; the API just answered strangers.
- **Fixed:** commit `1672fe9` — the key is no longer passed through `environment:` (env_file owns it), and `_warn_on_open_topic_api` logs an error at boot if the combination recurs. Prod remediated live before the commit.
- **Watch for:** the same `${VAR:-}` override pattern on any other secret in `docker-compose.yml`.

### RAG env vars dropped on container recreate
- **Symptom:** `rag_context_refs: []` + `"RAG unavailable — no .env configuration found"`
- **Cause:** `docker compose up --force-recreate` drops env injection for `claude_agent`
- **Workaround:**
  ```bash
  docker compose up -d --force-recreate claude_agent
  docker compose exec claude_agent sh -lc 'env | grep -E "^RAG_"'
  # if blank: check docker-compose.yml env_file order for claude_agent
  ```
- **Full debug steps:** `docs/ops/debugging.md` → "RAG unavailable" section

### Cancel does not abort an in-flight run
- **Symptom:** `POST /v1/topics/{id}/cancel` during planning/delivering returns `cancelled`, but the topic later reappears at `planned_awaiting_review`/`reported`.
- **Cause:** the background plan/deliver task (and its Claude subprocess) is not cancelled; it runs to completion and re-sets state via `set_state`.
- **Impact:** cancel is only reliable from a gate/terminal state; mid-run cancel does not stop token spend.
- **Found:** #17 Lane B smoke (2026-06-02). Fix needs cooperative cancellation of `run_plan`/`run_deliver`.

---

## Recently Completed

| What | Date | Spec |
|---|---|---|
| **#51 Report grounding** — deliver leg exports the #42 corpus and keeps the plan's RAG context; `.xlsx` readable in the search path; feed staleness marked; `evidence_count` / `feeds_count` / `facets_degraded` on both legs' events; one `source_mix` definition, served as a file to owner and public views; `PATCH /monitor` can change the query plan. **Offline only — no slot run yet** | Sep 9, 2026 | `docs/specs/done/report_grounding_completion_51.md` |
| **#40 Public topic sharing** — anonymous GET-only router, per-row opt-in, all four write verbs 405; deployed prod + test1. Freeze half superseded by #50 | Aug 1, 2026 | `docs/specs/done/public_topic_sharing_40.md` |
| **#42 Search evidence capture + content fetcher** — `search_documents` / `search_observations` / `search_queries`, robots-respecting fetcher, per-domain accessibility map; ~89 % read rate measured in prod. **Judging pass deliberately out of scope** → #46 item 4 | Aug 2, 2026 | `docs/specs/done/search_evidence_capture_42.md` |
| **#39 Source authority enforcement** — `source_quality.py`, two-tier freshness, authority-aware ranking, confidence caps; refresh source mix 0 % → 80 % primary/official on prod. Residual `thesis_status` rule batched with the next prompt change (#45) | Jul 31, 2026 | `docs/specs/done/source_authority_enforcement_39.md` |
| **#38 Multilingual topic grounding** — diacritics folding, Unicode tokenizer, `topic_parse` leg; deployed on prod (`1672fe9`) and test1 (2026-09-01) | Sep 1, 2026 | `docs/specs/done/multilingual_topic_grounding_38.md` |
| **#29 Source whitelist seed** — `source_whitelist.json`, 622 entries, baked into the image; top-20 sign-off absorbed into #47 | Sep 8, 2026 (closed out) | `docs/specs/done/source_whitelist_seed_29.md` |
| **#24 Topic user ownership** — `owner_user_id` + migration `0006`; JWT auth on all topic routes; service-key bypass for harness; verified on test1 | Jul 26, 2026 | `docs/specs/done/topic_user_ownership_24.md` |
| **#36 Hybrid pipeline orchestration** — Python `source_discover` pre-plan stage writes `source_targets.json`; deterministic topic→entity resolution (no LLM); plan agent consumes pre-resolved domains; `execute_search` contract documented only | Jul 24, 2026 | `docs/specs/done/hybrid_pipeline_orchestration_36.md` |
| **#32 `/source-discover`** — Python `apps/claude_agent/sources` (whitelist + local playbooks) + Cursor skill; CLI `python -m apps.claude_agent.sources`; pipeline wire-up = #36 | Jul 23, 2026 | `docs/specs/done/source_discover_skill_32.md` |
| **#30 Coverage playbooks seed** — 55 playbooks in `local_knowledge_sources/playbooks/`; ingest `document_type=playbook`; Meta-RAG ready (pipeline wiring = #36) | Jul 23, 2026 | `docs/specs/done/coverage_playbooks_seed_30.md` |
| **#25 Slim main — archive legacy stack** — tag `archive/pre-slim-2026`, branch `archive/signal_gather-platform`; removed `signal_gather` + CrewAI deps; slim compose | Jun 16, 2026 | `docs/specs/done/slim_main_archive_25.md` |
| **#15 Application verification** — `qa_rules.json`, extended gate (16 checks), `tests/qa/`, fixtures; V001 `test1/latest` `qa_report.json` PASS; stage checks fixed for spaced NDJSON | Jun 2, 2026 | `docs/specs/done/newsfind_application_verification_15.md` |
| **#17 Backend V1 pilot-ready** — `GET /v1/topics` deployed; vector run QA PASS on test1; Lane B smoke (concurrent ✅, webhook+HMAC ✅, cancel mid-run ⚠️ gap); 2 harness bugs fixed | Jun 2, 2026 | `docs/specs/done/pilot_ops_v1_17.md` |
| **#11 RAG full stable evaluation** — vector runner, recovery, `evaluation.json` | May 27, 2026 | `docs/specs/done/rag_full_stable_evaluation_11.md` |
| **News Pipeline v2 — monitor & refresh** — `/monitor`, `/refresh`, `/deltas`, `/newsfind-refresh` | May 2026 | `apps/claude_agent/topics/refresh.py`, `testing/app_testing_scenario.md` §7 |
| **#10 RAG main corpus (highest ROI)** — download, chunk, ingest (66 docs / 3090 events) | May 22, 2026 | `docs/specs/done/rag_main_corpus_highest_roi_10.md` |
| Reproducible run artifacts + token-aware cache for `/newsfind-queries` | May 9–10, 2026 | `docs/specs/done/reproducible_artifacts_and_cache.md` |
| News pipeline v1 deployment to VPS (topic orchestrator + event stream) | May 2026 | `docs/specs/done/deployment_newsfind_pipeline_v1.md` |
| Non-root container user migration (UID 1001) | May 2026 | `docs/ops/debugging.md` |

---

## Blocked / Parked

_(nothing currently)_
