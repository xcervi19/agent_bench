import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import type { TopicDetail, TopicState } from '../lib/types'

const publishTopic = vi.fn()
const unpublishTopic = vi.fn()

vi.mock('../lib/api', () => ({
  ApiError: class extends Error {
    detail = ''
  },
  publishTopic: (id: string) => publishTopic(id),
  unpublishTopic: (id: string) => unpublishTopic(id),
}))

const { SharePanel } = await import('./SharePanel')

function topic(state: TopicState = 'reported', over: Partial<TopicDetail> = {}): TopicDetail {
  return {
    id: 't1',
    topic: 'Hormuz closure',
    state,
    available_actions: [],
    last_event_seq: 12,
    created_at: '2026-07-30T10:00:00+00:00',
    updated_at: '2026-07-31T10:00:00+00:00',
    plan_run_id: 'p1',
    deliver_run_id: 'd1',
    error: null,
    is_public: false,
    published_at: null,
    public_path: null,
    ...over,
  }
}

beforeEach(() => {
  publishTopic.mockReset().mockResolvedValue({ is_public: true })
  unpublishTopic.mockReset().mockResolvedValue({ is_public: false })
})

describe('publishing', () => {
  it('publishes a finished topic and reports the change upward', async () => {
    const onChanged = vi.fn()
    render(<SharePanel topic={topic()} onChanged={onChanged} />)

    await userEvent.click(screen.getByRole('button', { name: /share publicly/i }))

    expect(publishTopic).toHaveBeenCalledWith('t1')
    await waitFor(() => expect(onChanged).toHaveBeenCalled())
  })

  it('refuses to offer sharing before the topic has a report', () => {
    render(<SharePanel topic={topic('delivering')} onChanged={vi.fn()} />)

    const button = screen.getByRole('button', { name: /share publicly/i }) as HTMLButtonElement
    expect(button.disabled).toBe(true)
    expect(screen.getByText(/only a finished topic can be shared/i)).toBeTruthy()
  })

  it('warns that publishing freezes the topic before it is clicked', () => {
    render(<SharePanel topic={topic()} onChanged={vi.fn()} />)

    expect(screen.getByText(/monitoring pauses/i)).toBeTruthy()
    expect(screen.getByText(/cannot proceed, cancel, refresh or monitor/i)).toBeTruthy()
  })
})

describe('a published topic', () => {
  const published = topic('reported', {
    is_public: true,
    published_at: '2026-08-01T09:00:00+00:00',
    public_path: '/v1/public/topics/t1',
  })

  it('shows the link a reader without an account can open', () => {
    render(<SharePanel topic={published} onChanged={vi.fn()} />)

    const link = screen.getByLabelText('Public link') as HTMLInputElement
    expect(link.value).toContain('/shared/t1')
    expect(link.readOnly).toBe(true)
    expect(screen.getByText(/no account needed/i)).toBeTruthy()
  })

  it('offers no publish button, only a way back to private', async () => {
    const onChanged = vi.fn()
    render(<SharePanel topic={published} onChanged={onChanged} />)

    expect(screen.queryByRole('button', { name: /share publicly/i })).toBeNull()
    await userEvent.click(screen.getByRole('button', { name: /stop sharing/i }))

    expect(unpublishTopic).toHaveBeenCalledWith('t1')
    await waitFor(() => expect(onChanged).toHaveBeenCalled())
  })

  it('says the topic is frozen while shared', () => {
    render(<SharePanel topic={published} onChanged={vi.fn()} />)
    expect(screen.getByText(/nothing on this topic runs while it is\s+shared/i)).toBeTruthy()
  })
})
