import { useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { absoluteTime, relativeTime } from '../lib/format'
import {
  getPublicDelta,
  getPublicDeltaNews,
  getPublicDeltaReportMarkdown,
} from '../lib/publicApi'
import { usePublicTopic } from '../lib/usePublicTopic'
import { useAuth } from '../lib/useAuth'
import type { PlannedQuery } from '../lib/types'
import { Markdown } from '../components/Markdown'
import { QueryTable } from '../components/QueryTable'
import { StateBadge } from '../components/StateBadge'
import { ReportView } from '../components/report/ReportView'
import { SourcesPanel } from '../components/report/SourcesPanel'
import { DeltaTimeline } from '../components/monitor/DeltaTimeline'
import type { DeltaLoaders } from '../components/monitor/DeltaTimeline'
import { Card, EmptyState, ErrorNote, SectionHeading, Skeleton, cx } from '../components/primitives'

type Tab = 'report' | 'sources' | 'plan' | 'history'

const PUBLIC_LOADERS: DeltaLoaders = {
  getDelta: getPublicDelta,
  getDeltaNews: getPublicDeltaNews,
  getDeltaReportMarkdown: getPublicDeltaReportMarkdown,
}

/**
 * A shared topic, as anyone sees it (#40) — including someone with no account.
 *
 * This page renders the same report, sources and plan components as the owner's
 * workspace, minus every control: no proceed/cancel, no monitoring, no refresh,
 * no activity stream. That is not only a styling choice — the client it reads
 * through (`publicApi.ts`) has no write call to make, and the server's public
 * router has no write route to answer, so there is nothing here that can cost
 * anybody anything.
 */
export function PublicTopicPage() {
  const { topicId = '' } = useParams()
  const { user } = useAuth()
  const shared = usePublicTopic(topicId)
  const [chosen, setChosen] = useState<Tab | null>(null)

  const tabs = useMemo<{ id: Tab; label: string }[]>(() => {
    const entries: { id: Tab; label: string }[] = []
    if (shared.report || shared.reportMarkdown) entries.push({ id: 'report', label: 'Report' })
    if (shared.news?.sources?.length) entries.push({ id: 'sources', label: 'Sources' })
    if (shared.introMarkdown || shared.intro || shared.parsed) {
      entries.push({ id: 'plan', label: 'Plan' })
    }
    if (shared.deltas.length) entries.push({ id: 'history', label: 'Updates' })
    return entries
  }, [shared])

  // Which sections exist depends on what was published, so a remembered choice
  // is only honoured while it still points at something.
  const tab = chosen && tabs.some((entry) => entry.id === chosen) ? chosen : tabs[0]?.id

  if (shared.error) {
    return (
      <div className="mx-auto w-full max-w-4xl px-4 py-12 sm:px-6">
        <ErrorNote>{shared.error}</ErrorNote>
        <p className="mt-4 text-sm text-ink-muted">
          <Link to="/shared" className="text-accent underline">
            Browse shared topics
          </Link>
        </p>
      </div>
    )
  }

  if (shared.loading && !shared.topic) {
    return (
      <div className="mx-auto w-full max-w-4xl px-4 py-10 sm:px-6">
        <Card className="p-6">
          <Skeleton lines={4} />
        </Card>
      </div>
    )
  }

  const topic = shared.topic
  if (!topic) return null

  return (
    <div className="mx-auto w-full max-w-4xl px-4 py-6 sm:px-6">
      <header>
        <Link to="/shared" className="text-xs text-ink-muted hover:text-ink">
          ← Shared topics
        </Link>
        <div className="mt-2 flex flex-wrap items-start justify-between gap-3">
          <h1 className="min-w-0 flex-1 text-lg font-semibold tracking-tight text-ink">
            {topic.topic}
          </h1>
          <StateBadge state={topic.state} />
        </div>
        <p className="mt-2 text-xs text-ink-faint">
          <span className="rounded-full border border-line px-2 py-0.5">Read-only</span>{' '}
          {topic.published_at ? (
            <span title={absoluteTime(topic.published_at)}>
              Shared {relativeTime(topic.published_at)} — this is the state of the research at
              that moment.
            </span>
          ) : (
            <span>This is a shared snapshot of someone else&apos;s research.</span>
          )}
        </p>
      </header>

      {shared.loading && (
        <div className="mt-5">
          <Card className="p-5">
            <Skeleton lines={4} />
          </Card>
        </div>
      )}

      {!shared.loading && tabs.length === 0 && (
        <div className="mt-5">
          <EmptyState title="Nothing to show yet">
            This topic was shared before it produced any readable output.
          </EmptyState>
        </div>
      )}

      {!shared.loading && tabs.length > 0 && (
        <div className="mt-5 space-y-5">
          {tabs.length > 1 && (
            <nav className="flex flex-wrap gap-1" role="tablist" aria-label="Sections">
              {tabs.map((entry) => (
                <button
                  key={entry.id}
                  role="tab"
                  aria-selected={tab === entry.id}
                  onClick={() => setChosen(entry.id)}
                  className={cx(
                    'rounded-lg px-3 py-1.5 text-sm font-medium transition-colors',
                    tab === entry.id
                      ? 'bg-accent/15 text-accent'
                      : 'text-ink-muted hover:bg-surface-raised hover:text-ink',
                  )}
                >
                  {entry.label}
                </button>
              ))}
            </nav>
          )}

          {tab === 'report' && (
            <ReportView
              report={shared.report}
              reportMarkdown={shared.reportMarkdown}
              news={shared.news}
              loading={false}
            />
          )}

          {tab === 'sources' && <SourcesPanel news={shared.news} />}

          {tab === 'plan' && (
            <PublicPlan
              introMarkdown={shared.introMarkdown}
              headline={shared.intro?.headline}
              understanding={shared.intro?.understanding}
              queries={shared.parsed?.queries ?? []}
            />
          )}

          {tab === 'history' && (
            <DeltaTimeline
              topicId={topic.id}
              deltas={shared.deltas}
              loading={false}
              loaders={PUBLIC_LOADERS}
              title="Updates while this topic was monitored"
            />
          )}
        </div>
      )}

      {!user && (
        <footer className="mt-8 rounded-xl border border-line bg-surface-raised px-4 py-3 text-sm text-ink-muted">
          You are reading a shared topic. To research your own,{' '}
          <Link to="/" className="text-accent underline">
            sign in
          </Link>
          .
        </footer>
      )}
    </div>
  )
}

/** The plan, without the review gate: what was asked and what was searched. */
function PublicPlan({
  introMarkdown,
  headline,
  understanding,
  queries,
}: {
  introMarkdown: string | null
  headline?: string
  understanding?: string
  queries: PlannedQuery[]
}) {
  return (
    <div className="space-y-5">
      <Card>
        <SectionHeading>Brief</SectionHeading>
        <div className="space-y-3 px-4 py-4">
          {introMarkdown ? (
            <Markdown source={introMarkdown} />
          ) : (
            <>
              {headline && <h2 className="text-base font-semibold text-ink">{headline}</h2>}
              <p className="text-sm text-ink-muted">
                {understanding ?? 'No brief was shared with this topic.'}
              </p>
            </>
          )}
        </div>
      </Card>

      {queries.length > 0 && (
        <Card>
          <SectionHeading
            aside={<span className="text-xs text-ink-faint">{queries.length} queries</span>}
          >
            Research plan
          </SectionHeading>
          <QueryTable queries={queries} />
        </Card>
      )}
    </div>
  )
}
