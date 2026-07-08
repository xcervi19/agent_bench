import { Link } from 'react-router-dom'
import { ChevronRight, Sparkles } from 'lucide-react'
import { StateBadge } from '@/components/ui/Badge'
import type { TopicSummary } from '@/lib/types'
import { formatRelativeTime, truncate } from '@/lib/utils'
import { hasNewActivity } from '@/lib/storage'
import { cn } from '@/lib/utils'

export function TopicCard({
  topic,
  monitorActive,
  latestDeltaAt,
}: {
  topic: TopicSummary
  monitorActive?: boolean
  latestDeltaAt?: string | null
}) {
  const isNew = hasNewActivity(topic.id, topic.updated_at, latestDeltaAt)

  return (
    <Link
      to={`/topics/${topic.id}`}
      className={cn(
        'group block rounded-xl border border-border bg-surface-raised p-4 transition-all',
        'hover:border-accent/40 hover:bg-surface-overlay',
      )}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0 flex-1 text-left">
          <div className="flex flex-wrap items-center gap-2 mb-1.5">
            <StateBadge state={topic.state} />
            {monitorActive && (
              <span className="inline-flex items-center gap-1 rounded-md bg-success/15 px-2 py-0.5 text-[10px] font-medium text-success border border-success/20">
                <span className="h-1.5 w-1.5 rounded-full bg-success animate-pulse" />
                Monitoring
              </span>
            )}
            {isNew && (
              <span className="inline-flex items-center gap-1 rounded-md bg-accent/15 px-2 py-0.5 text-[10px] font-medium text-accent border border-accent/20">
                <Sparkles className="h-3 w-3" />
                New activity
              </span>
            )}
          </div>
          <p className="text-sm font-medium text-text leading-snug">
            {truncate(topic.topic, 160)}
          </p>
          <p className="mt-1.5 text-xs text-text-muted">
            Updated {formatRelativeTime(topic.updated_at)}
          </p>
        </div>
        <ChevronRight className="h-5 w-5 text-text-muted group-hover:text-accent shrink-0 mt-1 transition-colors" />
      </div>
    </Link>
  )
}
