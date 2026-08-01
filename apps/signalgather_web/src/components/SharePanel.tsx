import { useState } from 'react'
import { ApiError, publishTopic, unpublishTopic } from '../lib/api'
import { shareUrl } from '../lib/publicApi'
import { absoluteTime, relativeTime } from '../lib/format'
import type { TopicDetail } from '../lib/types'
import { Button, Card, ErrorNote, SectionHeading } from './primitives'

/**
 * Publish a finished topic so anyone can read it (#40).
 *
 * The panel is blunt about the trade because the trade is the feature: what you
 * share is this exact state, and while it is shared the topic is frozen —
 * monitoring pauses, refresh and the pipeline actions are refused. That is what
 * makes the link safe to hand to someone with no account: there is nothing on
 * the other end of it for them to press.
 */
export function SharePanel({
  topic,
  onChanged,
}: {
  topic: TopicDetail
  onChanged: () => void
}) {
  const [pending, setPending] = useState<'publish' | 'unpublish' | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [copied, setCopied] = useState(false)

  const canPublish = topic.state === 'reported'
  const url = shareUrl(topic.id)

  async function run(action: 'publish' | 'unpublish') {
    setPending(action)
    setError(null)
    setCopied(false)
    try {
      if (action === 'publish') await publishTopic(topic.id)
      else await unpublishTopic(topic.id)
      onChanged()
    } catch (err) {
      setError(err instanceof ApiError ? err.detail : String(err))
    } finally {
      setPending(null)
    }
  }

  async function copy() {
    try {
      await navigator.clipboard.writeText(url)
      setCopied(true)
    } catch {
      // Clipboard access can be denied (insecure origin, permission). The input
      // below is selectable, so the link is never actually out of reach.
      setCopied(false)
      setError('Could not copy automatically — select the link and copy it.')
    }
  }

  return (
    <Card>
      <SectionHeading
        aside={
          <span
            className={
              topic.is_public
                ? 'rounded-full border border-positive/50 bg-positive/10 px-2.5 py-1 text-xs font-medium text-positive'
                : 'rounded-full border border-line bg-surface-sunken px-2.5 py-1 text-xs font-medium text-ink-faint'
            }
          >
            {topic.is_public ? 'Shared' : 'Private'}
          </span>
        }
      >
        Sharing
      </SectionHeading>

      {topic.is_public ? (
        <div className="space-y-4 px-4 py-5">
          <p className="text-sm text-ink-muted">
            Anyone with this link can read the report, the sources and the plan — no account
            needed. They cannot change anything, and nothing on this topic runs while it is
            shared.
          </p>

          <div className="flex flex-wrap items-center gap-2">
            <input
              readOnly
              value={url}
              aria-label="Public link"
              onFocus={(e) => e.currentTarget.select()}
              className="min-w-0 flex-1 rounded-lg border border-line bg-surface-sunken px-3 py-2 font-mono text-xs text-ink"
            />
            <Button variant="secondary" onClick={copy}>
              {copied ? 'Copied' : 'Copy link'}
            </Button>
          </div>

          {topic.published_at && (
            <p className="text-xs text-ink-faint" title={absoluteTime(topic.published_at)}>
              Shared {relativeTime(topic.published_at)}.
            </p>
          )}

          <div className="flex flex-wrap items-center justify-between gap-3 border-t border-line pt-4">
            <p className="text-xs text-ink-muted">
              Stop sharing to edit, refresh or monitor this topic again. The link stops working
              immediately; monitoring stays paused until you turn it back on.
            </p>
            <Button variant="danger" busy={pending === 'unpublish'} onClick={() => run('unpublish')}>
              Stop sharing
            </Button>
          </div>
        </div>
      ) : (
        <div className="space-y-4 px-4 py-5">
          <p className="text-sm text-ink-muted">
            Sharing publishes this topic as it stands right now: report, sources, plan and
            refresh history, readable by anyone with the link and findable in the shared list.
          </p>
          <ul className="space-y-1.5 text-sm text-ink-muted">
            <Point>Readers cannot proceed, cancel, refresh or monitor — the API refuses.</Point>
            <Point>Monitoring pauses, so a shared topic never runs up cost on its own.</Point>
            <Point>You can stop sharing at any time and pick the topic back up.</Point>
          </ul>

          <div className="flex flex-wrap items-center justify-between gap-3 border-t border-line pt-4">
            <p className="text-xs text-ink-muted">
              {canPublish
                ? 'Publishing freezes the topic until you stop sharing it.'
                : `Only a finished topic can be shared. This one is ${topic.state}.`}
            </p>
            <Button
              variant="primary"
              disabled={!canPublish}
              busy={pending === 'publish'}
              onClick={() => run('publish')}
            >
              Share publicly
            </Button>
          </div>
        </div>
      )}

      {error && (
        <div className="px-4 pb-4">
          <ErrorNote>{error}</ErrorNote>
        </div>
      )}
    </Card>
  )
}

function Point({ children }: { children: React.ReactNode }) {
  return (
    <li className="flex gap-2">
      <span aria-hidden="true" className="text-ink-faint">
        ·
      </span>
      <span>{children}</span>
    </li>
  )
}

/** Shown across the workspace while a topic is published, not only on its tab. */
export function PublishedBanner({ topic }: { topic: TopicDetail }) {
  if (!topic.is_public) return null
  return (
    <div className="rounded-xl border border-positive/40 bg-positive/10 px-4 py-3 text-sm text-ink">
      <span className="font-medium">This topic is shared publicly.</span>{' '}
      <span className="text-ink-muted">
        It is read-only until you stop sharing — actions and monitoring are paused so the
        snapshot everyone sees stays the one you published.
      </span>
    </div>
  )
}
