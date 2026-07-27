import { describe, expect, it } from 'vitest'
import { describeEvent } from './eventText'
import type { TopicEvent } from './types'

function event(type: string, payload: Record<string, unknown> = {}): TopicEvent {
  return { seq: 1, event_type: type, topic_id: 't1', payload }
}

describe('describeEvent', () => {
  it('names pipeline stages in product language', () => {
    expect(describeEvent(event('stage.started', { stage: 'source_discover' })).title).toBe(
      'Finding trusted sources',
    )
  })

  it('summarises a finished stage with duration and cost', () => {
    const line = describeEvent(
      event('stage.finished', { stage: 'plan', duration_ms: 42_000, total_cost_usd: 0.315 }),
    )
    expect(line.title).toBe('Building the query plan — done')
    expect(line.detail).toBe('42.0s · $0.32')
  })

  it('marks a failed state change as bad', () => {
    const line = describeEvent(event('state.changed', { from: 'planning', to: 'failed' }))
    expect(line.tone).toBe('bad')
    expect(line.title).toBe('State → failed')
  })

  it('collapses tool input behind a disclosure', () => {
    const line = describeEvent(event('tool_use', { tool: 'WebSearch', input_preview: '{"q":"x"}' }))
    expect(line.title).toBe('WebSearch')
    expect(line.expandable).toBe('{"q":"x"}')
  })

  it('flags an errored tool result', () => {
    expect(describeEvent(event('tool_result', { is_error: true })).tone).toBe('warn')
  })

  it('calls out the review gate', () => {
    const line = describeEvent(event('needs_input', { gate: 'planned_awaiting_review' }))
    expect(line.tone).toBe('warn')
    expect(line.title).toContain('Proceed')
  })

  it('omits missing optional detail rather than printing undefined', () => {
    const line = describeEvent(event('stage.finished', { stage: 'deliver' }))
    expect(line.detail).toBeUndefined()
  })

  it('falls back to the wire name for an unknown event type', () => {
    expect(describeEvent(event('some.future.event')).title).toBe('some.future.event')
  })
})
