# Insurance & vessel-tracking source branch for chokepoint topics — #44

**Status:** planned
**Lane:** Product / quality — *whether the report can answer the question it was asked*
**Depends on:** #29 (whitelist), #30 (playbooks), #32 (`source_discover`), #39 (source authority)
**Related:** #31 (scraping — the official-social gap below is blocked on it), #41 (measurement caveat)

## Problem

The frozen evaluation baseline `testing/baselines/hormuz_90d_2026-08-01`
(topic `a83a1d57`) scores **`primary_source_discovery` 1.8/5** — 7 of 28 sources
primary/official. Research Quality is 4.59 and Trading Intelligence 4.36 on the
same run, so the agent reasons well over what it finds. What it finds is the
problem, and the baseline README already names the lever:

> **`primary_source_discovery` 1.75/5** — 7 of 28 sources primary/official.
> #39 stopped the freshness filter deleting primaries; it did not create more.
> Whitelist coverage for maritime/insurance primaries is the open lever.

The client brief (`testing/baselines/hormuz_90d_2026-08-01/topic.txt`) asks, in
its own words, for:

> war-risk insurance premiums and whether underwriters have withdrawn cover for
> Gulf calls

The delivered report answered it from trade press, because there was no primary
source in the system that could answer it. Every war-risk premium figure in the
report (`~1-3% → 7.5-10% of hull value`) is sourced `[s05, s11, s13]` —
secondary reporting on the insurance market rather than the market's own
publications.

## Diagnosis

Two separate causes. Fixing either one alone changes nothing.

### 1. Inventory — there is no insurance source to find

`source_whitelist.json` holds 610 entries: **602 `type: official`, 8
`type: data_feed`**. Breaking down by category, `shipping` has 11 entries (IMO,
MARAD, UKMTO, Baltic Exchange, ICS, USCG NAVCEN, Rosmorport, Equasis, EMSA,
Sabine-Neches, Oman MSC).

There is **no marine-insurance body anywhere in the file** — no Joint War
Committee, no International Group of P&I Clubs, no IUMI, no IMB Piracy Reporting
Centre. There is likewise no vessel-tracking or AIS-derived data feed.

### 2. Routing — a whitelist entry alone never reaches the topic

`discover_sources_for_topic` (`apps/claude_agent/sources/discover.py:145-166`)
resolves a topic to sources through exactly two paths:

```python
named = entities_named_in(whitelist, t)
playbook_hits = playbooks_for_topic(playbooks_root, t, {e.domain for e in named})
return _assemble(t, named, playbook_hits, resolve_playbook_entries(playbook_hits, whitelist, t))
```

`entities_named_in` (`apps/claude_agent/sources/whitelist.py:82-95`) requires the
entity name to be **literally present in the brief** — it token-matches the
entity against the topic text. The brief says "war-risk insurance premiums" and
"underwriters"; it does not say "Joint War Committee". So a whitelist entry that
is not also referenced by a matched **playbook** is unreachable for this topic.

**The playbook is the routing layer; the whitelist is only the register.**

### 3. The playbook names the driver and maps it to the wrong sources

`local_knowledge_sources/playbooks/strait_of_hormuz.md` lists as price driver #4:

> War-risk premiums and convoy/escort posture (Royal Navy, regional navies).

It identifies war-risk premiums as a top-four price driver and then routes them
to **navies**. Navies publish escort posture; they do not publish premiums or
underwriting terms. Neither *Key entities* nor *Primary Official Sources* nor
*Tier 2 context sources* contains an insurance entity.

So the chain is: brief asks for premiums → playbook routes to navies → whitelist
has no underwriter → report falls back to trade press → `primary_source_discovery`
1.8/5.

## Also in scope (same files, same review)

- **Dead P1 query.** The playbook lists `nioc.ir` as **P1**. #39 recorded
  `site:nioc.ir` returning **0 results across both monitored cycles**, and the
  baseline report's own *Risks & blind spots* section says official Iranian sites
  "returned only generic background pages, not current operational data, despite
  being queried directly". The query is generated because the playbook ranks the
  domain P1. Demote or drop it, and record why in the changelog.
- **Empty official-social section.** The playbook's *Official Social Media* table
  is a single em-dash row: *"No verified Telegram/X handles in
  `source_whitelist.json`"*. UKMTO and CENTCOM post to X before their web pages
  update, and this is the largest available lever on `information_latency`
  (0.0/5 on the baseline). **Out of scope here** — it depends on #31 scraping
  infrastructure. Note it in the playbook so the gap is visible rather than
  implied.

## What to change

All three edits ship together or not at all.

1. **`source_whitelist.json`** — add a marine war-risk / vessel-tracking tier.
   **Free-publishing sources only** (see Non-goals). Candidates to verify before
   adding: Joint War Committee listed areas (Lloyd's Market Association),
   International Group of P&I Clubs circulars, IUMI, IMB Piracy Reporting Centre,
   plus the EIA/IEA chokepoint series if not already reachable. Each entry needs
   `entity`, `domain`, `type`, `category`, `notes`, `agreement_count` — the schema
   is enforced by `load_whitelist` (`whitelist.py:27-51`) and a missing
   `entity`/`domain` raises. Consider whether these want a new `category`
   (`insurance`) or fit `industry_body`.
2. **`local_knowledge_sources/playbooks/strait_of_hormuz.md`** — rewrite price
   driver #4 to route to the new sources, add them to *Key entities* and
   *Primary Official Sources* with scan priorities, and bump *Last reviewed* +
   *Changelog*. Without this the whitelist entries stay unreachable.
3. **`nioc.ir`** — demote from P1 or remove, with the reason recorded.

Consider whether the other chokepoint playbooks with the same driver
(`red_sea_bab_el_mandeb.md`, `turkish_straits_bospor.md`) need the same branch;
if so this becomes a shared *war-risk* source block rather than a Hormuz-local
edit.

## Deployment note — this is not a hot config change

`docker/Dockerfile.claude_agent:49-50` bakes both files into the image:

```dockerfile
COPY source_whitelist.json ./
COPY local_knowledge_sources/playbooks ./local_knowledge_sources/playbooks
```

They are **not** volume-mounted (`docker-compose.yml` mounts only
`claude_agent_fe`, `claude_home`, `state` into `claude_agent`). Editing either
file on disk changes nothing on a running slot — it requires an image rebuild and
redeploy. Plan this as a deploy, not a config tweak, and do not land it on a slot
that is about to be shown to anyone.

## Verification

Re-run `testing/baselines/hormuz_90d_2026-08-01/topic.txt` **verbatim** (the
baseline README is explicit that a different brief measures the topic, not the
system) and compare:

```bash
scripts/evaluate_output.sh relative \
  --baseline  testing/baselines/hormuz_90d_2026-08-01 \
  --candidate testing/results/prod/<new-run>
```

Primary signal: `primary_source_discovery` moves off 1.8/5, and at least one
war-risk premium claim in the new report cites an underwriting body rather than
trade press. Secondary: the #39 `SourceMix` primary/official share.

**Measurement caveat (#41).** One run against a live web is not a verdict — the
run-to-run spread has never been measured and four of the five categories at 40 %
weight move with the news cycle. `primary_source_discovery` is one of the more
structural categories, so a large move is meaningful, but do not read a ±0.3
delta as a result.

## Non-goals

- **Paywalled aggregators.** Lloyd's List Intelligence, Vortexa, Kpler and
  similar would look authoritative in the whitelist, but the fetcher cannot read
  them; they would be counted as discovered sources while contributing no text,
  diluting the source mix with entries that resolve to nothing. Excluded
  deliberately. Revisit only if licensed access exists.
- **Official social handles** — blocked on #31.
- **The `information_latency` 0.0/5 gap** — a different problem with a different
  cause; not addressed here.
