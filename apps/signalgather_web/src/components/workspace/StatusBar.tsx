import { ArrowLeft, Wifi, WifiOff } from 'lucide-react'
import { Link } from 'react-router-dom'
import { StateBadge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import type { TopicDetail } from '@/lib/types'
import type { SseStatus } from '@/lib/sse'
import { elapsedSince } from '@/lib/utils'
import { cn } from '@/lib/utils'

export function StatusBar({
  topic,
  sseStatus,
  onProceed,
  onCancel,
  actionLoading,
}: {
  topic: TopicDetail
  sseStatus: SseStatus
  onProceed: () => void
  onCancel: () => void
  actionLoading: string | null
}) {
  const canProceed = topic.available_actions.includes('proceed')
  const canCancel = topic.available_actions.includes('cancel')

  return (
    <div className="rounded-xl border border-border bg-surface-raised p-4">
      <div className="flex flex-col lg:flex-row lg:items-center gap-4">
        <div className="flex items-start gap-3 min-w-0 flex-1">
          <Link
            to="/"
            className="mt-0.5 rounded-lg p-1.5 text-text-muted hover:text-text hover:bg-surface-overlay transition-colors"
          >
            <ArrowLeft className="h-4 w-4" />
          </Link>
          <div className="min-w-0 flex-1 text-left">
            <div className="flex flex-wrap items-center gap-2 mb-1">
              <StateBadge state={topic.state} />
              <SseIndicator status={sseStatus} />
              <span className="text-xs text-text-muted">
                Running {elapsedSince(topic.updated_at)}
              </span>
            </div>
            <h1 className="text-base font-medium text-text leading-snug">{topic.topic}</h1>
            {topic.error && (
              <p className="mt-1 text-xs text-danger">{topic.error}</p>
            )}
          </div>
        </div>

        <div className="flex flex-wrap gap-2 shrink-0">
          {canProceed && (
            <Button onClick={onProceed} loading={actionLoading === 'proceed'}>
              Proceed with Plan
            </Button>
          )}
          {canCancel && (
            <Button
              variant="danger"
              onClick={onCancel}
              loading={actionLoading === 'cancel'}
            >
              Cancel
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}

function SseIndicator({ status }: { status: SseStatus }) {
  const connected = status === 'connected'
  const reconnecting = status === 'reconnecting' || status === 'connecting'

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1 rounded-md px-2 py-0.5 text-[10px] font-medium border',
        connected && 'bg-success/10 text-success border-success/20',
        reconnecting && 'bg-warning/10 text-warning border-warning/20',
        !connected && !reconnecting && 'bg-surface-overlay text-text-muted border-border',
      )}
    >
      {connected ? <Wifi className="h-3 w-3" /> : <WifiOff className="h-3 w-3" />}
      {status === 'connected' && 'Live'}
      {status === 'connecting' && 'Connecting'}
      {status === 'reconnecting' && 'Reconnecting'}
      {status === 'disconnected' && 'Offline'}
      {status === 'error' && 'Stream error'}
    </span>
  )
}
