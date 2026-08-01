/**
 * Turn a raw topic event into one scannable line.
 *
 * The activity feed is the user's window into a long agent run, so every event
 * type the pipeline emits gets a human phrasing here; unknown types fall back to
 * their wire name rather than disappearing.
 */

import { formatDuration, formatUsd } from './format'
import type { TopicEvent } from './types'

export type EventTone = 'neutral' | 'active' | 'good' | 'warn' | 'bad'

export interface EventLine {
  tone: EventTone
  title: string
  /** Secondary line — shown under the title when present. */
  detail?: string
  /** Long tool I/O, collapsed behind a disclosure. */
  expandable?: string
}

function str(payload: Record<string, unknown>, key: string): string | undefined {
  const value = payload[key]
  return typeof value === 'string' && value.trim() ? value : undefined
}

const STAGE_LABELS: Record<string, string> = {
  source_discover: 'Finding trusted sources',
  plan: 'Building the query plan',
  deliver: 'Searching and writing the report',
}

function stageLabel(stage: string | undefined): string {
  if (!stage) return 'stage'
  return STAGE_LABELS[stage] ?? stage
}

export function describeEvent(event: TopicEvent): EventLine {
  const p = event.payload ?? {}

  switch (event.event_type) {
    case 'topic.created':
      return { tone: 'neutral', title: 'Topic created', detail: str(p, 'topic') }

    case 'state.changed': {
      const to = str(p, 'to') ?? '?'
      const from = str(p, 'from')
      return {
        tone: to === 'failed' ? 'bad' : to === 'reported' ? 'good' : 'neutral',
        title: `State → ${to}`,
        detail: from ? `from ${from}${str(p, 'error') ? ` · ${str(p, 'error')}` : ''}` : undefined,
      }
    }

    case 'stage.started':
      return { tone: 'active', title: stageLabel(str(p, 'stage')) }

    case 'stage.finished': {
      const bits = [formatDuration(p.duration_ms), formatUsd(p.total_cost_usd)].filter(Boolean)
      const entities = typeof p.entities === 'number' ? `${p.entities} entities` : null
      if (entities) bits.unshift(entities)
      return {
        tone: 'good',
        title: `${stageLabel(str(p, 'stage'))} — done`,
        detail: bits.length ? bits.join(' · ') : undefined,
      }
    }

    case 'tool_use':
      return {
        tone: 'neutral',
        title: str(p, 'tool') ?? 'tool',
        expandable: str(p, 'input_preview'),
      }

    case 'tool_result':
      return {
        tone: p.is_error ? 'warn' : 'neutral',
        title: p.is_error ? 'Tool error' : 'Tool result',
        expandable: str(p, 'output_preview'),
      }

    case 'intro.ready':
      return {
        tone: 'good',
        title: 'Plan ready for review',
        detail: str(p, 'headline') ?? str(p, 'understanding'),
      }

    case 'needs_input':
      return { tone: 'warn', title: 'Waiting for you to Proceed or Cancel' }

    case 'report.ready':
      return { tone: 'good', title: 'Report ready', detail: str(p, 'headline') }

    case 'error':
      return {
        tone: 'bad',
        title: `Error in ${stageLabel(str(p, 'stage'))}`,
        detail: str(p, 'error'),
      }

    case 'monitor.started':
      return { tone: 'good', title: 'Monitoring enabled' }
    case 'monitor.updated':
      return { tone: 'neutral', title: 'Monitoring settings updated' }
    case 'monitor.stopped':
      return { tone: 'neutral', title: 'Monitoring paused' }

    case 'refresh.started':
      return { tone: 'active', title: 'Refresh started', detail: str(p, 'trigger') }
    case 'refresh.completed':
      return { tone: 'good', title: 'Refresh completed' }
    case 'refresh.failed':
      return { tone: 'bad', title: 'Refresh failed', detail: str(p, 'error') }
    case 'refresh.skipped':
      return { tone: 'neutral', title: 'Refresh skipped', detail: str(p, 'reason') }

    case 'topic.published':
      return {
        tone: 'good',
        title: 'Shared publicly',
        detail: p.monitoring_paused ? 'Monitoring paused; the topic is now read-only.' : undefined,
      }
    case 'topic.unpublished':
      return { tone: 'neutral', title: 'Sharing stopped' }

    default:
      return { tone: 'neutral', title: event.event_type }
  }
}
