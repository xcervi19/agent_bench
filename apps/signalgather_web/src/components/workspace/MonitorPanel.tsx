import { useState } from 'react'
import { Bell, BellOff, RefreshCw, History } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { Markdown } from '@/components/ui/Markdown'
import { SourcesList } from './SourcesList'
import type { DeltaSummary, MonitorStatus } from '@/lib/types'
import type { NewsArtifact } from '@/lib/types'
import { formatRelativeTime } from '@/lib/utils'
import { cn } from '@/lib/utils'

export function MonitorPanel({
  monitor,
  deltas,
  selectedDelta,
  deltaDetail,
  onEnable,
  onDisable,
  onRefresh,
  onOpenDelta,
  onCloseDelta,
  actionLoading,
  visible,
}: {
  monitor: MonitorStatus | null
  deltas: DeltaSummary[]
  selectedDelta: number | null
  deltaDetail: {
    delta: Record<string, unknown> | null
    news: NewsArtifact | null
    reportMd: string | null
  }
  onEnable: (hours: number) => void
  onDisable: () => void
  onRefresh: () => void
  onOpenDelta: (seq: number) => void
  onCloseDelta: () => void
  actionLoading: string | null
  visible: boolean
}) {
  const [maxAgeHours, setMaxAgeHours] = useState(48)

  if (!visible) return null

  const isActive = monitor?.status === 'active'

  return (
    <div className="rounded-xl border border-border bg-surface-raised">
      <div className="flex items-center justify-between px-4 py-3 border-b border-border">
        <div className="flex items-center gap-2">
          <Bell className="h-4 w-4 text-accent" />
          <h2 className="text-sm font-medium text-text">Monitoring</h2>
          {isActive && (
            <span className="text-xs text-success bg-success/10 px-2 py-0.5 rounded-md border border-success/20">
              Active · {monitor.max_age_hours}h window
            </span>
          )}
        </div>
        <div className="flex gap-2">
          {isActive ? (
            <>
              <Button
                size="sm"
                variant="secondary"
                onClick={onRefresh}
                loading={actionLoading === 'refresh'}
                disabled={monitor.refresh_locked}
              >
                <RefreshCw className={cn('h-3.5 w-3.5', monitor.refresh_locked && 'animate-spin')} />
                Refresh now
              </Button>
              <Button
                size="sm"
                variant="ghost"
                onClick={onDisable}
                loading={actionLoading === 'monitor'}
              >
                <BellOff className="h-3.5 w-3.5" />
                Pause
              </Button>
            </>
          ) : (
            <div className="flex items-center gap-2">
              <select
                value={maxAgeHours}
                onChange={(e) => setMaxAgeHours(Number(e.target.value))}
                className="rounded-lg border border-border bg-surface px-2 py-1.5 text-xs text-text"
              >
                <option value={24}>24h window</option>
                <option value={48}>48h window</option>
                <option value={72}>72h window</option>
                <option value={168}>7d window</option>
              </select>
              <Button
                size="sm"
                onClick={() => onEnable(maxAgeHours)}
                loading={actionLoading === 'monitor'}
              >
                <Bell className="h-3.5 w-3.5" />
                Enable monitoring
              </Button>
            </div>
          )}
        </div>
      </div>

      <div className="p-4">
        {monitor && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4 text-left">
            <Stat label="Refreshes" value={String(monitor.refresh_count)} />
            <Stat
              label="Last refresh"
              value={
                monitor.last_refresh_at
                  ? formatRelativeTime(monitor.last_refresh_at)
                  : 'Never'
              }
            />
            <Stat label="Queries" value={String(monitor.short_term_queries?.length ?? 0)} />
            <Stat
              label="Status"
              value={monitor.refresh_locked ? 'Refreshing…' : monitor.status}
            />
          </div>
        )}

        <div className="flex items-center gap-2 mb-3">
          <History className="h-4 w-4 text-text-muted" />
          <h3 className="text-xs font-medium text-text-muted uppercase tracking-wide">
            Refresh history ({deltas.length})
          </h3>
        </div>

        {deltas.length === 0 ? (
          <p className="text-sm text-text-muted text-center py-6">
            No refresh cycles yet. Enable monitoring and trigger a refresh.
          </p>
        ) : (
          <div className="space-y-2">
            {deltas.map((delta) => (
              <button
                key={delta.seq}
                type="button"
                onClick={() =>
                  selectedDelta === delta.seq ? onCloseDelta() : onOpenDelta(delta.seq)
                }
                className={cn(
                  'w-full rounded-lg border p-3 text-left transition-colors',
                  selectedDelta === delta.seq
                    ? 'border-accent bg-accent/5'
                    : 'border-border bg-surface hover:border-accent/30',
                )}
              >
                <div className="flex items-center justify-between gap-2">
                  <span className="text-sm font-medium text-text">
                    Refresh #{delta.seq}
                  </span>
                  <span
                    className={cn(
                      'text-[10px] px-2 py-0.5 rounded-md border capitalize',
                      delta.status === 'completed'
                        ? 'bg-success/10 text-success border-success/20'
                        : 'bg-danger/10 text-danger border-danger/20',
                    )}
                  >
                    {delta.status}
                  </span>
                </div>
                <div className="mt-1 flex flex-wrap gap-3 text-xs text-text-muted">
                  <span>+{delta.new_sources_count} sources</span>
                  <span>{delta.queries_executed} queries</span>
                  {delta.duration_ms && <span>{Math.round(delta.duration_ms / 1000)}s</span>}
                  <span>{formatRelativeTime(delta.created_at)}</span>
                </div>
                {delta.summary_md && (
                  <p className="mt-1.5 text-xs text-text-muted line-clamp-2">
                    {delta.summary_md}
                  </p>
                )}
              </button>
            ))}
          </div>
        )}

        {selectedDelta !== null && deltaDetail && (
          <div className="mt-4 rounded-lg border border-accent/30 bg-surface p-4 space-y-4">
            <h4 className="text-sm font-medium text-text">Delta #{selectedDelta} detail</h4>
            {deltaDetail.reportMd && <Markdown content={deltaDetail.reportMd} />}
            {deltaDetail.news && (
              <SourcesList
                sources={deltaDetail.news.sources}
                title="New sources"
                compact
              />
            )}
          </div>
        )}
      </div>
    </div>
  )
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg bg-surface-overlay p-2.5">
      <p className="text-[10px] text-text-muted">{label}</p>
      <p className="text-sm font-medium text-text capitalize">{value}</p>
    </div>
  )
}
