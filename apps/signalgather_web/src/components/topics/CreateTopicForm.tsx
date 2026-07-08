import { useState } from 'react'
import { Plus } from 'lucide-react'
import { Button } from '@/components/ui/Button'

const EXAMPLE =
  'I primarily trade European gas and LNG. Monitor geopolitical risks to supply through the Strait of Hormuz and their impact on TTF and JKM spreads.'

export function CreateTopicForm({
  onSubmit,
  loading,
}: {
  onSubmit: (topic: string) => Promise<void>
  loading?: boolean
}) {
  const [topic, setTopic] = useState('')
  const [expanded, setExpanded] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!topic.trim()) return
    await onSubmit(topic.trim())
    setTopic('')
    setExpanded(false)
  }

  if (!expanded) {
    return (
      <Button onClick={() => setExpanded(true)} className="w-full sm:w-auto">
        <Plus className="h-4 w-4" />
        New Topic
      </Button>
    )
  }

  return (
    <form
      onSubmit={(e) => void handleSubmit(e)}
      className="rounded-xl border border-border bg-surface-raised p-4 space-y-3"
    >
      <label className="block text-sm font-medium text-text">
        Describe your trading topic
      </label>
      <textarea
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        placeholder={EXAMPLE}
        rows={4}
        autoFocus
        className="w-full rounded-lg border border-border bg-surface px-3 py-2.5 text-sm text-text placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-accent/40 resize-y min-h-[100px]"
      />
      <div className="flex flex-wrap gap-2 justify-end">
        <Button
          type="button"
          variant="ghost"
          size="sm"
          onClick={() => {
            setExpanded(false)
            setTopic('')
          }}
        >
          Cancel
        </Button>
        <Button type="submit" size="sm" loading={loading} disabled={!topic.trim()}>
          Start Planning
        </Button>
      </div>
    </form>
  )
}
