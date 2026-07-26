I removed the old router-level _require_api_key dependency — the principal check replaces it and is strictly stronger. To be sure nothing slipped through, I introspected the built app and confirmed resolve_principal appears on all 22 topic routes.

Decisions worth knowing about:

owner_user_id is nullable, no backfill. A NULL owner means "service-owned", so pre-migration topics on test1/prod and harness-created topics remain readable by the service key and invisible to users. That avoids inventing a bootstrap user and needing an ops script.

No tenant_id column. The spec called it optional/recommended; nothing consumes it yet, so ownership is a single column. User.tenant_id still exists if you want tenant isolation later.

Service key bypass defaults to on (CLAUDE_AGENT_ALLOW_SERVICE_KEY_BYPASS). This makes the change non-breaking: test_vector_runner.sh, VPS smoke and CI keep working unchanged, and when CLAUDE_AGENT_API_KEY is empty the API stays as open as it was before. A product slot sets it to false so only JWTs are accepted. This is the one thing to flip deliberately at deploy time rather than discover later.

Two integration details that needed care. The users table lives on agentic_core's declarative base while topics lives on its own, so the foreign key is created in migration 0006 and the model declares a plain UUID column — declaring the FK in the model would force SQLAlchemy to resolve a table it can't see. And agentic_core.Settings requires Redis/S3 values that auth never reads, so bootstrap_auth_env() points DATABASE_URL at the claude_agent database and fills placeholders for the rest, following the same pattern apps/rag_adhoc/bootstrap.py already uses.

Not done, and outside what #24 asked for: CORS for the frontend origin (#16 deploy concern), and Postgres row-level security, which the spec lists as an optional follow-up since app-layer checks cover V1. I also left the spec file in docs/specs/active/ rather than moving it to done/, since you appear to be managing those moves yourself.

Before this reaches a real environment you'll need alembic upgrade head for migration 0006, and JWT_SECRET set consistently across services that issue tokens for the same users.