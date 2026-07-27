import { useState } from 'react'
import { cancelTopic, proceedTopic } from '../lib/api'
import type { IntroArtifact, ParsedArtifact, TopicDetail } from '../lib/types'
import { Markdown } from './Markdown'
import { QueryTable } from './QueryTable'
import { Button, Card, ErrorNote, SectionHeading, Skeleton, cx } from './primitives'

type Tab = 'brief' | 'queries'

/**
 * The human review gate: what the agent understood, and the queries it wants to
 * run. Proceed/Cancel are only live in `planned_awaiting_review` — the server
 * answers 409 otherwise, so the buttons mirror that instead of inviting a click.
 */
export function PlanReview({
  topic,
  intro,
  introMarkdown,
  parsed,
  loading,
  onDecision,
}: {
  topic: TopicDetail
  intro: IntroArtifact | null
  introMarkdown: string | null
  parsed: ParsedArtifact | null
  loading: boolean
  onDecision: () => void
}) {
  const [tab, setTab] = useState<Tab>('brief')
  const [pending, setPending] = useState<'proceed' | 'cancel' | null>(null)
  const [error, setError] = useState<string | null>(null)

  const atGate = topic.state === 'planned_awaiting_review'
  const queries = parsed?.queries ?? []
  const nothingYet = !loading && !introMarkdown && !intro && !parsed

  async function decide(action: 'proceed' | 'cancel') {
    setPending(action)
    setError(null)
    try {
      if (action === 'proceed') await proceedTopic(topic.id)
      else await cancelTopic(topic.id)
      onDecision()
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err))
    } finally {
      setPending(null)
    }
  }

  return (
    <Card>
      <SectionHeading
        aside={
          <div className="flex gap-1" role="tablist" aria-label="Plan sections">
            <TabButton active={tab === 'brief'} onClick={() => setTab('brief')}>
              Brief
            </TabButton>
            <TabButton active={tab === 'queries'} onClick={() => setTab('queries')}>
              Queries{queries.length ? ` (${queries.length})` : ''}
            </TabButton>
          </div>
        }
      >
        Plan review
      </SectionHeading>

      {loading && !introMarkdown && (
        <div className="px-4 py-5">
          <Skeleton lines={5} />
        </div>
      )}

      {nothingYet && (
        <p className="px-4 py-6 text-sm text-ink-muted">
          The agent is still drafting the plan. This panel fills in as soon as{' '}
          <code className="font-mono text-xs">intro.md</code> is written.
        </p>
      )}

      {tab === 'brief' && (introMarkdown || intro) && (
        <div className="space-y-4 px-4 py-4">
          {intro?.approach && <ApproachChips intro={intro} />}
          {introMarkdown ? (
            <Markdown source={introMarkdown} />
          ) : (
            <IntroFallback intro={intro!} />
          )}
        </div>
      )}

      {tab === 'queries' && (parsed ? <QueryTable queries={queries} /> : <NoParsed loading={loading} />)}

      <div className="flex flex-wrap items-center justify-between gap-3 border-t border-line px-4 py-3">
        <p className="text-xs text-ink-muted">
          {atGate
            ? intro?.next_step ?? 'Proceed starts web search and source collection.'
            : 'Review is closed for this topic — its state has moved on.'}
        </p>
        <div className="flex gap-2">
          <Button
            variant="danger"
            disabled={!topic.available_actions.includes('cancel')}
            busy={pending === 'cancel'}
            onClick={() => decide('cancel')}
          >
            Cancel topic
          </Button>
          <Button
            variant="primary"
            disabled={!atGate}
            busy={pending === 'proceed'}
            onClick={() => decide('proceed')}
          >
            Proceed
          </Button>
        </div>
      </div>

      {error && (
        <div className="px-4 pb-4">
          <ErrorNote>{error}</ErrorNote>
        </div>
      )}
    </Card>
  )
}

function TabButton({
  active,
  onClick,
  children,
}: {
  active: boolean
  onClick: () => void
  children: React.ReactNode
}) {
  return (
    <button
      role="tab"
      aria-selected={active}
      onClick={onClick}
      className={cx(
        'rounded-md px-2.5 py-1 text-xs font-medium transition-colors',
        active ? 'bg-accent/15 text-accent' : 'text-ink-muted hover:text-ink',
      )}
    >
      {children}
    </button>
  )
}

function ApproachChips({ intro }: { intro: IntroArtifact }) {
  const { queries_count, languages, regions, key_actors_top5 } = intro.approach ?? {}
  const chips: string[] = []
  if (queries_count) chips.push(`${queries_count} queries`)
  if (languages?.length) chips.push(languages.join(' · '))
  if (regions?.length) chips.push(regions.join(' · '))
  if (chips.length === 0 && !key_actors_top5?.length) return null

  return (
    <div className="flex flex-wrap gap-1.5">
      {chips.map((chip) => (
        <span
          key={chip}
          className="rounded-full border border-line bg-surface-sunken px-2.5 py-1 text-xs text-ink-muted"
        >
          {chip}
        </span>
      ))}
      {key_actors_top5?.map((actor) => (
        <span
          key={actor}
          className="rounded-full border border-accent/40 bg-accent/10 px-2.5 py-1 text-xs text-accent"
        >
          {actor}
        </span>
      ))}
    </div>
  )
}

/** intro.md is the preferred surface; intro.json keeps the gate usable without it. */
function IntroFallback({ intro }: { intro: IntroArtifact }) {
  return (
    <div className="space-y-3 text-sm">
      {intro.headline && <h3 className="text-base font-semibold text-ink">{intro.headline}</h3>}
      {intro.understanding && <p className="text-ink-muted">{intro.understanding}</p>}
      {intro.current_state_short && (
        <Field label="Current state">{intro.current_state_short}</Field>
      )}
      {intro.working_thesis_short && (
        <Field label="Working thesis">{intro.working_thesis_short}</Field>
      )}
      {intro.highlights?.length ? (
        <ul className="list-disc space-y-1 pl-5 text-ink-muted">
          {intro.highlights.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      ) : null}
    </div>
  )
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <p className="text-xs font-medium tracking-wide text-ink-faint uppercase">{label}</p>
      <p className="mt-0.5 text-ink-muted">{children}</p>
    </div>
  )
}

function NoParsed({ loading }: { loading: boolean }) {
  return (
    <div className="px-4 py-6">
      {loading ? (
        <Skeleton lines={4} />
      ) : (
        <p className="text-sm text-ink-muted">
          The query plan (<code className="font-mono text-xs">parsed.json</code>) is not on disk yet.
        </p>
      )}
    </div>
  )
}
