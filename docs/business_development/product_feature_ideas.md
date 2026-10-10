# Product feature ideas — from the test2 topic review

**Written:** 2026-10-10
**Context:** the three topics on test2 — Japan nuclear fleet (#55, `0a354872`), India gas
re-run (`e3482cd0`), India coal (#56, `009ff1c4`) — reviewed as pre-sales material for a
trading desk. The product is a proof of concept; the goal now is to make a trading house
want to negotiate and pay, not to sell a finished product.

---

## What the review established

These are the facts the ideas below rest on. Each is measured, and the source is named.

- **Our edge is the regulator's own table, not the prose.** The strongest material in all
  three topics came from data the obliged party publishes: JEPX HJKS (every Japanese
  reactor stop, filed the same day), CEA's Daily Coal Stock Report (every Indian coal
  plant's stock against its required minimum), PPAC's monthly gas tables. A trader does
  not get these from news; news reports them later, one plant or one number at a time.
- **Search cannot reach the current official files.** On India coal the domain-filtered
  queries fetched dozens of official documents from coal.gov.in, CEA, NTPC, DGCI&S and
  CERC — all from 2020–2024. The index serves the regulator's old files; the current ones
  arrive only when we fetch them directly (#56 spec, "First run"). The same was found for
  PPAC on #45.
- **Daily monitoring is where test2 beats test1, not the first report.** India gas: first
  report 64 % authoritative on test1 vs 55 % on test2 — one run each, not a measurement.
  But test1's refresh, on pre-#54 code, returned zero official sources in eight of nine
  cycles, and its month-old standing report still says Hormuz has reopened. On test2 the
  refresh keeps primaries (Japan: 15 of 22 new sources authoritative over five cycles).
- **Trust breaks on small details.** Japan: Mihama-3's shutdown date and cause contradict
  between report and cycle 5, and the report cites an LNG calculation it does not contain.
  Coal: rake loading taken from a stock-quote page contradicts the Ministry table the
  analyst had in hand. A desk judges credibility on exactly these.

**Verdict for sending:** yes as a demo, walked through live, after fixing the three named
defects; not as a finished product sent cold.

---

## Ideas

### 1. Sell access to primary data, not reports

**Status:** idea

**Idea.** Position the product as "for each country and commodity, we find the table the
regulator keeps, and we automate it". The register of obliged-party datasets — HJKS, CEA,
PPAC, ONS, Ministry of Coal, Coal India filings — becomes the thing sold, and the report
becomes one view of it.

**Why a desk pays.** Finding, verifying and automating these tables is work a trading desk
does not do itself. It is also the work that took three weeks for India (#45) and a day
for Japan once the method existed. That method is the consulting product.

**First step.** A one-page "source register" per topic for the client: which official
datasets, how often they update, the lag we observed, what we automated.

### 2. A morning "what changed" digest instead of a long report

**Status:** idea

**Idea.** A short message each morning, computed from the feeds rather than written by the
model: plants that became critical yesterday, a reactor that tripped with no return date,
a stock draw above a threshold, a new monthly filing landed. Prose only where it adds context.

**Why a desk pays.** A trader wants a signal, not an essay. A diff of the regulator's
table has no room for hallucination — it is a comparison of two official files.

**First step.** The CEA adapter already computes "newly critical" and "largest draws" over
a week; the same diff day-on-day, sent to email or Slack.

### 3. Keep the history nobody else keeps

**Status:** idea

**Idea.** Store every daily snapshot of every feed. CEA publishes one day per file; HJKS
shows the current state. After a few months we hold a plant-level time series that is not
available anywhere as a dataset.

**Why a desk pays.** It is backtestable: plant stocks against CIL e-auction premiums, IEX
power prices, Indonesian HBA; Japanese reactor availability against JKM. A data moat that
grows every day without extra work.

**First step.** Archive the raw daily files and parsed rows on the slot, not just the
latest text feed. The crawler already writes them; it overwrites them today.

### 4. Measure and show the lead over news

**Status:** idea

**Idea.** For concrete events, document how many hours or days the primary source had it
before Reuters, Bloomberg or the trade press — a plant entering critical stock, a reactor's
unplanned stop, a monthly production number.

**Why a desk pays.** One documented sentence — "we had NTPC Barh critical N days before the
first article" — sells more than a full report. It is also the #21 timeliness metric,
expressed in the buyer's terms.

**First step.** For the 8 coal plants newly critical in the week to 2026-10-08, find the
first news mention of each and record the gap.

### 5. One view of the Asian energy balance

**Status:** idea

**Idea.** Connect the topics through what they share: Asian LNG demand. Indian coal short →
more gas-fired dispatch; a Japanese reactor out → more LNG imports; Indian gas → LNG imports
directly. A single view that rolls the three into a JKM-relevant balance.

**Why a desk pays.** It speaks to the price the desk actually trades, rather than to three
separate country stories.

**First step.** A shared "LNG impact" section fed from the three topics' feeds — after idea 6,
so the conversions are computed, not asserted.

### 6. Numbers computed by code, explained by the model

**Status:** idea

**Idea.** Every conversion — GW offline to LNG tonnes, days of stock to import need,
receipt-minus-burn trends — is computed deterministically from the feeds, and the model only
comments on the result. Plus a rule that a figure from a feed outranks a secondary source
on the same quantity, and a block list for stock-quote pages (groww, zerodha, tickertape,
scanx), which carry no primary content for any topic.

**Why a desk pays.** It removes the class of error that broke trust in this review (the
rake-loading figure, the missing LNG calculation).

**First step.** The feed-outranks-secondary rule in the deliver prompt and a
`blocked_domains` list — both recorded as #56's item 5b.

### 7. The coverage map as a deliverable

**Status:** idea

**Idea.** Give the client the audit of their space: for Indian coal, 22 official sources,
which answer, which block us, how fast each publishes, which are automated. Update it as the
register grows.

**Why a desk pays.** It is proof of rigour and the natural scope document for a paid
engagement — "auditable coverage of a defined space", as #46 put it, rather than a claim to
read the whole internet.

**First step.** Generate it from the register and the `search_documents` fetch statuses we
already store.

### 8. Fix access from the right place

**Status:** idea

**Idea.** Several primaries refuse our European VPS but answer elsewhere: `coalindia.in` and
`mahanadicoal.in` (403 from the VPS, 200 from the operator's machine), `tepco.co.jp` (403
everywhere we tried). Options: a small fetcher with an Indian or Japanese address, or the
semi-automatic browser-assisted route already described in
`docs/architecture/source_acquisition_pipeline.md`.

**Why a desk pays.** Coal India's own monthly filings and TEPCO's plant pages are exactly the
sources a desk expects us to have.

**First step.** Price a regional fetcher against the number of blocked primaries it unlocks.

### 9. A short pilot on the client's own question

**Status:** idea

**Idea.** Offer the first client a time-boxed pilot on a topic they choose: we find the
regulator's table for their question, automate it, and run a daily watch. The commercial
conversation follows the pilot, not the other way round.

**Why a desk pays.** It matches the consulting-first approach — the per-topic engineering is
what is valuable and must not be given away as a cheap licence (see
`go_to_market_first_customer.md`).

**First step.** Agree with the owner on the pilot's length, scope and what "success" means
for the desk, before the next client conversation.

---

## Defects to fix before any of this is shown

From the review; each is tracked in its own spec.

| Topic | Defect | Where |
|---|---|---|
| Japan | Mihama-3 date and cause contradict between report and cycle 5 | #55 item 7 |
| Japan | Report cites an LNG-displacement calculation it does not contain | #55 item 8 |
| India coal | Rake loading "19 → 41/day" from a stock-quote page contradicts the Ministry feed (304.7/day) | #56 "First run", item 5b |
| India coal | The CEA stock trend (20.6 Mt, receipts below burn all week) is missing from the report | #56 "First run", item 5b |
| India gas (test2) | Does not describe the current state of Hormuz | review 2026-10-09 |
