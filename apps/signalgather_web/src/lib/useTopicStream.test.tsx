import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, renderHook, waitFor } from '@testing-library/react'
import type { StreamOptions } from './sse'
import type { TopicDetail } from './types'

/**
 * Guards the spec's "event-driven, not poll-heavy" rule: artifacts are fetched
 * because an event said they exist, never on a timer — and each group is
 * fetched once per burst of events, not once per event.
 */

const getTopic = vi.fn<(id: string) => Promise<TopicDetail>>()
const getIntro = vi.fn(async () => ({ headline: 'Strait closure' }))
const getIntroMarkdown = vi.fn(async () => '# Brief')
const getParsed = vi.fn(async () => ({ queries: [{ id: 'q01', query: 'x' }] }))
const getReport = vi.fn(async () => ({ thesis_status: 'supported' }))
const getReportMarkdown = vi.fn(async () => '## Snapshot')
const getNews = vi.fn(async () => ({ sources: [{ id: 's01' }] }))
const getMonitor = vi.fn(async () => ({ status: 'active', max_age_hours: 48 }))
const listDeltas = vi.fn(async () => [{ seq: 1, run_id: 'r1' }])

let emit: (options: StreamOptions) => Promise<void> = async () => {}

vi.mock('./api', () => ({
  ApiError: class extends Error {
    isNotFound = false
    isAuthError = false
    detail = ''
  },
  getTopic: (id: string) => getTopic(id),
  getIntro: () => getIntro(),
  getIntroMarkdown: () => getIntroMarkdown(),
  getParsed: () => getParsed(),
  getReport: () => getReport(),
  getReportMarkdown: () => getReportMarkdown(),
  getNews: () => getNews(),
  getMonitor: () => getMonitor(),
  listDeltas: () => listDeltas(),
}))

vi.mock('./sse', () => ({
  streamTopicEvents: async (options: StreamOptions) => {
    await emit(options)
    return 0
  },
}))

const { useTopicStream } = await import('./useTopicStream')

function topic(overrides: Partial<TopicDetail> = {}): TopicDetail {
  return {
    id: 't1',
    topic: 'Hormuz',
    state: 'planning',
    available_actions: ['cancel'],
    last_event_seq: 0,
    created_at: '2026-07-26T10:00:00+00:00',
    updated_at: '2026-07-26T10:00:00+00:00',
    plan_run_id: null,
    deliver_run_id: null,
    error: null,
    ...overrides,
  }
}

const event = (type: string, seq = 1) => ({
  seq,
  event_type: type,
  topic_id: 't1',
  payload: {},
})

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
  emit = async () => {}
})

describe('useTopicStream — no polling', () => {
  it('does not touch artifact routes before any run exists', async () => {
    getTopic.mockResolvedValue(topic())
    const { result } = renderHook(() => useTopicStream('t1'))

    await waitFor(() => expect(result.current.topic).not.toBeNull())
    expect(getIntro).not.toHaveBeenCalled()
    expect(getReport).not.toHaveBeenCalled()
    expect(getMonitor).not.toHaveBeenCalled()
    expect(listDeltas).not.toHaveBeenCalled()
  })

  it('replays from seq 0 so a reload keeps the feed history', async () => {
    getTopic.mockResolvedValue(topic({ last_event_seq: 42 }))
    let seen: number | undefined
    emit = async ({ fromSeq }) => {
      seen = fromSeq
    }
    renderHook(() => useTopicStream('t1'))
    await waitFor(() => expect(seen).toBe(0))
  })
})

describe('useTopicStream — plan group', () => {
  it('hydrates the plan when intro.ready arrives', async () => {
    getTopic.mockResolvedValue(topic())
    emit = async ({ onEvent }) => onEvent(event('intro.ready'))

    const { result } = renderHook(() => useTopicStream('t1'))

    await waitFor(() => expect(result.current.introMarkdown).toBe('# Brief'))
    expect(result.current.parsed?.queries).toHaveLength(1)
  })

  it('collapses a burst of plan events into a bounded number of fetches', async () => {
    getTopic.mockResolvedValue(topic())
    emit = async ({ onEvent }) => {
      // A real gate emits intro.ready then needs_input back to back; a retrying
      // agent can emit more. None of them may fan out into one fetch each.
      onEvent(event('intro.ready', 1))
      onEvent(event('needs_input', 2))
      onEvent(event('intro.ready', 3))
      onEvent(event('needs_input', 4))
    }

    const { result } = renderHook(() => useTopicStream('t1'))
    await waitFor(() => expect(result.current.introMarkdown).toBe('# Brief'))
    // One in flight + exactly one re-run for everything that arrived during it.
    expect(getIntroMarkdown.mock.calls.length).toBeLessThanOrEqual(2)
  })

  it('does not drop a change that lands while a fetch is already running', async () => {
    getTopic.mockResolvedValue(topic())
    let resolveFirst: (v: string) => void = () => {}
    getIntroMarkdown
      .mockImplementationOnce(() => new Promise<string>((r) => (resolveFirst = r)))
      .mockResolvedValue('# Second')

    emit = async ({ onEvent }) => {
      onEvent(event('intro.ready', 1))
      // Still in flight; the response about to arrive predates this event.
      onEvent(event('needs_input', 2))
      resolveFirst('# First')
    }

    const { result } = renderHook(() => useTopicStream('t1'))
    await waitFor(() => expect(result.current.introMarkdown).toBe('# Second'))
  })

  it('hydrates on mount when the gate was passed while the user was away', async () => {
    getTopic.mockResolvedValue(topic({ state: 'planned_awaiting_review', plan_run_id: 'run-1' }))
    const { result } = renderHook(() => useTopicStream('t1'))

    await waitFor(() => expect(result.current.parsed).not.toBeNull())
    expect(getParsed).toHaveBeenCalledTimes(1)
    expect(getReport).not.toHaveBeenCalled()
  })
})

describe('useTopicStream — report group (16b)', () => {
  it('hydrates report and news on report.ready', async () => {
    getTopic.mockResolvedValue(topic({ state: 'delivering', plan_run_id: 'p1' }))
    emit = async ({ onEvent }) => onEvent(event('report.ready'))

    const { result } = renderHook(() => useTopicStream('t1'))

    await waitFor(() => expect(result.current.reportMarkdown).toBe('## Snapshot'))
    expect(result.current.report?.thesis_status).toBe('supported')
    expect(result.current.news?.sources).toHaveLength(1)
  })

  it('hydrates the report on mount when a deliver run already exists', async () => {
    getTopic.mockResolvedValue(
      topic({ state: 'reported', plan_run_id: 'p1', deliver_run_id: 'd1' }),
    )
    const { result } = renderHook(() => useTopicStream('t1'))

    await waitFor(() => expect(result.current.report).not.toBeNull())
    expect(getNews).toHaveBeenCalledTimes(1)
  })

  it('loads report and monitor when the topic reaches reported mid-stream', async () => {
    getTopic
      .mockResolvedValueOnce(topic({ state: 'delivering', plan_run_id: 'p1' }))
      .mockResolvedValue(topic({ state: 'reported', plan_run_id: 'p1', deliver_run_id: 'd1' }))
    emit = async ({ onEvent }) => onEvent(event('state.changed'))

    const { result } = renderHook(() => useTopicStream('t1'))

    await waitFor(() => expect(result.current.topic?.state).toBe('reported'))
    await waitFor(() => expect(result.current.monitor).not.toBeNull())
    expect(getReport).toHaveBeenCalled()
  })
})

describe('useTopicStream — monitoring group (16c)', () => {
  const monitored = () =>
    topic({ state: 'reported', plan_run_id: 'p1', deliver_run_id: 'd1' })

  it('loads monitor and deltas on mount for a reported topic', async () => {
    getTopic.mockResolvedValue(monitored())
    const { result } = renderHook(() => useTopicStream('t1'))

    await waitFor(() => expect(result.current.monitor?.status).toBe('active'))
    expect(result.current.deltas).toHaveLength(1)
  })

  it('re-reads monitor when the schedule changes', async () => {
    getTopic.mockResolvedValue(monitored())
    emit = async ({ onEvent }) => onEvent(event('monitor.updated'))

    renderHook(() => useTopicStream('t1'))
    // once on mount, once for the event
    await waitFor(() => expect(getMonitor).toHaveBeenCalledTimes(2))
  })

  it('re-reads monitor and deltas when a refresh completes', async () => {
    getTopic.mockResolvedValue(monitored())
    emit = async ({ onEvent }) => onEvent(event('refresh.completed'))

    renderHook(() => useTopicStream('t1'))
    await waitFor(() => expect(listDeltas).toHaveBeenCalledTimes(2))
    expect(getMonitor).toHaveBeenCalledTimes(2)
  })

  it('does not re-read deltas for a refresh that was skipped', async () => {
    getTopic.mockResolvedValue(monitored())
    emit = async ({ onEvent }) => onEvent(event('refresh.skipped'))

    renderHook(() => useTopicStream('t1'))
    await waitFor(() => expect(getMonitor).toHaveBeenCalledTimes(2))
    expect(listDeltas).toHaveBeenCalledTimes(1)
  })

  it('exposes per-group loading flags', async () => {
    getTopic.mockResolvedValue(monitored())
    const { result } = renderHook(() => useTopicStream('t1'))

    await waitFor(() => expect(result.current.monitor).not.toBeNull())
    expect(result.current.loading).toEqual({
      plan: false,
      report: false,
      monitor: false,
      deltas: false,
    })
  })
})

describe('useTopicStream — general', () => {
  it('appends events to the activity feed in order', async () => {
    getTopic.mockResolvedValue(topic())
    emit = async ({ onEvent }) => {
      onEvent(event('topic.created', 1))
      onEvent(event('stage.started', 2))
    }

    const { result } = renderHook(() => useTopicStream('t1'))
    await waitFor(() => expect(result.current.events).toHaveLength(2))
    expect(result.current.events.map((e) => e.seq)).toEqual([1, 2])
  })

  it('reports a load failure instead of rendering an empty shell', async () => {
    getTopic.mockRejectedValue(new Error('boom'))
    const { result } = renderHook(() => useTopicStream('t1'))

    await waitFor(() => expect(result.current.loadError).toBe('boom'))
    expect(result.current.status).toBe('error')
  })

  it('refresh(groups) re-reads only what was asked for', async () => {
    getTopic.mockResolvedValue(topic({ state: 'reported', plan_run_id: 'p1', deliver_run_id: 'd1' }))
    const { result } = renderHook(() => useTopicStream('t1'))

    await waitFor(() => expect(result.current.monitor).not.toBeNull())
    vi.clearAllMocks()
    getTopic.mockResolvedValue(topic({ state: 'reported', plan_run_id: 'p1', deliver_run_id: 'd1' }))

    await result.current.refresh(['monitor'])
    expect(getMonitor).toHaveBeenCalledTimes(1)
    expect(getReport).not.toHaveBeenCalled()
  })
})
