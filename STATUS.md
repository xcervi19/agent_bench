# Development Status

_Update this file as work progresses. The agent reads it every session to understand current context._

**Ticket numbers:** `docs/specs/TICKET_REGISTRY.md` (next: **#51**).  
**How to create / prioritize tickets:** `AGENT.md` → Creating a new ticket, Build queue.

---

## ⚠️ ROLLBACK ANCHOR — read before deploying anything from 2026-08-22 onward

**We are deliberately breaking a working, demoed system.** #45 and #46 change the search
path itself; the first customer's decision rests on the build that was demoed. Write the
way back down before taking it, not after.

| | |
|---|---|
| **Last commit before we started changing things** | `de67d92` — *"#44 Plan the insurance and vessel-tracking source branch"* (2026-08-11). Docs only. |
| **Last commit that touched application code** | `5b6d689` — *"Send a citation click to the source it cites"* (2026-08-11) |
| **`origin/main`** | `de67d92` — local `main` and `origin/main` agree; nothing unpushed |
| **The demoed UI is in here** | `5b99c26` Particle TICO rename, `27c6ad8` activity feed, `5b6d689` citation click — all 2026-08-10/11 |

**Roll back to `de67d92`.** It is the last state that was working and presented, and being
docs-only it is code-identical to `5b6d689`.

### What is NOT verified, and cannot be from here

**Nobody has confirmed which commit prod is actually running.** The last prod deploy this
file records is `bb924d7` (2026-08-01, #40) — which predates #42, the Particle TICO rename
and everything since. Either prod is genuinely on `bb924d7` and the demo ran on an older
build, or it was deployed later and no one wrote it down. The operator believes the last
working pre-presentation commit is what is deployed; that is a belief, not a check.

**The application does not report its own build.** `GET /v1/agent/info` returns Claude
binary, workspace and limits — no commit, no build SHA. So the running system cannot be
asked what it is. A rollback anchor you cannot compare against production is half an anchor.

Confirm before deploying:

```bash
ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212
cd ~/agent_bench && git rev-parse --short HEAD && git status --short
docker compose ps
```

Then record the answer here. **Consider adding the build SHA to `/v1/agent/info`** — this
is the second time the deployed state has had to be reconstructed from memory.

### What lands next, and why it is not reversible by `git revert` alone

- **Migration `0012_search_queries`** — a schema change. Rolling back the code does not roll
  back the database. `downgrade()` is written and tested offline, but has never run.
- **`source_whitelist.json` + `playbooks/` are baked into the image**
  (`docker/Dockerfile.claude_agent:49-50`, no volume mount) — a rebuild is required, and a
  rollback is another rebuild, not a restart.
- **Prompt contract changes** in `newsfind-plan.md` / `-deliver.md` / `-refresh.md` change
  how every topic searches, including topics already monitored.

**Do not deploy any of this to the slot the customer sees until India (#45) has run on a
non-demo slot and been read.** #44 touches the same baked files — batch the rebuilds.

**And do not ship `allowed_domains` before #47.** The domain filter turns the register from
a list into an instruction. Today that instruction would send an India gas topic to `mop.ir`
(Iran) and two Bangladeshi power ministries — they would burn slots in a batch of 5–8,
return nothing, and fill `search_queries` with zero-hit rows that look like dead sources
rather than misrouting. The evidence layer shipped 2026-08-22; the filter waits for labels.

---

## Build queue — Platform / Data (source pipeline)

_Order for improving search reliability and grounding. Separate from the V1 UI queue below; execute when platform work is the priority._

| Order | Ticket | Why now | Unblocks |
|------|--------|---------|----------|
| 1 | **#31** Scraping infrastructure | Social channel reads; fills the #36 `execute_search` contract | Live social in deliver/refresh |
| — | **#33** Plan source integration | **Superseded by #36** — do not implement separately | — |
| later | **#35** Graph retrieval layer | v2 after #36 MVP measured | Precision on relational topics |

**Shipped:** **#30** playbooks, **#32** `apps/claude_agent/sources` + `/source-discover` skill, **#36** hybrid pipeline (`source_discover` pre-plan stage; `execute_search` documented, not built). **#29** whitelist mostly done; finish commit + top-20 sign-off.

**Dependency sketch (platform):**

```
#29 (whitelist, mostly done) ──► #30 (playbooks, done) ──► #32 (discover, done) ──► #36 (hybrid pipeline, done)
                                                                              └──► #31 (scraping) ──► #36 execute_search
#35 (graph) — after #36 quality baseline
```

---

## Build queue (prioritized)

_Order for completing the **shipped V1 application** (Newsfind + UI + eval). Recompute with **technical-architect** when scope or business priority changes; ticket `#` is an ID, not priority._

| Order | Ticket | Why now | Unblocks |
|------|--------|---------|----------|
| 1 | **#22** Topic refresh scheduler *(in progress — code done, VPS verify pending)* | Automatic monitoring cadence — product expectation for pilot; #16's monitoring UI is its first user-facing surface | #16 monitoring, #20 |
| 2 | **#16** SignalGather frontend V1 *(16a–d verified on prod via API — **browser smoke pending**)* | User-facing setup, approval, report, and monitoring journey on shipped API (#17, #24 done) | Pilot flow without curl; #37 |
| 3 | **#37** Pilot first-use experience | Make the completed topic journey self-explanatory and trustworthy before broad pilot acquisition | Self-serve pilot onboarding |
| 4 | **#50** Live public sharing | Removes the #40 freeze: a shared report stays live and owner-controlled. A link that keeps updating is the cheapest demo we have, and today sharing one costs the owner their monitoring | #37 (a prospect-facing link), public demos |
| 5 | **#21** Timeliness & channel metrics | Measurable inputs for eval lanes | #18, #20 (richer verdicts) |
| 6 | **#23** Trading Intelligence Evaluation Framework | Lane A — runnable framework (generalizes #18); offline + LLM judge | Pilot go/no-go narrative; version-vs-version verdicts |
| 7 | **#18** Business output evaluation | Lane A rubric/playbook narrative — folded into #23 framework | Pilot go/no-go narrative |
| 8 | **#20** Continuous monitoring evaluation | Lane A over time — needs scheduler + rubric | Longitudinal product proof |

**Suggested next pick:** **drive `testing/ui_smoke_16.md` in a browser against prod `/app`.** The full pipeline is now verified end to end on prod *through the API* (plan -> gate -> report -> two refresh cycles, #39 included), so what remains unproven is the UI itself — reconnect (§5) and responsive (§11) are the criteria no automated check can close. Then **#37** (first-use, loading/error/recovery, return-use clarity, new-account pilot smoke) before broad pilot acquisition. **#22**'s scheduled path is still unexercised (`CLAUDE_AGENT_SCHEDULER_ENABLED=false` on prod); it shares `run_refresh` with the verified manual path, differing only in `trigger`. **CI:** add GitHub secrets (`.github/README.md`) then run workflow “VPS E2E test1” for a live green artifact.

**Parallel (when deps met):** #21 after harness artifacts (#11); #18 can start rubric using `testing/results/test1/latest` (Lane B PASS); do not start #20 until **#22** + **#18** rubric exist.

**Dependency sketch:**

```
#11,#13,#15,#17,#19,#24 (done) ──► #16 (16a–d built) ──► #37 (pilot first-use) ──► pilot acquisition
                       └──► #22 ──► #16 monitoring verified on test1
                       └──► #21 ──┐
#15 PASS (test1/latest) ───────► #18 ──► #20
#22 + #18 + #21 ───────────────────────────► #20
```

---

## In Progress

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

### India gas — country fundamentals pilot (#45) — encoding done, not yet run
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
- **Next step:** ingest the playbook, rebuild + deploy (with #44), run the topic once, read the source mix before touching anything else.

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
- **DEPLOYED TO PROD 2026-07-27** (commit `1672fe9`, `agent.particletico.com`): image builds the SPA, `/app` serves it over HTTPS, anonymous `/v1/topics` is 401, service key still 200, `readyz` ready. Deployed to **prod rather than test1** deliberately — test1's RAG corpus is empty (0 documents vs 141 on prod), so the RAG-grounded plan stage cannot be exercised there at all.
- **Two problems surfaced by the deploy, both fixed:** the anonymous-read exposure above, and `/newsfind-topic-parse` missing from prod's `CLAUDE_AGENT_ALLOWED_COMMANDS` (which would have silently degraded #38's grounding leg — caught by the boot warning added in this same work).
- **Still not exercised:** no topic has been run end to end on the new build. `CLAUDE_AGENT_SCHEDULER_ENABLED=false` on prod, so 16c's *scheduled* refresh path cannot be tested there until that is flipped (no subscription currently has `schedule_enabled`, so flipping it is safe); manual refresh works.
- **Next step:** work `testing/ui_smoke_16.md` end to end against `https://agent.particletico.com/app` — §7b (widgets), §7d (monitoring/deltas), §5 (reconnect) and §11 (responsive) are what unit tests cannot close.

### Public topic sharing (#40) — deployed to test1 + prod, browser pass outstanding
- **Spec:** `docs/specs/active/public_topic_sharing_40.md`
- **Lane:** Product / API + frontend — *a finished topic leaving the account that made it*
- **Why:** a report is worth something to more people than its owner, but everything under `/v1/topics/*` is owner-scoped (#24) and no UI route renders without a session. The two constraints that shaped the design: anonymous read must be **per-row opt-in**, not a config flag (the 2026-07-27 incident, `1672fe9`, was exactly the loose version), and no anonymous request may cause a Claude run — we do not check permissions before spending, there is simply no route that spends.
- **Shipped (code):** migration `0007_topic_public` (`is_public` NOT NULL default false, `published_at`, partial index); `POST|DELETE /v1/topics/{id}/publish`; `_mutable()` → 409 on proceed/cancel/subscribe/monitor/refresh while published, `available_actions` empty; publishing pauses monitoring + clears its schedule, and is itself refused while a cycle is in flight; scheduler due-query and `run_refresh` both skip published topics; new **GET-only, auth-free** router `/v1/public/topics/*` (list + detail + plan/report/news artifacts + deltas, no SSE, no owner/run-id leakage); `serving.py` shared by both routers. Frontend: `/app/shared` + `/app/shared/<id>` render with no session via a token-free client (`lib/publicApi.ts`), Share tab + published banner, monitoring/plan panels explain the freeze. 24 backend + 17 frontend tests (`tests/topics/test_public_sharing.py`, `publicApi.test.ts`, `SharePanel.test.tsx`, `PublicTopicPage.test.tsx`).
- **Verified on test1 (2026-08-01, `fda0876`):** migration `0006 -> 0007` applied, images rebuilt, boot clean. Anonymous `GET /v1/topics` **401**; anonymous `GET /v1/public/topics` **200** listing only the published row; all four write verbs on the public router **405**; report/news/parsed/intro/deltas all readable with no credentials; refresh/proceed/cancel/monitor **409 with a valid service key**; unpublish → 404 + empty listing + owner regains control. Details in the spec.
- **Deployed to prod (2026-08-01, `bb924d7`):** migration applied before the restart; boot clean. All 8 existing topics `is_public = f` — the deploy published nothing. Anonymous `GET /v1/topics` **401**, `GET /v1/public/topics` **200 but empty**, all four write verbs **405**, and a *real* unpublished prod topic **404s** on every public route. `/app/shared` resolves.
- **What's missing:** browser pass of `testing/ui_smoke_16.md` §7e in a logged-out window — the DevTools check (only `GET /v1/public/topics/*`, no `Authorization` header) is the one no automated check closes.
- **Next step:** browser check on `https://agent-test1.particletico.com/app/shared/9f2607da-4a94-494d-83bc-2af3ad9a8842` (left published on test1). Nothing is shared on prod; that stays each owner's decision.
- **Noticed while deploying (unrelated):** test1's `CLAUDE_AGENT_ALLOWED_COMMANDS` still lacks `/newsfind-topic-parse`, so #38's grounding leg degrades on that slot; prod got it in `1672fe9`. Also, the test1 worktree was carrying a stale destructive index (82 staged deletions) — stashed as `test1 slot-local before #40 deploy`, recoverable with `git stash pop`.

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

### Search evidence capture + report-from-evidence (#42) — shipped, running in prod, **undocumented here until 2026-08-20**
- **Spec:** `docs/specs/done/search_evidence_capture_42.md` (status says done 2026-08-02; the spec is **stale** — see below)
- **Lane:** Platform / backend — *content acquisition and processing of everything search returns*
- **What it does:** every hit web search returns is captured — `search_documents` (dedup per topic+URL) and `search_observations` (append-only per query/run/rank) — then `search_content.py` reads the page behind it in the background under a self-identifying, robots-respecting client. Outcomes are first-class data, not errors: `fetched` / `thin` / `blocked` / `not_found` / `disallowed` / `unsupported` / `error`, accumulating into a **per-domain accessibility map**. JSON-LD `articleBody` and PDFs are read; one retry on 429/503. No verdict at capture time — by design.
- **Then `3ea0fbe` closed the loop:** the corpus is exported into the run dir (one file per document, provenance front matter + index) and the refresh command reads it **before** WebFetch and prefers it — "WebFetch returns a model's answer to a prompt, a corpus file is the article". Unreadable documents are counted in the index so absence is not mistaken for silence.
- **Query breadth:** the plan was capped at a literal `12` in three places — now `settings.refresh_max_queries`, **default 40**. The cap, not fetch success, is what bounds corpus size.
- **Measured in prod:** ~9 links per query, **~89 % read successfully**, last pre-change run = **121 documents** averaging ~16k chars. `ab6b98f` (NUL bytes breaking an asyncpg INSERT) was diagnosed against a 29k-char article in prod.
- **The spec is stale on two points:** it says "migrations not yet applied" and "the fetcher has never run against the live web". Both were true on 2026-08-02 and are not true now.
- **What #42 deliberately did NOT do:** the judging pass over the corpus. Recording is separate from using; the strategy for a cheap model reading the articles is **not designed**. That is now the real gap behind "correctly filter" in the business requirements.
- **Why this matters for #46/#45:** the Hormuz baseline (2026-08-01) is the last run *before* this landed, so its opaque `drops` describe a system state that no longer exists. Any claim about "we cannot tell what was discarded" must be re-checked against a post-#42 run.

### Insurance & vessel-tracking source branch (#44) — planned
- **Spec:** `docs/specs/active/insurance_vessel_tracking_sources_44.md`
- **Lane:** Product / quality — *whether the report can answer the question it was asked*
- **Why:** the Hormuz baseline scores `primary_source_discovery` **1.8/5**, and the brief explicitly asks about war-risk premiums and whether underwriters withdrew cover. `source_whitelist.json` contains **no marine-insurance body at all** (602 `official` + 8 `data_feed`, none underwriting), and `strait_of_hormuz.md` names war-risk premiums as price driver #4 while routing them to *navies*. So the report answered the insurance question from trade press because nothing else was reachable.
- **Two causes, both must be fixed:** inventory (no such source in the whitelist) *and* routing — `entities_named_in` (`sources/whitelist.py:82-95`) only matches entities **literally named in the brief**, so a whitelist entry not referenced by a matched playbook is unreachable. **The playbook is the routing layer; the whitelist is only the register.**
- **Confirmed live 2026-08-10:** LMA states war cover *is* available (88 % of the Lloyd's marine war market still writing hull war risks) and that reduced traffic is driven by crew/vessel safety, not insurance availability; Lloyd's List separately debunks the "P&I clubs cancelled war risk cover" story (it was charterers' liability extensions only). The report's conclusion was right but undefendable on its own sourcing — exactly the gap #44 closes.
- **Also in scope:** demote/drop `nioc.ir` (P1 in the playbook, `site:nioc.ir` returned 0 across both #39 cycles); record the empty official-social section as blocked on #31.
- **Not a hot config change:** `docker/Dockerfile.claude_agent:49-50` bakes `source_whitelist.json` and `playbooks/` into the image (no volume mount), so this needs a rebuild + redeploy — do not land it on a slot about to be demoed.
- **Next step:** pick the free-publishing insurance tier (JWC/LMA, IG P&I, IUMI, IMB), wire it into the playbook, rebuild, then re-run `topic.txt` verbatim and compare with `scripts/evaluate_output.sh relative`.

### Source authority enforcement (#39)
- **Spec:** `docs/specs/active/source_authority_enforcement_39.md`
- **Lane:** Product / quality — *what a report is allowed to stand on*
- **Why:** the first monitored refresh on prod returned 8/8 secondary sources, 0 primary, 0 whitelisted — including Russian state media behind its highest-confidence finding. Cause was not grounding: four queries were site-scoped to official domains, returned three hits, and all three were dropped as `too_old`. Primary sources publish on an event cadence, news outlets continuously, so a uniform freshness window structurally deletes the authoritative tier.
- **Shipped:** `topics/source_quality.py` (deterministic `SourceMix`, emitted on `report.ready` / `refresh.completed`, no migration); two-tier freshness + authority-aware ranking + confidence caps + mandatory source-mix statement in the deliver/refresh contracts; `SourceMixNote` in the report and every delta detail. 23 backend + 6 frontend tests.
- **Verified on prod:** refresh source mix went **0 % -> 80 % primary/official**, Sputnik gone, contract rules 1–4 all held on the first live run.
- **Outstanding:** the `thesis_status` divergence rule did not take (cycle reported `supported` against the report's `weakened` without noting the contrast) — prompt rewording, batch with the next contract change. Follow-ups: whitelist stance on state-affiliated media, maritime/insurance primary coverage, and `site:nioc.ir` returning 0 across both cycles.

### Topic refresh scheduler (#22)
- **Spec:** `docs/specs/active/topic_refresh_scheduler_22.md`
- **Lane:** Product / backend — *automatic refresh cadence per monitored topic*
- **What's done (code):** schedule fields on `TopicSubscription` + migration `0005_topic_schedule`; in-app async scheduler (`apps/claude_agent/topics/scheduler.py`) reusing `run_refresh`; `trigger` (`manual|scheduled`) on all `refresh.*` events; `POST`/`PATCH /monitor` schedule on/off + interval (default OFF, clamped to bounds); `GET /monitor` exposes `schedule_enabled`/`interval`/`next_refresh_at`/`last_scheduled_refresh_at`; lifespan start/stop gated by `CLAUDE_AGENT_SCHEDULER_ENABLED` + DB; 8 offline tests in `tests/topics/`; docs (testing README, scenario §7.2a, ops vps.md)
- **What's missing:** live VPS verification (scheduled refresh fires without manual POST on test1); optional `--scheduled` flag in `scripts/test_vector_runner.sh` / `test_refresh_cycle.sh`; enable on test1/prod
- **Next step:** Deploy to test1, run migration `0005`, set a 1h schedule on V001, confirm `scheduler.dispatch` + a `refresh.completed` with `trigger=scheduled`

### Trading Intelligence Evaluation Framework (#23)
- **Spec:** `docs/specs/active/trading_intelligence_evaluation_23.md`
- **Lane:** A — *Is the deliverable valuable for users' business decisions?* (generalizes #18)
- **What's done:** `libs/eval_framework/` package — configurable 3-layer/14-category rubric (Information Discovery 40% / Research 30% / Trading 30%, 0–5), absolute + relative (Better/Equal/Worse) modes, win-rate aggregation, offline deterministic `HeuristicEvaluator` + `LLMEvaluator` (Output Quality Curator), pluggable benchmark-provider registry, `quality_review.{json,md}` rendering, CLI (`python -m eval_framework`) + `scripts/evaluate_output.sh`, rubric doc (`testing/output_evaluation_rubric.md`), 25 offline tests in `tests/eval/`
- **What's missing:** one **LLM-judge** write-up on `test1/latest` referencing a #15 PASS; adoption in pilot go/no-go; optional #21 timeliness/channel hints wired into latency scoring
- **Next step:** Run `scripts/evaluate_output.sh absolute --run-dir testing/results/test1/latest --evaluator llm` on a technically-passing run and attach the verdict to the pilot checklist

### Business output evaluation (#18)
- **Spec:** `docs/specs/active/business_output_evaluation_18.md`
- **Lane:** A — *Is the deliverable valuable for users' business decisions?*
- **What's done:** Evaluator-agent (Output Quality Curator) role defined; phase-aware rubric (P1 comprehension, P2a/P2b query disciplines, P3 latest-news effectiveness, P4 monitoring value); server evaluation flow
- **What's missing:** `testing/output_evaluation_rubric.md`, `quality_review.json` schema + evaluator playbook, one phase-aware write-up on test1
- **Next step:** Publish rubric + curator playbook; run one evaluated test1 run referencing technical PASS from #15

### Continuous monitoring evaluation & valuable-update feedback (#20)
- **Spec:** `docs/specs/active/continuous_monitoring_evaluation_20.md`
- **Lane:** A — *monitoring-over-time variant of #18*
- **What's done:** Gap framed; two modes (A: `/refresh` smoke, B: scheduler window + timeline + retrospective P4); `monitoring_timeline.json` + evaluator bundle specified
- **What's missing:** Timeline assembly, Mode B harness, monitoring-quality rubric, valuable-update labels, one retrospective evaluator run
- **Next step:** After #22 cadence exists, run one monitoring window on test1 → assemble timeline → P4 evaluator review

### Topic refresh scheduler (#22)
- **Spec:** `docs/specs/active/topic_refresh_scheduler_22.md`
- **Lane:** Product / backend — *automatic refresh cadence per monitored topic*
- **What's done:** Gap framed; manual `/refresh` + monitor shipped (#17); scheduler container defined but not running on VPS
- **What's missing:** Schedule fields on subscription, internal scheduler job, VPS scheduler service, harness tests for scheduled vs manual refresh
- **Next step:** Decide interval model (hours vs cron); extend `POST/PATCH /monitor`; implement scheduler job calling `run_refresh`

### Timeliness & source-channel coverage metrics (#21)
- **Spec:** `docs/specs/active/timeliness_channel_metrics_21.md`
- **Lane:** Instrumentation — *feeds #15, #18, #20*
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
| **#24 Topic user ownership** — `owner_user_id` + migration `0006`; JWT auth on all topic routes; service-key bypass for harness; verified on test1 | Jul 26, 2026 | `docs/specs/done/topic_user_ownership_24.md` |
| **#36 Hybrid pipeline orchestration** — Python `source_discover` pre-plan stage writes `source_targets.json`; deterministic topic→entity resolution (no LLM); plan agent consumes pre-resolved domains; `execute_search` contract documented only | Jul 24, 2026 | `docs/specs/active/hybrid_pipeline_orchestration_36.md` |
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
