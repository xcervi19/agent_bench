import { describe, expect, it } from 'vitest'
import { isAuthoritative, summarizeSources } from './sourceQuality'
import type { SourceRef } from './widgets/types'

const source = (over: Partial<SourceRef> = {}): SourceRef => ({
  id: 's01',
  source_class: 'specialist_outlet',
  ...over,
})

describe('isAuthoritative', () => {
  it('accepts primary_official', () => {
    expect(isAuthoritative(source({ source_class: 'primary_official' }))).toBe(true)
  })

  it('accepts data_feed', () => {
    expect(isAuthoritative(source({ source_class: 'data_feed' }))).toBe(true)
  })

  it('rejects outlets, aggregators and blogs', () => {
    for (const cls of ['specialist_outlet', 'aggregator', 'blog_or_newsletter', 'social']) {
      expect(isAuthoritative(source({ source_class: cls }))).toBe(false)
    }
  })

  it('rejects a source with no class', () => {
    expect(isAuthoritative(source({ source_class: undefined }))).toBe(false)
  })
})

describe('summarizeSources', () => {
  it('counts authoritative sources', () => {
    const mix = summarizeSources([
      source({ source_class: 'primary_official' }),
      source({ source_class: 'specialist_outlet' }),
      source({ source_class: 'data_feed' }),
    ])
    expect(mix).toEqual({ total: 3, authoritative: 2, entirelySecondary: false })
  })

  it('flags a run with no primary sources', () => {
    const mix = summarizeSources([source(), source({ source_class: 'aggregator' })])
    expect(mix.entirelySecondary).toBe(true)
  })

  it('does not flag an empty run', () => {
    expect(summarizeSources([])).toEqual({
      total: 0,
      authoritative: 0,
      entirelySecondary: false,
    })
  })

  it('treats undefined as empty', () => {
    expect(summarizeSources(undefined).total).toBe(0)
  })

  it('flags the observed prod refresh', () => {
    const observed = ['Al Hadath', 'France 24', 'Sputnik', 'Bloomberg', 'Al Jazeera'].map(
      (publisher) => source({ publisher, source_class: 'specialist_outlet' }),
    )
    expect(summarizeSources(observed).entirelySecondary).toBe(true)
  })
})
