import type {
  AppSettings,
  DeltaDetail,
  DeltaSummary,
  MonitorStatus,
  NewsArtifact,
  QueryPlan,
  ReportArtifact,
  TopicDetail,
  TopicSummary,
} from './types'
import { API_ENVIRONMENTS } from './types'

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public detail?: string,
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

export function resolveBaseUrl(settings: AppSettings): string {
  if (settings.environment === 'custom') {
    return settings.customBaseUrl.replace(/\/$/, '')
  }
  return API_ENVIRONMENTS[settings.environment]
}

function headers(settings: AppSettings): HeadersInit {
  const h: Record<string, string> = {
    Accept: 'application/json',
  }
  if (settings.apiKey) {
    h['X-API-Key'] = settings.apiKey
  }
  return h
}

async function request<T>(
  settings: AppSettings,
  path: string,
  init?: RequestInit,
): Promise<T> {
  const base = resolveBaseUrl(settings)
  const url = `${base}${path}`
  const res = await fetch(url, {
    ...init,
    headers: {
      ...headers(settings),
      ...(init?.headers ?? {}),
    },
  })

  if (!res.ok) {
    let detail = res.statusText
    try {
      const body = await res.json()
      detail = body.detail ?? JSON.stringify(body)
    } catch {
      // ignore
    }
    throw new ApiError(`Request failed: ${path}`, res.status, String(detail))
  }

  const contentType = res.headers.get('content-type') ?? ''
  if (contentType.includes('application/json')) {
    return res.json() as Promise<T>
  }
  const text = await res.text()
  return text as unknown as T
}

export async function checkHealth(settings: AppSettings): Promise<{ status: string }> {
  return request(settings, '/readyz')
}

export async function listTopics(settings: AppSettings): Promise<{
  items: TopicSummary[]
  count: number
}> {
  return request(settings, '/v1/topics?limit=100')
}

export async function getTopic(settings: AppSettings, id: string): Promise<TopicDetail> {
  return request(settings, `/v1/topics/${id}`)
}

export async function createTopic(
  settings: AppSettings,
  topic: string,
): Promise<{ topic_id: string; state: string; events_url: string }> {
  return request(settings, '/v1/topics', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ topic }),
  })
}

export async function proceedTopic(settings: AppSettings, id: string): Promise<void> {
  await request(settings, `/v1/topics/${id}/proceed`, { method: 'POST' })
}

export async function cancelTopic(settings: AppSettings, id: string): Promise<void> {
  await request(settings, `/v1/topics/${id}/cancel`, { method: 'POST' })
}

export async function fetchParsed(settings: AppSettings, id: string): Promise<QueryPlan> {
  return request(settings, `/v1/topics/${id}/parsed`)
}

export async function fetchIntroMd(settings: AppSettings, id: string): Promise<string> {
  return request(settings, `/v1/topics/${id}/intro.md`)
}

export async function fetchNews(settings: AppSettings, id: string): Promise<NewsArtifact> {
  return request(settings, `/v1/topics/${id}/news`)
}

export async function fetchReport(settings: AppSettings, id: string): Promise<ReportArtifact> {
  return request(settings, `/v1/topics/${id}/report`)
}

export async function fetchReportMd(settings: AppSettings, id: string): Promise<string> {
  return request(settings, `/v1/topics/${id}/report.md`)
}

export async function getMonitor(settings: AppSettings, id: string): Promise<MonitorStatus | null> {
  try {
    return await request(settings, `/v1/topics/${id}/monitor`)
  } catch (e) {
    if (e instanceof ApiError && e.status === 404) return null
    throw e
  }
}

export async function startMonitor(
  settings: AppSettings,
  id: string,
  maxAgeHours = 48,
): Promise<MonitorStatus> {
  return request(settings, `/v1/topics/${id}/monitor`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ max_age_hours: maxAgeHours }),
  })
}

export async function stopMonitor(settings: AppSettings, id: string): Promise<void> {
  await request(settings, `/v1/topics/${id}/monitor`, { method: 'DELETE' })
}

export async function triggerRefresh(
  settings: AppSettings,
  id: string,
): Promise<{ accepted: boolean; queued: boolean }> {
  return request(settings, `/v1/topics/${id}/refresh`, { method: 'POST' })
}

export async function listDeltas(
  settings: AppSettings,
  id: string,
): Promise<{ deltas: DeltaSummary[]; count: number }> {
  return request(settings, `/v1/topics/${id}/deltas`)
}

export async function fetchDelta(
  settings: AppSettings,
  topicId: string,
  seq: number,
): Promise<DeltaDetail> {
  return request(settings, `/v1/topics/${topicId}/deltas/${seq}`)
}

export async function fetchDeltaNews(
  settings: AppSettings,
  topicId: string,
  seq: number,
): Promise<NewsArtifact> {
  return request(settings, `/v1/topics/${topicId}/deltas/${seq}/news`)
}

export async function fetchDeltaReport(
  settings: AppSettings,
  topicId: string,
  seq: number,
): Promise<string> {
  return request(settings, `/v1/topics/${topicId}/deltas/${seq}/report`)
}

export async function fetchArtifactSafe<T>(
  fetcher: () => Promise<T>,
): Promise<{ data: T | null; error: string | null }> {
  try {
    const data = await fetcher()
    return { data, error: null }
  } catch (e) {
    if (e instanceof ApiError && e.status === 404) {
      return { data: null, error: null }
    }
    return { data: null, error: e instanceof Error ? e.message : 'Unknown error' }
  }
}
