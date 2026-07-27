/**
 * Widget contract for adaptive artifact rendering (#16b).
 *
 * The agent decides how a block of its output is presented; the frontend only
 * owns the registry of renderable types. Adding a presentation to a report means
 * the agent emits a new widget and we add one entry to the registry — never a
 * new branch in the report screen.
 *
 * Why not `markdown-ui` (blueprintlab): its widget set is closed (hard-coded
 * `typeMapping` over a static import, no registration API) and covers chat forms
 * and quizzes, not report presentation; it also renders without sanitization.
 * See `docs/specs/active/signalgather_frontend_v1_16.md` → "16b".
 *
 * The fence name `markdown-ui-widget` is kept deliberately so their widgets stay
 * adoptable later. We deviate on the body: JSON rather than their positional
 * DSL, because an LLM emits valid JSON far more reliably than a bespoke
 * quoted-positional grammar, and it validates cleanly.
 */

export interface EntityChipsWidget {
  type: 'entity-chips'
  items: string[]
  label?: string
}

export interface HighlightsWidget {
  type: 'highlights'
  items: string[]
  title?: string
}

/** Renders one source from news.json in full. Resolved through WidgetContext. */
export interface NewsCardWidget {
  type: 'news-card'
  sourceId: string
}

/** Omit sourceIds to show every source the artifact carries. */
export interface SourceListWidget {
  type: 'source-list'
  sourceIds?: string[]
  title?: string
}

export interface KeyFindingsWidget {
  type: 'key-findings'
  findings: {
    finding: string
    confidence?: 'high' | 'medium' | 'low' | string
    source_ids?: string[]
  }[]
  title?: string
}

export interface ScenarioTableWidget {
  type: 'scenario-table'
  scenarios: {
    id?: string
    label?: string
    premise?: string
    rationale?: string
    p_before?: number
    p_after?: number
    verdict?: 'supports' | 'weakens' | 'kills' | 'neutral' | string
    evidence_ids?: string[]
  }[]
  title?: string
}

export interface CalloutWidget {
  type: 'callout'
  tone?: 'info' | 'good' | 'warn' | 'risk' | string
  title?: string
  body: string
}

export interface MetricsWidget {
  type: 'metrics'
  items: { label: string; value: string | number; hint?: string }[]
}

export type WidgetSpec =
  | EntityChipsWidget
  | HighlightsWidget
  | NewsCardWidget
  | SourceListWidget
  | KeyFindingsWidget
  | ScenarioTableWidget
  | CalloutWidget
  | MetricsWidget

export type WidgetType = WidgetSpec['type']

/**
 * A widget the registry does not know, or one whose payload failed validation.
 * Kept as a value rather than dropped: an agent shipping ahead of the frontend
 * must degrade visibly, not silently lose a section of the report.
 */
export interface UnknownWidget {
  type: 'unknown'
  declaredType: string
  raw: string
  reason: string
}

export type AnyWidget = WidgetSpec | UnknownWidget

/** One piece of an artifact: prose to render as markdown, or a widget. */
export type ArtifactSegment =
  | { kind: 'markdown'; text: string }
  | { kind: 'widget'; widget: AnyWidget }

/** A source from news.json, as the widgets need it. */
export interface SourceRef {
  id: string
  url?: string
  title?: string
  publisher?: string
  published_at?: string | null
  language?: string
  snippet?: string
  source_class?: string
  relevance_score?: number
  novelty_score?: number
  query_ids?: string[]
}
