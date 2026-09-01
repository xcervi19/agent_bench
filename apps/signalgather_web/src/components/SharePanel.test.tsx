import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import type { TopicDetail, TopicState } from '../lib/types'

const publishTopic = vi.fn()
const unpublishTopic = vi.fn()
const setShareMode = vi.fn()

vi.mock('../lib/api', () => ({
  ApiError: class extends Error {
    detail = ''
  },
  publishTopic: (id: string, mode: string) => publishTopic(id, mode),
  unpublishTopic: (id: string) => unpublishTopic(id),
  setShareMode: (id: string, mode: string) => setShareMode(id, mode),
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
    share_mode: null,
    frozen_at: null,
    ...over,
  }
}

beforeEach(() => {
  publishTopic.mockReset().mockResolvedValue({ is_public: true })
  unpublishTopic.mockReset().mockResolvedValue({ is_public: false })
  setShareMode.mockReset().mockResolvedValue({ is_public: true })
})

describe('publishing', () => {
  it('publishes a finished topic and reports the change upward', async () => {
    const onChanged = vi.fn()
    render(<SharePanel topic={topic()} onChanged={onChanged} />)

    await userEvent.click(screen.getByRole('button', { name: /share publicly/i }))

    expect(publishTopic).toHaveBeenCalledWith('t1', 'live')
    await waitFor(() => expect(onChanged).toHaveBeenCalled())
  })

  it('refuses to offer sharing before the topic has a report', () => {
    render(<SharePanel topic={topic('delivering')} onChanged={vi.fn()} />)

    const button = screen.getByRole('button', { name: /share publicly/i }) as HTMLButtonElement
    expect(button.disabled).toBe(true)
    expect(screen.getByText(/only a finished topic can be shared/i)).toBeTruthy()
  })

  it('offers live sharing by default, and says what each mode costs', () => {
    render(<SharePanel topic={topic()} onChanged={vi.fn()} />)

    expect(screen.getByRole('radio', { name: /live/i }).getAttribute('aria-checked')).toBe('true')
    expect(screen.getByRole('radio', { name: /snapshot/i }).getAttribute('aria-checked')).toBe(
      'false',
    )
    expect(screen.getByText(/you keep every control/i)).toBeTruthy()
    expect(screen.getByText(/monitoring pauses/i)).toBeTruthy()
  })

  it('publishes a snapshot when the owner picks one', async () => {
    render(<SharePanel topic={topic()} onChanged={vi.fn()} />)

    await userEvent.click(screen.getByRole('radio', { name: /snapshot/i }))
    await userEvent.click(screen.getByRole('button', { name: /share publicly/i }))

    expect(publishTopic).toHaveBeenCalledWith('t1', 'frozen')
  })

  it('never claims a reader can act, in either mode', () => {
    render(<SharePanel topic={topic()} onChanged={vi.fn()} />)
    expect(screen.getByText(/cannot proceed, cancel, refresh or monitor/i)).toBeTruthy()
  })
})

describe('a published topic', () => {
  const published = topic('reported', {
    is_public: true,
    published_at: '2026-08-01T09:00:00+00:00',
    public_path: '/v1/public/topics/t1',
    share_mode: 'live',
  })

  const pinned = topic('reported', {
    is_public: true,
    published_at: '2026-08-01T09:00:00+00:00',
    public_path: '/v1/public/topics/t1',
    share_mode: 'frozen',
    frozen_at: '2026-08-01T09:00:00+00:00',
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

  it('says a live share keeps up, and does not claim the topic is stopped', () => {
    render(<SharePanel topic={published} onChanged={vi.fn()} />)

    expect(screen.getByText(/keeps up as this topic updates/i)).toBeTruthy()
    expect(screen.queryByText(/nothing on this topic runs/i)).toBeNull()
  })

  it('says a pinned share is holding still, and why', () => {
    render(<SharePanel topic={pinned} onChanged={vi.fn()} />)
    expect(screen.getByText(/nothing on this topic runs while it stays pinned/i)).toBeTruthy()
  })

  it('lets the owner pin a live share without touching the link', async () => {
    const onChanged = vi.fn()
    render(<SharePanel topic={published} onChanged={onChanged} />)

    await userEvent.click(screen.getByRole('button', { name: /pin to a snapshot/i }))

    expect(setShareMode).toHaveBeenCalledWith('t1', 'frozen')
    await waitFor(() => expect(onChanged).toHaveBeenCalled())
  })

  it('lets the owner take a pinned share back to live', async () => {
    render(<SharePanel topic={pinned} onChanged={vi.fn()} />)

    await userEvent.click(screen.getByRole('button', { name: /switch to live/i }))

    expect(setShareMode).toHaveBeenCalledWith('t1', 'live')
  })
})
