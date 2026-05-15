SET app.tenant_id = '00000000-0000-0000-0000-000000000001';

SELECT id, source, title, language, created_at
FROM documents
WHERE id = 'f41db256-4d3f-460b-9bfe-57d9ff838c95';

SELECT COUNT(*) FROM events WHERE document_id = 'f41db256-4d3f-460b-9bfe-57d9ff838c95';
SELECT id, category, commodity, region, occurred_at, left(summary, 120) AS summary_preview
FROM events

WHERE document_id = 'f41db256-4d3f-460b-9bfe-57d9ff838c95'
ORDER BY occurred_at NULLS LAST
LIMIT 10;