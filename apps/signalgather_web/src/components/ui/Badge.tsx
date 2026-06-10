import { cn } from '@/lib/utils'
import type { TopicState } from '@/lib/types'
import { STATE_COLORS, STATE_LABELS } from '@/lib/types'

export function Badge({
  className,
  children,
}: {
  className?: string
  children: React.ReactNode
}) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-medium',
        className,
      )}
    >
      {children}
    </span>
  )
}

export function StateBadge({ state }: { state: TopicState }) {
  return <Badge className={STATE_COLORS[state]}>{STATE_LABELS[state]}</Badge>
}
