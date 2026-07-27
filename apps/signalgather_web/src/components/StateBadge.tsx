import type { StreamStatus } from '../lib/sse'
import type { TopicState } from '../lib/types'
import { Spinner, cx } from './primitives'

interface StateStyle {
  label: string
  className: string
  /** Pipeline is working — show motion. */
  active?: boolean
}

const STATES: Record<TopicState, StateStyle> = {
  planning: { label: 'Planning', className: 'text-accent border-accent/50 bg-accent/10', active: true },
  planned_awaiting_review: {
    label: 'Awaiting your review',
    className: 'text-warning border-warning/50 bg-warning/10',
  },
  delivering: {
    label: 'Researching',
    className: 'text-accent border-accent/50 bg-accent/10',
    active: true,
  },
  reported: { label: 'Report ready', className: 'text-positive border-positive/50 bg-positive/10' },
  failed: { label: 'Failed', className: 'text-danger border-danger/50 bg-danger/10' },
  cancelled: { label: 'Cancelled', className: 'text-ink-faint border-line bg-surface-sunken' },
}

const FALLBACK: StateStyle = { label: 'Unknown', className: 'text-ink-faint border-line' }

export function StateBadge({ state, className }: { state: TopicState | string; className?: string }) {
  const style = STATES[state as TopicState] ?? { ...FALLBACK, label: state }
  return (
    <span
      className={cx(
        'inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-medium whitespace-nowrap',
        style.className,
        className,
      )}
    >
      {style.active ? (
        <Spinner className="size-2.5" />
      ) : (
        <span className="size-1.5 rounded-full bg-current" />
      )}
      {style.label}
    </span>
  )
}

const STREAM: Record<StreamStatus, { label: string; className: string }> = {
  connecting: { label: 'Connecting…', className: 'text-ink-faint' },
  open: { label: 'Live', className: 'text-positive' },
  reconnecting: { label: 'Reconnecting…', className: 'text-warning' },
  done: { label: 'Stream closed', className: 'text-ink-faint' },
  error: { label: 'Disconnected', className: 'text-danger' },
}

export function StreamBadge({ status, detail }: { status: StreamStatus; detail?: string }) {
  const style = STREAM[status]
  return (
    <span
      title={detail}
      className={cx('inline-flex items-center gap-1.5 text-xs font-medium', style.className)}
    >
      <span
        className={cx(
          'size-1.5 rounded-full bg-current',
          status === 'open' && 'animate-pulse',
        )}
      />
      {style.label}
    </span>
  )
}
