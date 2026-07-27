/**
 * Where the UI points and who it says it is.
 *
 * Both values live in localStorage so a reload keeps you signed in and pointed
 * at the same slot. The token is a fastapi-users JWT (bearer transport), which
 * is why it can be read by JS at all — there is no cookie to fall back on.
 */

const TOKEN_KEY = 'signalgather.token'
const BASE_KEY = 'signalgather.apiBase'

export interface ApiEnv {
  id: string
  label: string
  /** Empty string = same origin as the page (the bundled /app mount). */
  baseUrl: string
}

/** Slots from docs/product/README.md, plus whatever origin served this page. */
export const API_ENVS: ApiEnv[] = [
  { id: 'same-origin', label: 'This host (bundled UI)', baseUrl: '' },
  { id: 'local', label: 'Local (localhost:8002)', baseUrl: 'http://localhost:8002' },
  { id: 'test1', label: 'test1', baseUrl: 'https://agent-test1.particletico.com' },
  { id: 'test2', label: 'test2', baseUrl: 'https://agent-test2.particletico.com' },
  { id: 'prod', label: 'prod', baseUrl: 'https://agent.particletico.com' },
]

/**
 * Dev runs behind the Vite proxy (same origin), so the default is '' there too.
 * A build-time override is available for one-off bundles.
 */
const DEFAULT_BASE = (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? ''

function normalizeBase(raw: string): string {
  return raw.trim().replace(/\/+$/, '')
}

export function getApiBase(): string {
  const stored = localStorage.getItem(BASE_KEY)
  return stored === null ? DEFAULT_BASE : normalizeBase(stored)
}

export function setApiBase(baseUrl: string): void {
  localStorage.setItem(BASE_KEY, normalizeBase(baseUrl))
}

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token)
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY)
}

/** Absolute URL for an API path, honouring the selected slot. */
export function apiUrl(path: string, params?: Record<string, string | number | undefined>): string {
  const base = getApiBase()
  const query = new URLSearchParams()
  for (const [key, value] of Object.entries(params ?? {})) {
    if (value !== undefined) query.set(key, String(value))
  }
  const suffix = query.size > 0 ? `?${query}` : ''
  return `${base}${path}${suffix}`
}
