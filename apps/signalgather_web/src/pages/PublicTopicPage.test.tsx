import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import type { PublicTopicState } from '../lib/usePublicTopic'

let state: PublicTopicState

vi.mock('../lib/usePublicTopic', () => ({
  usePublicTopic: () => state,
}))

vi.mock('../lib/useAuth', () => ({
  useAuth: () => ({ user: null }),
}))

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual<typeof import('react-router-dom')>('react-router-dom')
  return { ...actual, useParams: () => ({ topicId: 't1' }) }
})

const { PublicTopicPage } = await import('./PublicTopicPage')

function baseState(over: Partial<PublicTopicState> = {}): PublicTopicState {
  return {
    topic: {
      id: 't1',
      topic: 'Hormuz closure',
      state: 'reported',
      published_at: '2026-08-01T09:00:00+00:00',
      created_at: '2026-07-30T10:00:00+00:00',
      updated_at: '2026-07-31T10:00:00+00:00',
      read_only: true,
      share_mode: 'live',
      frozen_at: null,
      updates: {
        live: true,
        last_updated_at: '2026-08-02T09:00:00+00:00',
        update_count: 3,
        latest_seq: 3,
      },
      has_plan: true,
      has_report: true,
    },
    intro: null,
    introMarkdown: null,
    parsed: null,
    report: null,
    reportMarkdown: '## Findings\n\nTanker rates moved.',
    news: null,
    sourceMix: null,
    deltas: [],
    loading: false,
    error: null,
    updatesSinceOpened: 0,
    ...over,
  }
}

function renderPage() {
  return render(
    <MemoryRouter>
      <PublicTopicPage />
    </MemoryRouter>,
  )
}

beforeEach(() => {
  state = baseState()
})

describe('a shared topic', () => {
  it('shows the research and says it is read-only', () => {
    renderPage()

    expect(screen.getByText('Hormuz closure')).toBeTruthy()
    expect(screen.getByText(/read-only/i)).toBeTruthy()
    expect(screen.getByText(/Tanker rates moved/)).toBeTruthy()
  })

  it('offers a reader no way to act on someone else’s topic', () => {
    state = baseState({
      parsed: { queries: [{ id: 'q1', query: 'hormuz tanker rates' }] },
      introMarkdown: '# Brief',
      deltas: [
        {
          seq: 1,
          run_id: 'r1',
          status: 'completed',
          new_sources_count: 2,
          queries_executed: 4,
          duration_ms: 1000,
          total_cost_usd: 0.2,
          summary_md: 'Two new sources.',
          error: null,
          created_at: '2026-07-31T10:00:00+00:00',
        },
      ],
    })
    renderPage()

    // Nothing that spends money, on any section of the page.
    for (const label of [/proceed/i, /cancel/i, /refresh/i, /enable monitoring/i, /share publicly/i]) {
      expect(screen.queryByRole('button', { name: label })).toBeNull()
    }
  })

  it('explains a withdrawn link instead of showing an empty page', () => {
    state = baseState({
      topic: null,
      error: 'This topic is not shared. The link may have been withdrawn by its owner.',
    })
    renderPage()

    expect(screen.getByText(/not shared/i)).toBeTruthy()
    expect(screen.getByRole('link', { name: /browse shared topics/i })).toBeTruthy()
  })

  it('invites a signed-out reader to sign in for their own research', () => {
    renderPage()
    expect(screen.getByRole('link', { name: /sign in/i })).toBeTruthy()
  })
})

describe('freshness', () => {
  it('tells a reader a live share keeps up, and when it last moved', () => {
    renderPage()

    expect(screen.getByText('Live')).toBeTruthy()
    expect(screen.getByText(/this page keeps up as the topic does/i)).toBeTruthy()
  })

  it('dates a snapshot instead, because there the share date is the freshness', () => {
    const base = baseState()
    state = baseState({
      topic: {
        ...base.topic!,
        share_mode: 'frozen',
        frozen_at: '2026-08-01T09:00:00+00:00',
        updates: { ...base.topic!.updates, live: false },
      },
    })
    renderPage()

    expect(screen.getByText('Snapshot')).toBeTruthy()
    expect(screen.getByText(/the state of the research at that moment/i)).toBeTruthy()
    expect(screen.queryByText(/keeps up as the topic does/i)).toBeNull()
  })

  it('says when updates landed under the reader rather than swapping silently', () => {
    state = baseState({ updatesSinceOpened: 2 })
    renderPage()

    expect(screen.getByRole('status').textContent).toMatch(/2 updates have landed/i)
  })
})
