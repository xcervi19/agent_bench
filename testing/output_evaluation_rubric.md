# Output evaluation rubric — Trading Intelligence (#23)

Business-facing rubric for Lane A. The evaluator is a **senior trading analyst**
at a professional trading organization (energy/commodity trading firm, commodity
trading house, quant fund, asset manager, or market-intelligence desk) — **not**
a generic chatbot.

The machine-readable source of truth is `libs/eval_framework/rubric.json`. This
document is the human explanation. See the spec:
`docs/specs/active/trading_intelligence_evaluation_23.md`.

## Core philosophy

The most important capability of our system is **not text generation** — it is
**discovering, acquiring, validating, connecting, and synthesizing information
from the internet**. A system that writes an excellent report from incomplete
information must score **lower** than one that discovers superior information and
produces actionable intelligence. This is why **Information Discovery is weighted
highest (40%)**.

## Modes

- **Absolute (Mode 1):** score one report against the rubric. *"Would this be
  useful for a professional trader, analyst, PM, or risk manager?"* No comparison.
- **Relative (Mode 2):** compare a **baseline** vs a **candidate** run →
  **Better / Equal / Worse**, with win-rate aggregation across many pairs.
  *"Did the new agent version improve or degrade performance?"*

## Scale (every category)

| Score | Meaning |
|---|---|
| 0 | Absent or actively misleading |
| 1 | Poor; generic-LLM level or worse |
| 2 | Below professional bar; notable gaps |
| 3 | Adequate; usable with caveats |
| 4 | Strong; professional quality |
| 5 | Exceptional; clear information advantage |

## Layers, weights, and categories

Weights are **configurable** (`--layer-weight`, `--category-weight`, or a custom
rubric JSON). Defaults below.

### Layer 1 — Information Discovery (weight 40%)

Quality of information **acquisition**.

| Category | Question |
|---|---|
| **Primary Source Discovery** | Did it reach the *original* source (regulatory filings, company/grid/TSO/exchange/port-authority announcements, government agencies, official reports, valuable/official regional social accounts) rather than aggregators, blogs, or secondary reporting? |
| **Information Latency** | How close to the original publication event is the discovered info (e.g. original 08:00 vs Reuters 08:12 vs later media)? Closer = higher. |
| **Source Coverage** | Was the information space broad enough across official institutions, regulatory databases, industry orgs, regional media, specialist publications, academic sources, corporate comms, technical reports, official regional social? |
| **Non-Obvious Source Discovery** | Did it find sources generic search misses (terminal-operator reports, shipping-authority data, infrastructure notices, local-government disclosures, industry datasets) — not just Reuters/Bloomberg? |
| **Source Authority Assessment** | Can it distinguish information **producers** vs **consumers** vs **commentators** vs **aggregators**? |

### Layer 2 — Research Quality (weight 30%)

How well information becomes intelligence.

| Category | Question |
|---|---|
| **Entity Discovery** | Relevant entities found (companies, assets, infrastructure, commodities, countries, regulators, key individuals)? |
| **Relationship Discovery** | Relationships between entities (supply-chain, infrastructure, ownership, market, regulatory dependencies)? |
| **Causal Reasoning** | Why it happened, what caused it, likely consequences? |
| **Research Depth** | Beyond surface reporting: multiple independent sources, cross-validation, supporting evidence, historical context? |
| **Signal-to-Noise Ratio** | Focused on what matters; irrelevant detail minimized? |

### Layer 3 — Trading Intelligence (weight 30%)

Business value.

| Category | Question |
|---|---|
| **Market Relevance** | Relevant to market participants? |
| **Actionability** | Can a trader/analyst/risk manager act on it? |
| **Potential Market Impact** | Could it move prices, volatility, supply, demand, or risk? |
| **Information Edge** | Insights **not obvious** to generic LLMs or standard news workflows? *(One of the most important metrics.)* |

## Scoring & aggregation

- Each category scored **0–5**.
- **Layer score** = weighted average of its categories (equal within-layer by default).
- **Overall** = `0.40·Discovery + 0.30·Research + 0.30·Trading` (configurable),
  reported on the 0–5 scale and normalized to 0–100.
- Stored per run as `business_output/quality_review.json` (+ `quality_review.md`).

## Guardrails (hard rules for the evaluator)

- Judge **relevance and specificity, not volume**.
- **Never** equate `tool_errors == 0` or large source counts with a "good product".
- Keep **operational health** (Lane B / #15) separate from **information value**.
- Cite the specific artifact/source being judged; no unsupported claims.

## How to run

```bash
# Absolute (Mode 1)
scripts/evaluate_output.sh absolute --run-dir testing/results/test1/latest

# Relative (Mode 2)
scripts/evaluate_output.sh relative \
  --baseline testing/results/test1/<older> \
  --candidate testing/results/test1/latest

# LLM judge (Output Quality Curator persona) instead of offline heuristic
scripts/evaluate_output.sh absolute --run-dir <dir> --evaluator llm
```

## Future benchmarking

The framework scores **any** provider with this same rubric via pluggable
benchmark providers (`libs/eval_framework/benchmarks.py`): generic LLM,
internet-disabled model, standard search workflow, human analyst, Bloomberg-/
Reuters-style reports. New providers register without redesigning the evaluator.
