import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MonitorPanel } from './MonitorPanel'
import type { RefreshAck } from '../../lib/api'
import type { MonitorState, TopicDetail, TopicState } from '../../lib/types'

const startMonitor = vi.fn(async () => ({}) as MonitorState)
const updateMonitor = vi.fn(async () => ({}) as MonitorState)
const stopMonitor = vi.fn(async () => {})
const triggerRefresh = vi.fn<() => Promise<RefreshAck>>(async () => ({
  accepted: true,
  subscription_id: 1,
  queued: true,
}))

vi.mock('../../lib/api', () => ({
  ApiError: class extends Error {
    detail = ''
  },
  startMonitor: (...a: unknown[]) => startMonitor(...(a as [])),
  updateMonitor: (...a: unknown[]) => updateMonitor(...(a as [])),
  stopMonitor: (...a: unknown[]) => stopMonitor(...(a as [])),
  triggerRefresh: (...a: unknown[]) => triggerRefresh(...(a as [])),
}))

function topic(state: TopicState = 'reported'): TopicDetail {
  return {
    id: 't1',
    topic: 'Hormuz',
    state,
    available_actions: [],
    last_event_seq: 9,
    created_at: '2026-07-26T10:00:00+00:00',
    updated_at: '2026-07-26T12:00:00+00:00',
    plan_run_id: 'p1',
    deliver_run_id: 'd1',
    error: null,
  }
}

function monitor(overrides: Partial<MonitorState> = {}): MonitorState {
  return {
    subscription_id: 1,
    status: 'active',
    max_age_hours: 48,
    refresh_count: 3,
    refresh_locked: false,
    schedule_enabled: false,
    schedule_interval_hours: null,
    next_refresh_at: null,
    last_refresh_at: '2026-07-26T11:00:00+00:00',
    last_scheduled_refresh_at: null,
    last_refresh_run_id: 'r1',
    ...overrides,
  }
}

function renderPanel(over: Partial<Parameters<typeof MonitorPanel>[0]> = {}) {
  const props = {
    topic: topic(),
    monitor: monitor(),
    loading: false,
    onChanged: vi.fn(),
    ...over,
  }
  return { ...render(<MonitorPanel {...props} />), props }
}

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
})

describe('MonitorPanel', () => {
  it('explains why monitoring is unavailable before a report exists', () => {
    renderPanel({ topic: topic('delivering'), monitor: null })
    expect(screen.getByText(/starts once the topic has a finished report/)).toBeTruthy()
    expect(screen.queryByRole('button', { name: 'Enable monitoring' })).toBeNull()
  })

  it('offers to enable monitoring on a reported topic', async () => {
    const { props } = renderPanel({ monitor: null })
    await userEvent.click(screen.getByRole('button', { name: 'Enable monitoring' }))
    await waitFor(() => expect(startMonitor).toHaveBeenCalledWith('t1', { maxAgeHours: 48 }))
    expect(props.onChanged).toHaveBeenCalled()
  })

  it('changes the freshness window', async () => {
    renderPanel()
    await userEvent.click(screen.getByRole('button', { name: '24h' }))
    await waitFor(() => expect(updateMonitor).toHaveBeenCalledWith('t1', { maxAgeHours: 24 }))
  })

  it('turns the schedule on with an interval', async () => {
    renderPanel()
    await userEvent.click(screen.getByRole('button', { name: 'Every 6h' }))
    await waitFor(() =>
      expect(updateMonitor).toHaveBeenCalledWith('t1', {
        scheduleEnabled: true,
        scheduleIntervalHours: 6,
      }),
    )
  })

  it('turns the schedule off without touching the subscription', async () => {
    renderPanel({ monitor: monitor({ schedule_enabled: true, schedule_interval_hours: 24 }) })
    await userEvent.click(screen.getByRole('button', { name: 'Off' }))
    await waitFor(() =>
      expect(updateMonitor).toHaveBeenCalledWith('t1', { scheduleEnabled: false }),
    )
    expect(stopMonitor).not.toHaveBeenCalled()
  })

  it('shows a freshness window set outside the presets', () => {
    renderPanel({ monitor: monitor({ max_age_hours: 120 }) })
    const button = screen.getByRole('button', { name: '120h' })
    expect(button.getAttribute('aria-pressed')).toBe('true')
  })

  it('keeps preset windows in ascending order when injecting the current value', () => {
    renderPanel({ monitor: monitor({ max_age_hours: 120 }) })
    const labels = ['24h', '48h', '72h', '120h', '168h']
    const rendered = labels.map((l) => screen.getByRole('button', { name: l }).textContent)
    expect(rendered).toEqual(labels)
  })

  it('does not duplicate a window already in the presets', () => {
    renderPanel({ monitor: monitor({ max_age_hours: 48 }) })
    expect(screen.getAllByRole('button', { name: '48h' })).toHaveLength(1)
  })

  it('marks the active schedule interval', () => {
    renderPanel({ monitor: monitor({ schedule_enabled: true, schedule_interval_hours: 24 }) })
    expect(screen.getByRole('button', { name: 'Daily' }).getAttribute('aria-pressed')).toBe('true')
    expect(screen.getByRole('button', { name: 'Off' }).getAttribute('aria-pressed')).toBe('false')
  })

  it('pauses an active subscription', async () => {
    renderPanel()
    await userEvent.click(screen.getByRole('button', { name: 'Pause' }))
    await waitFor(() => expect(stopMonitor).toHaveBeenCalledWith('t1'))
  })

  it('resumes a paused subscription and keeps its freshness window', async () => {
    renderPanel({ monitor: monitor({ status: 'paused', max_age_hours: 72 }) })
    await userEvent.click(screen.getByRole('button', { name: 'Resume' }))
    await waitFor(() => expect(startMonitor).toHaveBeenCalledWith('t1', { maxAgeHours: 72 }))
  })

  it('triggers a manual refresh and confirms it started', async () => {
    renderPanel()
    await userEvent.click(screen.getByRole('button', { name: 'Refresh now' }))
    await waitFor(() => expect(triggerRefresh).toHaveBeenCalledWith('t1'))
    expect(await screen.findByText(/Refresh started/)).toBeTruthy()
  })

  it('reports an already-running cycle as information, not an error', async () => {
    triggerRefresh.mockResolvedValueOnce({
      accepted: true,
      subscription_id: 1,
      queued: false,
      reason: 'refresh already running',
    })
    renderPanel()
    await userEvent.click(screen.getByRole('button', { name: 'Refresh now' }))
    expect(await screen.findByText('refresh already running')).toBeTruthy()
    expect(screen.queryByRole('alert')).toBeNull()
  })

  it('blocks manual refresh while a cycle is locked', () => {
    renderPanel({ monitor: monitor({ refresh_locked: true }) })
    expect(screen.getByRole('button', { name: 'Refresh now' }).hasAttribute('disabled')).toBe(true)
    expect(screen.getByText('A refresh cycle is running now.')).toBeTruthy()
  })

  it('blocks manual refresh while paused', () => {
    renderPanel({ monitor: monitor({ status: 'paused' }) })
    expect(screen.getByRole('button', { name: 'Refresh now' }).hasAttribute('disabled')).toBe(true)
  })

  it('surfaces a rejected change', async () => {
    updateMonitor.mockRejectedValueOnce(new Error('interval out of bounds'))
    renderPanel()
    await userEvent.click(screen.getByRole('button', { name: 'Weekly' }))
    await waitFor(() =>
      expect(screen.getByRole('alert').textContent).toContain('interval out of bounds'),
    )
  })
})
