import { useCallback, useEffect, useState } from 'react'
import { ApiError, getDelta, getDeltaNews, getDeltaReportMarkdown } from '../../lib/api'
import { absoluteTime, formatDuration, formatUsd, relativeTime } from '../../lib/format'
import type { DeltaArtifact, DeltaSummary, NewsArtifact } from '../../lib/types'
import { ArtifactMarkdown } from '../ArtifactMarkdown'
import { SourceCard } from '../widgets/SourceCard'
import { SourceMixNote } from '../report/SourceMixNote'
import { ThesisBadge } from '../report/ThesisBadge'
import { Card, EmptyState, ErrorNote, SectionHeading, Skeleton, cx } from '../primitives'

/**
 * "What's new since I last looked" (16c).
 *
 * Each refresh cycle is a row; opening one lazily loads its artifacts. Cycles
 * that found nothing are kept visible rather than filtered out — knowing the
 * system looked and found nothing is itself the answer a monitored topic owes
 * the user.
 */
export function DeltaTimeline({
  topicId,
  deltas,
  loading,
}: {
  topicId: string
  deltas: DeltaSummary[]
  loading: boolean
}) {
  const [openSeq, setOpenSeq] = useState<number | null>(null)

  if (loading && deltas.length === 0) {
    return (
      <Card className="p-5">
        <Skeleton lines={3} />
      </Card>
    )
  }

  return (
    <Card>
      <SectionHeading
        aside={
          deltas.length > 0 ? (
            <span className="text-xs text-ink-faint">{deltas.length} cycles</span>
          ) : undefined
        }
      >
        Refresh history
      </SectionHeading>

      {deltas.length === 0 ? (
        <div className="px-4 py-6">
          <EmptyState title="No refresh cycles yet">
            Once monitoring runs — on a schedule or via Refresh now — each cycle appears here with
            what it found.
          </EmptyState>
        </div>
      ) : (
        <ol className="divide-y divide-line">
          {deltas.map((delta) => (
            <DeltaRow
              key={delta.seq}
              topicId={topicId}
              delta={delta}
              open={openSeq === delta.seq}
              onToggle={() => setOpenSeq(openSeq === delta.seq ? null : delta.seq)}
            />
          ))}
        </ol>
      )}
    </Card>
  )
}

function DeltaRow({
  topicId,
  delta,
  open,
  onToggle,
}: {
  topicId: string
  delta: DeltaSummary
  open: boolean
  onToggle: () => void
}) {
  const found = delta.new_sources_count ?? 0
  const failed = delta.status === 'failed' || Boolean(delta.error)

  return (
    <li>
      <button
        onClick={onToggle}
        aria-expanded={open}
        className="flex w-full flex-wrap items-center justify-between gap-3 px-4 py-3 text-left hover:bg-surface-sunken"
      >
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2">
            <span className="font-mono text-xs text-ink-faint">#{delta.seq}</span>
            <span
              className={cx(
                'rounded-full border px-2 py-0.5 text-xs font-medium',
                failed
                  ? 'border-danger/50 bg-danger/10 text-danger'
                  : found > 0
                    ? 'border-positive/50 bg-positive/10 text-positive'
                    : 'border-line bg-surface-sunken text-ink-faint',
              )}
            >
              {failed ? 'Failed' : found > 0 ? `${found} new` : 'Nothing new'}
            </span>
            <span
              className="text-xs text-ink-faint"
              title={absoluteTime(delta.created_at)}
            >
              {relativeTime(delta.created_at)}
            </span>
          </div>
          {delta.error ? (
            <p className="mt-1 text-xs text-danger">{delta.error}</p>
          ) : delta.summary_md ? (
            <p className="mt-1 line-clamp-2 text-xs text-ink-muted">
              {delta.summary_md.replace(/[#*`>]/g, '').trim()}
            </p>
          ) : null}
        </div>
        <span className="shrink-0 text-xs text-ink-faint">
          {[
            delta.queries_executed !== null ? `${delta.queries_executed}q` : null,
            formatDuration(delta.duration_ms),
            formatUsd(delta.total_cost_usd),
          ]
            .filter(Boolean)
            .join(' · ')}
        </span>
      </button>

      {open && <DeltaDetail topicId={topicId} seq={delta.seq} />}
    </li>
  )
}

/** Artifacts load only when a cycle is opened — never for the whole list. */
function DeltaDetail({ topicId, seq }: { topicId: string; seq: number }) {
  const [delta, setDelta] = useState<DeltaArtifact | null>(null)
  const [news, setNews] = useState<NewsArtifact | null>(null)
  const [markdown, setMarkdown] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [attempt, setAttempt] = useState(0)

  const retry = useCallback(() => setAttempt((n) => n + 1), [])

  useEffect(() => {
    let cancelled = false
    Promise.all([
      getDelta(topicId, seq),
      getDeltaNews(topicId, seq),
      getDeltaReportMarkdown(topicId, seq),
    ])
      .then(([d, n, md]) => {
        if (cancelled) return
        setDelta(d)
        setNews(n)
        setMarkdown(md)
        setError(null)
      })
      .catch((err: unknown) => {
        if (!cancelled) setError(err instanceof ApiError ? err.detail : String(err))
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [topicId, seq, attempt])

  if (loading) {
    return (
      <div className="border-t border-line px-4 py-4">
        <Skeleton lines={3} />
      </div>
    )
  }

  if (error) {
    return (
      <div className="border-t border-line px-4 py-4">
        <ErrorNote onRetry={retry}>{error}</ErrorNote>
      </div>
    )
  }

  const newSourceIds = new Set((delta?.new_sources ?? []).map((id) => id.toLowerCase()))
  const newSources = (news?.sources ?? []).filter(
    (source) => newSourceIds.size === 0 || newSourceIds.has(source.id.toLowerCase()),
  )

  return (
    <div className="space-y-4 border-t border-line bg-surface-sunken/40 px-4 py-4">
      {delta?.thesis_status && (
        <div className="flex flex-wrap items-center gap-2">
          <ThesisBadge status={delta.thesis_status} />
          {delta.trigger_terms_hit?.map((term) => (
            <span
              key={term}
              className="rounded-full border border-warning/40 bg-warning/10 px-2 py-0.5 text-xs text-warning"
              title="Monitoring trigger term matched"
            >
              {term}
            </span>
          ))}
        </div>
      )}

      <SourceMixNote sources={news?.sources} />

      {(delta?.summary_md || markdown) && (
        <ArtifactMarkdown source={markdown ?? delta?.summary_md ?? ''} sources={news?.sources} />
      )}

      {delta?.key_changes?.length ? (
        <div>
          <p className="mb-1.5 text-xs font-medium tracking-wide text-ink-faint uppercase">
            Key changes
          </p>
          <ul className="space-y-1.5">
            {delta.key_changes.map((change, index) => (
              <li key={index} className="text-sm text-ink-muted">
                {change.finding}
                {change.source_ids?.length ? (
                  <span className="ml-1 font-mono text-xs text-ink-faint">
                    [{change.source_ids.join(', ')}]
                  </span>
                ) : null}
              </li>
            ))}
          </ul>
        </div>
      ) : null}

      {newSources.length > 0 ? (
        <div>
          <p className="mb-1.5 text-xs font-medium tracking-wide text-ink-faint uppercase">
            New sources ({newSources.length})
          </p>
          <div className="space-y-2">
            {newSources.map((source) => (
              <SourceCard key={source.id} source={source} compact />
            ))}
          </div>
        </div>
      ) : (
        <p className="text-sm text-ink-faint">
          This cycle found no genuinely new sources.
        </p>
      )}
    </div>
  )
}
