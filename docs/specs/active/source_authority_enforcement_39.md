# Source authority enforcement — #39

**Status:** verified on prod 2026-07-31 (commit `ad60e09`) — one contract rule outstanding, follow-ups open
**Lane:** Product / quality — *what the report is allowed to stand on*
**Depends on:** #29 (whitelist), #30 (playbooks), #36 (source_discover), #16b (report UI)

## Problem

The first monitored refresh cycle on prod (topic `8a2add2e`, 2026-07-31) returned
**8 of 8 sources classed `specialist_outlet`, zero primary/official, and zero on
the 610-domain whitelist** — Al Hadath, France 24 Arabic, Sputnik Arabic,
Bloomberg, Al Jazeera ×2, CNBC, SCMP. One of the three sources behind the
cycle's highest-confidence finding was Russian state media, reporting on Iranian
naval activity.

That is not a product a trading desk can be shown.

The full report was better but not good: 6/35 primary_official, 3/35 whitelisted
(9 %).

## Diagnosis

The grounding was not the failure. Four of the twelve monitoring queries were
site-scoped to official domains, and their yield was:

| Query | Results |
|---|---|
| `site:nioc.ir OR site:pmo.ir OR site:shana.ir OR site:mop.ir` | 0 |
| `site:ukmto.org OR site:imo.org` | 1 |
| `site:aramco.com OR …` | 1 |
| `site:adnoc.ae OR …` | 1 |

Three hits, **all discarded** — `drops.too_old: 14`. The delta said it plainly:
*"the most recent UKMTO advisory on file is still 2026-07-07, unchanged."*

**Primary sources publish on an event cadence; news outlets publish
continuously.** UKMTO issues an advisory when one is warranted; Aramco reports
throughput quarterly; SHANA publishes irregularly. A uniform freshness window
therefore selects for high-frequency publishers and structurally excludes
primary sources — and monitoring inherently wants a tight window, so the skew is
built in, not a tuning accident. **"Newest" and "most authoritative" are
anti-correlated in this domain.**

The second cause: `source_class` was recorded and never used. A grep across
`apps/claude_agent/` returned nothing outside the two prompt contracts. Ranking
was purely `relevance_score`. The system measured source authority and ignored
it.

## Design

Policy that must be deterministic lives in Python. Judgement that needs a reader
lives in the agent contract. Nothing is enforced twice.

### Code — `apps/claude_agent/topics/source_quality.py`

Pure functions over a run's `news.json`, no I/O beyond loading whitelist
domains. A source counts as authoritative when its `source_class` is
`primary_official` / `data_feed`, **or** its host matches a whitelist domain
(exact or subdomain — `ukmto.org.evil.com` does not match).

`SourceMix{total, authoritative, whitelisted}` is computed after every deliver
and refresh and emitted on `report.ready` and `refresh.completed` under
`source_mix`, including `entirely_secondary`. No migration: the measurement
rides the event and the artifact, not the schema.

This deliberately **measures and exposes rather than blocks**. A cycle can
legitimately find only secondary reporting; the defect was hiding it, not having
it. Failing the cycle would trade a visible weakness for an invisible gap.

### Agent contract — `newsfind-deliver.md`, `newsfind-refresh.md`

1. **Two-tier freshness.** `primary_official` and `data_feed` are exempt from
   `max_age_hours` and marked `freshness: "standing"`. An unchanged advisory is
   the current state of the world, not stale news.
2. **Authority participates in ranking**, not as an end-stage tiebreaker.
3. **Confidence capped by sourcing.** `high` requires a primary/official source
   or two genuinely independent outlets. State-affiliated outlets never count
   toward independence on a story about their own state.
4. **Source mix stated, never implied.** `summary_md` opens with the count. When
   no primary source survived, the report must say so up front and name which
   primary sources were queried and returned nothing.

### UI

`SourceMixNote` sits above the executive summary and in every delta detail. Zero
primary sources renders as a warning, not a footnote.

## Verification

Unit-tested both sides, including regression cases built from the eight sources
the failing prod cycle actually returned (`test_matches_the_observed_prod_refresh`,
`flags the observed prod refresh`).

**Verified live on prod**, topic `8a2add2e`, same subscription, same 12 queries,
same 120 h window. The primary-source hits cycle 1 discarded were *dropped*, so
they never entered `news.json` and never entered `seen_url_hashes` — they stayed
eligible, which makes this close to a controlled before/after.

| | Cycle 1 (before) | Cycle 2 (after) |
|---|---|---|
| Sources | 8 | 5 |
| `primary_official` | **0** | **4** |
| On whitelist | 0 | 3 |
| Authoritative ratio | **0 %** | **80 %** |
| `entirely_secondary` | **true** | false |
| State-affiliated media | Sputnik Arabic | none |

Cycle 2 returned Saudi Aramco, OPEC, U.S. Department of War and UKMTO/JMIC —
all four carrying `freshness: "standing"`, i.e. exactly the sources the uniform
window had been deleting. Cost 519 s / $1.86 versus 287 s / $1.41: reading
official documents is slower and dearer than reading news snippets.

Contract rules 1–4 all held on the first real run. `summary_md` opened with
`Sources: 5 new (4 primary/official, 1 secondary).`; the cycle named what
returned nothing (Fujairah/ADNOC channels, NIOC/SHANA, a second IEA round); the
single aggregator-sourced finding was capped at `medium` and labelled
*"Single-sourced (aggregator), medium confidence only."*; and the agent
volunteered a distinction we had not asked for — *"the original primary
documents, newly indexed this cycle but not new developments."*

Content improved with the sourcing. Two findings were structurally unavailable
to cycle 1: Aramco's own Q1 results confirming the East-West pipeline at
7.0 mmbpd against Yanbu's ~3–4 mmbpd loading ceiling, and OPEC's record showing
the 5 July meeting was a routine +188 kbd adjustment rather than emergency
deployment — which closes an open question the full report had flagged as
unresolved.

**Do not read the 8 → 5 volume drop as a regression.** `drops.already_seen: 7`:
cycle 1's own sources were correctly excluded, so cycle 2 searched a thinner
remaining pool. The mix comparison is valid; a raw volume comparison is not.

### Outstanding

**The `thesis_status` divergence rule did not take.** Cycle 2 reported
`supported` while the full report says `weakened`, without the required note
that the two diverge. Likely cause: the instruction was appended as a
subordinate clause to a bullet about something else, rather than standing on its
own. Fix is a prompt rewording, but verifying it costs another live cycle, so it
should be batched with the next contract change rather than deployed alone.

## Out of scope — open follow-ups

- A hard primary-source floor that fails a cycle — see the reasoning above.
- **Whitelist policy on state-affiliated media.** Sputnik is not on the
  whitelist; nothing excludes it either. It did not reappear in cycle 2, but
  that is a side effect of better ranking, not a rule. Needs an editorial
  decision, not code.
- **Whitelist coverage gaps** for maritime and insurance primaries (Lloyd's Joint
  War Committee, IG P&I clubs) — part of why several queries found nothing.
- **`site:nioc.ir OR site:pmo.ir OR site:shana.ir OR site:mop.ir` returns 0**
  across both cycles. Two-tier freshness cannot fix a query that matches nothing:
  either those hosts are not search-indexed or the Farsi site-scoping is wrong.
  Needs one manual check before assuming Iranian primary sources are reachable
  at all.

## Related

- `apps/claude_agent/topics/source_quality.py`, `tests/topics/test_source_quality.py`
- `apps/signalgather_web/src/lib/sourceQuality.ts`
- `docs/specs/active/signalgather_frontend_v1_16.md` — report + sources UI
- `docs/specs/done/source_discover_skill_32.md`, `coverage_playbooks_seed_30.md`
