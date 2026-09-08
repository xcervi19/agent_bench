# Ticket registry

_Canonical list of spec ticket numbers. Update this file whenever you **create**, **move**, or **retire** a numbered ticket._

**Next available number:** `#52` (assign to the next new ticket; then bump this line)

---

## How to use

1. Before creating a ticket, read this file and confirm the number is unused.
2. After creating `docs/specs/active/<name>_<n>.md`, add a row under **Active** below.
3. When shipping, move the file to `docs/specs/done/` and move the row to **Done**.
3b. When a ticket stops being relevant, **retire** it: move the file to `docs/specs/done/`,
   replace its `Status:` line with `retired (YYYY-MM-DD)` plus a `Retired because:` block
   naming the ticket that now holds the problem, and move the row to **Retired**. Never
   delete a spec — the decision not to build something is context too.
4. Update **`STATUS.md` → Build queue** if priority or dependency chain changes.

**Validation:** Ticket numbers must be unique across active + done + legacy rows. Filename must match: `*_<n>.md` where `<n>` equals the ticket number in the doc header.

---

## Active (executable)

_18 open tickets. A row here means work remains; the spec file lives in `docs/specs/active/`
and its `Status:` line says `planned` or `in progress`. Reconciled 2026-09-08 — the previous
list carried seven shipped or retired tickets and omitted #42._

| # | File | Status | Blocks / unblocks |
|---|------|--------|---------------------|
| 51 | `docs/specs/active/report_grounding_completion_51.md` | planned | **Connects four shipped acquisition mechanisms to the leg that writes the report.** The deliver leg reads neither the captured corpus (#42) nor the plan's RAG context, spreadsheets are recorded `unsupported`, and the feed channel goes silently to zero when facets degrade. Changes what the analyst can read, not what search finds. Needs #42, #45; blocks a credible second India run |
| 45 | `docs/specs/active/india_gas_country_pilot_45.md` | in progress | **First customer topic.** First run delivered on test1 2026-09-03; PPAC feed connected 2026-09-05. Next: second run, then monitoring at weekly cadence. Template for country #2 |
| 47 | `docs/specs/active/register_labels_47.md` | planned | **Demo-critical, promoted 2026-09-08.** `entities_named_in` matches entity names and never reads the domain, so adding "Ministry of Petroleum and Natural Gas" to a discovery query takes an India topic from 32 to 54 targets — 9 Iranian domains, 2 Bangladeshi ministries, and `iran_oil_geopolitics.md` displacing an India playbook. Blocks `allowed_domains` being safe by construction |
| 16 | `docs/specs/active/signalgather_frontend_v1_16.md` | in progress | 16a–d built and verified through the API; **no one has driven the UI in a browser**. §5 reconnect and §11 responsive close nothing automated can |
| 50 | `docs/specs/active/live_public_sharing_50.md` | in progress | Implemented 2026-09-01, applied on test1. Awaiting prod migration + the logged-out browser pass (inherited from #40). Feeds #37 |
| 22 | `docs/specs/active/topic_refresh_scheduler_22.md` | in progress | Code + tests done; the *scheduled* path has never fired on a slot. Blocks #16 monitoring, #20 |
| 23 | `docs/specs/active/trading_intelligence_evaluation_23.md` | in progress | Lane A framework shipped. **Absorbs #18.** LLM path blocked on #43 |
| 46 | `docs/specs/active/topic_onboarding_loop_46.md` | planned | **Method ticket** — five gates per customer topic. Build item 0 shipped; items 1–4 open. India (#45) is its first test case |
| 48 | `docs/specs/active/topic_bootstrap_job_48.md` | planned | The India onboarding automated. Needs #47. Highest leverage and highest risk in the set — every leg generative |
| 49 | `docs/specs/active/discovery_lane_and_promotion_49.md` | planned | Budgeted unfiltered discovery, known-source polling off the search budget, promotion from evidence #42 already collects. Needs #42, #47 |
| 44 | `docs/specs/active/insurance_vessel_tracking_sources_44.md` | planned | Marine war-risk / vessel-tracking branch for chokepoint topics. Carries #39's maritime follow-up. **Needs an image rebuild — config is baked in** |
| 43 | `docs/specs/active/claude_llm_judge_migration_43.md` | planned | Move the eval judge off OpenAI onto Claude Code. Blocks trusting any LLM-scored number (#23, #41) |
| 37 | `docs/specs/active/pilot_first_use_experience_37.md` | planned | First-use and return-use UX after #16. Blocks broad pilot acquisition |
| 41 | `docs/specs/active/multi_run_evaluation_baseline_41.md` | planned (parked by request) | N≥3 repeat runs × M topics. Blocks any credible "did this improve?" claim |
| 34 | `docs/specs/active/topic_ops_table_frontend_34.md` | planned | Topic ops table (user + admin). Needs #16, #24, #22 |
| 31 | `docs/specs/active/scraping_infrastructure_31.md` | planned | `twscrape` / `Pyrogram` for Twitter/Telegram. The blocker behind the empty official-social section in #39 and #44, and behind #36's unbuilt `execute_search` |
| 20 | `docs/specs/active/continuous_monitoring_evaluation_20.md` | planned | Lane A over time. Do not start before #22 fires scheduled and #23 has a rubric write-up |
| 21 | `docs/specs/active/timeliness_channel_metrics_21.md` | planned | Timeliness + channel-coverage metrics. Feeds #23, #20 |

---

## Done (shipped)

| # | File | Shipped |
|---|------|---------|
| 40 | `docs/specs/done/public_topic_sharing_40.md` | 2026-08-01 |
| 42 | `docs/specs/done/search_evidence_capture_42.md` | 2026-08-02 |
| 39 | `docs/specs/done/source_authority_enforcement_39.md` | 2026-07-31 |
| 38 | `docs/specs/done/multilingual_topic_grounding_38.md` | 2026-09-01 |
| 24 | `docs/specs/done/topic_user_ownership_24.md` | 2026-07-26 |
| 36 | `docs/specs/done/hybrid_pipeline_orchestration_36.md` | 2026-07-24 |
| 32 | `docs/specs/done/source_discover_skill_32.md` | 2026-07-23 |
| 30 | `docs/specs/done/coverage_playbooks_seed_30.md` | 2026-07-23 |
| 29 | `docs/specs/done/source_whitelist_seed_29.md` | 2026-09-08 (closed out) |
| 25 | `docs/specs/done/slim_main_archive_25.md` | 2026-06-16 |
| 19 | `docs/specs/done/devops_vps_test_execution_19.md` | 2026-06-02 |
| 17 | `docs/specs/done/pilot_ops_v1_17.md` | 2026-06-02 |
| 15 | `docs/specs/done/newsfind_application_verification_15.md` | 2026-06-02 |
| 13 | `docs/specs/done/multi_env_pre_frontend_13.md` | — |
| 12 | `docs/specs/done/setup_caddy_reverse_proxy_12.md` | — |
| 11 | `docs/specs/done/rag_full_stable_evaluation_11.md` | 2026-05 |
| 10 | `docs/specs/done/rag_main_corpus_highest_roi_10.md` | 2026-05 |

---

## Retired (no longer relevant)

Kept as files, removed from Active. A retired ticket records a decision we took and a road we
did not; the `Retired because:` block at the top of each says which ticket, if any, holds the
problem now. **Do not reuse these numbers.**

| # | File | Retired | Why |
|---|------|---------|-----|
| 33 | `docs/specs/done/plan_source_integration_33.md` | 2026-09-08 | Superseded by **#36**. Source discovery is a Python pre-plan stage, not agent-inline `/source-discover` calls |
| 35 | `docs/specs/done/graph_retrieval_layer_35.md` | 2026-09-08 | The relational-retrieval problem is being answered as a **set query over labels** (**#47**) plus a growth path (**#49**), not activation spreading over a source graph. Its own start condition — vector retrieval measurably failing on relations — was never met; the measured failure was inventory and routing |
| 18 | `docs/specs/done/business_output_evaluation_18.md` | 2026-09-08 | Folded into **#23**, which generalises it. Its rubric shipped as `testing/output_evaluation_rubric.md` |

---

## Unnumbered archive (no `#` in filename)

Historical specs without ticket numbers — do not reuse their numbers; add new work with the next `#` from the top of this file.

| File | Notes |
|------|--------|
| `docs/specs/done/deployment_newsfind_pipeline_v1.md` | Pipeline v1 deploy |
| `docs/specs/done/reproducible_artifacts_and_cache.md` | Artifacts + cache |
| `docs/specs/done/agentic_search_claude_code_architecture.md` | Architecture reference |

---

## Gaps in numbering

Numbers **#14**, **#9** (cited in #16 only as historical ref) are not allocated in this repo. Do not invent retroactive files for missing numbers unless explicitly recovering lost work.
