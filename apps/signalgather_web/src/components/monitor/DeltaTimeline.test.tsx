import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { DeltaTimeline } from './DeltaTimeline'
import type { DeltaSummary } from '../../lib/types'

const getDelta = vi.fn()
const getDeltaNews = vi.fn()
const getDeltaReportMarkdown = vi.fn()

vi.mock('../../lib/api', () => ({
  ApiError: class extends Error {
    detail = 'boom'
  },
  getDelta: (...a: unknown[]) => getDelta(...(a as [])),
  getDeltaNews: (...a: unknown[]) => getDeltaNews(...(a as [])),
  getDeltaReportMarkdown: (...a: unknown[]) => getDeltaReportMarkdown(...(a as [])),
}))

function delta(over: Partial<DeltaSummary> = {}): DeltaSummary {
  return {
    seq: 1,
    run_id: 'r1',
    status: 'completed',
    new_sources_count: 3,
    queries_executed: 12,
    duration_ms: 42_000,
    total_cost_usd: 0.21,
    summary_md: 'Two tankers rerouted since the last cycle.',
    error: null,
    created_at: '2026-07-26T12:00:00+00:00',
    ...over,
  }
}

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
})

describe('DeltaTimeline', () => {
  it('invites monitoring when no cycle has run', () => {
    render(<DeltaTimeline topicId="t1" deltas={[]} loading={false} />)
    expect(screen.getByText('No refresh cycles yet')).toBeTruthy()
  })

  it('lists cycles with what they found', () => {
    render(<DeltaTimeline topicId="t1" deltas={[delta()]} loading={false} />)
    expect(screen.getByText('3 new')).toBeTruthy()
    expect(screen.getByText(/Two tankers rerouted/)).toBeTruthy()
  })

  it('keeps a cycle that found nothing visible', () => {
    render(<DeltaTimeline topicId="t1" deltas={[delta({ new_sources_count: 0 })]} loading={false} />)
    expect(screen.getByText('Nothing new')).toBeTruthy()
  })

  it('marks a failed cycle and shows its error', () => {
    render(
      <DeltaTimeline
        topicId="t1"
        deltas={[delta({ status: 'failed', error: 'search timed out' })]}
        loading={false}
      />,
    )
    expect(screen.getByText('Failed')).toBeTruthy()
    expect(screen.getByText('search timed out')).toBeTruthy()
  })

  it('shows cost and duration per cycle', () => {
    render(<DeltaTimeline topicId="t1" deltas={[delta()]} loading={false} />)
    expect(screen.getByText(/12q · 42\.0s · \$0\.21/)).toBeTruthy()
  })

  it('does not fetch artifacts until a cycle is opened', () => {
    render(<DeltaTimeline topicId="t1" deltas={[delta()]} loading={false} />)
    expect(getDelta).not.toHaveBeenCalled()
  })

  it('loads the detail on open and shows new sources', async () => {
    getDelta.mockResolvedValue({
      new_sources: ['s01'],
      thesis_status: 'weakened',
      trigger_terms_hit: ['SPR release'],
      key_changes: [{ finding: 'Exports cut', source_ids: ['s01'] }],
    })
    getDeltaNews.mockResolvedValue({
      sources: [{ id: 's01', title: 'Exports cut 12%', publisher: 'Reuters' }],
    })
    getDeltaReportMarkdown.mockResolvedValue('## Refresh delta\n\nExports cut [s01].')

    render(<DeltaTimeline topicId="t1" deltas={[delta()]} loading={false} />)
    await userEvent.click(screen.getByRole('button', { expanded: false }))

    await waitFor(() => expect(getDelta).toHaveBeenCalledWith('t1', 1))
    expect(await screen.findByText('Exports cut 12%')).toBeTruthy()
    expect(screen.getByText('Thesis weakened')).toBeTruthy()
    expect(screen.getByText('SPR release')).toBeTruthy()
    expect(screen.getByText(/Exports cut$/)).toBeTruthy()
  })

  it('says so when a cycle brought no new sources', async () => {
    getDelta.mockResolvedValue({ new_sources: [], summary_md: 'No new material.' })
    getDeltaNews.mockResolvedValue({ sources: [] })
    getDeltaReportMarkdown.mockResolvedValue(null)

    render(<DeltaTimeline topicId="t1" deltas={[delta({ new_sources_count: 0 })]} loading={false} />)
    await userEvent.click(screen.getByRole('button', { expanded: false }))

    expect(await screen.findByText(/found no genuinely new sources/)).toBeTruthy()
  })

  it('offers a retry when the detail cannot be loaded', async () => {
    getDelta.mockRejectedValue(new Error('network down'))
    getDeltaNews.mockResolvedValue(null)
    getDeltaReportMarkdown.mockResolvedValue(null)

    render(<DeltaTimeline topicId="t1" deltas={[delta()]} loading={false} />)
    await userEvent.click(screen.getByRole('button', { expanded: false }))

    expect(await screen.findByRole('alert')).toBeTruthy()
    expect(screen.getByRole('button', { name: 'Retry' })).toBeTruthy()
  })

  it('collapses an open cycle again', async () => {
    getDelta.mockResolvedValue({ new_sources: [] })
    getDeltaNews.mockResolvedValue({ sources: [] })
    getDeltaReportMarkdown.mockResolvedValue(null)

    render(<DeltaTimeline topicId="t1" deltas={[delta()]} loading={false} />)
    const row = screen.getByRole('button', { expanded: false })
    await userEvent.click(row)
    await screen.findByText(/found no genuinely new sources/)
    await userEvent.click(row)
    expect(screen.queryByText(/found no genuinely new sources/)).toBeNull()
  })
})
