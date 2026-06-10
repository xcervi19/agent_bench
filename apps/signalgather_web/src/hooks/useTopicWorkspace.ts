import { useCallback, useEffect, useRef, useState } from 'react'
import type {
  DeltaSummary,
  MonitorStatus,
  NewsArtifact,
  QueryPlan,
  ReportArtifact,
  TopicDetail,
  TopicEvent,
} from '@/lib/types'
import {
  cancelTopic,
  fetchArtifactSafe,
  fetchDelta,
  fetchDeltaNews,
  fetchDeltaReport,
  fetchIntroMd,
  fetchNews,
  fetchParsed,
  fetchReport,
  fetchReportMd,
  getMonitor,
  getTopic,
  listDeltas,
  proceedTopic,
  startMonitor,
  stopMonitor,
  triggerRefresh,
} from '@/lib/api'
import { TopicSseClient, type SseStatus } from '@/lib/sse'
import { useSettings } from '@/context/SettingsContext'

export interface WorkspaceArtifacts {
  introMd: string | null
  parsed: QueryPlan | null
  reportMd: string | null
  report: ReportArtifact | null
  news: NewsArtifact | null
}

export function useTopicWorkspace(topicId: string) {
  const { settings } = useSettings()
  const [topic, setTopic] = useState<TopicDetail | null>(null)
  const [events, setEvents] = useState<TopicEvent[]>([])
  const [sseStatus, setSseStatus] = useState<SseStatus>('disconnected')
  const [sseError, setSseError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState<string | null>(null)
  const [artifacts, setArtifacts] = useState<WorkspaceArtifacts>({
    introMd: null,
    parsed: null,
    reportMd: null,
    report: null,
    news: null,
  })
  const [artifactLoading, setArtifactLoading] = useState<Record<string, boolean>>({})
  const [monitor, setMonitor] = useState<MonitorStatus | null>(null)
  const [deltas, setDeltas] = useState<DeltaSummary[]>([])
  const [selectedDelta, setSelectedDelta] = useState<number | null>(null)
  const [deltaDetail, setDeltaDetail] = useState<{
    delta: Record<string, unknown> | null
    news: NewsArtifact | null
    reportMd: string | null
  }>({ delta: null, news: null, reportMd: null })
  const sseRef = useRef<TopicSseClient | null>(null)
  const lastSeqRef = useRef(0)

  const refreshTopic = useCallback(async () => {
    const data = await getTopic(settings, topicId)
    setTopic(data)
    return data
  }, [settings, topicId])

  const refreshMonitor = useCallback(async () => {
    const data = await getMonitor(settings, topicId)
    setMonitor(data)
    return data
  }, [settings, topicId])

  const refreshDeltas = useCallback(async () => {
    const data = await listDeltas(settings, topicId)
    setDeltas(data.deltas)
    return data.deltas
  }, [settings, topicId])

  const loadArtifact = useCallback(
    async (key: keyof WorkspaceArtifacts, loader: () => Promise<unknown>) => {
      setArtifactLoading((prev) => ({ ...prev, [key]: true }))
      const { data, error } = await fetchArtifactSafe(loader)
      setArtifactLoading((prev) => ({ ...prev, [key]: false }))
      if (data !== null) {
        setArtifacts((prev) => ({ ...prev, [key]: data }))
      }
      return { data, error }
    },
    [],
  )

  const hydrateFromState = useCallback(
    async (detail: TopicDetail) => {
      if (detail.state === 'planned_awaiting_review' || detail.state === 'reported') {
        void loadArtifact('introMd', () => fetchIntroMd(settings, topicId))
        void loadArtifact('parsed', () => fetchParsed(settings, topicId))
      }
      if (detail.state === 'reported') {
        void loadArtifact('reportMd', () => fetchReportMd(settings, topicId))
        void loadArtifact('report', () => fetchReport(settings, topicId))
        void loadArtifact('news', () => fetchNews(settings, topicId))
        void refreshMonitor()
        void refreshDeltas()
      }
    },
    [loadArtifact, refreshDeltas, refreshMonitor, settings, topicId],
  )

  const handleEvent = useCallback(
    async (event: TopicEvent) => {
      setEvents((prev) => {
        if (prev.some((e) => e.seq === event.seq)) return prev
        return [...prev, event]
      })
      lastSeqRef.current = Math.max(lastSeqRef.current, event.seq)

      switch (event.event_type) {
        case 'state.changed':
        case 'topic.created':
          void refreshTopic().then(hydrateFromState)
          break
        case 'intro.ready':
        case 'needs_input':
          void loadArtifact('introMd', () => fetchIntroMd(settings, topicId))
          void loadArtifact('parsed', () => fetchParsed(settings, topicId))
          void refreshTopic()
          break
        case 'report.ready':
          void loadArtifact('reportMd', () => fetchReportMd(settings, topicId))
          void loadArtifact('report', () => fetchReport(settings, topicId))
          void loadArtifact('news', () => fetchNews(settings, topicId))
          void refreshTopic()
          break
        case 'monitor.started':
        case 'monitor.updated':
        case 'monitor.stopped':
          void refreshMonitor()
          break
        case 'refresh.completed':
          void refreshDeltas()
          void refreshMonitor()
          void refreshTopic()
          break
        case 'refresh.failed':
        case 'error':
          void refreshTopic()
          break
        default:
          break
      }
    },
    [hydrateFromState, loadArtifact, refreshDeltas, refreshMonitor, refreshTopic, settings, topicId],
  )

  useEffect(() => {
    let cancelled = false

    async function init() {
      setLoading(true)
      try {
        const detail = await refreshTopic()
        if (cancelled) return
        await hydrateFromState(detail)
        if (cancelled) return

        const client = new TopicSseClient({
          settings,
          topicId,
          fromSeq: detail.last_event_seq ?? 0,
          onEvent: handleEvent,
          onStatusChange: setSseStatus,
          onError: setSseError,
        })
        sseRef.current = client
        lastSeqRef.current = detail.last_event_seq ?? 0
        client.start()
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    void init()

    return () => {
      cancelled = true
      sseRef.current?.stop()
      sseRef.current = null
    }
  }, [topicId, settings, refreshTopic, hydrateFromState, handleEvent])

  const runAction = async (name: string, fn: () => Promise<void>) => {
    setActionLoading(name)
    try {
      await fn()
      await refreshTopic()
    } finally {
      setActionLoading(null)
    }
  }

  const proceed = () => runAction('proceed', () => proceedTopic(settings, topicId))
  const cancel = () => runAction('cancel', () => cancelTopic(settings, topicId))
  const enableMonitor = (hours: number) =>
    runAction('monitor', async () => {
      const status = await startMonitor(settings, topicId, hours)
      setMonitor(status)
    })
  const disableMonitor = () =>
    runAction('monitor', async () => {
      await stopMonitor(settings, topicId)
      setMonitor(null)
    })
  const refresh = () =>
    runAction('refresh', async () => {
      await triggerRefresh(settings, topicId)
    })

  const openDelta = async (seq: number) => {
    setSelectedDelta(seq)
    const [deltaRes, newsRes, reportRes] = await Promise.all([
      fetchArtifactSafe(() => fetchDelta(settings, topicId, seq)),
      fetchArtifactSafe(() => fetchDeltaNews(settings, topicId, seq)),
      fetchArtifactSafe(() => fetchDeltaReport(settings, topicId, seq)),
    ])
    setDeltaDetail({
      delta: deltaRes.data as Record<string, unknown> | null,
      news: newsRes.data,
      reportMd: reportRes.data,
    })
  }

  return {
    topic,
    events,
    sseStatus,
    sseError,
    loading,
    actionLoading,
    artifacts,
    artifactLoading,
    monitor,
    deltas,
    selectedDelta,
    deltaDetail,
    proceed,
    cancel,
    enableMonitor,
    disableMonitor,
    refresh,
    openDelta,
    closeDelta: () => setSelectedDelta(null),
    refreshTopic,
    refreshDeltas,
  }
}
