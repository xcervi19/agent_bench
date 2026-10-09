# Japan nuclear fleet — customer topic with daily monitoring (#55)

**Status:** in progress — onboarded and deployed to test2, 2026-10-03
**Lane:** Product / business value — *a customer's ask, the third country topic*
**Depends on:** #53 (feed channel delivering), #54 (refresh keeps official sources)
**Related:** #45 / #53 (the method this repeats), #46 (the five gates), #22 (scheduler), #47 (routing contamination)

---

## The ask

The customer wants to follow Japanese nuclear power over the long run: **planned
operation, outages, and any news that moves the fleet**. Created as a monitored topic on
test2 with a **daily** refresh.

## Could we find primary sources? Not before this ticket

Measured 2026-10-03 against the register and playbooks as they stood on #54:

- `source_whitelist.json` held **no** Japanese nuclear source — no regulator (NRA), no
  operator, no outage register. METI/ANRE, JMA and IAEA were the only overlap.
- The candidate topic string routed to **`brazil_power_hydro_thermal.md`** (on the token
  `power`) and `japan_korea_lng_demand.md`, and returned **zero** nuclear primaries.

A run on that would have been a news-aggregator report. So this ticket is the
onboarding, the same shape as #45 and #53.

## What was done

- **Playbook 58** `local_knowledge_sources/playbooks/japan_nuclear_reactor_fleet.md`.
  Three gates (NRA → prefecture → operator schedule), eight drivers, cadence table,
  anti-patterns. The fleet numbers are **read from HJKS**, not recalled: 15 units in
  the operating cycle (~14.6 GW), Kashiwazaki-Kariwa 6 back since 2026-02, two
  unplanned Kansai stops open with no return date.
- **Register 629 → 651.** NRA, JEPX HJKS (`data_feed`), JEPX, OCCTO, JAIF, FEPC, nine
  nuclear operators, JNFL, the Atomic Energy Commission, Niigata / Fukui / Ibaraki
  prefectures, the courts, WNA. Each verified by reachability plus page identity;
  the operator-facing ones re-checked from the VPS that runs the agent.
- **Refused, and recorded: `tepco.co.jp`** — HTTP 403 on every path, from both the
  laptop and the VPS. Kashiwazaki-Kariwa is reached through HJKS, NRA and Niigata.
- **A new feed: the HJKS outage register.** `source_crawler/adapters/hjks_outages.py`
  + seed `japan_nuclear_official`. Every Japanese generator ≥100 MW must register a
  planned stop, an unplanned stop or a derating, with a cause and an expected return.
  The adapter downloads the register (GET for session + `_csrf`, then the CSV POST),
  keeps the 217 nuclear rows, and writes a ~30 kB text feed: an "open now" section
  and every entry newest-update first.
- **`nuclear` synonym group** in `feeds.COMMODITY_SYNONYMS` — `nuclear` /
  `nuclear power` / `nuclear energy` are one good. Deliberately **not** joined to
  `power`: an outage table is not evidence for every Japanese electricity question.
- **`scripts/devops/slot_refresh_feeds.sh`** — crawl, extract, publish for one seed and
  slot, so a cron line can keep a daily feed daily. Until now every feed was published
  by hand, which suits monthly PPAC and not a register edited the hour a unit trips.

## Three things the adapter had to get right

1. **The form's fuel filter does nothing for the CSV.** `format=1` (原子力) returned all
   58 788 rows of every fuel type. The filter is applied on the column instead.
2. **TLS.** HJKS negotiates only `ECDHE-RSA-AES128-SHA` over TLS 1.2 and rejects
   OpenSSL 3's default security level with a handshake-failure alert — curl over
   LibreSSL connected, Python did not, and the first local crawl failed on it. The
   adapter uses `@SECLEVEL=0` capped at TLS 1.2, for this host only; certificate
   verification is unchanged.
3. **"As of" is the register's newest update, not the fetch clock.** The text then
   changes only when the publisher's data does, which is what `feeds.publish` keys
   its `collected_at` stamp on.

## The topic string, and why this one

Measured with `discover_sources_for_topic`:

| Candidate | Sources | JP nuclear primaries | Playbooks |
|---|---|---|---|
| "Japan nuclear power: reactor restarts, outages, NRA safety reviews, planned operation of nuclear plants" | 44 | 25 | **brazil_power**, japan_korea_lng, japan_nuclear |
| "…; NRA reviews, Kansai and Kyushu Electric, LNG displacement" | 41 | 25 | **australia_lng**, japan_korea_lng, japan_nuclear |
| **"Japan nuclear reactor fleet: … NRA reviews, HJKS outage register, Kansai and Kyushu Electric"** | **34** | **25** | japan_korea_lng, japan_nuclear |

The words `power` and `plants` pull the Brazil playbook in on one shared token; `LNG`
pulls Australia. **Chosen:**

```
Japan nuclear reactor fleet: long-term operating schedule, periodic inspections,
unplanned outages and restarts — NRA reviews, HJKS outage register, Kansai and
Kyushu Electric
```

**Known residual risk, not fixed here.** Production routes on
`discovery_query(facets)`, not the bare string, and a parse leg that writes
`nuclear power` into `commodity` brings the token `power` back: simulated with
plausible facets, the Brazil playbook takes the third slot (44 sources). The Japan
playbook is never displaced — it is the top match — so the cost is noise in the
plan, not lost primaries. A fix belongs to the router (a single generic stem token
should not route a playbook) and would change India's and Brazil's measured routing,
so it is #47's to decide. Check `playbook_refs` on the first plan.

## Build items, in order

1. ~~Playbook, register, feed, synonym, refresh script~~ — done 2026-10-03.
2. ~~Deploy to test2, publish the feed, daily feed cron~~ — see `STATUS.md`.
3. ~~Create the topic, deliver, enable daily monitoring~~ — topic `0a354872`, $4.58,
   `feeds_count: 1`, monitored every 24 h from 2026-10-04 16:19 UTC. See `STATUS.md`.
4. ~~Read the first report's source mix~~ — **11/15 authoritative (73.3 %)**, against
   India 64 % and Brazil 61 %. The residual routing risk did not fire: the parse leg
   left `commodity` empty, so no `power` token and no Brazil playbook.
5. **Re-check `tepco.co.jp`** from a Japanese vantage point, or find the path that answers.
6. **Two cycles of pile, then the operator review** (#46 Gate 5).

## Trader-demo readiness — review 2026-10-09

**Verdict:** the topic shows that the method works (official sources, a live feed,
a daily watch that finds real things), but it is not yet a finished product for a
trader. Show it live and talk it through; do not send the link on its own until items
7 and 8 are done. Read from the public link
(`/app/shared/0a354872-bfed-4318-8d10-e17c35097ea1`, live, 5 cycles 10-04..10-08).

**Strong enough to show:** 11/15 authoritative sources (73.3 %), cited to HJKS, NRA,
KEPCO, OCCTO. In five cycles the monitoring found things the first report did not
have: Ohi-3's root cause and its move into inspection, Shimane-2 back in commercial
operation, a temperature anomaly at Takahama-1, three separate faults at Mihama-3
this year. A quiet cycle says it is quiet, and a weakened thesis says it is weakened.

### Open items, in order

7. **Mihama-3 contradicts itself — the first thing a trader would catch.**
   The standing report says a manual shutdown on **09-18** for a corroded secondary
   pipe (a 14×4 mm hole, a cover fitted upside down) [s01,s11]. Cycle 5 (10-08) says a
   manual shutdown on **09-17** for a water leak near a high-pressure feedwater-heater
   valve, cause undetermined. It calls this "not previously surfaced" and "a third
   Kansai unit" outside operation, which it is not. Cycle 3 had already cited KEPCO's
   Mihama-3 filings.
   *Proposed fix:* (a) check by hand against KEPCO's release and HJKS whether this is
   one event or two, and correct the text the reader sees. (b) Structural fix: give
   refresh an **entity/event ledger** (unit + event type + date) built from the
   standing report and earlier deltas. A hit on a unit already in the ledger is then
   classed as *update / conflict / duplicate* instead of "new". Where two sources give
   different dates or causes, the delta should say so ("sources disagree")
   rather than pick one. Belongs with #54's open "content-digest revisits".

8. **The report promises numbers it does not contain.** "Risks & blind spots" says
   "the LNG-displacement math in this report assumes…", but the report does no such
   calculation. It also gives no GW offline and no effect on LNG/JKM. That is the
   question a trader brings to Japanese nuclear.
   *Proposed fix:* add a **fleet-state block** to the Japan playbook and the deliver
   prompt: units operating / in inspection / in unplanned outage, with GW, computed
   from HJKS + NRA. Then a rough conversion of GW offline to LNG demand
   (≈ 0.13–0.15 Mt LNG/month per GW, to be confirmed with the operator), labelled as
   an estimate. And a grounding rule: the report must not refer to a calculation it
   does not show (a check for #51).

9. **The standing report does not take in what the cycles find.** The public page
   shows the deliver report from 10-03 ("no return date as of October 2"). Ohi-3 in
   inspection, Shimane-2 and Takahama-1 exist only in the delta timeline. A reader who
   opens the link sees the state from a week ago at the top. By design: the public
   router serves `public_deliver_run_id`.
   *Proposed fix:* the cheaper option is a **"What changed since"** block above the
   report on the public page, built from the summaries of the last N deltas (frontend
   only, no extra Claude spend). The more expensive one is a periodic
   **re-consolidation** of the standing report (e.g. weekly, one deliver-sized run
   ≈ $3.4) that writes the deltas into the main text. Pick together with #50.

10. **`report.json` on the public route is not valid JSON, and it carries another
    topic's id.** `GET /v1/public/topics/0a354872…/report` → `JSONDecodeError` at char
    5915 (an unescaped `"regulatory setback"` inside `summary_md`). The file's
    `topic_id` is `d5067cb1-8240-4546-8416-7698507d7274`, not `0a354872…`. The UI reads
    `report.md`, so the page renders, but any API consumer or eval reading the JSON
    breaks.
    *Proposed fix:* deliver should produce `report.json` through `json.dumps` from a
    structured result, never written as text by the model. Validate it before saving
    (on failure, regenerate or fall back to `report.md`). The backend should overwrite
    `topic_id` with the real id instead of trusting the model. Check India and Brazil
    for the same defect.

11. **Cosmetics that undermine trust.** Ohi-3's root cause is reported as new in both
    cycle 1 and cycle 2. Cycle 1 (10-04) says the unit "entered" inspection on 10-05,
    a past tense for a future date. The Takahama-1 watch item (65 °C, a 77 °C
    shutdown limit) is not followed up by any later cycle.
    *Proposed fix:* item 7's ledger covers the duplicates. The prompt should keep
    announced and completed events apart (`scheduled` vs `occurred`). Open watch
    items should go into the next cycle's queries as explicit follow-ups, until they
    are resolved or past their window.

12. **Expert review and the TEPCO source** — items 5 and 6 above still hold. The
    operator review (#46 Gate 5) is the step that turns this list into priorities
    from the trader's side. Ask the trader directly whether item 8 (GW → LNG) is
    the main value for them.
