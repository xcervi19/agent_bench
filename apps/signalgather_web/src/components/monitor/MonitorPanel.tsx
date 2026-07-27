import { useState } from 'react'
import {
  ApiError,
  startMonitor,
  stopMonitor,
  triggerRefresh,
  updateMonitor,
} from '../../lib/api'
import { absoluteTime, relativeTime } from '../../lib/format'
import type { MonitorState, TopicDetail } from '../../lib/types'
import { Button, Card, ErrorNote, SectionHeading, Skeleton, cx } from '../primitives'

/** Bounds enforced by the API (`schedule_{min,max}_interval_hours`). */
const INTERVALS = [
  { hours: 1, label: 'Hourly' },
  { hours: 6, label: 'Every 6h' },
  { hours: 12, label: 'Every 12h' },
  { hours: 24, label: 'Daily' },
  { hours: 168, label: 'Weekly' },
]

const AGE_WINDOWS = [24, 48, 72, 168]

/**
 * Monitoring controls (16c).
 *
 * Monitoring is a two-part idea and the UI keeps them visibly separate:
 * the *subscription* (active/paused, how fresh a source must be) and the
 * *schedule* (whether the server refreshes on its own, #22). A subscription can
 * be active with no schedule — manual refresh only — which is the default the
 * API gives us, so the panel must not imply enabling one enables the other.
 */
export function MonitorPanel({
  topic,
  monitor,
  loading,
  onChanged,
}: {
  topic: TopicDetail
  monitor: MonitorState | null
  loading: boolean
  onChanged: () => void
}) {
  const [pending, setPending] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [notice, setNotice] = useState<string | null>(null)

  const canMonitor = topic.state === 'reported'
  const active = monitor?.status === 'active'

  async function run(label: string, action: () => Promise<unknown>) {
    setPending(label)
    setError(null)
    setNotice(null)
    try {
      await action()
      onChanged()
    } catch (err) {
      setError(err instanceof ApiError ? err.detail : String(err))
    } finally {
      setPending(null)
    }
  }

  if (loading && !monitor) {
    return (
      <Card className="p-5">
        <Skeleton lines={3} />
      </Card>
    )
  }

  if (!canMonitor) {
    return (
      <Card>
        <SectionHeading>Monitoring</SectionHeading>
        <p className="px-4 py-6 text-sm text-ink-muted">
          Monitoring starts once the topic has a finished report. This topic is{' '}
          <span className="text-ink">{topic.state}</span>.
        </p>
      </Card>
    )
  }

  return (
    <Card>
      <SectionHeading
        aside={
          <span
            className={cx(
              'rounded-full border px-2.5 py-1 text-xs font-medium',
              active
                ? 'border-positive/50 bg-positive/10 text-positive'
                : 'border-line bg-surface-sunken text-ink-faint',
            )}
          >
            {active ? 'Active' : monitor ? 'Paused' : 'Off'}
          </span>
        }
      >
        Monitoring
      </SectionHeading>

      {!monitor ? (
        <div className="px-4 py-5">
          <p className="text-sm text-ink-muted">
            Turn on monitoring to keep collecting only what is new on this topic. The agent builds
            a short-term query plan from the report and reuses it every cycle.
          </p>
          <Button
            variant="primary"
            className="mt-4"
            busy={pending === 'start'}
            onClick={() => run('start', () => startMonitor(topic.id, { maxAgeHours: 48 }))}
          >
            Enable monitoring
          </Button>
        </div>
      ) : (
        <div className="divide-y divide-line">
          <Row
            label="Freshness window"
            hint="How old a source may be and still count as new."
          >
            <div className="flex flex-wrap gap-1">
              {AGE_WINDOWS.map((hours) => (
                <Choice
                  key={hours}
                  active={monitor.max_age_hours === hours}
                  busy={pending === `age-${hours}`}
                  onClick={() =>
                    run(`age-${hours}`, () => updateMonitor(topic.id, { maxAgeHours: hours }))
                  }
                >
                  {hours}h
                </Choice>
              ))}
            </div>
          </Row>

          <Row
            label="Automatic refresh"
            hint={
              monitor.schedule_enabled
                ? 'The server refreshes on its own — no need to keep this tab open.'
                : 'Off: refreshes only happen when you press Refresh now.'
            }
          >
            <div className="flex flex-wrap gap-1">
              <Choice
                active={!monitor.schedule_enabled}
                busy={pending === 'sched-off'}
                onClick={() =>
                  run('sched-off', () => updateMonitor(topic.id, { scheduleEnabled: false }))
                }
              >
                Off
              </Choice>
              {INTERVALS.map((option) => (
                <Choice
                  key={option.hours}
                  active={
                    monitor.schedule_enabled &&
                    monitor.schedule_interval_hours === option.hours
                  }
                  busy={pending === `sched-${option.hours}`}
                  onClick={() =>
                    run(`sched-${option.hours}`, () =>
                      updateMonitor(topic.id, {
                        scheduleEnabled: true,
                        scheduleIntervalHours: option.hours,
                      }),
                    )
                  }
                >
                  {option.label}
                </Choice>
              ))}
            </div>
          </Row>

          <div className="grid grid-cols-2 gap-x-4 gap-y-2 px-4 py-3 text-xs sm:grid-cols-4">
            <Fact label="Cycles run" value={String(monitor.refresh_count)} />
            <Fact
              label="Last refresh"
              value={monitor.last_refresh_at ? relativeTime(monitor.last_refresh_at) : '—'}
              title={monitor.last_refresh_at ? absoluteTime(monitor.last_refresh_at) : undefined}
            />
            <Fact
              label="Next scheduled"
              value={
                monitor.schedule_enabled && monitor.next_refresh_at
                  ? relativeTime(monitor.next_refresh_at)
                  : '—'
              }
              title={monitor.next_refresh_at ? absoluteTime(monitor.next_refresh_at) : undefined}
            />
            <Fact
              label="Queries"
              value={
                monitor.queries_count !== undefined
                  ? String(monitor.queries_count)
                  : monitor.short_term_queries
                    ? String(monitor.short_term_queries.length)
                    : '—'
              }
            />
          </div>

          <div className="flex flex-wrap items-center justify-between gap-3 px-4 py-3">
            <p className="text-xs text-ink-muted">
              {monitor.refresh_locked
                ? 'A refresh cycle is running now.'
                : 'Manual refresh runs one cycle immediately.'}
            </p>
            <div className="flex gap-2">
              {active ? (
                <Button
                  variant="secondary"
                  busy={pending === 'pause'}
                  onClick={() => run('pause', () => stopMonitor(topic.id))}
                >
                  Pause
                </Button>
              ) : (
                <Button
                  variant="secondary"
                  busy={pending === 'resume'}
                  onClick={() =>
                    run('resume', () =>
                      startMonitor(topic.id, { maxAgeHours: monitor.max_age_hours }),
                    )
                  }
                >
                  Resume
                </Button>
              )}
              <Button
                variant="primary"
                disabled={!active || monitor.refresh_locked}
                busy={pending === 'refresh'}
                onClick={() =>
                  run('refresh', async () => {
                    const ack = await triggerRefresh(topic.id)
                    setNotice(
                      ack.queued
                        ? 'Refresh started — watch the activity feed.'
                        : (ack.reason ?? 'A refresh is already running.'),
                    )
                  })
                }
              >
                Refresh now
              </Button>
            </div>
          </div>
        </div>
      )}

      {(error || notice) && (
        <div className="px-4 pb-4">
          {error ? <ErrorNote>{error}</ErrorNote> : <p className="text-xs text-positive">{notice}</p>}
        </div>
      )}
    </Card>
  )
}

function Row({
  label,
  hint,
  children,
}: {
  label: string
  hint?: string
  children: React.ReactNode
}) {
  return (
    <div className="flex flex-wrap items-start justify-between gap-3 px-4 py-3">
      <div className="min-w-0">
        <p className="text-sm text-ink">{label}</p>
        {hint && <p className="mt-0.5 text-xs text-ink-faint">{hint}</p>}
      </div>
      {children}
    </div>
  )
}

function Choice({
  active,
  busy,
  onClick,
  children,
}: {
  active: boolean
  busy: boolean
  onClick: () => void
  children: React.ReactNode
}) {
  return (
    <button
      onClick={onClick}
      disabled={busy}
      aria-pressed={active}
      className={cx(
        'rounded-md border px-2.5 py-1 text-xs font-medium transition-colors disabled:opacity-50',
        active
          ? 'border-accent/50 bg-accent/15 text-accent'
          : 'border-line text-ink-muted hover:text-ink',
      )}
    >
      {children}
    </button>
  )
}

function Fact({ label, value, title }: { label: string; value: string; title?: string }) {
  return (
    <div title={title}>
      <p className="text-ink-faint">{label}</p>
      <p className="mt-0.5 text-ink-muted">{value}</p>
    </div>
  )
}
