/**
 * The workspace's live model of one topic.
 *
 * Rules from the spec's UX principles:
 *   - artifacts are fetched when an event says they exist, never on a timer;
 *   - the stream is the only thing polling, and it resumes by `seq`;
 *   - a reload replays from seq 0 so the activity feed keeps its history.
 *
 * Artifacts are grouped by the pipeline stage that produces them. Each group
 * has one loader, one in-flight guard, and a set of events that invalidate it,
 * so adding a stage is a table entry rather than another copy of this logic.
 */

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import {
  ApiError,
  getIntro,
  getIntroMarkdown,
  getMonitor,
  getNews,
  getParsed,
  getReport,
  getReportMarkdown,
  getTopic,
  listDeltas,
} from './api'
import { streamTopicEvents } from './sse'
import type { StreamStatus } from './sse'
import type {
  DeltaSummary,
  IntroArtifact,
  MonitorState,
  NewsArtifact,
  ParsedArtifact,
  ReportArtifact,
  TopicDetail,
  TopicEvent,
} from './types'

/** Tool traffic is chatty; keep the feed bounded so long runs stay responsive. */
const MAX_EVENTS = 500

export type ArtifactGroup = 'plan' | 'report' | 'monitor' | 'deltas'

export interface Artifacts {
  intro: IntroArtifact | null
  introMarkdown: string | null
  parsed: ParsedArtifact | null
  report: ReportArtifact | null
  reportMarkdown: string | null
  news: NewsArtifact | null
  monitor: MonitorState | null
  deltas: DeltaSummary[]
}

const EMPTY: Artifacts = {
  intro: null,
  introMarkdown: null,
  parsed: null,
  report: null,
  reportMarkdown: null,
  news: null,
  monitor: null,
  deltas: [],
}

/** Which group each event invalidates. Anything absent touches no artifact. */
const EVENT_GROUPS: Record<string, ArtifactGroup[]> = {
  'intro.ready': ['plan'],
  needs_input: ['plan'],
  'report.ready': ['report'],
  'monitor.started': ['monitor'],
  'monitor.updated': ['monitor'],
  'monitor.stopped': ['monitor'],
  'refresh.started': ['monitor'],
  'refresh.completed': ['monitor', 'deltas'],
  'refresh.failed': ['monitor', 'deltas'],
  'refresh.skipped': ['monitor'],
}

/** Events that mean the topic row itself moved. */
const TOPIC_EVENTS = new Set(['state.changed', 'error'])

export interface TopicStreamState extends Artifacts {
  topic: TopicDetail | null
  events: TopicEvent[]
  status: StreamStatus
  statusDetail?: string
  loading: Record<ArtifactGroup, boolean>
  loadError: string | null
  /** Re-read the topic and the named groups (default: all that apply). */
  refresh: (groups?: ArtifactGroup[]) => Promise<void>
}

export function useTopicStream(topicId: string): TopicStreamState {
  const [topic, setTopic] = useState<TopicDetail | null>(null)
  const [events, setEvents] = useState<TopicEvent[]>([])
  const [status, setStatus] = useState<StreamStatus>('connecting')
  const [statusDetail, setStatusDetail] = useState<string | undefined>()
  const [artifacts, setArtifacts] = useState<Artifacts>(EMPTY)
  const [loading, setLoading] = useState<Record<ArtifactGroup, boolean>>({
    plan: false,
    report: false,
    monitor: false,
    deltas: false,
  })
  const [loadError, setLoadError] = useState<string | null>(null)

  // Navigating between topics must not flash the previous topic's data. React's
  // "adjust state during render" pattern clears it before the first paint of the
  // new id — an effect would render stale content once first.
  const [renderedFor, setRenderedFor] = useState(topicId)
  if (renderedFor !== topicId) {
    setRenderedFor(topicId)
    setTopic(null)
    setEvents([])
    setArtifacts(EMPTY)
    setLoadError(null)
    setStatus('connecting')
    setStatusDetail(undefined)
  }

  const aliveRef = useRef(true)
  // One in-flight fetch per group: two events arriving together (intro.ready +
  // needs_input, monitor.updated + refresh.completed) must not double-fetch.
  const inFlight = useRef<Partial<Record<ArtifactGroup, Promise<void>>>>({})
  // ...but a request that arrives *during* a fetch cannot just be dropped: the
  // response in flight may predate the change that triggered it. Mark the group
  // and re-run once, so N requests collapse to at most one extra fetch and the
  // last one is never lost.
  const dirty = useRef<Set<ArtifactGroup>>(new Set())

  const loaders = useMemo<Record<ArtifactGroup, () => Promise<Partial<Artifacts>>>>(
    () => ({
      plan: async () => {
        const [intro, introMarkdown, parsed] = await Promise.all([
          getIntro(topicId),
          getIntroMarkdown(topicId),
          getParsed(topicId),
        ])
        return { intro, introMarkdown, parsed }
      },
      report: async () => {
        const [report, reportMarkdown, news] = await Promise.all([
          getReport(topicId),
          getReportMarkdown(topicId),
          getNews(topicId),
        ])
        return { report, reportMarkdown, news }
      },
      monitor: async () => ({ monitor: await getMonitor(topicId) }),
      deltas: async () => ({ deltas: await listDeltas(topicId) }),
    }),
    [topicId],
  )

  const loadTopic = useCallback(async () => {
    try {
      const detail = await getTopic(topicId)
      if (aliveRef.current) setTopic(detail)
      return detail
    } catch (err) {
      if (aliveRef.current) setLoadError(describe(err))
      return null
    }
  }, [topicId])

  const loadGroup = useCallback(
    (group: ArtifactGroup): Promise<void> => {
      const existing = inFlight.current[group]
      if (existing) {
        dirty.current.add(group)
        return existing
      }

      setLoading((prev) => ({ ...prev, [group]: true }))
      const job = (async () => {
        // Loop rather than recurse: keep fetching while requests keep landing
        // mid-flight, so the group ends up reflecting the last one.
        do {
          dirty.current.delete(group)
          try {
            const partial = await loaders[group]()
            if (aliveRef.current) setArtifacts((prev) => ({ ...prev, ...partial }))
          } catch (err) {
            if (aliveRef.current) setLoadError(describe(err))
            break // a failing endpoint must not spin here
          }
        } while (dirty.current.has(group) && aliveRef.current)
        dirty.current.delete(group)
      })().finally(() => {
        delete inFlight.current[group]
        if (aliveRef.current) setLoading((prev) => ({ ...prev, [group]: false }))
      })

      inFlight.current[group] = job
      return job
    },
    [loaders],
  )

  const refresh = useCallback(
    async (groups?: ArtifactGroup[]) => {
      const detail = await loadTopic()
      const wanted = groups ?? groupsFor(detail)
      await Promise.all(wanted.map(loadGroup))
    },
    [loadTopic, loadGroup],
  )

  useEffect(() => {
    aliveRef.current = true
    inFlight.current = {}
    dirty.current.clear()
    const controller = new AbortController()

    void (async () => {
      const detail = await loadTopic()
      if (!detail) {
        if (aliveRef.current) setStatus('error')
        return
      }

      // Reconnect-safe hydration: whatever the pipeline finished while we were
      // away exists now, and no future event will announce it.
      for (const group of groupsFor(detail)) void loadGroup(group)

      await streamTopicEvents({
        topicId,
        fromSeq: 0,
        signal: controller.signal,
        onStatus: (next, why) => {
          if (!aliveRef.current) return
          setStatus(next)
          setStatusDetail(why)
        },
        onEvent: (event) => {
          if (!aliveRef.current) return
          setEvents((prev) => {
            const next = [...prev, event]
            return next.length > MAX_EVENTS ? next.slice(next.length - MAX_EVENTS) : next
          })
          for (const group of EVENT_GROUPS[event.event_type] ?? []) void loadGroup(group)
          if (TOPIC_EVENTS.has(event.event_type)) {
            void loadTopic().then((moved) => {
              // Reaching `reported` unlocks report + monitoring in one step.
              if (moved?.state === 'reported') {
                void loadGroup('report')
                void loadGroup('monitor')
              }
            })
          }
        },
      })

      // Terminal or exhausted: reconcile once more so the badge and available
      // actions match the server, whatever happened to the stream.
      if (aliveRef.current) void loadTopic()
    })()

    return () => {
      aliveRef.current = false
      controller.abort()
    }
  }, [topicId, loadGroup, loadTopic])

  return {
    ...artifacts,
    topic,
    events,
    status,
    statusDetail,
    loading,
    loadError,
    refresh,
  }
}

/** Which groups have artifacts worth fetching for a topic in this state. */
function groupsFor(detail: TopicDetail | null): ArtifactGroup[] {
  if (!detail) return []
  const groups: ArtifactGroup[] = []
  if (detail.plan_run_id) groups.push('plan')
  if (detail.deliver_run_id) groups.push('report')
  // Monitoring only exists after a report, and only then can deltas exist.
  if (detail.state === 'reported') groups.push('monitor', 'deltas')
  return groups
}

function describe(err: unknown): string {
  if (err instanceof ApiError) {
    if (err.isNotFound) return 'Topic not found — it may belong to another account.'
    if (err.isAuthError) return 'Your session expired. Sign in again.'
    return err.detail
  }
  return err instanceof Error ? err.message : String(err)
}
