/**
 * Typed client for the claude_agent topic API (#17/#24).
 *
 * Every call carries the user's JWT. Artifact routes 404 until the agent has
 * written the file, so `missing` is a first-class result rather than an error:
 * the UI shows a placeholder and re-fetches when the matching event arrives.
 */

import { apiUrl, clearToken, getToken } from './session'
import type {
  CreateTopicResponse,
  DeltaArtifact,
  DeltaSummary,
  IntroArtifact,
  MonitorState,
  NewsArtifact,
  ParsedArtifact,
  ReportArtifact,
  TopicDetail,
  TopicListResponse,
} from './types'

export class ApiError extends Error {
  readonly status: number
  readonly detail: string

  constructor(status: number, detail: string) {
    super(detail || `request failed (${status})`)
    this.name = 'ApiError'
    this.status = status
    this.detail = detail
  }

  /** The session is gone or was never valid — the UI must send the user to login. */
  get isAuthError(): boolean {
    return this.status === 401
  }

  /** Owned-but-not-ready, or someone else's topic. Callers decide which. */
  get isNotFound(): boolean {
    return this.status === 404
  }
}

export function authHeaders(extra?: HeadersInit): Headers {
  const headers = new Headers(extra)
  const token = getToken()
  if (token) headers.set('Authorization', `Bearer ${token}`)
  return headers
}

async function errorFrom(res: Response): Promise<ApiError> {
  let detail = res.statusText
  try {
    const body = await res.json()
    const raw = (body as { detail?: unknown }).detail
    if (typeof raw === 'string') detail = raw
    else if (Array.isArray(raw)) {
      // FastAPI validation errors: [{loc, msg, type}, ...]
      detail = raw
        .map((item) => (item as { msg?: string }).msg)
        .filter(Boolean)
        .join('; ')
    } else if (raw) detail = JSON.stringify(raw)
  } catch {
    /* non-JSON body (proxy/HTML error page) — keep statusText */
  }
  return new ApiError(res.status, detail)
}

async function request(path: string, init: RequestInit = {}): Promise<Response> {
  const res = await fetch(apiUrl(path), {
    ...init,
    headers: authHeaders(init.headers),
  })
  if (res.ok) return res
  const error = await errorFrom(res)
  // A dead token must not linger: the next render would retry with it forever.
  if (error.isAuthError) clearToken()
  throw error
}

async function getJson<T>(path: string): Promise<T> {
  const res = await request(path, { method: 'GET' })
  return (await res.json()) as T
}

/** `null` when the artifact has not been produced yet (404). */
async function getOptionalJson<T>(path: string): Promise<T | null> {
  try {
    return await getJson<T>(path)
  } catch (err) {
    if (err instanceof ApiError && err.isNotFound) return null
    throw err
  }
}

async function getOptionalText(path: string): Promise<string | null> {
  try {
    const res = await request(path, { method: 'GET' })
    return await res.text()
  } catch (err) {
    if (err instanceof ApiError && err.isNotFound) return null
    throw err
  }
}

// ---- auth ------------------------------------------------------------------

/** fastapi-users login: form-encoded, `username` is the email. */
export async function login(email: string, password: string): Promise<string> {
  const body = new URLSearchParams({ username: email, password })
  const res = await fetch(apiUrl('/auth/jwt/login'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  })
  if (!res.ok) throw await errorFrom(res)
  const data = (await res.json()) as { access_token?: string }
  if (!data.access_token) throw new ApiError(500, 'login response had no access_token')
  return data.access_token
}

export interface RegisterInput {
  email: string
  password: string
  /** Required by agentic_core's UserCreate; the UI mints one per new account. */
  tenantId: string
}

export async function register(input: RegisterInput): Promise<void> {
  const res = await fetch(apiUrl('/auth/register'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email: input.email,
      password: input.password,
      tenant_id: input.tenantId,
    }),
  })
  if (!res.ok) throw await errorFrom(res)
}

export interface CurrentUser {
  id: string
  email: string
  is_active: boolean
  tenant_id: string
}

export function fetchCurrentUser(): Promise<CurrentUser> {
  return getJson<CurrentUser>('/users/me')
}

// ---- topics ----------------------------------------------------------------

export function listTopics(limit = 50, offset = 0): Promise<TopicListResponse> {
  return getJson<TopicListResponse>(`/v1/topics?limit=${limit}&offset=${offset}`)
}

export function getTopic(topicId: string): Promise<TopicDetail> {
  return getJson<TopicDetail>(`/v1/topics/${topicId}`)
}

export async function createTopic(topic: string): Promise<CreateTopicResponse> {
  const res = await request('/v1/topics', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ topic }),
  })
  return (await res.json()) as CreateTopicResponse
}

export async function proceedTopic(topicId: string): Promise<void> {
  await request(`/v1/topics/${topicId}/proceed`, { method: 'POST' })
}

export async function cancelTopic(topicId: string): Promise<void> {
  await request(`/v1/topics/${topicId}/cancel`, { method: 'POST' })
}

// ---- plan artifacts (16a) --------------------------------------------------

export function getIntro(topicId: string): Promise<IntroArtifact | null> {
  return getOptionalJson<IntroArtifact>(`/v1/topics/${topicId}/intro`)
}

export function getIntroMarkdown(topicId: string): Promise<string | null> {
  return getOptionalText(`/v1/topics/${topicId}/intro.md`)
}

export function getParsed(topicId: string): Promise<ParsedArtifact | null> {
  return getOptionalJson<ParsedArtifact>(`/v1/topics/${topicId}/parsed`)
}

// ---- report artifacts (16b) ------------------------------------------------

export function getReport(topicId: string): Promise<ReportArtifact | null> {
  return getOptionalJson<ReportArtifact>(`/v1/topics/${topicId}/report`)
}

export function getReportMarkdown(topicId: string): Promise<string | null> {
  return getOptionalText(`/v1/topics/${topicId}/report.md`)
}

export function getNews(topicId: string): Promise<NewsArtifact | null> {
  return getOptionalJson<NewsArtifact>(`/v1/topics/${topicId}/news`)
}

// ---- monitoring (16c) ------------------------------------------------------

export interface StartMonitorInput {
  maxAgeHours?: number
  scheduleEnabled?: boolean
  scheduleIntervalHours?: number | null
}

/** `null` when the topic has never been monitored (the API 404s that case). */
export function getMonitor(topicId: string): Promise<MonitorState | null> {
  return getOptionalJson<MonitorState>(`/v1/topics/${topicId}/monitor`)
}

/**
 * Idempotent: a second call re-activates a paused subscription and rebuilds the
 * short-term query plan. Requires the topic to be `reported` (409 otherwise).
 */
export async function startMonitor(
  topicId: string,
  input: StartMonitorInput = {},
): Promise<MonitorState> {
  const res = await request(`/v1/topics/${topicId}/monitor`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      max_age_hours: input.maxAgeHours ?? 48,
      schedule_enabled: input.scheduleEnabled ?? false,
      schedule_interval_hours: input.scheduleIntervalHours ?? null,
    }),
  })
  return (await res.json()) as MonitorState
}

/** PATCH semantics: only the fields passed here change. */
export async function updateMonitor(
  topicId: string,
  input: StartMonitorInput,
): Promise<MonitorState> {
  const body: Record<string, unknown> = {}
  if (input.maxAgeHours !== undefined) body.max_age_hours = input.maxAgeHours
  if (input.scheduleEnabled !== undefined) body.schedule_enabled = input.scheduleEnabled
  if (input.scheduleIntervalHours !== undefined) {
    body.schedule_interval_hours = input.scheduleIntervalHours
  }
  const res = await request(`/v1/topics/${topicId}/monitor`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  return (await res.json()) as MonitorState
}

export async function stopMonitor(topicId: string): Promise<void> {
  await request(`/v1/topics/${topicId}/monitor`, { method: 'DELETE' })
}

export interface RefreshAck {
  accepted: boolean
  subscription_id: number
  /** False when a cycle was already running — the API is idempotent, not an error. */
  queued: boolean
  reason?: string
  trigger?: string
}

export async function triggerRefresh(topicId: string): Promise<RefreshAck> {
  const res = await request(`/v1/topics/${topicId}/refresh`, { method: 'POST' })
  return (await res.json()) as RefreshAck
}

export async function listDeltas(topicId: string, limit = 50): Promise<DeltaSummary[]> {
  const res = await request(`/v1/topics/${topicId}/deltas?limit=${limit}`, { method: 'GET' })
  const body = (await res.json()) as { deltas?: DeltaSummary[] }
  return body.deltas ?? []
}

export function getDelta(topicId: string, seq: number): Promise<DeltaArtifact | null> {
  return getOptionalJson<DeltaArtifact>(`/v1/topics/${topicId}/deltas/${seq}`)
}

export function getDeltaNews(topicId: string, seq: number): Promise<NewsArtifact | null> {
  return getOptionalJson<NewsArtifact>(`/v1/topics/${topicId}/deltas/${seq}/news`)
}

export function getDeltaReportMarkdown(topicId: string, seq: number): Promise<string | null> {
  return getOptionalText(`/v1/topics/${topicId}/deltas/${seq}/report`)
}
