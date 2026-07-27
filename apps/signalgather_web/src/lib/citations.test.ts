import { describe, expect, it } from 'vitest'
import { indexSources, linkCitations, sourceAnchorId } from './citations'
import type { SourceRef } from './widgets/types'

const SOURCES: SourceRef[] = [
  { id: 's01', title: 'Tanker traffic halves', publisher: 'Reuters', url: 'https://r.co/1' },
  { id: 's03', title: 'SPR release considered', publisher: 'Bloomberg' },
]

const index = indexSources(SOURCES)

describe('indexSources', () => {
  it('indexes case-insensitively and skips rows with no id', () => {
    const map = indexSources([...SOURCES, { id: '' } as SourceRef])
    expect(map.get('s01')?.publisher).toBe('Reuters')
    expect(map.size).toBe(2)
  })

  it('returns an empty map for undefined', () => {
    expect(indexSources(undefined).size).toBe(0)
  })
})

describe('linkCitations', () => {
  it('links a known citation to its source anchor', () => {
    const html = linkCitations('<p>Traffic halved [s01].</p>', { sources: index })
    expect(html).toContain(`href="#${sourceAnchorId('s01')}"`)
    expect(html).toContain('class="citation"')
    expect(html).toContain('Tanker traffic halves — Reuters')
  })

  it('keeps the surrounding brackets and prose', () => {
    const html = linkCitations('<p>Traffic halved [s01].</p>', { sources: index })
    expect(html).toMatch(/Traffic halved \[<a[^>]*>s01<\/a>\]\./)
  })

  it('splits a multi-source citation into separate links', () => {
    const html = linkCitations('<p>Both [s01, s03] agree.</p>', { sources: index })
    expect(html.match(/<a /g)).toHaveLength(2)
    expect(html).toContain('>s01<')
    expect(html).toContain('>s03<')
  })

  it('accepts a semicolon separator', () => {
    const html = linkCitations('<p>[s01; s03]</p>', { sources: index })
    expect(html.match(/<a /g)).toHaveLength(2)
  })

  it('marks a citation with no matching source as unresolved', () => {
    const html = linkCitations('<p>Claimed [s99].</p>', { sources: index })
    expect(html).toContain('citation-missing')
    expect(html).not.toContain('<a')
  })

  it('leaves citations inside code untouched', () => {
    const html = linkCitations('<pre><code>grep [s01] file</code></pre>', { sources: index })
    expect(html).not.toContain('<a')
    expect(html).toContain('[s01]')
  })

  it('does not nest a link inside an existing link', () => {
    const html = linkCitations('<a href="https://x.co">see [s01]</a>', { sources: index })
    expect(html.match(/<a /g)).toHaveLength(1)
  })

  it('leaves text with no citations byte-identical', () => {
    const input = '<p>Nothing to cite here.</p>'
    expect(linkCitations(input, { sources: index })).toBe(input)
  })

  it('ignores bracketed text that is not a source id', () => {
    const input = '<p>An aside [see below] and [2024].</p>'
    expect(linkCitations(input, { sources: index })).toBe(input)
  })

  it('handles several citations in one text node', () => {
    const html = linkCitations('<p>[s01] then [s03] then [s01].</p>', { sources: index })
    expect(html.match(/<a /g)).toHaveLength(3)
  })

  it('works with no source index at all', () => {
    const html = linkCitations('<p>[s01]</p>')
    expect(html).toContain('citation-missing')
  })

  it('does not resurrect markup from the citation text', () => {
    // Input is already sanitized; the walker must only ever add anchors.
    const html = linkCitations('<p>&lt;script&gt; [s01]</p>', { sources: index })
    expect(html).not.toContain('<script')
  })
})
