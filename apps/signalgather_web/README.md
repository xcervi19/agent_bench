# SignalGather Web — Topic Intelligence UI

Trader-grade web frontend for the Newsfind topic pipeline (`claude_agent` API).

## Features

- **Topic list** — browse topics with state badges, monitoring status, and new-activity indicators
- **Create topic** — natural-language input starts the planning pipeline
- **Live activity** — SSE event stream with reconnect (`from_seq`) and collapsible tool I/O
- **Plan review** — intro markdown + query table at the human gate; Proceed / Cancel
- **Strategic report** — markdown with citation links, findings, scenarios, and ranked sources
- **Monitoring** — enable/pause, manual refresh, delta timeline with detail view
- **Settings** — API key, environment switcher (local / test1 / test2 / prod), theme

## Development

```bash
cd apps/signalgather_web
npm install
npm run dev
```

The Vite dev server proxies `/v1` to `http://localhost:8002`. Start the API:

```bash
uvicorn apps.claude_agent.app:app --host 0.0.0.0 --port 8002
```

Open **Settings** and configure your API key if `CLAUDE_AGENT_API_KEY` is set on the server.

## Build

```bash
npm run build
npm run preview   # serve dist/ on :4173
```

## Deploy (test1)

1. Build static assets: `npm run build`
2. Serve `dist/` on the VPS (e.g. Caddy `file_server` at `app.particletico.com`)
3. Point the UI at `https://agent-test1.particletico.com` in Settings (or bake in `VITE_API_BASE_URL`)

Example Caddy block:

```caddy
app.particletico.com {
    root * /path/to/signalgather_web/dist
    file_server
    try_files {path} /index.html
}
```

CORS is enabled on `claude_agent` for cross-origin API calls from the UI host.

## Manual smoke test

See `testing/ui_smoke_checklist.md`.
