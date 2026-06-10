import { useCallback, useEffect, useState } from 'react'
import { Radio } from 'lucide-react'
import { CreateTopicForm } from './CreateTopicForm'
import { TopicCard } from './TopicCard'
import { EmptyState } from '@/components/ui/EmptyState'
import { CardSkeleton } from '@/components/ui/Skeleton'
import { useSettings } from '@/context/SettingsContext'
import { createTopic, getMonitor, listDeltas, listTopics } from '@/lib/api'
import type { TopicSummary } from '@/lib/types'

interface TopicMeta {
  monitorActive: boolean
  latestDeltaAt: string | null
}

export function TopicList() {
  const { settings } = useSettings()
  const [topics, setTopics] = useState<TopicSummary[]>([])
  const [meta, setMeta] = useState<Record<string, TopicMeta>>({})
  const [loading, setLoading] = useState(true)
  const [creating, setCreating] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const loadTopics = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const { items } = await listTopics(settings)
      setTopics(items)

      const metaMap: Record<string, TopicMeta> = {}
      await Promise.all(
        items
          .filter((t) => t.state === 'reported')
          .map(async (t) => {
            try {
              const [mon, deltas] = await Promise.all([
                getMonitor(settings, t.id),
                listDeltas(settings, t.id),
              ])
              metaMap[t.id] = {
                monitorActive: mon?.status === 'active',
                latestDeltaAt: deltas.deltas[0]?.created_at ?? null,
              }
            } catch {
              metaMap[t.id] = { monitorActive: false, latestDeltaAt: null }
            }
          }),
      )
      setMeta(metaMap)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load topics')
    } finally {
      setLoading(false)
    }
  }, [settings])

  useEffect(() => {
    void loadTopics()
  }, [loadTopics])

  const handleCreate = async (topic: string) => {
    setCreating(true)
    try {
      await createTopic(settings, topic)
      await loadTopics()
    } finally {
      setCreating(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-text">Topics</h1>
          <p className="text-sm text-text-muted mt-1">
            Natural-language intelligence pipelines for your trading desk
          </p>
        </div>
        <CreateTopicForm onSubmit={handleCreate} loading={creating} />
      </div>

      {error && (
        <div className="rounded-lg border border-danger/30 bg-danger/10 px-4 py-3 text-sm text-danger">
          {error}
          <button
            onClick={() => void loadTopics()}
            className="ml-2 underline hover:no-underline"
          >
            Retry
          </button>
        </div>
      )}

      {loading ? (
        <div className="grid gap-3 sm:grid-cols-2">
          {Array.from({ length: 4 }).map((_, i) => (
            <CardSkeleton key={i} />
          ))}
        </div>
      ) : topics.length === 0 ? (
        <EmptyState
          icon={Radio}
          title="No topics yet"
          description="Create your first topic to start an intelligence pipeline. Describe your trading focus in natural language — the system will plan searches, gather sources, and produce a strategic report."
          action={<CreateTopicForm onSubmit={handleCreate} loading={creating} />}
        />
      ) : (
        <div className="grid gap-3 sm:grid-cols-2">
          {topics.map((topic) => (
            <TopicCard
              key={topic.id}
              topic={topic}
              monitorActive={meta[topic.id]?.monitorActive}
              latestDeltaAt={meta[topic.id]?.latestDeltaAt}
            />
          ))}
        </div>
      )}
    </div>
  )
}
