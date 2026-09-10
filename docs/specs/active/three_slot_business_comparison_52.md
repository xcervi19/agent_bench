# Three-slot business comparison — prod vs test1 vs test2 (#52)

**Status:** planned (2026-09-10)
**Lane:** Product / measurement — *are we getting better at the thing the customer buys?*
**Depends on:** #23 (rubric), #41 (multi-run baseline), #43 (Claude judge — no LLM number is
worth tuning against before it)
**Blocks:** any claim that a change improved business value rather than moved a counter
**Related:** #45 (the topic under comparison), #46 (the tuning loop this measures), #49
(discovery — the main candidate for what test2 will change), #20 (monitoring over time)

---

## Why this exists

Three slots now hold three different builds, and the product owner's question is which of
them serves a desk better. Today that cannot be answered, for a reason that has nothing to
do with the rubric: **test2 has no RAG corpus at all.**

Measured 2026-09-10:

| Slot | `documents` | `events` | Build |
|---|---|---|---|
| prod (`agentic`) | 141 | 9519 | `de67d92` |
| test1 (`agentic_test1`) | 141 | 9519 | `test1-stable-2026-09-10` |
| test2 (`agentic_test2`) | **0** | **0** | `main` @ `de67d92` |

The plan leg retrieves from that corpus, so a test2 run is not a worse version of a test1
run — it is a differently-shaped one, missing an input the other two have. Any comparison
across the three today measures the corpus gap and reports it as a quality difference.

`events` is the searched corpus, not `documents`; a count of documents alone will look
right and prove nothing.

## Core question

*Given the same topic run on three builds, can we say which produced the more valuable
result for a trading desk — and defend the answer against the objection that we measured
news-cycle variance, corpus differences, or our own rubric's preferences?*

## Scope

### 1. test2 gets its own RAG, verifiably equal to the other two

Not "a corpus" — the *same* corpus, or the comparison has a confound baked in from the
first run.

- Replicate the 141 documents / 9519 events into `agentic_test2`.
- Set `ivfflat.probes = 10`, as prod and test1 both carry. A different probe count changes
  what retrieval returns without changing what the corpus holds, which is the subtlest way
  to make two slots quietly incomparable.
- Verify parity the way test1 was verified on 2026-09-01: `md5` over ids **and** summaries,
  the same tenant (`0000…0001`), the same counts. Record the numbers in this ticket.
- Re-verify before each comparison round. A corpus that drifts between rounds invalidates
  the round, and drift is silent.

### 2. The three builds are pinned and named

A comparison of "prod vs test1 vs test2" is meaningless six weeks later unless each arm
says what it was.

- Each arm records the commit it ran. test1 is `test1-stable-2026-09-10`; the others get
  tags at the moment of the run.
- **`GET /v1/agent/info` still returns no build SHA.** This is the third time the deployed
  state has had to be reconstructed by hand (see the retired rollback anchor in `STATUS.md`).
  Add it — a comparison whose arms cannot identify themselves is not evidence. Small enough
  to live in this ticket rather than its own.

### 3. The measure is business value, not counters

The counters (`primary_official` share, `evidence_count`, `feeds_count`, cost per cycle)
say the inputs arrived. They do not say the output was worth reading, and #45's second run
is the cautionary case: the primary share rose *and* two of the four inputs were broken.

- Score with #23's rubric, absolute and relative.
- **Re-weight first, against what the customer said on 2026-09-10** — the primary sources
  were the most interesting part, *including one ranked low on relevance*, and a Bloomberg
  article was less interesting for being unofficial. If the rubric weights relevance above
  publisher class for a country-fundamentals topic, it disagrees with the buyer, and tuning
  against it optimises for the wrong thing. Decide the weights **before** seeing the scores.
- The judge stays heuristic until **#43**. No `--evaluator llm` number is tuned against
  while the judge runs on OpenAI.

### 4. The comparison is honest about variance

- **#41's caveat governs**: a single run per arm cannot separate a build difference from
  news-cycle variance. Either run N≥3 per arm or state the result as directional and
  unproven — those are the only two honest options.
- Same topic string, same brief, same window, arms run close together in time. News moves
  daily and the India topic is monitored daily.
- **Stagger the runs.** One Claude subscription is shared by every slot on the box; three
  concurrent delivers contend for it and the timing data becomes noise.

### 5. Only test2 moves

Per the slot policy: test1 is frozen and prod is untouched. test2 is the arm that carries
whatever change is being evaluated — the current candidate being **#49**'s discovery lane,
since improving automatic discovery of primary sources is the stated direction and the
customer's feedback is the strongest argument for it yet.

That asymmetry is the design, not a flaw: test1 and prod are the controls, and a control
you keep editing is not one.

## Out of scope

| Not here | Owner |
|---|---|
| Moving the judge off OpenAI | **#43** |
| The rubric's categories and scoring machinery | **#23** |
| N≥3 repeat-run harness | **#41** |
| What test2 actually changes | **#49**, and whatever follows it |
| Monitoring-over-time evaluation | **#20** |

## Acceptance criteria

- [ ] `agentic_test2` holds 141 documents / 9519 events, `ivfflat.probes = 10`, verified by
      `md5` over ids and summaries against prod, with the numbers recorded here
- [ ] `GET /v1/agent/info` reports the running commit on all three slots
- [ ] Rubric weights reviewed against the 2026-09-10 customer feedback, and the decision
      recorded **before** any comparison run is scored
- [ ] One comparison round: the same topic on all three arms, each arm's commit named, run
      close together in time and staggered
- [ ] A written verdict that states its own confidence — including "directional only" if
      N=1 — and names what would change it

## Open questions

- **Which topic?** India is what the customer judged, which argues for it; India is also
  the topic test1 has been tuned on, which argues against — test1 would win on home
  ground. A second country topic would be fairer and is not yet built.
- **Does prod belong in the comparison at all?** It runs the pre-#45 build, so it mostly
  measures how far we have come rather than which direction to go next. Keeping it is
  cheap; reading it as a live option is not.
- **How often?** Every round costs three delivers plus judging. Per-milestone is probably
  right; per-change certainly is not.

## Related

- `STATUS.md` → **Slot policy** and **What the customer actually valued**
- `docs/specs/active/india_gas_country_pilot_45.md` — the topic and its second run
- `docs/specs/active/discovery_lane_and_promotion_49.md` — the likely test2 arm
- `docs/specs/active/multi_run_evaluation_baseline_41.md` — why N=1 cannot settle this
- `docs/ops/db_commands.md` — corpus replication between slots
