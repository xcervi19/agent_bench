import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { ApiError } from '../lib/api'
import { listPublicTopics } from '../lib/publicApi'
import { absoluteTime, relativeTime } from '../lib/format'
import type { PublicTopic } from '../lib/types'
import { StateBadge } from '../components/StateBadge'
import { Card, EmptyState, ErrorNote, Skeleton } from '../components/primitives'

/**
 * Everything anyone has shared (#40) — the "everyone can find this topic" half
 * of publishing. Open to readers without an account, and read-only: there is no
 * control on this page, or on the pages it links to, that runs anything.
 */
export function PublicTopicListPage() {
  const [query, setQuery] = useState('')
  const [submitted, setSubmitted] = useState('')
  const [topics, setTopics] = useState<PublicTopic[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [reloadKey, setReloadKey] = useState(0)

  // Clear the previous result set before the first paint of a new search rather
  // than inside the effect, so the list never shows the old matches under a new
  // heading. (Same "adjust state during render" pattern as useTopicStream.)
  const [renderedFor, setRenderedFor] = useState(submitted)
  if (renderedFor !== submitted) {
    setRenderedFor(submitted)
    setTopics(null)
  }

  useEffect(() => {
    let cancelled = false
    listPublicTopics(submitted)
      .then((res) => {
        if (cancelled) return
        setTopics(res.items)
        setError(null)
      })
      .catch((err: unknown) => {
        if (cancelled) return
        setTopics([])
        setError(err instanceof ApiError ? err.detail : String(err))
      })
    return () => {
      cancelled = true
    }
  }, [submitted, reloadKey])

  return (
    <div className="mx-auto w-full max-w-5xl px-4 py-8 sm:px-6">
      <Card className="p-5">
        <h1 className="text-lg font-semibold tracking-tight text-ink">Shared topics</h1>
        <p className="mt-1 text-sm text-ink-muted">
          Research other people have published. Each one is a finished snapshot — free to read,
          nothing to run.
        </p>
        <form
          className="mt-4 flex flex-wrap gap-2"
          onSubmit={(e) => {
            e.preventDefault()
            setSubmitted(query)
          }}
        >
          <label htmlFor="q" className="sr-only">
            Search shared topics
          </label>
          <input
            id="q"
            value={query}
            placeholder="Search by topic"
            onChange={(e) => setQuery(e.target.value)}
            className="min-w-0 flex-1 rounded-lg border border-line bg-surface-sunken px-3 py-2 text-sm text-ink placeholder:text-ink-faint focus-visible:outline-2 focus-visible:outline-offset-1 focus-visible:outline-accent"
          />
        </form>
      </Card>

      <section className="mt-8">
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-sm font-semibold tracking-wide text-ink uppercase">
            {submitted ? `Matching “${submitted}”` : 'Recently shared'}
          </h2>
          {topics && topics.length > 0 && (
            <span className="text-xs text-ink-faint">{topics.length} shown</span>
          )}
        </div>

        {error && (
          <div className="mb-4">
            <ErrorNote onRetry={() => setReloadKey((n) => n + 1)}>{error}</ErrorNote>
          </div>
        )}

        {topics === null ? (
          <Card className="p-5">
            <Skeleton lines={4} />
          </Card>
        ) : topics.length === 0 ? (
          <EmptyState title={submitted ? 'No shared topic matches that' : 'Nothing shared yet'}>
            {submitted
              ? 'Try a different word, or clear the search to see everything that has been shared.'
              : 'When someone publishes a finished topic, it shows up here for anyone to read.'}
          </EmptyState>
        ) : (
          <ul className="space-y-2">
            {topics.map((topic) => (
              <li key={topic.id}>
                <Link
                  to={`/shared/${topic.id}`}
                  className="block rounded-xl border border-line bg-surface-raised px-4 py-3.5 transition-colors hover:border-ink-faint focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent"
                >
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <p
                      className="line-clamp-2 min-w-0 flex-1 text-sm font-medium text-ink"
                      title={topic.topic}
                    >
                      {topic.topic}
                    </p>
                    <StateBadge state={topic.state} />
                  </div>
                  <div className="mt-2 flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-ink-faint">
                    {topic.published_at && (
                      <span title={absoluteTime(topic.published_at)}>
                        Shared {relativeTime(topic.published_at)}
                      </span>
                    )}
                    {topic.has_report && (
                      <>
                        <span aria-hidden="true">·</span>
                        <span>Report included</span>
                      </>
                    )}
                  </div>
                </Link>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  )
}
