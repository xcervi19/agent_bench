import type { AppSettings, TopicEvent } from './types'
import { resolveBaseUrl } from './api'

export type SseStatus = 'connecting' | 'connected' | 'reconnecting' | 'disconnected' | 'error'

export interface SseClientOptions {
  settings: AppSettings
  topicId: string
  fromSeq?: number
  onEvent: (event: TopicEvent) => void
  onStatusChange: (status: SseStatus) => void
  onError?: (error: string) => void
}

export class TopicSseClient {
  private abort: AbortController | null = null
  private lastSeq: number
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null
  private running = false
  private backoff = 1000

  constructor(private options: SseClientOptions) {
    this.lastSeq = options.fromSeq ?? 0
  }

  start(): void {
    if (this.running) return
    this.running = true
    void this.connect()
  }

  stop(): void {
    this.running = false
    this.abort?.abort()
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer)
    this.options.onStatusChange('disconnected')
  }

  getLastSeq(): number {
    return this.lastSeq
  }

  private async connect(): Promise<void> {
    if (!this.running) return

    this.abort?.abort()
    this.abort = new AbortController()

    const status = this.lastSeq > 0 ? 'reconnecting' : 'connecting'
    this.options.onStatusChange(status)

    const base = resolveBaseUrl(this.options.settings)
    const url = `${base}/v1/topics/${this.options.topicId}/events?from_seq=${this.lastSeq}`

    const headers: Record<string, string> = {
      Accept: 'text/event-stream',
    }
    if (this.options.settings.apiKey) {
      headers['X-API-Key'] = this.options.settings.apiKey
    }

    try {
      const res = await fetch(url, {
        headers,
        signal: this.abort.signal,
      })

      if (!res.ok) {
        throw new Error(`SSE failed: ${res.status}`)
      }

      if (!res.body) {
        throw new Error('SSE stream unavailable')
      }

      this.options.onStatusChange('connected')
      this.backoff = 1000

      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (this.running) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const parts = buffer.split('\n\n')
        buffer = parts.pop() ?? ''

        for (const part of parts) {
          this.parseEvent(part)
        }
      }

      if (this.running) {
        this.scheduleReconnect()
      }
    } catch (e) {
      if (this.abort?.signal.aborted) return
      const msg = e instanceof Error ? e.message : 'SSE connection error'
      this.options.onError?.(msg)
      this.options.onStatusChange('error')
      if (this.running) {
        this.scheduleReconnect()
      }
    }
  }

  private parseEvent(raw: string): void {
    if (!raw.trim() || raw.startsWith(':')) return

    let eventType = 'message'
    let data = ''

    for (const line of raw.split('\n')) {
      if (line.startsWith('event:')) {
        eventType = line.slice(6).trim()
      } else if (line.startsWith('data:')) {
        data += line.slice(5).trim()
      } else if (line.startsWith('id:')) {
        // seq tracked from data payload
      }
    }

    if (!data) return

    try {
      const parsed = JSON.parse(data) as TopicEvent & { payload?: Record<string, unknown> }
      const event: TopicEvent = {
        seq: parsed.seq ?? (parsed.payload as { seq?: number })?.seq ?? this.lastSeq + 1,
        event_type: parsed.event_type ?? eventType,
        topic_id: parsed.topic_id ?? this.options.topicId,
        payload: parsed.payload ?? (parsed as unknown as Record<string, unknown>),
      }
      if (event.seq > this.lastSeq) {
        this.lastSeq = event.seq
      }
      this.options.onEvent(event)
    } catch {
      // ignore malformed events
    }
  }

  private scheduleReconnect(): void {
    this.options.onStatusChange('reconnecting')
    this.reconnectTimer = setTimeout(() => {
      void this.connect()
    }, this.backoff)
    this.backoff = Math.min(this.backoff * 1.5, 15000)
  }
}
