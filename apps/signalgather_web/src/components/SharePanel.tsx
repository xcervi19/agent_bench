import { useState } from 'react'
import { ApiError, publishTopic, setShareMode, unpublishTopic } from '../lib/api'
import { shareUrl } from '../lib/publicApi'
import { absoluteTime, relativeTime } from '../lib/format'
import type { ShareMode, TopicDetail } from '../lib/types'
import { Button, Card, ErrorNote, SectionHeading, cx } from './primitives'

/**
 * Publish a finished topic so anyone can read it (#40), live or pinned (#50).
 *
 * The panel leads with the choice because the choice is the feature. Sharing
 * live is the default and costs the owner nothing: the topic keeps refreshing,
 * monitoring keeps running, and the link keeps up. Sharing a snapshot stops the
 * topic for everyone until it is unshared — worth having for "the picture as of
 * today", worth being explicit about the rest of the time.
 *
 * What does not change between them: readers can only read. That is structural
 * — the public client has no write call and the public router has no write
 * route — so it is stated once rather than sold twice.
 */
export function SharePanel({
  topic,
  onChanged,
}: {
  topic: TopicDetail
  onChanged: () => void
}) {
  const [pending, setPending] = useState<'publish' | 'unpublish' | ShareMode | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [copied, setCopied] = useState(false)
  const [chosen, setChosen] = useState<ShareMode>('live')

  const canPublish = topic.state === 'reported'
  const url = shareUrl(topic.id)
  const live = topic.share_mode !== 'frozen'

  async function run(action: 'publish' | 'unpublish' | ShareMode) {
    setPending(action)
    setError(null)
    setCopied(false)
    try {
      if (action === 'publish') await publishTopic(topic.id, chosen)
      else if (action === 'unpublish') await unpublishTopic(topic.id)
      else await setShareMode(topic.id, action)
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
            {topic.is_public ? (live ? 'Shared · live' : 'Shared · snapshot') : 'Private'}
          </span>
        }
      >
        Sharing
      </SectionHeading>

      {topic.is_public ? (
        <div className="space-y-4 px-4 py-5">
          <p className="text-sm text-ink-muted">
            {live
              ? 'Anyone with this link can read the report, the sources and the plan — no account needed. They cannot change anything, and the page keeps up as this topic updates.'
              : 'Anyone with this link can read the report, the sources and the plan — no account needed. It shows the state you pinned, and nothing on this topic runs while it stays pinned.'}
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
              {!live && topic.frozen_at && (
                <span title={absoluteTime(topic.frozen_at)}>
                  {' '}
                  Pinned {relativeTime(topic.frozen_at)}.
                </span>
              )}
            </p>
          )}

          <div className="space-y-3 border-t border-line pt-4">
            <p className="text-xs text-ink-muted">
              {live
                ? 'Pin it to a snapshot if you need the link to stop moving — that pauses monitoring and holds the report where it is.'
                : 'Switch back to live to keep working on this topic. Monitoring stays off until you turn it back on.'}
            </p>
            <div className="flex flex-wrap items-center justify-between gap-3">
              <Button
                variant="secondary"
                busy={pending === (live ? 'frozen' : 'live')}
                onClick={() => run(live ? 'frozen' : 'live')}
              >
                {live ? 'Pin to a snapshot' : 'Switch to live'}
              </Button>
              <Button
                variant="danger"
                busy={pending === 'unpublish'}
                onClick={() => run('unpublish')}
              >
                Stop sharing
              </Button>
            </div>
            <p className="text-xs text-ink-faint">
              Stopping kills the link immediately. The topic itself stays yours either way.
            </p>
          </div>
        </div>
      ) : (
        <div className="space-y-4 px-4 py-5">
          <p className="text-sm text-ink-muted">
            Sharing publishes this topic — report, sources, plan and refresh history — readable
            by anyone with the link and findable in the shared list.
          </p>

          <div role="radiogroup" aria-label="What sharing does" className="space-y-2">
            <ModeChoice
              mode="live"
              chosen={chosen}
              onChoose={setChosen}
              title="Live"
              detail="The page keeps up with the topic. You keep every control — refresh, monitoring, settings — and readers see each update once it finishes."
            />
            <ModeChoice
              mode="frozen"
              chosen={chosen}
              onChoose={setChosen}
              title="Snapshot"
              detail="The link shows this exact state. Monitoring pauses and the topic is read-only for you too, until you unpin or stop sharing."
            />
          </div>

          <p className="text-sm text-ink-muted">
            Either way, readers cannot proceed, cancel, refresh or monitor — the public API has
            no route that would let them.
          </p>

          <div className="flex flex-wrap items-center justify-between gap-3 border-t border-line pt-4">
            <p className="text-xs text-ink-muted">
              {canPublish
                ? 'You can stop sharing at any time.'
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

function ModeChoice({
  mode,
  chosen,
  onChoose,
  title,
  detail,
}: {
  mode: ShareMode
  chosen: ShareMode
  onChoose: (mode: ShareMode) => void
  title: string
  detail: string
}) {
  const selected = chosen === mode
  return (
    <button
      type="button"
      role="radio"
      aria-checked={selected}
      onClick={() => onChoose(mode)}
      className={cx(
        'w-full rounded-lg border px-3 py-2.5 text-left transition-colors',
        selected
          ? 'border-accent/60 bg-accent/10'
          : 'border-line bg-surface-sunken hover:border-accent/40',
      )}
    >
      <span className="text-sm font-medium text-ink">{title}</span>
      <span className="mt-0.5 block text-xs text-ink-muted">{detail}</span>
    </button>
  )
}

/** Shown across the workspace while a topic is published, not only on its tab. */
export function PublishedBanner({ topic }: { topic: TopicDetail }) {
  if (!topic.is_public) return null
  const live = topic.share_mode !== 'frozen'
  return (
    <div className="rounded-xl border border-positive/40 bg-positive/10 px-4 py-3 text-sm text-ink">
      <span className="font-medium">
        {live ? 'This topic is shared publicly — live.' : 'This topic is shared as a snapshot.'}
      </span>{' '}
      <span className="text-ink-muted">
        {live
          ? 'Readers see it update as you refresh it, and cannot change anything. You keep full control.'
          : 'It is read-only until you switch it back to live or stop sharing — actions and monitoring are paused so the state everyone sees stays the one you pinned.'}
      </span>
    </div>
  )
}
