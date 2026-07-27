# Widget vocabulary — how markdown artifacts render as UI

Reference shared by `/newsfind-plan`, `/newsfind-deliver`, and `/newsfind-refresh`.
The frontend (#16b) renders any widget listed here. **You choose how your output
is presented** — the UI needs no change when you use a different widget.

## Syntax

A widget is a fenced block whose info string is `markdown-ui-widget` and whose
body is a single JSON object with a `type`:

````
```markdown-ui-widget
{"type": "entity-chips", "items": ["NIOC", "OPEC", "IEA"]}
```
````

Rules:

* The block must start at the beginning of a line, with nothing else on it.
* The body is **one JSON object**. Not an array, not several objects.
* Everything around it is normal markdown. Interleave freely.
* Widgets do not nest.

## Available types

| `type` | Payload | Use for |
|---|---|---|
| `entity-chips` | `items: string[]`, `label?` | Actors, regions, tickers — short labels |
| `highlights` | `items: string[]`, `title?` | 2–6 scannable takeaways |
| `callout` | `body`, `tone?` (`info\|good\|warn\|risk`), `title?` | One thing the reader must not miss |
| `metrics` | `items: [{label, value, hint?}]` | Small numbers side by side |
| `key-findings` | `findings: [{finding, confidence?, source_ids?}]` | Cited findings with confidence |
| `scenario-table` | `scenarios: [{id?, label?, premise?, rationale?, p_before?, p_after?, verdict?, evidence_ids?}]` | Scenario probability moves |
| `news-card` | `sourceId` | One source shown in full |
| `source-list` | `sourceIds?: string[]`, `title?` | Several sources; omit ids for all |

`news-card` / `source-list` ids must exist in the run's `news.json#sources[].id`.

## Citations

Cite inline as `[s01]` or `[s01, s03]`, referencing `news.json#sources[].id`.
The frontend turns these into links to the source. **Do not** wrap a citation in
a widget — plain `[s01]` in prose is correct and is what the reader expects.

## Rules

* Only the types above render. Anything else is shown to the operator as
  "cannot display", which is worse than plain markdown — so if none fits, write
  normal markdown.
* Never put a fact in a widget that is not also supported by the artifact's JSON.
* A widget is presentation. It never replaces the structured `*.json` file the
  orchestrator reads.

## Legacy

Older artifacts use inline tags — `<EntityChips>`, `<Highlights>`,
`<NewsCard source-id="…"/>`. The frontend still renders those so old reports keep
working. **Do not emit them in new output**; use the fenced form above.
