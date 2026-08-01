import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { TopicListPage } from './TopicListPage'
import type { TopicListItem, TopicState } from '../lib/types'

const listTopics = vi.fn()
const createTopic = vi.fn()
const navigate = vi.fn()

vi.mock('../lib/api', () => ({
  ApiError: class ApiError extends Error {
    detail = 'boom'
  },
  listTopics: () => listTopics(),
  createTopic: (topic: string) => createTopic(topic),
}))

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual<typeof import('react-router-dom')>('react-router-dom')
  return { ...actual, useNavigate: () => navigate }
})

function item(state: TopicState, topic = 'Hormuz closure'): TopicListItem {
  return {
    id: 't1',
    topic,
    state,
    available_actions: [],
    last_event_seq: 3,
    created_at: '2026-07-26T10:00:00+00:00',
    updated_at: '2026-07-26T10:04:00+00:00',
    is_public: false,
    published_at: null,
    public_path: null,
  }
}

function renderPage() {
  return render(
    <MemoryRouter>
      <TopicListPage />
    </MemoryRouter>,
  )
}

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
})

describe('TopicListPage', () => {
  it('invites a first topic when the account is empty', async () => {
    listTopics.mockResolvedValue({ items: [] })
    renderPage()
    expect(await screen.findByText('No topics yet')).toBeTruthy()
  })

  it('lists the users topics with their state', async () => {
    listTopics.mockResolvedValue({ items: [item('delivering')] })
    renderPage()
    expect(await screen.findByText('Hormuz closure')).toBeTruthy()
    expect(screen.getByText('Researching')).toBeTruthy()
  })

  it('flags a topic that is waiting on the user', async () => {
    listTopics.mockResolvedValue({ items: [item('planned_awaiting_review')] })
    renderPage()
    expect(await screen.findByText('Needs your review')).toBeTruthy()
  })

  it('creates a topic from plain language and opens its workspace', async () => {
    listTopics.mockResolvedValue({ items: [] })
    createTopic.mockResolvedValue({ topic_id: 'new-1', state: 'planning', events_url: '/x' })
    renderPage()

    await userEvent.type(screen.getByLabelText('Topic'), 'Hormuz strait closure')
    await userEvent.click(screen.getByRole('button', { name: 'Start planning' }))

    await waitFor(() => expect(createTopic).toHaveBeenCalledWith('Hormuz strait closure'))
    expect(navigate).toHaveBeenCalledWith('/topics/new-1')
  })

  it('keeps the start button inert until something is typed', async () => {
    listTopics.mockResolvedValue({ items: [] })
    renderPage()
    await screen.findByText('No topics yet')
    expect(screen.getByRole('button', { name: 'Start planning' }).hasAttribute('disabled')).toBe(
      true,
    )
  })

  it('shows a retryable error when the list cannot be loaded', async () => {
    listTopics.mockRejectedValueOnce(new Error('network down'))
    renderPage()

    const alert = await screen.findByRole('alert')
    expect(alert.textContent).toContain('network down')

    listTopics.mockResolvedValue({ items: [item('reported')] })
    await userEvent.click(screen.getByRole('button', { name: 'Retry' }))
    expect(await screen.findByText('Hormuz closure')).toBeTruthy()
  })
})
