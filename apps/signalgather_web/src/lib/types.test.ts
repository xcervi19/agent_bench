import { describe, expect, it } from 'vitest'
import { TERMINAL_STATES, TOPIC_STATES, isPipelineWorking } from './types'

describe('isPipelineWorking', () => {
  it('is true exactly while the agent is producing something', () => {
    expect(isPipelineWorking('planning')).toBe(true)
    expect(isPipelineWorking('delivering')).toBe(true)
  })

  it('is false while a plan waits on the user', () => {
    // Nothing is running here — the topic is parked on the approval gate, and a
    // live feed of what already finished is noise rather than reassurance.
    expect(isPipelineWorking('planned_awaiting_review')).toBe(false)
  })

  it('is false in every terminal state', () => {
    for (const state of TERMINAL_STATES) {
      expect(isPipelineWorking(state)).toBe(false)
    }
  })

  it('covers every state the API can report', () => {
    // A new state added to the union defaults to "not working", which hides the
    // feed. This is here so that stays a decision rather than an oversight.
    for (const state of TOPIC_STATES) {
      expect(typeof isPipelineWorking(state)).toBe('boolean')
    }
  })
})
