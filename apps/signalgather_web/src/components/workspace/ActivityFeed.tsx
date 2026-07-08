import { useEffect, useRef, useState } from 'react'
import { ChevronDown, ChevronRight, Terminal } from 'lucide-react'
import type { TopicEvent } from '@/lib/types'
import { cn } from '@/lib/utils'

const STAGE_EVENTS = new Set([
  'stage.started',
  'stage.finished',
  'tool_use',
  'tool_result',
  'refresh.started',
  'refresh.completed',
  'refresh.failed',
  'error',
  'state.changed',
  'intro.ready',
  'report.ready',
  'needs_input',
  'monitor.started',
  'monitor.updated',
  'monitor.stopped',
])

function eventLabel(event: TopicEvent): string {
  const p = event.payload
  switch (event.event_type) {
    case 'stage.started':
      return `Stage started: ${String(p.stage ?? p.name ?? 'unknown')}`
    case 'stage.finished':
      return `Stage finished: ${String(p.stage ?? p.name ?? 'unknown')}`
    case 'tool_use':
      return `Tool: ${String(p.tool ?? 'unknown')}`
    case 'tool_result':
      return `Result: ${String(p.tool ?? 'unknown')}`
    case 'state.changed':
      return `State → ${String(p.state ?? p.to ?? 'unknown')}`
    case 'intro.ready':
      return `Plan ready (${String(p.queries_count ?? '?')} queries)`
    case 'report.ready':
      return `Report ready (${String(p.sources_count ?? '?')} sources)`
    case 'refresh.started':
      return 'Refresh started'
    case 'refresh.completed':
      return `Refresh complete (+${String(p.new_sources_count ?? 0)} sources)`
    case 'refresh.failed':
      return `Refresh failed: ${String(p.error ?? 'unknown')}`
    case 'error':
      return `Error: ${String(p.error ?? p.message ?? 'unknown')}`
    case 'monitor.started':
      return 'Monitoring enabled'
    case 'monitor.stopped':
      return 'Monitoring paused'
    default:
      return event.event_type
  }
}

function eventColor(type: string): string {
  if (type.includes('error') || type === 'refresh.failed') return 'text-danger'
  if (type.includes('ready') || type.includes('completed')) return 'text-success'
  if (type.includes('started') || type === 'tool_use') return 'text-accent'
  return 'text-text-muted'
}

function EventRow({ event }: { event: TopicEvent }) {
  const [open, setOpen] = useState(false)
  const hasDetail =
    event.event_type === 'tool_use' ||
    event.event_type === 'tool_result' ||
    Object.keys(event.payload).length > 2

  return (
    <div className="border-b border-border-subtle last:border-0">
      <button
        type="button"
        onClick={() => hasDetail && setOpen(!open)}
        className={cn(
          'w-full flex items-start gap-2 px-3 py-2 text-left text-xs hover:bg-surface-overlay/50 transition-colors',
          !hasDetail && 'cursor-default',
        )}
      >
        <span className="text-text-muted font-mono shrink-0 w-8">#{event.seq}</span>
        <span className={cn('flex-1', eventColor(event.event_type))}>
          {eventLabel(event)}
        </span>
        {hasDetail &&
          (open ? (
            <ChevronDown className="h-3.5 w-3.5 text-text-muted shrink-0" />
          ) : (
            <ChevronRight className="h-3.5 w-3.5 text-text-muted shrink-0" />
          ))}
      </button>
      {open && hasDetail && (
        <pre className="mx-3 mb-2 rounded-md bg-surface p-2 text-[10px] font-mono text-text-muted overflow-x-auto max-h-32">
          {JSON.stringify(event.payload, null, 2)}
        </pre>
      )}
    </div>
  )
}

export function ActivityFeed({ events }: { events: TopicEvent[] }) {
  const bottomRef = useRef<HTMLDivElement>(null)
  const [autoScroll, setAutoScroll] = useState(true)

  const filtered = events.filter((e) => STAGE_EVENTS.has(e.event_type) || e.seq > 0)

  useEffect(() => {
    if (autoScroll) {
      bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }
  }, [filtered.length, autoScroll])

  return (
    <div className="rounded-xl border border-border bg-surface-raised flex flex-col h-full min-h-[280px]">
      <div className="flex items-center justify-between px-4 py-3 border-b border-border">
        <div className="flex items-center gap-2">
          <Terminal className="h-4 w-4 text-text-muted" />
          <h2 className="text-sm font-medium text-text">Live Activity</h2>
          <span className="text-xs text-text-muted">({filtered.length})</span>
        </div>
        <label className="flex items-center gap-1.5 text-xs text-text-muted cursor-pointer">
          <input
            type="checkbox"
            checked={autoScroll}
            onChange={(e) => setAutoScroll(e.target.checked)}
            className="rounded border-border"
          />
          Auto-scroll
        </label>
      </div>

      <div className="flex-1 overflow-y-auto max-h-[400px]">
        {filtered.length === 0 ? (
          <p className="p-4 text-xs text-text-muted text-center">
            Waiting for pipeline events…
          </p>
        ) : (
          filtered.map((event) => <EventRow key={event.seq} event={event} />)
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  )
}
