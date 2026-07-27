import { describe, expect, it, vi } from 'vitest'
import { SseParser, backoffFor, frameToEvent, streamTopicEvents } from './sse'
import { setApiBase, setToken } from './session'
import type { TopicEvent } from './types'

function frame(seq: number, type: string, payload: Record<string, unknown> = {}): string {
  const data = JSON.stringify({ seq, event_type: type, topic_id: 't1', payload })
  return `id: ${seq}\nevent: ${type}\ndata: ${data}\n\n`
}

/** A Response whose body streams the given chunks, then ends. */
function streamResponse(chunks: string[], status = 200): Response {
  const encoder = new TextEncoder()
  const body = new ReadableStream<Uint8Array>({
    start(controller) {
      for (const chunk of chunks) controller.enqueue(encoder.encode(chunk))
      controller.close()
    },
  })
  return new Response(body, { status, headers: { 'Content-Type': 'text/event-stream' } })
}

describe('SseParser', () => {
  it('parses a complete frame', () => {
    const frames = new SseParser().push(frame(1, 'topic.created'))
    expect(frames).toHaveLength(1)
    expect(frames[0]!.id).toBe('1')
    expect(frames[0]!.event).toBe('topic.created')
    expect(frames[0]!.done).toBe(false)
  })

  it('holds a partial frame until the rest arrives', () => {
    const parser = new SseParser()
    const raw = frame(7, 'stage.started', { stage: 'plan' })
    const cut = Math.floor(raw.length / 2)

    expect(parser.push(raw.slice(0, cut))).toHaveLength(0)
    const frames = parser.push(raw.slice(cut))
    expect(frames).toHaveLength(1)
    expect(frameToEvent(frames[0]!)?.seq).toBe(7)
  })

  it('splits several frames delivered in one chunk', () => {
    const frames = new SseParser().push(frame(1, 'a') + frame(2, 'b') + frame(3, 'c'))
    expect(frames.map((f) => f.id)).toEqual(['1', '2', '3'])
  })

  it('recognises the servers `: done` close marker', () => {
    const frames = new SseParser().push(': done\n\n')
    expect(frames).toHaveLength(1)
    expect(frames[0]!.done).toBe(true)
  })

  it('tolerates CRLF line endings', () => {
    const frames = new SseParser().push('id: 4\r\nevent: ping\r\ndata: {}\r\n\r\n')
    expect(frames[0]!.event).toBe('ping')
  })

  it('joins multi-line data fields', () => {
    const frames = new SseParser().push('data: {"seq":1,\ndata: "event_type":"x","payload":{}}\n\n')
    expect(frameToEvent(frames[0]!)?.event_type).toBe('x')
  })
})

describe('frameToEvent', () => {
  it('rejects malformed JSON instead of throwing', () => {
    expect(frameToEvent({ data: '{not json', done: false })).toBeNull()
  })

  it('rejects payloads missing the wire contract', () => {
    expect(frameToEvent({ data: '{"hello":1}', done: false })).toBeNull()
  })

  it('defaults a missing payload to an empty object', () => {
    const event = frameToEvent({ data: '{"seq":2,"event_type":"error"}', done: false })
    expect(event?.payload).toEqual({})
  })
})

describe('backoffFor', () => {
  it('grows then plateaus', () => {
    expect(backoffFor(0)).toBe(500)
    expect(backoffFor(2)).toBe(2000)
    expect(backoffFor(99)).toBe(10000)
  })
})

describe('streamTopicEvents', () => {
  const collect = () => {
    const events: TopicEvent[] = []
    return { events, onEvent: (e: TopicEvent) => events.push(e) }
  }

  it('delivers events and stops on the servers done marker', async () => {
    const { events, onEvent } = collect()
    const fetchImpl = vi.fn(async () =>
      streamResponse([frame(1, 'topic.created'), frame(2, 'intro.ready'), ': done\n\n']),
    )
    const statuses: string[] = []

    const last = await streamTopicEvents({
      topicId: 't1',
      onEvent,
      onStatus: (s) => statuses.push(s),
      signal: new AbortController().signal,
      fetchImpl: fetchImpl as unknown as typeof fetch,
    })

    expect(events.map((e) => e.seq)).toEqual([1, 2])
    expect(last).toBe(2)
    expect(statuses).toContain('open')
    expect(statuses.at(-1)).toBe('done')
    expect(fetchImpl).toHaveBeenCalledTimes(1)
  })

  it('resumes from the highest seq seen after a drop', async () => {
    const urls: string[] = []
    const fetchImpl = vi.fn(async (url: string) => {
      urls.push(url)
      // First body ends without `: done` — a network drop, not a clean close.
      return urls.length === 1
        ? streamResponse([frame(1, 'a'), frame(2, 'b')])
        : streamResponse([frame(3, 'c'), ': done\n\n'])
    })
    const { events, onEvent } = collect()

    await streamTopicEvents({
      topicId: 't1',
      onEvent,
      signal: new AbortController().signal,
      fetchImpl: fetchImpl as unknown as typeof fetch,
      sleepImpl: async () => {},
    })

    expect(events.map((e) => e.seq)).toEqual([1, 2, 3])
    expect(urls[0]).toContain('from_seq=0')
    expect(urls[1]).toContain('from_seq=2')
  })

  it('never re-delivers a seq the caller already saw', async () => {
    const fetchImpl = vi.fn(async () =>
      streamResponse([frame(1, 'a'), frame(1, 'a'), frame(2, 'b'), ': done\n\n']),
    )
    const { events, onEvent } = collect()

    await streamTopicEvents({
      topicId: 't1',
      onEvent,
      signal: new AbortController().signal,
      fetchImpl: fetchImpl as unknown as typeof fetch,
    })

    expect(events.map((e) => e.seq)).toEqual([1, 2])
  })

  it('starts after fromSeq when the caller already has history', async () => {
    const urls: string[] = []
    const fetchImpl = vi.fn(async (url: string) => {
      urls.push(url)
      return streamResponse([': done\n\n'])
    })

    await streamTopicEvents({
      topicId: 't1',
      fromSeq: 12,
      onEvent: () => {},
      signal: new AbortController().signal,
      fetchImpl: fetchImpl as unknown as typeof fetch,
    })

    expect(urls[0]).toContain('from_seq=12')
  })

  it('gives up without retrying when the topic is not ours (404)', async () => {
    const fetchImpl = vi.fn(async () => new Response('{}', { status: 404 }))
    const statuses: [string, string | undefined][] = []

    await streamTopicEvents({
      topicId: 't1',
      onEvent: () => {},
      onStatus: (s, d) => statuses.push([s, d]),
      signal: new AbortController().signal,
      fetchImpl: fetchImpl as unknown as typeof fetch,
    })

    expect(fetchImpl).toHaveBeenCalledTimes(1)
    expect(statuses.at(-1)).toEqual(['error', 'topic not found'])
  })

  it('gives up without retrying when the session expired (401)', async () => {
    const fetchImpl = vi.fn(async () => new Response('{}', { status: 401 }))
    const statuses: string[] = []

    await streamTopicEvents({
      topicId: 't1',
      onEvent: () => {},
      onStatus: (s) => statuses.push(s),
      signal: new AbortController().signal,
      fetchImpl: fetchImpl as unknown as typeof fetch,
    })

    expect(fetchImpl).toHaveBeenCalledTimes(1)
    expect(statuses.at(-1)).toBe('error')
  })

  it('stops after maxRetries when the transport keeps failing', async () => {
    const fetchImpl = vi.fn(async () => {
      throw new TypeError('network down')
    })
    const statuses: [string, string | undefined][] = []

    await streamTopicEvents({
      topicId: 't1',
      onEvent: () => {},
      onStatus: (s, d) => statuses.push([s, d]),
      signal: new AbortController().signal,
      fetchImpl: fetchImpl as unknown as typeof fetch,
      sleepImpl: async () => {},
      maxRetries: 2,
    })

    expect(fetchImpl).toHaveBeenCalledTimes(3)
    expect(statuses.at(-1)?.[0]).toBe('error')
  })

  it('stops immediately once the caller aborts', async () => {
    const controller = new AbortController()
    controller.abort()
    const fetchImpl = vi.fn(async () => streamResponse([': done\n\n']))

    await streamTopicEvents({
      topicId: 't1',
      onEvent: () => {},
      signal: controller.signal,
      fetchImpl: fetchImpl as unknown as typeof fetch,
    })

    expect(fetchImpl).not.toHaveBeenCalled()
  })

  it('sends the bearer token and targets the selected slot', async () => {
    setToken('jwt-123')
    setApiBase('https://agent-test1.particletico.com/')
    let seenUrl = ''
    let seenAuth: string | null = null
    const fetchImpl = vi.fn(async (url: string, init: RequestInit) => {
      seenUrl = url
      seenAuth = new Headers(init.headers).get('Authorization')
      return streamResponse([': done\n\n'])
    })

    await streamTopicEvents({
      topicId: 'abc',
      onEvent: () => {},
      signal: new AbortController().signal,
      fetchImpl: fetchImpl as unknown as typeof fetch,
    })

    expect(seenUrl).toBe(
      'https://agent-test1.particletico.com/v1/topics/abc/events?from_seq=0',
    )
    expect(seenAuth).toBe('Bearer jwt-123')
  })
})
