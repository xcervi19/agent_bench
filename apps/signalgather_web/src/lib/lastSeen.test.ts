import { describe, expect, it, vi } from 'vitest'
import { hasUnseenActivity, lastSeenAt, markTopicSeen } from './lastSeen'

const T0 = '2026-07-26T10:00:00.000Z'
const T1 = '2026-07-26T12:00:00.000Z'

describe('lastSeen', () => {
  it('records and reads a visit', () => {
    markTopicSeen('t1', Date.parse(T0))
    expect(lastSeenAt('t1')).toBe(T0)
  })

  it('flags a topic that moved after the visit', () => {
    markTopicSeen('t1', Date.parse(T0))
    expect(hasUnseenActivity('t1', T1)).toBe(true)
  })

  it('does not flag a topic that has not moved', () => {
    markTopicSeen('t1', Date.parse(T1))
    expect(hasUnseenActivity('t1', T0)).toBe(false)
  })

  it('does not flag a topic that was never opened', () => {
    // Otherwise every brand-new topic would carry a "new since last visit" badge
    // on top of its state badge, which says nothing.
    expect(hasUnseenActivity('never-opened', T1)).toBe(false)
  })

  it('keeps topics independent', () => {
    markTopicSeen('t1', Date.parse(T1))
    expect(hasUnseenActivity('t1', T1)).toBe(false)
    expect(hasUnseenActivity('t2', T1)).toBe(false)
  })

  it('ignores an unparseable timestamp instead of flagging', () => {
    markTopicSeen('t1', Date.parse(T0))
    expect(hasUnseenActivity('t1', 'not-a-date')).toBe(false)
  })

  it('survives corrupt storage', () => {
    localStorage.setItem('signalgather.lastSeen', '{not json')
    expect(() => hasUnseenActivity('t1', T1)).not.toThrow()
    expect(hasUnseenActivity('t1', T1)).toBe(false)
  })

  it('does not throw when storage rejects a write', () => {
    const spy = vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
      throw new Error('QuotaExceededError')
    })
    expect(() => markTopicSeen('t1')).not.toThrow()
    spy.mockRestore()
  })
})
