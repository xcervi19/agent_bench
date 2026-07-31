import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { TopicWorkspacePage } from './TopicWorkspacePage'
import type { TopicDetail, TopicState } from '../lib/types'

const LONG_TOPIC =
  'Strait of Hormuz transit risk and Middle East escalation. ' + 'Detail sentence. '.repeat(20)

let detail: TopicDetail

vi.mock('../lib/useTopicStream', () => ({
  useTopicStream: () => ({
    topic: detail,
    events: [],
    status: 'done',
    loading: { plan: false, report: false, monitor: false, deltas: false },
    loadError: null,
    intro: null,
    introMarkdown: null,
    parsed: null,
    report: null,
    reportMarkdown: null,
    news: null,
    monitor: null,
    deltas: [],
    refresh: vi.fn(),
  }),
}))

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual<typeof import('react-router-dom')>('react-router-dom')
  return { ...actual, useParams: () => ({ topicId: 't1' }) }
})

function topic(state: TopicState, over: Partial<TopicDetail> = {}): TopicDetail {
  return {
    id: 't1',
    topic: LONG_TOPIC,
    state,
    available_actions: [],
    last_event_seq: 231,
    created_at: '2026-07-27T10:00:00+00:00',
    updated_at: '2026-07-31T17:49:00+00:00',
    plan_run_id: 'p1',
    deliver_run_id: 'd1',
    error: null,
    ...over,
  }
}

function renderPage() {
  return render(
    <MemoryRouter>
      <TopicWorkspacePage />
    </MemoryRouter>,
  )
}

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
})

describe('TopicWorkspacePage — long topic brief', () => {
  it('clamps a long brief and offers to expand it', async () => {
    detail = topic('reported')
    const { container } = renderPage()

    expect(container.querySelector('h1')?.className).toContain('line-clamp-2')
    await userEvent.click(screen.getByRole('button', { name: 'Show full brief' }))
    expect(container.querySelector('h1')?.className).not.toContain('line-clamp-2')
    expect(screen.getByRole('button', { name: 'Show less' })).toBeTruthy()
  })

  it('leaves a short brief unclamped and offers no toggle', () => {
    detail = topic('reported', { topic: 'Hormuz closure' })
    const { container } = renderPage()

    expect(container.querySelector('h1')?.className).not.toContain('line-clamp')
    expect(screen.queryByRole('button', { name: 'Show full brief' })).toBeNull()
  })
})

describe('TopicWorkspacePage — elapsed time', () => {
  it('shows a running duration only while the pipeline is working', () => {
    detail = topic('delivering')
    renderPage()
    expect(screen.getByText('Running for')).toBeTruthy()
    expect(screen.queryByText('Total time')).toBeNull()
  })

  it('reports last activity rather than a wall-clock "total time" once terminal', () => {
    // updated_at is bumped by every refresh cycle, so created->updated is not
    // pipeline duration; claiming it as "Total time" read as 97h for a 14m run.
    detail = topic('reported')
    renderPage()
    expect(screen.getByText('Last activity')).toBeTruthy()
    expect(screen.queryByText('Total time')).toBeNull()
    expect(screen.queryByText(/97h/)).toBeNull()
  })
})
