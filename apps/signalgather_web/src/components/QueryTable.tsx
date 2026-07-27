import { useState } from 'react'
import type { PlannedQuery } from '../lib/types'
import { cx } from './primitives'

/**
 * The query plan the user approves at the gate. Read-only by design — editing
 * plans in the UI is explicitly out of scope for V1.
 */
export function QueryTable({ queries }: { queries: PlannedQuery[] }) {
  const [expanded, setExpanded] = useState<string | null>(null)

  if (queries.length === 0) {
    return <p className="px-4 py-6 text-sm text-ink-faint">This plan contains no queries.</p>
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[42rem] text-left text-sm">
        <thead className="text-xs tracking-wide text-ink-faint uppercase">
          <tr className="border-b border-line">
            <th scope="col" className="px-4 py-2 font-medium">
              #
            </th>
            <th scope="col" className="px-4 py-2 font-medium">
              Query
            </th>
            <th scope="col" className="px-4 py-2 font-medium">
              Intent
            </th>
            <th scope="col" className="px-4 py-2 font-medium">
              Lang
            </th>
            <th scope="col" className="px-4 py-2 font-medium">
              Freshness
            </th>
            <th scope="col" className="px-4 py-2 font-medium">
              Priority
            </th>
          </tr>
        </thead>
        <tbody>
          {queries.map((query, index) => {
            const id = query.id ?? `q${index + 1}`
            const open = expanded === id
            const hasMore = Boolean(query.rationale || query.covers_entity?.length || query.source_class)
            return (
              <tr
                key={id}
                onClick={() => hasMore && setExpanded(open ? null : id)}
                className={cx(
                  'border-b border-line/60 align-top',
                  hasMore && 'cursor-pointer hover:bg-surface-sunken',
                )}
              >
                <td className="px-4 py-2.5 font-mono text-xs text-ink-faint">{id}</td>
                <td className="px-4 py-2.5">
                  <span className="text-ink" lang={query.language}>
                    {query.query ?? '—'}
                  </span>
                  {open && hasMore && (
                    <dl className="mt-2 space-y-1 text-xs text-ink-muted">
                      {query.rationale && (
                        <div>
                          <dt className="inline font-medium">Why: </dt>
                          <dd className="inline">{query.rationale}</dd>
                        </div>
                      )}
                      {query.source_class && (
                        <div>
                          <dt className="inline font-medium">Sources: </dt>
                          <dd className="inline">{query.source_class}</dd>
                        </div>
                      )}
                      {query.covers_entity?.length ? (
                        <div>
                          <dt className="inline font-medium">Covers: </dt>
                          <dd className="inline">{query.covers_entity.join(', ')}</dd>
                        </div>
                      ) : null}
                    </dl>
                  )}
                </td>
                <td className="px-4 py-2.5">
                  <IntentTag intent={query.intent} />
                </td>
                <td className="px-4 py-2.5 font-mono text-xs text-ink-muted">
                  {query.language ?? '—'}
                </td>
                <td className="px-4 py-2.5 text-xs text-ink-muted">{query.freshness ?? '—'}</td>
                <td className="px-4 py-2.5 text-xs text-ink-muted">{query.priority ?? '—'}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

function IntentTag({ intent }: { intent?: string }) {
  if (!intent) return <span className="text-ink-faint">—</span>
  return (
    <span
      className={cx(
        'rounded-full border px-2 py-0.5 text-xs whitespace-nowrap',
        intent === 'monitoring'
          ? 'border-accent/50 bg-accent/10 text-accent'
          : 'border-line bg-surface-sunken text-ink-muted',
      )}
    >
      {intent}
    </span>
  )
}
