# Japan nuclear — reactor fleet operation, outages and restarts

**Commodity:** nuclear power (with the LNG / coal burn it displaces)  
**Geography:** Japan — ten utility service areas; the operating fleet sits in Kansai, Kyushu, Shikoku, Chugoku, Tohoku and TEPCO areas  
**Last reviewed:** 2026-10-03  
**Analyst owner:** Japan nuclear customer topic (#55)

## Executive summary

Japan's nuclear output is decided by **three gates, each published by the party that
holds it**: the regulator's safety review (NRA), the host prefecture's consent, and the
operator's own schedule of periodic inspections and outages. A reactor that has passed
all three runs about thirteen months, stops for an inspection, and comes back through a
test-run derating. Every one of those stops — planned or not — must be registered on
**JEPX's HJKS outage platform** the day it happens, with a cause and an expected return.

That register is the reason this topic can be done well. News reports a trip a day
later and one plant at a time; HJKS has the whole fleet, the booked inspections into
2028, and the units that tripped without a return date. Whoever reads it directly
sees an availability change before it is a headline.

**Measured from HJKS on 2026-10-03** (217 nuclear entries; the register is the source):

- **15 units have stop or derating entries dated 2024 or later**, i.e. are in the
  operating cycle: Takahama 1–4, Ohi 3–4, Mihama 3 (Kansai); Sendai 1–2, Genkai 3–4
  (Kyushu); Ikata 3 (Shikoku); Shimane 2 (Chugoku); Onagawa 2 (Tohoku);
  Kashiwazaki-Kariwa 6 (TEPCO). Licensed capacity **~14.6 GW**.
- **Kashiwazaki-Kariwa 6 is back:** test-run derating from 2026-02-16, an equipment-failure
  stop 03-14 → 03-22, and the register notes rated output reached 2026-03-27.
- **Open on 2026-10-03:** Ohi 3 **unplanned stop since 2026-08-08, generator failure,
  no return date**; Mihama 3 stopped 2026-09-18 for an equipment issue under
  investigation (調査中), no return date; Genkai 3 in inspection to 2026-10-29;
  Takahama 3 in inspection to 2026-11-10.
- **Booked ahead:** Ohi 3 periodic inspection from 2026-10-05; Takahama 4 from
  2026-11-14 to 2027-07-10; Ikata 3 from 2027-02-20; Onagawa 2 from 2027-07-08 to
  2028-08-30; Kashiwazaki-Kariwa 6 inspections booked 2027-04 and 2028-08.
- **25 further units carry a single stop entry from 2008–2012 and nothing since** —
  Hamaoka 3–5, Tomari 1–3, Shika 1–2, Tsuruga 2, Tokai 2, Higashidori 1,
  Kashiwazaki-Kariwa 1–5 and 7, Onagawa 3, and units since retired. Those entries
  are the register's leftovers, not news (see anti-patterns).

## Price drivers (trader lens)

1. **Operating units and their availability** — the count of units actually generating,
   and the GW behind it. The HJKS register answers this directly.
2. **Unplanned stops without a return date** (計画外停止, 復旧見通し なし) — the
   surprise that moves a regional balance. Two were open on 2026-10-03, both Kansai.
3. **Periodic inspection calendar** — booked months ahead; overlapping inspections in
   one area in winter or summer peaks are the predictable squeeze.
4. **Restarts of idle units** — NRA approval, prefectural consent, then a test run
   (試運転). Each restart of a ~1.1–1.4 GW unit displaces gas- or coal-fired generation
   for its whole operating cycle. A common rule of thumb is ~1 Mt/yr of LNG per GW
   running — a framing, not a figure to quote without its source.
5. **Regional concentration** — most operating capacity is in Kansai and Kyushu
   (west, 60 Hz); the Tokyo area runs only Kashiwazaki-Kariwa 6. A Kansai outage moves
   western area prices; frequency conversion between 50 Hz and 60 Hz limits relief.
6. **JEPX area spot prices and OCCTO reserve margins** — where an outage becomes a price.
7. **Policy and lifetime rules** — operation beyond 40/60 years and the strategic
   energy plan's nuclear share set the long-run fleet size.
8. **Fuel cycle** — the Rokkasho reprocessing plant's completion schedule and spent-fuel
   storage limits can constrain a plant's operation independently of the reactor.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| NRA — Nuclear Regulation Authority (原子力規制委員会) | Safety reviews, restart approvals, inspection findings, incident reports | NRA |
| JEPX HJKS (発電情報公開システム) | Mandatory register of every generator stop and derating ≥100 MW | JEPX HJKS |
| ANRE / METI (資源エネルギー庁) | Energy policy, strategic energy plan, restart policy, lifetime rules | ANRE |
| OCCTO (電力広域的運営推進機関) | Supply-demand outlook, reserve margins, inter-area flows | OCCTO |
| Kansai Electric (関西電力) | Takahama, Ohi, Mihama — the largest operating fleet | Kansai Electric |
| Kyushu Electric (九州電力) | Sendai, Genkai | Kyushu Electric |
| Shikoku Electric (四国電力) | Ikata 3 | Shikoku Electric |
| Chugoku Electric (中国電力) | Shimane 2; Shimane 3 under construction | Chugoku Electric |
| Tohoku Electric (東北電力) | Onagawa 2, Higashidori | Tohoku Electric |
| Hokkaido Electric (北海道電力) | Tomari 1–3 | Hokkaido Electric |
| Hokuriku Electric (北陸電力) | Shika 1–2 | Hokuriku Electric |
| Chubu Electric (中部電力) | Hamaoka 3–5 | Chubu Electric |
| Japan Atomic Power (日本原子力発電) | Tokai 2, Tsuruga 2 | JAPC |
| TEPCO (東京電力) | Kashiwazaki-Kariwa, Fukushima decommissioning | *not in register — see below* |
| JAIF (日本原子力産業協会) | Fleet status summaries, industry news (Atoms in Japan) | JAIF |
| FEPC (電気事業連合会) | Utilities' federation; fleet-wide statements | FEPC |
| JNFL (日本原燃) | Rokkasho reprocessing and enrichment | JNFL |
| Atomic Energy Commission (原子力委員会) | Cabinet-level nuclear policy | AEC |
| Niigata / Fukui / Ibaraki prefectures | Host consent for Kashiwazaki-Kariwa / the Wakasa plants / Tokai 2 | prefecture |
| Courts (裁判所) | Operating injunctions | Courts in Japan |
| JMA (気象庁) | Earthquake reports — the trigger for precautionary stops | JMA |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| NRA — Nuclear Regulation Authority | nra.go.jp | Conformity review decisions, restart approvals, inspection findings, incident and trip reports, committee agendas | P1 |
| JEPX HJKS outage register | hjks.jepx.or.jp | **Every nuclear stop and derating**: unplanned trips, inspection bookings, expected return dates — crawled daily as a feed | P1 |
| ANRE — Agency for Natural Resources and Energy | meti.go.jp | Strategic energy plan, restart and lifetime policy, electricity supply-demand measures | P1 |
| Kansai Electric | kepco.co.jp | Takahama / Ohi / Mihama operating status, inspection starts and returns, trip notices | P1 |
| Kyushu Electric | kyuden.co.jp | Sendai / Genkai operating status and inspection schedule | P1 |
| OCCTO | occto.or.jp | Supply-demand outlook, reserve margins, tight-supply warnings | P1 |
| JAIF | jaif.or.jp | Fleet operating status summaries; Atoms in Japan news | P1 |
| Shikoku Electric | yonden.co.jp | Ikata 3 status and inspections | P2 |
| Chugoku Electric | energia.co.jp | Shimane 2 status; Shimane 3 review | P2 |
| Tohoku Electric | tohoku-epco.co.jp | Onagawa 2 status; Higashidori review | P2 |
| Hokkaido Electric | hepco.co.jp | Tomari 3 restart path | P2 |
| Hokuriku Electric | rikuden.co.jp | Shika 2 review; post-Noto-earthquake checks | P2 |
| Chubu Electric | chuden.co.jp | Hamaoka review | P2 |
| Japan Atomic Power | japc.co.jp | Tokai 2 safety works; Tsuruga 2 after review rejection | P2 |
| JEPX | jepx.jp | Area spot prices where an outage becomes a price | P2 |
| FEPC | fepc.or.jp | Fleet-wide statements and statistics | P2 |
| Niigata Prefecture | pref.niigata.lg.jp | Kashiwazaki-Kariwa host consent and safety committee | P2 |
| Fukui Prefecture | pref.fukui.lg.jp | Wakasa plants (Takahama, Ohi, Mihama, Tsuruga) — host statements | P2 |
| JNFL | jnfl.co.jp | Rokkasho completion schedule, spent-fuel receipt | P2 |
| Atomic Energy Commission | aec.go.jp | Cabinet-level nuclear policy, white paper | P3 |
| Ibaraki Prefecture | pref.ibaraki.jp | Tokai 2 evacuation planning and consent | P3 |
| Courts in Japan | courts.go.jp | Injunction rulings on reactor operation | P3 |
| JMA | jma.go.jp | Earthquakes near plant sites | P3 |
| IAEA | iaea.org | PRIS reactor database; international review missions | P3 |
| World Nuclear Association | world-nuclear.org | Country profile; fleet reference | P3 |

**Deliberately absent, and why.** `tepco.co.jp` answered **HTTP 403 to every request on
2026-10-03, from both the operator's machine and the VPS** that runs the agent, for the
home page, the English site and the Kashiwazaki-Kariwa pages alike. TEPCO is exactly the
source a Kashiwazaki-Kariwa question wants, but an unreachable domain in the register is
a query that returns nothing, as `epe.gov.br` was on Brazil and `fert.gov.in` on India.
Kashiwazaki-Kariwa is covered instead by HJKS (operating state), NRA (regulation) and
Niigata Prefecture (consent). Re-check TEPCO before relying on it.

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official handle in `source_whitelist.json`; blocked on #31 |

## Infrastructure & logistics

The operating fleet is **PWR-heavy and western**: Kansai's three Wakasa-bay sites in Fukui
(Takahama, Ohi, Mihama), Kyushu's Sendai and Genkai, and Shikoku's Ikata all sit in the
60 Hz grid. The BWRs that have returned — Onagawa 2, Shimane 2 and Kashiwazaki-Kariwa 6 —
are the exception. The east (50 Hz) and west (60 Hz) grids are linked only through
frequency converters, so surplus nuclear output in the west does not fully relieve Tokyo,
and a Kansai trip is felt first in western area prices. Spent fuel is stored on site until
Rokkasho operates, so pool capacity is a slow-moving constraint on individual plants.

## Geopolitical and market triggers

- **An unplanned stop with no return date** at a large unit — the HJKS register shows it
  the day it happens.
- **NRA review decisions** — approvals start a restart path; a rejection (as Tsuruga 2's
  in 2024) ends one.
- **Host prefecture consent or refusal** — the gate after NRA approval, and political.
- **Court injunctions** halting an operating reactor.
- **Earthquakes near a site** — precautionary stops and post-event inspections.
- **Anti-terrorism facility (特定重大事故等対処施設) deadlines** — a unit without the
  facility completed by its deadline must stop.
- **Inspection overlaps in peak seasons** — winter and summer reserve-margin warnings
  from OCCTO.
- **Strategic energy plan and lifetime-extension rules** — the long-run fleet size.
- **Rokkasho schedule changes** — the fuel cycle's credibility and spent-fuel limits.
- **LNG spot (JKM) moves** — the price at which nuclear availability is worth most.

## Data cadence

| Source | Frequency | Observed lag (2026-10-03) |
|--------|-----------|---------------------------|
| JEPX HJKS outage register | event-driven, edited same hour | the newest entry was minutes old |
| NRA committee decisions and incident reports | weekly committee; incidents same day | same day |
| Utility press releases (Kansai, Kyushu, …) | event-driven | same day |
| OCCTO supply-demand outlook | daily / weekly / seasonal | same day |
| JEPX area spot prices | daily | next day |
| JAIF fleet summaries | periodic | days |
| ANRE policy documents | event-driven | — |

**This cadence is the point.** The register changes whenever a unit stops or a booking
moves, so a daily cycle has something to read whenever the fleet does something — and
reads nothing new, cheaply, when it does not.

## Tier 2 context sources

JAIF's Atoms in Japan, World Nuclear Association country profile, IAEA PRIS, OIES and IEA
analyses of Japanese power and LNG demand, academic work on Japan's restart process.
Useful for framing; not primary scan anchors.

## Anti-patterns

- **Reading a 2011 stop entry in HJKS as current news.** Twenty-five units carry a
  single stop from 2008–2012 and no update since — some are retired. Their "open"
  status is a leftover, not an outage.
- **Treating "planned stop" (計画停止) as benign.** Mihama 3's 2026-09-18 stop is filed
  as planned with the cause "under investigation" and no return date. Read the type and
  the cause, not only the stop kind.
- **Treating a 9998/9999 date as a date.** It is the platform's placeholder for "not fixed".
- **Treating NRA approval as a restart.** Prefectural consent, construction of safety
  works and a test run follow, and each can take years.
- **Quoting "Japan's nuclear output" without the area.** The fleet is concentrated in
  the west; the Tokyo area runs one unit.
- **Asserting an LNG volume from a reactor outage.** The chain runs outage → replacement
  generation by fuel → fuel burn → import. Each step needs its own source.
- **Citing TEPCO's site** until `tepco.co.jp` verifies — see above.
- **Inventing operator or ministry domains** not present in `source_whitelist.json`.

## Related playbooks

- japan_korea_lng_demand.md — the LNG demand that nuclear availability swings
- lng_global_supply.md — the supply side of that swing
- southeast_asia_lng_imports.md — competing Asian buyers
- natural_gas_global.md

## Changelog

- 2026-10-03 — initial draft for a customer topic (#55). Every primary domain above was
  verified on 2026-10-03 by **reachability plus page identity**, from the operator's
  machine and for the key ones from the VPS. `tepco.co.jp` failed (HTTP 403 from both)
  and is excluded. The fleet numbers in the executive summary were **read from the HJKS
  register** on 2026-10-03, not estimated.
