import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { act, cleanup, renderHook } from '@testing-library/react'
import type { PublicTopic, ShareMode } from './types'

/**
 * The reader's side of #50. Three rules, each of which the server cannot
 * enforce for us:
 *
 *   - a live share is re-checked, so an open tab does not quietly go stale;
 *   - the check is cheap — artifacts are re-fetched only when the topic says
 *     something actually moved, not every minute;
 *   - a frozen share and a hidden tab poll nothing at all.
 */

const getPublicTopic = vi.fn<(id: string) => Promise<PublicTopic>>()
const getPublicReportMarkdown = vi.fn(async () => '## Findings')
const listPublicDeltas = vi.fn(async () => [])

vi.mock('./api', () => ({
  ApiError: class extends Error {
    isNotFound = false
    detail = ''
  },
}))

vi.mock('./publicApi', () => ({
  getPublicTopic: (id: string) => getPublicTopic(id),
  getPublicIntro: async () => null,
  getPublicIntroMarkdown: async () => null,
  getPublicParsed: async () => null,
  getPublicReport: async () => null,
  getPublicReportMarkdown: () => getPublicReportMarkdown(),
  getPublicNews: async () => null,
  getPublicSourceMix: async () => null,
  listPublicDeltas: () => listPublicDeltas(),
}))

const { usePublicTopic, POLL_INTERVAL_MS } = await import('./usePublicTopic')

function topic(over: Partial<PublicTopic> = {}, updates: Partial<PublicTopic['updates']> = {}): PublicTopic {
  return {
    id: 't1',
    topic: 'Hormuz closure',
    state: 'reported',
    published_at: '2026-08-01T09:00:00+00:00',
    created_at: '2026-07-30T10:00:00+00:00',
    updated_at: '2026-08-01T09:00:00+00:00',
    read_only: true,
    share_mode: 'live' as ShareMode,
    frozen_at: null,
    has_plan: true,
    has_report: true,
    ...over,
    updates: {
      live: true,
      last_updated_at: '2026-08-01T09:00:00+00:00',
      update_count: 1,
      latest_seq: 1,
      ...updates,
    },
  }
}

beforeEach(() => {
  vi.useFakeTimers()
  getPublicTopic.mockReset().mockResolvedValue(topic())
  getPublicReportMarkdown.mockClear()
  listPublicDeltas.mockClear()
})

afterEach(() => {
  cleanup()
  vi.useRealTimers()
})

/** Let the queued promises settle while timers are faked. */
async function settle() {
  await act(async () => {
    await vi.advanceTimersByTimeAsync(0)
  })
}

async function tickPoll() {
  await act(async () => {
    await vi.advanceTimersByTimeAsync(POLL_INTERVAL_MS)
  })
}

describe('a live share', () => {
  it('loads once, then re-checks the topic on a timer', async () => {
    renderHook(() => usePublicTopic('t1'))
    await settle()
    expect(getPublicTopic).toHaveBeenCalledTimes(1)

    await tickPoll()
    expect(getPublicTopic).toHaveBeenCalledTimes(2)
  })

  it('does not re-fetch the report when nothing moved', async () => {
    renderHook(() => usePublicTopic('t1'))
    await settle()
    expect(getPublicReportMarkdown).toHaveBeenCalledTimes(1)

    await tickPoll()
    await tickPoll()
    // Three checks of one cached row; one download of the actual research.
    expect(getPublicTopic).toHaveBeenCalledTimes(3)
    expect(getPublicReportMarkdown).toHaveBeenCalledTimes(1)
  })

  it('re-fetches and counts the update when a cycle completes', async () => {
    const { result } = renderHook(() => usePublicTopic('t1'))
    await settle()

    getPublicTopic.mockResolvedValue(
      topic({}, { last_updated_at: '2026-08-01T11:00:00+00:00', update_count: 2, latest_seq: 2 }),
    )
    await tickPoll()
    await settle()

    expect(getPublicReportMarkdown).toHaveBeenCalledTimes(2)
    expect(result.current.updatesSinceOpened).toBe(1)
  })
})

describe('a frozen share', () => {
  it('is fetched once and leaves no timer running in the reader’s tab', async () => {
    getPublicTopic.mockResolvedValue(
      topic({ share_mode: 'frozen', frozen_at: '2026-08-01T09:00:00+00:00' }, { live: false }),
    )
    const { result } = renderHook(() => usePublicTopic('t1'))
    await settle()

    expect(result.current.loading).toBe(false)
    await tickPoll()
    await tickPoll()
    expect(getPublicTopic).toHaveBeenCalledTimes(1)
  })
})

describe('a hidden tab', () => {
  it('checks nothing until someone looks at it again', async () => {
    const visibility = vi.spyOn(document, 'visibilityState', 'get').mockReturnValue('hidden')
    renderHook(() => usePublicTopic('t1'))
    await settle()
    expect(getPublicTopic).not.toHaveBeenCalled()

    visibility.mockReturnValue('visible')
    await act(async () => {
      document.dispatchEvent(new Event('visibilitychange'))
      await vi.advanceTimersByTimeAsync(0)
    })
    expect(getPublicTopic).toHaveBeenCalledTimes(1)
    visibility.mockRestore()
  })
})
