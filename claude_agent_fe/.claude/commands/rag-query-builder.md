# RAG-Informed Query Builder

Given a topic, first educate yourself from the RAG knowledge base, then generate targeted queries grounded in what the RAG actually contains.

**Topic:** $ARGUMENTS

## Steps

### Phase 1 — Discovery (learn what the RAG knows)

Run 3 broad discovery queries against the RAG to understand its vocabulary and coverage:

```bash
source .env

curl -sS -X POST "${RAG_BASE_URL}" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: ${RAG_TENANT_ID}" \
  -H "X-API-Key: ${RAG_API_KEY}" \
  -d "{\"query\":\"$ARGUMENTS overview fundamentals\",\"limit\":3}"

curl -sS -X POST "${RAG_BASE_URL}" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: ${RAG_TENANT_ID}" \
  -H "X-API-Key: ${RAG_API_KEY}" \
  -d "{\"query\":\"$ARGUMENTS mechanisms history\",\"limit\":3}"

curl -sS -X POST "${RAG_BASE_URL}" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: ${RAG_TENANT_ID}" \
  -H "X-API-Key: ${RAG_API_KEY}" \
  -d "{\"query\":\"$ARGUMENTS supply disruption response\",\"limit\":3}"
```

### Phase 2 — Analyse what you learned

From the RAG responses, extract:
- **Key concepts and terms** the RAG uses (exact vocabulary)
- **Chapters / sources** that are relevant
- **Knowledge gaps** — what the RAG did NOT return

### Phase 3 — Generate grounded queries

Produce two sets of queries:

**A) Deep-dive RAG queries** — use exact vocabulary and concepts found in Phase 1, designed to retrieve the most relevant RAG chunks:
- List 5-8 specific `/rag-search` queries the user can run

**B) Web search queries** — for knowledge gaps the RAG does not cover (current events, live prices, recent news):
- List 3-5 Google/news queries to complement the RAG

### Output format

```
## What the RAG knows about: [TOPIC]
[2-3 sentence summary of RAG coverage]

## RAG queries to run next
/rag-search [query 1]
/rag-search [query 2]
...

## Web search queries (gaps not in RAG)
[query 1]
[query 2]
...
```
