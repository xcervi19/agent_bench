# Repository instructions for cloud agents

## Cursor Cloud specific instructions

- Standard setup/run commands live in `README.md` and `AGENT.md`; use those as the source of truth for the Docker Compose workflow and API smoke commands.
- The Compose stack expects local env files that are intentionally not committed. Before starting services, create `.env` from `.env.example.pro`, create `apps/claude_agent/.env` with local `CLAUDE_AGENT_API_KEY`/RAG values as needed, and ensure `/etc/claude-worker.env` exists (it can be empty) because `claude_agent` lists it in `env_file`.
- `claude_agent` mounts `./claude_home` into the container. `/readyz` can report the Claude binary version even when `claude auth status` is logged out; actual Newsfind topic runs require a valid Claude CLI session in that mounted directory.
- Without `OPENAI_API_KEY`, Signal Gather and `rag_adhoc` still run, but retrieval falls back to text/category filters. Use exact terms from seeded summaries or categories for local smoke tests.
