import type { NewsArtifact, ReportArtifact } from '../../lib/types'
import { ArtifactMarkdown } from '../ArtifactMarkdown'
import { WidgetRenderer } from '../widgets/registry'
import { WidgetContext } from '../widgets/WidgetContext'
import { indexSources } from '../../lib/citations'
import { SourceMixNote } from './SourceMixNote'
import { ThesisBadge } from './ThesisBadge'
import { Card, SectionHeading, Skeleton } from '../primitives'
import { useMemo } from 'react'

/**
 * The finished report (16b).
 *
 * `report.md` is the agent's own narrative and is rendered through the widget
 * pipeline, so anything it declares is drawn without this component knowing the
 * type. The structured blocks below it come from `report.json` and are rendered
 * through the *same* registry — key findings and scenarios are widgets, not
 * bespoke JSX, so the two paths can never drift apart.
 */
export function ReportView({
  report,
  reportMarkdown,
  news,
  loading,
}: {
  report: ReportArtifact | null
  reportMarkdown: string | null
  news: NewsArtifact | null
  loading: boolean
}) {
  const sources = useMemo(() => indexSources(news?.sources), [news])

  if (loading && !reportMarkdown && !report) {
    return (
      <Card className="p-5">
        <Skeleton lines={6} />
      </Card>
    )
  }

  if (!reportMarkdown && !report) {
    return (
      <Card>
        <SectionHeading>Report</SectionHeading>
        <p className="px-4 py-6 text-sm text-ink-muted">
          The report artifacts are not on disk for this run. If the topic reached{' '}
          <code className="font-mono text-xs">reported</code>, check the deliver run directory on
          the server.
        </p>
      </Card>
    )
  }

  const findings = report?.key_findings?.filter((row) => row.finding) ?? []
  const scenarios = report?.scenario_updates ?? []

  return (
    <div className="space-y-5">
      <Card>
        <SectionHeading aside={<ThesisBadge status={report?.thesis_status} />}>
          Report
        </SectionHeading>

        <div className="border-b border-line bg-surface-sunken px-4 py-4">
          <SourceMixNote sources={news?.sources} className="mb-3" />
          {report?.summary_md && (
            <>
              <p className="mb-2 text-xs font-medium tracking-wide text-ink-faint uppercase">
                Executive summary
              </p>
              <ArtifactMarkdown source={report.summary_md} sources={news?.sources} />
            </>
          )}
        </div>

        <div className="px-4 py-4">
          {reportMarkdown ? (
            <ArtifactMarkdown source={reportMarkdown} sources={news?.sources} />
          ) : report?.report_md ? (
            <ArtifactMarkdown source={report.report_md} sources={news?.sources} />
          ) : (
            <p className="text-sm text-ink-muted">
              No report body was written — only the structured fields below.
            </p>
          )}
        </div>

        {report?.thesis_update_md && (
          <div className="border-t border-line px-4 py-4">
            <p className="mb-2 text-xs font-medium tracking-wide text-ink-faint uppercase">
              How the thesis moves
            </p>
            <ArtifactMarkdown source={report.thesis_update_md} sources={news?.sources} />
          </div>
        )}
      </Card>

      {(findings.length > 0 || scenarios.length > 0) && (
        <Card>
          <SectionHeading>Structured findings</SectionHeading>
          <div className="px-4 py-2">
            <WidgetContext.Provider value={{ sources }}>
              {findings.length > 0 && (
                <WidgetRenderer
                  widget={{
                    type: 'key-findings',
                    findings: findings.map((row) => ({
                      finding: row.finding ?? '',
                      confidence: row.confidence,
                      source_ids: row.source_ids,
                    })),
                  }}
                />
              )}
              {scenarios.length > 0 && (
                <WidgetRenderer
                  widget={{ type: 'scenario-table', scenarios, title: 'Scenario updates' }}
                />
              )}
            </WidgetContext.Provider>
          </div>
        </Card>
      )}

      {(report?.open_questions?.length || report?.next_queries?.length) && (
        <Card>
          <SectionHeading>What is still open</SectionHeading>
          <div className="grid gap-4 px-4 py-4 sm:grid-cols-2">
            {report.open_questions?.length ? (
              <div>
                <p className="mb-2 text-xs font-medium tracking-wide text-ink-faint uppercase">
                  Open questions
                </p>
                <ul className="space-y-1.5">
                  {report.open_questions.map((question) => (
                    <li key={question} className="flex gap-2 text-sm text-ink-muted">
                      <span aria-hidden="true" className="text-ink-faint">
                        ?
                      </span>
                      <span>{question}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ) : null}

            {report.next_queries?.length ? (
              <div>
                <p className="mb-2 text-xs font-medium tracking-wide text-ink-faint uppercase">
                  Suggested next cycle
                </p>
                <ul className="space-y-1.5">
                  {report.next_queries.map((next, index) => (
                    <li key={next.q ?? index} className="text-sm">
                      <span className="text-ink">{next.q}</span>
                      {next.rationale && (
                        <span className="block text-xs text-ink-faint">{next.rationale}</span>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            ) : null}
          </div>
        </Card>
      )}
    </div>
  )
}
