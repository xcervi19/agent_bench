/**
 * Where the UI points and who it says it is.
 *
 * All three values live in localStorage so a reload keeps you signed in and
 * pointed at the same slot. The access token is a JWT (bearer transport), which
 * is why it can be read by JS at all — there is no cookie to fall back on.
 *
 * The access token expires within the hour; the refresh token is what turns
 * that into a session you do not have to re-enter a password for. It is a
 * server-side row, so signing out actually ends it rather than just forgetting
 * it here.
 */

const TOKEN_KEY = 'signalgather.token'
const REFRESH_KEY = 'signalgather.refreshToken'
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

export function getRefreshToken(): string | null {
  return localStorage.getItem(REFRESH_KEY)
}

export function setRefreshToken(token: string): void {
  localStorage.setItem(REFRESH_KEY, token)
}

/**
 * Forget the whole session. Used where the user is genuinely signed out — the
 * refresh token failed, or they asked to leave — never for a single 401 that a
 * renewal could still answer.
 */
export function clearSession(): void {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(REFRESH_KEY)
}

/** Absolute URL for an API path, honouring the selected slot. */
/**
 * Where a *shared* page reads from: the host in the link, always.
 *
 * The slot picker is an operator convenience stored in `localStorage`, and it
 * has no business deciding what a shared link resolves against. A colleague who
 * once pointed this browser at another slot would otherwise open an
 * `agent-test1` link and watch it query `agent-test2` — the topic is not there,
 * so the page sits on its skeleton and the link looks broken. Observed exactly
 * that way on 2026-09-09, on the first shared India link.
 *
 * Same origin is not a fallback here, it is the rule: the public API is mounted
 * on the same server that served the page, in every deployment and behind the
 * dev proxy alike.
 */
export function publicUrl(path: string, params?: Record<string, string | number | undefined>): string {
  return buildUrl('', path, params)
}

export function apiUrl(path: string, params?: Record<string, string | number | undefined>): string {
  return buildUrl(getApiBase(), path, params)
}

function buildUrl(
  base: string,
  path: string,
  params?: Record<string, string | number | undefined>,
): string {
  const query = new URLSearchParams()
  for (const [key, value] of Object.entries(params ?? {})) {
    if (value !== undefined) query.set(key, String(value))
  }
  const suffix = query.size > 0 ? `?${query}` : ''
  return `${base}${path}${suffix}`
}
