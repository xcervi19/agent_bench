import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { useState } from 'react'
import { ArtifactMarkdown } from '../components/ArtifactMarkdown'
import { CitationNavContext, useCitationNavigation } from './citationNav'
import type { SourceRef } from './widgets/types'

/**
 * The bug this closes: citations render as `<a href="#src-s04">`, but the anchor
 * only exists where a SourceCard mounts. Tabs render conditionally, so while the
 * reader is on Report the Sources panel is absent and the jump does nothing.
 */

const SOURCES: SourceRef[] = [
  { id: 's01', title: 'Tanker traffic halves', publisher: 'Reuters' },
  { id: 's04', title: 'War-risk premiums repriced', publisher: "Lloyd's List" },
]

const widget = (payload: string) => '```markdown-ui-widget\n' + payload + '\n```'

beforeEach(() => {
  // jsdom implements neither, and both run on the navigation path.
  Element.prototype.scrollIntoView = vi.fn()
})
afterEach(cleanup)

/** By class, not by text: a rendered SourceCard prints the same id in its header. */
function citation(id: string): HTMLAnchorElement {
  const links = Array.from(document.querySelectorAll<HTMLAnchorElement>('a.citation'))
  const link = links.find((node) => node.textContent === id)
  if (!link) throw new Error(`no citation link for ${id}`)
  return link
}

describe('citation click delegation', () => {
  it('hands over a citation whose source card is not currently mounted', () => {
    const navigate = vi.fn()
    render(
      <CitationNavContext.Provider value={navigate}>
        <ArtifactMarkdown source={'Premiums moved [s04].'} sources={SOURCES} />
      </CitationNavContext.Provider>,
    )

    const link = citation('s04')
    expect(link.getAttribute('href')).toBe('#src-s04')
    // fireEvent returns false once preventDefault has been called.
    const notPrevented = fireEvent.click(link)

    expect(navigate).toHaveBeenCalledWith('s04')
    expect(notPrevented).toBe(false)
  })

  it('leaves the native jump alone when the card is already on screen', () => {
    const navigate = vi.fn()
    render(
      <CitationNavContext.Provider value={navigate}>
        <ArtifactMarkdown
          source={'Traffic halved [s01].\n\n' + widget('{"type":"news-card","sourceId":"s01"}')}
          sources={SOURCES}
        />
      </CitationNavContext.Provider>,
    )

    // The widget put `#src-s01` in the DOM, so the anchor resolves on its own.
    expect(document.getElementById('src-s01')).toBeTruthy()
    const notPrevented = fireEvent.click(citation('s01'))

    expect(navigate).not.toHaveBeenCalled()
    expect(notPrevented).toBe(true)
  })

  it('does nothing without a navigator, so a tabless surface is unaffected', () => {
    render(<ArtifactMarkdown source={'Premiums moved [s04].'} sources={SOURCES} />)
    expect(fireEvent.click(citation('s04'))).toBe(true)
  })
})

/** A two-tab stand-in for the workspace and public pages. */
function TabbedPage() {
  const [tab, setTab] = useState<'report' | 'sources'>('report')
  const navigate = useCitationNavigation<'report' | 'sources'>('sources', tab, setTab)
  return (
    <CitationNavContext.Provider value={navigate}>
      <p>tab:{tab}</p>
      {tab === 'report' && <ArtifactMarkdown source={'Premiums moved [s04].'} sources={SOURCES} />}
      {tab === 'sources' && <article id="src-s04">War-risk premiums repriced</article>}
    </CitationNavContext.Provider>
  )
}

describe('useCitationNavigation', () => {
  it('switches to the sources tab and scrolls to the cited row', async () => {
    render(<TabbedPage />)
    expect(screen.getByText('tab:report')).toBeTruthy()

    fireEvent.click(citation('s04'))

    expect(await screen.findByText('tab:sources')).toBeTruthy()
    const target = document.getElementById('src-s04')
    expect(target?.classList.contains('citation-target')).toBe(true)
    expect(Element.prototype.scrollIntoView).toHaveBeenCalled()
  })
})
