Why metadata matters for your case
Scope control — Vector search alone can return plausible-sounding but wrong-domain chunks (e.g. “shipping” in finance vs maritime). Metadata narrows the candidate set before or alongside similarity.

Governance & UX — You can tag audience, asset class, jurisdiction, data freshness, risk level, source type (research vs news vs edu), so downstream logic and humans know what the chunk is for.

Operational routing — A coarse tag like domain / collection / vertical lets you later split indexes, filters, or even different retrieval strategies without re-embedding everything.

How this fits your stack
Your events row already has:

Structured filters: category, commodity, region (good for fast SQL filters alongside vector search — your API already accepts some of these).
Flexible payload: entities JSON — this is where rich, evolving metadata belongs without schema churn.
So the usual pattern is:

Use columns for fields you filter on often and want stable indexing (you might map “domain” → category, market theme → commodity, geography → region, or introduce new columns later if needed).
Use entities for everything else: pedagogical level, topic taxonomy, source URL, instrument identifiers, chapter/section, embedding_model, chunking params, confidence, etc.
Design habits that work well at “sophisticated” scale
Stable taxonomy — Define a small set of top-level dimensions (e.g. domain, subdomain, content_type, audience, geo, time_horizon) with controlled vocabularies where possible. Free-form tags alone drift.

Don’t over-fragment recall — Too many mandatory filters → empty results. Prefer optional filters + clear defaults; use metadata for ranking/explanation when filtering isn’t needed.

Align metadata with the query path — Whatever you store, plan how the agent or API will pass filters (commodity, region, etc.) vs rely on pure semantic search.

Keep “what this chunk is about” in text too — Put a short human-readable label or lead sentence in summary or first line of chunk text so embeddings capture semantic type, not only JSON metadata.