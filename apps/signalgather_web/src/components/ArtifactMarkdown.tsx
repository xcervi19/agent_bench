import { useMemo } from 'react'
import { indexSources, linkCitations } from '../lib/citations'
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

  return (
    <WidgetContext.Provider value={{ sources: index }}>
      <div className={cx('text-sm text-ink', className)}>
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
