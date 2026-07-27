/**
 * Split an agent-written artifact into prose and widgets.
 *
 * Two input forms are accepted:
 *
 * 1. **Current contract** — a fenced block:
 *
 *        ```markdown-ui-widget
 *        {"type": "entity-chips", "items": ["NIOC", "OPEC"]}
 *        ```
 *
 * 2. **Legacy tags** that shipped artifacts already contain, because
 *    `newsfind-plan.md` / `newsfind-deliver.md` asked for them before the widget
 *    contract existed: `<EntityChips>`, `<Highlights>`, `<NewsCard source-id/>`.
 *    Reports already on disk must keep rendering, so these are mapped onto the
 *    same registry rather than dropped.
 *
 * Validation is per type and total: a widget whose payload does not match its
 * declared shape becomes an `unknown` widget carrying the reason, so a
 * prompt/frontend version skew is visible instead of silently blank.
 */

import type { AnyWidget, ArtifactSegment, WidgetSpec } from './types'

const FENCE = /^[ \t]*(?:```|~~~)[ \t]*markdown-ui-widget[ \t]*\n([\s\S]*?)^[ \t]*(?:```|~~~)[ \t]*$/gm

/** Block-level legacy tags: `<Tag ...>text</Tag>` or `<Tag ... />` alone on a line. */
const LEGACY_BLOCK = /^[ \t]*<(EntityChips|Highlights|NewsCard)\b([^>]*?)(?:\/>|>([\s\S]*?)<\/\1>)[ \t]*$/gim

/** Inline `<NewsCard source-id="s01"/>` — degraded to a citation, never dropped. */
const INLINE_NEWSCARD = /<NewsCard\b[^>]*?source-id\s*=\s*["']([^"']+)["'][^>]*?\/?>/gi

export function parseArtifact(markdown: string): ArtifactSegment[] {
  const source = inlineNewsCardsToCitations(markdown)
  const found: { start: number; end: number; widget: AnyWidget }[] = []

  for (const match of source.matchAll(FENCE)) {
    found.push({
      start: match.index,
      end: match.index + match[0].length,
      widget: fromJson(match[1] ?? ''),
    })
  }

  for (const match of source.matchAll(LEGACY_BLOCK)) {
    // A legacy tag inside a fenced widget would double-count; fences win.
    if (found.some((f) => match.index >= f.start && match.index < f.end)) continue
    found.push({
      start: match.index,
      end: match.index + match[0].length,
      widget: fromLegacyTag(match[1] ?? '', match[2] ?? '', match[3] ?? '', match[0]),
    })
  }

  found.sort((a, b) => a.start - b.start)

  const segments: ArtifactSegment[] = []
  let cursor = 0
  for (const item of found) {
    pushMarkdown(segments, source.slice(cursor, item.start))
    segments.push({ kind: 'widget', widget: item.widget })
    cursor = item.end
  }
  pushMarkdown(segments, source.slice(cursor))
  return segments
}

function pushMarkdown(segments: ArtifactSegment[], text: string): void {
  if (text.trim()) segments.push({ kind: 'markdown', text })
}

/**
 * An inline NewsCard cannot become a block widget without breaking the
 * paragraph it sits in, so it becomes the citation it stands for. The source is
 * still reachable — nothing is lost but the card styling.
 */
function inlineNewsCardsToCitations(markdown: string): string {
  return markdown.replace(
    INLINE_NEWSCARD,
    (whole, sourceId: string, offset: number, full: string) => {
      const lineStart = full.lastIndexOf('\n', offset - 1) + 1
      const lineEnd = full.indexOf('\n', offset)
      const line = full.slice(lineStart, lineEnd === -1 ? full.length : lineEnd)
      // Alone on its line? Leave it for the block matcher to render as a card.
      return line.trim() === whole.trim() ? whole : `[${sourceId}]`
    },
  )
}

function fromJson(body: string): AnyWidget {
  const raw = body.trim()
  let parsed: unknown
  try {
    parsed = JSON.parse(raw)
  } catch (err) {
    return unknown('', raw, `payload is not valid JSON: ${(err as Error).message}`)
  }
  if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) {
    return unknown('', raw, 'payload is not a JSON object')
  }
  const declared = (parsed as { type?: unknown }).type
  if (typeof declared !== 'string' || !declared) {
    return unknown('', raw, 'payload has no "type"')
  }
  return validate(declared, parsed as Record<string, unknown>, raw)
}

function fromLegacyTag(tag: string, attrs: string, inner: string, raw: string): AnyWidget {
  const name = tag.toLowerCase()
  if (name === 'newscard') {
    const sourceId = attr(attrs, 'source-id') ?? attr(attrs, 'sourceId')
    return sourceId
      ? { type: 'news-card', sourceId }
      : unknown('NewsCard', raw, 'missing source-id')
  }

  // <EntityChips entities="a, b"/> and <EntityChips>a, b</EntityChips> both occur.
  const listAttr = name === 'entitychips' ? attr(attrs, 'entities') : attr(attrs, 'items')
  const items = splitList(listAttr ?? inner)
  if (items.length === 0) return unknown(tag, raw, 'no items')
  return name === 'entitychips'
    ? { type: 'entity-chips', items }
    : { type: 'highlights', items }
}

function attr(attrs: string, name: string): string | undefined {
  const match = new RegExp(`${name}\\s*=\\s*["']([^"']*)["']`, 'i').exec(attrs)
  return match?.[1]?.trim() || undefined
}

/** Legacy tag bodies are comma-, newline-, or bullet-separated. */
function splitList(value: string): string[] {
  return value
    .split(/[\n,]+/)
    .map((part) => part.replace(/^[\s*\-•]+/, '').trim())
    .filter(Boolean)
}

function unknown(declaredType: string, raw: string, reason: string): AnyWidget {
  return { type: 'unknown', declaredType, raw, reason }
}

// ---- per-type validation ---------------------------------------------------

function strings(value: unknown): string[] | null {
  if (!Array.isArray(value)) return null
  const out = value.filter((item): item is string => typeof item === 'string' && item.trim() !== '')
  return out.length === value.length ? out : null
}

function objects(value: unknown): Record<string, unknown>[] | null {
  if (!Array.isArray(value)) return null
  return value.every((item) => typeof item === 'object' && item !== null && !Array.isArray(item))
    ? (value as Record<string, unknown>[])
    : null
}

function optionalString(value: unknown): string | undefined {
  return typeof value === 'string' && value.trim() !== '' ? value : undefined
}

function validate(declared: string, body: Record<string, unknown>, raw: string): AnyWidget {
  switch (declared) {
    case 'entity-chips': {
      const items = strings(body.items)
      return items
        ? ({ type: 'entity-chips', items, label: optionalString(body.label) } as WidgetSpec)
        : unknown(declared, raw, '"items" must be an array of non-empty strings')
    }

    case 'highlights': {
      const items = strings(body.items)
      return items
        ? ({ type: 'highlights', items, title: optionalString(body.title) } as WidgetSpec)
        : unknown(declared, raw, '"items" must be an array of non-empty strings')
    }

    case 'news-card': {
      const sourceId = optionalString(body.sourceId) ?? optionalString(body.source_id)
      return sourceId
        ? ({ type: 'news-card', sourceId } as WidgetSpec)
        : unknown(declared, raw, '"sourceId" is required')
    }

    case 'source-list': {
      const ids = body.sourceIds ?? body.source_ids
      const sourceIds = ids === undefined ? undefined : (strings(ids) ?? undefined)
      if (ids !== undefined && sourceIds === undefined) {
        return unknown(declared, raw, '"sourceIds" must be an array of strings')
      }
      return { type: 'source-list', sourceIds, title: optionalString(body.title) } as WidgetSpec
    }

    case 'key-findings': {
      const rows = objects(body.findings)
      if (!rows) return unknown(declared, raw, '"findings" must be an array of objects')
      const findings = rows
        .map((row) => ({
          finding: optionalString(row.finding) ?? '',
          confidence: optionalString(row.confidence),
          source_ids: strings(row.source_ids) ?? undefined,
        }))
        .filter((row) => row.finding !== '')
      return findings.length
        ? ({ type: 'key-findings', findings, title: optionalString(body.title) } as WidgetSpec)
        : unknown(declared, raw, 'no finding had a non-empty "finding"')
    }

    case 'scenario-table': {
      const rows = objects(body.scenarios)
      if (!rows) return unknown(declared, raw, '"scenarios" must be an array of objects')
      return {
        type: 'scenario-table',
        title: optionalString(body.title),
        scenarios: rows.map((row) => ({
          id: optionalString(row.id),
          label: optionalString(row.label),
          premise: optionalString(row.premise),
          rationale: optionalString(row.rationale),
          p_before: typeof row.p_before === 'number' ? row.p_before : undefined,
          p_after: typeof row.p_after === 'number' ? row.p_after : undefined,
          verdict: optionalString(row.verdict),
          evidence_ids: strings(row.evidence_ids) ?? undefined,
        })),
      } as WidgetSpec
    }

    case 'callout': {
      const text = optionalString(body.body) ?? optionalString(body.text)
      return text
        ? ({
            type: 'callout',
            body: text,
            tone: optionalString(body.tone),
            title: optionalString(body.title),
          } as WidgetSpec)
        : unknown(declared, raw, '"body" is required')
    }

    case 'metrics': {
      const rows = objects(body.items)
      if (!rows) return unknown(declared, raw, '"items" must be an array of objects')
      const items = rows
        .map((row) => ({
          label: optionalString(row.label) ?? '',
          value: typeof row.value === 'number' ? row.value : (optionalString(row.value) ?? ''),
          hint: optionalString(row.hint),
        }))
        .filter((row) => row.label !== '' && row.value !== '')
      return items.length
        ? ({ type: 'metrics', items } as WidgetSpec)
        : unknown(declared, raw, 'no item had both a label and a value')
    }

    default:
      return unknown(declared, raw, 'no renderer is registered for this widget type')
  }
}
