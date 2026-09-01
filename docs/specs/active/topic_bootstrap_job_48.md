# Topic bootstrap job — seed a new topic's knowledge and register automatically (#48)

**Status:** planned (2026-08-23)
**Lane:** Product / Platform — *the onboarding work currently done by hand, per customer*
**Depends on:** **#47** (labels — without them the output lands in unlabelled soup)
**Blocks:** country #2 and every subsequent demo topic at acceptable cost
**Related:** #46 (this is Gates 1–3, executable), #45 (the manual run this generalises), #49 (grows what this seeds)

---

## Why this exists

Onboarding India took a person and an agent working together: read the operator's brief,
work out how the market functions, find who publishes what, verify the domains, write the
playbook, add the register entries. That is the work that has to happen for **every** new
customer topic, and at the moment it happens by hand.

It has been done before, twice, both times as a one-off for the whole world at once:

| leg | produced | how it ran |
|---|---|---|
| `.cursor/skills/trading-geopolitical-analyst/source-catalog-brief.md` | authority catalog — 1139 entries, 64 countries × 10 roles | once, across several agents, reviewed batch by batch |
| `…/playbook-template.md` | 55 coverage playbooks (#30) | once |
| `source_ingest/` | RAG corpus | ongoing, but **general trading books only** |

So this ticket is not a new capability. It is **running those three legs for one topic, on
demand**, instead of for the whole world once.

## The three legs, and what each must do differently

### Leg 1 — Education: acquire it, because the corpus does not have it

The RAG corpus is Yergin's *The Prize*, *Oil Trading Manual*, *Petroleum Refining*,
*Commodities Demystified*, the OIES corpus, *Ports and Terminals*. It teaches what a crude
benchmark is. **It contains nothing about how Indian gas works** — not one document. So
#46's Gate 2 ("draft from brief + RAG + web") has an empty RAG leg for every new topic.

The job must find and ingest 5–15 authoritative explainers for the topic. For India those
exist and surfaced unprompted during scoping: the IEA *India Gas Market Report*, PNGRB's own
2030/2040 projection and vision PDFs, PPAC methodology — plus the customer's Platts deck.
Ingest via `source_ingest/preprocess.py` + `ingest.py` with a topic-scoped `document_type`
(precedent exists: `playbook`, `methodology`). #42's fetcher already reads PDFs, so
acquisition is largely solved.

Then playbook drafting and query wording stand on **read text** rather than model recall.

### Leg 2 — Authorities: derive the role skeleton from the value chain

The catalog's ten slots are a **crude-export skeleton**. Compare what the India gas topic
actually needed, none of which any slot covers:

| what the topic needed | who | in the 10 slots? |
|---|---|---|
| who publishes the balance | PPAC | no |
| who regulates distribution | PNGRB | no |
| who operates transmission | GAIL | no |
| who operates import terminals | Petronet | no |
| who runs the power system | CEA / NPP | no |
| consuming ministry | Fertilizers | no |

This is why the India catalog batch existed and was still useless here. The job must derive
roles from the commodity's chain — *who produces, who imports, who transports, who regulates,
who consumes, who publishes the numbers* — and only then look for the institutions filling
them. The skeleton is an output of the topic, not a constant.

### Leg 3 — Verification is code, not judgment

An agent asked "who are the authorities for Indian gas" returns a confident, plausible list
containing dead and invented domains. The catalog already anticipates this with
`status: proposed | unverified`. What made the #45 list safe was the mechanical check —
reachability plus page identity — which correctly refused `fert.gov.in` and `grid-india.in`.
That check is **mandatory in the job**, not an optional final step.

## Output, and where it feeds back

Three channels, all of which already exist:

- labelled register entries (#47) → `allowed_domains` batches → Lane A of #49
- a drafted playbook → routing and priorities
- ingested education → RAG → framing and query wording in the plan stage

The job seeds the register at t=0; #49's discovery and promotion grow it every week after.
Together they are the whole lifecycle of a topic.

## Risk, stated plainly

Of everything in the #45/#46/#47/#48/#49 set, this has the highest leverage **and** the
highest chance of producing confident nonsense, because every leg is generative. Three
guards:

1. verification as code (Leg 3);
2. `status: proposed` until a human signs the batch — as the catalog run already did;
3. **measure the job by the next run's primary-source share, not by how good the list looks.**

## Acceptance criteria

- [ ] One command takes a topic brief and produces: an education set ingested to RAG, a draft playbook, and labelled candidate register entries — all `status: proposed`
- [ ] Role skeleton derived from the topic's value chain, not from the fixed 10 slots; India's gas roles come out of it
- [ ] Every candidate domain reachability- and identity-checked before it is offered; failures recorded with a reason, not dropped
- [ ] Re-run on India reproduces the hand-built #45 result — same primaries, no invented domains, and it independently refuses `fert.gov.in` / `grid-india.in`
- [ ] Human review step over a batch, as in the original catalog run
- [ ] Measured: primary-source share of the first topic run after bootstrap vs. before

## Out of scope

- Discovery and promotion of sources the job did not find — **#49**
- The register schema itself — **#47**
- The judging pass over the captured corpus (#42's non-scope; #46 build item 1b)

## Open questions

- How much of the education set can be chosen automatically before human review stops being real review?
- Licensed input (the Platts deck): correct the playbook from it, or ingest it? Ingesting third-party licensed content into a shared corpus needs a licensing decision first.
- Does each topic get its own RAG namespace, or does topic education pollute the general corpus for other topics?
