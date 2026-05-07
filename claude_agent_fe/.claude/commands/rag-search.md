# RAG Knowledge Base Search

Search the internal trading knowledge base and return summarised results.

**Query:** $ARGUMENTS

## Steps
1. Read `.env` from the project root and extract `RAG_BASE_URL`, `RAG_TENANT_ID`, `RAG_API_KEY`.
2. Run the search:

```bash
source .env
curl -sS -X POST "${RAG_BASE_URL}" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: ${RAG_TENANT_ID}" \
  -H "X-API-Key: ${RAG_API_KEY}" \
  -d '{"query":"$ARGUMENTS","limit":3}'
```

3. Parse the response:
   - Main content lives in `results[].summary`
   - Cite `results[].source` when present
4. Return a concise trader-style summary of the findings.

## API contract reference
| Field      | Type   | Notes                                      |
|------------|--------|--------------------------------------------|
| query      | string | Required — natural-language question       |
| commodity  | string | Optional — `crude_oil` or `natural_gas`    |
| region     | string | Optional — `europe`, `north_america`, etc. |
| limit      | int    | Optional — default 3                       |

Response: `{ "results": [ { "summary": "...", "source": "..." } ] }`
