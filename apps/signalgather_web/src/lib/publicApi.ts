/**
 * Client for shared topics (#40) — the read-only half of the product.
 *
 * Deliberately a separate module from `api.ts`, mirroring the separate router on
 * the server:
 *
 *   - it never sends the user's token, so a shared page behaves identically for
 *     a signed-in reader and a stranger, and a stale token cannot make one of
 *     them see something the other does not;
 *   - every function here is a GET. Nothing in this file can start a run,
 *     trigger a refresh, or otherwise spend money — the server would refuse, but
 *     the client should not know how to ask.
 *
 * A 401 is not treated as "session expired" either: there is no session to
 * expire, so `clearToken()` is never called from this path.
 */

import { ApiError, errorFrom } from './api'
import { apiUrl } from './session'
import type {
  DeltaArtifact,
  DeltaSummary,
  IntroArtifact,
  NewsArtifact,
  ParsedArtifact,
  PublicTopic,
  PublicTopicListResponse,
  ReportArtifact,
} from './types'

const BASE = '/v1/public/topics'

async function get(path: string): Promise<Response> {
  const res = await fetch(apiUrl(path), { method: 'GET' })
  if (res.ok) return res
  throw await errorFrom(res)
}

async function getJson<T>(path: string): Promise<T> {
  return (await (await get(path)).json()) as T
}

/** `null` when the artifact was never produced (404) — same contract as api.ts. */
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
    return await (await get(path)).text()
  } catch (err) {
    if (err instanceof ApiError && err.isNotFound) return null
    throw err
  }
}

// ---- discovery -------------------------------------------------------------

export function listPublicTopics(
  query = '',
  limit = 50,
  offset = 0,
): Promise<PublicTopicListResponse> {
  const params = new URLSearchParams({ limit: String(limit), offset: String(offset) })
  if (query.trim()) params.set('q', query.trim())
  return getJson<PublicTopicListResponse>(`${BASE}?${params}`)
}

export function getPublicTopic(topicId: string): Promise<PublicTopic> {
  return getJson<PublicTopic>(`${BASE}/${topicId}`)
}

// ---- artifacts -------------------------------------------------------------

export function getPublicIntro(topicId: string): Promise<IntroArtifact | null> {
  return getOptionalJson<IntroArtifact>(`${BASE}/${topicId}/intro`)
}

export function getPublicIntroMarkdown(topicId: string): Promise<string | null> {
  return getOptionalText(`${BASE}/${topicId}/intro.md`)
}

export function getPublicParsed(topicId: string): Promise<ParsedArtifact | null> {
  return getOptionalJson<ParsedArtifact>(`${BASE}/${topicId}/parsed`)
}

export function getPublicReport(topicId: string): Promise<ReportArtifact | null> {
  return getOptionalJson<ReportArtifact>(`${BASE}/${topicId}/report`)
}

export function getPublicReportMarkdown(topicId: string): Promise<string | null> {
  return getOptionalText(`${BASE}/${topicId}/report.md`)
}

export function getPublicNews(topicId: string): Promise<NewsArtifact | null> {
  return getOptionalJson<NewsArtifact>(`${BASE}/${topicId}/news`)
}

// ---- refresh history -------------------------------------------------------

export async function listPublicDeltas(topicId: string, limit = 50): Promise<DeltaSummary[]> {
  const body = await getJson<{ deltas?: DeltaSummary[] }>(`${BASE}/${topicId}/deltas?limit=${limit}`)
  return body.deltas ?? []
}

export function getPublicDelta(topicId: string, seq: number): Promise<DeltaArtifact | null> {
  return getOptionalJson<DeltaArtifact>(`${BASE}/${topicId}/deltas/${seq}`)
}

export function getPublicDeltaNews(topicId: string, seq: number): Promise<NewsArtifact | null> {
  return getOptionalJson<NewsArtifact>(`${BASE}/${topicId}/deltas/${seq}/news`)
}

export function getPublicDeltaReportMarkdown(
  topicId: string,
  seq: number,
): Promise<string | null> {
  return getOptionalText(`${BASE}/${topicId}/deltas/${seq}/report`)
}

/**
 * The link an owner hands out. Absolute, so it survives a paste into chat.
 *
 * The SPA lives at `/app` in the bundled deployment and at `/` under `vite dev`,
 * so the base comes from wherever this page is actually running rather than from
 * an assumption that would produce a dead link in one of the two.
 */
export function shareUrl(topicId: string): string {
  const base = window.location.pathname.startsWith('/app') ? '/app' : ''
  return new URL(`${base}/shared/${topicId}`, window.location.origin).toString()
}
