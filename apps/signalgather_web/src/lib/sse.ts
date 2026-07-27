/**
 * Server-sent events from `GET /v1/topics/{id}/events`.
 *
 * `EventSource` cannot set an Authorization header and the topic stream is
 * owner-scoped (#24), so this is a fetch + ReadableStream reader instead.
 *
 * Resilience contract from the spec:
 *   - resume with `from_seq` = highest seq seen, so a drop replays nothing twice
 *     and skips nothing;
 *   - a `: done` comment means the server closed on purpose (terminal state) —
 *     do not reconnect;
 *   - anything else that ends the body is a drop — reconnect with backoff.
 */

import { authHeaders } from './api'
import { apiUrl } from './session'
import type { TopicEvent } from './types'

export type StreamStatus = 'connecting' | 'open' | 'reconnecting' | 'done' | 'error'

/** One `id:/event:/data:` block, or the server's end-of-stream comment. */
export interface SseFrame {
  id?: string
  event?: string
  data: string
  /** True for the `: done` comment the topic stream sends before closing. */
  done: boolean
}

/**
 * Incremental parser: `push` accepts arbitrary chunk boundaries and returns the
 * frames that completed. Split across the wire is normal, so state carries over.
 */
export class SseParser {
  private buffer = ''

  push(chunk: string): SseFrame[] {
    this.buffer += chunk.replace(/\r\n/g, '\n')
    const frames: SseFrame[] = []
    let boundary = this.buffer.indexOf('\n\n')
    while (boundary !== -1) {
      const block = this.buffer.slice(0, boundary)
      this.buffer = this.buffer.slice(boundary + 2)
      const frame = parseBlock(block)
      if (frame) frames.push(frame)
      boundary = this.buffer.indexOf('\n\n')
    }
    return frames
  }
}

function parseBlock(block: string): SseFrame | null {
  const frame: SseFrame = { data: '', done: false }
  const dataLines: string[] = []
  let sawField = false

  for (const line of block.split('\n')) {
    if (line === '') continue
    if (line.startsWith(':')) {
      // Comment. The topic stream uses `: done` as its close marker.
      if (line.slice(1).trim() === 'done') frame.done = true
      continue
    }
    const colon = line.indexOf(':')
    const field = colon === -1 ? line : line.slice(0, colon)
    const value = colon === -1 ? '' : line.slice(colon + 1).replace(/^ /, '')
    sawField = true
    if (field === 'id') frame.id = value
    else if (field === 'event') frame.event = value
    else if (field === 'data') dataLines.push(value)
  }

  frame.data = dataLines.join('\n')
  if (!sawField && !frame.done) return null
  return frame
}

/** Decode a frame's JSON payload into a TopicEvent, or null if it isn't one. */
export function frameToEvent(frame: SseFrame): TopicEvent | null {
  if (!frame.data) return null
  let parsed: unknown
  try {
    parsed = JSON.parse(frame.data)
  } catch {
    return null
  }
  if (typeof parsed !== 'object' || parsed === null) return null
  const candidate = parsed as Partial<TopicEvent>
  if (typeof candidate.seq !== 'number' || typeof candidate.event_type !== 'string') return null
  return {
    seq: candidate.seq,
    event_type: candidate.event_type,
    topic_id: String(candidate.topic_id ?? ''),
    payload: (candidate.payload ?? {}) as Record<string, unknown>,
  }
}

export interface StreamOptions {
  topicId: string
  /** Replay starts *after* this seq. Pass the topic's last_event_seq to skip history. */
  fromSeq?: number
  onEvent: (event: TopicEvent) => void
  onStatus?: (status: StreamStatus, detail?: string) => void
  signal: AbortSignal
  /** Injectable for tests. */
  fetchImpl?: typeof fetch
  sleepImpl?: (ms: number) => Promise<void>
  maxRetries?: number
}

const BACKOFF_MS = [500, 1000, 2000, 5000, 10000] as const

export function backoffFor(attempt: number): number {
  return BACKOFF_MS[Math.min(attempt, BACKOFF_MS.length - 1)] ?? 10000
}

const defaultSleep = (ms: number) => new Promise<void>((resolve) => setTimeout(resolve, ms))

/**
 * Stream until the server says `done`, the caller aborts, or retries run out.
 * Resolves with the highest seq delivered so callers can reconcile after.
 */
export async function streamTopicEvents(options: StreamOptions): Promise<number> {
  const {
    topicId,
    onEvent,
    onStatus,
    signal,
    fetchImpl = fetch,
    sleepImpl = defaultSleep,
    maxRetries = Number.POSITIVE_INFINITY,
  } = options

  let lastSeq = options.fromSeq ?? 0
  let attempt = 0

  while (!signal.aborted) {
    onStatus?.(attempt === 0 ? 'connecting' : 'reconnecting')
    try {
      const res = await fetchImpl(
        apiUrl(`/v1/topics/${topicId}/events`, { from_seq: lastSeq }),
        {
          method: 'GET',
          headers: authHeaders({ Accept: 'text/event-stream' }),
          signal,
          // Long-lived response; never let the browser serve a cached body.
          cache: 'no-store',
        },
      )

      if (res.status === 401 || res.status === 404) {
        onStatus?.('error', res.status === 401 ? 'session expired' : 'topic not found')
        return lastSeq
      }
      if (!res.ok || !res.body) {
        throw new Error(`event stream failed (${res.status})`)
      }

      onStatus?.('open')
      attempt = 0

      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      const parser = new SseParser()
      let closedByServer = false

      while (!signal.aborted) {
        const { done, value } = await reader.read()
        if (done) break
        for (const frame of parser.push(decoder.decode(value, { stream: true }))) {
          if (frame.done) {
            closedByServer = true
            continue
          }
          const event = frameToEvent(frame)
          if (!event || event.seq <= lastSeq) continue
          lastSeq = event.seq
          onEvent(event)
        }
        if (closedByServer) break
      }

      await reader.cancel().catch(() => {})

      if (closedByServer) {
        onStatus?.('done')
        return lastSeq
      }
      if (signal.aborted) return lastSeq
      // Body ended without `: done` — treat as a drop and resume from lastSeq.
    } catch (err) {
      if (signal.aborted) return lastSeq
      onStatus?.('reconnecting', err instanceof Error ? err.message : String(err))
    }

    if (attempt >= maxRetries) {
      onStatus?.('error', 'lost connection to the event stream')
      return lastSeq
    }
    await sleepImpl(backoffFor(attempt))
    attempt += 1
  }

  return lastSeq
}
