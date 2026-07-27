import { afterEach, describe, expect, it } from 'vitest'
import { cleanup, render, screen } from '@testing-library/react'
import { ReportView } from './ReportView'
import { SourcesPanel } from './SourcesPanel'
import type { NewsArtifact, ReportArtifact } from '../../lib/types'

const NEWS: NewsArtifact = {
  sources: [
    {
      id: 's01',
      title: 'Tanker traffic halves',
      publisher: 'Reuters',
      url: 'https://example.com/1',
      source_class: 'primary_official',
      relevance_score: 0.83,
      published_at: '2026-07-25T08:00:00+00:00',
    },
    {
      id: 's02',
      title: 'Analyst note',
      publisher: 'A Blog',
      source_class: 'blog_or_newsletter',
      relevance_score: 0.41,
      published_at: '2026-07-26T08:00:00+00:00',
    },
  ],
  drops: { deduped: 4, low_relevance: 2 },
  search_budget_used: { queries_executed: 13, web_searches: 13, web_fetches: 4 },
}

const REPORT: ReportArtifact = {
  summary_md: 'Traffic through the strait fell sharply [s01].',
  thesis_status: 'weakened',
  thesis_update_md: 'The bypass assumption no longer holds.',
  key_findings: [{ finding: 'Exports down 12%', confidence: 'high', source_ids: ['s01'] }],
  scenario_updates: [{ label: 'Full closure', p_before: 0.2, p_after: 0.35, verdict: 'supports' }],
  open_questions: ['Will OPEC respond?'],
  next_queries: [{ q: 'OPEC emergency meeting', rationale: 'Watch for a supply answer' }],
}

afterEach(cleanup)

describe('ReportView', () => {
  it('shows a skeleton while the report is loading', () => {
    const { container } = render(
      <ReportView report={null} reportMarkdown={null} news={null} loading />,
    )
    expect(container.querySelector('.animate-pulse')).toBeTruthy()
  })

  it('says the artifacts are missing rather than rendering blank', () => {
    render(<ReportView report={null} reportMarkdown={null} news={null} loading={false} />)
    expect(screen.getByText(/not on disk for this run/)).toBeTruthy()
  })

  it('renders the report body and its thesis verdict', () => {
    render(
      <ReportView
        report={REPORT}
        reportMarkdown={'## Snapshot\n\nTraffic is down [s01].'}
        news={NEWS}
        loading={false}
      />,
    )
    expect(screen.getByRole('heading', { name: 'Snapshot' })).toBeTruthy()
    expect(screen.getByText('Thesis weakened')).toBeTruthy()
    expect(screen.getByText('The bypass assumption no longer holds.')).toBeTruthy()
  })

  it('links citations in the body to the sources', () => {
    const { container } = render(
      <ReportView
        report={REPORT}
        reportMarkdown="Traffic is down [s01]."
        news={NEWS}
        loading={false}
      />,
    )
    expect(container.querySelector('a.citation')?.getAttribute('href')).toBe('#src-s01')
  })

  it('renders structured findings and scenarios through the widget registry', () => {
    render(
      <ReportView report={REPORT} reportMarkdown={null} news={NEWS} loading={false} />,
    )
    expect(screen.getByText('Exports down 12%')).toBeTruthy()
    expect(screen.getByText('high confidence')).toBeTruthy()
    expect(screen.getByText('Full closure')).toBeTruthy()
    expect(screen.getByText('35%')).toBeTruthy()
  })

  it('shows open questions and the suggested next cycle', () => {
    render(<ReportView report={REPORT} reportMarkdown={null} news={NEWS} loading={false} />)
    expect(screen.getByText('Will OPEC respond?')).toBeTruthy()
    expect(screen.getByText('OPEC emergency meeting')).toBeTruthy()
  })

  it('falls back to report_md when report.md is absent', () => {
    render(
      <ReportView
        report={{ ...REPORT, report_md: '## From JSON' }}
        reportMarkdown={null}
        news={NEWS}
        loading={false}
      />,
    )
    expect(screen.getByRole('heading', { name: 'From JSON' })).toBeTruthy()
  })
})

describe('SourcesPanel', () => {
  it('says so when news.json is missing', () => {
    render(<SourcesPanel news={null} />)
    expect(screen.getByText(/is not on disk for this run/)).toBeTruthy()
  })

  it('lists sources with the counts in the heading', () => {
    render(<SourcesPanel news={NEWS} />)
    expect(screen.getByText(/Sources \(2\)/)).toBeTruthy()
    expect(screen.getByText('Tanker traffic halves')).toBeTruthy()
  })

  it('shows the search budget and drop counts', () => {
    render(<SourcesPanel news={NEWS} />)
    expect(screen.getByText(/13 queries executed/)).toBeTruthy()
    expect(screen.getByText(/4 deduped/)).toBeTruthy()
  })

  it('orders by relevance by default, matching the citation ids', () => {
    const { container } = render(<SourcesPanel news={NEWS} />)
    const titles = [...container.querySelectorAll('article')].map((a) =>
      a.textContent?.includes('Tanker') ? 's01' : 's02',
    )
    expect(titles).toEqual(['s01', 's02'])
  })

  it('gives each source an anchor a citation can jump to', () => {
    const { container } = render(<SourcesPanel news={NEWS} />)
    expect(container.querySelector('#src-s01')).toBeTruthy()
  })

  it('handles an empty source list without breaking', () => {
    render(<SourcesPanel news={{ sources: [] }} />)
    expect(screen.getByText('No sources')).toBeTruthy()
  })
})
