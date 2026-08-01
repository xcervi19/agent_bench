import { useCallback, useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { ApiError, createTopic, listTopics } from '../lib/api'
import { absoluteTime, relativeTime } from '../lib/format'
import { hasUnseenActivity } from '../lib/lastSeen'
import type { TopicListItem } from '../lib/types'
import { StateBadge } from '../components/StateBadge'
import { Button, Card, EmptyState, ErrorNote, Skeleton } from '../components/primitives'

const EXAMPLE = 'Hormuz strait closure — options to lower crude price exposure'

/**
 * Home: everything the signed-in user owns, newest activity first, plus the
 * single natural-language field that starts a new topic.
 */
export function TopicListPage() {
  const navigate = useNavigate()
  const [topics, setTopics] = useState<TopicListItem[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  // Bumping the key is the only way to re-run the fetch; that keeps every
  // setState inside a promise callback instead of the effect body.
  const [reloadKey, setReloadKey] = useState(0)
  const reload = useCallback(() => setReloadKey((key) => key + 1), [])

  useEffect(() => {
    let cancelled = false
    listTopics()
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
  }, [reloadKey])

  return (
    <div className="mx-auto w-full max-w-5xl px-4 py-8 sm:px-6">
      <NewTopicForm
        onCreated={(id) => navigate(`/topics/${id}`)}
        onError={(message) => setError(message)}
      />

      <section className="mt-8">
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-sm font-semibold tracking-wide text-ink uppercase">Your topics</h2>
          {topics && topics.length > 0 && (
            <span className="text-xs text-ink-faint">{topics.length} total</span>
          )}
        </div>

        {error && (
          <div className="mb-4">
            <ErrorNote onRetry={reload}>{error}</ErrorNote>
          </div>
        )}

        {topics === null ? (
          <Card className="p-5">
            <Skeleton lines={4} />
          </Card>
        ) : topics.length === 0 ? (
          <EmptyState title="No topics yet">
            Describe what you want to track in plain language above. SignalGather plans the
            research, shows you the plan for approval, then gathers and reports on it.
          </EmptyState>
        ) : (
          <ul className="space-y-2">
            {topics.map((topic) => (
              <li key={topic.id}>
                <TopicRow topic={topic} />
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  )
}

function TopicRow({ topic }: { topic: TopicListItem }) {
  const needsYou = topic.state === 'planned_awaiting_review'
  // Computed once per render of the row; the value only changes when the list
  // refetches, which is exactly when it should.
  const unseen = hasUnseenActivity(topic.id, topic.updated_at)
  return (
    <Link
      to={`/topics/${topic.id}`}
      className="block rounded-xl border border-line bg-surface-raised px-4 py-3.5 transition-colors hover:border-ink-faint focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent"
    >
      <div className="flex flex-wrap items-start justify-between gap-3">
        <p className="line-clamp-2 min-w-0 flex-1 text-sm font-medium text-ink" title={topic.topic}>
          {topic.topic}
        </p>
        <StateBadge state={topic.state} />
      </div>
      <div className="mt-2 flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-ink-faint">
        <span title={absoluteTime(topic.updated_at)}>
          Updated {relativeTime(topic.updated_at)}
        </span>
        <span aria-hidden="true">·</span>
        <span title={absoluteTime(topic.created_at)}>
          Created {relativeTime(topic.created_at)}
        </span>
        {topic.is_public && (
          <span
            className="rounded-full bg-positive/15 px-2 py-0.5 font-medium text-positive"
            title="Published — anyone with the link can read it, and it is frozen until you stop sharing"
          >
            Shared
          </span>
        )}
        {needsYou && (
          <span className="rounded-full bg-warning/15 px-2 py-0.5 font-medium text-warning">
            Needs your review
          </span>
        )}
        {unseen && !needsYou && (
          <span className="rounded-full bg-accent/15 px-2 py-0.5 font-medium text-accent">
            New since your last visit
          </span>
        )}
      </div>
    </Link>
  )
}

function NewTopicForm({
  onCreated,
  onError,
}: {
  onCreated: (topicId: string) => void
  onError: (message: string) => void
}) {
  const [value, setValue] = useState('')
  const [busy, setBusy] = useState(false)

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    const topic = value.trim()
    if (!topic) return
    setBusy(true)
    try {
      const created = await createTopic(topic)
      onCreated(created.topic_id)
    } catch (err) {
      onError(err instanceof ApiError ? err.detail : String(err))
    } finally {
      setBusy(false)
    }
  }

  return (
    <Card className="p-5">
      <h1 className="text-lg font-semibold tracking-tight text-ink">Track a new topic</h1>
      <p className="mt-1 text-sm text-ink-muted">
        Describe it the way you would to an analyst. You approve the research plan before any
        searching starts.
      </p>
      <form onSubmit={onSubmit} className="mt-4 space-y-3">
        <label htmlFor="topic" className="sr-only">
          Topic
        </label>
        <textarea
          id="topic"
          rows={3}
          required
          value={value}
          placeholder={EXAMPLE}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => {
            // Long topics need newlines; Cmd/Ctrl+Enter submits.
            if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) e.currentTarget.form?.requestSubmit()
          }}
          className="w-full resize-y rounded-lg border border-line bg-surface-sunken px-3 py-2.5 text-sm text-ink placeholder:text-ink-faint focus-visible:outline-2 focus-visible:outline-offset-1 focus-visible:outline-accent"
        />
        <div className="flex flex-wrap items-center justify-between gap-3">
          <span className="text-xs text-ink-faint">⌘/Ctrl + Enter to start</span>
          <Button type="submit" variant="primary" busy={busy} disabled={!value.trim()}>
            Start planning
          </Button>
        </div>
      </form>
    </Card>
  )
}
