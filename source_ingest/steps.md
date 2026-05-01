1. From scanned PDF to clean text
Scanned PDFs are images of pages, not real text. You need OCR (and usually layout preservation).

Typical steps:

Pick an OCR path

Desktop tools: Adobe Acrobat “Recognize Text”, Abbey FineReader, macOS Preview sometimes helps — good for one-off books.
Programmatic: Tesseract, AWS Textract, Google Document AI, Azure Document Intelligence — better if you automate or have many pages.
Preserve structure where it matters

Books need chapters, sections, headings, footnotes, page breaks. Prefer pipelines that output structured layout (blocks with reading order), not a single blob per page.
Normalize the output

Fix hyphenation across line breaks (hyphen- ation → hyphenation).
Normalize Unicode and whitespace; drop repeated headers/footers if your OCR repeats them every page (optional but improves chunks).
Choose a “good format” for downstream

Markdown or HTML with headings is usually better than raw .txt if your chunker can split on # / <h2> — it mirrors book structure.
Plain text with explicit markers (e.g. ## Chapter 3) also works if you keep hierarchy consistent.
Quality pass

Spot-check random pages; OCR errors cluster on small font, tables, figures, math. For RAG, wrong numbers or garbled terms hurt more than a few typos in prose — fix or drop low-confidence regions if your stack exposes confidence.
2. Chunk design (aligned with your notes)
Your doc stresses taxonomy, optional filters, semantic signal in text, and alignment with how queries will hit the index.

Practical chunking for books:

Idea	Why
Chunk by semantic unit (section/subsection, not arbitrary 512 tokens)
Keeps one idea per retrieval unit.
Overlap between chunks
Reduces cuts mid-argument (often 10–20% overlap or ~1–2 sentences).
Respect headings
Start chunks at heading boundaries when possible so titles aren’t orphaned from body text.
Separate “noise”
Footnotes, bibliography, index — own chunks or separate collection so they don’t dominate recall.
Put “what this chunk is” into the embedded text (your file says this explicitly): e.g. a short prefix line like “Book X — Chapter 4 — Risk limits — discusses …” so embeddings capture topic, not only JSON metadata.

3. Metadata and labels (what to attach per chunk)
Match your stack: columns for high-frequency filters, flexible JSON (entities) for the rest, as in your design notes.

Useful dimensions for a book:

Source: title, author, edition, year, publisher (or source_id).
Structure: chapter_number, chapter_title, section_path (e.g. ["IV","§2","Liquidity"]).
Position: page_start, page_end (or PDF page index).
Content type: prose | table | figure_caption | footnote | appendix — helps filtering and UX.
Audience / domain: if your API uses things like category, commodity, region, map book-level themes into those where honest; otherwise keep in entities.
Labels / tags: use a small controlled vocabulary at the top level (domain, content_type, audience) so filters stay stable; put long-tail tags in entities so you avoid schema churn.

4. Ordered checklist you can follow
OCR scanned PDF → structured text (with layout/reading order).
Clean and normalize; optionally strip recurring headers/footers.
Export to Markdown/HTML or tagged text reflecting chapters/sections.
Define chunk boundaries (section-aware + overlap + special handling for tables/notes).
For each chunk, build metadata + short textual lead-in for embedding.
Embed; index with optional metadata filters plus vector search (as your design describes).
Evaluate: sample queries that should hit specific chapters; tune chunk size and overlap.
5. Reality check
Scanned + figures-heavy: expect OCR limits; RAG will be only as good as the text layer.
Copyright: ensure you have rights to process and store the book in your system.
If you want this wired to your repo’s exact schemas (events row, entities, API filters), say what format your ingest expects (JSON schema, DB columns) and we can map fields one-to-one — still in Ask mode I can only specify the mapping, not implement it unless you switch to Agent mode.