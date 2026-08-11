import { useCallback, useMemo } from 'react'
import { indexSources, linkCitations } from '../lib/citations'
import { useCitationNav } from '../lib/citationNav'
import { renderMarkdown } from '../lib/markdown'
import { parseArtifact } from '../lib/widgets/parse'
import type { SourceRef } from '../lib/widgets/types'
import { WidgetContext } from './widgets/WidgetContext'
import { WidgetRenderer } from './widgets/registry'
import { cx } from './primitives'

/**
 * The one way agent-written artifacts reach the screen.
 *
 * Pipeline per segment: split prose from widgets → render prose as markdown →
 * sanitize → link `[s01]` citations → render widgets from the registry. Prose
 * and widgets interleave as React siblings, so a widget is a real component and
 * never HTML injected into a markdown blob.
 *
 * Used by the plan brief (`intro.md`), the report (`report.md`), and delta
 * reports — none of which know anything about widget types.
 */
export function ArtifactMarkdown({
  source,
  sources,
  className,
}: {
  source: string
  /** news.json sources, for citation links and source-backed widgets. */
  sources?: SourceRef[]
  className?: string
}) {
  const index = useMemo(() => indexSources(sources), [sources])
  const segments = useMemo(() => parseArtifact(source), [source])

  const rendered = useMemo(
    () =>
      segments.map((segment) =>
        segment.kind === 'markdown'
          ? { kind: 'html' as const, html: linkCitations(renderMarkdown(segment.text), {
              sources: index,
            }) }
          : { kind: 'widget' as const, widget: segment.widget },
      ),
    [segments, index],
  )

  // Citations are plain anchors in the sanitized HTML, so the click is caught by
  // delegation rather than per-link handlers. A citation whose card is already
  // rendered here (a `news-card` widget) keeps the native jump; only one whose
  // anchor is absent — it lives on the Sources tab — is handed to the navigator.
  const navigateToSource = useCitationNav()
  const onClick = useCallback(
    (event: React.MouseEvent<HTMLDivElement>) => {
      if (!navigateToSource) return
      if (event.defaultPrevented || event.metaKey || event.ctrlKey || event.shiftKey) return
      const anchor = (event.target as HTMLElement).closest?.('a.citation')
      const href = anchor?.getAttribute('href')
      if (!href?.startsWith('#src-')) return
      if (document.getElementById(href.slice(1))) return
      event.preventDefault()
      navigateToSource(href.slice('#src-'.length))
    },
    [navigateToSource],
  )

  return (
    <WidgetContext.Provider value={{ sources: index }}>
      {/* Delegation, not a widget: the click target is always a real <a>, so
          keyboard activation bubbles here the same way a pointer click does. */}
      <div className={cx('text-sm text-ink', className)} onClick={onClick}>
        {rendered.map((item, position) =>
          item.kind === 'html' ? (
            <div
              key={position}
              className="prose-artifact"
              dangerouslySetInnerHTML={{ __html: item.html }}
            />
          ) : (
            <WidgetRenderer key={position} widget={item.widget} />
          ),
        )}
      </div>
    </WidgetContext.Provider>
  )
}
