#!/usr/bin/env bash
# Source this once before launching Claude Code:
#   source export-env.sh
# Or add to ~/.zshrc:
#   source /Users/karel.cervicek/Documents/rag_test/export-env.sh

set -a   # auto-export every variable defined below
# shellcheck source=.env
source "$(dirname "${BASH_SOURCE[0]}")/.env"
set +a

echo "RAG env vars exported: RAG_BASE_URL, RAG_TENANT_ID, RAG_API_KEY"
