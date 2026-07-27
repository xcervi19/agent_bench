# /newsfind-topic-parse — Stage 0: restate the topic in English

You normalize one topic string into English facets. This runs before any search
planning, and everything downstream keys on English: the source whitelist, the
playbooks, and the query planner all speak it.

You do **no** research. No `WebSearch`, no `WebFetch`, no RAG. Answer from what
you already know about the words in front of you, write one file, and stop.
This leg is expected to finish in seconds.

`$ARGUMENTS` is a single absolute path: a directory containing `input.json`:

```json
{"topic": "<the operator's topic string, in any language>"}
```

Write exactly one file into that directory: `facets.json`.

---

## Phase 0 — read the input

```bash
PARSE_DIR="$ARGUMENTS"
cat "$PARSE_DIR/input.json"
```

---

## Phase 1 — translate and decompose

Work out these fields. Where the topic is already English, translation is a
no-op and you simply decompose it.

* **`canonical_topic_en`** — the whole topic restated as one English sentence.
  Preserve the operator's intent and scope; do not narrow it, do not add an
  angle they did not ask for. Use the standard English exonym for every place
  and organization: `Estreito de Ormuz` → `Strait of Hormuz`, `Ормузский
  пролив` → `Strait of Hormuz`, `荷姆兹海峡` → `Strait of Hormuz`.

* **`input_language`** — ISO 639-1 code of the topic as written (`cs`, `pt`,
  `ar`, `en`). If it is mixed, use the dominant language.

* **`geo`** — English names of places: straits, countries, ports, basins,
  fields, pipelines.

* **`commodity`** — English names of the goods or instruments at stake (`crude
  oil`, `LNG`, `diesel`, `freight rates`). Empty if the topic is not about one.

* **`entities`** — English or standard-Latin names of named organizations:
  companies, ministries, regulators, state operators. Include the form the
  organization itself uses in English (`NIOC`, `QatarEnergy`, `ADNOC`,
  `Ministry of Petroleum`). Expand an abbreviation only when you are confident
  of it. Do not invent members of an industry you merely assume are involved —
  name only those the topic implies.

* **`signals`** — English terms for what would count as news here: `exports`,
  `shipping disruption`, `sanctions`, `production cuts`, `storage levels`.

* **`source_languages`** — ISO 639-1 codes worth searching in, most useful
  first. Include the languages primary sources publish in for this region, and
  the operator's own language when local coverage matters. Always include `en`.
  For a Strait of Hormuz topic asked in Czech, that is `["en","ar","fa","cs"]`.

Cap each list at 12 entries. Prefer the few names that actually identify the
topic over an exhaustive list — these feed a lexical matcher, and a wrong name
pulls in a wrong source.

---

## Phase 2 — write `facets.json`

```bash
cat > "$PARSE_DIR/facets.json" <<'JSON'
{
  "schema_version": "0.1.0",
  "canonical_topic_en": "Strait of Hormuz oil and gas flows and the resulting impact on supply",
  "input_language": "cs",
  "geo": ["Strait of Hormuz", "Persian Gulf", "Iran", "Oman", "United Arab Emirates"],
  "commodity": ["crude oil", "LNG", "natural gas"],
  "entities": ["NIOC", "ADNOC", "QatarEnergy", "UKMTO", "IMO"],
  "signals": ["shipping disruption", "exports", "tanker traffic", "insurance rates"],
  "source_languages": ["en", "ar", "fa", "cs"]
}
JSON
```

Verify it parses before you finish:

```bash
jq -e . "$PARSE_DIR/facets.json" > /dev/null && echo "facets ok"
```

---

## Hard rules

* Write `facets.json` and nothing else. Do not create `parsed.json`,
  `summary.json` or any other artifact.
* Never search the web and never call RAG. If you do not recognize a name,
  leave it out of `entities` and keep it in `canonical_topic_en` as written.
* `canonical_topic_en` must always be non-empty — it is the only required
  field. An empty one makes the orchestrator discard your whole output and
  fall back to the untranslated topic.
* Every value in every list is English (or the organization's own Latin-script
  name). Never emit a term in the input language.
* The run is complete when `facets.json` exists on disk. Your final assistant
  message is ignored.
