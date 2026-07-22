# RAG label vocabulary (controlled)

**Status:** active  
**Owner:** human (agent may only *propose*)

Labels gate retrieval. New values are **not** valid until listed here and wired into consumers.

## `document_type` (exactly one)

| Value | Meaning |
|-------|---------|
| `playbook` | Meta strategy: where to look first |
| `methodology` | PRA / assessment / specs guides |
| `education` | Books, handbooks, teaching material |
| `official_data` | Agency data docs, series docs |
| `news` | Time-sensitive news/articles |
| `reference` | Small reference sheets (e.g. oil101) |

## `use_for` (one or more)

| Value | Consumer intent |
|-------|-----------------|
| `source_discovery` | Playbook / whitelist discovery (#30/#36) |
| `pricing_context` | Benchmarks, assessment windows, grades |
| `trading_knowhow` | How markets/instruments work |
| `facts` | Stable factual reference |

## `label_assignment` (exactly one — human ack)

| Value | Meaning |
|-------|---------|
| `human` | Human set `document_type` + `use_for` at source init |
| `agent` | Human explicitly deferred; QA agent must fill labels |

Missing `label_assignment` → crawl / promote **blocked**.  
Agent must not invent production labels when assignment is `human`.

## Adding a label

1. Propose in seed or QA as `proposed_labels[]` (optional).
2. Add row to this file.
3. Add a retrieval consumer that filters on it.
4. Then use in sidecars / ingest.
