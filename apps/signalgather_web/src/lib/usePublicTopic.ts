/**
 * A shared topic's contents (#40), kept up to date while it is live (#50).
 *
 * The owner's workspace hook (`useTopicStream`) holds an event stream open,
 * because an owner needs to watch work happen. A reader does not, and an
 * unauthenticated long-poll per stranger is a resource tap the public API
 * deliberately does not offer. So this polls instead, and only where polling
 * buys something:
 *
 *   - a **frozen** share cannot change, so it is fetched once and left alone —
 *     no timer runs in that reader's tab, exactly as before;
 *   - a **live** share is checked every 60s against one cached, single-row
 *     endpoint. The artifacts — report, sources, plan, history — are re-fetched
 *     only when that check says something actually moved;
 *   - a hidden tab checks nothing at all, and catches up the moment it is looked
 *     at again;
 *   - repeated failures back off rather than hammering a server that is having
 *     a bad day.
 *
 * What the reader sees only ever advances in whole cycles: the API serves the
 * last *completed* state, so there is no partially-written report to land in the
 * middle of.
 */

import { useCallback, useEffect, useRef, useState } from 'react'
import { ApiError } from './api'
import {
  getPublicIntro,
  getPublicIntroMarkdown,
  getPublicNews,
  getPublicParsed,
  getPublicReport,
  getPublicReportMarkdown,
  getPublicSourceMix,
  getPublicTopic,
  listPublicDeltas,
} from './publicApi'
import type {
  DeltaSummary,
  IntroArtifact,
  NewsArtifact,
  ParsedArtifact,
  PublicTopic,
  ReportArtifact,
  SourceMixPayload,
} from './types'

export const POLL_INTERVAL_MS = 60_000
const MAX_BACKOFF_MS = 5 * 60_000

export interface PublicTopicState {
  topic: PublicTopic | null
  intro: IntroArtifact | null
  introMarkdown: string | null
  parsed: ParsedArtifact | null
  report: ReportArtifact | null
  reportMarkdown: string | null
  news: NewsArtifact | null
  sourceMix: SourceMixPayload | null
  deltas: DeltaSummary[]
  loading: boolean
  /** Set when the topic itself could not be read — usually "not shared". */
  error: string | null
  /**
   * Completed cycles that landed while this page was open. The reader is told
   * the page moved rather than having the ground shift under them silently.
   */
  updatesSinceOpened: number
}

const EMPTY: Omit<PublicTopicState, 'loading' | 'error' | 'updatesSinceOpened'> = {
  topic: null,
  intro: null,
  introMarkdown: null,
  parsed: null,
  report: null,
  reportMarkdown: null,
  news: null,
  sourceMix: null,
  deltas: [],
}

/** Everything that means "the shared state moved", in one comparable string. */
function stamp(topic: PublicTopic): string {
  return [
    topic.state,
    topic.share_mode,
    topic.updates.last_updated_at ?? '',
    topic.updates.latest_seq ?? '',
  ].join('|')
}

export function usePublicTopic(topicId: string): PublicTopicState {
  const [state, setState] = useState<Omit<PublicTopicState, 'loading' | 'error' | 'updatesSinceOpened'>>(EMPTY)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [updatesSinceOpened, setUpdatesSinceOpened] = useState(0)

  // Following one shared link to another must not paint the previous topic's
  // report under the new topic's title, so the reset happens during render
  // rather than in the effect below.
  const [renderedFor, setRenderedFor] = useState(topicId)
  if (renderedFor !== topicId) {
    setRenderedFor(topicId)
    setState(EMPTY)
    setLoading(true)
    setError(null)
    setUpdatesSinceOpened(0)
  }

  const lastStamp = useRef<string | null>(null)
  const baselineCycles = useRef<number | null>(null)

  const loadArtifacts = useCallback(async (topic: PublicTopic) => {
    // Artifacts are optional by design: a topic can be published with a plan
    // and no report, and each loader already resolves 404 to null.
    const [intro, introMarkdown, parsed, report, reportMarkdown, news, sourceMix, deltas] =
      await Promise.all([
        getPublicIntro(topicId).catch(() => null),
        getPublicIntroMarkdown(topicId).catch(() => null),
        getPublicParsed(topicId).catch(() => null),
        getPublicReport(topicId).catch(() => null),
        getPublicReportMarkdown(topicId).catch(() => null),
        getPublicNews(topicId).catch(() => null),
        getPublicSourceMix(topicId).catch(() => null),
        listPublicDeltas(topicId).catch(() => [] as DeltaSummary[]),
      ])
    return {
      topic,
      intro,
      introMarkdown,
      parsed,
      report,
      reportMarkdown,
      news,
      sourceMix,
      deltas,
    }
  }, [topicId])

  useEffect(() => {
    let cancelled = false
    let timer: ReturnType<typeof setTimeout> | undefined
    let failures = 0

    function schedule(delay: number) {
      if (cancelled) return
      clearTimeout(timer)
      timer = setTimeout(() => void tick(), delay)
    }

    async function tick() {
      if (cancelled) return
      // A backgrounded tab polls nothing; `visibilitychange` below brings it
      // back the moment someone looks at it.
      if (typeof document !== 'undefined' && document.visibilityState === 'hidden') return

      let topic: PublicTopic
      try {
        topic = await getPublicTopic(topicId)
      } catch (err) {
        if (cancelled) return
        if (err instanceof ApiError && err.isNotFound) {
          // The owner withdrew the link while this tab was open. Say so and stop
          // polling — there is nothing to come back to.
          setError(describe(err))
          setLoading(false)
          return
        }
        failures += 1
        // A first load that fails must not leave the reader staring at a
        // skeleton; a later one keeps what is already on screen and retries.
        if (lastStamp.current === null) {
          setError(describe(err))
          setLoading(false)
        }
        schedule(Math.min(POLL_INTERVAL_MS * 2 ** failures, MAX_BACKOFF_MS))
        return
      }
      failures = 0
      if (cancelled) return
      setError(null)

      const next = stamp(topic)
      const first = lastStamp.current === null
      const moved = lastStamp.current !== next
      lastStamp.current = next

      if (first) baselineCycles.current = topic.updates.update_count ?? 0

      if (moved) {
        setState((prev) => ({ ...prev, topic }))
        const loaded = await loadArtifacts(topic)
        if (cancelled) return
        setState(loaded)
        setLoading(false)
        if (!first) {
          const base = baselineCycles.current ?? 0
          setUpdatesSinceOpened(Math.max(0, (topic.updates.update_count ?? 0) - base))
        }
      }

      // A frozen share cannot move: stop here and leave no timer behind.
      if (topic.share_mode === 'live') schedule(POLL_INTERVAL_MS)
    }

    function onVisible() {
      if (document.visibilityState === 'visible') void tick()
    }

    void tick()
    document.addEventListener('visibilitychange', onVisible)

    return () => {
      cancelled = true
      clearTimeout(timer)
      document.removeEventListener('visibilitychange', onVisible)
      lastStamp.current = null
      baselineCycles.current = null
    }
  }, [topicId, loadArtifacts])

  return { ...state, loading, error, updatesSinceOpened }
}

function describe(err: unknown): string {
  if (err instanceof ApiError && err.isNotFound) {
    return 'This topic is not shared. The link may have been withdrawn by its owner.'
  }
  if (err instanceof ApiError) return err.detail
  return err instanceof Error ? err.message : String(err)
}
