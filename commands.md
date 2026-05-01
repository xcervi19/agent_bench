ssh -i ~/.ssh/contabo_ed25519 root@79.143.179.212

scp -i ~/.ssh/contabo_ed25519 .env.examplesmall root@79.143.179.212:~/agent_bench/.env

ssh -i ~/.ssh/contabo_ed25519 -L 5433:127.0.0.1:5432 root@79.143.179.212

docker compose run --rm --no-deps --entrypoint alembic api upgrade head

curl -sS -X POST "http://79.143.179.212:8001/v1/search" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: 00000000-0000-0000-0000-000000000001" \
  -H "X-API-Key: kjdjuhf6s8i783hd8j47" \
  -d '{"query":"test","limit":5}'