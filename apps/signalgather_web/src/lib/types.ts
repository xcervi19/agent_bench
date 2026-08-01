/**
 * Shapes returned by the claude_agent topic API.
 *
 * Sources of truth:
 *   - routes:     apps/claude_agent/topics/routes.py
 *   - artifacts:  claude_agent_fe/.claude/commands/newsfind-plan.md
 *   - events:     apps/claude_agent/topics/pipeline.py (`emit(...)`)
 *
 * Artifacts are written by an agent, so every field beyond the ones the
 * orchestrator itself validates is treated as optional here — the UI degrades
 * instead of throwing when a run produced a thinner document than expected.
 */

import type { SourceRef } from './widgets/types'

export type { SourceRef }

export const TOPIC_STATES = [
  'planning',
  'planned_awaiting_review',
  'delivering',
  'reported',
  'failed',
  'cancelled',
] as const

export type TopicState = (typeof TOPIC_STATES)[number]

/** States after which no further pipeline work happens on its own. */
export const TERMINAL_STATES: readonly TopicState[] = ['reported', 'failed', 'cancelled']

export type TopicAction = 'proceed' | 'cancel'

export interface TopicListItem {
  id: string
  topic: string
  state: TopicState
  available_actions: TopicAction[]
  last_event_seq: number
  created_at: string
  updated_at: string
  /** Sharing (#40). Published topics are world-readable and frozen. */
  is_public: boolean
  published_at: string | null
  /** API path anyone can read while published; null when private. */
  public_path: string | null
}

export interface TopicListResponse {
  items: TopicListItem[]
  count: number
  limit: number
  offset: number
  state: string | null
}

export interface TopicDetail extends TopicListItem {
  plan_run_id: string | null
  deliver_run_id: string | null
  error: string | null
}

export interface CreateTopicResponse {
  topic_id: string
  state: TopicState
  events_url: string
}

// ---- sharing (#40) ---------------------------------------------------------

export interface ShareState {
  is_public: boolean
  published_at: string | null
  public_path: string | null
}

export interface PublishResponse extends ShareState {
  already_published?: boolean
  already_private?: boolean
  /** Publishing pauses monitoring — the UI says so rather than letting it surprise. */
  monitoring_paused?: boolean
}

/**
 * A published topic as an anonymous reader sees it: no owner, no run ids, no
 * `available_actions` — there are none. `GET /v1/public/topics[/{id}]`.
 */
export interface PublicTopic {
  id: string
  topic: string
  state: TopicState
  published_at: string | null
  created_at: string
  updated_at: string
  read_only: true
  has_plan: boolean
  has_report: boolean
}

export interface PublicTopicListResponse {
  items: PublicTopic[]
  count: number
  limit: number
  offset: number
  q: string | null
}

// ---- events ---------------------------------------------------------------

export type TopicEventType =
  | 'topic.created'
  | 'state.changed'
  | 'stage.started'
  | 'stage.finished'
  | 'tool_use'
  | 'tool_result'
  | 'intro.ready'
  | 'needs_input'
  | 'report.ready'
  | 'error'
  | 'monitor.started'
  | 'monitor.updated'
  | 'monitor.stopped'
  | 'refresh.started'
  | 'refresh.completed'
  | 'refresh.failed'
  | 'refresh.skipped'
  | 'topic.published'
  | 'topic.unpublished'

export interface TopicEvent {
  seq: number
  event_type: TopicEventType | string
  topic_id: string
  payload: Record<string, unknown>
}

// ---- artifacts ------------------------------------------------------------

export interface IntroArtifact {
  schema_version?: string
  topic_id?: string
  headline?: string
  understanding?: string
  current_state_short?: string
  working_thesis_short?: string
  approach?: {
    queries_count?: number
    languages?: string[]
    regions?: string[]
    key_actors_top5?: string[]
  }
  highlights?: string[]
  next_step?: string
}

export interface PlannedQuery {
  id?: string
  query?: string
  intent?: 'monitoring' | 'context' | string
  source_class?: string
  language?: string
  region?: string
  freshness?: '24h' | '7d' | '30d' | 'any' | string
  priority?: number
  covers_entity?: string[]
  rationale?: string
}

/** news.json — searched sources + dedup stats (`newsfind-deliver.md` phase 3). */
export interface NewsArtifact {
  schema_version?: string
  topic_id?: string
  executed_queries?: { id?: string; query?: string; results_count?: number; error?: string }[]
  sources?: SourceRef[]
  drops?: { deduped?: number; low_relevance?: number; off_topic?: number }
  search_budget_used?: {
    queries_executed?: number
    web_searches?: number
    web_fetches?: number
  }
}

export type ThesisStatus =
  | 'supported'
  | 'weakened'
  | 'invalidated'
  | 'inconclusive'
  | 'unchanged'

/** report.json — the synthesis (`newsfind-deliver.md` phase 4). */
export interface ReportArtifact {
  schema_version?: string
  topic_id?: string
  summary_md?: string
  report_md?: string
  key_findings?: {
    finding?: string
    confidence?: 'high' | 'medium' | 'low' | string
    source_ids?: string[]
  }[]
  scenario_updates?: {
    id?: string
    label?: string
    p_before?: number
    p_after?: number
    rationale?: string
    evidence_ids?: string[]
    verdict?: 'supports' | 'weakens' | 'kills' | 'neutral' | string
  }[]
  thesis_status?: ThesisStatus | string
  thesis_update_md?: string
  open_questions?: string[]
  next_queries?: { q?: string; intent?: string; rationale?: string }[]
}

// ---- monitoring (16c) ------------------------------------------------------

export interface MonitorState {
  subscription_id: number
  status: 'active' | 'paused' | string
  max_age_hours: number
  refresh_count: number
  refresh_locked: boolean
  schedule_enabled: boolean
  schedule_interval_hours: number | null
  next_refresh_at: string | null
  last_refresh_at: string | null
  last_scheduled_refresh_at: string | null
  last_refresh_run_id: string | null
  short_term_queries?: PlannedQuery[]
  queries_count?: number
}

/** One row of `GET /v1/topics/{id}/deltas`. */
export interface DeltaSummary {
  seq: number
  run_id: string
  status: string
  new_sources_count: number | null
  queries_executed: number | null
  duration_ms: number | null
  total_cost_usd: number | null
  summary_md: string | null
  error: string | null
  created_at: string
}

/** delta.json — what actually changed in one refresh cycle. */
export interface DeltaArtifact {
  schema_version?: string
  topic_id?: string
  refresh_run_id?: string
  since_iso?: string | null
  today_iso?: string
  summary_md?: string
  new_sources?: string[]
  trigger_terms_hit?: string[]
  thesis_status?: ThesisStatus | string
  key_changes?: { finding?: string; source_ids?: string[]; confidence?: string }[]
}

export interface ParsedArtifact {
  schema_version?: string
  topic?: string
  topic_restated?: string
  domain?: string
  current_state?: string
  working_thesis?: string
  entities?: {
    actors?: string[]
    regions?: string[]
    primary_languages?: string[]
  }
  scenarios?: { id?: string; label?: string; premise?: string; probability?: number }[]
  source_targets?: { entity?: string; known_domains?: string[]; playbook_refs?: string[] }[]
  queries?: PlannedQuery[]
  monitoring_plan?: { trigger_terms?: string[]; cadence?: string }
}
