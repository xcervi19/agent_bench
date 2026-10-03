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
