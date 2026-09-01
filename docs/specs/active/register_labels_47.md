# Register labels — restore the country and role we already annotated (#47)

**Status:** planned (2026-08-23)
**Lane:** Platform / Data — *making domain selection a set query instead of lexical guessing*
**Depends on:** #29 (whitelist), #30 (playbooks), #32 (discover)
**Blocks:** **#46 build item 0** (`allowed_domains`) — do not ship the filter before this
**Related:** #45 (first topic to need it), #48, #49

---

## Why this exists

`entities_named_in` (`sources/whitelist.py:82`) picks whitelist entries by matching the
**entity name** against the topic, as a bag of tokens. It never looks at the domain. The
country of a source is encoded *only* in its domain. So the matcher cannot know a country
exists, and routes across borders.

Two mechanisms, both measured on the India gas topic:

**1. One institution's name is a subset of another's.**

```
entity "Ministry of Petroleum"  [mop.ir, Iran]  → tokens {ministry, petroleum}
topic contains "Ministry of Petroleum and Natural Gas"
covers({ministry, petroleum}, topic) = True     → Iran routed into an India topic
```

**2. Tokens are collected from the whole text, with no phrase structure.**

```
entity "Ministry of Power, Energy & Mineral Res"  [mpemr.gov.bd, Bangladesh]
_name_variants splits on the comma → head "Ministry of Power" → {ministry, power}
the phrase "Ministry of Power" NEVER APPEARS in the topic:
   'ministry' came from "Ministry of Petroleum and Natural Gas"
   'power'    came from "power generation"
the two tokens sit 115 characters apart and are unrelated  → Bangladesh routed in
```

`_name_variants` (`whitelist.py:77`) makes this worse. Splitting on a comma and keeping the
head is right for `"ADNOC — Abu Dhabi National Oil Company"` (head = the distinguishing
part) and exactly backwards for `"Ministry of Power, Energy & Mineral Res"` (head = the
generic part). The rule assumes names run specific→generic; institution names run the other
way.

And the mirror failure: `covers` requires **every** entity token, so precise long names are
harder to match than vague short ones. `"Petroleum Planning & Analysis Cell (PPAC)"` did not
match a topic that literally says PPAC, because `planning`/`analysis`/`cell` were absent. The
register systematically favours its least specific entries.

## The root cause is not the matcher

The labels that answer all of this were annotated and then dropped at merge:

```
docs/knowledge/source_catalog/…/catalog.json    1139 entries / 741 domains
   id, country, geo_target, authority_type, social_role,
   entity, domain, category, type, signals, status, notes

source_whitelist.json                            622 entries   ← what runtime uses
   entity, domain, type, category, notes, agreement_count
                    ↑ no country, no authority_type, no signals
```

The catalog knows `mop.ir` is `country: IR`. The whitelist does not. The matcher guesses
lexically because the structured answer was taken away from it.

## What to do

### 1. Rejoin — 84 % is free

Measured: **527 of 622** whitelist domains rejoin the catalog by domain. Of those, **495**
carry `country`, **443** `authority_type`, **527** `signals`. The remaining ~95, plus the 12
India gas entries added in #45, need labelling by hand — bounded, one-off.

Also sitting unused: **213 catalog domains never merged into the whitelist at all.**

### 2. Extend the schema

Add `country` (ISO-3166-2), `authority_type`, `sector`, `signals` to `source_whitelist.json`
and `WhitelistEntry`. Keep `entity`/`domain`/`type`/`category` as they are.

`sector` is new — the catalog has none, and it is what the India case needed: its authority
slots are a **crude-export skeleton** (`ministry_petroleum`, `noc`, `mfa`, `customs_export`,
`upstream_regulator`, `port_maritime_authority`, `national_exchange`, `central_bank`,
`environment_regulator`, `coast_guard_navy`) with nothing for demand statistics, downstream
regulation, transmission, import terminals or power dispatch. See #48.

### 3. Select by label, not by name

Replace `entities_named_in` as the routing mechanism with a set query — `country=IN AND
sector IN {gas, power}`. Keep lexical matching only as a fallback for entities a topic names
explicitly. Selection becomes deterministic and, crucially, **enumerable**: you can list what
a label selected and diff it against the register. Gate 3 of #46 is trivial with this and
impossible without it.

### 4. Let playbooks declare labels

Today a playbook enumerates domains in its `Primary Official Sources` table, so a domain
added to the register is invisible until someone edits the playbook. A playbook that declares
`country=IN, sectors=[gas, power]` picks up new register entries automatically — that is the
structural form of "nothing must escape". **Keep the table** as priority (P1/P2/P3) and
what-to-watch: labels give coverage, the table gives ranking.

## Acceptance criteria

- [ ] `country` / `authority_type` / `sector` / `signals` on every whitelist entry; rejoin script committed, hand-labelled remainder reviewed
- [ ] The 213 unmerged catalog domains triaged — merged or explicitly rejected with a reason
- [ ] Label-based selection replaces `entities_named_in` for routing; lexical match kept as a named-entity fallback
- [ ] India gas topic routes to **zero** non-India authorities (today: `mop.ir`, `mpemr.gov.bd`, `powerdivision.gov.bd`)
- [ ] Playbooks may declare label selectors; `india_gas_demand.md` converted as the first case
- [ ] Coverage report per topic: which label slots are filled, which are empty (Gate 3 of #46)

## Open questions

- Is `sector` a flat list or does gas/power/crude need a value-chain position too (produce / import / transport / regulate / consume / report)? #48 needs the latter.
- Multi-country bodies (IEA, OPEC, EU) — `country: null` plus a `scope: global|regional` label?
- Do we keep `agreement_count`, now that it was the tiebreaker for a ranking we are replacing?
