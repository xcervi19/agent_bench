export type TopicState =
  | 'planning'
  | 'planned_awaiting_review'
  | 'delivering'
  | 'reported'
  | 'failed'
  | 'cancelled'

export type ApiEnvironment = 'local' | 'test1' | 'test2' | 'prod' | 'custom'

export interface TopicSummary {
  id: string
  topic: string
  state: TopicState
  available_actions: string[]
  last_event_seq: number
  created_at: string
  updated_at: string
}

export interface TopicDetail extends TopicSummary {
  plan_run_id: string | null
  deliver_run_id: string | null
  error: string | null
}

export interface TopicEvent {
  seq: number
  event_type: string
  topic_id: string
  payload: Record<string, unknown>
}

export interface QueryPlan {
  topic_restated?: string
  working_thesis?: string
  queries?: Array<{
    id: string
    query: string
    language: string
    intent?: string
    priority?: string | number
  }>
  entities?: Record<string, unknown>
  monitoring_plan?: Record<string, unknown>
  rag_context_refs?: Array<{ source: string; source_id: string; score: number }>
}

export interface NewsSource {
  id: string
  url: string
  url_hash?: string
  title: string
  publisher?: string
  published_at?: string
  language?: string
  snippet?: string
  relevance_score?: number
  novelty_score?: number
  source_class?: string
  query_ids?: string[]
}

export interface NewsArtifact {
  sources: NewsSource[]
  executed_queries?: Array<{ id: string; query: string; results_count: number }>
  drops?: Record<string, number>
  search_budget_used?: Record<string, number>
}

export interface ReportArtifact {
  thesis_status?: string
  thesis_update_md?: string
  summary_md?: string
  key_findings?: Array<{
    finding: string
    confidence?: string
    source_ids?: string[]
  }>
  scenarios?: Array<{
    name: string
    probability?: string
    summary?: string
  }>
  open_questions?: string[]
  next_queries?: string[]
}

export interface MonitorStatus {
  subscription_id: number
  status: 'active' | 'paused'
  max_age_hours: number
  refresh_count: number
  refresh_locked: boolean
  last_refresh_at: string | null
  last_refresh_run_id: string | null
  short_term_queries: Array<Record<string, unknown>>
}

export interface DeltaSummary {
  seq: number
  run_id: string
  status: string
  new_sources_count: number
  queries_executed: number
  duration_ms: number | null
  total_cost_usd: number | null
  summary_md: string | null
  created_at: string
}

export interface DeltaDetail {
  new_sources?: NewsSource[]
  summary_md?: string
  thesis_status?: string
  [key: string]: unknown
}

export interface AppSettings {
  apiKey: string
  environment: ApiEnvironment
  customBaseUrl: string
  theme: 'dark' | 'light' | 'system'
}

export const API_ENVIRONMENTS: Record<Exclude<ApiEnvironment, 'custom'>, string> = {
  local: 'http://localhost:8002',
  test1: 'https://agent-test1.particletico.com',
  test2: 'https://agent-test2.particletico.com',
  prod: 'https://agent.particletico.com',
}

export const STATE_LABELS: Record<TopicState, string> = {
  planning: 'Planning',
  planned_awaiting_review: 'Awaiting Review',
  delivering: 'Delivering',
  reported: 'Reported',
  failed: 'Failed',
  cancelled: 'Cancelled',
}

export const STATE_COLORS: Record<TopicState, string> = {
  planning: 'bg-info/20 text-info border-info/30',
  planned_awaiting_review: 'bg-warning/20 text-warning border-warning/30',
  delivering: 'bg-accent/20 text-accent border-accent/30',
  reported: 'bg-success/20 text-success border-success/30',
  failed: 'bg-danger/20 text-danger border-danger/30',
  cancelled: 'bg-text-muted/20 text-text-muted border-border',
}
