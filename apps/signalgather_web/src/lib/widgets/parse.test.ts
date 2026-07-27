import { describe, expect, it } from 'vitest'
import { parseArtifact } from './parse'
import type { AnyWidget } from './types'

const widgets = (md: string): AnyWidget[] =>
  parseArtifact(md)
    .filter((s) => s.kind === 'widget')
    .map((s) => (s as { widget: AnyWidget }).widget)

const prose = (md: string): string[] =>
  parseArtifact(md)
    .filter((s) => s.kind === 'markdown')
    .map((s) => (s as { text: string }).text.trim())

function fence(payload: string): string {
  return '```markdown-ui-widget\n' + payload + '\n```'
}

describe('parseArtifact — prose', () => {
  it('returns plain markdown untouched as a single segment', () => {
    const segments = parseArtifact('# Title\n\nBody text.')
    expect(segments).toHaveLength(1)
    expect(segments[0]).toMatchObject({ kind: 'markdown' })
  })

  it('drops whitespace-only gaps between widgets', () => {
    const md = `${fence('{"type":"highlights","items":["a"]}')}\n\n${fence('{"type":"highlights","items":["b"]}')}`
    expect(prose(md)).toEqual([])
    expect(widgets(md)).toHaveLength(2)
  })

  it('keeps prose on both sides of a widget, in order', () => {
    const segments = parseArtifact(
      `Before.\n\n${fence('{"type":"entity-chips","items":["NIOC"]}')}\n\nAfter.`,
    )
    expect(segments.map((s) => s.kind)).toEqual(['markdown', 'widget', 'markdown'])
    expect(prose(segments.map(() => '').join(''))).toEqual([])
    expect((segments[0] as { text: string }).text).toContain('Before.')
    expect((segments[2] as { text: string }).text).toContain('After.')
  })

  it('supports tilde fences', () => {
    const md = '~~~markdown-ui-widget\n{"type":"highlights","items":["a"]}\n~~~'
    expect(widgets(md)[0]).toMatchObject({ type: 'highlights' })
  })
})

describe('parseArtifact — fenced widgets', () => {
  it('parses entity-chips', () => {
    expect(widgets(fence('{"type":"entity-chips","items":["NIOC","OPEC"],"label":"Actors"}'))[0])
      .toEqual({ type: 'entity-chips', items: ['NIOC', 'OPEC'], label: 'Actors' })
  })

  it('parses key-findings and drops entries with no text', () => {
    const w = widgets(
      fence(
        '{"type":"key-findings","findings":[{"finding":"A","confidence":"high","source_ids":["s01"]},{"finding":""}]}',
      ),
    )[0]
    expect(w).toMatchObject({ type: 'key-findings' })
    expect((w as { findings: unknown[] }).findings).toHaveLength(1)
  })

  it('parses scenario-table with probabilities', () => {
    const w = widgets(
      fence('{"type":"scenario-table","scenarios":[{"id":"sc1","p_before":0.3,"p_after":0.55}]}'),
    )[0]
    expect(w).toMatchObject({ type: 'scenario-table' })
  })

  it('accepts snake_case aliases the agent may emit', () => {
    expect(widgets(fence('{"type":"news-card","source_id":"s04"}'))[0]).toEqual({
      type: 'news-card',
      sourceId: 's04',
    })
    expect(widgets(fence('{"type":"source-list","source_ids":["s01","s02"]}'))[0]).toMatchObject({
      sourceIds: ['s01', 's02'],
    })
  })

  it('treats source-list without ids as "all sources"', () => {
    expect(widgets(fence('{"type":"source-list"}'))[0]).toEqual({
      type: 'source-list',
      sourceIds: undefined,
      title: undefined,
    })
  })
})

describe('parseArtifact — degradation', () => {
  it('keeps an unregistered type visible with its payload', () => {
    const w = widgets(fence('{"type":"sankey-diagram","data":[1,2]}'))[0]
    expect(w).toMatchObject({ type: 'unknown', declaredType: 'sankey-diagram' })
    expect((w as { raw: string }).raw).toContain('sankey-diagram')
  })

  it('reports invalid JSON rather than throwing', () => {
    const w = widgets(fence('{"type": broken'))[0]
    expect(w).toMatchObject({ type: 'unknown' })
    expect((w as { reason: string }).reason).toMatch(/not valid JSON/)
  })

  it('reports a payload that fails its type contract', () => {
    const w = widgets(fence('{"type":"entity-chips","items":"NIOC"}'))[0]
    expect(w).toMatchObject({ type: 'unknown', declaredType: 'entity-chips' })
    expect((w as { reason: string }).reason).toMatch(/items/)
  })

  it('rejects a widget with no type', () => {
    expect(widgets(fence('{"items":["a"]}'))[0]).toMatchObject({ type: 'unknown' })
  })

  it('rejects a JSON array payload', () => {
    expect(widgets(fence('[1,2,3]'))[0]).toMatchObject({ type: 'unknown' })
  })
})

describe('parseArtifact — legacy tags already on disk', () => {
  it('renders <EntityChips> body as chips', () => {
    expect(widgets('<EntityChips>NIOC, OPEC, IEA</EntityChips>')[0]).toEqual({
      type: 'entity-chips',
      items: ['NIOC', 'OPEC', 'IEA'],
    })
  })

  it('renders <EntityChips entities="..."/> attribute form', () => {
    expect(widgets('<EntityChips entities="NIOC, OPEC"/>')[0]).toEqual({
      type: 'entity-chips',
      items: ['NIOC', 'OPEC'],
    })
  })

  it('renders a bulleted <Highlights> block', () => {
    const w = widgets('<Highlights>\n- 13 angles\n- 3 languages\n</Highlights>')[0]
    expect(w).toEqual({ type: 'highlights', items: ['13 angles', '3 languages'] })
  })

  it('renders a block-level <NewsCard/> as a card', () => {
    expect(widgets('<NewsCard source-id="s01"/>')[0]).toEqual({
      type: 'news-card',
      sourceId: 's01',
    })
  })

  it('degrades an inline <NewsCard/> to a citation instead of losing it', () => {
    const segments = parseArtifact('- Tankers rerouted <NewsCard source-id="s03"/> this week.')
    expect(segments).toHaveLength(1)
    expect((segments[0] as { text: string }).text).toContain('[s03]')
    expect((segments[0] as { text: string }).text).not.toContain('NewsCard')
  })

  it('does not double-count a legacy tag inside a fenced widget', () => {
    const md = fence('{"type":"callout","body":"see <EntityChips>x</EntityChips>"}')
    const found = widgets(md)
    expect(found).toHaveLength(1)
    expect(found[0]).toMatchObject({ type: 'callout' })
  })

  it('leaves an unknown legacy tag to the sanitizer', () => {
    expect(widgets('<SomethingElse>x</SomethingElse>')).toHaveLength(0)
  })
})
