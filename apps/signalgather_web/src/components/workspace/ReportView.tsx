import { FileText, Lightbulb, Target } from 'lucide-react'
import { Markdown } from '@/components/ui/Markdown'
import { Skeleton } from '@/components/ui/Skeleton'
import { SourcesList } from './SourcesList'
import type { NewsArtifact, ReportArtifact } from '@/lib/types'
import { buildSourceMap, resolveCitations } from '@/lib/utils'

export function ReportView({
  reportMd,
  report,
  news,
  loading,
  visible,
}: {
  reportMd: string | null
  report: ReportArtifact | null
  news: NewsArtifact | null
  loading: boolean
  visible: boolean
}) {
  if (!visible && !loading) return null

  const sourceMap = buildSourceMap(news?.sources ?? [])
  const resolvedMd = reportMd
    ? resolveCitations(reportMd, sourceMap)
    : report?.summary_md
      ? resolveCitations(report.summary_md, sourceMap)
      : null

  return (
    <div className="rounded-xl border border-border bg-surface-raised">
      <div className="flex items-center gap-2 px-4 py-3 border-b border-border">
        <FileText className="h-4 w-4 text-success" />
        <h2 className="text-sm font-medium text-text">Strategic Report</h2>
        {report?.thesis_status && (
          <span className="text-xs bg-success/10 text-success px-2 py-0.5 rounded-md border border-success/20 capitalize">
            Thesis: {report.thesis_status}
          </span>
        )}
      </div>

      <div className="p-4 space-y-6">
        {loading && !resolvedMd ? (
          <div className="space-y-2">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-5/6" />
            <Skeleton className="h-32 w-full" />
          </div>
        ) : resolvedMd ? (
          <Markdown content={resolvedMd} />
        ) : (
          <p className="text-sm text-text-muted">
            Report will appear when delivery completes.
          </p>
        )}

        {report?.key_findings && report.key_findings.length > 0 && (
          <div>
            <div className="flex items-center gap-2 mb-3">
              <Lightbulb className="h-4 w-4 text-warning" />
              <h3 className="text-sm font-medium text-text">Key Findings</h3>
            </div>
            <div className="space-y-2">
              {report.key_findings.map((f, i) => (
                <div
                  key={i}
                  className="rounded-lg border border-border bg-surface p-3 text-left"
                >
                  <p className="text-sm text-text">{f.finding}</p>
                  <div className="mt-1 flex gap-2 text-[10px] text-text-muted">
                    {f.confidence && (
                      <span className="capitalize">Confidence: {f.confidence}</span>
                    )}
                    {f.source_ids && (
                      <span className="font-mono">{f.source_ids.join(', ')}</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {report?.scenarios && report.scenarios.length > 0 && (
          <div>
            <div className="flex items-center gap-2 mb-3">
              <Target className="h-4 w-4 text-accent" />
              <h3 className="text-sm font-medium text-text">Scenarios</h3>
            </div>
            <div className="grid gap-2 sm:grid-cols-2">
              {report.scenarios.map((s, i) => (
                <div
                  key={i}
                  className="rounded-lg border border-border bg-surface p-3 text-left"
                >
                  <div className="flex items-center justify-between mb-1">
                    <p className="text-sm font-medium text-text">{s.name}</p>
                    {s.probability && (
                      <span className="text-xs text-accent">{s.probability}</span>
                    )}
                  </div>
                  {s.summary && <p className="text-xs text-text-muted">{s.summary}</p>}
                </div>
              ))}
            </div>
          </div>
        )}

        {news && <SourcesList sources={news.sources} />}
      </div>
    </div>
  )
}
