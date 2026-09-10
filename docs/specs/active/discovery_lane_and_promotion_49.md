# Discovery lane and source promotion — keep the system from closing in on itself (#49)

**Status:** planned (2026-08-23)
**Lane:** Product / quality — *how the register grows after a topic is seeded*
**Depends on:** #42 (evidence store — the substrate), #47 (labels — promotion writes into them), #46 build item 0
**Related:** #48 (seeds what this grows), #39 (source authority), #20 (monitoring evaluation)

---

## Why this exists

`allowed_domains` is a closed world by construction. It makes the system reliable and, left
alone, blind: a source that is not in the register can never be found, so the register can
never grow, so the blindness is permanent. The filter is the right answer to reliability and
the wrong answer to discovery, and the two need separate machinery.

Today unfiltered queries exist **by accident** — they are whatever the plan agent did not
scope to a domain. They need to exist **by mandate**, with their own budget and their own
metric.

And there is a second, larger gap: **nothing learns.** An excellent unknown source can be
found, read, cited in a report — and is then forgotten. It never enters the register. There
is no path from "this turned out to be good" to "we will look here next time".

## Two lanes

| | Lane A — known | Lane B — unknown |
|---|---|---|
| Mechanism | label-selected `allowed_domains` (#47) | unfiltered queries |
| Job | guarantee the known authorities are covered | find what the register lacks |
| Budget | the majority | a **reserved** share, ~25–30 % |
| Measured by | primary-source share, slot coverage | **new-domain discovery rate** |

Lane B must not be judged on report citations. Its output is candidates, most of which will
be rejected; scoring it on citations would quietly starve it.

**A third channel makes both affordable.** For sources we already know, search is the wrong
instrument — we know the URL, we need to *read it on a cadence*. RSS, sitemap, or direct
polling of a ministry's news page costs zero search budget. #42's fetcher already does
robots-respecting reads; it only lacks a second writer into `SearchDocument`
(`search_evidence.py:66` is currently the only one, and it is fed exclusively by WebSearch).
Moving known-source polling off the search budget frees the whole aperture for Lane B.

## Promotion — the missing loop

The evidence needed to judge an unknown domain is **already being collected**. Nothing new
has to be captured:

| store | what it says about an unknown domain |
|---|---|
| `search_observations` | how many distinct queries surfaced it, at what rank, across how many cycles |
| `search_queries` (#46) | whether it appeared **without** a domain filter — i.e. genuinely new |
| `search_documents.fetch_status` | whether we can read it at all, or it is paywalled / blocked |
| `news.json#sources` | whether it was cited, with `source_class`, `relevance_score`, `novelty_score` |
| `topics/source_quality.py` | deterministic classification; `AUTHORITATIVE_CLASSES` |

Pipeline: unknown domain appears → evidence accumulates over cycles → a scoring pass ranks
candidates → the **weekly review** shows the operator ~5 with their evidence → accept or
reject → accepted domains are written into the register with labels (#47) → next cycle they
are in Lane A.

The loop closes on the weekly review the customer already agreed to do, which is what makes
it cheap.

## Where this gets poisoned, and the defence

"An agent judges whether a source is good" is precisely where a register fills up with
confident, fluent SEO content. The defence is to keep the model away from the verdict:

- **The model writes the summary; the signals decide.** Deterministic class
  (`source_quality.py`), `fetch_status` (what we cannot read we cannot verify), and
  **repeated independent surfacing** across distinct queries and cycles — none of which can
  be talked into existence.
- **Human gate, at least initially.** Source authority is the entire product claim (#39).
  A two-minute weekly decision over five candidates is not a bottleneck worth automating away.
- **Promotion is reversible.** A promoted domain that stops earning its place gets demoted;
  record why, so the same domain is not re-promoted next quarter.

## Acceptance criteria

- [ ] Lane B has a reserved share of the query budget, set in config, not left as a residue
- [ ] New-domain discovery rate reported per cycle, separately from primary share
- [ ] A second writer into `SearchDocument` for known-source polling (RSS / sitemap / direct), costing no search budget
- [ ] Candidate dossier computable from existing stores with no new capture
- [ ] Weekly review surfaces ranked candidates with their evidence; accept writes a labelled register entry
- [ ] Demotion path exists and records a reason
- [ ] Measured over ≥4 India cycles: how many candidates surfaced, how many promoted, and whether primary share moved

## Out of scope

- The register schema — **#47**
- Seeding a topic from zero — **#48**
- The general judging pass over the whole corpus (#42's non-scope; #46 build item 1b) — this ticket only judges *domains*, not every document

## Open questions

- How many cycles of independent surfacing before a domain is even a candidate? Too few and the register fills with noise; too many and discovery feels dead to the operator.
- Should promotion be per-topic or global? A source that is authoritative for India gas may be noise for Hormuz.
- Does Lane B's budget scale with topic age — more exploration early, more exploitation later?

---

## Customer signal, 2026-09-10 — the case for the unfiltered lane

First feedback on the India demo (#45): the **primary sources were the most interesting
part, including one the system ranked low on relevance**, and a Bloomberg article was less
interesting for being unofficial.

That is the strongest argument this ticket has. The value the customer named lives in
official sources — and the register is a closed world, so a domain filter can only ever
return the primaries **we already know about**. The unfiltered discovery budget is how a
ministry, regulator or state utility nobody has registered yet gets in front of a desk at
all.

It also aims the promotion criteria: promote on **publisher class and independent
resurfacing**, not on how often a document was cited. A source can be worth keeping while
being cited rarely — the low-relevance primary the customer singled out is exactly that
case, and a click- or citation-weighted rule would have demoted it.
