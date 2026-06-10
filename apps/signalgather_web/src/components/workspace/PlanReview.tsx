import { ClipboardList } from 'lucide-react'
import { Markdown } from '@/components/ui/Markdown'
import { Skeleton } from '@/components/ui/Skeleton'
import type { QueryPlan } from '@/lib/types'

export function PlanReview({
  introMd,
  parsed,
  loading,
  visible,
}: {
  introMd: string | null
  parsed: QueryPlan | null
  loading: boolean
  visible: boolean
}) {
  if (!visible && !loading) return null

  return (
    <div className="rounded-xl border border-border bg-surface-raised">
      <div className="flex items-center gap-2 px-4 py-3 border-b border-border">
        <ClipboardList className="h-4 w-4 text-warning" />
        <h2 className="text-sm font-medium text-text">Plan Review</h2>
        <span className="text-xs text-warning bg-warning/10 px-2 py-0.5 rounded-md border border-warning/20">
          Human gate
        </span>
      </div>

      <div className="p-4 space-y-4">
        {loading && !introMd ? (
          <div className="space-y-2">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-3/4" />
            <Skeleton className="h-24 w-full" />
          </div>
        ) : introMd ? (
          <Markdown content={introMd} />
        ) : (
          <p className="text-sm text-text-muted">Plan intro will appear when planning completes.</p>
        )}

        {parsed && (
          <div className="space-y-3">
            {parsed.working_thesis && (
              <div className="rounded-lg bg-surface-overlay p-3">
                <p className="text-xs font-medium text-text-muted mb-1">Working thesis</p>
                <p className="text-sm text-text">{parsed.working_thesis}</p>
              </div>
            )}

            {parsed.queries && parsed.queries.length > 0 && (
              <div>
                <p className="text-xs font-medium text-text-muted mb-2">
                  Search queries ({parsed.queries.length})
                </p>
                <div className="overflow-x-auto rounded-lg border border-border">
                  <table className="w-full text-xs">
                    <thead>
                      <tr className="bg-surface-overlay text-text-muted">
                        <th className="px-3 py-2 text-left font-medium">ID</th>
                        <th className="px-3 py-2 text-left font-medium">Query</th>
                        <th className="px-3 py-2 text-left font-medium">Lang</th>
                        <th className="px-3 py-2 text-left font-medium">Priority</th>
                      </tr>
                    </thead>
                    <tbody>
                      {parsed.queries.map((q) => (
                        <tr key={q.id} className="border-t border-border-subtle">
                          <td className="px-3 py-2 font-mono text-text-muted">{q.id}</td>
                          <td className="px-3 py-2 text-text">{q.query}</td>
                          <td className="px-3 py-2 text-text-muted">{q.language}</td>
                          <td className="px-3 py-2 text-text-muted">{q.priority ?? '—'}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
