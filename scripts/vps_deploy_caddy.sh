#!/usr/bin/env bash
# Install/update host Caddy on the Contabo VPS and reload config from the repo.
set -euo pipefail

SSH_KEY="${SSH_KEY:-$HOME/.ssh/contabo_ed25519}"
VPS_HOST="${VPS_HOST:-root@79.143.179.212}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

scp -i "$SSH_KEY" "$REPO_ROOT/infra/caddy/Caddyfile" "$VPS_HOST:/etc/caddy/Caddyfile"

ssh -i "$SSH_KEY" "$VPS_HOST" bash -s <<'REMOTE'
set -euo pipefail
if ! command -v caddy >/dev/null 2>&1; then
  apt-get update -qq
  apt-get install -y debian-keyring debian-archive-keyring apt-transport-https curl
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' \
    | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' \
    | tee /etc/apt/sources.list.d/caddy-stable.list
  apt-get update -qq
  apt-get install -y caddy
fi
caddy validate --config /etc/caddy/Caddyfile
systemctl enable caddy
systemctl reload caddy || systemctl restart caddy
systemctl --no-pager status caddy
REMOTE

echo "Caddy deployed. Test: curl -sI https://app.particletico.com"
