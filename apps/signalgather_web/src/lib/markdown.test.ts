import { describe, expect, it } from 'vitest'
import { renderMarkdown } from './markdown'

describe('renderMarkdown', () => {
  it('renders ordinary markdown', () => {
    const html = renderMarkdown('## Understanding\n\n- one\n- two')
    expect(html).toContain('<h2>Understanding</h2>')
    expect(html).toContain('<li>one</li>')
  })

  it('strips script tags from agent-written content', () => {
    const html = renderMarkdown('Hello <script>alert(1)</script> world')
    expect(html).not.toContain('<script')
    expect(html).not.toContain('alert(1)')
  })

  it('strips inline event handlers', () => {
    expect(renderMarkdown('<img src=x onerror="alert(1)">')).not.toContain('onerror')
  })

  it('drops javascript: links but keeps the text', () => {
    const html = renderMarkdown('[click](javascript:alert(1))')
    expect(html).not.toContain('javascript:')
    expect(html).toContain('click')
  })

  it('keeps http links intact for source citations', () => {
    expect(renderMarkdown('[Reuters](https://reuters.com/a)')).toContain(
      'href="https://reuters.com/a"',
    )
  })

  it('unwraps intro.md pseudo-tags while keeping their text', () => {
    const html = renderMarkdown('<EntityChips>NIOC, OPEC</EntityChips>')
    expect(html).not.toContain('EntityChips')
    expect(html).toContain('NIOC, OPEC')
  })

  it('renders tables (gfm) used by the plan brief', () => {
    const html = renderMarkdown('| a | b |\n| --- | --- |\n| 1 | 2 |')
    expect(html).toContain('<table>')
  })
})
