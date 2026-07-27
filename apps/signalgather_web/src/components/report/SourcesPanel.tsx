import { useMemo, useState } from 'react'
import type { NewsArtifact, SourceRef } from '../../lib/types'
import { SourceCard } from '../widgets/SourceCard'
import { Card, EmptyState, SectionHeading, cx } from '../primitives'

type SortKey = 'relevance' | 'recency'

/**
 * Every source behind the report, with the scores that decided its rank.
 *
 * Ordered by relevance by default because that is the order the agent numbered
 * them in (`s01` is the strongest), which keeps citation ids and reading order
 * aligned.
 */
export function SourcesPanel({ news }: { news: NewsArtifact | null }) {
  const [sort, setSort] = useState<SortKey>('relevance')
  const [officialOnly, setOfficialOnly] = useState(false)

  const sources = useMemo(() => {
    const list = [...(news?.sources ?? [])]
    const filtered = officialOnly
      ? list.filter((s) => s.source_class === 'primary_official')
      : list
    return filtered.sort(comparator(sort))
  }, [news, sort, officialOnly])

  const total = news?.sources?.length ?? 0

  if (!news) {
    return (
      <Card>
        <SectionHeading>Sources</SectionHeading>
        <p className="px-4 py-6 text-sm text-ink-muted">
          <code className="font-mono text-xs">news.json</code> is not on disk for this run.
        </p>
      </Card>
    )
  }

  return (
    <Card>
      <SectionHeading
        aside={
          <div className="flex flex-wrap items-center gap-3 text-xs">
            <label className="flex items-center gap-1.5 text-ink-muted">
              <input
                type="checkbox"
                checked={officialOnly}
                onChange={(e) => setOfficialOnly(e.target.checked)}
                className="accent-accent"
              />
              Official only
            </label>
            <div className="flex gap-1">
              <SortTab active={sort === 'relevance'} onClick={() => setSort('relevance')}>
                Relevance
              </SortTab>
              <SortTab active={sort === 'recency'} onClick={() => setSort('recency')}>
                Newest
              </SortTab>
            </div>
          </div>
        }
      >
        Sources ({sources.length}
        {sources.length !== total ? ` of ${total}` : ''})
      </SectionHeading>

      <div className="space-y-2 px-4 py-4">
        {sources.length === 0 ? (
          <EmptyState title={officialOnly ? 'No official sources in this run' : 'No sources'}>
            {officialOnly
              ? 'Clear the filter to see every source the agent kept.'
              : 'The search returned nothing that passed the relevance floor.'}
          </EmptyState>
        ) : (
          sources.map((source) => <SourceCard key={source.id} source={source} />)
        )}
      </div>

      <SearchBudget news={news} />
    </Card>
  )
}

function comparator(sort: SortKey) {
  return (a: SourceRef, b: SourceRef) => {
    if (sort === 'relevance') return (b.relevance_score ?? 0) - (a.relevance_score ?? 0)
    const at = a.published_at ? Date.parse(a.published_at) : 0
    const bt = b.published_at ? Date.parse(b.published_at) : 0
    return (Number.isNaN(bt) ? 0 : bt) - (Number.isNaN(at) ? 0 : at)
  }
}

function SortTab({
  active,
  onClick,
  children,
}: {
  active: boolean
  onClick: () => void
  children: React.ReactNode
}) {
  return (
    <button
      onClick={onClick}
      aria-pressed={active}
      className={cx(
        'rounded-md px-2 py-0.5 font-medium transition-colors',
        active ? 'bg-accent/15 text-accent' : 'text-ink-muted hover:text-ink',
      )}
    >
      {children}
    </button>
  )
}

/** What the run cost in search terms — how much of the plan actually executed. */
function SearchBudget({ news }: { news: NewsArtifact }) {
  const budget = news.search_budget_used
  const drops = news.drops
  if (!budget && !drops) return null

  const parts = [
    budget?.queries_executed !== undefined && `${budget.queries_executed} queries executed`,
    budget?.web_searches !== undefined && `${budget.web_searches} searches`,
    budget?.web_fetches !== undefined && `${budget.web_fetches} fetches`,
    drops?.deduped ? `${drops.deduped} deduped` : null,
    drops?.low_relevance ? `${drops.low_relevance} below relevance floor` : null,
    drops?.off_topic ? `${drops.off_topic} off topic` : null,
  ].filter(Boolean)

  if (parts.length === 0) return null
  return (
    <p className="border-t border-line px-4 py-2.5 text-xs text-ink-faint">{parts.join(' · ')}</p>
  )
}
