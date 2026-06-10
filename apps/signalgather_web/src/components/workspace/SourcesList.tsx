import { ExternalLink } from 'lucide-react'
import type { NewsSource } from '@/lib/types'
import { formatRelativeTime, scorePercent } from '@/lib/utils'

export function SourcesList({
  sources,
  title = 'Sources',
  compact = false,
}: {
  sources: NewsSource[]
  title?: string
  compact?: boolean
}) {
  if (sources.length === 0) return null

  const sorted = [...sources].sort(
    (a, b) => (b.relevance_score ?? 0) - (a.relevance_score ?? 0),
  )

  return (
    <div className="space-y-2">
      <h3 className="text-xs font-medium text-text-muted uppercase tracking-wide">
        {title} ({sources.length})
      </h3>
      <div className="space-y-2">
        {sorted.map((source) => (
          <a
            key={source.id}
            href={source.url}
            target="_blank"
            rel="noopener noreferrer"
            className="block rounded-lg border border-border bg-surface p-3 hover:border-accent/40 transition-colors group"
          >
            <div className="flex items-start justify-between gap-2">
              <div className="min-w-0 flex-1 text-left">
                <div className="flex items-center gap-2 mb-0.5">
                  <span className="font-mono text-[10px] text-text-muted">{source.id}</span>
                  {source.publisher && (
                    <span className="text-[10px] text-accent">{source.publisher}</span>
                  )}
                  {source.relevance_score !== undefined && (
                    <span className="text-[10px] text-success">
                      {scorePercent(source.relevance_score)} relevant
                    </span>
                  )}
                </div>
                <p className="text-sm font-medium text-text group-hover:text-accent transition-colors line-clamp-2">
                  {source.title}
                </p>
                {!compact && source.snippet && (
                  <p className="mt-1 text-xs text-text-muted line-clamp-2">{source.snippet}</p>
                )}
                <div className="mt-1 flex flex-wrap gap-2 text-[10px] text-text-muted">
                  {source.published_at && (
                    <span>{formatRelativeTime(source.published_at)}</span>
                  )}
                  {source.language && <span>{source.language.toUpperCase()}</span>}
                  {source.source_class && <span>{source.source_class}</span>}
                </div>
              </div>
              <ExternalLink className="h-4 w-4 text-text-muted group-hover:text-accent shrink-0" />
            </div>
          </a>
        ))}
      </div>
    </div>
  )
}
