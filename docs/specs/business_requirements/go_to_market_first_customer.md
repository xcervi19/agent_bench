# Go-to-market — first customer (PowerTica)

**Status:** plan, written 2026-09-16
**Lane:** Business — *how the India demo becomes a signed, paid engagement*
**Owner:** product owner
**Decision point:** 2026-09-29
**Related:** `business_requirements.md` (what the product is), `STATUS.md` → *What the
customer actually valued (2026-09-10)*, #45 (the topic under demo), #48 / #47 (the manual
work being sold), #16b/#16c + #37 (what "an environment they configure themselves" means),
#52 (how we would defend a quality claim)

---

## Situation

PowerTica — a trading firm with three power plants — saw the India gas demo on
**2026-09-10** and reacted positively. There is **no commercial relationship**: reports are
hand-delivered by the product owner, wired up as an external API, in his capacity as an
employee rather than as a vendor. Nothing is billed.

**The live share is still running and nobody has been asked to read it.** Measured
2026-09-16 against `GET /v1/public/topics/4a6a4504-a7bd-4e0f-ab88-cdff6119d1a6`:

```
update_count: 7      last_updated_at: 2026-09-15T21:59:48Z      share_mode: live
```

Seven delta cycles have landed since publication, one a day, at $2.94 each. That pile is
simultaneously the strongest sales asset we hold and the clearest risk indicator: if nobody
opened it, "interesting" was politeness.

### What we actually have, in numbers

| | |
|---|---|
| Works | India topic end-to-end; `primary_official` **21 % → 53 % → 64 %**; PPAC feed in the output; live shared link; 7 cycles banked |
| Unit cost | plan+deliver **$3.79**; refresh **$2.94 / cycle** → ~$20/week/topic → ~**$1 000/topic/year** |
| Manual | topic onboarding is a person plus an agent. India: whitelist entries 2026-08-20 → good run 2026-09-10 = **~3 weeks**. #48 does not exist; #47 blocks it |
| Missing for a product | report reading and monitoring are **API-only** (`docs/product/README.md`); the UI smoke has never been driven in a browser; accounts are invitation-only; no password reset; **no billing**; cancel does not stop an in-flight run; test2 has an empty RAG |
| Cannot yet defend | the LLM judge runs on OpenAI (#43); one baseline, one topic, one run (#41) |
| Commercial layer | **does not exist in this repo** — no pricing, offer or contract material anywhere (`git log -S` confirms) |

---

## Decision: sell consulting, not a product licence

1. **What the customer buys today is work, not software.** Onboarding, playbook, source
   register, feed adapter, tuning — three weeks per topic. Work is paid for as work.
2. **A licence now commits us to what we do not have** — self-service, SLA, billing,
   multi-tenancy — and fixes a low price on something whose shape will change three more
   times.
3. **Consulting pays for exactly the development that turns this into a product.** #47,
   #48, #16b/c and #37 are scope items of a paid pilot. Productization happens *inside* the
   engagement, not before it.

Framed as a **Design Partner pilot**, not a supplier contract: it gives them a reason for a
price below build rate, and gives us the right to keep the output.

---

## Pricing ladder

Offer **one** price, never a menu.

| Stage | What | Price |
|---|---|---|
| **1. Paid pilot, 8 weeks** | 3 topics (India + 2 of theirs), 2 named users, daily collection / weekly pile, live shared link, 2 tuning rounds, closing review + the source register handed over | **€24 000 fixed** (range 18–30k) |
| **2. Build their environment** | The application they configure themselves — finish #16b/#16c, #37, #48 bootstrap, their accounts | **€75–120 000**, 3–4 months, milestone-billed. Or T&M €950/day with a cap |
| **3. Annual run** | Platform + 5 topics, support, cadence | **€48 000/year**; each further topic €6 000/year |

**Floor: €12 000.** Below that the pilot price becomes an anchor that destroys Stage 2 and 3.

**Anchors to defend it with:** a Bloomberg terminal is ~$30k/year *per seat*;
Platts / ICIS / Argus / Montel packages run €15–60k/year; a fully-loaded junior analyst is
€50–70k/year. The annual price belongs **between a data subscription and an analyst**,
because that is what is being delivered.

**Hook:** 50 % of the pilot fee credits against Stage 2 if they proceed within 30 days of
the pilot ending. A reason to say yes now that does not lower the anchor.

Gross margin at €48k/year against ~$1k/topic COGS is above 95 %. The price is
value-based and must stay that way — cost-plus pricing here gives away the entire product.

---

## Plan — 14 days

**70 % commercial, 30 % keeping the pile alive. No new development.**

### Wed 16.09
- **30 min** — check whether an access log records hits on `/app/shared/<id>`. Did they open
  it, and how often? If no log exists, **do not switch one on**: Caddy is shared with prod
  and test1 is frozen. Replace it with a direct question in the email.
- **60 min** — read all 7 deltas and pull out **three concrete findings in a trader's
  words**. Not "the system works" but *"fertiliser gas use 1 399.7 → 1 773.7 MMSCM,
  April–August, straight from the PPAC feed."* This is also #45's outstanding operator
  review.
- **30 min** — one-page value memo: what was delivered, what it cost, what they said, what
  we propose.

### Thu 17.09
- **The email goes out from a Particle TICO representative, not from a colleague.** Thanks
  for the 2026-09-10 feedback, the live link (7th cycle, daily), the three findings, two
  questions (*which two further topics? who else would read this?*), and a request for a
  45-minute meeting on 22.–24.09 — with the trader **and whoever approves budget**.
- Settle IP and role. Employee vs. vendor is what kills this at legal review, not the price.

### Fri 18.09
- Write the pilot offer (2 pages: scope, deliverables, price, dates, what we need from
  them). **Do not send it** — the offer follows the meeting.
- Price Stage 2 on one page. Price it; do not build it.

### Sat–Sun 19.–20.09
Nothing. Monitoring runs itself for ~$6.

### Mon 21.09
Follow up; if silent, call the trader. The pile will hold ~11 cycles.

### Tue 22. – Thu 24.09 — the meeting, 45 minutes
5 min the live link open on their screen · 10 min the three findings · 5 min *"you said the
primary sources were the most valuable part — here is the first thing we would change"*
(#46 yield counted in primaries, #49 discovery lane) · 10 min the pilot and **the price said
out loud** · 15 min their topics and who will use it.

Answer *"that's a lot"* **with scope, not with a discount.**

### Fri 25.09
Written offer within 24 hours of the meeting, valid to 09.10, naming who signs.

### Mon 28. – Tue 29.09 — decision point
No written yes, or at least a named purchasing process with a date → hand-delivered reports
for PowerTica stop and capacity moves to a second customer.

### Standing rule on free reports
They continue until the meeting + one week at most, and **every one of them is exchanged for
something**: written feedback, a second topic, or an introduction to budget. If they say
"keep sending them", the answer is *"yes — under the pilot, from 01.10."*

---

## Not to be done in these 14 days

- **Do not touch test1.** It holds the demo they will be shown again.
- **Do not build #47, #48 or #49, and do not fill test2's RAG.** None of it sells anything.
  They are pilot scope items, and that is precisely their value.
- **Do not finish the UI.** "An environment they configure themselves" is Stage 2. Building
  it now, unpaid, deletes €75–120k from the offer.
- Do not send a price list with options.

---

## Risks, stated plainly

- **"Interesting" is not demand.** The tests are whether they opened the link and whether
  they will pay anything at all. Both are answerable within 10 days.
- The preference for *official over relevant* is **one desk, one topic, said once** —
  `STATUS.md` already records it as a hypothesis. It belongs in the offer as "this is what
  the pilot verifies", not as a finding.
- **3 topics in 8 weeks is tight** (India took ~3 weeks with the infrastructure already
  built). Either offer 2 topics plus an option, or write into the scope that the third
  topic's onboarding starts after the first tuning round.
- Key-man and IP exposure while the owner is an employee delivering as a vendor.
- The contract must say **decision support, not investment advice or recommendation**
  (MiFID II), carry no accuracy SLA, and define cadence and response times.
