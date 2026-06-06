# Ticket registry

_Canonical list of spec ticket numbers. Update this file whenever you **create**, **move**, or **retire** a numbered ticket._

**Next available number:** `#24` (assign to the next new ticket; then bump this line)

---

## How to use

1. Before creating a ticket, read this file and confirm the number is unused.
2. After creating `docs/specs/active/<name>_<n>.md`, add a row under **Active** below.
3. When shipping, move the file to `docs/specs/done/` and move the row to **Done**.
4. Update **`STATUS.md` → Build queue** if priority or dependency chain changes.

**Validation:** Ticket numbers must be unique across active + done + legacy rows. Filename must match: `*_<n>.md` where `<n>` equals the ticket number in the doc header.

---

## Active (executable)

| # | File | Status | Blocks / unblocks |
|---|------|--------|---------------------|
| 16 | `docs/specs/active/signalgather_frontend_v1_16.md` | planned | User-facing V1 UI; needs #17 done |
| 18 | `docs/specs/active/business_output_evaluation_18.md` | planned | Needs #15 PASS; pairs with #20, #21 |
| 20 | `docs/specs/active/continuous_monitoring_evaluation_20.md` | planned | Needs #18, #21, **#22** |
| 21 | `docs/specs/active/timeliness_channel_metrics_21.md` | planned | Feeds #15, #18, #20 |
| 22 | `docs/specs/active/topic_refresh_scheduler_22.md` | planned | Blocks #16 (16c), #20 |
| 23 | `docs/specs/active/trading_intelligence_evaluation_23.md` | in progress | Lane A framework; generalizes #18; needs #15 PASS |

---

## Done (shipped)

| # | File | Shipped |
|---|------|---------|
| 10 | `docs/specs/done/rag_main_corpus_highest_roi_10.md` | 2026-05 |
| 11 | `docs/specs/done/rag_full_stable_evaluation_11.md` | 2026-05 |
| 12 | `docs/specs/done/setup_caddy_reverse_proxy_12.md` | — |
| 13 | `docs/specs/done/multi_env_pre_frontend_13.md` | — |
| 15 | `docs/specs/done/newsfind_application_verification_15.md` | 2026-06-02 |
| 17 | `docs/specs/done/pilot_ops_v1_17.md` | 2026-06-02 |
| 19 | `docs/specs/done/devops_vps_test_execution_19.md` | 2026-06-02 |

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
