import { afterEach, describe, expect, it } from 'vitest'
import { cleanup, render, screen } from '@testing-library/react'
import { ArtifactMarkdown } from './ArtifactMarkdown'
import type { SourceRef } from '../lib/widgets/types'

/** End-to-end for the adaptive rendering path: prose + widgets + citations. */

const SOURCES: SourceRef[] = [
  {
    id: 's01',
    title: 'Tanker traffic halves',
    publisher: 'Reuters',
    url: 'https://example.com/1',
    source_class: 'primary_official',
    relevance_score: 0.83,
  },
  { id: 's02', title: 'SPR release weighed', publisher: 'Bloomberg' },
]

const widget = (payload: string) => '```markdown-ui-widget\n' + payload + '\n```'

afterEach(cleanup)

describe('ArtifactMarkdown', () => {
  it('renders prose as markdown', () => {
    render(<ArtifactMarkdown source={'## Snapshot\n\nTraffic is down.'} />)
    expect(screen.getByRole('heading', { name: 'Snapshot' })).toBeTruthy()
  })

  it('renders a widget the agent declared, without the page knowing its type', () => {
    render(
      <ArtifactMarkdown source={widget('{"type":"entity-chips","items":["NIOC","OPEC"]}')} />,
    )
    expect(screen.getByText('NIOC')).toBeTruthy()
    expect(screen.getByText('OPEC')).toBeTruthy()
  })

  it('interleaves prose and widgets in source order', () => {
    const { container } = render(
      <ArtifactMarkdown
        source={`First para.\n\n${widget('{"type":"highlights","items":["A point"]}')}\n\nLast para.`}
      />,
    )
    const text = container.textContent ?? ''
    expect(text.indexOf('First para.')).toBeLessThan(text.indexOf('A point'))
    expect(text.indexOf('A point')).toBeLessThan(text.indexOf('Last para.'))
  })

  it('links citations to their source', () => {
    const { container } = render(
      <ArtifactMarkdown source="Traffic halved [s01]." sources={SOURCES} />,
    )
    const link = container.querySelector('a.citation')
    expect(link?.getAttribute('href')).toBe('#src-s01')
    expect(link?.getAttribute('title')).toContain('Reuters')
  })

  it('marks a citation with no matching source as unresolved', () => {
    const { container } = render(
      <ArtifactMarkdown source="Claimed [s09]." sources={SOURCES} />,
    )
    expect(container.querySelector('.citation-missing')).toBeTruthy()
    expect(container.querySelector('a.citation')).toBeNull()
  })

  it('resolves a news-card widget against the run sources', () => {
    render(
      <ArtifactMarkdown source={widget('{"type":"news-card","sourceId":"s01"}')} sources={SOURCES} />,
    )
    expect(screen.getByText('Tanker traffic halves')).toBeTruthy()
    expect(screen.getByText('Reuters')).toBeTruthy()
  })

  it('says so when a widget names a source the run does not have', () => {
    render(
      <ArtifactMarkdown source={widget('{"type":"news-card","sourceId":"s99"}')} sources={SOURCES} />,
    )
    expect(screen.getByText(/referenced but not present/)).toBeTruthy()
  })

  it('shows every source when source-list omits ids', () => {
    render(<ArtifactMarkdown source={widget('{"type":"source-list"}')} sources={SOURCES} />)
    expect(screen.getByText('Tanker traffic halves')).toBeTruthy()
    expect(screen.getByText('SPR release weighed')).toBeTruthy()
  })

  it('degrades an unknown widget visibly instead of blanking the section', () => {
    render(<ArtifactMarkdown source={widget('{"type":"heatmap","cells":[]}')} />)
    expect(screen.getByText(/Cannot display/)).toBeTruthy()
    expect(screen.getByText('heatmap')).toBeTruthy()
  })

  it('still sanitizes prose around widgets', () => {
    const { container } = render(
      <ArtifactMarkdown
        source={`<script>alert(1)</script>\n\n${widget('{"type":"highlights","items":["ok"]}')}`}
      />,
    )
    expect(container.querySelector('script')).toBeNull()
    expect(screen.getByText('ok')).toBeTruthy()
  })

  it('renders legacy tags from artifacts already on disk', () => {
    render(<ArtifactMarkdown source="<EntityChips>NIOC, OPEC</EntityChips>" />)
    expect(screen.getByText('NIOC')).toBeTruthy()
  })

  it('renders key-findings with confidence and citations', () => {
    render(
      <ArtifactMarkdown
        source={widget(
          '{"type":"key-findings","findings":[{"finding":"Exports down 12%","confidence":"high","source_ids":["s01"]}]}',
        )}
        sources={SOURCES}
      />,
    )
    expect(screen.getByText('Exports down 12%')).toBeTruthy()
    expect(screen.getByText('high confidence')).toBeTruthy()
  })

  it('renders a scenario table with probability moves', () => {
    render(
      <ArtifactMarkdown
        source={widget(
          '{"type":"scenario-table","scenarios":[{"label":"Closure","p_before":0.2,"p_after":0.45,"verdict":"supports"}]}',
        )}
      />,
    )
    expect(screen.getByText('Closure')).toBeTruthy()
    expect(screen.getByText('20%')).toBeTruthy()
    expect(screen.getByText('45%')).toBeTruthy()
    expect(screen.getByText('supports')).toBeTruthy()
  })

  it('renders a callout', () => {
    render(
      <ArtifactMarkdown
        source={widget('{"type":"callout","tone":"risk","title":"Blind spot","body":"No Farsi coverage."}')}
      />,
    )
    expect(screen.getByText('Blind spot')).toBeTruthy()
    expect(screen.getByText('No Farsi coverage.')).toBeTruthy()
  })

  it('renders metrics', () => {
    render(
      <ArtifactMarkdown
        source={widget('{"type":"metrics","items":[{"label":"Sources","value":17}]}')}
      />,
    )
    expect(screen.getByText('Sources')).toBeTruthy()
    expect(screen.getByText('17')).toBeTruthy()
  })
})
