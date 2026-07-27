import { useEffect, useRef, useState } from 'react'
import { describeEvent } from '../lib/eventText'
import type { EventTone } from '../lib/eventText'
import type { StreamStatus } from '../lib/sse'
import type { TopicEvent } from '../lib/types'
import { StreamBadge } from './StateBadge'
import { Card, SectionHeading, cx } from './primitives'

const TONE_DOT: Record<EventTone, string> = {
  neutral: 'bg-ink-faint',
  active: 'bg-accent',
  good: 'bg-positive',
  warn: 'bg-warning',
  bad: 'bg-danger',
}

/**
 * Append-only feed of pipeline events.
 *
 * Auto-scroll follows the tail but yields the moment the user scrolls up —
 * reading a tool result should never be yanked away by the next event.
 */
export function ActivityFeed({
  events,
  status,
  statusDetail,
}: {
  events: TopicEvent[]
  status: StreamStatus
  statusDetail?: string
}) {
  const scrollRef = useRef<HTMLDivElement>(null)
  const [follow, setFollow] = useState(true)

  useEffect(() => {
    if (!follow) return
    const node = scrollRef.current
    if (node) node.scrollTop = node.scrollHeight
  }, [events, follow])

  function onScroll() {
    const node = scrollRef.current
    if (!node) return
    const atBottom = node.scrollHeight - node.scrollTop - node.clientHeight < 40
    setFollow(atBottom)
  }

  return (
    <Card className="flex min-h-0 flex-col">
      <SectionHeading
        aside={
          <div className="flex items-center gap-3">
            <StreamBadge status={status} detail={statusDetail} />
            <label className="flex items-center gap-1.5 text-xs text-ink-muted">
              <input
                type="checkbox"
                checked={follow}
                onChange={(e) => setFollow(e.target.checked)}
                className="accent-accent"
              />
              Follow
            </label>
          </div>
        }
      >
        Live activity
      </SectionHeading>

      <div
        ref={scrollRef}
        onScroll={onScroll}
        role="log"
        aria-live="polite"
        aria-label="Pipeline activity"
        className="min-h-40 flex-1 overflow-y-auto px-4 py-3 lg:max-h-[calc(100vh-19rem)]"
      >
        {events.length === 0 ? (
          <p className="py-6 text-center text-sm text-ink-faint">
            {status === 'connecting' ? 'Connecting to the event stream…' : 'No activity yet.'}
          </p>
        ) : (
          <ol className="space-y-2">
            {events.map((event) => (
              <FeedRow key={event.seq} event={event} />
            ))}
          </ol>
        )}
      </div>
    </Card>
  )
}

function FeedRow({ event }: { event: TopicEvent }) {
  const line = describeEvent(event)
  return (
    <li className="flex gap-2.5 text-sm">
      <span
        aria-hidden="true"
        className={cx('mt-1.5 size-1.5 shrink-0 rounded-full', TONE_DOT[line.tone])}
      />
      <div className="min-w-0 flex-1">
        <div className="flex items-baseline justify-between gap-3">
          <span className="font-medium text-ink">{line.title}</span>
          <span className="shrink-0 font-mono text-[0.7rem] text-ink-faint">#{event.seq}</span>
        </div>
        {line.detail && (
          <p className="mt-0.5 text-xs break-words text-ink-muted">{line.detail}</p>
        )}
        {line.expandable && (
          <details className="mt-1">
            <summary className="cursor-pointer text-xs text-ink-faint hover:text-ink-muted">
              details
            </summary>
            <pre className="mt-1 max-h-48 overflow-auto rounded-md border border-line bg-surface-sunken p-2 font-mono text-[0.7rem] whitespace-pre-wrap text-ink-muted">
              {line.expandable}
            </pre>
          </details>
        )}
      </div>
    </li>
  )
}
