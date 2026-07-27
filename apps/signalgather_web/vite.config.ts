import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// The app is served from /app on claude_agent (see `_mount_web` in
// apps/claude_agent/app.py), so asset URLs must be built against that base.
// `vite dev` keeps the same base and proxies /v1 + /auth + /users to the API,
// which makes dev same-origin too — no CORS needed for the default setup.
const API_TARGET = process.env.SIGNALGATHER_API_URL ?? 'http://localhost:8002'
const PROXIED = ['/v1', '/auth', '/users', '/healthz', '/readyz']

export default defineConfig({
  base: '/app/',
  plugins: [react(), tailwindcss()],
  server: {
    port: 5173,
    proxy: Object.fromEntries(
      PROXIED.map((path) => [
        path,
        // SSE must not be buffered by the dev proxy.
        { target: API_TARGET, changeOrigin: true, ws: false },
      ]),
    ),
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.ts'],
    include: ['src/**/*.test.{ts,tsx}'],
  },
})
