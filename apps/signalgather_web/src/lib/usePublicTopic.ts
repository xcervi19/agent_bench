/**
 * A shared topic's contents, loaded once (#40).
 *
 * The owner's workspace hook (`useTopicStream`) exists because a live topic
 * keeps changing: it holds an event stream open and re-fetches the artifacts an
 * event says are stale. A published topic cannot change — the API refuses every
 * write while `is_public` is set — so this hook is the whole story: fetch, then
 * stop. No stream, no polling, no retry timer running in a stranger's tab.
 */

import { useEffect, useState } from 'react'
import { ApiError } from './api'
import {
  getPublicIntro,
  getPublicIntroMarkdown,
  getPublicNews,
  getPublicParsed,
  getPublicReport,
  getPublicReportMarkdown,
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
} from './types'

export interface PublicTopicState {
  topic: PublicTopic | null
  intro: IntroArtifact | null
  introMarkdown: string | null
  parsed: ParsedArtifact | null
  report: ReportArtifact | null
  reportMarkdown: string | null
  news: NewsArtifact | null
  deltas: DeltaSummary[]
  loading: boolean
  /** Set when the topic itself could not be read — usually "not shared". */
  error: string | null
}

const EMPTY: Omit<PublicTopicState, 'loading' | 'error'> = {
  topic: null,
  intro: null,
  introMarkdown: null,
  parsed: null,
  report: null,
  reportMarkdown: null,
  news: null,
  deltas: [],
}

export function usePublicTopic(topicId: string): PublicTopicState {
  const [state, setState] = useState<Omit<PublicTopicState, 'loading' | 'error'>>(EMPTY)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Following one shared link to another must not paint the previous topic's
  // report under the new topic's title, so the reset happens during render
  // rather than in the effect below.
  const [renderedFor, setRenderedFor] = useState(topicId)
  if (renderedFor !== topicId) {
    setRenderedFor(topicId)
    setState(EMPTY)
    setLoading(true)
    setError(null)
  }

  useEffect(() => {
    let cancelled = false

    void (async () => {
      let topic: PublicTopic
      try {
        topic = await getPublicTopic(topicId)
      } catch (err) {
        if (!cancelled) {
          setError(describe(err))
          setLoading(false)
        }
        return
      }
      if (cancelled) return
      setState((prev) => ({ ...prev, topic }))

      // Artifacts are optional by design: a topic can be published with a plan
      // and no report, and each loader already resolves 404 to null.
      const [intro, introMarkdown, parsed, report, reportMarkdown, news, deltas] =
        await Promise.all([
          getPublicIntro(topicId).catch(() => null),
          getPublicIntroMarkdown(topicId).catch(() => null),
          getPublicParsed(topicId).catch(() => null),
          getPublicReport(topicId).catch(() => null),
          getPublicReportMarkdown(topicId).catch(() => null),
          getPublicNews(topicId).catch(() => null),
          listPublicDeltas(topicId).catch(() => [] as DeltaSummary[]),
        ])

      if (cancelled) return
      setState({ topic, intro, introMarkdown, parsed, report, reportMarkdown, news, deltas })
      setLoading(false)
    })()

    return () => {
      cancelled = true
    }
  }, [topicId])

  return { ...state, loading, error }
}

function describe(err: unknown): string {
  if (err instanceof ApiError && err.isNotFound) {
    return 'This topic is not shared. The link may have been withdrawn by its owner.'
  }
  if (err instanceof ApiError) return err.detail
  return err instanceof Error ? err.message : String(err)
}
