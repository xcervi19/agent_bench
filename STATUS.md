# Development Status

_Update this file as work progresses. The agent reads it every session to understand current context._

**Ticket numbers:** `docs/specs/TICKET_REGISTRY.md` (next: **#37**).  
**How to create / prioritize tickets:** `AGENT.md` → Creating a new ticket, Build queue.

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
