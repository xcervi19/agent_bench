docker compose build claude_agent
docker compose up -d claude_agent
docker compose logs -f claude_agent

curl -s http://79.143.179.212:8002/readyz
# expect: {"status":"ready","claude_version":"2.x.x ..."}

curl -s http://localhost:8002/v1/agent/info \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" | jq

curl -s -X POST http://79.143.179.212:8002/v1/agent/run \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $CLAUDE_AGENT_API_KEY" \
  -d '{"prompt":"Reply with exactly: HELLO_WORLD_OK","output_format":"json"}'


  The OAuth token must be inside the container: docker compose exec claude_agent env | grep CLAUDE_CODE_OAUTH_TOKEN should show it.
