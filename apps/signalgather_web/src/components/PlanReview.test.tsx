import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { PlanReview } from './PlanReview'
import type { ParsedArtifact, TopicDetail, TopicState } from '../lib/types'

const proceedTopic = vi.fn<(id: string) => Promise<void>>(async () => {})
const cancelTopic = vi.fn<(id: string) => Promise<void>>(async () => {})

vi.mock('../lib/api', () => ({
  proceedTopic: (id: string) => proceedTopic(id),
  cancelTopic: (id: string) => cancelTopic(id),
}))

function topicIn(state: TopicState): TopicDetail {
  const actions =
    state === 'planned_awaiting_review'
      ? (['proceed', 'cancel'] as const)
      : state === 'planning' || state === 'delivering'
        ? (['cancel'] as const)
        : ([] as const)
  return {
    id: 't1',
    topic: 'Hormuz closure',
    state,
    available_actions: [...actions],
    last_event_seq: 4,
    created_at: '2026-07-26T10:00:00+00:00',
    updated_at: '2026-07-26T10:05:00+00:00',
    plan_run_id: 'run-1',
    deliver_run_id: null,
    error: null,
  }
}

const PARSED: ParsedArtifact = {
  queries: [
    { id: 'q01', query: 'Hormuz tanker traffic', intent: 'monitoring', language: 'en' },
    { id: 'q02', query: 'تحركات ناقلات النفط', intent: 'context', language: 'ar' },
  ],
}

function renderGate(overrides: Partial<Parameters<typeof PlanReview>[0]> = {}) {
  const props = {
    topic: topicIn('planned_awaiting_review'),
    intro: null,
    introMarkdown: '# Understanding\n\nIran may close the strait.',
    parsed: PARSED,
    loading: false,
    onDecision: vi.fn(),
    ...overrides,
  }
  return { ...render(<PlanReview {...props} />), props }
}

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
})

describe('PlanReview', () => {
  it('renders the intro markdown brief', () => {
    renderGate()
    expect(screen.getByRole('heading', { name: 'Understanding' })).toBeTruthy()
    expect(screen.getByText(/Iran may close the strait/)).toBeTruthy()
  })

  it('shows the query plan with its count on the tab', async () => {
    renderGate()
    await userEvent.click(screen.getByRole('tab', { name: /Queries \(2\)/ }))
    expect(screen.getByText('Hormuz tanker traffic')).toBeTruthy()
    expect(screen.getByText('تحركات ناقلات النفط')).toBeTruthy()
  })

  it('calls proceed and notifies the parent at the gate', async () => {
    const { props } = renderGate()
    await userEvent.click(screen.getByRole('button', { name: 'Proceed' }))
    await waitFor(() => expect(proceedTopic).toHaveBeenCalledWith('t1'))
    expect(props.onDecision).toHaveBeenCalled()
  })

  it('calls cancel', async () => {
    renderGate()
    await userEvent.click(screen.getByRole('button', { name: 'Cancel topic' }))
    await waitFor(() => expect(cancelTopic).toHaveBeenCalledWith('t1'))
  })

  it('disables Proceed before the gate is reached', () => {
    renderGate({ topic: topicIn('planning') })
    expect(screen.getByRole('button', { name: 'Proceed' }).hasAttribute('disabled')).toBe(true)
    // Cancel stays live — a running plan can still be abandoned.
    expect(screen.getByRole('button', { name: 'Cancel topic' }).hasAttribute('disabled')).toBe(false)
  })

  it('disables both actions in a terminal state', () => {
    renderGate({ topic: topicIn('cancelled') })
    expect(screen.getByRole('button', { name: 'Proceed' }).hasAttribute('disabled')).toBe(true)
    expect(screen.getByRole('button', { name: 'Cancel topic' }).hasAttribute('disabled')).toBe(true)
  })

  it('surfaces a rejected decision instead of failing silently', async () => {
    proceedTopic.mockRejectedValueOnce(new Error('cannot proceed from state=delivering'))
    const { props } = renderGate()

    await userEvent.click(screen.getByRole('button', { name: 'Proceed' }))
    await waitFor(() =>
      expect(screen.getByRole('alert').textContent).toContain('cannot proceed from state=delivering'),
    )
    expect(props.onDecision).not.toHaveBeenCalled()
  })

  it('explains itself while the plan artifacts are still missing', () => {
    renderGate({ introMarkdown: null, parsed: null, loading: false })
    expect(screen.getByText(/still drafting the plan/)).toBeTruthy()
  })

  it('falls back to intro.json when intro.md is absent', () => {
    renderGate({
      introMarkdown: null,
      intro: { headline: 'Strait closure risk', highlights: ['13 angles in 3 languages'] },
    })
    expect(screen.getByText('Strait closure risk')).toBeTruthy()
    expect(screen.getByText('13 angles in 3 languages')).toBeTruthy()
  })
})
