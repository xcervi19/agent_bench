import { sourceAnchorId } from '../../lib/citations'
import { absoluteTime, relativeTime } from '../../lib/format'
import type { SourceRef } from '../../lib/widgets/types'
import { cx } from '../primitives'

const CLASS_LABELS: Record<string, string> = {
  primary_official: 'official',
  specialist_outlet: 'specialist',
  aggregator: 'aggregator',
  data_feed: 'data feed',
  blog_or_newsletter: 'blog',
  social: 'social',
  unknown: 'unknown',
}

/** Official sources carry the most weight on a trading desk — make that visible. */
const CLASS_STYLE: Record<string, string> = {
  primary_official: 'border-positive/50 bg-positive/10 text-positive',
  specialist_outlet: 'border-accent/50 bg-accent/10 text-accent',
  social: 'border-warning/50 bg-warning/10 text-warning',
}

export function SourceCard({ source, compact }: { source: SourceRef; compact?: boolean }) {
  const relevance = typeof source.relevance_score === 'number' ? source.relevance_score : null

  return (
    <article
      id={sourceAnchorId(source.id)}
      // scroll-mt clears the sticky top bar when a citation jumps here.
      className="scroll-mt-20 rounded-lg border border-line bg-surface-sunken px-3.5 py-3 target:border-accent"
    >
      <div className="flex flex-wrap items-baseline gap-x-2 gap-y-1">
        <span className="font-mono text-xs text-ink-faint">{source.id}</span>
        {source.url ? (
          <a
            href={source.url}
            target="_blank"
            rel="noopener noreferrer"
            className="min-w-0 flex-1 text-sm font-medium text-ink underline decoration-transparent underline-offset-2 hover:decoration-current"
          >
            {source.title ?? source.url}
          </a>
        ) : (
          <span className="min-w-0 flex-1 text-sm font-medium text-ink">
            {source.title ?? '(untitled source)'}
          </span>
        )}
        {relevance !== null && <RelevanceMeter value={relevance} />}
      </div>

      <div className="mt-1.5 flex flex-wrap items-center gap-x-2.5 gap-y-1 text-xs text-ink-faint">
        {source.publisher && <span className="text-ink-muted">{source.publisher}</span>}
        {source.source_class && (
          <span
            className={cx(
              'rounded-full border px-1.5 py-0.5',
              CLASS_STYLE[source.source_class] ?? 'border-line text-ink-faint',
            )}
          >
            {CLASS_LABELS[source.source_class] ?? source.source_class}
          </span>
        )}
        {source.language && <span className="font-mono">{source.language}</span>}
        {source.published_at && (
          <span title={absoluteTime(source.published_at)}>
            {relativeTime(source.published_at)}
          </span>
        )}
        {source.query_ids?.length ? (
          <span title="Queries that surfaced this source">
            via {source.query_ids.join(', ')}
          </span>
        ) : null}
      </div>

      {!compact && source.snippet && (
        <p className="mt-2 text-xs leading-relaxed text-ink-muted">{source.snippet}</p>
      )}
    </article>
  )
}

function RelevanceMeter({ value }: { value: number }) {
  const pct = Math.round(Math.min(Math.max(value, 0), 1) * 100)
  return (
    <span
      className="flex shrink-0 items-center gap-1.5 text-xs text-ink-faint"
      title={`Relevance ${pct}%`}
    >
      <span className="h-1 w-10 overflow-hidden rounded-full bg-line">
        <span
          className={cx(
            'block h-full rounded-full',
            pct >= 70 ? 'bg-positive' : pct >= 50 ? 'bg-accent' : 'bg-warning',
          )}
          style={{ width: `${pct}%` }}
        />
      </span>
      {pct}
    </span>
  )
}

/** Shown when a widget or citation names a source this run does not have. */
export function MissingSource({ sourceId }: { sourceId: string }) {
  return (
    <p className="rounded-lg border border-dashed border-line px-3.5 py-2.5 text-xs text-ink-faint">
      Source <span className="font-mono">{sourceId}</span> is referenced but not present in this
      run's <code className="font-mono">news.json</code>.
    </p>
  )
}
