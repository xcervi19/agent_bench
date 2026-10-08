# Refresh keeps official sources — classify before filtering (#54)

**Status:** shipped to test2 2026-10-03 (`8c924ce`); five cycles measured 2026-10-04 .. 10-08. **Not on test1**
**Lane:** Product quality — *why the daily update stopped carrying the sources the customer valued*
**Depends on:** nothing — a prompt reorder plus one pure helper
**Related:** #45 (the topic that exposed it), #46 (yield counted in primaries), #23 (authority vs relevance in the rubric), #49 (discovery lane), #55 (first topic monitored under the fix)

---

## The defect

The India topic's daily refresh stopped reporting official sources. Measured
2026-09-23 and again 2026-09-27 on test1: **eight of nine consecutive cycles
returned `authoritative: 0`**, and `source_mix.entirely_secondary` was `true` on
four of the last five. The marginal content of the pile had drifted to
`starsamachar.com`, `khaskhabar.com`, `inkl.com` and `discoveryalert.com`.

It was not a discovery problem. Search was returning official sources the whole
time — `search_documents` for that topic holds **44 distinct `ppac.gov.in` URLs**,
34 from `pngrb.gov.in`, 28 from `ongcindia.com`, with new ones still arriving on
2026-09-22. The pipeline was finding them and throwing them away.

**Where they went.** `Phase R3` of `newsfind-refresh.md` applied a freshness filter
**by source tier** in step 3, but only assigned `source_class` in step 6 — three
steps later. An agent following the steps in order has no class to exempt by when
it reaches the filter, so it applied the news-speed window (`max_age_hours`, 168 h
on this topic) to everything. Ministry documents are older than a week by nature;
that is the point of the exemption the phase could not reach. `drops.too_old` fired
**7–16 times per cycle**, every cycle.

**The deliver leg never had this bug**, which is why its runs report 53–64 %
primary while refresh reports 0 %. `newsfind-deliver.md` Phase 3 scores
`source_class` in the same block as relevance, says *"Never drop a
`primary_official` or `data_feed` hit for age"* **after** the class exists, and has
no age bucket in `drops` at all. Refresh had drifted from a design that worked.

Four deviations, all pushing the same way:

| | deliver (Phase 3) | refresh (Phase R3), before |
|---|---|---|
| `source_class` assigned | with the scores, before any drop | step 6, after the filters |
| Age filter | none | step 3, blind to class |
| Relevance floor | 0.35 | 0.40, applied to primaries too |
| Ordering | primary outranks secondary at equal relevance | relevance only |

**Size of the hole, measured.** Of 649 hits search returned for the India topic,
**76 reached a report and 573 were dropped — 209 of them on a whitelisted official
domain.** 209 is an upper bound: it includes landing pages and repeat sightings of
one document. It is the right order of magnitude, and it is counted rather than
estimated.

## What shipped

All of it in `newsfind-refresh.md` plus one helper, no schema change:

1. **R3 reordered** to `dedup → classify → filter`. Nothing is dropped before
   `source_class` exists, and the phase says why in the text, so the next edit does
   not quietly undo it.
2. **`primary_official` / `data_feed` are never dropped for age**, and get
   `freshness: "standing"`. This also fixed a latent mismatch: the old step 3 wrote
   `standing: true` while the `news.json` schema twenty lines below declares
   `"freshness":"fresh|unknown|standing"`.
3. **The relevance floor moved 0.40 → 0.35 and no longer applies to
   `primary_official` / `data_feed`.** This is the one place the fix goes beyond
   copying deliver, and the reason is the customer's own remark on 2026-09-10: the
   source they found most interesting was one the system had ranked *low* on
   relevance. Relevance decides order, not whether an official source survives.
4. **Authority entered the ordering** — a primary outranks a secondary of equal
   relevance, the same sentence deliver already carried.
5. **R2's three-hit cut is authority-aware.** Search returns ~9 links per query and
   refresh keeps 3; taking the first three in search order discarded official hits
   *before* R3 could classify them — the same defect one phase earlier, which would
   have capped the fix. The cap is still 3, so this costs nothing.
6. **`restamp_recency_hints()`** in `apps/claude_agent/topics/refresh.py`.
   `build_short_term_queries` bakes `latest YYYY-MM` into the query text and nothing
   rewrote it, so the India plan written 2026-09-09 was still asking for
   `latest 2026-09` in October. The hint is now re-stamped on the copy handed to the
   agent, from the same `today_iso` the artifact carries — **not** in the stored
   plan, which is the owner's and changes through `PATCH /monitor`. Six tests;
   suite 451 → 457.

## First measurement — Japan (#55), five cycles, 2026-10-04 .. 10-08

The first topic monitored entirely under this fix. Daily, 15 queries, `max_age_hours: 168`.

| Cycle | Date | New | Authoritative | `drops.too_old` | Cost |
|---|---|---|---|---|---|
| 1 | 10-04 | 8 | 4 (50 %) | 1 | $2.93 |
| 2 | 10-05 | 3 | 1 (33 %) | 3 | $4.61 |
| 3 | 10-06 | 9 | **9 (100 %)** | 0 | $3.67 |
| 4 | 10-07 | 1 | **0** — `entirely_secondary` | 3 | $3.77 |
| 5 | 10-08 | 1 | 1 (100 %) | 11 | $3.13 |
| | **total** | **22** | **15 = 68.2 %** | 18 (mean 3.6) | $18.11 |

Against the topic that exposed the bug, on the old code — India's last five cycles
(14–18, 2026-09-22 .. 09-26) produced **the same 22 new sources and 1 authoritative
among them, 4.5 %**, with `drops.too_old` firing 7–16 times every cycle and
`entirely_secondary: true` on four of the five.

**22 new sources either way; 15 official against 1.** That is the result, and the
matched denominator is luck rather than design — it just makes the composition easy
to read.

### Two things this does not support

**`too_old` did not go to zero, and the ticket should not claim it did.** It averages
3.6 per cycle against India's 7–16, but cycle 5 fired **11** — inside India's old
range — while still keeping its one official source. So the filter goes on dropping
things; what changed is that it no longer takes primaries with it. The counter does
not record a class, so "the 11 were all secondary" is inference from the kept mix,
not a measurement. If a cycle ever pairs a high `too_old` with `authoritative: 0`,
that is the signal this regressed, and it is worth watching for rather than assuming
away.

**The variance is larger than the effect is precise.** Five cycles ran from 1 to 9
new sources and from 0 % to 100 % authoritative, and one came back
`entirely_secondary` — rarer than India's four-in-five, not eliminated. The aggregate
is a real n=5 result; the per-cycle ratio is not a stable number and should not be
quoted as one. #41's caveat applies unchanged: one arm cannot separate a build
difference from the news cycle.

**Still not a controlled comparison.** Different country, different publication
cadence, different register and corpus. As a before/after of *what a daily update
actually carries* it is the strongest evidence available; as a measured effect size
of this code change it is not, and that experiment — the same topic run both ways —
belongs to #52 and needs a slot that is not frozen.

### Cost, since the aggregate changes it

$3.62 per cycle on average (range $2.93–$4.61), **~$25/week**, against the ~$3 and
~$20/week recorded in `STATUS.md` from cycle 1 alone. Still trivial against the
pricing in the go-to-market plan; worth correcting because it is a number that gets
quoted.

## Known limitation, deliberately left

Authority is a **tiebreaker at equal relevance**, nothing more. In the cycle above
the four primaries sort *below* four news items that scored higher, so a reader
sees news first. `STATUS.md` records the customer ordering the same set differently
— publisher class first, relevance second. Making class dominate the ordering is a
larger change than this ticket, it contradicts what `next_queries` currently tunes
toward, and per `STATUS.md` it rests on one preference stated once by one desk.
**Verify it against the buyer before building it** (#23, and the three-slot
comparison in #52).

## Remaining build items

1. **A class for the general press.** `source_class` has no slot for it, so Al
   Jazeera and the Washington Post file as `specialist_outlet` — and that is the
   class the confidence rule accepts two of in place of an official source. On
   test1, 2026-09-26, that pair minted a `confidence: high` finding on a Hormuz
   claim with `authoritative: 0`. Add `general_news`, anchor both classes with
   examples (specialist = Argus / Platts / ICIS / Montel; general = Reuters / BBC /
   Al Jazeera), and require trade press for `high`.
2. **Revisit standing sources.** Dedup is `sha1(url)[:16]`, URL only — there is no
   content digest anywhere (`content_hash|etag|last_modified` greps to nothing), and
   `_upsert_document` bumps only `last_seen_at` on conflict. A monthly series at a
   stable URL is therefore silenced permanently after its first sighting, while a
   news site gets a fresh URL per article and always passes. Needs
   `content_sha256` on `search_documents` (migration `0014`), a bounded `revisit[]`
   in `input.json`, and the revisited hit reported as an `update` rather than a
   `new` source.
3. **Yield per query, counted in primaries** (#46). `search_queries` already records
   every call with its `allowed_domains` and `hit_count`; joining that to
   `source_class` says which of a plan's queries earn their place. That measurement
   is the precondition for letting `report.next_queries` flow back into a stored
   plan instead of freezing it at onboarding.

## Slot state

- **test2** carries the fix and the Japan topic runs under it.
- **test1 does not.** It still runs `c772df6`, so its cycles still drop primaries on
  age *and* its stored plan still asks for `latest 2026-09`, which is two months
  stale as of 2026-10-04 and gets worse every day. Two routes, both needing the
  product owner: a `PATCH /monitor` re-stamping the 19 queries fixes the hint today
  without a deploy; deploying this branch fixes both permanently but is a `git pull`
  plus rebuild on a frozen slot. Neither has been done.
