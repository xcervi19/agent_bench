import { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { absoluteTime, elapsed, relativeTime } from '../lib/format'
import { markTopicSeen } from '../lib/lastSeen'
import { useTopicStream } from '../lib/useTopicStream'
import type { TopicDetail } from '../lib/types'
import { ActivityFeed } from '../components/ActivityFeed'
import { PlanReview } from '../components/PlanReview'
import { StateBadge } from '../components/StateBadge'
import { ReportView } from '../components/report/ReportView'
import { SourcesPanel } from '../components/report/SourcesPanel'
import { MonitorPanel } from '../components/monitor/MonitorPanel'
import { DeltaTimeline } from '../components/monitor/DeltaTimeline'
import { PublishedBanner, SharePanel } from '../components/SharePanel'
import { Card, ErrorNote, Skeleton, cx } from '../components/primitives'

type Tab = 'plan' | 'report' | 'sources' | 'monitor' | 'share'

/**
 * Single-topic command center: state, live activity, and one section per
 * pipeline stage. The section that matters right now is selected for you — a
 * topic mid-plan opens on the gate, a finished one opens on the report — but
 * every stage stays reachable, because "what did it plan?" is a fair question
 * to ask about a finished report.
 */
export function TopicWorkspacePage() {
  const { topicId = '' } = useParams()
  const stream = useTopicStream(topicId)
  const { topic, events, status, statusDetail } = stream

  const suggested = suggestedTab(topic)
  const [chosen, setChosen] = useState<Tab | null>(null)
  const [seenFor, setSeenFor] = useState<string | null>(null)

  // Follow the pipeline until the user picks a section themselves; then stop
  // moving the ground under them. Resets when the topic changes.
  if (seenFor !== topicId) {
    setSeenFor(topicId)
    setChosen(null)
  }
  const tab = chosen ?? suggested

  const tabs = useMemo(() => visibleTabs(topic), [topic])

  // Record the visit on the way out, not on arrival: a topic that keeps working
  // while you watch it should not come back flagged as unseen.
  useEffect(() => {
    if (!topicId) return
    return () => markTopicSeen(topicId)
  }, [topicId])

  if (stream.loadError && !topic) {
    return (
      <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
        <ErrorNote>{stream.loadError}</ErrorNote>
        <p className="mt-4 text-sm text-ink-muted">
          <Link to="/" className="text-accent underline">
            Back to your topics
          </Link>
        </p>
      </div>
    )
  }

  if (!topic) {
    return (
      <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
        <Card className="p-6">
          <Skeleton lines={3} />
        </Card>
      </div>
    )
  }

  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-6 sm:px-6">
      <StatusBar topic={topic} />

      {topic.is_public && (
        <div className="mt-4">
          <PublishedBanner topic={topic} />
        </div>
      )}

      {topic.error && (
        <div className="mt-4">
          <ErrorNote>{topic.error}</ErrorNote>
        </div>
      )}

      <div className="mt-5 grid min-h-0 gap-5 lg:grid-cols-[minmax(0,1.55fr)_minmax(0,1fr)]">
        <div className="min-w-0 space-y-5">
          <nav className="flex flex-wrap gap-1" role="tablist" aria-label="Topic sections">
            {tabs.map((entry) => (
              <TabButton
                key={entry.id}
                active={tab === entry.id}
                onClick={() => setChosen(entry.id)}
                badge={entry.id === 'monitor' ? stream.deltas.length || undefined : undefined}
              >
                {entry.label}
              </TabButton>
            ))}
          </nav>

          {tab === 'plan' && (
            <PlanReview
              topic={topic}
              intro={stream.intro}
              introMarkdown={stream.introMarkdown}
              parsed={stream.parsed}
              loading={stream.loading.plan}
              onDecision={() => void stream.refresh(['plan'])}
            />
          )}

          {tab === 'report' && (
            <ReportView
              report={stream.report}
              reportMarkdown={stream.reportMarkdown}
              news={stream.news}
              loading={stream.loading.report}
            />
          )}

          {tab === 'sources' && <SourcesPanel news={stream.news} />}

          {tab === 'monitor' && (
            <div className="space-y-5">
              <MonitorPanel
                topic={topic}
                monitor={stream.monitor}
                loading={stream.loading.monitor}
                onChanged={() => void stream.refresh(['monitor', 'deltas'])}
              />
              <DeltaTimeline
                topicId={topic.id}
                deltas={stream.deltas}
                loading={stream.loading.deltas}
              />
            </div>
          )}

          {tab === 'share' && (
            <SharePanel topic={topic} onChanged={() => void stream.refresh([])} />
          )}
        </div>

        <div className="min-w-0">
          <ActivityFeed events={events} status={status} statusDetail={statusDetail} />
        </div>
      </div>
    </div>
  )
}

const ALL_TABS: { id: Tab; label: string }[] = [
  { id: 'plan', label: 'Plan' },
  { id: 'report', label: 'Report' },
  { id: 'sources', label: 'Sources' },
  { id: 'monitor', label: 'Monitoring' },
  { id: 'share', label: 'Share' },
]

/** Report/Sources/Monitoring only appear once the pipeline can back them. */
function visibleTabs(topic: TopicDetail | null): { id: Tab; label: string }[] {
  if (!topic) return ALL_TABS.slice(0, 1)
  const hasReport = Boolean(topic.deliver_run_id)
  return ALL_TABS.filter((entry) => {
    if (entry.id === 'plan') return true
    if (entry.id === 'monitor') return topic.state === 'reported'
    // Sharing is offered on a finished topic, and stays reachable while shared
    // so the way to undo it is where the way to do it was.
    if (entry.id === 'share') return topic.state === 'reported' || topic.is_public
    return hasReport
  })
}

function suggestedTab(topic: TopicDetail | null): Tab {
  if (!topic) return 'plan'
  if (topic.state === 'reported') return 'report'
  return 'plan'
}

function TabButton({
  active,
  onClick,
  badge,
  children,
}: {
  active: boolean
  onClick: () => void
  badge?: number
  children: React.ReactNode
}) {
  return (
    <button
      role="tab"
      aria-selected={active}
      onClick={onClick}
      className={cx(
        'flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-sm font-medium transition-colors',
        active
          ? 'bg-accent/15 text-accent'
          : 'text-ink-muted hover:bg-surface-raised hover:text-ink',
      )}
    >
      {children}
      {badge !== undefined && (
        <span className="rounded-full bg-line px-1.5 text-xs text-ink-muted">{badge}</span>
      )}
    </button>
  )
}

function StatusBar({ topic }: { topic: TopicDetail }) {
  const [, tick] = useState(0)
  const running = topic.state === 'planning' || topic.state === 'delivering'

  // Elapsed time is only interesting while work is happening; re-render each
  // second in that case and never otherwise.
  useEffect(() => {
    if (!running) return
    const id = setInterval(() => tick((n) => n + 1), 1000)
    return () => clearInterval(id)
  }, [running])

  return (
    <header>
      <Link to="/" className="text-xs text-ink-muted hover:text-ink">
        ← All topics
      </Link>
      <div className="mt-2 flex flex-wrap items-start justify-between gap-3">
        <TopicHeading topic={topic.topic} />
        <StateBadge state={topic.state} />
      </div>
      <dl className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-ink-faint">
        <Meta
          label="Started"
          value={relativeTime(topic.created_at)}
          title={absoluteTime(topic.created_at)}
        />
        {running ? (
          <Meta label="Running for" value={elapsed(topic.created_at)} />
        ) : (
          <Meta
            label="Last activity"
            value={relativeTime(topic.updated_at)}
            title={absoluteTime(topic.updated_at)}
          />
        )}
        <Meta label="Events" value={String(topic.last_event_seq)} />
      </dl>
    </header>
  )
}

const COLLAPSED_TOPIC_CHARS = 180

function TopicHeading({ topic }: { topic: string }) {
  const [expanded, setExpanded] = useState(false)
  const isLong = topic.length > COLLAPSED_TOPIC_CHARS

  return (
    <div className="min-w-0 flex-1">
      <h1
        className={cx(
          'text-lg font-semibold tracking-tight text-ink',
          isLong && !expanded && 'line-clamp-2',
        )}
      >
        {topic}
      </h1>
      {isLong && (
        <button
          onClick={() => setExpanded(!expanded)}
          aria-expanded={expanded}
          className="mt-1 text-xs text-accent hover:underline"
        >
          {expanded ? 'Show less' : 'Show full brief'}
        </button>
      )}
    </div>
  )
}

function Meta({ label, value, title }: { label: string; value: string; title?: string }) {
  return (
    <div className="flex gap-1" title={title}>
      <dt>{label}</dt>
      <dd className="text-ink-muted">{value}</dd>
    </div>
  )
}
