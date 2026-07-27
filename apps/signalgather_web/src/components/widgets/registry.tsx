/**
 * type → component. The single place the frontend learns a new presentation.
 *
 * Adding a widget is one entry here plus a validator branch in
 * `lib/widgets/parse.ts`. Nothing in the report or plan screens changes, which
 * is the whole point of #16b: the agent chooses how its output looks.
 */

import type { ComponentType } from 'react'
import type {
  AnyWidget,
  CalloutWidget,
  EntityChipsWidget,
  HighlightsWidget,
  KeyFindingsWidget,
  MetricsWidget,
  NewsCardWidget,
  ScenarioTableWidget,
  SourceListWidget,
  WidgetType,
} from '../../lib/widgets/types'
import { useWidgetContext } from './WidgetContext'
import { MissingSource, SourceCard } from './SourceCard'
import { cx } from '../primitives'

function EntityChips({ widget }: { widget: EntityChipsWidget }) {
  return (
    <div className="my-3">
      {widget.label && (
        <p className="mb-1.5 text-xs font-medium tracking-wide text-ink-faint uppercase">
          {widget.label}
        </p>
      )}
      <div className="flex flex-wrap gap-1.5">
        {widget.items.map((item) => (
          <span
            key={item}
            className="rounded-full border border-accent/40 bg-accent/10 px-2.5 py-1 text-xs text-accent"
          >
            {item}
          </span>
        ))}
      </div>
    </div>
  )
}

function Highlights({ widget }: { widget: HighlightsWidget }) {
  return (
    <div className="my-3 rounded-lg border border-line bg-surface-sunken px-4 py-3">
      <p className="text-xs font-medium tracking-wide text-ink-faint uppercase">
        {widget.title ?? 'Highlights'}
      </p>
      <ul className="mt-2 space-y-1.5">
        {widget.items.map((item) => (
          <li key={item} className="flex gap-2 text-sm text-ink-muted">
            <span aria-hidden="true" className="mt-1.5 size-1.5 shrink-0 rounded-full bg-accent" />
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}

function NewsCard({ widget }: { widget: NewsCardWidget }) {
  const { sources } = useWidgetContext()
  const source = sources.get(widget.sourceId.toLowerCase())
  return (
    <div className="my-3">
      {source ? <SourceCard source={source} /> : <MissingSource sourceId={widget.sourceId} />}
    </div>
  )
}

function SourceListWidgetView({ widget }: { widget: SourceListWidget }) {
  const { sources } = useWidgetContext()
  const selected = widget.sourceIds
    ? widget.sourceIds.map((id) => ({ id, source: sources.get(id.toLowerCase()) }))
    : [...sources.values()].map((source) => ({ id: source.id, source }))

  if (selected.length === 0) {
    return <p className="my-3 text-sm text-ink-faint">No sources to show.</p>
  }

  return (
    <div className="my-3 space-y-2">
      {widget.title && (
        <p className="text-xs font-medium tracking-wide text-ink-faint uppercase">{widget.title}</p>
      )}
      {selected.map(({ id, source }) =>
        source ? (
          <SourceCard key={id} source={source} compact />
        ) : (
          <MissingSource key={id} sourceId={id} />
        ),
      )}
    </div>
  )
}

const CONFIDENCE_STYLE: Record<string, string> = {
  high: 'border-positive/50 bg-positive/10 text-positive',
  medium: 'border-warning/50 bg-warning/10 text-warning',
  low: 'border-line bg-surface-sunken text-ink-faint',
}

function KeyFindings({ widget }: { widget: KeyFindingsWidget }) {
  return (
    <div className="my-3">
      <p className="mb-2 text-xs font-medium tracking-wide text-ink-faint uppercase">
        {widget.title ?? 'Key findings'}
      </p>
      <ol className="space-y-2">
        {widget.findings.map((row, index) => (
          <li
            key={`${index}-${row.finding.slice(0, 24)}`}
            className="rounded-lg border border-line bg-surface-sunken px-3.5 py-2.5"
          >
            <p className="text-sm text-ink">{row.finding}</p>
            <div className="mt-1.5 flex flex-wrap items-center gap-2 text-xs">
              {row.confidence && (
                <span
                  className={cx(
                    'rounded-full border px-1.5 py-0.5',
                    CONFIDENCE_STYLE[row.confidence] ?? 'border-line text-ink-faint',
                  )}
                >
                  {row.confidence} confidence
                </span>
              )}
              {row.source_ids?.length ? (
                <span className="font-mono text-ink-faint">[{row.source_ids.join(', ')}]</span>
              ) : null}
            </div>
          </li>
        ))}
      </ol>
    </div>
  )
}

const VERDICT_STYLE: Record<string, string> = {
  supports: 'text-positive',
  weakens: 'text-warning',
  kills: 'text-danger',
  neutral: 'text-ink-faint',
}

function ScenarioTable({ widget }: { widget: ScenarioTableWidget }) {
  return (
    <div className="my-3">
      <p className="mb-2 text-xs font-medium tracking-wide text-ink-faint uppercase">
        {widget.title ?? 'Scenarios'}
      </p>
      <div className="overflow-x-auto rounded-lg border border-line">
        <table className="w-full min-w-[34rem] text-left text-sm">
          <thead className="text-xs tracking-wide text-ink-faint uppercase">
            <tr className="border-b border-line">
              <th className="px-3 py-2 font-medium">Scenario</th>
              <th className="px-3 py-2 font-medium">Before</th>
              <th className="px-3 py-2 font-medium">After</th>
              <th className="px-3 py-2 font-medium">Verdict</th>
            </tr>
          </thead>
          <tbody>
            {widget.scenarios.map((row, index) => (
              <tr key={row.id ?? index} className="border-b border-line/60 align-top last:border-0">
                <td className="px-3 py-2.5">
                  <span className="text-ink">{row.label ?? row.id ?? `#${index + 1}`}</span>
                  {(row.premise ?? row.rationale) && (
                    <p className="mt-0.5 text-xs text-ink-muted">{row.rationale ?? row.premise}</p>
                  )}
                  {row.evidence_ids?.length ? (
                    <p className="mt-1 font-mono text-xs text-ink-faint">
                      [{row.evidence_ids.join(', ')}]
                    </p>
                  ) : null}
                </td>
                <td className="px-3 py-2.5 font-mono text-xs text-ink-muted">
                  {pct(row.p_before)}
                </td>
                <td className="px-3 py-2.5 font-mono text-xs text-ink-muted">{pct(row.p_after)}</td>
                <td
                  className={cx(
                    'px-3 py-2.5 text-xs',
                    VERDICT_STYLE[row.verdict ?? ''] ?? 'text-ink-muted',
                  )}
                >
                  {row.verdict ?? '—'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function pct(value: number | undefined): string {
  if (typeof value !== 'number') return '—'
  // Probabilities arrive either as 0–1 or already as percentages.
  return `${Math.round(value <= 1 ? value * 100 : value)}%`
}

const TONE_STYLE: Record<string, string> = {
  info: 'border-accent/40 bg-accent/10',
  good: 'border-positive/40 bg-positive/10',
  warn: 'border-warning/40 bg-warning/10',
  risk: 'border-danger/40 bg-danger/10',
}

function Callout({ widget }: { widget: CalloutWidget }) {
  return (
    <aside
      className={cx(
        'my-3 rounded-lg border px-4 py-3',
        TONE_STYLE[widget.tone ?? 'info'] ?? TONE_STYLE.info,
      )}
    >
      {widget.title && <p className="text-sm font-semibold text-ink">{widget.title}</p>}
      <p className="mt-0.5 text-sm text-ink-muted">{widget.body}</p>
    </aside>
  )
}

function Metrics({ widget }: { widget: MetricsWidget }) {
  return (
    <dl className="my-3 grid grid-cols-2 gap-2 sm:grid-cols-4">
      {widget.items.map((item) => (
        <div
          key={item.label}
          className="rounded-lg border border-line bg-surface-sunken px-3 py-2.5"
          title={item.hint}
        >
          <dt className="text-xs text-ink-faint">{item.label}</dt>
          <dd className="mt-0.5 text-lg font-semibold text-ink tabular-nums">{item.value}</dd>
        </div>
      ))}
    </dl>
  )
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any -- registry erases the per-type prop
const REGISTRY: Record<WidgetType, ComponentType<{ widget: any }>> = {
  'entity-chips': EntityChips,
  highlights: Highlights,
  'news-card': NewsCard,
  'source-list': SourceListWidgetView,
  'key-findings': KeyFindings,
  'scenario-table': ScenarioTable,
  callout: Callout,
  metrics: Metrics,
}

/** Widget types this build can render — used by tests and the docs table. */
export const REGISTERED_WIDGETS = Object.keys(REGISTRY) as WidgetType[]

export function WidgetRenderer({ widget }: { widget: AnyWidget }) {
  if (widget.type === 'unknown') return <UnknownWidgetView widget={widget} />
  const Component = REGISTRY[widget.type]
  if (!Component) {
    return (
      <UnknownWidgetView
        widget={{
          type: 'unknown',
          declaredType: widget.type,
          raw: '',
          reason: 'no renderer is registered for this widget type',
        }}
      />
    )
  }
  return <Component widget={widget} />
}

/**
 * Visible degradation. An agent that ships a widget ahead of the frontend must
 * not silently blank a section of the report — the operator has to be able to
 * tell "nothing was said" from "we could not draw it".
 */
function UnknownWidgetView({
  widget,
}: {
  widget: Extract<AnyWidget, { type: 'unknown' }>
}) {
  return (
    <details className="my-3 rounded-lg border border-dashed border-warning/50 bg-warning/5 px-3.5 py-2.5">
      <summary className="cursor-pointer text-xs text-warning">
        Cannot display {widget.declaredType ? <code>{widget.declaredType}</code> : 'a widget'} —{' '}
        {widget.reason}
      </summary>
      {widget.raw && (
        <pre className="mt-2 max-h-48 overflow-auto font-mono text-[0.7rem] whitespace-pre-wrap text-ink-muted">
          {widget.raw}
        </pre>
      )}
    </details>
  )
}
