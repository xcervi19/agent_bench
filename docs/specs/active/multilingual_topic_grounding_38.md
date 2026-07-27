# Multilingual Topic Grounding — #38

**Status:** implemented, awaiting deploy
**Lane:** Platform / Backend
**Goal:** Make source grounding work for topics written in any language, by converging every internal representation on English while still accepting multilingual input from operators and from the web.

## Problem

Source grounding is lexical. `source_discover` (#36) matches the words of a topic against `source_whitelist.json` (#29) and the playbooks in `local_knowledge_sources/playbooks/` (#30). Both are written in English.

A production topic submitted in Czech — *"Situace kolem Hormuzského průplavu, ropa a plyn…"* — resolved **zero** entities and **zero** playbooks. The plan agent therefore got an empty `source_targets.json`, searched the open web unscoped, and produced a report with nothing from the whitelist. The pipeline reported success at every stage; only the report quality showed the failure.

Two independent causes:

1. **The tokenizer was ASCII-only.** `apps/claude_agent/sources/text.py` split on `[^a-z0-9]+`, so every non-ASCII character acted as a delimiter. `Hormuzský` became `hormuzsk`, `México` became `m` + `xico`. This also silently damaged the 27 accented entries already in the whitelist, so it was never purely a "foreign input" bug.

2. **No translation step.** Even with perfect tokenization, `ropa` will never match `crude oil` and `Estreito de Ormuz` will never match `Strait of Hormuz`. Shared proper nouns can be rescued lexically; vocabulary cannot.

## Design

Two layers, because the two causes need different tools. The split matters: the cheap layer must not depend on the expensive one being available.

### Layer 1 — deterministic normalization (always on)

`apps/claude_agent/sources/text.py`:

* **Diacritics folding.** `fold()` applies NFKD and drops combining marks, so `Hormuzský` and `Hormuzsky` produce the same token. Tokenization is now Unicode-aware, so non-Latin scripts survive as whole tokens instead of vanishing — they still will not match an English whitelist, but a zero-target topic is now visible in the tokens rather than hidden by the splitter.

* **Inflection-aware matching.** `token_matches(canonical, topical)` accepts a canonical token that is a prefix of the topical one, above `MIN_PREFIX_LEN = 4`. Latin-script languages inflect by suffix, so `hormuz` matches the Czech genitive `hormuzskeho`. The relation is **directional** on purpose — only the canonical side may be the prefix — which halves the false-positive surface.

The prefix rule admits some noise (`port` matches `portugal`). This is a deliberate trade: a false positive adds one more *whitelisted official domain* to a list the plan agent ranks, while a false negative costs all grounding. The whitelist remains the hard filter, and multi-token entity names must match every token, which is what keeps the noise bounded.

**Result:** the Czech Hormuz topic goes from 0 to 21 entities and correctly selects `strait_of_hormuz.md`, with no LLM involved.

### Layer 2 — `topic_parse` agent leg (best-effort)

A new slash command, `/newsfind-topic-parse`, runs before `source_discover` and writes `facets.json`:

```json
{
  "schema_version": "0.1.0",
  "canonical_topic_en": "Strait of Hormuz oil and gas supply risk",
  "input_language": "cs",
  "geo": ["Strait of Hormuz", "Persian Gulf"],
  "commodity": ["crude oil", "LNG"],
  "entities": ["NIOC", "ADNOC"],
  "signals": ["shipping disruption", "exports"],
  "source_languages": ["en", "ar", "fa", "cs"]
}
```

It does no research — no WebSearch, no WebFetch, no RAG — so it costs seconds and cents. `discovery_query()` concatenates the English facets *and* the original topic before handing them to `source_discover`, so the layer-1 inflection matches are never lost to a translation that dropped a proper noun.

Facets are cached at `state/news/<topic_hash>/facets.json`, per topic rather than per run, so refreshes and re-plans pay for the leg once.

**Degradation is the central property.** Grounding is an optimization over an agent that can still search the open web, so no failure here may cost the operator a report. A leg that times out, is missing from the allowlist, returns malformed JSON, or returns an empty `canonical_topic_en` falls back to `fallback_facets()` — the untranslated topic, which is exactly pre-#38 behaviour. Degraded facets are **not** cached, so a transient failure does not poison the topic. `source_discover` degrades the same way when the whitelist or playbooks are missing from the image, rather than failing the topic as it did in #36.

### Language policy

* **Internal representation: English.** `canonical_topic_en` drives framing, and every artifact the agent writes is English.
* **Search queries: multilingual.** A ministry publishes in its own language and an English-only query never reaches it. `source_languages` drives the existing ≥30 % non-`en` rule in `/newsfind-plan`.
* **Operator input: any language.** Handled by the two layers above; nothing is enforced at the API boundary.

## Observability

A grounding regression previously looked identical to a thin news week. `evaluation.json` now carries a `grounding` block, and the QA gate checks three things at `severity: "warning"` — reported, never gating, because a weakly grounded report is still a report:

| Check | Meaning when red |
|---|---|
| `stage_progression_source_discover` | Deploy gap: the image predates the grounding pipeline. |
| `source_targets_resolved` | Zero targets: whitelist/playbooks missing, or the topic was never translated. |
| `whitelist_source_ratio` | Targets resolved but the agent ignored them; reads like a generic web search. |

`min_whitelist_ratio` defaults to `0.15` — a floor asserting grounding reached the output, not a target. A healthy report also cites wire services and specialist outlets that are not on the whitelist.

`qa_check_run.sh` now honours `severity`: `failed_checks` counts only `error` rules, `warnings` collects the rest.

## Guarding the deploy gap

Deployments override `CLAUDE_AGENT_ALLOWED_COMMANDS` in their own `.env`, replacing the `config.py` defaults wholesale. Adding a leg in code is therefore not enough to make it run — and because `topic_parse` degrades silently by design, the only symptom would be a thin report. `app.py` now warns at startup when a command the topic pipeline drives is missing from the allowlist.

## Files

| File | Change |
|---|---|
| `apps/claude_agent/sources/text.py` | Folding, Unicode tokenization, directional prefix matching |
| `apps/claude_agent/sources/whitelist.py` | Uses `covers` / `explained_by` / `contains_folded` |
| `apps/claude_agent/sources/playbooks.py` | Uses `matched_tokens` / `contains_folded` |
| `apps/claude_agent/topics/facets.py` | New — facets contract, fallback, cache, discovery query |
| `apps/claude_agent/topics/pipeline.py` | `run_topic_parse` stage; `source_discover` degrades on missing data |
| `apps/claude_agent/config.py` | `/newsfind-topic-parse` allowlisted; `topic_parse_timeout_sec` |
| `apps/claude_agent/app.py` | Startup warning for disabled pipeline commands |
| `claude_agent_fe/.claude/commands/newsfind-topic-parse.md` | New leg |
| `claude_agent_fe/.claude/commands/newsfind-plan.md` | Consumes `facets.json`; language policy |
| `scripts/test_vector_runner.sh` | `grounding` block in `evaluation.json` |
| `scripts/qa_check_run.sh` | Severity-aware verdict; three grounding checks |
| `testing/qa_rules.json` | New rules + `min_whitelist_ratio` |

Tests: `tests/sources/test_multilingual.py`, `tests/topics/test_topic_parse_stage.py`.

## Deploy checklist

1. Add `/newsfind-topic-parse` to `CLAUDE_AGENT_ALLOWED_COMMANDS` in `apps/claude_agent/.env` on **each** slot (`~/agent_bench`, `~/agent_bench_test1`, `~/agent_bench_test2`). Without it the leg is rejected and every topic degrades to layer 1 only.
2. `docker compose build claude_agent && docker compose up -d claude_agent`.
3. Confirm the boot log has no `claude_agent.pipeline_commands_not_allowed`.
4. Run a Czech and an English vector; check `evaluation.json → grounding` shows `topic_parse_degraded: false` and a non-zero `whitelist_source_ratio`.

## Out of scope

* Multilingual stopword lists. Layer 1 handles orthography; vocabulary is layer 2's job, and a per-language stopword library would blur that line.
* Translating the whitelist or playbooks. Converging on English is cheaper than maintaining N translations of 610 entries.
* Enforcing English at the API boundary. Rejected: it pushes translation onto the operator and loses the original wording, which is still the best signal for local-language search.
