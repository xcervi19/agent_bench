# Brazil power — second country pilot (#53)

**Status:** onboarded offline 2026-09-18, **no run yet**
**Lane:** Product / business value — *the second country topic, chosen by us rather than asked for*
**Depends on:** test2 existing as a copy of test1 (see `STATUS.md` slot policy)
**Related:** #45 (the method this repeats), #46 (the five gates), #48 (what this proves is worth automating), #49 (third channel), #52 (the comparison this feeds)

---

## Why this topic

India was the customer's ask. This one is ours, and it is chosen to answer a
different question: **can we demonstrate quality a mainstream aggregator cannot
match, on a topic nobody briefed us on?**

Brazil qualifies on four counts, each checked rather than assumed:

1. **The register was blind to it.** `source_whitelist.json` held **13 Brazil
   entries, every one of them upstream oil, macro or weather** — no system
   operator, no market chamber, no power regulator. Of 56 playbooks, **not one
   covers the demand side of an electricity market** outside India.
2. **The driver is published daily, in Portuguese, by the operator.** ONS runs an
   open-data portal with **85 datasets**. Measured 2026-09-18, the four series
   that matter had been rewritten **that same afternoon** (last-modified
   15:00–15:02 UTC) carrying data through 2026-09-16.
3. **It is a standing question with a weekly pile**, structurally the same shape
   as India — so it tests the method, not a new one.
4. **It reaches the customer's own book.** Brazilian thermal dispatch buys
   Atlantic LNG cargoes that then do not reach Europe. The chain is:
   `inflow (ENA) → storage (EAR) → thermal dispatch → gas burn → LNG import → TTF`.

## The cadence argument, which is the real find

India's anchor series (PPAC) is **monthly**. Two of the first nine daily refresh
cycles on that topic added **zero** new sources, at $2.51 and $2.73 apiece. A
daily cycle against a monthly series is paying to re-read the same table.

Brazil's anchor series are **daily, with a ~2-day publication lag**. A daily cycle
has something new to read every single time it runs. If the pile's value is what
we sell, this topic is built to make the pile denser at the same cost.

## What was done (2026-09-18)

- **Playbook** `local_knowledge_sources/playbooks/brazil_power_hydro_thermal.md`
  — the 57th. Four subsystems, eight price drivers, cadence table, anti-patterns.
- **Register** 622 → **629 entries**: ONS, ONS open data, CCEE, ANEEL, ABRACEEL,
  IBGE, World Bank. Every one verified on 2026-09-18 by **reachability plus page
  identity**, the gate that refused `fert.gov.in` on the India topic.
- **Refused, and recorded:** `epe.gov.br` (HTTP 500, two attempts) and
  `dadosabertos.aneel.gov.br` (timeout). EPE is the planning office that
  publishes the ten-year plan — i.e. exactly the forecast source a report would
  want. It is **not** in the register until it verifies. Re-check before the run.
- **Crawler seed** `source_crawler/seeds/brazil_power_official.py` — four ONS
  series (EAR, ENA, subsystem balance, CMO), `static_file`, 24 h, registered in
  the CLI as `--seed brazil_power_official`.
- **Feed routing fixed** — `REGION_SYNONYMS` had no Brazil, and there was no
  commodity synonym table at all. See below; this was a latent repeat of the bug
  that cost the first India run its PPAC feed.
- **Measured the topic string** rather than guessing it.

## The topic string, and why this one

`discover_sources_for_topic` was run over five candidates. The phrase **"LNG
imports"** drags in `china_oil_gas_imports.md` and `southeast_asia_lng_imports.md`
and, at `MAX_TOPIC_PLAYBOOKS = 3`, displaces the Brazil playbook — the same
displacement #45 recorded for "Indian electricity".

| Candidate | Sources | Brazil primaries | Playbooks routed |
|---|---|---|---|
| "…LNG imports for gas-fired generation" | 31 | 9 | china, **brazil_power**, southeast_asia |
| "…electricity … wind in the Northeast" | 27 | 9 | natural_gas_global, **brazil_power**, north_sea_crude |
| "…domestic gas versus LNG" | 38 | 10 | brazil_pre_salt, **brazil_power**, europe_gas_storage_ttf, … |
| **"…ONS … CCEE … ANEEL … gas-fired generation"** | **36** | **10** | brazil_pre_salt, **brazil_power**, europe_gas_storage_ttf, energy_sanctions |

**Chosen:**

```
Brazil power: ONS reservoir stored energy and inflows, thermal dispatch by
subsystem, CCEE marginal cost, ANEEL auctions; gas-fired generation
```

All ten Brazilian primaries route, **no Chinese or Southeast Asian contamination**,
and it keeps `europe_gas_storage_ttf.md` — the market on the other side of the
cargo, which is the one the customer actually trades.

## The routing bug this found

`feeds.matches` compares the feed's `commodity` and `region` against the topic's
facets as sets. Two spellings of one thing therefore fail silently: the feed is
published, the topic is right, and `feeds_count` is simply 0.

- **Region:** `REGION_SYNONYMS` listed 16 countries and **not Brazil**. A seed
  filed `BR` could never reach facets saying `Brazil`.
- **Commodity:** there was no synonym table on that axis at all. A seed filed
  `power` could never reach facets saying `electricity` — and the parse prompt
  asks for "English names of the goods at stake", which yields either.

Both fixed in `apps/claude_agent/topics/feeds.py` (`COMMODITY_SYNONYMS`, shared
`_expand`). **Four tests added, deliberately shaped the way production produces
input** — facets say `electricity` / `Brazil` while the seed says `power` / `BR`,
so a missing table fails the test. The India fixture spelled the country twice
and passed against an input production never produces; that is not repeated here.
Suite: **448 passed**, ruff clean on the changed files.

## Build items, in order

1. **Recent-tail window for chronological feeds.** `feeds.py:250` truncates an
   exported feed at `MAX_CHARS_PER_FEED` (60 000) taking the **head**. The ONS
   files are chronological and run to ~4.5 MB for a year, so a straight export
   hands the analyst **January** and silently drops September. Until this exists
   the feeds must not be quoted as current. *Blocking for the first run.*
2. **`.csv` converter.** `source_crawler/extract.py:55` still skips `.csv`
   ("no converter"). The seed uses the XLSX twins to route around it, but CSV is
   the smaller, faster form of the same data and the gap will recur.
3. **Re-verify EPE and the ANEEL open-data portal**, then add them if they answer.
4. **First run on test2**, then read `feeds_count` in `stage.finished` before
   reading anything else. That number is the whole point of items 1–2.
5. **Operator review of the first pile**, as #46 Gate 5.

## What is explicitly not claimed

No topic has been run. Nothing here is a quality result — it is an onboarding,
verified at every step that could be verified offline. The comparison against
India's numbers belongs to #52 and needs test2 to exist with a corpus first.

The RAG leg is empty for this topic exactly as it was for India: the corpus holds
**141 documents, of which one** matches Brazil, power, electric or hydro. The
explainers gathered on 2026-09-18 (four ONS data dictionaries, EIA Brazil country
analysis, OIES, MME bulletins, ANEEL indicators, ONS operation bulletins, World
Bank) are the input to that leg and have **not** been ingested.
